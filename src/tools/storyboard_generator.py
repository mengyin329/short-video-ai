"""
分镜图生成工具

根据分镜描述自动生成对应的分镜图，支持多种风格。
支持生成HTML宫格展示页面。
支持用户自定义图像生成API配置。
"""

import os
import time
from typing import Optional, List, Dict
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import ImageGenerationClient
from coze_coding_dev_sdk.s3 import S3SyncStorage
from coze_coding_utils.runtime_ctx.context import new_context
import requests
import base64
import hashlib


# 分镜图风格预设
STYLE_PRESETS = {
    "电影感": "cinematic movie still, professional lighting, dramatic composition, film grain, 16:9 aspect ratio",
    "日系动漫": "anime style, Japanese animation, vibrant colors, clean lines, expressive characters",
    "韩系清新": "Korean drama style, soft lighting, pastel colors, romantic atmosphere, dreamy",
    "写实风格": "photorealistic, high detail, natural lighting, 4K quality, professional photography",
    "复古胶片": "vintage film photography, warm tones, film grain, nostalgic atmosphere, soft focus",
    "赛博朋克": "cyberpunk style, neon lights, futuristic, dark atmosphere, high contrast",
    "水彩插画": "watercolor illustration, soft edges, artistic, dreamy colors, hand-painted style",
    "黑白电影": "black and white photography, high contrast, dramatic shadows, classic film noir"
}

# 用户配置的 Header 名称
HEADER_USER_IMAGE_API_KEY = "x-user-image-api-key"
HEADER_USER_IMAGE_BASE_URL = "x-user-image-model"


def _get_user_image_config(runtime: ToolRuntime) -> Optional[Dict[str, str]]:
    """从运行时上下文获取用户图像生成配置"""
    if not runtime or not runtime.context:
        return None
    
    ctx = runtime.context
    # 尝试从 headers 中获取
    headers = getattr(ctx, 'headers', None) or {}
    
    api_key = headers.get(HEADER_USER_IMAGE_API_KEY)
    base_url = headers.get(HEADER_USER_IMAGE_BASE_URL)
    
    if api_key and base_url:
        return {
            "api_key": api_key,
            "base_url": base_url
        }
    return None


def _generate_image_with_user_config(
    prompt: str,
    api_key: str,
    base_url: str,
    size: str = "1024x1024"
) -> Optional[str]:
    """使用用户自定义配置生成图像"""
    try:
        # 支持 OpenAI 兼容的图像生成 API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "n": 1,
            "size": size,
            "response_format": "url"
        }
        
        response = requests.post(
            f"{base_url}/images/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                return data["data"][0].get("url") or data["data"][0].get("b64_json")
        
        print(f"用户API生成失败: {response.status_code} - {response.text}")
        return None
    
    except Exception as e:
        print(f"用户API调用出错: {e}")
        return None


def _generate_image_with_default(prompt: str, ctx) -> Optional[str]:
    """使用默认配置生成图像"""
    try:
        client = ImageGenerationClient(ctx=ctx)
        response = client.generate(prompt=prompt, size="2K", watermark=False)
        
        if response.success and response.image_urls:
            return response.image_urls[0]
        return None
    except Exception as e:
        print(f"默认API生成失败: {e}")
        return None


def _build_storyboard_prompt(
    scene_description: str,
    style: str = "电影感",
    mood: str = "",
    characters: str = "",
    camera_angle: str = ""
) -> str:
    """构建分镜图生成的Prompt"""
    style_prompt = STYLE_PRESETS.get(style, STYLE_PRESETS["电影感"])
    
    prompt_parts = [
        f"Storyboard frame for short video, {style_prompt}",
        f"Scene: {scene_description}"
    ]
    
    if characters:
        prompt_parts.append(f"Characters: {characters}")
    if camera_angle:
        prompt_parts.append(f"Camera: {camera_angle}")
    if mood:
        prompt_parts.append(f"Mood: {mood}")
    
    prompt_parts.extend([
        "high quality, detailed, professional storyboard art",
        "suitable for video production reference"
    ])
    
    return ", ".join(prompt_parts)


def _generate_grid_html(
    images: List[Dict[str, str]],
    title: str = "分镜图预览"
) -> str:
    """生成宫格展示HTML页面"""
    
    # 计算宫格布局
    total = len(images)
    cols = min(4, max(2, total))  # 2-4列
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 30px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{
            color: #fff;
            font-size: 2rem;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #888;
            font-size: 0.9rem;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat({cols}, 1fr);
            gap: 20px;
        }}
        .card {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(74,158,255,0.2);
        }}
        .card-image {{
            width: 100%;
            aspect-ratio: 16/9;
            object-fit: cover;
            display: block;
        }}
        .card-info {{
            padding: 15px;
        }}
        .card-number {{
            display: inline-block;
            background: linear-gradient(135deg, #4a9eff, #0066cc);
            color: #fff;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .card-desc {{
            color: #ccc;
            font-size: 0.85rem;
            line-height: 1.5;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 {title}</h1>
            <p>共 {total} 个分镜画面</p>
        </div>
        <div class="grid">
"""
    
    for i, img in enumerate(images, 1):
        scene_desc = img.get('description', f'场景 {i}')[:50]  # 限制描述长度
        html += f"""
            <div class="card">
                <img src="{img['url']}" alt="场景{i}" class="card-image">
                <div class="card-info">
                    <span class="card-number">场景 {i}</span>
                    <p class="card-desc">{scene_desc}</p>
                </div>
            </div>
"""
    
    html += """
        </div>
        <div class="footer">
            <p>由 短视频AI编剧助手 自动生成</p>
        </div>
    </div>
</body>
</html>
"""
    return html


def _upload_html_to_storage(html_content: str, title: str) -> str:
    """上传HTML到对象存储，返回访问链接"""
    try:
        storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
        
        # 生成唯一文件名
        timestamp = int(time.time())
        file_name = f"storyboard/storyboard_{timestamp}.html"
        
        # 上传HTML
        key = storage.upload_file(
            file_content=html_content.encode('utf-8'),
            file_name=file_name,
            content_type="text/html; charset=utf-8",
        )
        
        # 生成访问链接（有效期7天）
        url = storage.generate_presigned_url(key=key, expire_time=604800)
        return url
    
    except Exception as e:
        print(f"上传HTML失败: {e}")
        return ""


@tool
def generate_storyboard(
    scene_description: str,
    style: str = "电影感",
    mood: str = "",
    characters: str = "",
    camera_angle: str = "",
    runtime: ToolRuntime = None
) -> str:
    """
    生成单个分镜图
    
    根据场景描述生成专业的分镜图，支持多种画面风格。
    
    Args:
        scene_description: 场景描述（必需），描述画面中的场景、动作、环境等
        style: 画面风格，可选：电影感、日系动漫、韩系清新、写实风格、复古胶片、赛博朋克、水彩插画、黑白电影
        mood: 情绪氛围（可选），如：温馨、紧张、悲伤、欢乐等
        characters: 角色描述（可选），描述画面中的角色外观、表情、动作
        camera_angle: 镜头角度（可选），如：特写、中景、远景、俯视、仰视等
    
    Returns:
        生成的分镜图URL（Markdown图片格式）
    """
    try:
        ctx = runtime.context if runtime else new_context(method="generate_storyboard")
        
        prompt = _build_storyboard_prompt(
            scene_description=scene_description,
            style=style,
            mood=mood,
            characters=characters,
            camera_angle=camera_angle
        )
        
        # 检查用户是否有自定义图像生成配置
        user_config = _get_user_image_config(runtime)
        
        if user_config:
            # 使用用户自定义配置
            url = _generate_image_with_user_config(
                prompt=prompt,
                api_key=user_config["api_key"],
                base_url=user_config["base_url"]
            )
            if url:
                return f"✅ 分镜图生成成功！\n\n![分镜图]({url})\n\n📋 **风格**：{style}"
            else:
                return "❌ 分镜图生成失败：用户API调用失败，请检查配置是否正确"
        else:
            # 使用默认配置
            url = _generate_image_with_default(prompt, ctx)
            if url:
                return f"✅ 分镜图生成成功！\n\n![分镜图]({url})\n\n📋 **风格**：{style}"
            else:
                return "❌ 分镜图生成失败：请配置图像生成API或联系管理员"
    
    except Exception as e:
        return f"❌ 分镜图生成出错：{str(e)}"


@tool
def generate_storyboard_sequence(
    scenes: List[str],
    style: str = "电影感",
    title: str = "分镜图预览",
    runtime: ToolRuntime = None
) -> str:
    """
    批量生成分镜图序列并生成宫格展示页面
    
    支持两种输入格式：
    
    **格式1：简单场景描述**（适合快速生图）
    - 输入：场景描述列表，如 ["雨夜便利店，男主独自购物", "男主转身看到女主"]
    - 工具会自动添加风格前缀和画质后缀
    
    **格式2：完整Prompt**（适合配合第二层Prompt工程使用）
    - 输入：第二层输出的"首帧参考图Prompt"列表
    - 工具直接使用传入的Prompt，不再添加额外描述
    
    Args:
        scenes: 场景描述或完整Prompt列表
        style: 画面风格（仅对简单场景描述有效）
            - 可选：电影感、日系动漫、韩系清新、写实风格、复古胶片、赛博朋克、水彩插画、黑白电影
        title: 分镜标题，将显示在宫格展示页面顶部
    
    Returns:
        宫格展示页面链接 + 所有分镜图的Markdown展示
    
    使用示例：
        # 简单描述模式
        generate_storyboard_sequence(
            scenes=["雨夜便利店，男主独自购物", "男主转身看到女主"],
            style="电影感"
        )
        
        # 完整Prompt模式（从第二层输出）
        generate_storyboard_sequence(
            scenes=[
                "远景镜头，雨夜便利店外景，霓虹灯牌在雨幕中闪烁...",
                "中景镜头，男性角色站在货架前，背影孤独..."
            ],
            style="电影感"  # 此参数会被忽略，直接使用完整Prompt
        )
    """
    try:
        import asyncio
        
        ctx = runtime.context if runtime else new_context(method="generate_storyboard_sequence")
        
        # 检查用户是否有自定义图像生成配置
        user_config = _get_user_image_config(runtime)
        
        # 智能检测输入格式并构建Prompt
        prompts = []
        for scene in scenes:
            # 检测是否为完整Prompt（包含专业术语）
            is_full_prompt = any(keyword in scene for keyword in [
                "镜头", "特写", "远景", "中景", "近景", "全景", "大特写",
                "视角", "构图", "光影", "景深", "运镜"
            ]) and len(scene) > 50
            
            if is_full_prompt:
                # 完整Prompt模式：直接使用，只添加质量后缀
                prompts.append(f"{scene}，高质量，专业分镜图")
            else:
                # 简单描述模式：添加风格和质量描述
                prompts.append(_build_storyboard_prompt(scene, style))
        
        images = []
        markdown_images = []
        
        if user_config:
            # 使用用户自定义配置，逐个生成
            for i, prompt in enumerate(prompts):
                url = _generate_image_with_user_config(
                    prompt=prompt,
                    api_key=user_config["api_key"],
                    base_url=user_config["base_url"]
                )
                if url:
                    images.append({
                        "url": url,
                        "description": scenes[i]
                    })
                    markdown_images.append(f"**场景{i+1}**\n\n![场景{i+1}]({url})")
        else:
            # 使用默认配置
            client = ImageGenerationClient(ctx=ctx)
            
            async def generate_all():
                tasks = [
                    client.generate_async(prompt=prompt, size="2K", watermark=False)
                    for prompt in prompts
                ]
                return await asyncio.gather(*tasks)
            
            responses = asyncio.run(generate_all())
            
            for i, (response, scene_desc) in enumerate(zip(responses, scenes)):
                if response.success and response.image_urls:
                    url = response.image_urls[0]
                    images.append({
                        "url": url,
                        "description": scene_desc
                    })
                    markdown_images.append(f"**场景{i+1}**\n\n![场景{i+1}]({url})")
        
        if not images:
            return "❌ 所有分镜图生成失败"
        
        # 生成宫格展示HTML
        html_content = _generate_grid_html(images, title)
        
        # 上传HTML到存储
        grid_url = _upload_html_to_storage(html_content, title)
        
        # 构建返回结果
        result = f"✅ 已生成 {len(images)} 张分镜图！\n\n"
        
        if grid_url:
            result += f"🎨 **宫格预览页面**：[点击查看完整分镜]({grid_url})\n\n"
        
        result += "---\n\n**分镜图预览：**\n\n"
        result += "\n\n".join(markdown_images)
        
        return result
    
    except Exception as e:
        return f"❌ 批量生成出错：{str(e)}"


# 导出工具列表
STORYBOARD_TOOLS = [generate_storyboard, generate_storyboard_sequence]
