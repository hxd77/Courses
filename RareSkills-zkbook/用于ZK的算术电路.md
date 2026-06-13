# ZK 算术电路





在零知识证明的背景下，算术电路是一个模拟 NP 问题的一组方程式。

我们关于 P 与 NP 的文章中的一个要点是，任何 P 或 NP 问题的解都可以通过将问题建模为布尔电路来验证。

然后，我们将原始问题的解转换为布尔变量的值集（称为证物），使得布尔电路返回真值。

这篇文章基于上面链接的那篇文章，所以请先阅读那篇。



## 算术电路作为布尔电路的替代方案

使用布尔电路来表示问题解决方案的一个缺点是，在表示算术运算（如加法或乘法）时可能显得冗长。

例如，如果我们想表达 $a + b = c$ 其中 $a = 8, b = 4, c = 12$ 我们必须将 $a$ ， $b$ ，和 $c$ 转换为二进制数。二进制数中的每一位都对应一个不同的布尔变量。在这个例子中，假设我们需要 4 位来编码 $a$ ， $b$ ，和 $c$ ，其中 $a₀$ 表示最低有效位（LSB），而 $a₃$ 表示最高有效位（MSB）的数字 $a$ ，如下所示：

-   `a₃, a₂, a₁, a₀`
    -   $a = 1000$
-   `b₃, b₂, b₁, b₀`
    -   $b = 0100$
-   `c₃, c₂, c₁, c₀`
    -   $c = 1100$

(暂时不需要知道如何将数字转换为二进制，我们将在文章后面解释该方法)。

一旦我们将 $a$ 、 $b$ 和 $c$ 以二进制形式写出，我们就可以写一个布尔电路，其输入是所有二进制位 $(a₀, a₁, …, c₂, c₃)$ 。我们的目标是写出一个这样的布尔电路，使得当且仅当 $a + b = c$ 时，电路输出为真。

这比预期的要复杂，正如下面这个模拟 $a + b = c$ 的二进制的大电路所示。为了简洁起见，我们省略了推导过程。我们仅展示公式来说明这种电路可以有多冗长：

```javascript
((a₄ ∧ b₄ ∧ c₄) ∨ (¬a₄ ∧ ¬b₄ ∧ c₄) ∨ (¬a₄ ∧ b₄ ∧ ¬c₄) ∨ (a₄ ∧ ¬b₄ ∧ ¬c₄)) ∧

((a₃ ∧ b₃ ∧ ((a₂ ∧ b₂) ∨ (b₂ ∧ (a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀)))) ∨
 (¬a₃ ∧ ¬b₃ ∧ ((a₂ ∧ b₂) ∨ (b₂ ∧ (a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀)))) ∨
 (¬a₃ ∧ b₃ ∧ ¬((a₂ ∧ b₂) ∨ (b₂ ∧ (a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀)))) ∨
 (a₃ ∧ ¬b₃ ∧ ¬((a₂ ∧ b₂) ∨ (b₂ ∧ (a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀))))) ∧

((a₂ ∧ b₂ ∧ ((a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀))) ∨
 (¬a₂ ∧ ¬b₂ ∧ ((a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀))) ∨
 (¬a₂ ∧ b₂ ∧ ¬((a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀)))) ∨
 (a₂ ∧ ¬b₂ ∧ ¬((a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀))))) ∧

((a₁ ∧ b₁ ∧ c₀) ∨ (¬a₁ ∧ ¬b₁ ∧ c₀) ∨ (¬a₁ ∧ b₁ ∧ ¬c₀) ∨ (a₁ ∧ ¬b₁ ∧ ¬c₀)) ∧

((a₀ ∧ b₀ ∧ c₀) ∨ (¬a₀ ∧ ¬b₀ ∧ c₀) ∨ (¬a₀ ∧ b₀ ∧ ¬c₀) ∨ (a₀ ∧ ¬b₀ ∧ ¬c₀)) ∧

¬ ((a₄ ∧ b₄) ∨
     (b₄ ∧ (a₃ ∧ b₃) ∨ (b₃ ∧ (a₂ ∧ b₂) ∨ (b₂ ∧ (a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀))) ∨
     (a₃ ∧ (a₂ ∧ b₂) ∨ (b₂ ∧ (a₁ ∧ b₁) ∨ (b₁ ∧ c₀) ∨ (a₁ ∧ c₀))))
```

关键在于，如果我们仅限于布尔输入和基本的布尔运算（AND、OR、NOT），对于基本问题，构建电路很快就会变得复杂和繁琐，尤其是当它们涉及算术运算时。

相比之下，在电路内部直接表示数字会简单得多。我们不再用布尔公式来模拟加法，而是直接对这些数字进行加法和乘法运算。

本文展示了使用算术电路也可以对 P 或 NP 中的任何问题进行建模。



##  算术电路

算术电路是一个仅使用加法、乘法和等式的方程系统。像布尔电路一样，它检查一组输入是否有效，但不计算解决方案。

以下是我们第一个算术电路的例子：

```javascript
6 = x₁ + x₂
9 = x₁x₂
```

我们说一个布尔电路被满足，当且仅当输入变量有一个赋值结果为真。**类似地，一个算术电路被满足，当且仅当变量有一个赋值使得所有方程都成立。**

例如，上述电路被 x₁ = 3, x₂ = 3 满足，因为电路中的两个方程都成立。相反，电路不被 `x₁ = 1, x₂ = 6` 满足，因为方程 `9 = x₁x₂` 不成立。

因此，我们可以将算术电路与电路中的方程集互换使用。一组输入“满足电路”，当且仅当这些输入使得所有方程都成立。



## 符号和术语

算术电路中的变量被称为信号，因为我们将用于编写 ZK 证明的编程语言 Circom 将它们这样称呼。

为了表示相等，我们将使用 `===` 运算符。我们使用这种符号，因为 Circom 使用它来声明两个信号具有相等的值，因此我们不妨习惯于看到它。

我们强调 `===` 是断言左侧和右侧相等。例如，在以下电路中：

`c === a + b`

我们不是将 `a` 加到 `b` 并将结果赋值给 `c` 。相反，我们假设 `a` 、 `b` 和 `c` 作为输入被提供，并断言它们之间存在的关系成立。这会限制 `a` 和 `b` 的和为 `c` 。

可以将 `c === a + b` 视为完全等同于 `assertEq(c, a + b)` 。类似地，表达式 `a + b === c * d` 完全等同于 `assertEq(a + b, c * d)` 。本质上，在电路中验证这些方程式涉及检查某些条件（约束）是否满足。证明其证据有效性的代理可以为信号分配任何值。但是，只有当所有约束都满足时，他们的证明（证据）才会被视为有效。

例如，如果代理希望证明：

```javascript
a === b + c + 3
a * u === x * y
```

他们必须从电路外部提供 `(a, b, c, u, x, y)` ，并将其分配给电路中的信号。

记住，上面的代码等同于：

```javascript
assertEq(a, b + c + 3)
assertEq(a * u, x * y)
```

对算术电路的一个有用心智模型是：所有信号都被视为输入而没有输出。

为了强调这一点，我们在下面的视频中提供了一个可视化。所有信号都是输入，使用 `===` 来检查而不是赋值。

<video src="https://video.wixstatic.com/video/706568_f4fb9d3d127c4735a718deffbd9fed70/1080p/mp4/file.mp4"></video>

视频中的电路可以写成：

```javascript
z + y === x
x + y === u
```

保持原意不变。

算术电路 `x === x + 1` 并不表示增量 `x` 。它是一个没有解的算术电路，因为 x 不能等于 `x + 1` 。因此，不可能满足这个约束。



##解释算术电路

考虑以下电路：

```javascript
x₁(x₁ - 1) === 0
x₁x₂ === x₁
```

第一个约束 `x₁(x₁ - 1) === 0` 将 x₁的可能值限制在 0 或 1。对于 `x₁` 的任何其他值都不会满足这个约束。

在第二个约束 `x₁x₂ === x₁` 中，有两种可能的场景：

-   如果 `x₁ = 1` ，则 `x₂` 也必须等于1，否则第二个约束无法满足。如果 `x₁ = 1` 和 `x₂ ≠ 1` ，则第二个方程变为 `1 * x₂ === 1` ，这只能通过 `x₂ = 1` 来满足，从而产生冲突。
-   如果 `x₁ = 0` ，那么 `x₂` 可以有任何值，因为 `0x₂ === 0` 很容易满足。

以下对 `(x₁, x₂)` 的赋值都是有效的证据：

-   $(x₁, x₂) = (1, 1)$
-   $(x₁, x₂) = (0, 2)$
-   $(x₁, x₂) = (0, 1337)$
-   $(x₁, x₂) = (0, 404)$

记住，一个方程组可以有许多解。类似地，一个算术电路也可以有许多解。不过通常，我们只对验证一个给定的解感兴趣。我们不需要找出算术电路的所有解。



###  布尔电路与算术电路

下表展示了布尔电路和算术电路的区别，但请记住它们都服务于验证证人的相同目的：

|              布尔电路              |                     算术电路                     |
| :--------------------------------: | :----------------------------------------------: |
|            变量是 0，1             |                     包含数字                     |
|     仅有的操作是 AND、OR、NOT      |              仅有的操作是加法和乘法              |
|          当输出为真时满足          | 当所有方程的左侧等于右侧时（没有输出）时满足条件 |
| 见证是满足布尔电路的布尔变量的赋值 |        见证是满足所有等式约束的信号的赋值        |

除了在某些情况下使用较少变量带来的便利外，算术电路和布尔电路都是完成相同工作的工具——证明你有一个 NP 问题的证明。



### 回到最初的例子 a + b = c

让我们重新审视上面的例子：编写一个布尔电路来表示方程 `a + b = c` ，其中我们给出 `c = 12` 。对于布尔电路，我们需要将 `a` 、 `b` 和 `c` 编码为二进制，每个需要 4 位（在这个例子中）。总共，电路有 12 个输入。相比之下，算术电路只需要 3 个输入： `a` 、 `b` 和 `c` 。输入数量的减少和整体电路规模的减小是我们更倾向于使用算术电路进行 ZK 应用的原因。、



###方程组与算术电路的相似性

布尔电路总是有一个表达式，当证人为真时返回真或假。

例如，如果我们有一组信号 $x$ 、 $y$ 和 $z$ ，并且我们希望将 $x$ 和 $y$ 的和约束为 $5$ ，那么我们需要一个单独的方程来实现这一点。我们希望约束的任何 z 都会有它自己的单独方程。

为了证明算术电路与布尔电路是等价的，我们稍后将展示任何布尔电路都可以转换为算术电路。这表明它们可以互换使用，以证明一个代理对 P 或 NP 问题有一个证人。



### 所有 P 问题都是 NP 问题的子集

如前一章关于 P 与 NP 的讨论所述，所有 P 问题在验证证人的计算需求方面都是 NP 问题的子集，因此我们今后将仅提及 NP 问题，并理解这包括 P。

我们的结论是，如果 NP 问题中的任何解可以用布尔电路建模，那么 NP（或 P）问题中的任何解都可以用算术电路建模。

但在我们证明它们等价之前，我们将提供一些用算术电路对 NP 问题的解进行建模的例子，以便我们获得对算术电路如何使用的直观理解。



## 算术电路的示例

在我们的第一个示例中，我们重新解决澳大利亚的 3 着色问题。在第二个示例中，我们演示如何使用算术电路来证明一个列表是有序的。



### 示例 1：使用算术电路建模 3 着色问题

当我们使用布尔电路来对一个 3 着色问题建模时，每个区域都有 3 个布尔变量——每个颜色一个——用来表示该区域是否已被分配了那种颜色。然后我们添加了约束来强制每个区域必须正好有一种颜色（颜色约束），以及约束来确保相邻的区域不会分配相同的颜色（边界约束）。

使用算术电路来建模这个问题更容易，因为我们可以为每个区域分配一个信号，用可能的值 $\set{1, 2, 3}$ 来表示它们的颜色，而不是三个布尔变量。我们可以任意地将颜色分配给数字，比如 `blue = 1` 、 `red = 2` 和 `green = 3` 。

对于每个区域，我们将其单一颜色约束写为：

```javascript
0 === (1 - x) * (2 - x) * (3 - x)
```

为了确保每个区域有且仅有一种颜色。上述约束只有在 `x` 为 1、2 或 3 时才能满足。

**3-Coloring 澳大利亚 **

![3 coloring of Australia](https://cdn.jsdelivr.net/gh/hxd77/BlogImage/TyporaImage/20260414193400842.jpeg)

回想起来，澳大利亚有六个领地：

-   `WA` = 西澳大利亚
-   `SA` = 南澳大利亚
-   `NT` = 北领地
-   `Q` = 昆士兰
-   `NSW` = 新南威尔士
-   `V` = 维多利亚

说 `WA = 1` 相当于说“给西澳大利亚涂蓝色。”类似地， `WA = 2` 表示“红色”被分配给了西澳大利亚，而 `WA = 3` 表示“绿色”被分配。

我们为每个地区设定的颜色约束（每个地区必须为蓝色、红色或绿色）变为：

```javascript
1) 0 === (1 - WA) * (2 - WA) * (3 - WA)
2) 0 === (1 - SA) * (2 - SA) * (3 - SA)
3) 0 === (1 - NT) * (2 - NT) * (3 - NT)
4) 0 === (1 - Q) * (2 - Q) * (3 - Q)
5) 0 === (1 - NSW) * (2 - NSW) * (3 - NSW)
6) 0 === (1 - V) * (2 - V) * (3 - V)
```

现在我们希望强制相邻的领土没有相同的颜色。实现这一目标的一种方法是将相邻领土的信号相乘，并确保乘积是一个“可接受的”值。考虑以下相邻领土 `x` 和 `y` 的表格：

|  x   |  y   | product  乘积 |
| :--: | :--: | :-----------: |
|  1   |  1   |       1       |
|  1   |  2   |       2       |
|  1   |  3   |       3       |
|  2   |  1   |       2       |
|  2   |  2   |       4       |
|  2   |  3   |       6       |
|  3   |  1   |       3       |
|  3   |  2   |       6       |
|  3   |  3   |       9       |

如果两个信号（相邻区域）具有相同的数字（颜色），那么它们的乘积将是上方的红色数字之一 $\set{1,4,9}$ 。如果 `x` 和 `y` 被约束为 1、2 或 3，并且 `x` 和 `y` 不相等，那么乘积 `xy` 将是 $\set{2, 3, 6}$ 之一。因此，如果 `xy = 2` 或 `xy = 3` 或 `xy = 6` ，**我们接受这个赋值，因为它意味着这两个相邻区域具有不同的颜色。**

对于每个相邻的领域 `x` 和 `y` ，我们可以使用以下约束来强制它们不相等：

```javascript
0 === (2 - xy) * (3 - xy) * (6 - xy)
```

上述方程成立当且仅当乘积 `xy` 等于 2、3 或 6。

边界约束是通过遍历边界并在视频下方所示的方式中，将每对相邻领土之间应用边界约束来创建的：

<video src="https://video.wixstatic.com/video/706568_71747f743e8e49c0955fa5de2f827ab4/1080p/mp4/file.mp4"> </video>

我们现在展示边界约束：

```javascript
Western Australia and South Australia:
7) 0 === (2 - WA * SA) * (3 - WA * SA) * (6 - WA * SA)

Western Australia and Northern Territory
8) 0 === (2 - WA * NT) * (3 - WA * NT) * (6 - WA * NT)

Northern Territory and South Australia
9) 0 === (2 - NT * SA) * (3 - NT * SA) * (6 - NT * SA)

Northern Territory and Queensland
10) 0 === (2 - NT * Q) * (3 - NT * Q) * (6 - NT * Q)

South Australia and Queensland
11) 0 === (2 - SA * Q) * (3 - SA * Q) * (6 - SA * Q)

South Australia and New South Wales
12) 0 === (2 - SA * NSW) * (3 - SA * NSW) * (6 - SA * NSW)

South Australia and Victoria
13) 0 === (2 - SA * V) * (3 - SA * V) * (6 - SA * V)

Queensland and New South Wales
14) 0 === (2 - Q * NSW) * (3 - Q * NSW) * (6 - Q * NSW)

New South Wales and Victoria
15) 0 === (2 - NSW * V) * (3 - NSW * V) * (6 - NSW * V)
```

通过结合两者，我们看到完整的用于证明我们为澳大利亚提供了有效三着色的算术电路：

```javascript
// color constraints
0 === (1 - WA) * (2 - WA) * (3 - WA)
0 === (1 - SA) * (2 - SA) * (3 - SA)
0 === (1 - NT) * (2 - NT) * (3 - NT)
0 === (1 - Q) * (2 - Q) * (3 - Q)
0 === (1 - NSW) * (2 - NSW) * (3 - NSW)
0 === (1 - V) * (2 - V) * (3 - V)

// boundary constraints
0 === (2 - WA * SA) * (3 - WA * SA) * (6 - WA * SA)
0 === (2 - WA * NT) * (3 - WA * NT) * (6 - WA * NT)
0 === (2 - NT * SA) * (3 - NT * SA) * (6 - NT * SA)
0 === (2 - NT * Q) * (3 - NT * Q) * (6 - NT * Q)
0 === (2 - SA * Q) * (3 - SA * Q) * (6 - SA * Q)
0 === (2 - SA * NSW) * (3 - SA * NSW) * (6 - SA * NSW)
0 === (2 - SA * V) * (3 - SA * V) * (6 - SA * V)
0 === (2 - Q * NSW) * (3 - Q * NSW) * (6 - Q * NSW)
0 === (2 - NSW * V) * (3 - NSW * V) * (6 - NSW * V)
```

我们有与布尔电路一样多的 15 个约束，但变量（信号）数量只有 1/3。对于每个区域，我们不再使用 3 个布尔变量，而是为每个区域使用一个信号。对于更大的电路，这种复杂性和空间的减少可能非常显著。



### 示例 2：证明列表已排序

给定一个数字列表 `[a₁, a₂, ..., aₙ]` ，如果 `aₙ ≥ aₙ₋₁ ≥ … a₃ ≥ a₂ ≥ a₁` ，我们称该列表是“已排序”的。换句话说，从末尾到开头，数字是非递增的。

我们的目标是编写一个算术电路来验证列表是否已排序。

为此，我们需要一个能表达两个信号 `a ≥ b` 的算术电路。这比乍一看要复杂，因为算术电路只允许进行等式、加法和乘法运算，而不支持比较操作。

但如果我们有一个“大于或等于”电路——称之为 `GTE(a,b)` ，那么我们会构建比较每对连续列表元素的电路： `GTE(aₙ, aₙ₋₁), ..., GTE(a₃, a₂), GTE(a₂, a₁)` ，如果所有这些条件都满足，那么列表就是排序好的。

要在没有 $≥$ 操作符的情况下比较两个十进制数，我们首先需要一个验证数字建议的二进制表示的算术电路，因此我们先稍微绕个弯谈谈二进制数。



### 前提：二进制编码

我们用下标 2 来书写二进制数。例如，11₂等于 3，101₂等于 5。每个 1 和 0 都称为一个比特。我们称最左边的比特为最高有效位（MSB），最右边的比特为最低有效位（LSB）。

正如我们很快将展示的，在转换为十进制时，最高位乘以最大的系数，最低位乘以最小的系数。所以如果我们把一个四位的二进制数写成 `b₃b₂b₁b₀` ， `b₃` 是最高位， `b₀` 是最低位。

下面的视频展示了将二进制的 1101 转换为十进制的 13：

如视频所示，一个四位二进制数可以通过以下公式转换为十进制数 `v` ：

`v = 8b₃ + 4b₂ + 2b₁ + b₀`

这也可以写成：

`v = 2³b₃ + 2²b₂ + 2¹b₁ + 2⁰b₀`

例如，1001₂ = 9，1010₂ = 10，等等。对于一个一般的 `n` 位二进制数，转换方法是：

`v = 2ⁿ⁻¹b₃ + ... + 2¹b₁ + 2⁰b₀`

我们省略了如何将十进制数转换为二进制数的讨论。目前，如果读者希望转换为二进制，可以使用 Python 的内置 `bin` 函数：

```javascript
>>> bin(3)
'0b11'
>>> bin(9)
'0b1001'
>>> bin(10)
'0b1010'
>>> bin(1337)
'0b10100111001'
>>> bin(404)
'0b110010100'
```

我们可以通过以下电路创建一个断言“ `v` 是一个具有四位二进制表示 `b₃` 、 `b₂` 、 `b₁` 、 `b₀` 的十进制数”的算术电路：

```javascript
8b₃ + 4b₂ + 2b₁ + b₀ === v

// force the "bits" to be zero or one
b₀(b₀ - 1) === 0
b₁(b₁ - 1) === 0
b₂(b₂ - 1) === 0
b₃(b₃ - 1) === 0
```

信号 `b₃, b₂, b₁, b₀` 被约束为 `v` 的二进制表示。如果 `b₃, b₂, b₁, b₀` 不是二进制，或者不是 `v` 的二进制表示，那么电路无法满足。

注意到对于信号 `(v, b₃, b₂, b₁, b₀)` 没有满足的赋值，其中 `v > 15` 。也就是说，如果我们把 `b₃, b₂, b₁, b₀` 设置为所有 1，这是约束允许的最高值，那么和将是 15。不可能加上更高的值。在 ZK 中，这有时被称为对 `v` 的范围检查。上面的电路不仅展示了 `v` 的二进制表示，还强制了 `v < 16` 。

我们可以将其推广到以下电路，该电路约束了 $v < 2^n$ ，并给出了 `v` 的二进制表示：

```javascript
2ⁿ⁻¹bₙ₋₁ +...+ 2²b₂ + 2¹b₁ + b₀ === v
b₀(b₀ - 1) === 0
b₁(b₁ - 1) === 0
//...
bₙ₋₁(bₙ₋₁ - 1) === 0
```

**说数字 `v` 最多用 `n` 位编码，相当于说 $v < 2^n$ 。**

要了解 $2^n$ 如何随 $n$ 的变化而变化，请考虑以下表格：

| n bits  n 位 | max value (binary)  最大值（二进制） | max value (decimal)  最大值（十进制） | 2ⁿ (decimal)  2ⁿ（十进制） | 2ⁿ (binary)  2ⁿ (二进制) |
| ------------ | ------------------------------------ | ------------------------------------- | -------------------------- | ------------------------ |
| 2            | 11₂                                  | 3                                     | 4                          | 100                      |
| 3            | 111₂                                 | 7                                     | 8                          | 1000                     |
| 4            | 1111₂                                | 15                                    | 16                         | 10000                    |
| 5            | 11111₂                               | 31                                    | 32                         | 100000                   |

请注意，二进制中的数字 $2^n$ 需要比值 $2^n - 1$ 多 1 位来存储。通过将数字编码的位数限制为 $n$ 位，它强制该数字小于 $2^n$ 。

记住 $2$ 的幂与存储它们所需的位数之间的关系是有帮助的。

-   $2^n$ 需要 $n + 1$ 位来存储。例如， $2^0=1_2$ ， $2^1 = 10_2$ ， $2^2=100_2$ ， $2^3=1000_2$ 等等。
-   $2^{n-1}$ 是 $2^n$ 的一半，需要 $n$ 位来存储
-   $2^n − 1$ 需要 $n$ 位来存储。当所有位都设置为 $1$ 时，这是 $n$ 位可以存储的最大值。

如果我们取一个数字 $n$ 并计算 $2^n$ ，我们会得到一个 $n + 1$ 位的数字，最高位是 1，其余位是 0。 $n = 3$ 在下面的示例中：

$$
2^n=\underbrace{1000}_{n+1\space bits}
$$
$2^{n-1}$ 与 $2^n / 2$ 相同。由于它被写成某个幂的形式，它仍然具有二进制数“形状”的特征，即最高位为 1 其余位为 0，但它将需要 $n$ 位来编码，而不是 $n + 1$ 位。

$$
2^{n-1}=\underbrace{100}_{n\space bits}
$$
$2^n −1$ 是一个 $n$ 位的数，所有位都设置为 1。

$$
2^n-1=\underbrace{111}_{n\space bits}
$$


### 用二进制计算 ≥

如果我们处理的是固定大小的二进制数， $n$ 位，那么 $2^{n-1}$ 这个数很特别，因为我们可以轻易地断言一个 $n$ 位的二进制数是否大于或等于 $2^{n-1}$ — 或者小于它。我们称 $2^{n-1}$ 为“中点”。下面的视频说明了如何比较一个 $n$ 位数与 $2^{n-1}$ 的大小：

<video src="https://video.wixstatic.com/video/706568_adae25cac0e6414ab0643a5792a2ed52/1080p/mp4/file.mp4"></video>

通过检查一个 $n$ 位数的最高有效位，我们可以判断该数是否大于或等于 $2^{n-1}$ 或小于 $2^{n-1}$ 。

如果我们计算 $2^{n-1} + \Delta$ 并查看该和的最高有效位，我们可以快速判断 $\Delta$ 是正数还是负数。如果 $\Delta$ 是负数，那么 $2^{n-1} + \Delta$ 必须小于 $2^{n-1}$ 。

<video src="https://video.wixstatic.com/video/706568_6b61fecfedb64a888f6538bc91707f40/1080p/mp4/file.mp4"></video>





###  检测 $u \ge v$ 是否为 $u \ge v$

如果我们用 $u - v$ 替换 $\Delta$ ，那么 $2^{n-1} + (u - v)$ 的最高位将告诉我们 $u ≥ v$ 或 $u < v$ 。

<video src="https://video.wixstatic.com/video/706568_ea57bc6fb8c5493686c3dc4cf9123c72/1080p/mp4/file.mp4"></video>



#### 防止 $2^{n-1} + (u - v)$ 溢出

如果我们限制 $u$ 和 $v$ 用最多 $n - 1$ 位表示，而 $2^{n-1}$ 用 $n$ 位表示，那么就不会发生下溢和上溢。当 $u$ 和 $v$ 都用最多 $n - 1$ 位表示时， $|u - v|$ 的最大绝对值是一个 $n - 1$ 位数。

我们看到在这种情况下 $2^{n-1} + (u - v)$ 不会下溢，因为 $2^{n-1}$ 至少比 $|u - v|$ 多 1 位。

现在考虑溢出情况。不失一般性，对于 $n = 4$ ，即四位数字，中点是 $2^{n-1} = 2^{4-1} = 8$ 或 $1000_2$ 。在这种情况下， $|u - v|$ 作为三位数能表示的最大值是 $111_2$ 。加上 $1000_2 + 111_2$ 得到 $1111_2$ ，这不是溢出。



### $u ≥ v$ 的算术电路总结，当 $u$ 和 $v$ 是 $n - 1$ 位数字时

-   我们将 $u$ 和 $v$ 限制为最多 $n - 1$ 位的数字。
-   我们创建一个算术电路，该电路使用 $n$ 位来编码 $2^{n-1} + (u - v)$ 的二进制表示。
-   如果 $2^{n-1} + (u - v)$ 的最高位是 1，那么 $u \geq v$ 就是 0，反之亦然。

用于检查 $u \geq v$ 的最终算术电路如下。我们固定 $n = 4$ ，这意味着 $u$ 和 $v$ 必须被约束为 3 位数字。感兴趣的读者可以将其推广到 $n$ 的其他值：

```javascript
// u and v are represented with at most 3 bits:
2²a₂ + 2¹a₁ + a₀ === u
2²b₂ + 2¹b₁ + b₀ === v

// 0 1 constraints for aᵢ, bᵢ
a₀(a₀ - 1) === 0
a₁(a₁ - 1) === 0
a₂(a₂ - 1) === 0
b₀(b₀ - 1) === 0
b₁(b₁ - 1) === 0
b₂(b₂ - 1) === 0

// 2ⁿ⁻¹ + (u - v) binary representation
2³ + (u - v) === 8c₃ + 4c₂ + 2c₁ + c₀

// 0 1 constraints for cᵢ
c₀(c₀ - 1) === 0
c₁(c₁ - 1) === 0
c₂(c₂ − 1) === 0
c₃(c₃ − 1) === 0

// Check that the MSB is 1
c₃ === 1
```

### 断言一个列表是有序的

现在我们已经有了比较信号对的算术电路，我们将这个电路对列表中的每个顺序对重复，并验证它是排序好的。



## 示例总结

我们已经展示了如何创建一个算术电路来模拟上一章中问题的解决方案。

现在我们可以将这一点推广，说我们可以使用一个算术电路来模拟任何 NP 问题。



## 如何用算术电路对布尔电路进行建模

任何布尔电路都可以使用算术电路进行建模。这意味着我们可以定义一个将布尔电路 B 转换为算术电路 A 的过程，使得满足 B 的一组输入可以被转换为满足 A 的一组信号。下面，我们概述了这个过程的关键组成部分，并通过一个将特定布尔电路转换为算术电路的例子进行说明。

假设我们有以下布尔公式： `out = (x ∧ ¬ y) ∨ z` 。当 ( `x` 为真 AND `y` 为假) OR `z` 为真时，该公式为真。

我们将 `x` 、 `y` 和 `z` 编码为算术电路信号，并限制它们的值只能是 0 或 1。

以下算术电路只有在 `x` 、 `y` 和 `z` 每个都是 0 或 1 时才能被满足。

```javascript
x(x - 1) === 0
y(y - 1) === 0
z(z - 1) === 0
```

现在让我们展示如何将布尔电路运算符映射到算术电路运算符，假设输入变量已被约束为 0 或 1。



### 与门

我们将布尔 AND `t = u ∧ v` 翻译为算术电路如下：

```javascript
u(u - 1) === 0
v(v - 1) === 0
t === uv
```

`t` 只有在 `u` 和 `v` 都为 1 时才会为 1，因此这个算术电路模拟了一个与门。由于约束条件 `u(u - 1) = 0` 和 `v(v - 1) = 0` ， `t` 只能是 0 或 1。



###  非门

我们将布尔非 `t = ¬u` 翻译成算术电路如下：

```javascript
u(u - 1) === 0
t === 1 - u
```

`t` 在 `u` 为 0 时为 1，反之亦然。由于约束 `u(u - 1) === 0` ， `t` 只能是 0 或 1。



### 或门

我们将布尔或 `t === u ∨ v` 翻译成算术电路如下：

```javascript
u(u - 1) === 0
v(v - 1) === 0
t === u + v - uv
```

要理解它为何能模拟或门，请考虑以下表格：

| u    | v    | u + v | uv   | t (u + v - uv) |
| ---- | ---- | ----- | ---- | -------------- |
| 0    | 0    | 0     | 0    | 0              |
| 0    | 1    | 1     | 0    | 1              |
| 1    | 0    | 1     | 0    | 1              |
| 1    | 1    | 2     | 1    | 1              |

如果 `u` 或 `v` 为 1，则 `t` 将至少为 1。为了防止 `t` 等于 2（这是布尔运算器的无效输出），我们减去 `uv` ，当 `u` 和 `v` 都为 1 时，`uv` 将为 1。

观察到，由于所有上述门电路，我们不需要应用约束 `t(t - 1) === 0` 。输出 `t` 被隐式约束为 0 或 1，因为没有输入赋值会导致 `t` 的值大于 2。



###将 `out = (x ∧ ¬ y) ∨ z` 转换为算术电路

现在我们已经看到了如何将布尔电路的所有允许操作转换为算术电路，让我们来看一个将布尔电路转换为算术电路的例子。

###创建 0 1 约束

```javascript
x(x - 1) === 0
y(y - 1) === 0
z(z - 1) === 0
```

### 用 NOT 的算术电路替换 `¬ y`

out = (x ∧ ¬ y) ∨ z

out = (x ∧ (1 - y)) ∨ z

###用算术电路替换 `∧` 中的 AND

out = (x ∧ (1 - y)) ∨ z

out = (x(1 - y)) ∨ z

### 用算术电路替换 `∨` 中的 OR

out = (x(1 - y)) ∨ z

out = (x(1 - y)) + z - (x(1 - y))z

我们最终的算术电路 `out = (x ∧ ¬ y) ∨ z` 是：

```javascript
x(x - 1) === 0
y(y - 1) === 0
z(z - 1) === 0
out === (x(1 - y)) + z - (x(1 - y))z
```

如果需要，我们可以简化最后一个方程：

```javascript
out === (x(1 - y)) + z - ((x(1 - y))z)
out === x - xy + z - ((x - xy)z)
out === x - xy + z - (xz - xyz)

out === x - xy + z - xz + xyz
```

我们也可以将算术电路写成如下形式，而不会改变其含义：

```javascript
x² === x
y² === y
z² === z
out === x - xy + z - xz + xyz
```

## Summary  摘要

**如果 NP 中每个问题的解都可以用布尔电路来建模，并且每个布尔电路都可以转换为等效的算术电路，那么可以得出结论：NP 中每个问题的解都可以用算术电路来建模。**

在实践中，ZK 开发者更倾向于使用算术电路而不是布尔电路，因为如前文示例所示，它们通常需要更少的变量就能完成相同的任务。

没有必要先计算布尔电路再将其转换为算术电路。我们可以直接用算术电路来模拟 NP 问题的解。

## Next steps  下一步

We have glossed over two very important details in this article. Some other challenges exist that need to be addressed. For example:

在本文中，我们忽略了两个非常重要的细节。还存在其他需要解决的问题。例如：

-   We didn’t discuss what datatype we used to store signals for the arithmetic circuit and how we handle overflow during addition or multiplication.
  
    我们没有讨论用于存储算术电路信号的数据类型，以及如何在加法或乘法过程中处理溢出。
-   We have no way of expressing the value 2/3 without losing precision. Any fixed point or floating point representation we choose will have rounding issues
  
    我们无法表示 2/3 的值而不损失精度。任何我们选择的定点或浮点表示都会有舍入问题

To handle these problems, arithmetic circuits are calculated over _[finite fields](https://www.rareskills.io/post/finite-fields):_ a branch of mathematics where all addition and multiplication is done modulo a prime number.

为了处理这些问题，算术电路在有限域上进行计算：数学的一个分支，其中所有的加法和乘法都是模一个素数进行的。

Finite field arithmetic has some surprising differences from regular arithmetic introduced by the modulo operator, so the next chapter will explore them in detail.

有限域算术与普通算术由于模运算符引入了一些令人惊讶的不同之处，因此下一章将详细探讨它们。

## Learn more with RareSkills

通过 RareSkills 了解更多。

Learn more about [Zero Knowledge Proofs](https://www.rareskills.io/zk-book) in our free ZK Book. This tutorial is a chapter in that book.

了解更多关于零知识证明的知识，请查看我们的免费 ZK 书籍。本教程是该书的一章。

## Practice Problems  练习题

1.  Create an arithmetic circuit that takes signals `x₁`, `x₂`, …, `xₙ` and is satisfied if _at least_ one signal is 0.
  
    创建一个算术电路，输入信号为 `x₁` 、 `x₂` 、…、 `xₙ` ，当至少有一个信号为 0 时电路满足条件。
    
2.  Create an arithmetic circuit that takes signals `x₁`, `x₂`, …, `xₙ` and is satsified if all signals are 1.
  
    创建一个算术电路，输入信号为 `x₁` 、 `x₂` 、…、 `xₙ` ，当所有信号都为 1 时电路满足条件。
    
3.  A bipartite graph is a graph that can be colored with two colors such that no two neighboring nodes share the same color. Devise an arithmetic circuit scheme to show you have a valid witness of a 2-coloring of a graph. Hint: the scheme in this tutorial needs to be adjusted before it will work with a 2-coloring.
  
    二分图是一种可以用两种颜色着色的图，使得没有两个相邻的节点具有相同颜色。设计一个算术电路方案来证明你有一个有效的图 2 着色证明。提示：本教程中的方案需要调整才能用于图 2 着色。
    
4.  Create an arithmetic circuit that constrains `k` to be the maximum of `x`, `y`, or `z`. That is, `k` should be equal to `x` if `x` is the maximum value, and same for `y` and `z`.
  
    创建一个算术电路，将 `k` 限制为 `x` 、 `y` 或 `z` 中的最大值。也就是说，如果 `x` 是最大值，则 `k` 应该等于 `x` ，如果 `y` 是最大值，则 `y` 应该等于 `z` 。
    
5.  Create an arithmetic circuit that takes signals `x₁`, `x₂`, …, `xₙ`, constrains them to be binary, and outputs 1 if _at least_ one of the signals is 1. Hint: this is tricker than it looks. Consider combining what you learned in the first two problems and using the NOT gate.
  
    创建一个算术电路，输入信号为 `x₁` 、 `x₂` 、…、 `xₙ` ，将它们约束为二进制，如果至少有一个信号为 1，则输出 1。提示：这比看起来要复杂。考虑结合前两个问题中学到的知识，并使用 NOT 门。
    
6.  Create an arithmetic circuit to determine if a signal `v` is a power of two (1, 2, 4, 8, etc). Hint: create an arithmetic circuit that constrains another set of signals to encode the binary representation of `v`, then place additional restrictions on those signals.
  
    创建一个算术电路来判断信号 `v` 是否为 2 的幂（1、2、4、8 等）。提示：创建一个算术电路，将另一组信号约束为编码 `v` 的二进制表示，然后对这些信号施加额外的限制。
    
7.  Create an arithmetic circuit that models the [Subset sum problem](https://en.wikipedia.org/wiki/Subset_sum_problem). Given a set of integers (assume they are all non-negative), determine if there is a subset that sums to a given value $k$. For example, given the set $\set{3,5,17,21}$ and $k = 22$, there is a subset $\set{5, 17}$ that sums to $22$. Of course, a subset sum problem does not necessarily have a solution.
  
    创建一个算术电路来模拟子集和问题。给定一组整数（假设它们都是非负的），判断是否存在一个子集的和等于给定的值 $k$ 。例如，给定集合 $\set{3,5,17,21}$ 和 $k = 22$ ，存在一个子集 $\set{5, 17}$ 的和为 $22$ 。当然，子集和问题不一定有解。
    
    Hint  提示
    
    Use a "switch" that is 0 or 1 if a number is part of the subset or not.
    
    使用一个"开关"，如果数字是子集的一部分则为 0 或 1。
8.  The covering set problem starts with a set $S = \set{1, 2, …, 10}$ and several well-defined subsets of $S$, for example: $\set{1, 2, 3}$, $\set{3, 5, 7, 9}$, $\set{8, 10}$, $\set{5, 6, 7, 8}$, $\set{2, 4, 6, 8}$, and asks if we can take at most $k$ subsets of $S$ such that their union is $S$. In the example problem above, the answer for $k = 4$ is true because we can use $\set{1, 2, 3}$, $\set{3, 5, 7, 9}$, $\set{8, 10}$, $\set{2, 4, 6, 8}$. Note that for each problems, the subsets we can work with are determined at the beginning. We cannot construct the subsets ourselves. If we had been given the subsets $\set{1,2,3}$, $\set{4,5}$ $\set{7,8,9,10}$ then there would be no solution because the number $6$ is not in the subsets.
  
    覆盖集问题从一个集合 $S = \set{1, 2, …, 10}$ 和几个定义明确的 $S$ 的子集开始，例如： $\set{1, 2, 3}$ 、 $\set{3, 5, 7, 9}$ 、 $\set{8, 10}$ 、 $\set{5, 6, 7, 8}$ 、 $\set{2, 4, 6, 8}$ ，并询问我们是否可以选取最多 $k$ 个 $S$ 的子集，使得它们的并集是 $S$ 。在上面的示例问题中， $k = 4$ 的答案是正确的，因为我们可以使用 $\set{1, 2, 3}$ 、 $\set{3, 5, 7, 9}$ 、 $\set{8, 10}$ 、 $\set{2, 4, 6, 8}$ 。请注意，对于每个问题，我们可以使用的子集在开始时就已经确定。我们不能自己构造子集。如果我们被告知子集是 $\set{1,2,3}$ 、 $\set{4,5}$ $\set{7,8,9,10}$ ，那么将没有解决方案，因为数字 $6$ 不在子集中。
    
    On the other hand, if we had been given $S = \set{1,2,3,4,5}$ and the subsets $\set{1}, \set{1,2}, \set{3, 4}, \set{1, 4, 5}$ and asked can it be covered with $k = 2$ subsets, then there would be no solution. However, if $k = 3$ then a valid solution would be $\set{1, 2}, \set{3, 4}, \set{1, 4, 5}$.
    
    另一方面，如果我们被告知 $S = \set{1,2,3,4,5}$ 和子集 $\set{1}, \set{1,2}, \set{3, 4}, \set{1, 4, 5}$ ，并询问是否可以用 $k = 2$ 子集覆盖，那么将没有解。然而，如果 $k = 3$ ，那么一个有效的解将是 $\set{1, 2}, \set{3, 4}, \set{1, 4, 5}$ 。
    
    Our goal is to prove for a given set $S$ and a defined list of subsets of $S$, if we can pick a set of subsets such that their union is $S$. Specifically, the question is if we can do it with $k$ or fewer subsets. We wish to prove we know which $k$ (or fewer) subsets to use by encoding the problem as an arithmetic circuit.
    
    我们的目标是证明对于给定的集合 $S$ 和定义好的 $S$ 的子集列表，是否能够选择一组子集，使得它们的并集是 $S$ 。具体来说，问题是是否可以用 $k$ 个或更少的子集完成。我们希望通过将问题编码为算术电路来证明我们知道要使用哪些 $k$ （或更少）的子集。
    

_Originally Published April 23, 2024

最初发表于 2024 年 4 月 23 日_