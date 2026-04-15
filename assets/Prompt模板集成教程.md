# 短视频AI编剧助手 Prompt模板集成教程

## 🎯 目标

本教程将指导你如何将你自己编写的12个专业Prompt模板集成到Agent中。

---

## 📋 准备工作

你需要准备以下Prompt模板：

### 4个核心模块Prompt：
1. 故事种子孵化器 (StorySeed)
2. 角色关系编织师 (CharaWeave)
3. 叙事节拍控制师 (RhythmMaster)
4. 对话铸造师 (DialogueForge)

### 8个专业分支Prompt：
1. 剧情类广告植入师 (AdNarrativeWeave)
2. 知识科普编织师 (EduStoryWeave)
3. 情感治愈编剧师 (HealingNarrative)
4. 多人群戏导师 (GroupDramaDirector)
5. 情侣关系编剧师 (RomanceScriptWriter)
6. 职场关系编剧师 (WorkplaceDramaWriter)
7. 悬疑推理逻辑师 (MysteryLogicMaster)
8. 快节奏动作编剧师 (ActionPaceDirector)

---

## 🔧 集成步骤

### 第一步：定位Prompt文件目录

```
你的项目/
├── assets/
│   └── prompts/
│       ├── modules/        ← 核心模块Prompt放这里
│       │   ├── story_seed.txt
│       │   ├── chara_weave.txt
│       │   ├── rhythm_master.txt
│       │   └── dialogue_forge.txt
│       └── branches/       ← 专业分支Prompt放这里
│           ├── ad_narrative_weave.txt
│           ├── edu_story_weave.txt
│           ├── healing_narrative.txt
│           ├── group_drama_director.txt
│           ├── romance_script_writer.txt
│           ├── workplace_drama_writer.txt
│           ├── mystery_logic_master.txt
│           └── action_pace_director.txt
```

### 第二步：创建Prompt文件

按照上面的文件命名规范，在对应目录下创建`.txt`文件。

### 第三步：粘贴Prompt内容

将你编写好的Prompt内容直接粘贴到对应的文件中。

**示例：**

**文件：** `assets/prompts/modules/story_seed.txt`

```
# 故事种子孵化器

## 角色定义
你是一位专业的故事创意孵化专家...

## 核心能力
1. 创意评估与优化
2. 故事概念构建
3. 叙事结构选择
4. 钩子系统设计

## 工作流程
第一步：收集用户创意想法
...

## 输出格式
=== 故事概念方案 ===
...
```

### 第四步：保存并测试

保存所有文件后，Agent会自动读取你的Prompt模板。

---

## ✅ 验证集成是否成功

### 方法一：查看Agent行为

与Agent对话，观察它是否使用了你的Prompt逻辑。

### 方法二：检查日志

Agent启动时会输出日志，显示加载了哪些Prompt模板。

---

## 📝 Prompt编写建议

### 好的Prompt应该包含：

1. **角色定义**：明确Agent的身份和专业领域
2. **核心能力**：列出主要功能
3. **工作流程**：详细的执行步骤
4. **输出格式**：规定输出结构
5. **示例**：提供参考示例

### Prompt模板示例：

```
# [模块名称]

## 角色定义
你是[专业身份]，专门负责[核心职责]...

## 核心能力
1. [能力1]
2. [能力2]
3. [能力3]

## 工作流程
步骤1：[做什么]
步骤2：[做什么]
步骤3：[做什么]

## 输出格式
=== [输出标题] ===
[字段1]：...
[字段2]：...
[字段3]：...

## 示例
输入：...
输出：...
```

---

## 🚨 注意事项

1. **文件编码**：确保文件是UTF-8编码
2. **文件格式**：必须是纯文本文件（.txt）
3. **文件命名**：严格按照规定的文件名命名
4. **Prompt内容**：直接粘贴Prompt内容，不需要额外的标记或分隔符

---

## 💡 高级技巧

### 技巧1：模块间协作

在编写Prompt时，可以考虑如何让模块之间更好地协作：

```
## 输入信息
接收上一个模块的输出，包括：
- 故事核心概念
- 主要角色
- 情感基调

## 处理逻辑
基于输入信息，进行...
```

### 技巧2：专业分支的独立性

专业分支的Prompt应该是独立的，不依赖核心模块：

```
## 独立工作能力
即使没有前置信息，也能独立完成创作任务...
```

### 技巧3：输出标准化

为每个模块定义清晰的输出格式，便于后续模块使用：

```
## 标准输出格式
{
  "核心元素": "...",
  "详细信息": "...",
  "下一步建议": "..."
}
```

---

## 🎉 完成！

按照以上步骤，你就可以将你的12个专业Prompt模板成功集成到Agent中了！

如果遇到任何问题，随时告诉我！
