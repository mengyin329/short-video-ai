#!/bin/bash
# 短视频AI编剧助手 - Web界面启动脚本

echo "🎬 启动短视频AI编剧助手 Web界面..."
echo ""

cd "$(dirname "$0")/.."
python src/web_ui/app.py
