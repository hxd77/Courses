# CS 110L: 系统编程中的安全性

---
## 第二周练习：Hello world

## Purpose  目的

本周的练习旨在帮助你熟悉编译/运行 Rust 代码和使用基本的 Rust 语法。学习任何语言（无论是人类、计算机还是其他）的最佳方式是通过沉浸式学习，因此你可以将这视为你在 Rustland 的留学。确保在 Instagram 上发布相关信息，吃一些 Döner Kebap，享受夜生活。我们希望这次练习能让我们在下周讨论你可能尚未在所学语言中见过的概念时顺利启动。

我们会在这里提供一些作业建议，但你可能还需要查阅 Rust 文档、Stack Overflow 等资料。我们（Ryan 和 Julio）可以通过 Slack 为你提供作业帮助。你也可以联系你的同学一起合作（但这个作业你必须独立完成自己的代码）。

截止日期：周四，4 月 15 日，下午 12:30（太平洋时间）



完成这个作业需要 1-3 小时。虽然这个作业只是让你熟悉 Rust 语言，但我们预计可能会遇到挑战；Rust 是一种相当古怪的语言，需要一些时间来适应这种不熟悉感。如果你在 2 小时时还没有接近完成，请告诉我们，以便我们可以解决任何可能困扰你的问题。

## 第一部分：熟悉环境

本周练习的第一部分是将一个简单的“hello world”程序运行起来！

我们已经在 myth 上为你配置好了 Rust 工具链，所以如果你想在 myth 上开发代码（就像你在 CS 110 课程中那样），应该可以顺利使用。但是，如果你想在本地机器上运行代码（例如因为你的网络连接不好或者身处地球另一端），你需要安装 [Rust工具链](https://www.rust-lang.org/tools/install).。

Regardless of whether you decide to work on myth or on your personal computer, you should take a moment to get your development environment set up for Rust. Ryan wrote up a [list of tips](https://reberhardt.com/cs110l/spring-2021/handouts/tools-tips/) that may be helpful. We highly recommend using [VSCode](https://code.visualstudio.com/) with the [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=matklad.rust-analyzer) plugin, as this will show extra information about how the compiler is interpreting your code. (When you first install this extension, it will probably pop up a notice that rust-analyzer isn’t installed. Click the button to install it.) If you plan to work on myth, you should also [install the SSH plugin](https://youtu.be/6mfMywNPUgU). If you plan on using a different editor, we recommend [installing rust-analyzer for your editor](https://rust-analyzer.github.io/manual.html#toctitle) and checking out our [list of tooling tips](https://reberhardt.com/cs110l/spring-2021/handouts/tools-tips/) (especially for vim).

无论你决定在 myth 上工作还是在个人电脑上工作，你都应该花点时间设置好 Rust 的开发环境。Ryan 列出了一份可能有帮助的[提示清单](https://reberhardt.com/cs110l/spring-2021/handouts/tools-tips/)。我们强烈推荐使用带有 rust-analyzer 插件的 VSCode，因为这将显示编译器如何解释你的代码的额外信息。（当你第一次安装这个扩展时，它可能会弹出一个通知，提示 rust-analyzer 没有安装。点击按钮进行安装。）如果你计划在 myth 上工作，你还应该安装 SSH 插件。如果你计划使用不同的编辑器，我们推荐为你的编辑器安装 rust-analyzer，并查看我们的工具提示清单（尤其是针对 vim 的部分）。

现在，让我们获取初始代码！在本课程中，我们将使用 Github 来管理作业提交。Github 是一个基于 `git` 构建的强大协作平台， `git` 是一种版本控制软件。（版本控制软件允许你管理代码的不同版本；你可以在不同时间点保存快照，如果代码最终崩溃，你可以回到之前的快照。这比保存 `code.c` 、 `code-working.c` 、 `code-working-copy.c` 、 `code-final.c` 、 `code-final-seriously.c` 和 `code-final-i-actually-submitted.c` ，然后困惑于它们是什么要好。） `git` 和 Github 是行业中的标准工具，如果你之前没有接触过它们，我们认为接触它们会很有价值。

你应该已经收到一封邀请邮件，邀请你加入 `cs110l/week2-SUNETID` 仓库。（如果没有，请告诉我们。）一旦你接受邀请，你就可以将这个仓库“克隆”（下载）到你的电脑上：

```
git clone https://github.com/cs110l/week2-YOURSUNETID.git week2
```

然后， `cd` 到 `week2/part-1-hello-world` 。这个目录包含一个 Rust 包。你可以在 `src/` 目录中查看源代码；查看 `src/main.rs` 。

让我们尝试编译这段代码！为此，运行以下命令：

```
cargo build
```

Cargo 有点像 `make` ，但它功能更强大。如果你的项目有依赖项，Cargo 会自动处理下载和配置这些依赖项。（它在 JavaScript 领域做 `npm` 做的事情，在 Python 领域做 `setup.py` 做的事情。）Cargo 还可以运行自动化测试、生成文档、对你的代码进行基准测试等等。我们现在不讨论这些，但稍后在这个学期中你会看到这些功能派上用场。

当你运行 `cargo build` 时，Cargo 会编译可执行文件并将其保存在 `target/debug/hello-word` 。现在试着运行一下：

```
🍓  ./target/debug/hello-world
Hello, world!
```

为了方便起见，Cargo 提供了一个 `run` 命令，可以一次性编译并运行程序。试着修改 `src/main.rs` 以打印一些新内容，然后运行 `cargo run` （不运行 `cargo build` ）。Cargo 会检测到文件已更改，重新编译你的代码，并为你运行二进制文件。

```
🍓  cargo run
   Compiling hello-world v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.77s
     Running `target/debug/hello-world`
You rock!
```

恭喜！你已经运行了你的第一个 Rust 程序！



## 第二部分：Rust热身（购物清单）

让我们用 Rust 写一个超级基础的程序！这个程序将从用户那里读取多个字符串，然后将它们打印回屏幕上。这个功能并不怎么令人兴奋，但它将帮助我们熟悉 Rust 语法。其中很多内容可能会让你感到熟悉，但与其他语言相比，Rust 有一些独特的特点。

这是当我们完成时程序应该如何工作：

```rust
🍓  cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.03s
     Running `target/debug/part-2-shopping-list`
Enter an item to add to the list: apples
Enter an item to add to the list: bananas
Enter an item to add to the list: cucumbers
Enter an item to add to the list: done
Remember to buy:
* apples
* bananas
* cucumbers
```

在你的文本编辑器中打开 `part-2-shopping-list/src/main.rs` 。我们将一起在这个文件中工作。

_Note: the Rust syntax overview was inspired by Will Crichton’s [CS 242 Rust lab handout](http://cs242.stanford.edu/f19/labs/rust).

注意：Rust 语法概述受到了 Will Crichton 的 CS 242 Rust 实验讲义的启发。_

###  数字和变量

Rust 中的数值类型包括 `i8` 、 `i16` 、 `i32` 和 `i64` （所有这些类型都存储有符号数——正数或负数），以及 `u8` 、 `u16` 、 `u32` 和 `u64` （这些类型存储无符号数——严格非负数）。数字 `8` 、 `16` 等表示一个值由多少位组成。这是为了避免 C 语言遇到的问题，因为 C 语言规范没有定义数值类型的标准宽度。在 CS 110 的作业 2 中，你会遇到这种情况；今天，在大多数计算机上，一个 `int` 存储 4 个字节（对应于 Rust 的 `i32` ），但你要处理的是 70 年代的代码，其中 `int` 只存储两个字节。

要声明一个变量，我们使用 `let` 关键字并指定变量的类型：

```rust
// 声明一个存储有符号32位整数的变量。（等同于C语言中的"int n = 1"）
let n: i32 = 1;
```

Rust 有一个很棒的功能，叫做“类型推断”。它不会强迫你声明每个变量的类型，而是允许你在编译器能够推断出类型应该是什么的情况下省略变量的类型。大多数 Rust 代码看起来是这样的，并且只有在编译器无法推断出应该使用哪种类型时才会包含显式的类型注解。

```rust
let n = 1;
```

与大多数语言不同，Rust 中的变量默认是常量。这是为了减少错误；如果你修改了一个你本不想修改的变量（即没有明确标记为可变），编译器会报错。添加 `mut` 可以使得变量可变。

```rust
let mut n = 0;
n = n + 1;  // compiles fine
```

###  字符串

Rust 中的字符串有点奇怪。有两种字符串类型： `&str` 和 `String` 。 `&str` 是一个指向内存中某个字符串的不可变指针。例如：

```rust
let s: &str = "Hello world";    //`: &str` 注解是可选的
```

在这里，字符串 `Hello world` 被放置在程序的只读数据段（这也是 C 语言的工作方式），而 `s` 是指向该内存的只读指针。

`String` 类型存储一个堆分配的字符串。你可以修改 `String` （只要使用 `mut` 关键字）。

```rust
let mut s: String = String::from("Hello "); // "字符串"类型注解为可选
s.push_str("world!");
```

第一行在堆上分配内存； `s` 是一个 `String` 对象，包含指向该内存的指针。第二行向堆缓冲区追加内容，如果需要则重新分配/调整缓冲区大小。字符串的内存将在最后一行使用 `s` 后自动释放。我们将在周四的讲座中更详细地讨论内存分配/释放。（这与 C++ `string` 的工作方式有些类似。）

### 一起编程：读取输入

让我们实现一个只存储单个杂货项目的购物清单程序的简单版本。

首先，我们需要从用户获取输入：

```rust
let input = prompt_user_input("Enter an item to add to the list: ");

println!("Remember to buy:");
println!("* {}", input);
```

使用打印语句时， `{}` 作为你想要打印内容的占位符（类似于 C 中的 `%d` / `%s` /等等）。

请注意，即使我们没有明确指定 `input` 的类型，编译器也会看到 `prompt_user_input` 返回一个 `String` ，并将 `String` 分配为 `input` 的类型。（如果你使用的是带有 rust-analyzer 插件的 VSCode，你应该会看到 `: String` 类型注解显示出来。）

###  集合

存储事物集合最简单的方法是使用向量：

```rust
let mut v: Vec<i32> = Vec::new();
v.push(2);
v.push(3);
// 即便在这里，`: Vec<i32>` 类型注解也是可选的。如果省略它，
// 编译器会向前查看该向量的使用方式，并据此推断出向量元素的类型。很巧妙！
```

Rust 也支持固定大小的数组。与 C 不同的是，数组的长度作为数组类型的一部分存储。此外，数组访问通常在运行时进行边界检查。这意味着如果出现越界访问，程序会崩溃而不是允许访问（C/C++ 中就是这样处理的）。请勿出现缓冲区溢出！

```rust
let mut arr: [i32; 4] = [0, 2, 4, 8];
arr[0] = -2;
println!("{}", arr[0] + arr[1]);
```

### 一起编程：存储多个输入

与其只提示用户输入一个值，不如提示（并存储）三个购物项目。

首先，我们将创建一个向量来存储输入：

```rust
let mut shopping_list = Vec::new();
```

请注意，这需要声明为 `mut` ，以便我们稍后可以修改它。此外，尽管这里没有明确指定这是一个字符串向量，但编译器稍后会注意到我们向向量中放入了字符串，并推断 `Vec<String>` 是适当的类型。真酷！

然后，我们可以将多个输入放入列表中：

```rust
shopping_list.push(prompt_user_input("Enter an item to add to the list: "));
shopping_list.push(prompt_user_input("Enter an item to add to the list: "));
shopping_list.push(prompt_user_input("Enter an item to add to the list: "));
```

然后打印这些输入：

```rust
println!("Remember to buy:");
println!("* {}", shopping_list[0]);
println!("* {}", shopping_list[1]);
println!("* {}", shopping_list[2]);
```

### 循环

你可以使用迭代器以及一些非常棒、类似 Python 的语法来遍历集合：

```rust
for i in v.iter() { // v 是上述向量
    println!("{}", i);
}

// 另一种语法，编译后与上述代码效果完全相同
for i in &v {
    println!("{}", i);
}

// 注意上方的 & 符号至关重要！这段代码虽能正常运行，但循环会获取向量中每个元素的所有权，
// 因此后续你将无法再使用该向量：
for i in v { //不含“&”符号
    println!("{}", i);
}
```

While 循环:

```rust
while i<20{
	i+=1;
}
```



Rust 还有一个特殊的循环，应该用来代替 `while true` :

```rust
let mut i = 0;
loop {
    i += 1;
    if i == 10 { break; }
}
```

如果你好奇这个循环为何存在，这里有一些讨论。简而言之，它有助于编译器对变量初始化做出一些假设。

条件语句与你熟悉的语言非常相似：

```rust
let i = 0;
if i < 10 {
    println!("i is less than 10!");
}
```

### 让我们一起编程：读取任意数量的输入

让我们在循环中读取输入，当用户输入“done”时停止。

我们可以使用一个 `loop` (“while true”) 来实现：

```rust
loop {
    let input = prompt_user_input("Enter an item to add to the list: ");
    if input.to_lowercase() == "done" {
        break;
    }
    shopping_list.push(input);
}
```

要打印购物清单，我们可以使用一个 `for` 循环：

```rust
println!("Remember to buy:");
// 从列表中借用一个迭代器，然后我们使用该迭代器
// 遍历每一个元素：
for item in &shopping_list {
    println!("* {}", item);
}
```

###  函数

最后，Rust 函数的声明如下：

```rust
// 返回值类型为i32的函数
fn sum(a: i32, b: i32) -> i32 {
    a + b
}

// 无返回值函数（不含"->"）
fn main() {
    // do stuff...
}
```

这里有两个可能令人惊讶的地方：

-   与变量（Rust 会愉快地推断变量类型）不同，对于返回值的函数，你必须指定返回类型。
  
-   在 `sum` 函数中没有 `return` 关键字！而且……它少了一个分号！
  
    这两件事实际上是相关的。Rust 是一种基于表达式的语言。在你可能熟悉的绝大多数语言中，存在表达式（求值得到值）和语句（不求值）。例如，在 C++中，三元运算符是一个表达式；它求值得到一个可以存储在变量中的值：
    
    ```c
    int x = someBool ? 2 : 4;
    ```
    
    相比之下， `if` 语句是语句，因为它们不求值。这段代码无法编译：
    
    ```c
    int x = if (someBool) {
        2;
    } else {
        4;
    }
    ```
    
    然而，在 Rust 中，一切都是表达式。（这与安全性无关。这是因为 Rust 深受函数式编程语言的影响，而函数式编程语言超出了本课程的范畴。）这是有效的 Rust 代码：
    
    ```rust
    let x = if someBool { 2 } else { 4 }
    ```
    
    函数是由分号分隔的表达式序列，其结果为最后一个表达式的值。上述的 `sum` 函数只有一个表达式 `a + b` ，因此 `sum` 函数将评估为（即返回） `a + b` 最终的结果。
    
    如果你加上分号并写出以下代码，你实际上会得到一个编译错误：
    
    ```undefined
    fn sum(a: i32, b: i32) -> i32 {
        a + b;
    }
    ```
    
    记住，函数是由分号分隔的表达式。因此，这个函数实际上包含两个表达式：分号前的 `a + b` 和分号后的空表达式。由于最后一个表达式是空的，这个函数最终什么也不返回。编译器会给出错误，因为该函数被声明为具有 `i32` 返回类型。
    
    由于一切都是表达式，你可能会写出这样的函数：
    
    ```rust
    fn fib(n: i32) -> i32 {
        if n <= 1 { n } else { fib(n-1) + fib(n-2) }
    }
    ```
    
    这可能成为从 C、Java 和 Python 等语言过渡过来时最难适应的事情之一，但一旦你习惯了，它就可以成为编写程序的一种优雅而简洁的方式。如果你对这种设计背后的影响感兴趣，可以考虑选修 CS 242（程序设计语言）！我们下周会更多地讨论这种语法，所以如果它让你感到困惑，不要太担心。
    

### 一起编程：分解为函数

我们可以轻松地将这个程序分解为两个函数：一个用于读取输入以形成购物清单，另一个用于打印购物清单。

你可以用几种不同的方式来编写这些函数。如果你有兴趣，可以自己尝试编写！这是我决定如何编写它们的方式：

```rust
fn read_shopping_list() -> Vec<String> {
   // 读取购物清单并返回

  // 注意：如果你试图在函数末尾返回名为“shopping_list”的变量，
  // 该函数的最后一行应写为“shopping_list”，
  // 而非“return shopping_list;”。二者效果相同，
  // 但前者被视为更符合惯用风格的写法。
}

fn print_shopping_list(shopping_list: &Vec<String>) {
    // 打印购物清单
}

fn main() {
    let shopping_list = read_shopping_list();
    print_shopping_list(&shopping_list);
}
```

请注意， `read_shopping_list` 创建了一个向量，然后将该向量的所有权传递给 `main` ，`main` 负责释放任何已分配的内存。然后， `main` 将 `print_shopping_list` 的引用传递给 `print_shopping_list` ，这样 `print_shopping_list` 可以查看列表，但 `main` 仍然保留所有权。

在这种情况下，由于 `main` 在打印购物清单后什么也不做，我们可以将所有权转移给 `print_shopping_list` ，而不是传递引用。然而，你可能想象在未来修改这个程序，让 `main` 做更多事情（例如将购物清单同步到云端或其他花哨的业务），所以 `main` 可能想保留所有权。

## Part 3: Ownership short-answer exercises

第三部分：所有权简答题练习

让我们通过一些简答题来思考所有权问题。对于以下每个示例，回答：这段代码能否编译？解释原因或理由。如果它不能编译，你可以做些什么改变来使其编译？（如果你不确定，可以运行编译器并尝试，但你需要提供高级的英文解释来解释它为什么能或不能工作。）

-    示例 1：
  
    ```rust
    fn main() {
        let mut s = String::from("hello");
        let ref1 = &s;
        let ref2 = &ref1;
        let ref3 = &ref2;
        s = String::from("goodbye");
        println!("{}", ref3.to_uppercase());
    }
    ```
    
    这段代码**不能编译**。
    
    原因是：`ref1` 是 `s` 的不可变引用（borrow），`ref2` 是 `ref1` 的引用，`ref3` 是 `ref2` 的引用。它们形成了一条引用链，最终都指向 `s`。然后 `s = String::from("goodbye")` 试图修改 `s`，但此时 `ref3` 在之后的 `println!` 中还要被使用，也就是说对 `s` 的不可变借用仍然活跃。
    
    Rust 的核心规则是：**当存在活跃的不可变引用时，不能对原始数据进行修改（可变操作）。** 这里 `s` 的赋值是可变操作，但 `ref3`（间接引用着 `s`）直到 `println!` 才结束生命周期，两者产生了冲突。
    
    要修复的话，最简单的方式是把 `s` 的重新赋值移到所有引用使用完毕之后：
    
    rust
    
    ```rust
    fn main() {
        let mut s = String::from("hello");
        let ref1 = &s;
        let ref2 = &ref1;
        let ref3 = &ref2;
        println!("{}", ref3.to_uppercase());
        s = String::from("goodbye"); // 移到这里，引用已经不再使用
    }
    ```
    
    或者干脆去掉 `s` 的重新赋值，如果不需要的话。
    
    
    
-   示例 2：
  
    ```rust
    fn drip_drop() -> &String {
        let s = String::from("hello world!");
        return &s;
    }
    ```
    
    这段代码**不能编译**。
    
    原因是：`s` 是函数内部的局部变量，当函数执行完毕时，`s` 会被释放（drop）。但 `return &s` 试图返回一个指向 `s` 的引用。函数返回后 `s` 已经不存在了，这个引用就会指向一块已经被释放的内存。
    
    这就是经典的**悬垂引用（dangling reference）**问题。Rust 的借用检查器（borrow checker）正是为了防止这种情况而存在的，它会在编译时拒绝这段代码。
    
    要修复的话，直接返回 `String` 本身，把所有权转移给调用者，而不是返回引用：
    
    rust
    
    ```rust
    fn drip_drop() -> String {
        let s = String::from("hello world!");
        s
    }
    ```
    
    这样 `s` 的所有权从函数内部转移到了调用者手中，内存不会被提前释放，也就不存在悬垂引用的问题了。
    
    

- 示例 3：

    ```rust
    fn main() {
        let s1 = String::from("hello");
        let mut v = Vec::new();
        v.push(s1);
        let s2: String = v[0];
        println!("{}", s2);
    }
    ```

    这段代码**不能编译**。

    原因是：`let s2: String = v[0]` 试图把 `v[0]` 的值**移动（move）**出来。但 `v[0]` 是通过索引访问 Vec 中的元素，Rust 不允许直接从 Vec 中移出元素，因为这样会在 Vec 内部留下一个"空洞"，使 Vec 处于不一致的状态。

    `v[0]` 实际上返回的是一个引用，而 `String` 没有实现 `Copy` trait，所以不能隐式复制，只能移动。但从 Vec 中移动又是不允许的，因此编译失败。

    有几种修复方式：

    **方式一：借用而非移动**，用引用来读取：

    rust

    ```rust
    let s2: &String = &v[0];
    println!("{}", s2);
    ```

    **方式二：克隆一份副本**，如果确实需要一个独立的 `String`：

    rust

    ```rust
    let s2: String = v[0].clone();
    println!("{}", s2);
    ```

    **方式三：用 `remove` 把元素从 Vec 中取出**，这样 Vec 会把这个元素彻底移除，不会留下空洞：

    rust

    ```rust
    let s2: String = v.remove(0);
    println!("{}", s2);
    ```

    最常用的是前两种，根据你是否需要拥有这个值的所有权来选择。

    

## 第四部分：猜单词

你的目标是实现一个命令行猜单词游戏。以下是一个可能的游戏运行的示例：

```rust
Welcome to Guess the Word!
The word so far is -------
You have guessed the following letters:
You have 5 guesses left
Please guess a letter: r

The word so far is ------r
You have guessed the following letters: r
You have 5 guesses left
Please guess a letter: s

The word so far is ---s--r
You have guessed the following letters: rs
You have 5 guesses left
Please guess a letter: t

The word so far is ---st-r
You have guessed the following letters: rst
You have 5 guesses left
Please guess a letter: l

The word so far is l--st-r
You have guessed the following letters: rstl
You have 5 guesses left
Please guess a letter: a
Sorry, that letter is not in the word

The word so far is l--st-r
You have guessed the following letters: rstla
You have 4 guesses left
Please guess a letter: b

The word so far is l-bst-r
You have guessed the following letters: rstlab
You have 4 guesses left
Please guess a letter: c
Sorry, that letter is not in the word

The word so far is l-bst-r
You have guessed the following letters: rstlabc
You have 3 guesses left
Please guess a letter: o

The word so far is lobst-r
You have guessed the following letters: rstlabco
You have 3 guesses left
Please guess a letter: e

Congratulations you guessed the secret word: lobster!
```

或者，你可能没有收到这个消息：

```rust
Welcome to Guess the Word!
The word so far is --------
You have guessed the following letters:
You have 5 guesses left
Please guess a letter: a

The word so far is --a-----
You have guessed the following letters: a
You have 5 guesses left
Please guess a letter: b
Sorry, that letter is not in the word

The word so far is --a-----
You have guessed the following letters: ab
You have 4 guesses left
Please guess a letter: c

The word so far is c-a-----
You have guessed the following letters: abc
You have 4 guesses left
Please guess a letter: d
Sorry, that letter is not in the word

The word so far is c-a-----
You have guessed the following letters: abcd
You have 3 guesses left
Please guess a letter: e
Sorry, that letter is not in the word

The word so far is c-a-----
You have guessed the following letters: abcde
You have 2 guesses left
Please guess a letter: f

The word so far is c-a-f---
You have guessed the following letters: abcdef
You have 2 guesses left
Please guess a letter: g
Sorry, that letter is not in the word

The word so far is c-a-f---
You have guessed the following letters: abcdefg
You have 1 guesses left
Please guess a letter: h

The word so far is c-a-f--h
You have guessed the following letters: abcdefgh
You have 1 guesses left
Please guess a letter: i

The word so far is c-a-fi-h
You have guessed the following letters: abcdefghi
You have 1 guesses left
Please guess a letter: j
Sorry, that letter is not in the word

Sorry, you ran out of guesses!
```

程序会在你正确完成单词或用完所有猜测次数时退出。



