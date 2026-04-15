# 🎬 短视频AI编剧助手

> 基于LangChain和LangGraph的智能剧本创作工具，支持从创意构思到完整剧本、分镜设计、画面生成的全流程创作。

## ✨ 核心功能

- 🎬 **剧本创作**：支持职场、爱情、悬疑、搞笑等多种类型
- 📋 **导演分镜**：自动生成8列专业分镜表
- 🎨 **图像生成**：AI自动生成分镜概念图
- ✍️ **Prompt工程**：首帧图Prompt + 可灵/即梦Prompt
- 🔄 **多模型支持**：豆包、OpenAI、DeepSeek、Kimi等

## 🚀 快速开始

### 方式1：一键部署（推荐）

```bash
# 1. 克隆项目
git clone <your-repo-url> short-video-ai
cd short-video-ai

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填写你的 API Key

# 3. 启动服务
./start.sh

# 4. 访问应用
# 浏览器打开：http://localhost:5000
```

### 方式2：Docker部署（生产环境）

```bash
# 1. 克隆项目
git clone <your-repo-url> short-video-ai
cd short-video-ai

# 2. 配置环境变量
cp .env.example .env

# 3. 启动服务
docker-compose up -d

# 4. 访问应用
http://localhost:5000
```

### 方式3：OpenClaw环境部署

```bash
# 1. 在OpenClaw工作空间中导入项目
cd /workspace/projects
git clone <your-repo-url> short-video-ai

# 2. 配置环境变量
cd short-video-ai
cp .env.example .env
# 编辑 .env，填写你的 API Key

# 3. 启动服务
python src/main.py -m http -p 5000

# 4. 访问应用
# 浏览器打开项目提供的预览地址
```

## 📚 详细文档

- 📖 [快速开始](QUICKSTART.md) - 5分钟快速上手
- 📖 [完整部署指南](DEPLOYMENT.md) - 详细的配置说明
- 📖 [如何让别人部署](HOW_TO_DEPLOY.md) - 项目发布指南
- 📖 [API文档](http://localhost:5000/docs) - 服务启动后访问

## ⚙️ 配置说明

### 获取API Key

#### 豆包大模型（推荐）

1. 访问 [火山引擎方舟控制台](https://console.volcengine.com/ark)
2. 创建 API Key
3. 配置到 `.env` 文件：

```env
ARK_API_KEY=your_ark_api_key_here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/v3
ARK_MODEL=doubao-pro-32k
```

#### 其他OpenAI兼容模型

```env
# DeepSeek
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# Kimi
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.moonshot.cn/v1
OPENAI_MODEL=moonshot-v1-32k
```

## 📁 项目结构

```
short-video-ai/
├── src/                      # 源代码目录
│   ├── agents/              # Agent逻辑
│   ├── tools/               # 工具定义
│   ├── storage/             # 存储和记忆
│   └── main.py              # FastAPI主程序
├── static/                  # 前端静态文件
│   ├── index.html           # 主界面
│   └── welcome.html         # 欢迎页/配置页
├── config/                  # 配置文件
│   └── agent_llm_config.json # Agent配置
├── tests/                   # 测试文件
├── .env.example            # 环境变量示例
├── .env                    # 环境变量配置（需创建）
├── requirements.txt        # Python依赖
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker编排
├── start.sh               # 一键启动脚本
└── README.md              # 项目说明
```

## 🔧 本地运行

### 运行流程
```bash
bash scripts/local_run.sh -m flow
```

### 运行节点
```bash
bash scripts/local_run.sh -m node -n node_name
```

### 启动HTTP服务
```bash
bash scripts/http_run.sh -m http -p 5000
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境搭建

```bash
# 1. 克隆项目
git clone <your-repo-url> short-video-ai
cd short-video-ai

# 2. 安装开发依赖
pip install uv
uv sync --dev

# 3. 运行测试
pytest tests/

# 4. 启动开发服务器（支持热重载）
python src/main.py -m http -p 5000
```

## 📄 许可证

MIT License

## 📞 联系方式

- 提交 Issue：https://github.com/your-repo/issues
- 邮箱：your-email@example.com

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的LLM应用框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 有状态的Agent框架
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能Web框架
- [火山引擎方舟](https://www.volcengine.com/product/ark) - 豆包大模型

---

**祝你使用愉快！** 🎉

