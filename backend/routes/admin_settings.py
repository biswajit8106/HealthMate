from flask import Blueprint, request, jsonify
from utils.auth import admin_login_required

admin_settings_bp = Blueprint('admin_settings_bp', __name__, url_prefix='/admin/settings')

# In-memory settings store for demonstration
settings_store = {
    'max_file_size': 10485760,  # 10 MB
    'report_retention_days': 365,
    'ml_confidence_threshold': 0.8
}

@admin_settings_bp.route('/', methods=['GET'])
@admin_login_required
def get_settings():
    try:
        return jsonify(settings_store), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_settings_bp.route('/', methods=['PUT'])
@admin_login_required
def update_settings():
    try:
        data = request.json
        for key in settings_store.keys():
            if key in data:
                settings_store[key] = data[key]
        return jsonify({'message': 'Settings updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
