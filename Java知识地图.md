# Java 知识地图 · 按功能分类

> 用途：把 Java 当成一套「工具柜」，按**你要干什么**找工具，而不是按语法书目录背。
> 交叉功能会在多个域里重复出现（并用「交叉」列标出它还在哪出现）；
> **基础通用**与**备注**各自单列在最前面/最后面。

统计：**18 个功能域 · 144 个功能条目 · 12 条基础通用 · 12 组交叉 · 13 条备注**

图例：🟩 **必修**＝本课（EiP WS26/27）讲且会考 ｜ 🟦 **涉及**＝课上提到、作业用过 ｜ ⬜ **课外**＝本课不讲，后面自学
课程列 `L1`＝第 1 讲（`02_EiP-01_…pdf`），`Blatt 4`＝第 4 份 Übungsblatt。

---

## 0. 两层地基 + 一张地图

```
第 0 层  基础通用（所有域共用）—— 语句、变量、命名、编译运行、读报错
第 1 层  18 个功能域（按「要做什么」分）—— 下面每节一张表
跨层    交叉项（同一个概念在多个域出现）+ 备注（易错点、版本、取舍）
```

---

## 0.5 一页提纲（先扫这个）

- **1. 输入输出与交互**（Ein-/Ausgabe）：控制台输出 · 控制台输入 · 格式化输出 · 命令行参数 · 标准错误流 · 文件读写（小文件） · 缓冲读大文件 · 统一数据源
- **2. 类型与数据表示**（Datentypen）：八种基本类型 · 字面量与后缀 · 类型转换 · 包装类与自动装箱 · 数组 · 二维数组 · 枚举 enum · 记录类 record · 局部类型推断
- **3. 运算与表达式**（Ausdrücke）：算术运算 · 整除与取余的坑 · 关系与逻辑 · 优先级与括号 · 自增自减 · 三元运算符 · 浮点误差 · 位运算
- **4. 控制流**（Kontrollfluss）：if / else if / else · switch 与 switch 表达式 · for 计数循环 · 增强 for · while / do-while · break / continue · 嵌套循环 · 带标签跳转
- **5. 方法与递归**（Prozeduren）：定义与调用 · 返回值与 void · 参数传递（只有值传递） · 方法重载 · 递归 · 可变参数 · 作用域与生命周期 · 纯函数与副作用
- **6. 类与对象**（Klassen und Objekte）：类与实例 · 字段与可见性 · 构造方法 · this · getter / setter · static 成员 · final · toString · equals 与 hashCode · 对象组合 · 内部类 / 匿名类
- **7. 继承·抽象类·接口·多态**（Vererbung und Interface）：extends 继承 · super · 方法重写 @Override · 多态与动态绑定 · 抽象类 abstract · 接口 interface · 接口默认方法 · instanceof 与模式匹配 · Object 根类
- **8. 集合与容器**（Collections）：List / ArrayList · LinkedList · Set / HashSet · Map / HashMap · TreeMap / TreeSet · 遍历方式 · Comparator / Comparable · Collections 工具类 · 不可变集合 · 选型决策
- **9. 泛型与类型系统**（Generics）：泛型类 / 泛型方法 · 类型参数 · 通配符 · 类型擦除 · 泛型与数组
- **10. 异常与资源管理**（Ausnahmen）：try / catch / finally · throw / throws · 受检 vs 非受检 · 自定义异常 · try-with-resources · 读异常信息 · 断言 assert
- **11. 文本与字符串处理**（Zeichenketten）：String 不可变 · 常用方法 · StringBuilder · 字符串比较 · 格式化 · 正则 · 字符与编码 · 字符分类
- **12. 函数式与 Stream**（Funktionale Programmierung）：函数式接口 · Lambda · 方法引用 · Stream 管道 · Optional · 并行 Stream
- **13. 文件与持久化**（Dateien）：Path / Files · 逐行处理 · 目录操作 · 对象序列化 · CSV / JSON · 显式指定编码
- **14. 并发与线程**（Nebenläufigkeit）：Thread / Runnable · synchronized · volatile · ExecutorService · 并发集合 · 竞态与死锁 · 虚拟线程
- **15. 内存·JVM·性能**（Laufzeit）：栈与堆 · 垃圾回收 · 字节码与 .class · 引用强度 · JVM 参数 · 性能直觉 · 内存泄漏（Java 也有）
- **16. 工具链·测试·调试**（Werkzeuge）：javac / java · 包与 classpath · jar 打包 · IDE（Eclipse） · 构建工具 · 单元测试 JUnit · 调试器 · 版本管理 Git · JDK 版本 · 读报错三步
- **17. 数据结构与算法**（Datenstrukturen und Algorithmen）：数组 · 链表 · 栈 / 队列 · 哈希表 · 树 / 二叉搜索树 · 排序 · 查找 · 复杂度记号 · 递归与分治
- **18. 设计与建模**（Entwurf und Modellierung）：UML 类图 · 封装 · 继承 vs 组合 · 单一职责 · 设计模式（23 种） · 不可变对象 · 接口隔离 · 命名与可读性

---

## 1. 基础通用（第 0 层，单列）

| 条目 | 说明 | 例子 |
|---|---|---|
| 语句与表达式 | 每条语句以分号结束；表达式有值 | `System.out.println(31-18+1);` |
| 变量声明与作用域 | 先声明类型（或 `var`）再用；块内可见 | `int i = 0;` |
| 命名规范 | 类 UpperCamel、方法/变量 lowerCamel、常量 UPPER_SNAKE | `class WortZaehler`、`int maxWert` |
| 缩进与空白 | 一般不影响语义，但影响可读性 | 统一 4 空格 |
| 注释 | `//` 行注释、`/* */` 块注释；写 why 不写 what | `// 用 getOrDefault 避免 null` |
| main 签名 | `public static void main(String[] args)` 一字不差 | JVM 只认这一个入口 |
| 类名 = 文件名 | `public class X` 必须在 `X.java` 里 | 否则编译报错 |
| 编译 → 运行两步 | `.java` →（javac）→ `.class` →（java/JVM）→ 运行 | 改了代码必须重新编译 |
| 读编译器报错 | 看第一行、行号、报错处的符号 | `';' expected` = 少了分号 |
| 类型直觉 | 8 种基本类型 + 引用类型；`int/int` 是整除 | `7/2 == 3` |
| 查文档 | Java API 文档、`javadoc`、IDE 里 Ctrl+点击 | 别背方法名 |
| 调试习惯 | 先做最小可复现、再二分定位、别一次改五处 | — |

---

## 2. 十八个功能域

第 2 列前面的〔〕是这一条的性质：〔关键字〕 / 〔注解〕 / 〔标准库〕 / 〔写法〕——〔关键字〕是语言自带的词，〔注解〕写在类或方法上，〔标准库〕是 JDK 现成的类（查文档），〔写法〕是语法或思路，不是某个名字。

### 2.1 输入输出与交互（Ein-/Ausgabe）

**解决什么问题：**程序怎么和外界交换数据：打印、读键盘、读文件。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **控制台输出** | 〔标准库〕`System.out.print / println / printf` | 打印结果、临时调试 | L1 · Blatt 1 · 🟩 必修 | 文本 |
| **控制台输入** | 〔标准库〕`new Scanner(System.in)、nextInt / nextLine` | 读用户输入 | Blatt 3–4 · 🟦 涉及 | 方法 |
| **格式化输出** | 〔标准库〕`String.format("%.2f")、printf("%d %s")` | 表格对齐、保留小数位 | Blatt 4 · 6 · 🟦 涉及 | 文本 |
| **命令行参数** | 〔标准库〕`String[] args` | 从外部传文件名/参数 | Blatt 6 · 🟦 涉及 | 工具链 |
| **标准错误流** | 〔标准库〕`System.err` | 错误信息与正常输出分开 | — · ⬜ 课外 | 异常 |
| **文件读写（小文件）** | 〔标准库〕`Files.readString / writeString` | 一次读入整个语料 | — · ⬜ 课外 | 文件 |
| **缓冲读大文件** | 〔标准库〕`BufferedReader、Files.lines` | 逐行处理，不爆内存 | — · ⬜ 课外 | 文件、算法 |
| **统一数据源** | 〔标准库〕`InputStream / Reader 抽象` | 同一段代码换键盘/文件 | — · ⬜ 课外 | 文件 |

### 2.2 类型与数据表示（Datentypen）

**解决什么问题：**数据在内存里怎么表示：数字、字符、真假、序列。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **八种基本类型** | 〔关键字〕`byte short int long float double char boolean` | 选对类型，避免溢出和精度问题 | L2 · Blatt 1–2 · 🟩 必修 | 运算 |
| **字面量与后缀** | 〔写法〕`1_000、10L、1.5f、'a'、'\n'` | 写常量不写错类型 | L2 · Blatt 2 · 🟩 必修 | 文本 |
| **类型转换** | 〔标准库〕`(int) 3.9、Integer.parseInt(s)` | 精度丢失、字符串转数字 | L2 · Blatt 2 · 🟩 必修 | 运算 |
| **包装类与自动装箱** | 〔标准库〕`Integer、Double、Integer.valueOf` | 集合里只能放对象 | L2 · 🟦 涉及 | 集合 |
| **数组** | 〔关键字〕`int[] a = new int[5]; a.length` | 定长同类型序列（三角、矩阵） | L4 · Blatt 4 · 🟩 必修 | 算法 |
| **二维数组** | 〔关键字〕`int[][] m = new int[3][4]` | 矩阵、表格、棋盘 | L4 · 🟦 涉及 | 算法 |
| **枚举 enum** | 〔关键字〕`enum Farbe { ROT, GRUEN, BLAU }` | 有限取值，替代魔法数字 | — · ⬜ 课外 | 类 |
| **记录类 record** | 〔关键字〕`record Punkt(double x, double y) {}` | 不可变数据载体（Java 16+） | — · ⬜ 课外 | 类 |
| **局部类型推断** | 〔关键字〕`var liste = new ArrayList<String>();` | 少写重复类型（Java 10+） | — · ⬜ 课外 | 工具链 |

### 2.3 运算与表达式（Ausdrücke）

**解决什么问题：**怎么算：算术、比较、逻辑，以及它们怎么组合。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **算术运算** | 〔写法〕`+ - * / %` | 基本计算 | L2 · Blatt 2 · 🟩 必修 | — |
| **整除与取余的坑** | 〔写法〕`7/2 == 3、7%2 == 1` | 整数除法不是四舍五入 | L2 · Blatt 2 · 🟩 必修 | 类型 |
| **关系与逻辑** | 〔写法〕`== != < > && \|\| !` | 条件组合；&& 短路求值 | L2 · Blatt 2 · 🟩 必修 | 控制流 |
| **优先级与括号** | 〔写法〕`2+3*x 是 2+(3*x)` | 歧义是 bug 之源（L1 第 23 页） | L1 · 🟩 必修 | 基础 |
| **自增自减** | 〔写法〕`i++、++i` | 循环计数；注意副作用 | L3 · Blatt 3 · 🟩 必修 | 控制流 |
| **三元运算符** | 〔关键字〕`int max = a > b ? a : b;` | 两选一，替代短 if | L3 · 🟦 涉及 | 控制流 |
| **浮点误差** | 〔写法〕`0.1+0.2 != 0.3；Math.abs(a-b) < 1e-9` | 小数比较必须给容差 | Blatt 6 · 🟩 必修 | 备注 |
| **位运算** | 〔写法〕`& \| ^ ~ << >> >>>` | 掩码、底层优化、哈希 | — · ⬜ 课外 | 运行时 |

### 2.4 控制流（Kontrollfluss）

**解决什么问题：**程序往哪走：分支、循环、提前跳出。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **if / else if / else** | 〔关键字〕`if (x > 0) { … }` | 分支 | L3 · Blatt 3 · 🟩 必修 | — |
| **switch 与 switch 表达式** | 〔关键字〕`switch (x) { case 1: … }；case -> yield` | 多分支、枚举分派 | L3 · 🟦 涉及 | 类型 |
| **for 计数循环** | 〔关键字〕`for (int i = 0; i < n; i++)` | 次数已知的循环 | L3 · Blatt 3 · 🟩 必修 | 运算 |
| **增强 for** | 〔关键字〕`for (int x : arr) { … }` | 遍历数组/集合（只读） | L4 · Blatt 4 · 🟩 必修 | 集合 |
| **while / do-while** | 〔关键字〕`while (b > 0) { … }` | 次数未知（欧几里得算法） | L1 · L3 · 🟩 必修 | 方法 |
| **break / continue** | 〔关键字〕`break; continue;` | 提前退出、跳过一轮 | L3 · 🟦 涉及 | — |
| **嵌套循环** | 〔标准库〕`两层 for 打三角形（Blatt 4）` | 图案、矩阵、穷举 | Blatt 4 · 🟩 必修 | 算法 |
| **带标签跳转** | 〔关键字〕`outer: for (…) { break outer; }` | 跳出多层（可读性差，少用） | — · ⬜ 课外 | — |

### 2.5 方法与递归（Prozeduren）

**解决什么问题：**怎么把一件事拆成可复用的块。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **定义与调用** | 〔关键字〕`static int add(int a, int b) { return a + b; }` | 拆分逻辑、消除重复 | L3 · Blatt 4 · 🟩 必修 | — |
| **返回值与 void** | 〔关键字〕`return wert; / void` | 有没有结果要交回 | L3 · 🟩 必修 | — |
| **参数传递（只有值传递）** | 〔写法〕`f(x) 复制一份进去` | 对象传的是引用的副本，改字段有效、换引用无效 | L3 · Blatt 6 · 🟩 必修 | 基础、类 |
| **方法重载** | 〔标准库〕`add(int,int) 与 add(double,double)` | 同名不同参（看参数选） | L3 · Blatt 6 · 🟩 必修 | 类 |
| **递归** | 〔写法〕`fak(n) = n * fak(n-1)` | 分治、遍历树、排列组合 | L3 · 🟦 涉及 | 算法 |
| **可变参数** | 〔写法〕`void f(String... xs)` | 参数个数不定 | — · ⬜ 课外 | — |
| **作用域与生命周期** | 〔写法〕`局部变量 / 字段` | 变量在哪一层可见 | L3 · 🟩 必修 | 基础 |
| **纯函数与副作用** | 〔写法〕`只依赖参数、只返回值` | 好测试、好推理 | — · ⬜ 课外 | 设计 |

### 2.6 类与对象（Klassen und Objekte）

**解决什么问题：**怎么把数据和行为捆成一个实体。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **类与实例** | 〔关键字〕`class Punkt { double x; } → new Punkt()` | 建模现实实体 | L5 · Blatt 5 · 🟩 必修 | — |
| **字段与可见性** | 〔关键字〕`private / public / protected` | 封装：外部只能通过方法改 | L5 · Blatt 5 · 🟩 必修 | 继承 |
| **构造方法** | 〔写法〕`Punkt(double x, double y) { … }` | 保证对象一出生就合法 | L5 · Blatt 5 · 🟩 必修 | — |
| **this** | 〔关键字〕`this.x = x;` | 区分字段与同名参数 | L5 · 🟩 必修 | — |
| **getter / setter** | 〔写法〕`getX() / setX(int x)` | 受控访问，可在 setter 里校验 | L5 · Blatt 5 · 🟩 必修 | — |
| **static 成员** | 〔关键字〕`static int counter;` | 类级共享：计数器、工具方法、main | L5 · Blatt 6 · 🟦 涉及 | 工具链 |
| **final** | 〔关键字〕`final double PI = 3.14;` | 常量、引用不可换 | L5 · 🟦 涉及 | 设计 |
| **toString** | 〔注解〕`@Override public String toString() { … }` | 打印/日志时人类可读 | Blatt 5–6 · 🟩 必修 | 文本 |
| **equals 与 hashCode** | 〔注解〕`@Override equals(Object o)、hashCode()` | 内容相等；放进 HashSet/HashMap 必须成对重写 | Blatt 6 · 🟦 涉及 | 集合 |
| **对象组合** | 〔关键字〕`class Buch { private Autor autor; }` | has-a 关系，优先于继承 | Blatt 5 · 🟦 涉及 | 设计 |
| **内部类 / 匿名类** | 〔写法〕`new Comparator<Punkt>() { … }` | 一次性小对象（Lambda 可替代） | — · ⬜ 课外 | 函数式 |

### 2.7 继承·抽象类·接口·多态（Vererbung und Interface）

**解决什么问题：**怎么让多个类共享行为、互相替换。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **extends 继承** | 〔关键字〕`class Hund extends Tier` | is-a 复用 | L6 · 🟩 必修 | 设计 |
| **super** | 〔关键字〕`super(); super.laut();` | 调父类构造/方法 | L6 · 🟩 必修 | — |
| **方法重写 @Override** | 〔写法〕`同签名、换实现` | 多态的基础 | L6 · 🟩 必修 | — |
| **多态与动态绑定** | 〔标准库〕`Tier t = new Hund(); t.laut();` | 一个接口多种实现，调用处不用改 | L6 · 🟩 必修 | 设计 |
| **抽象类 abstract** | 〔关键字〕`abstract class Form { abstract double flaeche(); }` | 半成品模板：有字段、有已实现方法 | L6 · 🟩 必修 | 备注 |
| **接口 interface** | 〔关键字〕`interface Zahlbar { double betrag(); }` | 能力契约，一个类可多实现 | L6 · 🟩 必修 | 备注 |
| **接口默认方法** | 〔关键字〕`default void log() { … }` | 给旧接口加方法不破坏实现者 | — · ⬜ 课外 | — |
| **instanceof 与模式匹配** | 〔关键字〕`if (t instanceof Hund h) { h.bellen(); }` | 类型判断 + 自动绑定（16+） | L6 · 🟦 涉及 | — |
| **Object 根类** | 〔标准库〕`toString / equals / hashCode` | 所有类都继承它 | L5–L6 · 🟩 必修 | — |

### 2.8 集合与容器（Collections）

**解决什么问题：**怎么装一堆东西并高效取用。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **List / ArrayList** | 〔标准库〕`new ArrayList<>()、add / get / size` | 可变长序列（首选） | L7 · Blatt 6 · 🟩 必修 | 算法 |
| **LinkedList** | 〔标准库〕`new LinkedList<>()` | 频繁头尾插删 | L7 · 🟦 涉及 | — |
| **Set / HashSet** | 〔标准库〕`new HashSet<>()、contains` | 去重、快速成员判断 | — · ⬜ 课外 | 算法 |
| **Map / HashMap** | 〔标准库〕`put / get / getOrDefault / entrySet` | 键值表（词频统计） | L7 · 🟦 涉及 | 算法 |
| **TreeMap / TreeSet** | 〔标准库〕`new TreeMap<>()` | 自动按键排序，可 range 查询 | — · ⬜ 课外 | — |
| **遍历方式** | 〔标准库〕`for-each、Iterator、forEach` | 边遍历边删要用 Iterator | L7 · 🟩 必修 | — |
| **Comparator / Comparable** | 〔标准库〕`compareTo、Comparator.comparing(...)` | 自定义排序规则 | L7 · 🟦 涉及 | 函数式 |
| **Collections 工具类** | 〔标准库〕`sort / reverse / max / min` | 常用操作一行搞定 | L7 · 🟦 涉及 | — |
| **不可变集合** | 〔标准库〕`List.of(1, 2, 3)` | 常量表，防被改 | — · ⬜ 课外 | 设计 |
| **选型决策** | 〔写法〕`要顺序？要唯一？要键值？要排序？` | 选错容器是性能 bug 的常见来源 | L7 · 🟦 涉及 | 备注 |

### 2.9 泛型与类型系统（Generics）

**解决什么问题：**怎么让容器「只装某一种东西」，并且在编译期就查出来。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **泛型类 / 泛型方法** | 〔关键字〕`class Box<T> { T inhalt; }` | 类型安全的容器 | — · ⬜ 课外 | 集合 |
| **类型参数** | 〔标准库〕`List<String> 与 List<Integer> 不能互转` | 编译期检查，省掉强制转换 | — · ⬜ 课外 | 集合 |
| **通配符** | 〔标准库〕`List<? extends Number>、? super T` | 读写限制（PECS 原则） | — · ⬜ 课外 | — |
| **类型擦除** | 〔写法〕`运行时没有泛型信息` | 不能 new T()、不能 instanceof List<String> | — · ⬜ 课外 | 运行时 |
| **泛型与数组** | 〔标准库〕`new T[10] 编译不过` | 用 List<T> 代替 | — · ⬜ 课外 | — |

### 2.10 异常与资源管理（Ausnahmen）

**解决什么问题：**出错时怎么办，以及怎么保证资源被释放。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **try / catch / finally** | 〔关键字〕`try { … } catch (IOException e) { … } finally { … }` | 捕获、兜底、必执行清理 | — · ⬜ 课外 | 文件 |
| **throw / throws** | 〔关键字〕`throw new IllegalArgumentException("…");` | 主动报错 / 声明可能抛 | Blatt 5–6 参数校验 · 🟦 涉及 | 方法 |
| **受检 vs 非受检** | 〔标准库〕`IOException 必须处理；NullPointerException 不必` | 决定要不要写 catch | — · ⬜ 课外 | 备注 |
| **自定义异常** | 〔关键字〕`class UngueltigeEingabe extends Exception { }` | 领域错误有名字 | — · ⬜ 课外 | 设计 |
| **try-with-resources** | 〔关键字〕`try (var in = Files.newBufferedReader(p)) { … }` | 自动关闭文件/流 | — · ⬜ 课外 | 文件 |
| **读异常信息** | 〔标准库〕`从最下面一行往上找、看 Caused by` | 调试第一技能 | 全部 Blatt · 🟩 必修 | 基础 |
| **断言 assert** | 〔关键字〕`assert x > 0 : "x muss positiv sein";` | 开发期自检（默认关闭） | — · ⬜ 课外 | 工具链 |

### 2.11 文本与字符串处理（Zeichenketten）

**解决什么问题：**怎么切、查、拼、比较字符串（计算语言学的日常）。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **String 不可变** | 〔标准库〕`s.toUpperCase() 返回新串` | 可安全共享；循环拼接慢 | L4 · Blatt 4 · 🟩 必修 | 运行时 |
| **常用方法** | 〔标准库〕`length / charAt / substring / indexOf / split / replace / trim` | 切分与查找 | L4 · Blatt 4 · 🟩 必修 | — |
| **StringBuilder** | 〔标准库〕`sb.append(x); sb.toString()` | 循环里拼串的正确做法 | L4 · 🟦 涉及 | 运行时 |
| **字符串比较** | 〔标准库〕`equals / equalsIgnoreCase / compareTo` | 内容比较，永远不用 == | Blatt 2 · 4 · 🟩 必修 | 备注 |
| **格式化** | 〔标准库〕`String.format("%.2f", x)` | 对齐表格、固定小数 | Blatt 4 · 6 · 🟦 涉及 | io |
| **正则** | 〔标准库〕`"\\s+".split(s)、replaceAll("[^A-Za-z]", "")` | 清洗文本（词频任务就靠它） | — · ⬜ 课外 | 算法 |
| **字符与编码** | 〔关键字〕`char vs String、UTF-8 / UTF-16、getBytes` | 德语变音符号乱码的根源 | L2 · L4 · 🟦 涉及 | 文件 |
| **字符分类** | 〔标准库〕`Character.isLetter / isDigit / toLowerCase` | 判断字母数字、统一大小写 | L4 · 🟦 涉及 | 类型 |

### 2.12 函数式与 Stream（Funktionale Programmierung）

**解决什么问题：**怎么把「做什么」当参数传，少写循环。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **函数式接口** | 〔标准库〕`Function / Supplier / Consumer / Predicate` | 把行为当参数 | — · ⬜ 课外 | — |
| **Lambda** | 〔写法〕`(a, b) -> a + b` | 简短实现接口（排序最常用） | Blatt 5–6 排序 · 🟦 涉及 | 集合 |
| **方法引用** | 〔标准库〕`String::length、System.out::println` | Lambda 的进一步简写 | — · ⬜ 课外 | — |
| **Stream 管道** | 〔标准库〕`list.stream().filter(…).map(…).sorted(…).toList()` | 声明式处理集合 | — · ⬜ 课外 | 集合 |
| **Optional** | 〔标准库〕`Optional.ofNullable(x).orElse(0)` | 显式表达「可能没有值」 | — · ⬜ 课外 | 异常 |
| **并行 Stream** | 〔标准库〕`.parallelStream()` | 大数据加速（小数据更慢，慎用） | — · ⬜ 课外 | 并发 |

### 2.13 文件与持久化（Dateien）

**解决什么问题：**怎么把数据存下来、读回来。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **Path / Files** | 〔标准库〕`Path.of("a.txt")、Files.readString(p)` | 读写文本（显式 UTF-8） | — · ⬜ 课外 | io |
| **逐行处理** | 〔标准库〕`Files.lines(p)、BufferedReader.readLine()` | 大语料不爆内存 | — · ⬜ 课外 | 算法 |
| **目录操作** | 〔标准库〕`Files.list、Files.createDirectories` | 批量处理、建输出目录 | — · ⬜ 课外 | 工具链 |
| **对象序列化** | 〔关键字〕`implements Serializable、ObjectOutputStream` | 直接存对象（长期存储慎用） | — · ⬜ 课外 | — |
| **CSV / JSON** | 〔标准库〕`手写 split 或库（Jackson）` | 数据交换格式 | — · ⬜ 课外 | — |
| **显式指定编码** | 〔标准库〕`StandardCharsets.UTF_8` | 避免平台默认编码坑 | — · ⬜ 课外 | 文本 |

### 2.14 并发与线程（Nebenläufigkeit）

**解决什么问题：**怎么同时做多件事，以及为什么这很难。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **Thread / Runnable** | 〔标准库〕`new Thread(r).start()` | 并行执行 | — · ⬜ 课外 | — |
| **synchronized** | 〔关键字〕`synchronized void f() { … }` | 互斥访问共享状态 | — · ⬜ 课外 | — |
| **volatile** | 〔关键字〕`volatile boolean fertig;` | 保证可见性（不保证原子性） | — · ⬜ 课外 | 运行时 |
| **ExecutorService** | 〔标准库〕`Executors.newFixedThreadPool(4)` | 线程池，别手动 new 一堆 | — · ⬜ 课外 | — |
| **并发集合** | 〔标准库〕`ConcurrentHashMap、CopyOnWriteArrayList` | 多线程共享容器 | — · ⬜ 课外 | 集合 |
| **竞态与死锁** | 〔写法〕`先问：哪些状态是共享的？` | 并发 bug 的根源 | — · ⬜ 课外 | 备注 |
| **虚拟线程** | 〔标准库〕`Thread.ofVirtual().start(r)（Java 21+）` | 高并发 IO | — · ⬜ 课外 | — |

### 2.15 内存·JVM·性能（Laufzeit）

**解决什么问题：**程序跑起来之后发生了什么。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **栈与堆** | 〔写法〕`局部变量在栈、对象在堆` | 理解引用与生命周期 | — · ⬜ 课外 | 类型 |
| **垃圾回收** | 〔写法〕`不可达对象自动回收` | 不用手动 free（但不能不管内存） | L1 · 🟦 涉及 | — |
| **字节码与 .class** | 〔标准库〕`javap -c HelloWorld` | 看编译器到底生成了什么 | L1 · 🟦 涉及 | 工具链 |
| **引用强度** | 〔写法〕`强 / 软 / 弱 / 虚引用` | 缓存与内存敏感场景 | — · ⬜ 课外 | — |
| **JVM 参数** | 〔标准库〕`-Xmx512m、-Xms512m` | 内存上限与初始值 | — · ⬜ 课外 | — |
| **性能直觉** | 〔标准库〕`先看复杂度，再看常数：拼接、装箱、IO` | 先写对，再写快 | L8 · 🟦 涉及 | 算法 |
| **内存泄漏（Java 也有）** | 〔写法〕`集合只增不删、监听器没注销` | 长跑程序必查 | — · ⬜ 课外 | 备注 |

### 2.16 工具链·测试·调试（Werkzeuge）

**解决什么问题：**怎么编译、怎么查错、怎么验证。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **javac / java** | 〔标准库〕`javac -encoding UTF-8 -d build X.java；java -cp build X` | 编译与运行两步 | L0 · Blatt 1 · 🟩 必修 | 基础 |
| **包与 classpath** | 〔关键字〕`package a.b;、-cp build` | 类文件在哪、怎么找 | Blatt 1 · 🟦 涉及 | — |
| **jar 打包** | 〔标准库〕`jar --create --file x.jar -C build .` | 分发可执行包 | — · ⬜ 课外 | — |
| **IDE（Eclipse）** | 〔写法〕`语法高亮、自动编译、补全、向导` | 提高日常效率 | L34 页 · 🟦 涉及 | — |
| **构建工具** | 〔标准库〕`Maven / Gradle` | 依赖管理与标准目录 | — · ⬜ 课外 | — |
| **单元测试 JUnit** | 〔注解〕`@Test、assertEquals` | 自动验证改动没弄坏东西 | — · ⬜ 课外 | — |
| **调试器** | 〔写法〕`断点、单步、看变量` | 比到处 println 强 | — · ⬜ 课外 | — |
| **版本管理 Git** | 〔标准库〕`commit、branch、diff` | 作业与项目必备 | — · ⬜ 课外 | — |
| **JDK 版本** | 〔标准库〕`本课用 Java 21（LTS）；--release 21` | 新特性可用性、兼容性 | L0 第 11 页 · 🟩 必修 | 备注 |
| **读报错三步** | 〔写法〕`第一行 + 行号 + 符号/标识符` | 80% 的错看这三样就够 | 全部 · 🟩 必修 | 基础 |

### 2.17 数据结构与算法（Datenstrukturen und Algorithmen）

**解决什么问题：**数据怎么组织、操作要多少代价。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **数组** | 〔关键字〕`随机访问 O(1)、插入删除 O(n)` | 最基础的序列 | L4 · L7 · 🟩 必修 | — |
| **链表** | 〔写法〕`插入删除 O(1)、查找 O(n)` | 频繁增删的序列 | L7 · 🟩 必修 | — |
| **栈 / 队列** | 〔标准库〕`Deque、push/pop、offer/poll` | 括号匹配、BFS、撤销 | L7 · 🟦 涉及 | — |
| **哈希表** | 〔标准库〕`HashMap 均摊 O(1)` | 计数、去重、索引 | L7 · 🟦 涉及 | 集合 |
| **树 / 二叉搜索树** | 〔标准库〕`有序、查找 O(log n)` | 索引、范围查询 | L7 · 🟦 涉及 | — |
| **排序** | 〔标准库〕`冒泡/插入/归并/快排、Arrays.sort` | 排序与比较器 | L8 · 🟩 必修 | 方法 |
| **查找** | 〔标准库〕`线性查找、二分（Arrays.binarySearch）` | 有序数据快速定位 | L8 · 🟦 涉及 | — |
| **复杂度记号** | 〔标准库〕`O(1) / O(log n) / O(n) / O(n log n) / O(n²)` | 估算「输入变大十倍会怎样」 | L8 · 🟩 必修 | 备注 |
| **递归与分治** | 〔写法〕`归并排序、二分递归` | 把大问题切成同类小问题 | L8 · 🟦 涉及 | 方法 |

### 2.18 设计与建模（Entwurf und Modellierung）

**解决什么问题：**写代码之前怎么想清楚结构。

| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |
|---|---|---|---|---|
| **UML 类图** | 〔写法〕`类框（字段/方法）+ 关系箭头` | 先画再写，作业要交（Blatt 5） | Blatt 5 · 🟩 必修 | — |
| **封装** | 〔关键字〕`private 字段 + 公开方法` | 改内部实现不影响调用方 | L5 · 🟩 必修 | — |
| **继承 vs 组合** | 〔标准库〕`is-a 用继承；has-a 用组合` | 默认选组合，继承只在真 is-a 时用 | L6 · 🟩 必修 | 备注 |
| **单一职责** | 〔写法〕`一个类只干一件事` | 可读、可测、可改 | — · ⬜ 课外 | — |
| **设计模式（23 种）** | 〔写法〕`单例、工厂、观察者、策略…` | 求职与大项目；现在只需知道名字 | — · ⬜ 课外 | 备注 |
| **不可变对象** | 〔关键字〕`final 字段、无 setter、防御性拷贝` | 线程安全、易推理 | — · ⬜ 课外 | 并发 |
| **接口隔离** | 〔写法〕`小而专的接口，别做胖接口` | 实现方不必写空方法 | — · ⬜ 课外 | — |
| **命名与可读性** | 〔标准库〕`类名名词、方法动词、lowerCamelCase` | 代码即文档（也是评分点） | 全部 · 🟩 必修 | 基础 |

---

## 3. 交叉项总表（同一概念，多处出现）

| 概念 | 出现在哪些域 | 为什么交叉 |
|---|---|---|
| **String** | 类型 · 文本 · 集合（作键） · 文件 · 输入输出 | 既是数据类型，又是文本处理对象，还常当 Map 的键、文件内容、输出单位 |
| **equals / hashCode** | 类与对象 · 集合 · 文本 | 定义在 Object（类域），用于内容比较（文本域），HashSet/HashMap 依赖它（集合域） |
| **值传递** | 方法 · 基础通用 · 类与对象 | 语法上属方法调用，语义上决定对象能不能被「改到」，所以贯穿基础与类 |
| **泛型** | 集合 · 泛型 · 函数式 | 集合靠它保证类型安全，函数式接口也带类型参数 |
| **try-with-resources** | 异常 · 文件 | 语法在异常域，用途是文件/流的自动关闭 |
| **Lambda** | 集合 · 函数式 · 并发 | 集合排序在用（Comparator），Stream 的基石，并发的任务提交也用 |
| **递归** | 方法 · 数据结构与算法 | 方法的一种写法，但真正价值在分治与树/图遍历 |
| **复杂度** | 数据结构与算法 · 内存·JVM·性能 · 备注 | 算法域定义，性能域测量，备注里决定「先优化哪里」 |
| **编码 UTF-8** | 文本 · 文件 · 输入输出 | 文本域的概念，落到文件与 IO 才踩坑（德语变音符号） |
| **多态** | 继承·接口 · 设计 · 集合（Comparator） | 继承域的机制，设计域的目的，集合域里 Comparator 就是多态的应用 |
| **static** | 类与对象 · 工具链（main） · 设计 | 类域定义，工具链里 main 必须 static，设计上滥用会破坏可测性 |
| **不可变性** | 文本（String） · 设计 · 并发 | String 的天然属性，设计上的主动选择，并发里最省心的策略 |

---

## 4. 备注（单列：易错点、版本、取舍、顺序）

- **1.** `==` 与 `equals` —— 基本类型比 `==`；对象比内容用 `equals`。`String` 用 `==` 会时对时错——这是本课最高频的错。
- **2.** determiniert 与 deterministisch —— 算法两性质：同输入同结果（结果确定）≠ 步骤顺序唯一（过程确定）。随机数 +2 是前者不是后者；16/4 或 2*2 是后者不是前者。
- **3.** 重载与重写 —— 重载（overload）= 同名不同参数，编译期选；重写（override）= 同签名换实现，运行期选。
- **4.** 抽象类与接口 —— 抽象类可以带状态和已实现方法；接口是纯契约（可有 default 方法）。要共享代码选抽象类，要能力契约选接口。
- **5.** String 与 StringBuilder —— `String` 不可变，循环里 `+=` 是 O(n²)；循环内拼接用 `StringBuilder`。
- **6.** 浮点比较 —— `0.1+0.2 != 0.3`。比较小数用 `Math.abs(a-b) < 1e-9`，别用 `==`。
- **7.** 整数除法与溢出 —— `7/2 == 3`；`int` 最大约 21 亿，乘法前先想会不会溢出（`long` 或 `Math.multiplyExact`）。
- **8.** 版本差异 —— 本课用 **Java 21（LTS）**。`record`(16+)、`instanceof` 模式匹配(16+)、`switch` 表达式(14+)、虚拟线程(21+) 都可用了；装 25 也能跑。
- **9.** 继承优先组合 —— 只有真 is-a 才继承；其余用字段组合。继承层次一变，父类改动会波及所有子类。
- **10.** 学习顺序 —— ① 能编译能跑 → ② 能读懂报错 → ③ 能把长 main 拆成方法 → ④ 能设计出 2–3 个类 → ⑤ 再上集合/泛型 → ⑥ 最后才是并发/Stream。
- **11.** 本课扣分点 —— 类名≠文件名、main 签名写错、漏分号、命名不规范、注释只写 what。
- **12.** LLM 时代的提醒 —— 课程原话：LLM 能解出所有练习题，但 EiP 考的是**概念**；LLM 常生成胡话，没有概念知识就无法判断。
- **13.** 现在不要碰 —— Spring / MySQL / Redis / Kafka / 微服务 / 23 种设计模式——那是大三大四找实习的内容（见你 D 盘那份 xmind 的后半段）。

---

## 5. 反向查：我要做 X，看哪个域

| 我要…… | 去这里 |
|---|---|
| 打印一张对齐的表 | 输入输出 + 文本（`printf` / `String.format`） |
| 读文件统计词频 | 输入输出 + 集合（`HashMap`）+ 文本（`split`/正则） |
| 建一个实体类（Book、Punkt） | 类与对象（字段/构造/getter/toString） |
| 存一堆对象并按某字段排序 | 集合（`List`）+ 算法（`Comparator`） |
| 判断两次输入是否相等 / 去重 | 文本（`equals`）+ 集合（`HashSet`） |
| 程序对非法输入崩了 | 异常（校验 + `throw`） |
| 程序太慢 | 数据结构与算法（复杂度）+ 内存·JVM（拼接/装箱） |
| 多个类共享行为 | 继承·抽象类·接口（先想清楚是不是真 is-a） |
| 把程序交给别人跑 | 工具链（`jar` / classpath / JDK 版本） |
| 作业要交 UML | 设计与建模（类图 + 关系箭头） |

---

## 6. 与本课课件/作业的对照

| 课程单元 | 覆盖的功能域 |
|---|---|
| L0 Organisatorisches | 工具链 · 备注（版本、考试） |
| L1 Algorithmus und Programm | 基础通用 · 运算（优先级） · 控制流（while） · 内存·JVM（字节码） |
| L2 Datenrepräsentation und Variable | 类型 · 运算 · 文本（编码） |
| L3 Kontrollfluss und Prozeduren | 控制流 · 方法 |
| L4 Zusammengesetzte Datentypen | 类型（数组） · 文本 · 控制流（增强 for） |
| L5 OOP I: Klassen und Objekte | 类与对象 · 设计（UML） |
| L6 OOP II: Vererbung und Interface | 继承·接口·多态 · 方法（重载/重写） |
| L7 Dynamische Datenstrukturen | 集合 · 数据结构与算法（链表/栈/树） |
| L8 Sortieralgorithmen und Komplexität | 数据结构与算法（排序/复杂度） · 内存·JVM（性能） |
| Blatt 1–2 | 类型 · 运算 · 工具链 |
| Blatt 3–4 | 控制流 · 方法 · 类型（数组） · 文本 |
| Blatt 5–6 | 类与对象 · 继承·接口 · 设计（UML） · 方法（double 比较） |

---

## 7. 怎么用这张图

1. **先看第 0 层**：这些是所有域共用的地基，卡住 90% 的初学者问题都在这一层（分号、类名、报错读法）。
2. **按需查域**：写作业时先问「我在做哪件事」，再去对应域找 API，不要从头读语法书。
3. **交叉项当复习线**：`equals`、多态、不可变这三条贯穿全图，能讲清它们，Java 就通了。
4. **备注当错题本**：每次被某个坑咬到，回来在这 13 条里找对应的一条。
5. **对照表定位进度**：老师今天讲到 L3，你就只需要点亮控制流/方法两个域，其余先当目录看。
