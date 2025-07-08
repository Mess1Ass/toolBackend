from flask import Blueprint, request, jsonify, send_file
from services import file_service

file_bp = Blueprint("file_bp", __name__)

@file_bp.route("/files", methods=["GET"])
def get_files():
    parent = request.args.get("parent", "root")
    return jsonify(file_service.get_files(parent))

@file_bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    parent = request.args.get("parent", "root")
    result, err = file_service.save_file(file, parent)
    if err:
        return jsonify({"error": err}), 400
    return jsonify(result)

@file_bp.route("/create_folder", methods=["POST"])
def create_folder():
    data = request.get_json()
    name = data.get("name")
    parent = data.get("parent", "root")
    if not name:
        return jsonify({"error": "缺少 name 参数"}), 400
    result, code = file_service.create_folder(name, parent)
    return jsonify(result), code

@file_bp.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    path = file_service.get_file_path(file_id)
    if not path:
        return jsonify({"error": "文件未找到"}), 404
    return send_file(path, as_attachment=True)

@file_bp.route("/file/<file_id>", methods=["DELETE"])
def delete_file(file_id):
    success, msg = file_service.delete_by_id(file_id)
    if not success:
        return jsonify({"error": msg}), 400
    return jsonify({"message": msg})

@file_bp.route("/view_excel/<file_id>", methods=["GET"])
def view_excel(file_id):
    result, err = file_service.view_excel(file_id)
    if err:
        return jsonify({"error": err}), 400
    return jsonify(result)
