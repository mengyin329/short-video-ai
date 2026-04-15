"""
短视频AI编剧助手 - Web可视化界面

提供美观的可视化界面，包含侧边栏、按钮、表单、卡片等元素。
支持剧本创作、分镜图生成、场景设定图生成、角色设定图生成。

⚠️ 零消耗方案：用户需配置自己的API Key才能使用
"""

import gradio as gr
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

# 配置说明内容
CONFIG_GUIDE = """
<div style="padding: 15px;">
    <h3 style="color: #ff6b6b; margin: 0 0 15px 0; font-size: 1.1rem;">⚠️ 首次使用必读</h3>
    
    <p style="color: #ccc; font-size: 0.9rem; line-height: 1.8; margin-bottom: 15px;">
        本服务采用<b style="color:#4a9eff">零消耗方案</b>，需要您配置自己的API才能使用。
        所有API调用将直接使用您的账户，服务提供方<b style="color:#ff6b6b">零成本运营</b>。
    </p>
    
    <h4 style="color: #4a9eff; margin: 15px 0 10px 0;">📋 需要配置的内容</h4>
    
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 12px; margin-bottom: 10px;">
        <p style="color: #ff6b6b; margin: 0 0 8px 0; font-weight: bold;">1️⃣ 大模型 API（必填）</p>
        <p style="color: #888; margin: 0; font-size: 0.85rem;">
            • <b>API Key</b>：服务商提供的密钥（如 sk-xxxx）<br>
            • <b>Base URL</b>：API接口地址<br>
            • <b>模型名称</b>：如 gpt-4o、doubao-3.5、deepseek-chat
        </p>
    </div>
    
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 12px; margin-bottom: 15px;">
        <p style="color: #4a9eff; margin: 0 0 8px 0; font-weight: bold;">2️⃣ 图像生成 API（可选）</p>
        <p style="color: #888; margin: 0; font-size: 0.85rem;">
            用于生成分镜图、场景设定图、角色设定图<br>
            不配置则无法使用图像生成功能
        </p>
    </div>
    
    <h4 style="color: #4a9eff; margin: 15px 0 10px 0;">💡 支持的服务商</h4>
    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;">
        <span style="background: rgba(74,158,255,0.2); padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; color: #4a9eff;">OpenAI</span>
        <span style="background: rgba(74,158,255,0.2); padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; color: #4a9eff;">豆包/火山引擎</span>
        <span style="background: rgba(74,158,255,0.2); padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; color: #4a9eff;">DeepSeek</span>
        <span style="background: rgba(74,158,255,0.2); padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; color: #4a9eff;">Kimi/月之暗面</span>
        <span style="background: rgba(74,158,255,0.2); padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; color: #4a9eff;">其他 OpenAI 兼容 API</span>
    </div>
    
    <div style="background: rgba(255,107,107,0.1); border-radius: 10px; padding: 12px; border: 1px solid rgba(255,107,107,0.3);">
        <p style="color: #ff6b6b; margin: 0; font-size: 0.85rem;">
            🔒 <b>安全提示</b>：您的API Key仅存储在本地浏览器中，不会上传到服务器。
        </p>
    </div>
</div>
"""

# 使用说明内容
WELCOME_GUIDE = """
<div style="padding: 10px 0;">
    <p style="color: #aaa; font-size: 0.95rem; line-height: 1.8;">
        我是你的短视频AI编剧助手，可以帮你完成从创意构思到完整剧本的全流程创作，还能生成可视化素材。
    </p>
    
    <h3 style="color: #4a9eff; margin: 20px 0 12px 0; font-size: 1rem;">🎯 我能做什么</h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
        <tr>
            <td style="padding: 8px; color: #888;">📝 <b style="color:#fff">剧本创作</b></td>
            <td style="padding: 8px; color: #ccc;">完整剧本、故事大纲、角色设计、台词优化</td>
        </tr>
        <tr>
            <td style="padding: 8px; color: #888;">🎬 <b style="color:#fff">分镜图生成</b></td>
            <td style="padding: 8px; color: #ccc;">单个/批量分镜图，自动生成宫格展示</td>
        </tr>
        <tr>
            <td style="padding: 8px; color: #888;">🏙️ <b style="color:#fff">场景设定图</b></td>
            <td style="padding: 8px; color: #ccc;">8种风格，可上传参考图生成场景概念</td>
        </tr>
        <tr>
            <td style="padding: 8px; color: #888;">👤 <b style="color:#fff">角色设定图</b></td>
            <td style="padding: 8px; color: #ccc;">8种风格，支持演员照片参考、三视图</td>
        </tr>
    </table>
    
    <h3 style="color: #4a9eff; margin: 20px 0 12px 0; font-size: 1rem;">💡 快速上手</h3>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin: 10px 0;">
        <p style="color: #ccc; margin: 0 0 10px 0; font-size: 0.9rem;">
            <b style="color:#ff6b6b">方式一：</b>直接描述你的需求
        </p>
        <p style="color: #888; margin: 0; font-size: 0.85rem; padding-left: 15px;">
            "帮我创作一个30秒的职场逆袭短视频"<br>
            "生成一个深夜便利店的场景设定图"<br>
            "为这个角色生成设定图：25岁都市白领女性"
        </p>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin: 10px 0;">
        <p style="color: #ccc; margin: 0 0 10px 0; font-size: 0.9rem;">
            <b style="color:#ff6b6b">方式二：</b>使用下方表单
        </p>
        <p style="color: #888; margin: 0; font-size: 0.85rem; padding-left: 15px;">
            选择模式 → 填写需求 → 点击「开始创作」
        </p>
    </div>
    
    <h3 style="color: #4a9eff; margin: 20px 0 12px 0; font-size: 1rem;">🌿 三种创作模式</h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 10px 8px; color: #fff; font-weight: bold;">🔄 完整流程</td>
            <td style="padding: 10px 8px; color: #aaa;">从创意到剧本的完整创作链路</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 10px 8px; color: #fff; font-weight: bold;">🧩 模块化</td>
            <td style="padding: 10px 8px; color: #aaa;">单独使用某个模块（角色/节奏/台词）</td>
        </tr>
        <tr>
            <td style="padding: 10px 8px; color: #fff; font-weight: bold;">🌿 专业分支</td>
            <td style="padding: 10px 8px; color: #aaa;">悬疑/爱情/职场/治愈等专项创作</td>
        </tr>
    </table>
</div>
"""

# 自定义CSS样式
CUSTOM_CSS = """
.gradio-container {
    font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif !important;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

footer {display: none !important;}

/* 标题 */
.app-title {
    text-align: center;
    padding: 20px 0;
}

.app-title h1 {
    color: #fff !important;
    font-size: 2rem !important;
    margin-bottom: 5px;
}

.app-title p {
    color: #888 !important;
    font-size: 0.9rem;
}

/* 卡片样式 */
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

.card-title {
    color: #4a9eff;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(74,158,255,0.3);
}

/* 配置状态卡片 */
.config-status-card {
    background: rgba(0,0,0,0.3);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
}

.config-status-configured {
    background: rgba(76,175,80,0.15);
    border: 1px solid rgba(76,175,80,0.3);
}

.config-status-not-configured {
    background: rgba(255,107,107,0.15);
    border: 1px solid rgba(255,107,107,0.3);
}

/* 输入组件 */
input, textarea, select {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #4a9eff !important;
}

::placeholder {
    color: #555 !important;
}

label span {
    color: #ccc !important;
}

/* 按钮 */
.primary-btn {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
}

.primary-btn:disabled {
    background: rgba(100,100,100,0.3) !important;
    color: rgba(255,255,255,0.3) !important;
}

.secondary-btn {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

.config-btn {
    background: linear-gradient(135deg, #4a9eff 0%, #0066cc 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: bold !important;
}

/* 模式选择按钮 */
.mode-btn {
    width: 100%;
    text-align: left !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #fff !important;
    padding: 12px 15px !important;
    margin: 5px 0 !important;
}

.mode-btn:hover {
    background: rgba(74,158,255,0.2) !important;
}

.mode-btn-selected {
    background: linear-gradient(135deg, #4a9eff 0%, #0066cc 100%) !important;
    border-color: #4a9eff !important;
}

/* 模块选择 */
.module-radio label {
    background: rgba(0,0,0,0.2) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin: 3px 0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

.module-radio label:has(input:checked) {
    background: rgba(74,158,255,0.3) !important;
    border-color: #4a9eff !important;
}

/* 输出区域 */
.output-box {
    background: rgba(0,0,0,0.4) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

.output-box .markdown-text {
    color: #e0e0e0 !important;
}

/* 标签页 */
.tabs > .tab-nav {
    background: rgba(0,0,0,0.3) !important;
    border-radius: 12px;
    padding: 5px;
    margin-bottom: 20px;
}

.tabs > .tab-nav > button {
    background: transparent !important;
    color: #888 !important;
    border-radius: 8px !important;
}

.tabs > .tab-nav > button.selected {
    background: linear-gradient(135deg, #4a9eff 0%, #0066cc 100%) !important;
    color: white !important;
}

/* 快捷按钮 */
.quick-btn {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #fff !important;
    padding: 10px !important;
    text-align: center !important;
}

.quick-btn:hover {
    background: rgba(74,158,255,0.2) !important;
    border-color: #4a9eff !important;
}

/* 欢迎指南样式 */
.welcome-guide {
    background: rgba(0,0,0,0.2) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    margin-bottom: 20px !important;
}

.welcome-guide .label-wrap {
    background: linear-gradient(135deg, rgba(74,158,255,0.2) 0%, rgba(0,102,204,0.2) 100%) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}

.welcome-guide summary {
    color: #4a9eff !important;
    font-weight: bold !important;
    font-size: 1rem !important;
}
"""

def get_config_status_html(config):
    """获取配置状态HTML"""
    if config and config.get("api_key") and config.get("base_url") and config.get("model"):
        return """
            <div class="config-status-card config-status-configured">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5rem;">✅</span>
                    <div>
                        <div style="color: #4caf50; font-weight: bold;">已配置</div>
                        <div style="color: #888; font-size: 0.85rem;">模型: """ + config.get("model", "") + """</div>
                    </div>
                </div>
            </div>
        """
    else:
        return """
            <div class="config-status-card config-status-not-configured">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5rem;">⚠️</span>
                    <div>
                        <div style="color: #ff6b6b; font-weight: bold;">未配置</div>
                        <div style="color: #888; font-size: 0.85rem;">请先配置您的API才能使用</div>
                    </div>
                </div>
            </div>
        """

def call_agent(message: str, config: dict) -> str:
    """调用Agent进行创作"""
    try:
        # 动态创建Agent实例
        agent = build_agent(user_config=config)
        config_dict = {"configurable": {"thread_id": "web_ui_session"}}
        result = agent.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config_dict
        )
        return result["messages"][-1].content
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "unauthorized" in error_msg.lower():
            return f"❌ API认证失败，请检查您的API Key是否正确。\n\n错误信息：{error_msg}"
        elif "base_url" in error_msg.lower() or "connection" in error_msg.lower():
            return f"❌ 无法连接到API服务，请检查Base URL是否正确。\n\n错误信息：{error_msg}"
        else:
            return f"❌ 创作过程中出现错误: {error_msg}"

def create_interface():
    """创建Gradio界面"""
    
    with gr.Blocks(css=CUSTOM_CSS, title="短视频AI编剧助手") as demo:
        
        # 用户配置状态（使用 gr.State 存储）
        user_config = gr.State(value=None)
        
        # 标题
        gr.HTML("""
            <div class="app-title">
                <h1>🎬 短视频AI编剧助手</h1>
                <p>专业剧本创作 · 智能流程引导 · 多模式切换 · 零消耗方案</p>
            </div>
        """)
        
        # ===== 配置区域（折叠） =====
        with gr.Accordion("⚙️ API 配置（点击展开/收起）", open=True):
            gr.HTML(CONFIG_GUIDE)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # 大模型配置
                    gr.HTML('<div style="color: #ff6b6b; font-weight: bold; margin-bottom: 10px;">1️⃣ 大模型 API（必填）</div>')
                    
                    api_key = gr.Textbox(
                        label="API Key",
                        placeholder="sk-xxxxxxxx",
                        type="password",
                    )
                    
                    base_url = gr.Textbox(
                        label="Base URL",
                        placeholder="https://api.openai.com/v1",
                    )
                    
                    model = gr.Textbox(
                        label="模型名称",
                        placeholder="gpt-4o / doubao-3.5 / deepseek-chat",
                    )
                    
                    temperature = gr.Slider(
                        label="Temperature（可选）",
                        minimum=0,
                        maximum=2,
                        step=0.1,
                        value=0.7,
                    )
                
                with gr.Column(scale=1):
                    # 图像生成配置（可选）
                    gr.HTML('<div style="color: #4a9eff; font-weight: bold; margin-bottom: 10px;">2️⃣ 图像生成 API（可选）</div>')
                    
                    image_api_key = gr.Textbox(
                        label="Image API Key",
                        placeholder="sk-xxxxxxxx",
                        type="password",
                    )
                    
                    image_base_url = gr.Textbox(
                        label="Image Base URL",
                        placeholder="https://api.openai.com/v1",
                    )
                    
                    gr.HTML("""
                        <div style="margin-top: 20px; padding: 10px; background: rgba(74,158,255,0.1); border-radius: 8px; border: 1px solid rgba(74,158,255,0.2);">
                            <p style="color: #4a9eff; margin: 0; font-size: 0.85rem;">
                                💡 图像生成API用于分镜图、场景设定图、角色设定图生成
                            </p>
                        </div>
                    """)
            
            with gr.Row():
                save_config_btn = gr.Button("💾 保存配置", variant="primary", elem_classes=["config-btn"], scale=2)
                reset_config_btn = gr.Button("🔄 重置配置", elem_classes=["secondary-btn"], scale=1)
            
            # 配置状态显示
            config_status = gr.HTML(get_config_status_html(None))
        
        # 欢迎页使用说明（可折叠）
        with gr.Row():
            with gr.Column():
                with gr.Accordion("📖 使用说明（点击展开/收起）", open=False, elem_classes=["welcome-guide"]):
                    gr.HTML(WELCOME_GUIDE)
        
        with gr.Row():
            # 左侧边栏
            with gr.Column(scale=1, min_width=300):
                
                # 模式选择卡片
                with gr.Group():
                    gr.HTML('<div class="card-title">📱 选择模式</div>')
                    
                    mode = gr.Radio(
                        choices=[
                            ("🔄 完整流程模式", "full"),
                            ("🧩 模块化模式", "module"),
                            ("🌿 专业分支模式", "branch"),
                        ],
                        value="full",
                        label="",
                        container=False,
                    )
                
                # 核心模块选择
                with gr.Group(visible=False) as modules_group:
                    gr.HTML('<div class="card-title">🎯 选择核心模块</div>')
                    module = gr.Radio(
                        choices=[
                            ("🌱 故事种子孵化器", "story_seed"),
                            ("👥 角色关系编织师", "chara_weave"),
                            ("🎼 叙事节拍控制师", "rhythm_master"),
                            ("💬 对话铸造师", "dialogue_forge"),
                        ],
                        value=None,
                        label="",
                        container=False,
                        elem_classes=["module-radio"]
                    )
                
                # 专业分支选择
                with gr.Group(visible=False) as branches_group:
                    gr.HTML('<div class="card-title">🌿 选择专业分支</div>')
                    branch = gr.Radio(
                        choices=[
                            ("🎯 剧情类广告植入师", "ad_narrative_weave"),
                            ("📚 知识科普编织师", "edu_story_weave"),
                            ("💚 情感治愈编剧师", "healing_narrative"),
                            ("🎬 多人群戏导师", "group_drama_director"),
                            ("💕 情侣关系编剧师", "romance_script_writer"),
                            ("💼 职场关系编剧师", "workplace_drama_writer"),
                            ("🔍 悬疑推理逻辑师", "mystery_logic_master"),
                            ("💥 快节奏动作编剧师", "action_pace_director"),
                        ],
                        value=None,
                        label="",
                        container=False,
                        elem_classes=["module-radio"]
                    )
                
                # 当前选择
                current_selection = gr.HTML("""
                    <div style="background: rgba(74,158,255,0.15); border-radius: 10px; padding: 15px; margin-top: 15px; border: 1px solid rgba(74,158,255,0.3);">
                        <div style="color: #4a9eff; font-size: 0.85rem;">当前选择</div>
                        <div style="color: #fff; font-size: 1rem; font-weight: bold; margin-top: 5px;">🔄 完整流程模式</div>
                    </div>
                """)
            
            # 主内容区
            with gr.Column(scale=2):
                
                # 创作表单
                with gr.Group():
                    gr.HTML('<div class="card-title">📝 创作需求</div>')
                    
                    with gr.Row():
                        content_type = gr.Dropdown(
                            choices=["情感治愈", "职场逆袭", "悬疑推理", "搞笑喜剧", "知识科普", "爱情故事", "动作场面", "广告植入", "其他"],
                            label="🎭 内容类型",
                            value="情感治愈",
                            scale=1
                        )
                        duration = gr.Radio(
                            choices=["30秒", "1分钟", "2分钟", "3分钟"],
                            label="⏱️ 视频时长",
                            value="1分钟",
                            scale=1
                        )
                    
                    with gr.Row():
                        audience = gr.Dropdown(
                            choices=["年轻人(18-25)", "职场人(25-35)", "中年群体(35-50)", "全年龄段", "特定群体"],
                            label="👥 目标受众",
                            value="年轻人(18-25)",
                            scale=1
                        )
                        theme = gr.Textbox(
                            label="💡 核心主题",
                            placeholder="例如：陌生人的善意、职场逆袭...",
                            scale=1
                        )
                    
                    key_elements = gr.Textbox(
                        label="🎬 关键情节/场景（选填）",
                        placeholder="例如：雨天递伞、深夜便利店...",
                    )
                    
                    description = gr.Textbox(
                        label="📝 详细创作需求",
                        placeholder="请详细描述你想要创作的内容...",
                        lines=4
                    )
                    
                    # 快捷场景
                    gr.HTML("""
                        <div style="margin-top: 10px;">
                            <div style="color: #888; font-size: 0.85rem; margin-bottom: 8px;">⚡ 快捷场景</div>
                        </div>
                    """)
                    
                    with gr.Row():
                        quick_1 = gr.Button("💼 职场逆袭", elem_classes=["quick-btn"])
                        quick_2 = gr.Button("💚 情感治愈", elem_classes=["quick-btn"])
                        quick_3 = gr.Button("🔍 悬疑推理", elem_classes=["quick-btn"])
                        quick_4 = gr.Button("💕 爱情故事", elem_classes=["quick-btn"])
                    
                    with gr.Row():
                        create_btn = gr.Button("🚀 开始创作", variant="primary", elem_classes=["primary-btn"], scale=3)
                        clear_btn = gr.Button("🗑️ 清空", elem_classes=["secondary-btn"], scale=1)
                
                # 输出区域
                output = gr.Markdown(
                    value="⚠️ **请先配置您的API**\n\n在上方「API 配置」区域填写您的API Key、Base URL和模型名称，然后点击「保存配置」。\n\n配置完成后即可开始创作。",
                    elem_classes=["output-box"],
                    label="📜 创作结果"
                )
        
        # ===== 事件处理 =====
        
        def save_config(api_key, base_url, model, temperature, image_api_key, image_base_url):
            """保存用户配置"""
            if not api_key or not base_url or not model:
                return None, get_config_status_html(None), "⚠️ 请填写必填项（API Key、Base URL、模型名称）"
            
            config = {
                "api_key": api_key,
                "base_url": base_url,
                "model": model,
                "temperature": temperature,
                "image_api_key": image_api_key if image_api_key else None,
                "image_base_url": image_base_url if image_base_url else None,
            }
            
            return config, get_config_status_html(config), "✅ 配置保存成功！现在可以开始创作了。"
        
        def reset_config():
            """重置配置"""
            return None, get_config_status_html(None), "", "", "", 0.7, "", ""
        
        def update_mode(mode):
            """更新模式选择"""
            modules_visible = mode == "module"
            branches_visible = mode == "branch"
            
            mode_names = {
                "full": "🔄 完整流程模式",
                "module": "🧩 模块化模式",
                "branch": "🌿 专业分支模式"
            }
            
            selection_html = f"""
                <div style="background: rgba(74,158,255,0.15); border-radius: 10px; padding: 15px; margin-top: 15px; border: 1px solid rgba(74,158,255,0.3);">
                    <div style="color: #4a9eff; font-size: 0.85rem;">当前选择</div>
                    <div style="color: #fff; font-size: 1rem; font-weight: bold; margin-top: 5px;">{mode_names.get(mode, mode)}</div>
                </div>
            """
            
            return gr.update(visible=modules_visible), gr.update(visible=branches_visible), selection_html
        
        def on_create(config, mode, module, branch, content_type, duration, audience, theme, key_elements, description):
            """创建内容"""
            # 检查配置
            if not config or not config.get("api_key") or not config.get("base_url") or not config.get("model"):
                return "⚠️ **请先配置您的API**\n\n在上方「API 配置」区域填写您的API Key、Base URL和模型名称，然后点击「保存配置」。"
            
            prompt_parts = []
            
            # 根据模式添加提示
            if mode == "full":
                prompt_parts.append("请使用完整流程模式，按照故事孵化→角色设计→节奏规划→台词创作的顺序，帮我创作一个短视频剧本：\n")
            elif mode == "module" and module:
                module_names = {
                    "story_seed": "故事种子孵化器",
                    "chara_weave": "角色关系编织师",
                    "rhythm_master": "叙事节拍控制师",
                    "dialogue_forge": "对话铸造师",
                }
                prompt_parts.append(f"请使用「{module_names.get(module, module)}」模块，帮我完成以下创作：\n")
            elif mode == "branch" and branch:
                branch_names = {
                    "ad_narrative_weave": "剧情类广告植入师",
                    "edu_story_weave": "知识科普编织师",
                    "healing_narrative": "情感治愈编剧师",
                    "group_drama_director": "多人群戏导师",
                    "romance_script_writer": "情侣关系编剧师",
                    "workplace_drama_writer": "职场关系编剧师",
                    "mystery_logic_master": "悬疑推理逻辑师",
                    "action_pace_director": "快节奏动作编剧师",
                }
                prompt_parts.append(f"请使用「{branch_names.get(branch, branch)}」专业分支，帮我完成以下创作：\n")
            
            if content_type:
                prompt_parts.append(f"内容类型：{content_type}")
            if duration:
                prompt_parts.append(f"视频时长：{duration}")
            if audience:
                prompt_parts.append(f"目标受众：{audience}")
            if theme:
                prompt_parts.append(f"核心主题：{theme}")
            if key_elements:
                prompt_parts.append(f"关键元素：{key_elements}")
            if description:
                prompt_parts.append(f"详细需求：{description}")
            
            if len(prompt_parts) <= 1:
                return "⚠️ 请填写至少一项创作需求...\n\n你可以在上方选择内容类型、时长、受众等基本信息，或者直接在详细需求中描述你想创作的内容。"
            
            full_prompt = "\n".join(prompt_parts)
            return call_agent(full_prompt, config)
        
        def clear_form():
            return "情感治愈", "1分钟", "年轻人(18-25)", "", "", "", "*创作结果将在这里显示...*\n\n请在上方填写创作需求，然后点击「开始创作」按钮。"
        
        def quick_fill_1():
            return "职场逆袭", "职场人(25-35)", "职场反击", "", "我想创作一个职场新人被老员工抢功劳后，用专业能力反击的故事。主角是一个刚入职的女生，看起来软萌但内心很有实力。"
        
        def quick_fill_2():
            return "情感治愈", "年轻人(18-25)", "陌生人的善意", "", "我想创作一个人在低谷时收到陌生人善意的治愈故事。主角是一个在大城市打拼的年轻人，刚刚经历挫折感到很迷茫。"
        
        def quick_fill_3():
            return "悬疑推理", "年轻人(18-25)", "真相揭秘", "", "我想创作一个看似普通的案件背后隐藏惊人真相的悬疑故事。要有反转，让观众猜不到结局。"
        
        def quick_fill_4():
            return "爱情故事", "年轻人(18-25)", "心动瞬间", "", "我想创作两个人从误会到相爱的甜蜜爱情故事。要有很多让人心动的浪漫时刻。"
        
        # 绑定配置事件
        save_config_btn.click(
            save_config,
            inputs=[api_key, base_url, model, temperature, image_api_key, image_base_url],
            outputs=[user_config, config_status, output]
        )
        
        reset_config_btn.click(
            reset_config,
            outputs=[user_config, config_status, api_key, base_url, model, temperature, image_api_key, image_base_url]
        )
        
        # 绑定模式事件
        mode.change(update_mode, inputs=[mode], outputs=[modules_group, branches_group, current_selection])
        
        # 绑定创作事件
        create_btn.click(
            on_create,
            inputs=[user_config, mode, module, branch, content_type, duration, audience, theme, key_elements, description],
            outputs=[output]
        )
        
        clear_btn.click(clear_form, outputs=[content_type, duration, audience, theme, key_elements, description, output])
        
        quick_1.click(quick_fill_1, outputs=[content_type, audience, theme, key_elements, description])
        quick_2.click(quick_fill_2, outputs=[content_type, audience, theme, key_elements, description])
        quick_3.click(quick_fill_3, outputs=[content_type, audience, theme, key_elements, description])
        quick_4.click(quick_fill_4, outputs=[content_type, audience, theme, key_elements, description])
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
