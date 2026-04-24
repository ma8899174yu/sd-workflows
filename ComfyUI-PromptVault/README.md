# ComfyUI-PromptVault 提示词库节点

<div align="center">

![Banner](https://img.shields.io/badge/ComfyUI-PromptVault-FF6B6B?style=for-the-badge&logo=robot&logoColor=white)
[![GitHub stars](https://img.shields.io/github/stars/ma8899174yu/sd-workflows?style=for-the-badge)](https://github.com/ma8899174yu/sd-workflows/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**ComfyUI 自定义节点 | FLUX/MJ/自然语言预设提示词库**

📺 [B站教程](https://space.bilibili.com/3546745917148074) |
🔗 [YouTube频道](https://www.youtube.com/@SC2778)

</div>

---

## 📖 简介

**ComfyUI-PromptVault** 是为 ComfyUI 开发的自定义节点，可直接在 ComfyUI 界面中选择预设提示词模板，输出正向提示词、负向提示词和推荐参数。

节点包含 **30+ 精选预设**，覆盖：
- 🔥 **FLUX 写实摄影**（人像/城市/美食/产品/自然）
- 🎬 **FLUX 电影感**（人像/风景/武侠/科幻）
- 🎨 **FLUX 插画/概念艺术**
- ✨ **MJ 精选提示词**
- 📝 **自然语言描述型提示词**

> 💡 所有提示词均来自 [ai-prompt-templates](https://github.com/ma8899174yu/ai-prompt-templates) 仓库，可直接使用。

---

## 🚀 安装方式

### 方式一：Git 克隆（推荐）

```bash
# 克隆到 ComfyUI custom_nodes 目录
cd your/comfyui/path/custom_nodes
git clone https://github.com/ma8899174yu/ComfyUI-PromptVault.git
```

### 方式二：下载安装

1. 点击 Code → Download ZIP
2. 解压到 `ComfyUI/custom_nodes/ComfyUI-PromptVault` 目录

---

## 📦 包含的预设

### 🔥 FLUX 写实类 (13个)

| 预设名称 | 描述 |
|---------|------|
| FLUX 人像大师 | 商业级写真人像 |
| FLUX 商务人像 | 简历/职业照 |
| FLUX 证件照 | 签证/身份证规格 |
| FLUX 赛博朋克城市 | 霓虹夜景 |
| FLUX 上海航拍 | 城市天际线 |
| FLUX 东京时尚街拍 | 杂志封面风格 |
| FLUX 美食摄影 | 商业美食图 |
| FLUX 北欧室内 | 极简家居 |
| FLUX 产品渲染 | 白底产品图 |
| FLUX 野生动物 | 国家地理风格 |
| FLUX 中国夜景 | 传统+现代融合 |

### 🎬 FLUX 电影感 (4个)

| 预设名称 | 描述 |
|---------|------|
| FLUX 电影感人像 | 宽荧幕电影风格 |
| FLUX 史诗山景 | 风光大片 |
| FLUX 武侠英雄 | 侠客意境 |
| FLUX 星际飞船 | 科幻概念 |

### 🎨 FLUX 插画/概念 (8个)

| 预设名称 | 描述 |
|---------|------|
| FLUX 古风仙女 | 水墨+写实 |
| FLUX 中国山水 | 国画风格 |
| FLUX 龙骑士 | 奇幻概念 |
| FLUX 水墨山水 | 当代水墨 |
| FLUX 机甲战士 | 机战概念 |
| FLUX 未来建筑 | 建筑可视化 |
| FLUX 水下世界 | 亚特兰蒂斯 |
| FLUX 将军冲锋 | 历史战争 |

### ✨ MJ 精选 (4个)

| 预设名称 | 描述 |
|---------|------|
| MJ 古风美女 | 东方美学 |
| MJ 奇幻龙 | 西方奇幻 |
| MJ 情感人像 | 电影感人像 |
| MJ 复古相机 | 复古怀旧 |

### 📝 自然语言 (6个)

| 预设名称 | 描述 |
|---------|------|
| 自然语言 品牌故事 | 生活方式品牌 |
| 自然语言 头像设计 | 社交头像 |
| 自然语言 儿童绘本 | 插画风格 |
| 自然语言 产品展示 | 电商主图 |
| 自然语言 科技信息图 | 数据可视化 |
| 自然语言 视频缩略图 | YouTube封面 |

---

## 🔧 使用方法

### 在 ComfyUI 中使用

1. 安装节点后重启 ComfyUI
2. 在节点搜索栏输入 `Prompt Vault`
3. 拖入 **Prompt Vault 提示词选择器** 节点
4. 从下拉菜单中选择预设
5. 将输出的 `positive_prompt` 连接到 **CLIP Text Encode (Positive)**
6. 将输出的 `negative_prompt` 连接到 **CLIP Text Encode (Negative)**

### 输出参数

| 输出 | 类型 | 说明 |
|------|------|------|
| positive_prompt | STRING | 正向提示词 |
| negative_prompt | STRING | 负向提示词 |
| parameters | STRING | 推荐参数（格式：key: value, ...） |

---

## 📁 项目结构

```
ComfyUI-PromptVault/
├── __init__.py              # 节点入口
├── prompt_vault_node.py     # 核心节点代码
├── README.md                # 说明文档
└── LICENSE                  # MIT协议
```

---

## 🔄 与工作流结合

### 基础 FLUX 人像工作流

```
[PromptVaultLoader] → [CLIPTextEncode Positive] → [FluxDevLoader]
                                                              ↓
[KSampler] ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← [CLIPTextEncode Negative]
      ↓
[VAEDecode] → [PreviewImage]
```

### 完整参数传递工作流

```
[PromptVaultLoader]
      │
      ├── positive_prompt → CLIPTextEncode → Flux
      ├── negative_prompt → CLIPTextEncode → Flux
      └── parameters → [用于参考手动设置KSampler参数]
```

---

## 🤝 贡献提示词

欢迎提交新的预设提示词！

### 提交格式

在 `prompt_vault_node.py` 的 `PRESETS` 字典中添加：

```python
"your_preset_key": {
    "name": "你的预设名称",
    "category": "分类/子分类",
    "positive": "正向提示词内容",
    "negative": "负向提示词内容",
    "params": {
        "steps": "采样步数",
        "cfg": "CFG值",
        "sampler": "采样器",
        "guidance": "引导强度(FLUX)"
    }
}
```

---

## 📺 配套视频

| 视频 | 内容 |
|------|------|
| ComfyUI + FLUX 人像工作流 | 节点使用教程 |
| Prompt Vault 提示词库节点发布 | 功能介绍 |

---

## 📜 License

MIT License - 可商用，可修改，可分发。

---

<div align="center">

⭐ 如果对你有帮助，欢迎 Star！

🔗 [B站主页](https://space.bilibili.com/3546745917148074) |
[YouTube频道](https://www.youtube.com/@SC2778) |
[提示词库](https://github.com/ma8899174yu/ai-prompt-templates)

*让AI技术惠及每个人*

</div>
