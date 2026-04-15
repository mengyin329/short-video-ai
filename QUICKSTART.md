# 🎬 短视频AI编剧助手 - 快速开始

## 🚀 一键部署

### 前置要求

- Python 3.12+ 或 Docker
- 豆包API Key（或其他大模型API Key）

### 快速启动

```bash
# 1. 克隆项目
git clone <your-repo-url> short-video-ai
cd short-video-ai

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写你的 API Key

# 3. 运行启动脚本
./start.sh

# 4. 访问应用
# 浏览器打开：http://localhost:5000
```

## 📋 配置说明

### 获取豆包API Key

1. 访问 [火山引擎方舟控制台](https://console.volcengine.com/ark)
2. 创建 API Key
3. 复制到 `.env` 文件：

```env
ARK_API_KEY=your_ark_api_key_here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/v3
ARK_MODEL=doubao-pro-32k
```

### 使用其他模型

```env
# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# DeepSeek
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

## 🎯 使用方法

### 初始配置

1. 访问 http://localhost:5000
2. 如果未配置，会跳转到欢迎页
3. 填写 API Key 并保存

### 开始创作

- 💬 直接对话：描述你想创作的剧本类型
- 🎬 点击按钮：使用快捷功能（创作剧本、生成分镜等）
- 🔄 切换模型：随时切换不同的大模型

## 📚 详细文档

- **完整部署指南**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **项目结构**: 见 DEPLOYMENT.md
- **API文档**: http://localhost:5000/docs

## 🐳 Docker部署

```bash
# 方式1: 使用Docker Compose（推荐）
docker-compose up -d

# 方式2: 直接使用Docker
docker build -t short-video-ai .
docker run -d -p 5000:5000 --env-file .env short-video-ai
```

## ❓ 常见问题

### Q: 如何修改模型？

A: 修改 `.env` 文件或在网页界面点击"切换模型"

### Q: 如何持久化对话历史？

A: 在 `.env` 中配置 `DATABASE_URL` 启用数据库

### Q: 支持哪些模型？

A: 支持所有 OpenAI 兼容的模型：豆包、OpenAI、DeepSeek、Kimi等

## 🤝 问题反馈

提交 Issue: https://github.com/your-repo/issues

---

**祝你使用愉快！** 🎉
