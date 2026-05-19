# 翻译共享上下文

## 任务背景

把 Stanford **CS 110L（Safety in Systems Programming）** 2021 年春季第 3 讲的课堂转录稿翻译成**简体中文**，目标是一篇**可读性强的技术讲义**。原文是自动转写（ASR），存在无标点、口语填充词、转写错误等问题，译文必须**重写而非直译**。

## 目标风格

- **技术文档风格**：准确、清晰、简洁。
- **保留讲者亲和感**：课堂里讲师和学生互动的语气要在译文里能感受到，但不必逐字保留"嗯""呃""差不多""有点像"这些口语残留。
- **书面化语法**：完整句子、恰当标点、合理分段。
- **允许补小标题**：为了可读性，译文可以为主题段落增加二级/三级标题（原文本无结构）。

## 目标读者

通用读者（对系统编程/内存安全感兴趣但不一定天天写 C/C++/Rust）。需要注意：
- C/C++ 层面的底层名词（stack frame、malloc/free、buffer）可以稍加解释但不要啰嗦。
- Rust 特有术语（ownership、borrowing、move）首次出现配英文。
- 对非 Stanford 学生，关于 CS 107/106A/155 的课程内线索简要说明上下文。

## 翻译原则

1. **重写**，不是逐词翻译。"这段中文读起来像是母语作者重新写的吗？"是质量标准。
2. **准确至上**：技术事实、代码逻辑、数据不能改写。
3. **自然中文语序**：不要欧化长句，按需断句。
4. **术语一致**：按下文术语表统一翻译。首次出现技术术语时配英文（首次之后一般只用中文）。
5. **保留代码**：口述的代码要恢复成正规 Rust/C 代码块。
6. **图示描述**：讲者口头描述幻灯片图时，译文用"如图所示"或直接用文字还原图意。
7. **加注释补充**：对可能陌生的背景（如 CS 107 是 Stanford 的经典 C 编程课；Karel 是 CS 106A 的教学机器人）用 **（粗体括号）** 简要补充，**克制使用**，仅在帮助理解时加。

## 已识别的转写错误（按上下文还原）

| 转写 | 正确 |
|---|---|
| russ / rust | Rust |
| polio / valeo / blue / orion | Julio（主讲人名） |
| ran | Ryan |
| william | William（学生名） |
| vect / vek | vec |
| vec.data（讨论 C 代码时）| vec->data 或 vec.data |
| stir dupe | strdup |
| malik | malloc |
| dangly pointer | dangling pointer（悬垂指针）|
| stonemason carol | Stonemason Karel（石匠 Karel，CS 106A 机器人）|
| car star | `char*` |
| beer（在 bear 比喻处）| bear |
| vec free | vec_free |
| 106a | CS 106A |
| 107 | CS 107 |
| 155 | CS 155 |
| 242 | CS 242 |

## 术语表

| 英文 | 中文 | 备注 |
|---|---|---|
| memory safety | 内存安全 | |
| ownership model | 所有权模型 | 核心概念 |
| ownership | 所有权 | |
| owner | 所有者 | |
| borrow / borrowing | 借用 | 勿译为"租借" |
| move / moved | 移动（转移）/ 已移动 | Rust 所有权转移 |
| reference | 引用 | |
| memory leak | 内存泄漏 | |
| double free | 双重释放 | 括注 double free |
| use-after-free | 释放后使用 | 括注 use-after-free |
| dangling pointer | 悬垂指针 | 括注 dangling pointer |
| iterator invalidation | 迭代器失效 | |
| buffer overflow | 缓冲区溢出 | |
| remote code execution / RCE | 远程代码执行（RCE）| |
| stack / heap | 栈 / 堆 | |
| stack frame | 栈帧 | |
| pointer | 指针 | |
| pre/post condition | 前置条件 / 后置条件 | |
| type system | 类型系统 | |
| compile time | 编译期 | |
| compiler | 编译器 | |
| malloc / free | malloc / free | 函数名保持英文 |
| strdup | strdup | 同上 |
| vector / vec | 向量（vec）/ vec | C 语境译"向量"，Rust 的 `Vec` 保留类型名 |
| push | push | |
| allocate / free（动词）| 分配 / 释放 | |
| decomposition | 分解 | 编程教学语境 |
| scope | 作用域 | |
| function | 函数 | |
| variable | 变量 | |
| return | 返回 | |
| assignment | 赋值 | |
| buffer | 缓冲区 | |
| struct | 结构体 | |
| key / value（字典）| 键 / 值 | |
| heap allocated | 堆分配的（在堆上分配的）| |

## 比喻的处理

讲者用了多个生动比喻，翻译时完整保留：

- **Karel 机器人 / Stonemason 问题** → "石匠 Karel 问题（Stonemason Karel problem）"，保留机器人朝南/朝东的表述。
- **日托所 / 小熊玩偶 / 玩具架** → 贯穿 Rust 所有权介绍，用"玩具架""小熊""玩玩具"等自然中文表达。Julio 和 Ryan 作为"玩具的拥有者"的拟人化戏份要保留。
- **任天堂 DS（借给朋友又还回来）** → 直接保留为"任天堂 DS"。
- **拟人化代码（"我是个函数，我把这个值交给另一个人"）** → 保留第一人称比喻。

## 图示描述如何处理

讲者描述幻灯片图时使用 "here / this / that pointer is pointing to this" 等指示语。译文策略：
- 写成完整文字说明："向量初始指向一段旧缓冲区，push 触发扩容后我们分配新缓冲区，把数据拷过去，再把 `vec->data` 指向新缓冲区；而旧缓冲区仍未释放——这就是内存泄漏。"
- 必要时用"示意图"指代：如"（示意图中）迭代器 `n` 指向第一个元素"。

## 章节结构建议（译文组织）

根据内容主题，译文可分为以下小节（主标题用 H1，下列是 H2/H3）：

- **开场与事务通知**（极简处理）
- **向量练习：四类典型内存错误**
  - 内存泄漏（memory leak）
  - 双重释放（double free）与远程代码执行
  - 悬垂指针（dangling pointer）
  - 迭代器失效（iterator invalidation）
- **为什么这段代码这么糟？—— 结构与分解的价值**
  - 从石匠 Karel 讲起：分解与前/后置条件
  - 把思想搬到内存管理
- **C/C++ 中"所有权"的惯例表达**
  - openvswitch / ffmpeg 等真实案例
  - 自定义清理函数、键/值分别归属
- **C 类型系统的局限**
  - strdup 的启示
- **进入 Rust：所有权模型**
  - 一句 `let julio = bear_get()`
  - 赋值触发所有权移动
  - 编译期的检查与友好报错
- **所有权在函数调用中的表现**
- **借用（borrowing）：把分解找回来**
- **总结与 Q&A**
