#!/bin/bash

# 短视频AI编剧助手 - 快速启动脚本

set -e

echo "=========================================="
echo "  短视频AI编剧助手 - 快速部署"
echo "=========================================="
echo ""

# 检查Python版本
echo "📋 检查Python版本..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.12+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Python版本: $PYTHON_VERSION"
echo ""

# 检查是否已配置环境变量
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件"
    echo "📝 正在创建 .env 文件..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo ""
    echo "⚠️  请编辑 .env 文件，填写以下必要配置："
    echo "   - ARK_API_KEY (豆包API Key)"
    echo "   - ARK_BASE_URL (豆包Base URL)"
    echo "   - ARK_MODEL (模型名称)"
    echo ""
    read -p "按 Enter 继续，或按 Ctrl+C 取消..."
fi

# 检查是否已安装依赖
echo "📦 检查依赖..."
if ! command -v uv &> /dev/null; then
    echo "📥 安装 uv (推荐使用)..."
    pip install uv
fi

if [ -d ".venv" ]; then
    echo "✅ 虚拟环境已存在"
else
    echo "🔨 创建虚拟环境..."
    uv sync
fi

echo ""
echo "=========================================="
echo "  选择启动方式"
echo "=========================================="
echo "1. 直接启动 (适合开发)"
echo "2. Docker启动 (适合生产)"
echo "3. Docker Compose启动 (推荐)"
echo ""
read -p "请选择 (1/2/3, 默认3): " choice
choice=${choice:-3}

case $choice in
    1)
        echo ""
        echo "🚀 直接启动服务..."
        python src/main.py -m http -p 5000
        ;;
    2)
        echo ""
        echo "🐳 构建Docker镜像..."
        docker build -t short-video-ai .

        echo ""
        echo "🚀 启动Docker容器..."
        docker run -d \
            -p 5000:5000 \
            --name short-video-ai \
            --env-file .env \
            -v $(pwd)/logs:/app/logs \
            -v $(pwd)/assets:/app/assets \
            short-video-ai

        echo ""
        echo "✅ 服务已启动！"
        echo "📱 访问地址: http://localhost:5000"
        echo ""
        echo "📋 常用命令："
        echo "  查看日志: docker logs -f short-video-ai"
        echo "  停止服务: docker stop short-video-ai"
        echo "  删除容器: docker rm short-video-ai"
        ;;
    3)
        echo ""
        echo "🐳 使用Docker Compose启动..."
        if command -v docker-compose &> /dev/null; then
            docker-compose up -d
        else
            docker compose up -d
        fi

        echo ""
        echo "✅ 服务已启动！"
        echo "📱 访问地址: http://localhost:5000"
        echo ""
        echo "📋 常用命令："
        echo "  查看日志: docker-compose logs -f"
        echo "  停止服务: docker-compose down"
        echo "  重启服务: docker-compose restart"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "📖 使用说明："
echo "  1. 访问 http://localhost:5000"
echo "  2. 配置API Key（如果未配置）"
echo "  3. 开始使用短视频AI编剧助手"
echo ""
echo "📚 详细文档: 请查看 DEPLOYMENT.md"
echo ""
