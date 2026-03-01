#!/usr/bin/env python3
"""
ImageBin Backend - 自托管图床后端
支持本地上传、API 接口
"""
import os
import uuid
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(filename):
    """生成唯一文件名"""
    ext = filename.rsplit('.', 1)[1].lower()
    unique = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    return f"{unique}_{int(datetime.now().timestamp())}.{ext}"

@app.route('/api/upload', methods=['POST'])
def upload():
    """上传图片 API"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    filename = generate_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    file_url = f"/uploads/{filename}"
    
    return jsonify({
        'success': True,
        'url': file_url,
        'filename': filename,
        'size': os.path.getsize(filepath)
    })

@app.route('/uploads/<filename>')
def serve_image(filename):
    """提供图片访问"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/images', methods=['GET'])
def list_images():
    """列出所有图片"""
    images = []
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(f):
            path = os.path.join(app.config['UPLOAD_FOLDER'], f)
            images.append({
                'filename': f,
                'url': f'/uploads/{f}',
                'size': os.path.getsize(path),
                'created': datetime.fromtimestamp(os.path.getctime(path)).isoformat()
            })
    return jsonify({'images': images})

@app.route('/api/images/<filename>', methods=['DELETE'])
def delete_image(filename):
    """删除图片"""
    if '..' in filename or '/' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'success': True})
    return jsonify({'error': 'File not found'}), 404

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ImageBin API</title>
    </head>
    <body>
        <h1>🖼️ ImageBin API</h1>
        <p>API Endpoints:</p>
        <ul>
            <li>POST /api/upload - 上传图片</li>
            <li>GET /api/images - 列出图片</li>
            <li>DELETE /api/images/<filename> - 删除图片</li>
        </ul>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
