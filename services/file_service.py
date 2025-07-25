import os
import re
import pandas as pd
import datetime
from models.file_model import (
    insert_file_info, list_files, delete_file,
    find_file_by_id, find_by_name_and_parent, find_files_by_parent
)
import config
from flask import current_app

# UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 保存文件
def save_file(file, parent="root"):
    if not file or file.filename == "":
        return None, "未选择文件"

    filename = file.filename
    exists = find_by_name_and_parent(filename, parent)
    if exists:
        return None, "当前路径下已有同名文件"

    # 使用相对路径构建保存路径
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_folder, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)
    size = os.path.getsize(filepath)

    insert_file_info(filename, size, filepath, is_folder=False, parent=parent)
    return {"filename": filename, "size": size, "path": filepath}, None


# 创建文件夹
def create_folder(name, parent="root"):
    exists = find_by_name_and_parent(name, parent)
    if exists:
        return {"error": "同名文件夹已存在"}, 400

    resId = insert_file_info(name, 0, "", is_folder=True, parent=parent)
    return {"message": "Folder created", "name": name, "_id": resId}, 200

def get_files(parent="root"):
    return list_files(parent)


# 根据id删除文件/文件夹
def delete_by_id(file_id, force_delete_children=False):
    file = find_file_by_id(file_id)
    if not file:
        return False, "File not found"

    if file.get("is_folder"):
        # 判断是否强制删除所有子项
        if not force_delete_children:
            return False, "该文件夹包含子项，请确认是否删除全部内容"

        # 递归删除
        success, msg = recursive_delete(file_id)
        return success, msg

    # 如果是单个文件
    if file.get("path"):
        try:
            os.remove(file["path"])
        except Exception as e:
            return False, f"Failed to delete file: {str(e)}"

    delete_file(file_id)
    return True, "文件已删除"

# 递归删除文件并更新实体文件路径
def recursive_delete(file_id):
    file = find_file_by_id(file_id)
    if not file:
        return False, "File not found"

    # 如果是文件，先删文件本体
    if not file.get("is_folder") and file.get("path"):
        try:
            os.remove(file["path"])
        except Exception as e:
            # 忽略文件不存在问题
            print(f"Failed to delete physical file: {e}")

    # 找出子项，递归删除
    children = find_files_by_parent(file_id)
    for child in children:
        recursive_delete(str(child["_id"]))

    # 最后删掉自己
    delete_file(file_id)
    return True, "文件夹及其内容已删除"

# 获取文件路径
def get_file_path(file_id):
    file = find_file_by_id(file_id)
    return file.get("path") if file and not file.get("is_folder") else None

# 查看单excel文件内容
def view_excel(file_id):
    file = find_file_by_id(file_id)
    if not file or not file["filename"].endswith(".xlsx"):
        return None, "文件不存在或不是Excel"

    try:
        df_all = pd.read_excel(file["path"], header=None)
        if df_all.shape[0] < 2:
            return None, "Excel 格式错误，缺少表头"

        title = str(df_all.iloc[0, 0])  # A1 作为标题

        # 提取“队”与“礼包”之间的文字
        match = re.search(r"队(.*?)礼包", title)
        type_between = match.group(1).strip() if match else ""


        columns = df_all.iloc[1].fillna("").tolist()  # 第二行是表头
        data_rows = df_all.iloc[2:-4]  # 第3行开始到倒数第5行为正式数据
        data_rows.columns = columns

        data_rows = data_rows.fillna("")
        data = data_rows.to_dict(orient="records")

        # 最后四行作为 datalist
        datalist = df_all.iloc[-4:].fillna("").values.tolist()

        return {
            "title": title,
            "type": type_between,
            "columns": columns,
            "rows": data,
            "datalist": datalist,
            "id": str(file_id)
        }, None

    except Exception as e:
        return None, f"解析失败: {str(e)}"

# 上传文件夹及其内部文件
def save_uploaded_files(files, parent_id):
    existingFileNum = 0
    for file in files:
        print("上传文件:", file.filename)
        rel_path = os.path.normpath(file.filename)
        parts = rel_path.split(os.sep)

        current_parent_id = parent_id

        for i in range(len(parts) - 1):
            folder_name = parts[i]

            existingFolder = find_by_name_and_parent(folder_name, current_parent_id)
            if existingFolder:
                current_parent_id = str(existingFolder["_id"])
            else:
                data, status = create_folder(folder_name, current_parent_id)
                if status == 200 and data is not None:
                    current_parent_id = str(data["_id"])
                


        # 剩下保存 Excel 的逻辑保持不变
        filename = parts[-1]
        existingFile = find_by_name_and_parent(filename, current_parent_id)
        if existingFile:
            existingFileNum += 1
            continue

        # 使用相对路径构建保存路径
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        filepath = os.path.join(upload_folder, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        size = os.path.getsize(filepath)
        print("保存文件:", filepath)

        insert_file_info(filename, size, filepath, is_folder=False, parent=current_parent_id)
    if(existingFileNum >= len(files)):
        return {"message": "已存在相同文件"}, 400
    else:
        return {"message": "上传成功"}, 200


# 查看文件夹内全部excel（仅公演座位的excel）
def view_gift_excels(folder_id):
    folder = find_file_by_id(folder_id)
    if not folder or not folder.get("is_folder"):
        return {"error": "目标不是文件夹"}, 400

    children = find_files_by_parent(folder_id)
    if not children:
        return {"error": "文件夹为空"}, 400

    for child in children:
        if child.get("is_folder"):
            return {"error": f"存在子文件夹：{child['filename']}"}, 400
        if not child["filename"].endswith(".xlsx"):
            return {"error": f"存在非 Excel 文件：{child['filename']}"}, 400
        if "礼包" not in child["filename"]:
            return {"error": f"存在不含“礼包”的文件名：{child['filename']}"}, 400

    result_list = []
    for child in children:
        result, err = view_excel(child["_id"])
        if err or result is None:
            return {"error": f"{child['filename']} 解析失败: {err or '未知错误'}"}, 400
        result["filename"] = child["filename"]
        result_list.append(result)

    return {"data": result_list}, 200

# 获取该id对应数据库数据的文件类型
def get_file_type(file_id):
    file = find_file_by_id(file_id)
    if not file:
        return None, "文件不存在"

    if file.get("is_folder"):
        return {"type": "folder"}, None

    filename = file.get("filename", "")
    if filename.endswith(".xls") or filename.endswith(".xlsx"):
        return {"type": "excel"}, None

    return {"type": "other"}, None