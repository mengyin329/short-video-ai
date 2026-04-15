# 短视频AI编剧助手 - 独立部署指南

## 📖 项目简介

短视频AI编剧助手是一个基于 LangChain 和 LangGraph 的智能剧本创作工具，支持从创意构思到完整剧本、分镜设计、画面生成的全流程创作。

### 核心功能

- ✅ **剧本创作**：多种类型剧本（职场、爱情、悬疑、搞笑等）
- ✅ **导演分镜**：8列专业分镜表自动生成
- ✅ **Prompt工程**：首帧图Prompt + 可灵/即梦Prompt
- ✅ **分镜图生成**：AI自动生成分镜概念图
- ✅ **多模型支持**：支持豆包、OpenAI、DeepSeek、Kimi等

---

## 🚀 快速开始

### 方式一：直接部署（推荐OpenClaw用户）

如果你在OpenClaw环境中，可以直接使用现有代码：

```bash
# 1. 克隆项目到你的工作空间
cd /workspace
git clone <your-repo-url> short-video-ai
cd short-video-ai

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写你的 API Key

# 3. 安装依赖
uv sync

# 4. 启动服务
python src/main.py -m http -p 5000

# 5. 访问应用
# 浏览器打开：http://localhost:5000
```

### 方式二：Docker部署（推荐独立部署）

```bash
# 1. 构建镜像
docker build -t short-video-ai .

# 2. 启动容器
docker run -d \
  -p 5000:5000 \
  -e ARK_API_KEY=your_api_key \
  -e ARK_BASE_URL=https://ark.cn-beijing.volces.com/v3 \
  -e ARK_MODEL=doubao-pro-32k \
  short-video-ai

# 3. 访问应用
# 浏览器打开：http://localhost:5000
```

### 方式三：本地Python环境部署

```bash
# 1. 确保已安装 Python 3.12+
python --version

# 2. 安装依赖
pip install -r requirements.txt
# 或者使用 uv（推荐）
pip install uv
uv sync

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写配置

# 4. 启动服务
python src/main.py -m http -p 5000

# 5. 访问应用
# 浏览器打开：http://localhost:5000
```

---

## ⚙️ 配置说明

### 1. 环境变量配置

复制 `.env.example` 为 `.env` 并填写以下配置：

```bash
# 必填项
ARK_API_KEY=your_ark_api_key_here           # 豆包API Key
ARK_BASE_URL=https://ark.cn-beijing.volces.com/v3  # 豆包Base URL
ARK_MODEL=doubao-pro-32k                     # 模型名称

# 或使用其他 OpenAI 兼容模型
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```

### 2. 获取豆包API Key

1. 访问 [火山引擎方舟控制台](https://console.volcengine.com/ark)
2. 登录/注册账号
3. 进入"API Key管理"
4. 创建新的 API Key
5. 复制 API Key 到 `.env` 文件

### 3. 获取其他模型API Key

#### OpenAI
- 官网：https://platform.openai.com/
- Base URL：https://api.openai.com/v1

#### DeepSeek
- 官网：https://platform.deepseek.com/
- Base URL：https://api.deepseek.com/v1
- Model：deepseek-chat / deepseek-reasoner

#### Kimi（Moonshot）
- 官网：https://platform.moonshot.cn/
- Base URL：https://api.moonshot.cn/v1
- Model：moonshot-v1-8k / moonshot-v1-32k

---

## 📁 项目结构

```
short-video-ai/
├── src/                      # 源代码目录
│   ├── agents/              # Agent逻辑
│   │   └── agent.py         # 主Agent定义
│   ├── tools/               # 工具定义
│   │   └── storyboard_generator.py  # 分镜生成工具
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
├── pyproject.toml          # 项目依赖配置
├── Dockerfile              # Docker配置（需创建）
└── README.md               # 项目说明
```

---

## 🔄 如何脱离Coze平台使用

### 当前状态分析

项目当前依赖以下Coze平台特有的库：

| 依赖库 | 用途 | 独立部署处理方案 |
|--------|------|------------------|
| `coze-coding-utils` | 工具集、日志、上下文 | 保留（可通过 pip 安装） |
| `coze-workload-identity` | 身份认证 | 移除，使用环境变量 |
| `cozeloop` | 日志上报 | 移除，不影响功能 |
| `coze-coding-dev-sdk` | 图像生成 | 可保留或替换 |

### 方案一：最小改动部署（推荐）

保留 `coze-coding-utils` 和 `coze-coding-dev-sdk`，仅移除身份认证相关依赖。

**优点**：改动最小，部署快
**缺点**：仍依赖部分Coze SDK

**部署步骤**：

1. 安装依赖时排除身份认证库：
```bash
pip install coze-coding-utils>=0.2.6 coze-coding-dev-sdk>0.5.0
```

2. 创建 `.env` 文件配置API Key

3. 修改 `src/main.py`，移除身份认证检查（如需要）

### 方案二：完全独立部署（彻底脱离）

完全移除所有Coze依赖，使用标准库替代。

**优点**：完全独立，无平台绑定
**缺点**：需要重写部分代码

**需要重写的部分**：

1. **日志系统**：替换 `coze_coding_utils.log` 为标准 `logging`
2. **上下文管理**：实现简单的 `Context` 类
3. **图像生成**：替换为其他图像生成服务（如 Stable Diffusion API）

**工作量评估**：1-2天

### 方案三：混合部署（平衡方案）

- 保留核心业务逻辑（LangChain/LangGraph）
- 移除平台特定的基础设施依赖
- 使用Docker打包，内部包含必要的SDK

**优点**：兼顾独立性和开发效率
**缺点**：镜像较大

---

## 🐳 Docker部署（推荐生产环境）

### 1. 创建 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN pip install uv

# 复制项目文件
COPY . .

# 安装依赖
RUN uv sync --no-dev

# 暴露端口
EXPOSE 5000

# 启动服务
CMD ["python", "src/main.py", "-m", "http", "-p", "5000"]
```

### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ARK_API_KEY=${ARK_API_KEY}
      - ARK_BASE_URL=${ARK_BASE_URL}
      - ARK_MODEL=${ARK_MODEL}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      - ./logs:/app/logs
      - ./assets:/app/assets
    restart: unless-stopped
```

### 3. 使用 Docker Compose 部署

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

---

## 🔧 常见问题

### Q1: 如何切换模型？

**A**: 在 `.env` 文件中修改模型配置，或通过网页界面的"切换模型"按钮。

### Q2: 如何更换图像生成服务？

**A**: 修改 `src/tools/storyboard_generator.py` 中的图像生成客户端配置。

### Q3: 如何持久化对话历史？

**A**: 在 `.env` 中配置数据库连接，启用 PostgreSQL 作为对话历史存储。

### Q4: 如何在本地测试？

**A**: 使用 `test_run` 工具或直接访问 http://localhost:5000 进行测试。

### Q5: 如何自定义Agent提示词？

**A**: 修改 `config/agent_llm_config.json` 中的 `sp` 字段。

---

## 📚 API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

### 主要API端点

- `POST /run` - 运行Agent（同步）
- `POST /v1/chat/completions` - OpenAI兼容接口
- `GET /` - 主界面
- `GET /welcome.html` - 欢迎页
- `GET /health` - 健康检查

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境搭建

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd short-video-ai

# 2. 安装开发依赖
uv sync --dev

# 3. 运行测试
pytest tests/

# 4. 启动开发服务器（支持热重载）
python src/main.py -m http -p 5000
```

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- 提交 Issue：https://github.com/your-repo/issues
- 邮箱：your-email@example.com

---

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的LLM应用框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 有状态的Agent框架
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能Web框架
- [火山引擎方舟](https://www.volcengine.com/product/ark) - 豆包大模型

---

**祝你使用愉快！如有问题请随时反馈。** 🎉
