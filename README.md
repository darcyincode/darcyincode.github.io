# DarcyInCode 个人博客

基于 **Hexo** 构建的技术博客，专注于代码形式化验证与智能体系统研究。

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 本地预览

```bash
# 启动本地服务器
npm run server

# 访问 http://localhost:4000
```

### 清理和构建

```bash
# 清理生成文件
npm run clean

# 生成静态文件
npm run build
```

### 部署到GitHub Pages

```bash
# 部署（自动推送到gh-pages分支）
npm run deploy
```

## 📝 写作工作流

### 创建新文章

```bash
hexo new "我的新文章"
```

这会在 `source/_posts/` 创建新文件，包含 Front Matter：

```yaml
---
title: 我的新文章
date: 2026-01-23 10:00:00
tags:
  - 标签1
  - 标签2
categories:
  - 分类
---
```

### 文章分类

使用以下分类之一：
- `形式化验证` (formal-verification)
- `智能体系统` (ai-agents)
- `工具使用` (tools)
- `研究心得` (research)

示例：

```yaml
---
title: Coq中的归纳证明
date: 2026-01-20
categories:
  - 形式化验证
tags:
  - Coq
  - 归纳证明
  - 定理证明
---
---
```

3. 编写Markdown内容
4. 推送到GitHub，自动部署！

## 📁 项目结构

```
darcyincode.github.io/
├── _config.yml          # Jekyll配置
├── _posts/              # 博客文章（Jekyll格式）
├── _layouts/            # 页面布局
├── _includes/           # 可复用组件
├── index.md             # 首页
├── blog.md              # 博客列表页
├── style.css            # 样式表
├── Gemfile              # Ruby依赖
└── docs/                # 原始Markdown（可删除）
```

## 🎨 主题与样式

当前使用自定义样式（`style.css`），基于Jekyll的Minima主题扩展。

## 📝 文章分类

- **formal-verification**: 代码形式化验证
- **ai-agents**: 智能体系统
- **tools**: 工具使用教程
- **research**: 研究心得

## 🔧 GitHub Pages配置

推送到GitHub后，在仓库设置中：
1. Settings → Pages
2. Source 选择 `main` 分支
3. 自动使用Jekyll构建

## 📦 依赖

- Jekyll 3.9+
- jekyll-feed
- jekyll-seo-tag
- GitHub Pages gem

## License

MIT
- 自主决策算法
- 强化学习在智能体中的应用
- 分布式智能体系统

## 🎯 研究兴趣

我的研究兴趣集中在形式化方法与人工智能的交叉领域，特别关注：
- 可验证的智能体系统
- 形式化验证在AI安全性保障中的作用
- 智能体辅助的软件验证工具

## 💻 技术栈

**形式化工具**: Coq, Isabelle/HOL, Dafny, TLA+, CBMC  
**编程语言**: Python, Rust, OCaml, Haskell, C++  
**AI/ML框架**: PyTorch, TensorFlow, OpenAI Gym, Ray  

## 📫 联系方式

- GitHub: [@darcyincode](https://github.com/darcyincode)
- Email: [darcyincode@gmail.com](mailto:darcyincode@gmail.com)

---

💡 访问 [主页](https://darcyincode.github.io) 了解更多详情
