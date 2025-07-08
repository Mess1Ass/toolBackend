import os
import pandas as pd
from models.file_model import (
    insert_file_info, list_files, delete_file,
    find_file_by_id, find_by_name_and_parent
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_file(file, parent="root"):
    if not file or file.filename == "":
        return None, "未选择文件"

    filename = file.filename
    exists = find_by_name_and_parent(filename, parent)
    if exists:
        return None, "当前路径下已有同名文件"

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    size = os.path.getsize(filepath)

    insert_file_info(filename, size, filepath, is_folder=False, parent=parent)
    return {"filename": filename, "size": size, "path": filepath}, None


def create_folder(name, parent="root"):
    exists = find_by_name_and_parent(name, parent)
    if exists:
        return {"error": "同名文件夹已存在"}, 400

    insert_file_info(name, 0, "", is_folder=True, parent=parent)
    return {"message": "Folder created", "name": name}, 200

def get_files(parent="root"):
    return list_files(parent)

def delete_by_id(file_id):
    file = find_file_by_id(file_id)
    if not file:
        return False, "File not found"

    if not file.get("is_folder") and file.get("path"):
        try:
            os.remove(file["path"])
        except Exception as e:
            return False, f"Failed to delete file: {str(e)}"

    delete_file(file_id)
    return True, "Deleted successfully"

def get_file_path(file_id):
    file = find_file_by_id(file_id)
    return file.get("path") if file and not file.get("is_folder") else None

def view_excel(file_id):
    file = find_file_by_id(file_id)
    if not file or not file["filename"].endswith(".xlsx"):
        return None, "文件不存在或不是Excel"

    try:
        df_all = pd.read_excel(file["path"], header=None)
        if df_all.shape[0] < 2:
            return None, "Excel 格式错误，缺少表头"

        title = str(df_all.iloc[0, 0])  # A1 作为标题

        columns = df_all.iloc[1].fillna("").tolist()  # 第二行是表头
        data_rows = df_all.iloc[2:-4]  # 第3行开始到倒数第5行为正式数据
        data_rows.columns = columns

        data_rows = data_rows.fillna("")
        data = data_rows.to_dict(orient="records")

        # 最后四行作为 datalist
        datalist = df_all.iloc[-4:].fillna("").values.tolist()

        return {
            "title": title,
            "columns": columns,
            "rows": data,
            "datalist": datalist
        }, None

    except Exception as e:
        return None, f"解析失败: {str(e)}"

