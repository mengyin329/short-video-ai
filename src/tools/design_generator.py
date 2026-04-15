"""
场景设定图和角色设定图生成工具

支持上传参考图+提示词描述生成场景设定图和角色设定图。
支持用户自定义图像生成API配置。
"""

import os
from typing import Optional, List, Dict
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import ImageGenerationClient
from coze_coding_utils.runtime_ctx.context import new_context
import requests


# 用户配置的 Header 名称
HEADER_USER_IMAGE_API_KEY = "x-user-image-api-key"
HEADER_USER_IMAGE_BASE_URL = "x-user-image-model"


def _get_user_image_config(runtime: ToolRuntime) -> Optional[Dict[str, str]]:
    """从运行时上下文获取用户图像生成配置"""
    if not runtime or not runtime.context:
        return None
    
    ctx = runtime.context
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


# 场景风格预设
SCENE_STYLES = {
    "现代都市": "modern city scene, contemporary architecture, urban environment, realistic lighting",
    "复古怀旧": "vintage setting, nostalgic atmosphere, retro details, warm tones, film look",
    "科幻未来": "sci-fi futuristic scene, neon lights, cyberpunk elements, high-tech environment",
    "日系清新": "Japanese style scene, soft natural lighting, pastel colors, anime background",
    "中式古风": "Chinese traditional scene, ancient architecture, oriental aesthetics, ink painting style",
    "欧式古典": "European classical scene, baroque architecture, elegant interior, oil painting style",
    "暗黑风格": "dark moody scene, dramatic lighting, gothic atmosphere, high contrast",
    "自然风光": "natural landscape, outdoor scenery, golden hour lighting, cinematic composition"
}

# 角色风格预设
CHARACTER_STYLES = {
    "写实真人": "photorealistic portrait, real person style, natural skin texture, studio lighting, high detail",
    "日系动漫": "anime character design, Japanese animation style, clean lines, expressive eyes, vibrant colors",
    "美式卡通": "American cartoon style, stylized character, bold outlines, exaggerated features",
    "韩系插画": "Korean illustration style, soft features, pastel colors, romantic atmosphere",
    "水墨国风": "Chinese ink painting style, traditional oriental aesthetics, elegant brush strokes",
    "赛博朋克": "cyberpunk character, futuristic fashion, neon accents, tech elements",
    "奇幻风格": "fantasy character design, magical elements, ethereal glow, detailed costume",
    "像素风格": "pixel art character, retro game style, limited color palette, 8-bit aesthetic"
}


def _build_scene_prompt(
    description: str,
    style: str = "现代都市",
    time_of_day: str = "",
    weather: str = "",
    atmosphere: str = ""
) -> str:
    """构建场景设定图Prompt"""
    style_prompt = SCENE_STYLES.get(style, SCENE_STYLES["现代都市"])
    
    prompt_parts = [
        f"Scene concept art, {style_prompt}",
        f"Scene: {description}"
    ]
    
    if time_of_day:
        prompt_parts.append(f"Time: {time_of_day}")
    if weather:
        prompt_parts.append(f"Weather: {weather}")
    if atmosphere:
        prompt_parts.append(f"Atmosphere: {atmosphere}")
    
    prompt_parts.extend([
        "professional concept art, production ready, high quality",
        "detailed environment design, suitable for film or game production"
    ])
    
    return ", ".join(prompt_parts)


def _build_character_prompt(
    description: str,
    style: str = "写实真人",
    gender: str = "",
    age: str = "",
    clothing: str = "",
    expression: str = "",
    pose: str = ""
) -> str:
    """构建角色设定图Prompt"""
    style_prompt = CHARACTER_STYLES.get(style, CHARACTER_STYLES["写实真人"])
    
    prompt_parts = [
        f"Character design sheet, {style_prompt}",
        f"Character: {description}"
    ]
    
    if gender:
        prompt_parts.append(f"Gender: {gender}")
    if age:
        prompt_parts.append(f"Age: {age}")
    if clothing:
        prompt_parts.append(f"Clothing: {clothing}")
    if expression:
        prompt_parts.append(f"Expression: {expression}")
    if pose:
        prompt_parts.append(f"Pose: {pose}")
    
    prompt_parts.extend([
        "character reference sheet, multiple angles preferred",
        "professional character design, production ready"
    ])
    
    return ", ".join(prompt_parts)


@tool
def generate_scene_concept(
    description: str,
    reference_image: str = "",
    style: str = "现代都市",
    time_of_day: str = "",
    weather: str = "",
    atmosphere: str = "",
    runtime: ToolRuntime = None
) -> str:
    """
    生成场景设定图
    
    根据描述生成专业的场景设定图，可上传参考图进行风格参考。
    适用于电影、游戏、短视频的场景概念设计。
    
    Args:
        description: 场景描述（必需），详细描述场景的环境、建筑、物品等
        reference_image: 参考图URL（可选），上传参考图片，AI会参考图片风格进行生成
        style: 场景风格，可选：现代都市、复古怀旧、科幻未来、日系清新、中式古风、欧式古典、暗黑风格、自然风光
        time_of_day: 时间设定（可选），如：清晨、正午、黄昏、深夜
        weather: 天气设定（可选），如：晴天、阴天、雨天、雪天
        atmosphere: 氛围设定（可选），如：温馨、紧张、神秘、热闹
    
    Returns:
        生成的场景设定图（Markdown图片格式）
    """
    try:
        ctx = runtime.context if runtime else new_context(method="generate_scene_concept")
        
        prompt = _build_scene_prompt(
            description=description,
            style=style,
            time_of_day=time_of_day,
            weather=weather,
            atmosphere=atmosphere
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
                result = f"✅ 场景设定图生成成功！\n\n"
                result += f"![场景设定图]({url})\n\n"
                result += f"📋 **风格**：{style}\n"
                if time_of_day:
                    result += f"⏰ **时间**：{time_of_day}\n"
                if atmosphere:
                    result += f"🎭 **氛围**：{atmosphere}\n"
                return result
            else:
                return "❌ 场景设定图生成失败：用户API调用失败，请检查配置是否正确"
        else:
            # 使用默认配置
            client = ImageGenerationClient(ctx=ctx)
            
            if reference_image:
                response = client.generate(
                    prompt=prompt,
                    image=reference_image,
                    size="2K",
                    watermark=False
                )
            else:
                response = client.generate(
                    prompt=prompt,
                    size="2K",
                    watermark=False
                )
            
            if response.success and response.image_urls:
                url = response.image_urls[0]
                result = f"✅ 场景设定图生成成功！\n\n"
                result += f"![场景设定图]({url})\n\n"
                result += f"📋 **风格**：{style}\n"
                if time_of_day:
                    result += f"⏰ **时间**：{time_of_day}\n"
                if weather:
                    result += f"🌤️ **天气**：{weather}\n"
                if atmosphere:
                    result += f"🎭 **氛围**：{atmosphere}\n"
                if reference_image:
                    result += f"📷 **参考图**：已参考上传图片风格\n"
                return result
            else:
                return f"❌ 场景设定图生成失败：请配置图像生成API或联系管理员"
    
    except Exception as e:
        return f"❌ 场景设定图生成出错：{str(e)}"


@tool
def generate_character_design(
    description: str,
    reference_image: str = "",
    style: str = "写实真人",
    gender: str = "",
    age: str = "",
    clothing: str = "",
    expression: str = "",
    pose: str = "",
    runtime: ToolRuntime = None
) -> str:
    """
    生成角色设定图
    
    根据描述生成专业的角色设定图，可上传参考图进行风格参考。
    适用于电影、游戏、短视频的角色设计。
    
    Args:
        description: 角色描述（必需），详细描述角色的外貌、特征、气质等
        reference_image: 参考图URL（可选），上传参考图片，AI会参考图片中的人物进行生成
        style: 角色风格，可选：写实真人、日系动漫、美式卡通、韩系插画、水墨国风、赛博朋克、奇幻风格、像素风格
        gender: 性别（可选）
        age: 年龄（可选），如：20多岁、中年、老年
        clothing: 服装描述（可选）
        expression: 表情（可选），如：微笑、严肃、悲伤、惊讶
        pose: 姿势（可选），如：站立、坐着、奔跑、回眸
    
    Returns:
        生成的角色设定图（Markdown图片格式）
    """
    try:
        ctx = runtime.context if runtime else new_context(method="generate_character_design")
        
        prompt = _build_character_prompt(
            description=description,
            style=style,
            gender=gender,
            age=age,
            clothing=clothing,
            expression=expression,
            pose=pose
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
                result = f"✅ 角色设定图生成成功！\n\n"
                result += f"![角色设定图]({url})\n\n"
                result += f"📋 **风格**：{style}\n"
                if gender:
                    result += f"👤 **性别**：{gender}\n"
                if age:
                    result += f"📅 **年龄**：{age}\n"
                if clothing:
                    result += f"👔 **服装**：{clothing}\n"
                if expression:
                    result += f"😊 **表情**：{expression}\n"
                return result
            else:
                return "❌ 角色设定图生成失败：用户API调用失败，请检查配置是否正确"
        else:
            # 使用默认配置
            client = ImageGenerationClient(ctx=ctx)
            
            if reference_image:
                response = client.generate(
                    prompt=prompt,
                    image=reference_image,
                    size="2K",
                    watermark=False
                )
            else:
                response = client.generate(
                    prompt=prompt,
                    size="2K",
                    watermark=False
                )
            
            if response.success and response.image_urls:
                url = response.image_urls[0]
                result = f"✅ 角色设定图生成成功！\n\n"
                result += f"![角色设定图]({url})\n\n"
                result += f"📋 **风格**：{style}\n"
                if gender:
                    result += f"👤 **性别**：{gender}\n"
                if age:
                    result += f"📅 **年龄**：{age}\n"
                if clothing:
                    result += f"👔 **服装**：{clothing}\n"
                if expression:
                    result += f"😊 **表情**：{expression}\n"
                if pose:
                    result += f"🧍 **姿势**：{pose}\n"
                if reference_image:
                    result += f"📷 **参考图**：已参考上传图片\n"
                return result
            else:
                return f"❌ 角色设定图生成失败：请配置图像生成API或联系管理员"
    
    except Exception as e:
        return f"❌ 角色设定图生成出错：{str(e)}"


@tool
def generate_character_turnaround(
    description: str,
    reference_image: str = "",
    style: str = "写实真人",
    runtime: ToolRuntime = None
) -> str:
    """
    生成角色三视图
    
    生成角色的正视图、侧视图、背视图三视图设定，
    适用于需要多角度参考的制作场景。
    
    Args:
        description: 角色描述（必需）
        reference_image: 参考图URL（可选）
        style: 角色风格
    
    Returns:
        角色三视图（Markdown图片格式）
    """
    try:
        ctx = runtime.context if runtime else new_context(method="generate_character_turnaround")
        
        # 构建三视图Prompt
        prompt = f"Character turnaround sheet, {CHARACTER_STYLES.get(style, CHARACTER_STYLES['写实真人'])}, "
        prompt += f"Character: {description}, "
        prompt += "showing front view, side view, and back view, "
        prompt += "character reference sheet, production ready"
        
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
                return f"✅ 角色三视图生成成功！\n\n![角色三视图]({url})\n\n包含：正视图、侧视图、背视图"
            else:
                return "❌ 角色三视图生成失败：用户API调用失败，请检查配置是否正确"
        else:
            # 使用默认配置
            client = ImageGenerationClient(ctx=ctx)
            
            if reference_image:
                response = client.generate(
                    prompt=prompt,
                    image=reference_image,
                    size="2K",
                    watermark=False
                )
            else:
                response = client.generate(
                    prompt=prompt,
                    size="2K",
                    watermark=False
                )
            
            if response.success and response.image_urls:
                url = response.image_urls[0]
                return f"✅ 角色三视图生成成功！\n\n![角色三视图]({url})\n\n包含：正视图、侧视图、背视图"
            else:
                return f"❌ 角色三视图生成失败：请配置图像生成API或联系管理员"
    
    except Exception as e:
        return f"❌ 角色三视图生成出错：{str(e)}"


# 导出工具列表
DESIGN_TOOLS = [generate_scene_concept, generate_character_design, generate_character_turnaround]
