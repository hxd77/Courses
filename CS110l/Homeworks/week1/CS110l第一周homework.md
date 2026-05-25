# CS 110L: 系统编程中的安全性 

---
## 第一周练习

欢迎来到 CS 110L！很高兴在这里见到你。

##  目的

本周的练习旨在帮助你熟悉常见的 C/C++程序分析工具。静态和动态分析器非常有帮助，但它们各有主要局限性和不同的优势。这些练习将帮助你了解分析器可以检测的错误类型，以及那些更难发现的问题。

感到困惑？有疑问？我们很乐意交流！如果你遇到困难或对工具的功能感到好 奇，鼓励你在 Slack 上讨论。

截止日期：周四，4 月 8 日，晚上 11:59（太平洋时间）

这项作业需要 1-3 小时完成。

## 第一部分：熟悉环境

在这个作业中，我们将分析几个不同的程序。你可以从[这里](https://reberhardt.com/cs110l/spring-2021/assignments/week-1-exercises/week1.zip)下载源代码，或者，如果你在 myth 上工作，你可以使用命令行下载：

```
wget https://web.stanford.edu/class/cs110l/assignments/week-1-exercises/week1.zip
unzip week1.zip
```

你不需要为这个作业编写任何代码，但我们要求你写一些关于你调查发现的简要评论。你需要通过 Gradescope 提交一个 PDF 文件。

神话机器已经具备了本次作业中我们将使用的工具，但如果你希望在自己的计算机上工作，安装它们并不困难。你需要安装 Valgrind 和最新版本的 LLVM（版本 10 或更新版本），该版本包含 `clang-tidy` 和清理器。（如果你使用的是 Mac，默认安装不包括我们将使用的清理器，但你可以使用 `brew` 安装一个替代版本。）

## 程序 1：UPPERCASE

Our first target will be a simple program that takes a string as a command-line argument and prints that string uppercased:

我们的第一个目标是编写一个简单的程序，该程序接受一个命令行参数作为字符串，并打印该字符串的大写形式：

```
🍉  ./uppercase "hello world"
HELLO WORLD
```

该程序将输入字符串复制到一个可变缓冲区中，然后将每个小写字符替换为其大写对应字符。不幸的是，编写该程序的程序员忘记了字符串在末尾有一个空终止符，而用于存储大写字符串的缓冲区太小。

快速阅读一下代码，确保你理解了问题。然后，让我们尝试运行一些自动化工具，看看它们能发现什么！

侧注：你在 CS 110 的作业 2 中需要写类似这样的代码（不是将字符串转换为大写，而是将其分割成多个部分）。确保避免犯同样的（常见）错误 :)

### Static analysis  静态分析

This problem will manifest no matter what input you provide, and it’s one that an experienced programmer can easily find. How does `clang-tidy` fare?

这个问题无论你提供什么输入都会出现，而且一个有经验的程序员很容易发现。 `clang-tidy` 的表现如何？

`clang-tidy` is pretty easy to run. Give it a spin:

`clang-tidy` 运行起来相当简单。试试看：

```
🍉  clang-tidy 1-uppercase.c
Error while trying to load a compilation database:
Could not auto-detect compilation database for file "1-uppercase.c"
No compilation database found in /afs/.ir/users/r/e/rebs/static-analyzer-test or any parent directory
fixed-compilation-database: Error while opening fixed database: No such file or directory
json-compilation-database: Error while opening JSON database: No such file or directory
Running without flags.
```

Based on what you know from lecture, why might `clang-tidy` not see this problem? (There is no one correct answer we’re looking for here. Just speculate.)

根据你在讲座中学到的知识， `clang-tidy` 为什么可能看不到这个问题？（这里没有唯一正确的答案，只是进行推测。）

### Dynamic analysis with Valgrind

使用 Valgrind 进行动态分析

Let’s see if Valgrind does any better. First, we need to make sure you’ve compiled the program. Then, run it under Valgrind:

让我们看看 Valgrind 是否能做得更好。首先，我们需要确保你已经编译了程序。然后，在 Valgrind 下运行它：

```
🍉  make
🍉  valgrind ./1-uppercase "hello world"
==649566== Memcheck, a memory error detector
==649566== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==649566== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==649566== Command: ./1-uppercase hello\ world
==649566==
HELLO WORLD
==649566==
==649566== HEAP SUMMARY:
==649566==     in use at exit: 0 bytes in 0 blocks
==649566==   total heap usage: 1 allocs, 1 frees, 1,024 bytes allocated
==649566==
==649566== All heap blocks were freed -- no leaks are possible
==649566==
==649566== For lists of detected and suppressed errors, rerun with: -s
==649566== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

Uh oh… Valgrind thinks we’re in the clear as well. Based on what you know from lecture, why does Valgrind fail us here?

哎呀……Valgrind 也认为我们没问题。根据你在讲座中学到的知识，为什么 Valgrind 在这里会失败？

### Dynamic analysis with sanitizers

使用卫生器进行动态分析

Recall that Valgrind does “binary instrumentation”: you give it a fully compiled binary, and it injects extra assembly code that helps it observe every time a program accesses/allocates/frees memory.

回想一下 Valgrind 进行“二进制插桩”：你给它一个完全编译好的二进制文件，它会注入额外的汇编代码，帮助它观察程序每次访问/分配/释放内存的情况。

By contrast, LLVM sanitizers do “source instrumentation”: you give it source code, and it injects extra code that keeps track of memory accesses. Then, it compiles that modified source code into a binary that has these extra checks in place. Since this source instrumentation is actually part of the compilation process, we need to modify the way we run our compiler in order to use sanitizers.

相比之下，LLVM 卫生器进行“源代码插桩”：你给它源代码，它会注入额外的代码来跟踪内存访问。然后，它将修改后的源代码编译成一个包含这些额外检查的二进制文件。由于这种源代码插桩实际上是编译过程的一部分，我们需要修改我们运行编译器的方式才能使用卫生器。

This may sound intimidating, but it’s actually pretty simple. Normally, we can compile a `.c` file into a binary by running a command such as this:

这可能听起来令人望而生畏，但实际上相当简单。通常，我们可以通过运行类似以下命令将一个 `.c` 文件编译成二进制文件：

```
clang -g -O0 1-uppercase.c -o 1-uppercase
```

(Translation: with debugging enabled (`-g`) and compiler optimizations turned off (`-O0`), compile `1-uppercase.c` into the executable `1-uppercase`.)

To inject sanitizers into our code, we can simply tell the compiler which sanitizers we’d like to run using the `-fsanitize` flag:

要向我们的代码中注入检查器，我们只需使用 `-fsanitize` 标志告诉编译器我们希望运行哪些检查器：

```
clang -g -O0 -fsanitize=address,leak,undefined 1-uppercase.c -o 1-uppercase
```

If you run this command, it will produce a `1-uppercase` binary that you can run. The compiler has injected the sanitizers into your code, so they have also been compiled into this binary; when you run the binary, the sanitizers will run as well, keeping tabs on what your program is doing.

如果你运行这个命令，它将生成一个 `1-uppercase` 二进制文件，你可以运行它。编译器已经将检查器注入到你的代码中，因此它们也被编译到这个二进制文件中；当你运行这个二进制文件时，检查器也会运行，监控你的程序正在做什么。

However, most people don’t compile their projects by running `clang` directly. You need to run the compiler on each individual source code file, and since most projects have many files (tens to millions), that would be far too cumbersome. Instead, we rely on _build systems:_ we tell the build system what files make up our programs, and the build system puts together all the right compiler commands for us. Since this assignment is focused on tooling, we thought it might be apt to give you some more insight into how your existing tooling works and how you can modify it to add assurance checks for your code.

然而，大多数人不会直接运行 `clang` 来编译他们的项目。你需要对每个单独的源代码文件运行编译器，而大多数项目都有许多文件（从几十到数百万不等），这会非常繁琐。相反，我们依赖构建系统：我们告诉构建系统哪些文件构成了我们的程序，然后构建系统会为我们组合所有正确的编译命令。由于这个作业的重点是工具，我们认为让你更深入地了解现有工具的工作原理以及如何修改它以添加代码的保证检查可能很合适。

#### `make` crash course   `make` 简明教程

`make` is the build system that we use in CS 110. When you run `make`, it searches for a `Makefile` that specifies how you want to run the compiler; then, it runs all the relevant commands _for_ you:

`make` 是我们在 CS 110 中使用的构建系统。当你运行 `make` 时，它会搜索一个 `Makefile` 来指定你希望如何运行编译器；然后，它会为你运行所有相关的命令：

```
🍉  make
/usr/bin/clang-10 -g -O0 -Wall -Wextra -std=c11   -c -o 1-uppercase.o 1-uppercase.c
/usr/bin/clang-10 1-uppercase.o  -o 1-uppercase
```

_Side note:_ In this case, we’ve actually opted to split the compilation process into two commands: a first step that compiles the `.c` file into a `.o` “object file,” and a second “linker” step that assembles the `.o` file into a binary. This is unnecessary in our specific case, because our simple program is compiled from only one file. However, most programs are built from many separate files; each file needs to first be compiled into a `.o` file, and then all the `.o` files are combined into the final program. Because this is how your CS 110 programs are, we have written this Makefile in that way.

旁注：在这种情况下，我们实际上选择将编译过程分为两个命令：第一步将 `.c` 文件编译为 `.o` “目标文件”，第二步是“链接器”步骤，将 `.o` 文件组装成二进制文件。在我们的特定情况下这是不必要的，因为我们的简单程序只从一个文件编译。然而大多数程序是由许多单独的文件构建的；每个文件需要首先编译成 `.o` 文件，然后所有 `.o` 文件被组合成最终程序。因为 CS 110 程序就是这样构建的，所以我们以这种方式编写了 Makefile。

Let’s take a look at the `Makefile` to see how it is structured.

让我们看一下 `Makefile` 的结构。

The first half of a `Makefile` typically declares _variables_. You can define any variables you like, although there are some with special names that have specific meanings. For example, `CC` and `CXX` specify the C and C++ compilers that `make` will use. `CFLAGS` and `CXXFLAGS` specify command-line arguments that should be passed to the C and C++ compilers, respectively. `LDFLAGS` specifies flags that should be passed to the linker (i.e. the second command that combines `.o` files into a binary).

`Makefile` 的前半部分通常声明变量。你可以定义任何你喜欢的变量，尽管有一些具有特殊名称的变量具有特定含义。例如， `CC` 和 `CXX` 指定 `make` 将使用的 C 和 C++编译器。 `CFLAGS` 和 `CXXFLAGS` 分别指定应传递给 C 和 C++编译器的命令行参数。 `LDFLAGS` 指定应传递给链接器（即第二个将 `.o` 文件组合成二进制文件的命令）的标志。

The second half of a `Makefile` defines _targets_, which can be invoked by running `make <target name>`. For example, this is the definition of the `clean` target:

`Makefile` 的后半部分定义了目标，可以通过运行 `make <target name>` 来调用。例如，这是 `clean` 目标的定义：

```
clean::
	rm -fr $(C_PROGS) $(C_PROGS_OBJ)
	rm -fr $(CXX_PROGS) $(CXX_PROGS_OBJ)
```

Because of this, when you run `make clean`, Make will run the `rm` commands specified above.

因此，当你运行 `make clean` 时，Make 会运行上面指定的 `rm` 命令。

Additionally, targets can be run by other targets. When you run `make` (with no extra arguments), it will run the `default` target:

此外，目标可以被其他目标调用。当你运行 `make` （不带额外参数）时，它会运行 `default` 目标：

```
default: $(PROGS)
```

The `PROGS` variable will be expanded into `default: 1-uppercase 2-linkedlist 3-bracket-parser 4-fibonacci`, so `make` will then run the `1-uppercase`, `2-linkedlist`, and `3-bracket-parser` targets, and so on.

`PROGS` 变量会被展开为 `default: 1-uppercase 2-linkedlist 3-bracket-parser 4-fibonacci` ，所以 `make` 会接着运行 `1-uppercase` 、 `2-linkedlist` 和 `3-bracket-parser` 目标，依此类推。

Looking at this you might think: _wait, but I don’t see a `1-uppercase` target defined anywhere!_ This target is actually defined here:

看到这可能你会想：等等，但我没在任何地方看到定义了 `1-uppercase` 目标！这个目标实际上在这里定义的：

```
$(C_PROGS): %:%.o
	$(CC) $^ $(LDFLAGS) -o $@
```

This is expanded into a bunch of targets, one for every string in the `C_PROGS` variable. Expanded, they look like this:

```
1-uppercase: 1-uppercase.o
	$(CC) $^ $(LDFLAGS) -o 1-uppercase
```

(If you’re curious, see the Makefile documentation about [pattern rules](https://www.gnu.org/software/make/manual/html_node/Static-Usage.html#Static-Usage).)

This says, “first, run the `1-uppercase.o` target. Then, run the compiler with the provided `$(CC)` command (which is the linker command).”

_Wait, I don’t see a 1-uppercase.o target either!!!_ This one is even more confusing, because it’s an _[implicit target](https://www.gnu.org/software/make/manual/html_node/Catalogue-of-Rules.html#Catalogue-of-Rules)_ that is built into `make`. Long story short, it will automatically compile `1-uppercase.o` from `1-uppercase.c` using your `CC` and `CFLAGS` variables.

This long and confusing sequence of targets generates and runs these two compiler commands:

```
/usr/bin/clang-10 -g -O0 -Wall -Wextra -std=c11   -c -o 1-uppercase.o 1-uppercase.c
/usr/bin/clang-10 1-uppercase.o  -o 1-uppercase
```

And, if you have many programs in `C_PROGS` and `CXX_PROGS`, it will generate the appropriate commands for all of them.

Note: Makefiles are really arcane and confusing, and there have been many attempts to build modern replacements, but they’re still often used because they work, and you can copy/paste a Makefile from one project and tweak a few things for your new project until it does what you want it to (without understanding the whole thing). That’s mostly what we’re doing here, but we wanted you to have some basic insight into how they’re structured.

#### Updating your Makefile to enable sanitizers

Recall that the compiler and linker flags are controlled by the `CFLAGS`, `CXXFLAGS`, and `LDFLAGS` variables. To tell the compiler to inject AddressSanitizer, LeakSanitizer, and UndefinedBehaviorSanitizer into our programs, we simply need to add `-fsanitize=address,leak,undefined` to each of those three variables in our Makefile. Then, every time `make` runs the compiler, it will include that flag.

#### Recompile and run

With the Makefile updated, we can recompile and rerun (don’t forget to `make clean`):

```
🍉  make clean
rm -fr 1-uppercase 1-uppercase.o
rm -fr
🍉  make
/usr/bin/clang-10 -g -O0 -Wall -Wextra -std=c11 -fsanitize=address,leak,undefined   -c -o 1-uppercase.o 1-uppercase.c
/usr/bin/clang-10 1-uppercase.o -fsanitize=address,leak,undefined -o 1-uppercase
🍉  ./1-uppercase "hello world"
=================================================================
==655208==ERROR: AddressSanitizer: dynamic-stack-buffer-overflow on address 0x7ffda54e74eb at pc 0x0000004c32dc bp 0x7ffda54e7420 sp 0x7ffda54e7418
```

#### Question for you

Based on our discussions in lecture, how does AddressSanitizer find this error?

It is common to compile debug builds with sanitizers enabled. That way, you don’t need to go out of your way to test that your program doesn’t have memory errors (e.g. by separately running `valgrind ./myprogram`); every time you run it, the sanitizers will already be checking for you. However, sanitizers do slow your program down, so they are not included in release builds (i.e. versions of your program for others to use).

If you feel like trying sanitizers out on your CS 110 assignments, we’d love to hear how it goes! Later in the course, you won’t be doing much manual memory management, but there still may be a few things that the sanitizers catch. When you start writing multithreaded code, ThreadSanitizer will be very helpful.

## Program 2: Linked~~~Lists–

Take a look at `2-linkedlist.c`. This program creates a basic linked list with 20 elements. Then, it goes to the middle of the list and replaces the 10th node with a different one. Finally, it prints the list and frees all the elements.

There are at least two bugs in this program:

-   When replacing the 10th node, it removes an element from the list but does not free it, hence leaking memory.
-   At the end, when iterating over the list to print the values and free the nodes, the `while` condition is wrong. As written, it doesn’t print or free the last element of the list. (The condition should be `while (curr != NULL)`)

### Static analysis

Try running `clang-tidy` on this program. What do you find?

```
clang-tidy 2-linkedlist.c
```

I’m using `clang-tidy` from LLVM 10 (you can check the version by running `clang-tidy -v`), and at least in this version, `clang-tidy` reports a false positive about some dereference of a null pointer. That’s not actually possible in this program. Also, `clang-tidy` does not catch either memory leak.

Based on our discussions in class, speculate about what might be happening here. (There is no right answer that we are looking for.)

Interestingly, if you add `const` to `kNumElements` (it is declared as a global variable, even though it really should be a constant), the false positive goes away. Feel free to speculate about why, although this is optional. (It still does not catch the memory leaks.)

### Dynamic analysis

Let’s try running the sanitizers on this example! (No need to run Valgrind for this program.)

Your Makefile modifications for Program 1 should mean that Program 2 was also compiled with sanitizers included. If so, you can simply run the program:

```
./2-linkedlist
```

What do you find?

## Program 3: Parsing and Early Returns

Take a look at `3-bracket-parser.c`. This program takes a string formatted like `"abcd[efg]hij"` as an argument and prints out the portion of the string in brackets. For example:

```
🍉  ./3-bracket-parser 'hi [hello world]!'
Parsed string: hello world
```

However, this program has a very common error: it allocates resources at the beginning of the `parse` function, but fails to free the allocated memory if an error occurs (in this case, if a close `]` is not found).

### Static analysis

You know the drill! Let’s try running `clang-tidy`:

```
clang-tidy ./3-bracket-parser.c
```

What do you find?

### Dynamic analysis

Let’s try running sanitizers, which should already be baked into the program from your work in Program 1:

```
./3-bracket-parser 'hi [hello world]!'
```

Do the sanitizers catch any problems? Why or why not?

### Fuzzing

Recall that a “fuzzer” feeds a program with many semi-random inputs, aiming to find unusual inputs that trigger badly-behaved edge cases.

Let’s see if we can use a fuzzer to discover our bug. The two most common general-purpose fuzzers are [AFL](https://lcamtuf.coredump.cx/afl/) and [libFuzzer](https://llvm.org/docs/LibFuzzer.html). In this exercise, we’ll give libFuzzer a spin.

libFuzzer is built into LLVM/clang and injects extra code into your program similar to how the sanitizers work. libFuzzer will call a function in your program, providing you with some semi-random input; you can then pass that input to the code you want to fuzz.

Let’s see how this works.

#### Adding the fuzz target

First, add this function to `3-bracket-parser.c`:

```c
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // TODO: do something with `data` and `size`

    // libFuzzer functions always return 0
    return 0;
}
```

When we compile with libFuzzer, the fuzzer will dream up a strange input and pass a buffer/size containing this data to `LLVMFuzzerTestOneInput`. We can then manipulate this input and pass it to the part of our code that we are trying to fuzz.

In our case, we want to test our `parse` function. This function takes a null-terminated C string. Let’s transform libFuzzer’s input (which is just a buffer of arbitrary bytes) into a C string. First, allocate a buffer with enough space to fit the libFuzzer input plus a null terminator:

```c
char buf[size + 1];
```

Next, copy the input into the buffer:

```c
memcpy(buf, data, size);
```

Finally, null-terminate the string:

```c
buf[size] = '\0';
```

Now, `buf` contains a null-terminated string. Call `parse` on this string, and your fuzz target is complete!

**One last change:** libFuzzer will inject its own `main` function into your code, which starts the fuzzer (i.e. starts generating inputs and passing them to `LLVMFuzzerTestOneInput`). As such, you will need to comment out our `main` function, so that the two do not conflict.

#### Compiling with fuzzing enabled

To compile libFuzzer into our code, we simply add `fuzzer` to the list of sanitizers:

```
-fsanitize=fuzzer,address,leak,undefined
```

Doing this in the Makefile will cause problems because our Makefile is compiling several different programs, and we only set up one of them for fuzzing. Because our program is pretty simple, let’s just compile it directly without using `make`:

```
clang-10 -g -O0 -Wall -Wextra -std=gnu99 -fsanitize=fuzzer,address,leak,undefined -o 3-bracket-parser 3-bracket-parser.c
```

(If you are not running on `myth`, you may need to replace `clang-10` with whatever compiler you have installed.)

#### Running the fuzzer

Once everything is compiled, simply run the binary to start the fuzzer:

```
./3-bracket-parser
```

It shouldn’t take long for the fuzzer to find the memory leak. Take a look at the second to last line, which should say something like “Test unit written to `./leak-somelongstring`.” You can `cat` that file to view the input that libFuzzer found to cause your problem. In my case, the input was `\n[j`, although it’s likely to change each time you run the fuzzer.

#### Question for you

What input did your fuzzer generate?

Our parser is extremely simple and you could identify a problematic test case by hand, but parser code is known for being complicated, and there are many parsers with complex webs of `if` and `switch` statements and loops that are too hard to analyze by hand. Fuzzers are invaluable for analyzing these programs and have uncovered countless critical bugs in production software.

[“This Man Thought Opening a TXT File is Fine. He Thought Wrong”](https://www.paulosyibelo.com/2021/04/this-man-thought-opening-txt-file-is.html) is a fascinating writeup of a bug in MacOS TextEdit that allowed an attacker to steal arbitrary files via a simple .txt file. Fuzzing played a key role in discovering this vulnerability. (While fuzzing is usually used to figure out how to trigger memory errors in program, this researcher used it to figure out how to get TextEdit to send him information through a network request.)

## Program 4: Fibonacci

Take a look at `4-fibonacci.cpp`. This program has correctness problems. (For reference, the fibonacci sequence should be 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, …)

Does `clang-tidy` find any problems with this file? What about the sanitizers? Why do you think this might be?

## Part 5: Weekly survey

As you know, this is still an experimental class, and we want to make it as enjoyable and meaningful of an experience as possible. Please let us know how you’re doing using [this survey](https://forms.gle/nh93S9urFPADiehU7).

When you have submitted the survey, you should see a password. Include this code in your writeup when submitting.

## Submitting your work

Please submit a PDF writeup of your work on Gradescope.

There are five parts to this assignment, each worth 20%. You’ll earn the full 20% for each part if we can see that you’ve made a good-faith effort to complete it.
