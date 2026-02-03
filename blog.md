---
layout: default
title: 技术文档
permalink: /blog.html
---

<div class="hero">
  <div class="container text-center">
    <h1>技术文档</h1>
    <p class="subtitle">分享代码形式化验证与智能体系统的技术见解</p>
  </div>
</div>

<div class="section">
  <div class="filter-tabs">
    <button class="filter-tab active" data-category="all">全部</button>
    <button class="filter-tab" data-category="formal-verification">形式化验证</button>
    <button class="filter-tab" data-category="ai-agents">智能体系统</button>
    <button class="filter-tab" data-category="tools">工具使用</button>
    <button class="filter-tab" data-category="research">研究心得</button>
  </div>
</div>

<div class="section">
  <div class="articles-grid">
    {% assign sorted_posts = site.posts | sort: 'date' | reverse %}
    {% for post in sorted_posts %}
      <article class="article-card" data-category="{{ post.category }}">
        <div class="article-meta">
          <span class="article-date">{{ post.date | date: "%Y-%m-%d" }}</span>
          <span class="tag tag-primary">{{ site.categories[post.category] | default: post.category }}</span>
        </div>
        <h3 class="article-title">
          <a href="{{ post.url | relative_url }}" class="article-link">{{ post.title }}</a>
        </h3>
        <p class="article-excerpt">
          {{ post.excerpt | strip_html | truncate: 150 }}
        </p>
        {% if post.tags %}
          <div class="article-tags">
            {% for tag in post.tags %}
              <span class="tag">{{ tag }}</span>
            {% endfor %}
          </div>
        {% endif %}
      </article>
    {% endfor %}
  </div>
</div>

<script>
  // 分类筛选功能
  document.addEventListener('DOMContentLoaded', function() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    const articles = document.querySelectorAll('.article-card');

    filterTabs.forEach(tab => {
      tab.addEventListener('click', function() {
        const category = this.dataset.category;
        
        filterTabs.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
        
        articles.forEach(article => {
          if (category === 'all' || article.dataset.category === category) {
            article.style.display = 'block';
          } else {
            article.style.display = 'none';
          }
        });
      });
    });
  });
</script>
