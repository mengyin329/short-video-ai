FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（编译依赖）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv（更快的包管理工具）
RUN pip install uv

# 复制项目文件
COPY . .

# 安装Python依赖
RUN uv sync --no-dev

# 创建必要的目录
RUN mkdir -p logs assets static

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 启动服务
CMD ["python", "src/main.py", "-m", "http", "-p", "5000"]
