import os
from flask import Flask, render_template, request, jsonify
from PIL import Image

app = Flask(__name__)

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