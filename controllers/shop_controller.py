from flask import Blueprint, request, jsonify, send_file
from services import shop_service 
from io import BytesIO

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/api/shop", methods=["POST"])
def fetch_shop_page():
    if request.method == 'OPTIONS':
        return '', 204  # 响应预检请求
    try:
        data = request.json or {}

        total_count = int(data.get("totalCount", 0))
        brand_id = int(data.get("brand_id", 0))
        page_num = int(data.get("pageNum", 1))
        cookies = data.get("cookies")

        html, err = shop_service.get_shop_page(total_count, brand_id, cookies, page_num)
        if err:
            return jsonify({"status": 500, "data": "", "error": err})

        parsed = shop_service.parse_shop_html(html)
        return jsonify({"status": 200, "data": parsed, "error": ""})
    except Exception as e:
        return jsonify({"status": 400, "data": "", "error": f"参数错误：{str(e)}"})
    
@shop_bp.route("/api/item", methods=["POST"])
def fetch_good_detail():
    if request.method == 'OPTIONS':
        return '', 204  # 响应预检请求
    try:
        data = request.json or {}

        url = data.get("url")
        cookies = data.get("cookies")

        html, err = shop_service.get_good_detail(url, cookies)
        if err:
            return jsonify({"status": 500, "data": "", "error": err})

        
        return jsonify({"status": 200, "data": html, "error": ""})
    except Exception as e:
        return jsonify({"status": 400, "data": "", "error": f"参数错误：{str(e)}"})
    
@shop_bp.route("/api/exportGoodsExcel", methods=["POST"])
def fetch_goods_excel():
    if request.method == 'OPTIONS':
        return '', 204  # 响应预检请求
    data = request.json or {}

    oneData = data.get("data")
    cookies = data.get("cookies")

    # 创建一个 BytesIO 内存文件
    output = BytesIO()
    excelName, err = shop_service.export_items_excel(oneData, cookies, output)
    output.seek(0)  # 移动到开头
    if err:
        return jsonify({"status": 500, "data": "", "error": err})
        
        

    return send_file(
        output,
        as_attachment=True,
        download_name=excelName + ".xlsx",  # 自动下载的文件名
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
