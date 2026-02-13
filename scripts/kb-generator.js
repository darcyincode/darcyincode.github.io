'use strict';

// 生成知识库 JSON API：/api/kb.json
hexo.extend.generator.register('kb-json', function (locals) {
  const categories = {};

  locals.posts.forEach(function (post) {
    const cats = post.categories.toArray();
    const postData = {
      title: post.title,
      slug: post.slug,
      date: post.date.format('YYYY-MM-DD'),
      content: post.content,
      path: post.path,
      order: post.order || 999 // 默认顺序为999（最后）
    };

    if (cats.length === 0) {
      if (!categories['未分类']) categories['未分类'] = { posts: [], subcategories: {} };
      categories['未分类'].posts.push(postData);
    } else if (cats.length === 1) {
      var catName = cats[0].name;
      if (!categories[catName]) categories[catName] = { posts: [], subcategories: {} };
      categories[catName].posts.push(postData);
    } else {
      var parentName = cats[0].name;
      var childName = cats[1].name;
      if (!categories[parentName]) categories[parentName] = { posts: [], subcategories: {} };
      if (!categories[parentName].subcategories[childName]) {
        categories[parentName].subcategories[childName] = { posts: [] };
      }
      categories[parentName].subcategories[childName].posts.push(postData);
    }
  });

  // 对所有分类和子分类的文章按 order 排序
  Object.keys(categories).forEach(function(catName) {
    // 排序顶级分类的文章
    categories[catName].posts.sort(function(a, b) {
      return a.order - b.order;
    });
    
    // 排序子分类的文章
    Object.keys(categories[catName].subcategories).forEach(function(subName) {
      categories[catName].subcategories[subName].posts.sort(function(a, b) {
        return a.order - b.order;
      });
    });
  });

  return {
    path: 'api/kb.json',
    data: JSON.stringify({ categories: categories })
  };
});
