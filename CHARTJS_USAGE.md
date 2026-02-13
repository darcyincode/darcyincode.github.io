# Chart.js 数学函数图表使用指南

在知识库 Markdown 文章中使用 Chart.js 绘制数学函数图表。

## 基础用法

在代码块中使用 `chart` 语言标记，内容为 Chart.js 配置 JSON：

````markdown
```chart
{
  "type": "line",
  "data": {
    "labels": [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6],
    "datasets": [{
      "label": "y = x²",
      "data": [36, 25, 16, 9, 4, 1, 0, 1, 4, 9, 16, 25, 36],
      "borderColor": "#6D3896",
      "backgroundColor": "rgba(109, 56, 150, 0.1)",
      "tension": 0.4
    }]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": {
        "display": true,
        "text": "抛物线 y = x²"
      }
    }
  }
}
```
````

## 激活函数示例

### Sigmoid 函数

````markdown
```chart
{
  "type": "line",
  "data": {
    "labels": [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6],
    "datasets": [{
      "label": "Sigmoid",
      "data": [0.002, 0.007, 0.018, 0.047, 0.119, 0.269, 0.5, 0.731, 0.881, 0.953, 0.982, 0.993, 0.998],
      "borderColor": "#6D3896",
      "backgroundColor": "rgba(109, 56, 150, 0.1)",
      "borderWidth": 3,
      "tension": 0.4,
      "pointRadius": 0
    }]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": { "display": true, "text": "Sigmoid激活函数" },
      "legend": { "display": false }
    },
    "scales": {
      "y": { "min": 0, "max": 1 }
    }
  }
}
```
````

### ReLU 函数

````markdown
```chart
{
  "type": "line",
  "data": {
    "labels": [-3, -2, -1, 0, 1, 2, 3, 4, 5],
    "datasets": [{
      "label": "ReLU",
      "data": [0, 0, 0, 0, 1, 2, 3, 4, 5],
      "borderColor": "#B4E600",
      "backgroundColor": "rgba(180, 230, 0, 0.1)",
      "borderWidth": 3,
      "tension": 0,
      "pointRadius": 0
    }]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": { "display": true, "text": "ReLU激活函数" }
    }
  }
}
```
````

### Tanh 函数

````markdown
```chart
{
  "type": "line",
  "data": {
    "labels": [-4, -3, -2, -1, 0, 1, 2, 3, 4],
    "datasets": [{
      "label": "Tanh",
      "data": [-0.999, -0.995, -0.964, -0.762, 0, 0.762, 0.964, 0.995, 0.999],
      "borderColor": "#6D3896",
      "backgroundColor": "rgba(109, 56, 150, 0.1)",
      "borderWidth": 3,
      "tension": 0.4,
      "pointRadius": 0
    }]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": { "display": true, "text": "Tanh激活函数" }
    },
    "scales": {
      "y": { "min": -1.2, "max": 1.2 }
    }
  }
}
```
````

### 多函数对比

````markdown
```chart
{
  "type": "line",
  "data": {
    "labels": [-3, -2, -1, 0, 1, 2, 3],
    "datasets": [
      {
        "label": "ReLU",
        "data": [0, 0, 0, 0, 1, 2, 3],
        "borderColor": "#B4E600",
        "borderWidth": 2,
        "tension": 0,
        "pointRadius": 0
      },
      {
        "label": "Leaky ReLU",
        "data": [-0.3, -0.2, -0.1, 0, 1, 2, 3],
        "borderColor": "#6D3896",
        "borderWidth": 2,
        "tension": 0,
        "pointRadius": 0
      }
    ]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": { "display": true, "text": "ReLU vs Leaky ReLU" }
    }
  }
}
```
````

## 配置说明

### 基本结构

```json
{
  "type": "line",        // 图表类型：line, bar, scatter等
  "data": {
    "labels": [...],     // X轴标签（数值）
    "datasets": [{       // 数据集数组
      "label": "...",    // 数据集名称
      "data": [...],     // Y轴数据
      "borderColor": "#6D3896",  // 线条颜色
      "backgroundColor": "rgba(109, 56, 150, 0.1)",  // 填充颜色
      "borderWidth": 3,  // 线条宽度
      "tension": 0.4,    // 曲线张力（0=直线，0.4=平滑）
      "pointRadius": 0   // 数据点大小（0=不显示）
    }]
  },
  "options": {
    "responsive": true,  // 响应式
    "plugins": {
      "title": {
        "display": true,
        "text": "图表标题"
      }
    },
    "scales": {
      "y": {
        "min": 0,        // Y轴最小值
        "max": 1         // Y轴最大值
      }
    }
  }
}
```

### 常用颜色

- 紫色主题：`#6D3896`
- 绿色主题：`#B4E600`
- 半透明紫色：`rgba(109, 56, 150, 0.1)`
- 半透明绿色：`rgba(180, 230, 0, 0.1)`

### 常用配置

- `tension: 0` - 直线连接（ReLU）
- `tension: 0.4` - 平滑曲线（Sigmoid/Tanh）
- `pointRadius: 0` - 隐藏数据点
- `borderWidth: 3` - 较粗的线条

## 数据生成提示

对于复杂函数，可以用 Python/JavaScript 生成数据：

```python
import numpy as np

# Sigmoid
x = np.linspace(-6, 6, 13)
y = 1 / (1 + np.exp(-x))
print(list(y.round(3)))

# Tanh
y = np.tanh(x)
print(list(y.round(3)))

# ReLU
y = np.maximum(0, x)
print(list(y.round(3)))
```

## 注意事项

1. **代码块语言必须是 `chart`**
2. **内容必须是有效的 JSON**（属性名用双引号）
3. **数组长度要匹配**：labels 和 data 长度必须相同
4. **颜色使用主题色**：紫色 `#6D3896`，绿色 `#B4E600`
5. **刷新页面自动渲染**

## 完整示例

参见 [`激活函数-修正版.md`](source/_posts/ai-learning/基础知识/激活函数-修正版.md) 中的图表代码。
