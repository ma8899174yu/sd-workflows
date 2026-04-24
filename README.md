# Stable Diffusion Workflows 工作流分享

<div align="center">

![Banner](https://img.shields.io/badge/SD-Workflows-00D9FF?style=for-the-badge&logo=workflow&logoColor=white)
[![GitHub stars](https://img.shields.io/github/stars/ma8899174yu/sd-workflows?style=for-the-badge)](https://github.com/ma8899174yu/sd-workflows/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Stable Diffusion & ComfyUI 工作流分享库**

📺 [配套B站视频教程](https://space.bilibili.com/3546745917148074)

</div>

---

## 📖 项目介绍

收录我在B站AI教学视频中使用的工作流配置，包括：

- 🔄 ComfyUI 工作流 JSON 文件
- ⚙️ Stable Diffusion WebUI 参数预设
- 🎯 特定效果的工作流模板
- 📦 LoRA / Checkpoint 组合方案

## 📁 目录结构

```
sd-workflows/
├── README.md
├── LICENSE
├── workflows/
│   ├── portraits/                   # 人像类工作流
│   │   ├── realistic-face.json
│   │   └── anime-style.json
│   ├── artistic/                   # 艺术风格
│   │   ├── watercolor.json
│   │   └── oil-painting.json
│   └── special-effects/            # 特效类
│       ├── product-shot.json
│       └── fashion-photo.json
├── presets/                        # 参数预设
│   ├── fast-generation.json
│   └── high-quality.json
└── tools/                          # 辅助工具
    ├── workflow-to-image.py
    └── batch-export.py
```

## 🚀 使用方法

### ComfyUI 工作流

1. 下载 `.json` 文件
2. 打开 ComfyUI
3. 点击 `Load` 加载 JSON 文件
4. 根据需要调整节点参数

### 参数预设

将 JSON 文件复制到对应的配置目录即可。

## 📺 配套视频

| 视频标题 | 工作流类型 | 状态 |
|---------|----------|------|
| 【ComfyUI】基础工作流搭建 | 入门级 | ✅ 已发布 |
| 【进阶】人像精修工作流 | 进阶级 | 制作中 |

## 📊 使用统计

![Downloads](https://img.shields.io/github/downloads/ma8899174yu/sd-workflows/total?style=for-the-badge)

## 🤝 贡献指南

欢迎提交你自己的工作流！

### 提交格式

```bash
workflows/[category]/your-workflow-name.json
```

## 📜 License

MIT License - 详见 [LICENSE](LICENSE)

---

<div align="center">

⭐ 你的 Star 是我更新的动力！

🔗 [B站主页](https://space.bilibili.com/3546745917148074)

</div>
