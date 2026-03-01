# 🖼️ ImageBin - 图床工具

> 简单好用的图床，支持本地上传和在线使用

## 🌟 功能

- 📤 拖拽上传图片
- 📋 一键复制链接（Markdown / HTML / URL）
- 📚 上传历史记录
- 🌐 免安装，浏览器直接用
- 🔧 支持自托管后端

## 🚀 快速开始

### 方式一：直接使用（在线版）

1. 打开 https://fangwenky.github.io/ImageBin/
2. 拖拽或点击上传图片
3. 复制链接

### 方式二：自托管后端

```bash
# 克隆
git clone https://github.com/Fangwenky/ImageBin.git
cd ImageBin

# 安装依赖
pip install -r requirements.txt

# 启动后端
python backend.py
```

然后访问 http://localhost:5000

### 方式三：Docker 部署

```bash
docker build -t imagebin .
docker run -d -p 5000:5000 -v ./uploads:/app/uploads imagebin
```

## 📦 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 前端页面（浏览器直接打开或部署到任意静态托管） |
| `backend.py` | Python Flask 后端（需要自托管时使用） |
| `requirements.txt` | Python 依赖 |

## 🔧 API

### 上传图片

```bash
curl -X POST -F "image=@/path/to/image.jpg" http://localhost:5000/api/upload
```

响应：
```json
{
  "success": true,
  "url": "/uploads/abc123.jpg",
  "filename": "abc123.jpg",
  "size": 1024
}
```

### 列出图片

```bash
curl http://localhost:5000/api/images
```

### 删除图片

```bash
curl -X DELETE http://localhost:5000/api/images/abc123.jpg
```

## 📱 配置自定义 API

在前端页面可以配置自定义 API 地址，实现真正的自托管：

1. 部署后端服务
2. 在前端输入后端地址
3. 即可使用自己的图床

## 🛠️ 技术栈

- 前端：HTML / CSS / JavaScript（原生）
- 后端：Python Flask
- 存储：本地文件系统

---

💻 Made with ❤️
