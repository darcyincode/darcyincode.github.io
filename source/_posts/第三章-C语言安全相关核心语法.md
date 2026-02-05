---
title: C语言安全相关核心语法
date: 2026-02-03
categories:
  - 安全语言
tags:
  - C语言
  - 内存安全
  - 存储类
  - 类型限定符
  - 指针
---

# C语言安全相关核心语法

## 概述

第二章介绍了程序运行时的内存布局：栈、堆、数据段等各自的特性和用途。那么，C语言中哪些语法特性会影响变量被分配到哪个内存区域？如何控制变量的生命周期和可见性？如何安全地操作内存地址？

本章**专注于与内存安全密切相关的语法特性**：`static`/`extern`等存储类说明符决定变量的存储位置和链接属性；`const`/`volatile`等类型限定符控制访问权限；指针作为C语言直接操作内存的核心机制。这些语法是理解和编写安全C代码的基础。

**与普通语法的区别**：本章不涉及`if`/`for`/`while`等控制流语句，而是聚焦于那些直接影响内存安全的关键字——它们是理解第四章内存安全问题的前置知识，只有掌握了变量如何存储、指针如何工作，才能理解为什么会发生栈溢出、悬空指针等安全问题。

## 本章内容组织

C语言中影响内存安全的语法特性可以分为两大类：**关键字**和**语法规则**。理解它们的分类和关系，是掌握C语言内存机制的关键。

### 关键字分类概览

在C语言中，有一组特殊的关键字**不影响程序的逻辑流程**（如if/while），而是控制**数据如何存储和访问**：

| 分类 | 关键字 | 作用范围 | 核心职责 |
|------|--------|---------|---------|
| **存储类说明符**<br>(Storage Class Specifiers) | `static`、`extern` | 控制变量的**存储位置**<br>和**链接属性** | • 决定变量在内存中的位置（栈/堆/Data段）<br>• 控制生命周期（何时创建/销毁）<br>• 控制可见性（本文件/跨文件） |
| **类型限定符**<br>(Type Qualifiers) | `const`、`volatile`<br>`restrict` | 控制变量的**访问方式**<br>和**优化行为** | • 限制读写权限（只读/易变）<br>• 影响编译器优化策略<br>• 提供类型安全保证 |

**指针（Pointer）的特殊地位**：

虽然指针不是关键字（`*`和`&`是运算符），但它是C语言**直接操作内存地址的核心机制**，与上述关键字紧密配合：

```c
// 指针 + 存储类说明符
static int *ptr;              // 指针变量本身是静态的
extern int *shared_ptr;       // 引用其他文件的指针

// 指针 + 类型限定符
const int *p1;                // 指向常量的指针（不能通过p1修改值）
int * const p2;               // 常量指针（指针本身不能改变指向）
const int * const p3;         // 两者都是常量

// 指针是连接"内存地址"和"数据"的桥梁
int x = 42;
int *ptr = &x;                // 取地址运算符&
*ptr = 100;                   // 解引用运算符*
```

指针是理解C语言内存安全问题的**核心**，本章将单独深入讲解。

### 语法规则与概念

除了关键字，还有一些重要的**语法规则和概念**决定了变量的行为和安全性：

| 概念 | 作用 | 为什么重要 |
|------|------|-----------|
| **作用域（Scope）** | 决定变量名在代码中的**可见范围** | 理解变量何时可访问、命名冲突如何避免 |
| **生命周期（Lifetime）** | 决定变量在内存中**存在的时间** | 理解悬空指针、内存泄漏等安全问题的根源 |
| **链接属性（Linkage）** | 决定标识符在**多个编译单元间**的可见性 | 理解跨文件变量共享、符号冲突问题 |
| **初始化行为** | 决定变量的**初始值来源** | 未初始化变量是常见漏洞源 |

这些概念与存储类说明符密切相关：
- `static`局部变量延长**生命周期**（从函数调用期间→整个程序）
- `static`全局变量限制**链接属性**（从外部链接→内部链接）
- `extern`声明引用其他文件定义的变量（跨文件**链接**）

---

## 存储类说明符（Storage Class Specifiers）

存储类说明符决定了变量的**存储位置**、**生命周期**和**可见性**。C语言中与安全相关的存储类主要有两种：`static`和`extern`。

### static：改变生命周期和可见性

`static`是最重要的存储类说明符，它在不同上下文中有不同作用，但核心思想是**限制作用域**或**延长生命周期**。

#### 1. 修饰全局变量：限制文件作用域

```c
// file1.c
int global_var = 10;        // 外部链接，其他文件可通过extern访问
static int file_var = 20;   // 内部链接，仅本文件可见

// file2.c
extern int global_var;      // 可以访问file1.c的global_var
extern int file_var;        // 错误！file_var是静态的，无法访问
```

**作用**：防止命名冲突，实现模块化。多个文件可以各自定义同名的`static`变量而不冲突。

**内存位置**：仍在Data段或BSS段（取决于是否初始化），`static`不改变存储位置，只改变链接属性。

#### 2. 修饰局部变量：延长生命周期

```c
void counter() {
    static int count = 0;  // 只初始化一次，存储在Data段
    count++;
    printf("%d\n", count);
}

int main() {
    counter();  // 输出: 1
    counter();  // 输出: 2
    counter();  // 输出: 3
    return 0;
}
```

**关键区别**：

| 特性 | 普通局部变量 | 静态局部变量 |
|------|-------------|-------------|
| **存储位置** | 栈 | Data段/BSS段 |
| **生命周期** | 函数调用期间 | 整个程序运行期 |
| **作用域** | 函数内部 | 函数内部 |
| **初始化** | 每次调用时重新初始化 | 只初始化一次 |

#### 3. 修饰函数：限制函数可见性

```c
// utils.c
static void helper_function() {  // 仅本文件可见
    // 辅助函数实现
}

void public_function() {         // 可被其他文件调用
    helper_function();
}
```

**作用**：隐藏内部实现细节，避免函数名冲突。

#### 4. 在头文件中的特殊用法

当函数定义在头文件中时，`static`有特殊作用：避免多个源文件包含同一头文件时产生的链接冲突。

**理解前提**：`#include`是**文本复制**，不是链接！

当多个`.c`文件包含同一个头文件时，预处理器会将头文件的内容**逐字复制**到每个`.c`文件中。

```c
// 错误示范：不加static
// header.h
void helper() {  // 没有static
    printf("help\n");
}

// file1.c
#include "header.h"  // 预处理后：file1.c中有void helper()的定义

// file2.c
#include "header.h"  // 预处理后：file2.c中也有void helper()的定义

// 结果：链接错误"helper重复定义"
// 因为file1.o和file2.o中都有helper函数的实体

// 正确做法：加static
// header.h
static void helper() {  // 有static
    printf("help\n");
}

// file1.c
#include "header.h"  // 复制后：file1.c中有static void helper()

// file2.c
#include "header.h"  // 复制后：file2.c中有static void helper()

// 结果：file1.o和file2.o各自有自己的helper副本，互不冲突
// 原因：static保证每个文件的helper是私有的（内部链接）
// 代价：如果helper很大，会在每个.o中生成重复代码（浪费空间）
```

**为什么不矛盾**：
- 虽然每个文件都包含头文件（文本复制）
- 但`static`保证每个文件的函数副本是**私有的**
- 链接器看到的是：file1.o有私有helper，file2.o也有私有helper，互不干扰
- 类比：两个人各自抄写了同一份食谱，static的作用是"这份食谱只在你家厨房用"

**典型应用**：`static inline`函数常放在头文件中（见内联函数章节）。

### extern：声明外部链接

`extern`用于声明变量或函数定义在其他文件中。

```c
// global.c
int shared_data = 100;  // 定义

// main.c
extern int shared_data; // 声明（不分配内存）
printf("%d\n", shared_data);
```

**关键点**：
- `extern`声明**不分配内存**，只是告诉编译器"这个变量在别处定义"
- 函数默认是`extern`的，可以省略（除非用`static`修饰）
- 避免在头文件中定义全局变量，应该只声明（用`extern`）

**常见错误**：
```c
// header.h
int global = 0;  // 错误！多个文件包含此头文件会导致重复定义

// 正确做法：
// header.h
extern int global;  // 声明

// source.c
int global = 0;     // 定义
```

---

## 类型限定符（Type Qualifiers）

类型限定符为类型添加额外的属性，主要用于优化和安全。

### const：只读保护

`const`修饰的对象不能被修改（或者说，修改它是未定义行为）。

#### 1. 基本用法

```c
const int max_size = 100;  // max_size不可修改
max_size = 200;            // 编译错误
```

#### 2. 指针与const的组合

```c
// 1. 指向常量的指针（pointer to const）
const int *ptr1 = &x;
*ptr1 = 10;   // 错误：不能通过ptr1修改x
ptr1 = &y;    // 正确：可以改变指针指向

// 2. 常量指针（const pointer）
int *const ptr2 = &x;
*ptr2 = 10;   // 正确：可以修改x
ptr2 = &y;    // 错误：不能改变指针指向

// 3. 指向常量的常量指针
const int *const ptr3 = &x;
*ptr3 = 10;   // 错误
ptr3 = &y;    // 错误

// 记忆技巧：const修饰它左边的内容，如果左边没有则修饰右边
```

#### 3. 函数参数中的const

```c
// 保证函数不修改输入参数
void process(const char *str) {
    str[0] = 'A';  // 编译错误
}

// 防止意外修改
size_t strlen(const char *str);  // 标准库函数的声明
```

**安全价值**：
- 编译期防止意外修改
- 明确接口契约（函数是否会修改参数）
- 允许编译器优化（const全局变量可能被放在只读数据段，const局部变量可能被优化到寄存器）

### volatile：禁止优化

`volatile`告诉编译器：这个变量可能被程序外部因素改变（如硬件、中断处理程序、其他线程），**不要优化对它的访问**。

```c
volatile int hardware_register;  // 硬件寄存器映射

// 编译器不会优化掉看似"多余"的读取
int a = hardware_register;
int b = hardware_register;  // 确保读取两次，因为硬件可能在两次读取间改变值
```

**典型场景**：
1. **硬件寄存器**：内存映射I/O
2. **信号处理**：被信号处理程序修改的标志变量
3. **嵌入式系统**：状态寄存器、中断标志

> **注意**：`volatile`只保证每次访问都从内存读取，不提供线程安全保证。多线程安全问题将在第四章详细讨论。

### restrict：指针别名优化（C99）

`restrict`承诺：该指针是访问其指向对象的**唯一途径**，允许编译器进行激进优化。

```c
void copy(int *restrict dest, const int *restrict src, size_t n) {
    for (size_t i = 0; i < n; i++) {
        dest[i] = src[i];  // 编译器可以假设dest和src不重叠
    }
}

// 如果违反restrict承诺，结果未定义
int arr[10];
copy(arr, arr + 1, 5);  // 未定义行为！dest和src重叠
```

**优化效果**：编译器可以重排内存访问、使用向量化指令，因为它知道不会有别名干扰。

**注意**：违反`restrict`承诺是程序员的责任，编译器不会检查，违反时行为未定义。

---

## 变量作用域与生命周期

### 作用域（Scope）

作用域决定了变量名在代码中的**可见范围**。

#### 1. 文件作用域（File Scope）

```c
int global_var;           // 文件作用域，整个文件可见
static int file_local;    // 文件作用域，仅本文件可见（内部链接）

void func() {
    global_var = 10;      // 可以访问
}
```

#### 2. 函数作用域（Function Scope）

```c
void func() {
    int local_var;        // 函数作用域
}  // local_var在此处失效

void other_func() {
    local_var = 10;       // 错误！local_var不可见
}
```

#### 3. 块作用域（Block Scope）

```c
void func() {
    int x = 10;
    
    if (x > 5) {
        int y = 20;       // 块作用域，仅在if内可见
        printf("%d\n", x);  // 可以访问外层x
    }
    
    printf("%d\n", y);    // 错误！y已超出作用域
}
```

**C99改进**：允许在任意位置声明变量（类似C++）

在C89中，所有变量必须在函数开头声明；C99放宽了这一限制，允许在需要时才声明变量，这样可以：
- **缩小作用域**：变量仅在需要的代码块中可见，减少命名冲突
- **就近初始化**：在使用变量的位置声明，避免未初始化错误
- **增强可读性**：变量声明靠近使用处，代码逻辑更清晰

```c
// C89风格：所有声明在函数开头
void old_style() {
    int i;
    int sum = 0;
    
    // 代码逻辑...
    for (i = 0; i < 10; i++) {
        sum += i;
    }
    // i在整个函数中都可见，即使只在for循环中使用
}

// C99风格：就近声明
void new_style() {
    int sum = 0;
    
    for (int i = 0; i < 10; i++) {  // i的作用域仅限于for循环
        sum += i;
    }
    // i在此处不可见，避免意外使用
    
    // 可以重新声明同名变量
    for (int i = 0; i < 5; i++) {   // 这是另一个i，与上面的不冲突
        printf("%d\n", i);
    }
}
```

这种改进提高了代码安全性：变量作用域越小，出错的可能性越低。

### 生命周期（Lifetime）

生命周期决定了变量在内存中**存在的时间**。

| 变量类型 | 生命周期 | 存储位置 |
|---------|---------|----------|
| 全局变量 | 程序启动到结束 | Data段/BSS段 |
| 静态变量（`static`） | 程序启动到结束 | Data段/BSS段 |
| 局部变量（自动） | 函数调用期间 | 栈 |
| 动态分配（`malloc`） | `malloc`到`free` | 堆 |

**常见陷阱：返回局部变量地址**
```c
int* dangerous_function() {
    int local = 42;
    return &local;  // 警告/错误！local在函数返回后被销毁
}

int main() {
    int *ptr = dangerous_function();
    printf("%d\n", *ptr);  // 未定义行为！悬空指针
}
```

**正确做法**：
```c
// 方案1：返回静态变量（但有线程安全问题）
int* static_function() {
    static int value = 42;
    return &value;
}

// 方案2：使用堆分配
int* heap_function() {
    int *ptr = malloc(sizeof(int));
    *ptr = 42;
    return ptr;  // 调用者负责free
}

// 方案3：由调用者提供缓冲区
void safe_function(int *output) {
    *output = 42;
}
```

---

## 指针深入（Pointers）

指针是C语言最强大也最危险的特性，它允许直接操作内存地址。指针与内存安全问题密不可分，理解指针的行为是避免漏洞的关键。

### 指针基础回顾

```c
int x = 42;
int *ptr = &x;   // ptr存储x的地址

// 根据printf的格式符决定打印什么：
printf("%p\n", (void*)ptr);   // %p要求void*类型，确保所有平台都能正确打印地址（不同编译器对指针格式的处理可能不同）
printf("%d\n", *ptr);         // %d：打印整数值，需要解引用获取指针指向的数据，输出：42
```

**关键概念**：
- **指针变量本身**（`ptr`）：占用内存（通常8字节，64位系统），存储的是一个地址值
- **指针的值**（`ptr`的内容）：是另一个变量的地址（如`0x7ffc12345678`）
- **解引用**（`*ptr`）：通过地址访问指针指向的数据（得到`42`）

**理解差异**：
```c
// ptr 本身是一个变量，它的值是地址
printf("ptr的值（x的地址）：%p\n", (void*)ptr);     // 输出：0x7ffc12345678（x所在的地址）

// *ptr 是解引用操作，获取指针指向位置的数据
printf("ptr指向的值：%d\n", *ptr);                  // 输出：42（x的值）

// &ptr 是ptr这个指针变量本身的地址（注意：不是x的地址！）
printf("ptr变量的地址：%p\n", (void*)&ptr);        // 输出：0x7ffc87654321（ptr变量自己所在的内存位置）
```

**内存布局示意**：
```
内存地址        存储内容         变量名
0x7ffc12345678  42              x（int型）
0x7ffc87654321  0x7ffc12345678  ptr（int*型，存储的是x的地址）

- ptr的值 = 0x7ffc12345678（指向x）
- &ptr的值 = 0x7ffc87654321（ptr自己的位置）
- *ptr的值 = 42（x的值）
```

### 指针与const的深入组合

在类型限定符章节我们简单介绍了`const`与指针，这里深入分析：

```c
int x = 10, y = 20;

// 1. 指向常量的指针（底层const）
const int *p1 = &x;
*p1 = 30;        // 错误：不能修改指向的值
p1 = &y;         // 正确：可以改变指向

// 2. 常量指针（顶层const）
int *const p2 = &x;
*p2 = 30;        // 正确：可以修改指向的值
p2 = &y;         // 错误：不能改变指向

// 3. 指向常量的常量指针
const int *const p3 = &x;
*p3 = 30;        // 错误
p3 = &y;         // 错误

// 4. 复杂声明
const int **pp1;              // 指向"指向const int的指针"的指针
int *const *pp2;              // 指向"const指针(指向int)"的指针
int **const pp3;              // 常量指针，指向"指向int的指针"
```

**阅读技巧**：从右向左读，遇到`*`读作"指向...的指针"
- `const int *p` → p是指向const int的指针
- `int *const p` → p是常量指针，指向int
- `const int *const p` → p是常量指针，指向const int

### 指针运算

指针运算不是简单的整数加减，而是基于**所指向类型的大小**。

```c
int arr[5] = {10, 20, 30, 40, 50};  // 创建数组，5个元素连续存储在内存中
int *p = arr;                        // p获得arr[0]的地址，指向数组首元素

printf("%d\n", *(p + 0));  // 10，arr[0]
printf("%d\n", *(p + 1));  // 20，arr[1]
printf("%d\n", *(p + 2));  // 30，arr[2]

// p + 1 实际移动了 sizeof(int) 字节（通常4字节）
// 而不是1字节！
```

**合法的指针运算**：
```c
int *p1 = arr;
int *p2 = arr + 3;

// 1. 指针 + 整数
p1 + 2;              // 指向arr[2]

// 2. 指针 - 整数
p2 - 1;              // 指向arr[2]

// 3. 指针 - 指针（同类型）
ptrdiff_t diff = p2 - p1;  // 结果为3（元素个数，不是字节数）

// 4. 指针比较（同一数组内）
if (p1 < p2) {       // 比较地址大小
    // p1指向的元素在p2之前
}
```

> **注意**：指针运算必须在同一数组（或同一对象）内进行才有意义。越界访问、类型不匹配等危险操作将在第四章"内存安全问题"中详细讨论。

### 多级指针

指针可以指向指针，形成多级间接访问。

```c
int x = 42;
int *p = &x;       // 一级指针：指向int
int **pp = &p;     // 二级指针：指向int*
int ***ppp = &pp;  // 三级指针：指向int**

// 访问x的多种方式
x         // 直接访问：42
*p        // 一级解引用：42
**pp      // 二级解引用：42
***ppp    // 三级解引用：42

// 修改p的指向
int y = 100;
*pp = &y;          // 通过pp修改p，现在p指向y
printf("%d\n", *p);  // 输出：100
```

**典型应用：修改指针本身**
```c
void allocate(int **pp) {
    // pp是指向指针的指针（二级指针）
    // *pp表示"pp指向的那个指针"，即main中的p
    // malloc返回新分配内存的地址，赋值给*pp，相当于修改main中的p
    *pp = malloc(sizeof(int));  
    
    // **pp表示"pp指向的指针所指向的值"
    // 第一次解引用*pp得到p，第二次解引用*p得到malloc分配的int
    // 相当于给新分配的内存写入值42
    **pp = 42;
}

int main() {
    int *p = NULL;
    allocate(&p);      // 传递p的地址（&p的类型是int**）
                       // 函数内通过*pp可以修改p本身的值
    printf("%d\n", *p);  // 输出：42
    free(p);
}
```

### 函数指针

函数指针存储函数的地址，允许动态选择要调用的函数。

```c
// 1. 声明函数指针
int (*func_ptr)(int, int);  // 指向"接受两个int，返回int"的函数

// 2. 赋值
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

func_ptr = add;             // 方式1
func_ptr = &add;            // 方式2（等价）

// 3. 调用
int result = func_ptr(10, 20);      // 30
int result2 = (*func_ptr)(10, 20);  // 等价写法

// 4. 切换函数
func_ptr = sub;
int result3 = func_ptr(10, 20);     // -10
```

**应用场景：回调函数**
```c
void process_array(int *arr, int size, int (*callback)(int)) {
    for (int i = 0; i < size; i++) {
        arr[i] = callback(arr[i]);
    }
}

int double_value(int x) { return x * 2; }
int square_value(int x) { return x * x; }

int arr[] = {1, 2, 3, 4, 5};
process_array(arr, 5, double_value);  // {2, 4, 6, 8, 10}
process_array(arr, 5, square_value);  // {4, 16, 36, 64, 100}
```

**复杂声明**：
```c
// 函数指针数组
int (*func_arr[10])(int, int);   // 10个函数指针的数组

// 返回函数指针的函数
int (*get_func())(int, int) {
    return add;
}

// typedef简化
typedef int (*BinaryOp)(int, int);
BinaryOp op = add;               // 更清晰
```

### void指针：通用指针

`void*`是一种特殊的**通用指针类型**，可以指向任意类型的数据，但不包含类型信息。

**核心特性**：
- **类型擦除**：可以从任何指针类型隐式转换为`void*`（无需强制转换）
- **不可解引用**：因为编译器不知道指向的数据是什么类型，无法确定读取多少字节
- **需要显式转换**：使用前必须转换回具体类型的指针

```c
void *generic_ptr;
int x = 42;
double y = 3.14;

generic_ptr = &x;      // 正确：int* → void*（隐式转换）
generic_ptr = &y;      // 正确：double* → void*（隐式转换）

// *generic_ptr = 100; // 错误！void*不能解引用（编译器不知道类型）

// 必须先转换为具体类型
int *ip = (int*)generic_ptr;
*ip = 100;             // 正确
```

**典型应用场景**：

1. **标准库函数**：`malloc`等内存分配函数返回`void*`
   ```c
   void *ptr = malloc(sizeof(int));  // malloc返回void*
   int *ip = (int*)ptr;               // 转换为int*
   *ip = 42;
   free(ptr);
   ```

2. **通用回调函数**：传递任意类型的用户数据
   ```c
   void process(void *data) {
       int *num = (int*)data;  // 根据约定转换为int*
       printf("%d\n", *num);
   }
   
   int x = 100;
   process(&x);  // 传递int*，自动转换为void*
   ```

3. **通用数据结构**：链表、哈希表等存储任意类型数据
   ```c
   struct Node {
       void *data;      // 可以存储任意类型
       struct Node *next;
   };
   ```

**安全注意事项**：
- `void*`失去了类型安全保护，转换时必须确保类型正确
- 错误的类型转换会导致未定义行为（如将`int*`转为`double*`）

---

## 初始化行为

C语言中不同类型变量的初始化规则差异很大，理解这些规则对避免使用未初始化变量至关重要。

### 全局变量与静态变量

```c
int global1;              // 自动初始化为0（存储在BSS段）
int global2 = 0;          // 显式初始化为0（优化后也在BSS段）
int global3 = 10;         // 初始化为10（存储在Data段）

static int static1;       // 自动初始化为0
static int static2 = 20;  // 初始化为20
```

**保证**：C标准保证全局和静态变量如果不显式初始化，会被自动清零。

### 局部变量

```c
void func() {
    int local;            // 未初始化！值是垃圾（栈上的随机数据）
    printf("%d\n", local); // 未定义行为
    
    int initialized = 0;   // 正确：显式初始化
}
```

**危险**：使用未初始化的局部变量是常见的安全漏洞来源。

### 动态分配

```c
int *ptr1 = malloc(sizeof(int));      // 未初始化，包含垃圾值
int *ptr2 = calloc(1, sizeof(int));   // 初始化为0

printf("%d\n", *ptr1);  // 未定义行为
printf("%d\n", *ptr2);  // 安全，输出0
```

**最佳实践**：
```c
// 总是初始化变量
int x = 0;

// 或者使用calloc而非malloc
int *arr = calloc(100, sizeof(int));  // 所有元素初始化为0
```

---

## 总结：本章语法特性概览

| 语法特性 | 主要特性/行为 | 关键使用要点 |
|---------|-------------|-------------|
| `static` 局部变量 | 延长生命周期至整个程序，存储在Data段 | 只初始化一次，多次调用保持值 |
| `static` 全局/函数 | 限制为内部链接，仅本文件可见 | 防止命名冲突，实现模块化 |
| `extern` | 声明外部链接，不分配内存 | 用于访问其他文件定义的变量 |
| `const` | 标记为只读，编译器检查修改 | 防止意外修改，明确接口契约 |
| `volatile` | 禁止编译器优化，每次从内存读取 | 用于硬件寄存器、信号处理 |
| `restrict` | 承诺指针是唯一访问途径 | 允许编译器激进优化 |
| **指针基础** | 存储内存地址，通过`*`解引用访问数据 | 区分指针本身、指针的值、指向的数据 |
| **指针运算** | 基于类型大小移动，`p+1`移动`sizeof(type)` | 只在同一数组/对象内有效 |
| **多级指针** | 指针指向指针，多级间接访问 | 用于修改指针本身（如函数参数） |
| **函数指针** | 存储函数地址，支持动态调用 | 用于回调函数、策略模式 |
| **void指针** | 通用指针，可指向任意类型 | 使用前必须转换回具体类型 |
| **数组与指针** | 数组名退化为指向首元素的指针 | `sizeof(arr)` ≠ `sizeof(ptr)` |
| **初始化** | 全局/静态自动清零，局部变量未初始化 | 局部变量必须显式初始化 |


本章介绍了C语言中与内存相关的语法特性及其**正确用法**。下一章将讨论这些语法特性的**不当使用**会导致哪些内存安全问题，例如：
- 指针的不当操作（悬空指针、野指针、空指针解引用）
- 缓冲区越界、use-after-free等安全漏洞
- 未初始化变量导致的信息泄露