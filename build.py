#!/usr/bin/env python3
"""
Markdown到HTML转换脚本
用于将docs/目录中的Markdown文档转换为网站可用的HTML
"""

import os
import json
import markdown
from pathlib import Path
from datetime import datetime

# 配置
DOCS_DIR = Path("docs")
OUTPUT_DIR = Path("articles")
TEMPLATE_FILE = Path("article-template.html")
METADATA_FILE = DOCS_DIR / "metadata.json"

# Markdown扩展
MD_EXTENSIONS = [
    'extra',           # 包含tables, fenced_code等
    'codehilite',      # 代码高亮
    'toc',             # 目录
    'nl2br',           # 换行转换
    'sane_lists',      # 更好的列表处理
]

def load_metadata():
    """加载文档元数据"""
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_template():
    """读取HTML模板"""
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return get_default_template()

def get_default_template():
    """默认HTML模板"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - DarcyInCode</title>
    <link rel="stylesheet" href="../style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github-dark.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="nav-content">
                <a href="../index.html" class="nav-brand">DarcyInCode</a>
                <div class="nav-links">
                    <a href="../index.html" class="nav-link">首页</a>
                    <a href="../docs.html" class="nav-link active">技术文档</a>
                </div>
            </div>
        </div>
    </nav>

    <div class="container article-container">
        <article class="article-content">
            <header class="article-header">
                <h1>{title}</h1>
                <div class="article-meta">
                    <span class="article-date">{date}</span>
                    <span class="tag tag-primary">{category_label}</span>
                </div>
                <div class="article-tags">
                    {tags_html}
                </div>
            </header>
            
            <div class="article-body">
                {content}
            </div>
            
            <footer class="article-footer">
                <a href="../docs.html" class="btn btn-outline">← 返回文档列表</a>
            </footer>
        </article>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</body>
</html>"""

def get_category_label(category):
    """获取分类的中文标签"""
    labels = {
        'formal-verification': '形式化验证',
        'ai-agents': '智能体系统',
        'tools': '工具使用',
        'research': '研究心得'
    }
    return labels.get(category, category)

def convert_markdown_to_html(md_file, metadata):
    """转换单个Markdown文件为HTML"""
    # 读取Markdown内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除YAML front matter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()
    
    # 转换Markdown为HTML
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    html_content = md.convert(content)
    
    # 生成标签HTML
    tags_html = ' '.join([
        f'<span class="tag">{tag}</span>' 
        for tag in metadata.get('tags', [])
    ])
    
    # 读取模板
    template = read_template()
    
    # 替换占位符
    html = template.format(
        title=metadata.get('title', ''),
        date=metadata.get('date', ''),
        category_label=get_category_label(metadata.get('category', '')),
        tags_html=tags_html,
        content=html_content
    )
    
    return html

def build_docs_index(metadata_list):
    """更新docs.html中的文章链接"""
    articles_html = []
    
    for meta in metadata_list:
        category_label = get_category_label(meta['category'])
        tags_html = ' '.join([
            f'<span class="tag">{tag}</span>' 
            for tag in meta['tags']
        ])
        
        article_html = f"""
                <article class="article-card" data-category="{meta['category']}">
                    <div class="article-meta">
                        <span class="article-date">{meta['date']}</span>
                        <span class="tag tag-primary">{category_label}</span>
                    </div>
                    <h3 class="article-title">
                        <a href="articles/{meta['slug']}.html" class="article-link">{meta['title']}</a>
                    </h3>
                    <p class="article-excerpt">
                        {meta['excerpt']}
                    </p>
                    <div class="article-tags">
                        {tags_html}
                    </div>
                </article>"""
        
        articles_html.append(article_html)
    
    return '\n'.join(articles_html)

def main():
    """主函数"""
    print("🚀 开始转换Markdown文档...")
    
    # 创建输出目录
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 加载元数据
    metadata_list = load_metadata()
    print(f"📄 找到 {len(metadata_list)} 篇文档")
    
    # 转换每个文档
    for meta in metadata_list:
        md_file = Path(meta['file'])
        if not md_file.exists():
            print(f"⚠️  文件不存在: {md_file}")
            continue
        
        print(f"📝 转换: {meta['title']}")
        
        # 转换为HTML
        html_content = convert_markdown_to_html(md_file, meta)
        
        # 保存HTML文件
        output_file = OUTPUT_DIR / f"{meta['slug']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 生成: {output_file}")
    
    # 更新docs.html
    print("\n📋 更新文档索引...")
    articles_html = build_docs_index(metadata_list)
    
    # 这里可以选择自动更新docs.html，或者手动复制生成的HTML
    index_output = OUTPUT_DIR / "articles-list.html"
    with open(index_output, 'w', encoding='utf-8') as f:
        f.write(articles_html)
    
    print(f"✅ 文章列表HTML已生成: {index_output}")
    print("   请手动将内容复制到docs.html的文章列表区域")
    
    print("\n✨ 转换完成！")
    print(f"   共处理 {len(metadata_list)} 篇文档")
    print(f"   输出目录: {OUTPUT_DIR.absolute()}")

if __name__ == '__main__':
    main()
