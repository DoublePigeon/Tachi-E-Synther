import os
import json
from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw, ImageChops

app = Flask(__name__)

# 遮罩超采样上限（像素数），用于让选区边缘更平滑
MAX_MASK_PIXELS = 16_000_000


def parse_polygons(raw):
    """解析前端传来的套索选区，返回 [([(x, y), ...], 'add' | 'subtract'), ...]。"""
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except (TypeError, ValueError):
        return []
    if not isinstance(data, list):
        return []

    polygons = []
    for item in data:
        if not isinstance(item, dict):
            continue
        points = item.get('points')
        if not isinstance(points, list) or len(points) < 3:
            continue
        try:
            parsed = [(float(p[0]), float(p[1])) for p in points]
        except (TypeError, ValueError, IndexError):
            continue
        op = 'subtract' if item.get('op') == 'subtract' else 'add'
        polygons.append((parsed, op))
    return polygons


def build_selection_mask(size, polygons, offset):
    """生成图片尺寸的选区遮罩（'L' 模式）：255 保留，0 剔除。

    polygons 中的坐标位于底图坐标系，offset 为该图片相对底图的偏移。
    """
    width, height = size

    # 自适应超采样倍率，先在高分辨率下绘制再缩小以获得抗锯齿边缘
    factor = 1
    while factor < 4 and width * height * (factor + 1) ** 2 <= MAX_MASK_PIXELS:
        factor += 1

    mask = Image.new('L', (width * factor, height * factor), 0)
    drawer = ImageDraw.Draw(mask)
    for points, op in polygons:
        scaled = [((x - offset[0]) * factor, (y - offset[1]) * factor) for x, y in points]
        drawer.polygon(scaled, fill=0 if op == 'subtract' else 255)

    if factor > 1:
        # BOX 即区域平均，缩放后边缘正好是 1 像素的过渡带，且不会像 LANCZOS 那样产生振铃
        mask = mask.resize((width, height), Image.BOX)

    return mask


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        # 获取表单数据
        output_dir = request.form.get('output_path')
        offset_x = int(request.form.get('x'))
        offset_y = int(request.form.get('y'))
        
        # 验证输出路径
        if not output_dir or not os.path.isdir(output_dir):
            return jsonify({"status": "error", "message": "输出路径不存在或无效，请检查文件夹路径。"}), 400

        # 获取文件
        body_file = request.files.get('body_image')
        expression_files = request.files.getlist('expression_images')

        # 套索选区（底图坐标），用于裁剪所有表情图片
        polygons = parse_polygons(request.form.get('polygons'))

        if not body_file:
             return jsonify({"status": "error", "message": "未上传人物底图。"}), 400

        # 读取人物图片 (底图)
        body_img = Image.open(body_file.stream).convert("RGBA")
        body_filename = os.path.splitext(body_file.filename)[0]

        count = 0
        
        # 遍历所有表情图片进行合成
        for expr_file in expression_files:
            # 处理可能传上来的空文件情况
            if expr_file.filename == '':
                continue
                
            # 读取表情图片
            expr_img = Image.open(expr_file.stream).convert("RGBA")
            expr_filename = os.path.splitext(expr_file.filename)[0]

            # 应用套索选区：只有套中的部分参与合成
            if polygons:
                mask = build_selection_mask(expr_img.size, polygons, (offset_x, offset_y))
                expr_img.putalpha(ImageChops.multiply(expr_img.getchannel("A"), mask))

            # 1. 创建一个和底图一样大的全透明图层
            layer = Image.new('RGBA', body_img.size, (0, 0, 0, 0))
            
            # 2. 将表情图片粘贴到这个透明图层的指定位置
            layer.paste(expr_img, (offset_x, offset_y))
            
            # 3. 使用 alpha_composite 进行图层混合
            final_image = Image.alpha_composite(body_img, layer)

            # 生成文件名
            output_filename = f"{body_filename}_{expr_filename}.png"
            output_full_path = os.path.join(output_dir, output_filename)

            # 保存
            final_image.save(output_full_path, format="PNG")
            count += 1

        if count == 0:
            return jsonify({"status": "error", "message": "没有检测到有效的表情图片。"}), 400

        return jsonify({"status": "success", "message": f"成功合成并保存了 {count} 张图片到 {output_dir}"})

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = 5000
    print(f"启动程序... http://127.0.0.1:{port}")
    app.run(debug=True, port=port)