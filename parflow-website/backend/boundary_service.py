"""按全量缓存、流域 ID 或地图视野提供 PFBAS 边界。"""

import gzip
import json
import shutil
from pathlib import Path

import geopandas as gpd
from flask import current_app, jsonify, request, send_file
from pyproj import Transformer
from shapely.geometry import box, mapping

from boundary_query import parse_bbox, parse_boundary_ids


ADAPTIVE_TOLS = {
    12: (0.001, 0.002, 0.005),
    14: (0.001, 0.002, 0.005),
}
_SOURCE_CRS_CACHE = {}


def _cache_path(level, cache_dir):
    return Path(cache_dir) / f"PFBAS{level}.geojson"


def _shp_path(level, shp_dir):
    return Path(shp_dir) / f"PFBAS{level}.shp"


def _prepare_for_web(level, gdf):
    """将源 CRS 几何转为 WGS84，并沿用既有分级简化规则。"""
    if gdf.empty:
        return gdf.to_crs("EPSG:4326") if gdf.crs else gdf

    areas_m2 = None
    if gdf.crs is not None and gdf.crs.is_projected:
        areas_m2 = gdf.geometry.area
        gdf = gdf.to_crs("EPSG:4326")
    elif gdf.crs is not None:
        gdf = gdf.to_crs("EPSG:4326")

    simplify_tolerance = {10: 0.002}.get(level, 0)
    if simplify_tolerance > 0:
        gdf = gdf.copy()
        gdf["geometry"] = gdf.geometry.simplify(
            tolerance=simplify_tolerance,
            preserve_topology=True,
        )
    elif level in ADAPTIVE_TOLS and areas_m2 is not None:
        small_tol, medium_tol, large_tol = ADAPTIVE_TOLS[level]
        gdf = gdf.copy()
        gdf["geometry"] = [
            geometry.simplify(
                small_tol if area < 100e6 else (
                    medium_tol if area < 500e6 else large_tol
                ),
                preserve_topology=True,
            )
            for geometry, area in zip(gdf.geometry, areas_m2)
        ]
    return gdf


def _build_cache(level, shp_dir, cache_dir):
    """为允许全量访问的低等级构建 GeoJSON 和 gzip 缓存。"""
    shp = _shp_path(level, shp_dir)
    if not shp.exists():
        raise FileNotFoundError(f"未找到 SHP 文件: {shp}")

    gdf = _prepare_for_web(level, gpd.read_file(shp))
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = _cache_path(level, cache_dir)
    temporary_file = cache_file.with_name(f".{cache_file.name}.tmp.geojson")
    temporary_gzip = Path(f"{temporary_file}.gz")
    gzip_file = Path(f"{cache_file}.gz")

    gdf.to_file(temporary_file, driver="GeoJSON", encoding="utf-8")
    with temporary_file.open("rb") as source, gzip.open(
        temporary_gzip, "wb", compresslevel=1
    ) as target:
        shutil.copyfileobj(source, target)
    temporary_file.replace(cache_file)
    temporary_gzip.replace(gzip_file)
    current_app.logger.info("已生成 PFBAS%s 边界缓存，共 %s 个要素", level, len(gdf))


def _serve_full_cache(level, shp_dir, cache_dir):
    cache_file = _cache_path(level, cache_dir)
    if not cache_file.exists():
        _build_cache(level, shp_dir, cache_dir)

    use_gzip = "gzip" in request.headers.get("Accept-Encoding", "").lower()
    response_path = Path(f"{cache_file}.gz") if use_gzip else cache_file
    if use_gzip and not response_path.exists():
        _build_cache(level, shp_dir, cache_dir)

    response = send_file(
        response_path,
        mimetype="application/json",
        conditional=True,
        max_age=86400,
    )
    if use_gzip:
        response.headers["Content-Encoding"] = "gzip"
    response.headers["Vary"] = "Accept-Encoding"
    return response


def _source_bbox(shp, geographic_bbox):
    """把浏览器 EPSG:4326 bbox 转换为 SHP 原始坐标系。"""
    cache_key = str(Path(shp).resolve())
    source_crs = _SOURCE_CRS_CACHE.get(cache_key)
    if source_crs is None:
        info = gpd.read_file(shp, rows=1)
        source_crs = info.crs
        if source_crs is not None:
            _SOURCE_CRS_CACHE[cache_key] = source_crs
    if source_crs is None:
        raise ValueError(f"SHP 缺少 CRS: {shp}")
    transformer = Transformer.from_crs("EPSG:4326", source_crs, always_xy=True)
    return transformer.transform_bounds(*geographic_bbox, densify_pts=21)


def _read_subset(level, shp_dir, requested_ids=None, geographic_bbox=None):
    """在驱动读取阶段按属性/空间范围过滤，避免加载整个高等级 SHP。"""
    shp = _shp_path(level, shp_dir)
    if not shp.exists():
        raise FileNotFoundError(f"未找到 SHP 文件: {shp}")

    kwargs = {"columns": ["PFBAS_ID"]}
    if requested_ids:
        quoted_ids = ",".join(f"'{basin_id}'" for basin_id in requested_ids)
        kwargs["where"] = f'PFBAS_ID IN ({quoted_ids})'
    if geographic_bbox:
        kwargs["bbox"] = _source_bbox(shp, geographic_bbox)

    gdf = gpd.read_file(shp, **kwargs)
    if "PFBAS_ID" not in gdf.columns:
        raise ValueError(f"SHP 缺少 PFBAS_ID 字段: {shp}")

    # 驱动支持程度不一致时再次过滤，确保返回范围严格正确。
    if requested_ids:
        gdf = gdf[gdf["PFBAS_ID"].astype(str).isin(requested_ids)]
    gdf = _prepare_for_web(level, gdf[["PFBAS_ID", "geometry"]])
    if geographic_bbox and not gdf.empty:
        gdf = gdf[gdf.geometry.intersects(box(*geographic_bbox))]
    return gdf


def _feature_collection(gdf):
    features = []
    for _, row in gdf.iterrows():
        geometry = row.geometry
        if geometry is None or geometry.is_empty:
            continue
        bounds = [float(value) for value in geometry.bounds]
        features.append({
            "type": "Feature",
            "bbox": bounds,
            "properties": {"PFBAS_ID": str(row["PFBAS_ID"])},
            "geometry": mapping(geometry),
        })
    return {"type": "FeatureCollection", "features": features}


def get_boundaries():
    """处理全量低等级、按 ID 搜索和按 bbox 视野查询。"""
    level_str = request.args.get("level", "").strip()
    try:
        level = int(level_str)
    except ValueError:
        return jsonify({"error": "level 必须为整数"}), 400
    if level < 2 or level > 14 or level % 2:
        return jsonify({"error": "level 必须为 2~14 之间的偶数"}), 400

    try:
        requested_ids = parse_boundary_ids(
            request.args.get("ids", ""),
            current_app.config["MAX_BOUNDARY_IDS"],
        )
        geographic_bbox = parse_bbox(request.args.get("bbox", ""))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    shp_dir = current_app.config["SHP_DIR"]
    cache_dir = current_app.config["BOUNDARY_CACHE_DIR"]
    full_max_level = current_app.config["FULL_BOUNDARY_MAX_LEVEL"]

    try:
        if requested_ids or geographic_bbox:
            gdf = _read_subset(level, shp_dir, requested_ids, geographic_bbox)
            max_features = current_app.config["MAX_BOUNDARY_FEATURES"]
            if len(gdf) > max_features:
                return jsonify({
                    "error": f"当前视野包含 {len(gdf)} 个流域，请继续放大地图",
                    "featureCount": len(gdf),
                    "maxFeatures": max_features,
                }), 422
            result = _feature_collection(gdf)
            return current_app.response_class(
                json.dumps(result, ensure_ascii=False, separators=(",", ":")),
                mimetype="application/json",
                headers={"Cache-Control": "private, max-age=60"},
            )

        if level > full_max_level:
            return jsonify({
                "error": (
                    f"PFBAS{level} 不支持全国全量加载，请提供 ids 或 bbox 参数"
                )
            }), 400
        return _serve_full_cache(level, shp_dir, cache_dir)
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception:
        current_app.logger.exception("获取 PFBAS%s 边界失败", level)
        return jsonify({"error": "获取边界数据失败，请联系管理员查看服务日志"}), 500
