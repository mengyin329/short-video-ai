"""
Prompt模板加载工具

负责从文件系统加载Prompt模板，支持核心模块和专业分支的Prompt加载。
"""

import os
from typing import Optional


def load_prompt_template(prompt_type: str, name: str) -> Optional[str]:
    """
    加载Prompt模板
    
    Args:
        prompt_type: 模板类型，可选值: "modules" 或 "branches"
        name: 模板名称（不含.txt后缀）
    
    Returns:
        Prompt模板内容，如果文件不存在则返回None
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    prompt_file = os.path.join(
        workspace_path, 
        "assets", 
        "prompts", 
        prompt_type, 
        f"{name}.txt"
    )
    
    if not os.path.exists(prompt_file):
        return None
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error loading prompt template {prompt_file}: {e}")
        return None


def get_module_prompt(module_name: str) -> Optional[str]:
    """
    获取核心模块的Prompt模板
    
    Args:
        module_name: 模块名称（如 story_seed, chara_weave 等）
    
    Returns:
        Prompt模板内容
    """
    return load_prompt_template("modules", module_name)


def get_branch_prompt(branch_name: str) -> Optional[str]:
    """
    获取专业分支的Prompt模板
    
    Args:
        branch_name: 分支名称（如 ad_narrative_weave, edu_story_weave 等）
    
    Returns:
        Prompt模板内容
    """
    return load_prompt_template("branches", branch_name)


# 核心模块名称映射
MODULE_NAMES = {
    "story_seed": "故事种子孵化器",
    "chara_weave": "角色关系编织师",
    "rhythm_master": "叙事节拍控制师",
    "dialogue_forge": "对话铸造师"
}

# 专业分支名称映射
BRANCH_NAMES = {
    "ad_narrative_weave": "剧情类广告植入师",
    "edu_story_weave": "知识科普编织师",
    "healing_narrative": "情感治愈编剧师",
    "group_drama_director": "多人群戏导师",
    "romance_script_writer": "情侣关系编剧师",
    "workplace_drama_writer": "职场关系编剧师",
    "mystery_logic_master": "悬疑推理逻辑师",
    "action_pace_director": "快节奏动作编剧师"
}


def list_available_prompts() -> dict:
    """
    列出所有可用的Prompt模板
    
    Returns:
        包含所有可用模板信息的字典
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    
    result = {
        "modules": {},
        "branches": {}
    }
    
    # 检查核心模块
    for module_name in MODULE_NAMES.keys():
        prompt = get_module_prompt(module_name)
        if prompt:
            result["modules"][module_name] = {
                "display_name": MODULE_NAMES[module_name],
                "available": True,
                "length": len(prompt)
            }
        else:
            result["modules"][module_name] = {
                "display_name": MODULE_NAMES[module_name],
                "available": False,
                "length": 0
            }
    
    # 检查专业分支
    for branch_name in BRANCH_NAMES.keys():
        prompt = get_branch_prompt(branch_name)
        if prompt:
            result["branches"][branch_name] = {
                "display_name": BRANCH_NAMES[branch_name],
                "available": True,
                "length": len(prompt)
            }
        else:
            result["branches"][branch_name] = {
                "display_name": BRANCH_NAMES[branch_name],
                "available": False,
                "length": 0
            }
    
    return result
