"""边界接口查询参数的纯函数校验。"""

import re


BASIN_ID_PATTERN = re.compile(r"^\d{14}$")


def parse_boundary_ids(value, max_ids=200):
    if not value or not value.strip():
        return None
    ids = list(dict.fromkeys(part.strip() for part in value.split(",") if part.strip()))
    if not ids:
        return None
    if len(ids) > max_ids:
        raise ValueError(f"一次最多查询 {max_ids} 个流域边界")
    invalid = [basin_id for basin_id in ids if not BASIN_ID_PATTERN.fullmatch(basin_id)]
    if invalid:
        raise ValueError(f"流域编号必须是14位数字: {invalid}")
    return ids


def parse_bbox(value):
    if not value or not value.strip():
        return None
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4:
        raise ValueError("bbox 必须是 minLng,minLat,maxLng,maxLat")
    try:
        min_lng, min_lat, max_lng, max_lat = map(float, parts)
    except ValueError as exc:
        raise ValueError("bbox 坐标必须是数字") from exc
    if not (-180 <= min_lng < max_lng <= 180):
        raise ValueError("bbox 经度范围无效")
    if not (-90 <= min_lat < max_lat <= 90):
        raise ValueError("bbox 纬度范围无效")
    return min_lng, min_lat, max_lng, max_lat
