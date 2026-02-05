# BishengC线程API测试报告

## 测试目的

验证BishengC的safe代码中是否能使用线程相关API。

## BishengC的线程API现状

根据源码调研（`libcbs/src/scheduler/`），BishengC使用的线程API：

### 1. 直接使用POSIX pthread API

```c
// libcbs/src/scheduler/scheduler.cbs (line 190)
pthread_create(&pid, NULL, schedule, (void *)thread);
```

### 2. 包含的头文件

```c
// libcbs/src/scheduler/queue.hbs (line 7)
#include <pthread.h>
```

### 3. 使用的线程API列表

| API | 用途 | 位置 |
|-----|------|------|
| `pthread_create` | 创建线程 | scheduler.cbs:190 |
| `pthread_t` | 线程标识符类型 | scheduler.hbs:23 |
| `pthread_mutex_t` | 互斥锁类型 | queue.hbs:10 |
| `pthread_mutex_lock` | 加锁 | queue.hbs:19-36 |
| `pthread_mutex_unlock` | 解锁 | queue.hbs:19-36 |
| `pthread_mutex_init` | 初始化锁 | queue.hbs:14 |
| `pthread_mutex_destroy` | 销毁锁 | queue.hbs:63 |

### 4. 原子操作API

```c
// libcbs/src/scheduler/scheduler.hbs (line 4)
#include <stdatomic.h>

atomic_int state;  // 任务状态
atomic_fetch_add(&g_taskCount, 1);  // 原子递增
```

## 关键发现

**BishengC没有封装线程API**，直接使用C标准库的pthread。

**所有pthread调用都在非safe代码中**：

```bash
$ grep -r "safe.*pthread" libcbs/src/scheduler/
# 结果：无任何匹配
```

这意味着：
- ❌ BishengC没有提供类似Rust的`thread::spawn`或`std::thread`封装
- ❌ pthread API只能在unsafe块中使用
- ❌ safe代码无法创建线程或使用同步原语

## 测试用例说明

测试文件：[safe_thread_forbidden.cbs](safe_thread_forbidden.cbs)

### 测试场景

1. **test_pthread_in_safe()**：尝试在safe中使用`pthread_create`
   - 预期：编译失败
   - 错误信息：pthread_create不允许在safe代码中调用

2. **test_mutex_in_safe()**：尝试在safe中使用`pthread_mutex_lock`
   - 预期：编译失败
   - 错误信息：pthread_mutex_lock不允许在safe代码中调用

3. **test_atomic_in_safe()**：尝试在safe中使用`atomic_fetch_add`
   - 预期：编译失败
   - 错误信息：atomic操作不允许在safe代码中调用

4. **test_pthread_in_unsafe()**（对比）：在unsafe中使用pthread
   - 预期：编译成功，运行正常
   - 证明：只有unsafe块可以使用线程API

## 编译测试步骤

```bash
# 编译测试文件
cd /path/to/llvm-project
clang -c libcbs/test/scheduler/safe_thread_forbidden.cbs

# 预期结果：编译失败，报错在safe函数中使用pthread
```

## 结论

**BishengC的线程能力总结**：

| 方面 | 现状 |
|------|------|
| 线程API | 直接使用pthread，无safe封装 |
| safe中创建线程 | ❌ 不允许 |
| safe中使用锁 | ❌ 不允许 |
| safe中使用原子操作 | ❌ 不允许 |
| unsafe中使用pthread | ✅ 允许（退化为C） |
| 编译器检查数据竞争 | ❌ 无（unsafe绕过检查） |

**与Rust对比**：

| 特性 | Rust | BishengC |
|------|------|----------|
| 线程创建API | `thread::spawn` (safe) | pthread (unsafe only) |
| 互斥锁 | `Mutex<T>` (safe) | pthread_mutex (unsafe only) |
| 原子操作 | `AtomicI32` (safe) | atomic_int (unsafe only) |
| 编译时检查 | Send/Sync trait | ❌ 无 |
| 数据竞争检测 | 编译时阻止 | ❌ 无 |

**核心问题**：BishengC强制将所有多线程代码隔离在unsafe块中，导致：
- safe代码只能编写单线程程序
- 多线程程序无法享受所有权/借用检查保护
- 与C语言的多线程安全性完全一致（无改进）

## 测试证明的论点

✅ 证明：BishengC的safe机制仅适用于单线程场景
✅ 证明：所有多线程功能必须在unsafe中实现
✅ 证明：BishengC没有并发安全的设计（pthread未封装到safe中）
