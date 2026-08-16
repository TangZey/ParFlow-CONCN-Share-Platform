import os
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from config import Config
from models import db, Watershed
from clip_worker import run_clip
from boundary_service import get_boundaries

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    app.config['JSON_AS_ASCII'] = False

    database_path = Path(app.config['SQLALCHEMY_DATABASE_URI'].removeprefix('sqlite:///'))
    database_path.parent.mkdir(parents=True, exist_ok=True)
    Path(app.config['JOB_ROOT']).mkdir(parents=True, exist_ok=True)
    Path(app.config['BOUNDARY_CACHE_DIR']).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    CORS(app, resources={r'/api/*': {'origins': app.config['ALLOWED_ORIGINS']}})

    with app.app_context():
        db.create_all()

    # ---------- API 路由 ----------
    @app.route('/api/config', methods=['GET'])
    def public_config():
        return jsonify({
            'maxBatchDownloads': app.config['MAX_BATCH_DOWNLOADS'],
            'fullBoundaryMaxLevel': app.config['FULL_BOUNDARY_MAX_LEVEL'],
            'maxBoundaryFeatures': app.config['MAX_BOUNDARY_FEATURES'],
        })

    @app.route('/api/watersheds', methods=['GET'])
    def search_watersheds():
        keyword = request.args.get('keyword', '').strip()
        region = request.args.get('region', '').strip()
        level = request.args.get('level', type=int)

        query = Watershed.query
        if keyword:
            query = query.filter(
                (Watershed.id.contains(keyword)) | (Watershed.name.contains(keyword))
            )
        if region:
            query = query.filter(Watershed.region == region)
        if level is not None:
            query = query.filter(Watershed.level == level)

        results = query.all()
        return jsonify([w.to_dict() for w in results])

    @app.route('/api/watersheds/<id>', methods=['GET'])
    def get_watershed(id):
        watershed = Watershed.query.get(id)
        if not watershed:
            return jsonify({'error': '流域不存在'}), 404
        return jsonify(watershed.to_dict())

    @app.route('/api/download', methods=['POST'])
    def download_data():
        data = request.get_json()
        if not data or 'ids' not in data:
            return jsonify({'error': '缺少 ids 参数'}), 400

        ids = data.get('ids')
        if isinstance(ids, str):
            ids = [ids]
        elif isinstance(ids, list):
            ids = [str(item) for item in ids]
        else:
            return jsonify({'error': 'ids 必须是字符串或列表'}), 400

        ids = [i.strip() for i in ids if i.strip()]
        ids = list(dict.fromkeys(ids))
        if not ids:
            return jsonify({'error': 'ids 不能为空'}), 400
        if len(ids) > app.config['MAX_BATCH_DOWNLOADS']:
            return jsonify({
                'error': f'单次最多下载 {app.config["MAX_BATCH_DOWNLOADS"]} 个流域'
            }), 400

        existing_ids = [w.id for w in Watershed.query.filter(Watershed.id.in_(ids)).all()]
        invalid_ids = [i for i in ids if i not in existing_ids]
        if invalid_ids:
            return jsonify({'error': f'以下编号不存在: {invalid_ids}'}), 404

        try:
            zip_path = run_clip(ids, Path(app.config['JOB_ROOT']))
            return send_file(zip_path, as_attachment=True)
        except Exception:
            app.logger.exception('裁剪或打包失败，流域编号: %s', ids)
            return jsonify({'error': '裁剪或打包失败，请联系管理员查看服务日志'}), 500

    # ---------- 流域边界 API ----------
    @app.route('/api/boundaries', methods=['GET'])
    def boundaries():
        """返回流域边界 GeoJSON（低等级全量，或按 id/bbox 筛选）"""
        return get_boundaries()

    # ---------- 前端静态文件服务 ----------
    dist_dir = Path(app.config['DIST_DIR'])

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # 如果是 API 请求，不处理（API 路由优先）
        if path.startswith('api/'):
            return '', 404

        # 尝试返回静态文件
        full_path = dist_dir / path
        if path != '' and os.path.exists(full_path) and os.path.isfile(full_path):
            return send_from_directory(dist_dir, path)
        else:
            # 返回 index.html（支持 Vue Router）
            return send_from_directory(dist_dir, 'index.html')

    return app


# ---------- 创建应用实例（供 gunicorn 使用） ----------
app = create_app()

# ---------- 直接运行（开发/测试） ----------
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=50001)
