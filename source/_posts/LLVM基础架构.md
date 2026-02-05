---
title: LLVM基础架构
date: 2026-02-11
categories:
  - 安全语言
tags:
  - LLVM
  - 编译器
  - IR
  - 工具链
---

# LLVM基础架构

## 概述

本文档介绍LLVM编译器基础设施的架构设计、LLVM IR中间表示的特性，以及编译器工具链的使用。

## LLVM架构概览

### 三层架构设计

LLVM采用模块化的三层架构：

```
前端 (Frontend)
  ├─ Clang (C/C++/Objective-C)
  ├─ Rust
  ├─ Swift
  ├─ Fortran
  └─ ... (多种语言)
        ↓ 生成
中间层 (LLVM IR)
  ├─ SSA形式
  ├─ 平台无关
  └─ 优化Pass框架
        ↓ 编译为
后端 (Backend)
  ├─ x86/x86-64
  ├─ ARM/AArch64
  ├─ RISC-V
  ├─ WebAssembly
  └─ ... (多种目标)
```

### 架构优势

**1. 前后端分离**
- 新增语言只需实现前端（生成LLVM IR）
- 新增目标只需实现后端（从LLVM IR生成代码）
- N种语言 × M种目标，只需 N + M 个模块（而非 N × M）

**2. 统一优化层**
- 所有语言共享优化Pass
- 一次优化实现，所有语言受益

**3. 可扩展性**
- Pass插件机制
- 自定义IR扩展

## LLVM IR 中间表示

### IR的三种形式

LLVM IR有三种等价表示形式：

**1. 内存形式 (In-Memory Form)**
- C++对象表示
- 编译器内部使用
- 最快的处理速度

**2. 文本形式 (Human-Readable Assembly)**
- 文件扩展名：.ll
- 人类可读
- 便于学习和调试

```llvm
define i32 @add(i32 %a, i32 %b) {
entry:
  %sum = add i32 %a, %b
  ret i32 %sum
}
```

**3. 字节码形式 (Bitcode)**
- 文件扩展名：.bc
- 二进制格式
- 紧凑存储，快速解析

### SSA形式 (Static Single Assignment)

**核心规则：** 每个变量只赋值一次

```llvm
; 非SSA形式（伪代码）
x = 1
x = x + 2    ; x被重新赋值
x = x * 3

; SSA形式 - 每次赋值创建新变量
%x1 = 1
%x2 = add i32 %x1, 2
%x3 = mul i32 %x2, 3
```

**PHI节点：** 处理控制流汇聚

```c
// C代码
int x;
if (cond) {
    x = 10;
} else {
    x = 20;
}
return x;
```

```llvm
; LLVM IR
define i32 @example(i1 %cond) {
entry:
  br i1 %cond, label %then, label %else

then:
  br label %merge

else:
  br label %merge

merge:
  %x = phi i32 [ 10, %then ], [ 20, %else ]
  ret i32 %x
}
```

**SSA的优势：**
- 简化数据流分析
- 便于优化算法实现
- 消除变量版本歧义

### LLVM IR的设计特点

**优势：**
- 平台无关性 - 同一份IR可编译到多种架构（x86、ARM等）
- SSA形式 - 简化数据流分析和优化
- 丰富的优化生态 - 数百个优化Pass
- 成熟稳定 - 被广泛应用于生产环境
- 类型系统 - 强类型检查保证安全性

**抽象级别：**
- 接近机器层 - 主要关注标量和向量操作
- 低层表示 - 指针、内存操作、基本算术
- 单一层次 - 固定的抽象级别

**局限性：**
- 高层语义丢失 - 循环、矩阵等结构信息降级后消失
- 扩展性受限 - 添加新操作类型需要修改核心
- 不适合高维数据 - 张量、稀疏矩阵难以高效表达

详见 [MLIR架构分析.md](MLIR架构分析.md) 了解如何通过多层IR解决这些局限性。

### LLVM IR基本元素

**数据类型：**

```llvm
i1              ; 1位整数（布尔）
i32             ; 32位整数
float           ; 32位浮点
double          ; 64位浮点
i32*            ; 指针类型
[10 x i32]      ; 数组类型
<4 x float>     ; 向量类型（SIMD）
{i32, float}    ; 结构体类型
```

**指令示例：**

```llvm
; 算术运算
%result = add i32 %a, %b
%result = fadd float %x, %y

; 内存操作
%value = load i32, i32* %ptr
store i32 42, i32* %ptr

; 控制流
br label %next_block
br i1 %condition, label %then, label %else

; 函数调用
%ret = call i32 @foo(i32 %arg)
```

## LLVM IR的局限性：高层语义丢失

### 问题根源

LLVM IR的低层抽象导致高层语言结构在转换过程中丢失语义信息，限制了编译器的优化能力。

### 示例1：矩阵加法

高层语义在降级到LLVM IR时的丢失问题。

**C代码（高层表达）：**

```c
// C代码
for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
        C[i][j] = A[i][j] + B[i][j];  // 矩阵加法
    }
}
```

降级到LLVM IR后：

```llvm
; 外层循环头
for.cond.outer:
  %i = phi i32 [ 0, %entry ], [ %i.next, %for.inc.outer ]
  %cmp.outer = icmp slt i32 %i, %N
  br i1 %cmp.outer, label %for.cond.inner, label %for.end

; 内层循环头  
for.cond.inner:
  %j = phi i32 [ 0, %for.cond.outer ], [ %j.next, %for.inc.inner ]
  %cmp.inner = icmp slt i32 %j, %M
  br i1 %cmp.inner, label %for.body, label %for.inc.outer

; 循环体：简单的加载-加法-存储
for.body:
  %idx = mul nsw i32 %i, %M
  %offset = add nsw i32 %idx, %j
  %ptr.A = getelementptr inbounds float, float* %A, i32 %offset
  %val.A = load float, float* %ptr.A
  %ptr.B = getelementptr inbounds float, float* %B, i32 %offset
  %val.B = load float, float* %ptr.B
  %sum = fadd float %val.A, %val.B    ; 只能看到标量加法
  %ptr.C = getelementptr inbounds float, float* %C, i32 %offset
  store float %sum, float* %ptr.C
  br label %for.inc.inner

; 内层循环递增
for.inc.inner:
  %j.next = add nsw i32 %j, 1
  br label %for.cond.inner

; 外层循环递增
for.inc.outer:
  %i.next = add nsw i32 %i, 1
  br label %for.cond.outer

for.end:
  ret void

; 问题：循环结构被展开成基本块、分支、PHI节点
; 丢失了"这是矩阵加法"的高层语义
; 丢失了循环嵌套的结构信息
```

**问题分析：**

1. **无法识别高层模式** 
   - 编译器只看到嵌套的基本块和标量操作
   - 不知道这是矩阵加法
   - 错失调用优化BLAS库的机会

2. **循环优化困难** 
   - 循环结构被"扁平化"为分支和PHI节点
   - 需要通过复杂的分析"恢复"循环结构
   - 循环分块、交换等优化更难应用

3. **领域知识无法利用** 
   - 无法应用矩阵运算的特定优化
   - 无法识别可并行的模式
   - 难以进行高层重组

### 示例2：数组操作

```c
// C代码
void add_arrays(float *A, float *B, float *C, int N) {
    for (int i = 0; i < N; i++) {
        C[i] = A[i] + B[i];
    }
}
```

**LLVM IR面临的挑战：**

- 需要在低层分析循环依赖
- 向量化决策更保守（不确定数组别名关系）
- 难以判断数组访问模式是否规律
- 无法直接看出"逐元素加法"的高层意图

### 解决方案：多层IR

详见 [MLIR架构分析.md](MLIR架构分析.md)，通过引入多层中间表示：

```
高层IR (保留语义)
  ↓ 渐进式降级
中层IR (LLVM IR)
  ↓ 继续降级
低层IR (机器码)
```

在每一层都可以应用适合该抽象级别的优化。

## 中间表示的作用

### 为什么需要IR

**1. 平台无关性**
- 前端只需生成IR，无需关心目标平台
- 一份IR可编译到多种架构

**2. 优化的统一接口**
- 所有优化在IR层面进行
- 优化与具体语言解耦

**3. 多语言支持**
- C、C++、Rust等共享优化和后端
- 降低新语言开发成本

**4. 模块化设计**
- 前端、优化器、后端独立开发
- 便于维护和扩展

### IR的抽象层次对比

| 层次 | 示例 | 抽象级别 | 优化类型 |
|------|------|---------|---------|
| 高层IR | AST, MLIR Dialect | 接近源语言 | 高层语义优化 |
| 中层IR | LLVM IR | 平台无关通用表示 | 通用优化 |
| 低层IR | 汇编/机器码 | 接近硬件 | 目标特定优化 |

## 编译器工具链

### Clang编译器

**基本使用：**

```bash
# 编译C程序
clang program.c -o program

# 查看预处理结果
clang -E program.c

# 生成汇编
clang -S program.c

# 生成LLVM IR（文本）
clang -S -emit-llvm program.c -o program.ll

# 生成LLVM IR（字节码）
clang -c -emit-llvm program.c -o program.bc

# 查看AST
clang -Xclang -ast-dump program.c
```

### 优化级别

```bash
# 无优化（调试）
clang -O0 program.c

# 标准优化（推荐）
clang -O2 program.c

# 激进优化
clang -O3 program.c

# 大小优化
clang -Os program.c
```

详见 [LLVM架构优化.md](LLVM架构优化.md) 了解各优化级别的详细说明。

### LLVM工具

**llvm-dis：** 字节码转文本

```bash
llvm-dis program.bc -o program.ll
```

**llvm-as：** 文本转字节码

```bash
llvm-as program.ll -o program.bc
```

**opt：** 运行优化Pass

```bash
# 运行特定优化
opt -O2 program.bc -o program_opt.bc

# 查看优化效果
opt -O2 -print-after-all program.bc
```

**llc：** IR转汇编

```bash
llc program.bc -o program.s
```

## 总结

### 关键要点

**1. LLVM架构**
- 三层设计：前端、LLVM IR、后端
- 前后端分离，模块化扩展
- 统一的优化基础设施

**2. LLVM IR特性**
- SSA形式 - 每个变量只赋值一次
- 平台无关 - 统一的中间表示
- 强类型 - 类型安全保证
- 可优化 - 丰富的Pass生态

**3. 架构优势**
- N种语言 + M种目标 = N + M个模块
- 多语言共享优化和后端
- 可扩展的Pass系统

**4. 局限性**
- 单一抽象层次
- 高层语义丢失
- 需要MLIR等多层IR方案补充

### IR的层次

编译器通常使用多层IR来平衡抽象级别和优化效果：

```
源代码
  ↓
高层IR (保留语义)
  ↓
中层IR (LLVM IR)
  ↓
低层IR (汇编/机器码)
```

每一层都可以应用适合该抽象级别的分析和优化。

## 相关文档

- [C语言编译原理基础.md](C语言编译原理基础.md) - C语言编译流程
- [LLVM架构优化.md](LLVM架构优化.md) - 详细的LLVM优化技术
- [MLIR架构分析.md](MLIR架构分析.md) - 多层IR解决高层语义丢失问题
- [BishengC编译流程.md](BishengC编译流程.md) - BishengC扩展实现
