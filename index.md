---
layout: default
title: 首页
---

<div class="hero">
  <div class="container text-center">
    <h1>DarcyInCode</h1>
    <p class="subtitle">独立研究者 · 技术探索者 · 终身学习者</p>
  </div>
</div>

<div class="intro">
  <p>我是一名研究爱好者，虽未踏入学院的殿堂，却对技术探索怀有满腔热忱。在这个技术日新月异的时代，我如同在茫茫大海中独自航行，没有灯塔的指引，只有内心对知识的渴望驱使着我前行。</p>
  <p>我在这里搭建了一片属于自己的净土，用以沉淀思考、记录成长。这里专注于代码形式化验证与智能体系统的研究，探索数学严谨性与智能系统的奇妙结合。如果你也是孤独的探索者，渴望找到志同道合的伙伴，欢迎在这里停留。让我们互相温暖，彼此赋能，在这条少有人走的路上，一起坚定前行。</p>
</div>

<div class="section">
  <h2 class="section-title">研究方向</h2>
  <div class="grid grid-2">
    <div class="card research-card">
      <h3>代码形式化验证</h3>
      <ul class="research-list">
        <li>程序正确性验证与证明</li>
        <li>形式化规格说明建模</li>
        <li>模型检验与静态分析</li>
        <li>契约式编程方法</li>
        <li>类型系统设计与实现</li>
      </ul>
    </div>
    <div class="card research-card">
      <h3>智能体系统</h3>
      <ul class="research-list">
        <li>多智能体协调与通信</li>
        <li>智能体架构设计</li>
        <li>自主决策算法</li>
        <li>强化学习在智能体中的应用</li>
        <li>分布式智能体系统</li>
      </ul>
    </div>
  </div>
</div>

<div class="section">
  <h2 class="section-title">最新文章</h2>
  <div class="articles-grid">
    {% assign recent_posts = site.posts | sort: 'date' | reverse | limit: 3 %}
    {% for post in recent_posts %}
      <article class="article-card">
        <div class="article-meta">
          <span class="article-date">{{ post.date | date: "%Y-%m-%d" }}</span>
          <span class="tag tag-primary">{{ site.categories[post.category] | default: post.category }}</span>
        </div>
        <h3 class="article-title">
          <a href="{{ post.url | relative_url }}" class="article-link">{{ post.title }}</a>
        </h3>
        <p class="article-excerpt">
          {{ post.excerpt | strip_html | truncate: 120 }}
        </p>
      </article>
    {% endfor %}
  </div>
  <div style="text-align: center; margin-top: 2rem;">
    <a href="/blog.html" class="btn btn-outline">查看全部文章 →</a>
  </div>
</div>

<div class="section">
  <h2 class="section-title">研究理念</h2>
  <div class="card">
    <p>作为一名研究爱好者，我深知这条路充满挑战——没有导师的指引，没有团队的支持，只有自己与技术的对话。但正是这种孤独，让我学会了独立思考，培养了坚韧的意志。</p>
    <p>我的研究聚焦于形式化方法与人工智能的交叉领域，探索如何将数学的严谨性与智能系统的灵活性相结合。每一次深入学习，都是对自己的超越；每一篇文档记录，都是思想的结晶。</p>
    <p>如果你也在技术的海洋中寻找方向，如果你也渴望与志同道合的人交流探讨，欢迎通过下方联系方式与我交流。让我们一起在这条看似孤独却充满意义的道路上，互相鼓励，共同成长。</p>
  </div>
</div>

<div class="contact-section">
  <h2 class="section-title text-center">联系方式</h2>
  <div class="contact-links">
    <a href="https://github.com/darcyincode" class="contact-link" target="_blank">GitHub</a>
    <a href="mailto:{{ site.email }}" class="contact-link">Email</a>
  </div>
</div>
