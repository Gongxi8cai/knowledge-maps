# -*- coding: utf-8 -*-
"""生成 Java 知识地图（Markdown + HTML）到 D:\\02_学业\\编程四门课\\01_Java\\"""
import html
import json
import os
import pathlib
import re

import tagkit

OUT = pathlib.Path(os.environ.get("JAVA_OUT", r"D:\02_学业\编程四门课\01_Java"))

# 状态: 必修 / 涉及 / 课外
D = []


def dom(did, name, de, goal, entries):
    D.append({"id": did, "name": name, "de": de, "goal": goal, "entries": entries})


def e(name, api, use, course, status, cross=None):
    return {"name": name, "api": api, "use": use, "course": course,
            "status": status, "cross": cross or []}


dom("io", "输入输出与交互", "Ein-/Ausgabe", "程序怎么和外界交换数据：打印、读键盘、读文件。",
    [e("控制台输出", "System.out.print / println / printf", "打印结果、临时调试", "L1 · Blatt 1", "必修", ["文本"]),
     e("控制台输入", "new Scanner(System.in)、nextInt / nextLine", "读用户输入", "Blatt 3–4", "涉及", ["方法"]),
     e("格式化输出", "String.format(\"%.2f\")、printf(\"%d %s\")", "表格对齐、保留小数位", "Blatt 4 · 6", "涉及", ["文本"]),
     e("命令行参数", "String[] args", "从外部传文件名/参数", "Blatt 6", "涉及", ["工具链"]),
     e("标准错误流", "System.err", "错误信息与正常输出分开", "—", "课外", ["异常"]),
     e("文件读写（小文件）", "Files.readString / writeString", "一次读入整个语料", "—", "课外", ["文件"]),
     e("缓冲读大文件", "BufferedReader、Files.lines", "逐行处理，不爆内存", "—", "课外", ["文件", "算法"]),
     e("统一数据源", "InputStream / Reader 抽象", "同一段代码换键盘/文件", "—", "课外", ["文件"])])

dom("types", "类型与数据表示", "Datentypen", "数据在内存里怎么表示：数字、字符、真假、序列。",
    [e("八种基本类型", "byte short int long float double char boolean", "选对类型，避免溢出和精度问题", "L2 · Blatt 1–2", "必修", ["运算"]),
     e("字面量与后缀", "1_000、10L、1.5f、'a'、'\\n'", "写常量不写错类型", "L2 · Blatt 2", "必修", ["文本"]),
     e("类型转换", "(int) 3.9、Integer.parseInt(s)", "精度丢失、字符串转数字", "L2 · Blatt 2", "必修", ["运算"]),
     e("包装类与自动装箱", "Integer、Double、Integer.valueOf", "集合里只能放对象", "L2", "涉及", ["集合"]),
     e("数组", "int[] a = new int[5]; a.length", "定长同类型序列（三角、矩阵）", "L4 · Blatt 4", "必修", ["算法"]),
     e("二维数组", "int[][] m = new int[3][4]", "矩阵、表格、棋盘", "L4", "涉及", ["算法"]),
     e("枚举 enum", "enum Farbe { ROT, GRUEN, BLAU }", "有限取值，替代魔法数字", "—", "课外", ["类"]),
     e("记录类 record", "record Punkt(double x, double y) {}", "不可变数据载体（Java 16+）", "—", "课外", ["类"]),
     e("局部类型推断", "var liste = new ArrayList<String>();", "少写重复类型（Java 10+）", "—", "课外", ["工具链"])])

dom("expr", "运算与表达式", "Ausdrücke", "怎么算：算术、比较、逻辑，以及它们怎么组合。",
    [e("算术运算", "+ - * / %", "基本计算", "L2 · Blatt 2", "必修", []),
     e("整除与取余的坑", "7/2 == 3、7%2 == 1", "整数除法不是四舍五入", "L2 · Blatt 2", "必修", ["类型"]),
     e("关系与逻辑", "== != < > && || !", "条件组合；&& 短路求值", "L2 · Blatt 2", "必修", ["控制流"]),
     e("优先级与括号", "2+3*x 是 2+(3*x)", "歧义是 bug 之源（L1 第 23 页）", "L1", "必修", ["基础"]),
     e("自增自减", "i++、++i", "循环计数；注意副作用", "L3 · Blatt 3", "必修", ["控制流"]),
     e("三元运算符", "int max = a > b ? a : b;", "两选一，替代短 if", "L3", "涉及", ["控制流"]),
     e("浮点误差", "0.1+0.2 != 0.3；Math.abs(a-b) < 1e-9", "小数比较必须给容差", "Blatt 6", "必修", ["备注"]),
     e("位运算", "& | ^ ~ << >> >>>", "掩码、底层优化、哈希", "—", "课外", ["运行时"])])

dom("flow", "控制流", "Kontrollfluss", "程序往哪走：分支、循环、提前跳出。",
    [e("if / else if / else", "if (x > 0) { … }", "分支", "L3 · Blatt 3", "必修", []),
     e("switch 与 switch 表达式", "switch (x) { case 1: … }；case -> yield", "多分支、枚举分派", "L3", "涉及", ["类型"]),
     e("for 计数循环", "for (int i = 0; i < n; i++)", "次数已知的循环", "L3 · Blatt 3", "必修", ["运算"]),
     e("增强 for", "for (int x : arr) { … }", "遍历数组/集合（只读）", "L4 · Blatt 4", "必修", ["集合"]),
     e("while / do-while", "while (b > 0) { … }", "次数未知（欧几里得算法）", "L1 · L3", "必修", ["方法"]),
     e("break / continue", "break; continue;", "提前退出、跳过一轮", "L3", "涉及", []),
     e("嵌套循环", "两层 for 打三角形（Blatt 4）", "图案、矩阵、穷举", "Blatt 4", "必修", ["算法"]),
     e("带标签跳转", "outer: for (…) { break outer; }", "跳出多层（可读性差，少用）", "—", "课外", [])])

dom("method", "方法与递归", "Prozeduren", "怎么把一件事拆成可复用的块。",
    [e("定义与调用", "static int add(int a, int b) { return a + b; }", "拆分逻辑、消除重复", "L3 · Blatt 4", "必修", []),
     e("返回值与 void", "return wert; / void", "有没有结果要交回", "L3", "必修", []),
     e("参数传递（只有值传递）", "f(x) 复制一份进去", "对象传的是引用的副本，改字段有效、换引用无效", "L3 · Blatt 6", "必修", ["基础", "类"]),
     e("方法重载", "add(int,int) 与 add(double,double)", "同名不同参（看参数选）", "L3 · Blatt 6", "必修", ["类"]),
     e("递归", "fak(n) = n * fak(n-1)", "分治、遍历树、排列组合", "L3", "涉及", ["算法"]),
     e("可变参数", "void f(String... xs)", "参数个数不定", "—", "课外", []),
     e("作用域与生命周期", "局部变量 / 字段", "变量在哪一层可见", "L3", "必修", ["基础"]),
     e("纯函数与副作用", "只依赖参数、只返回值", "好测试、好推理", "—", "课外", ["设计"])])

dom("class", "类与对象", "Klassen und Objekte", "怎么把数据和行为捆成一个实体。",
    [e("类与实例", "class Punkt { double x; } → new Punkt()", "建模现实实体", "L5 · Blatt 5", "必修", []),
     e("字段与可见性", "private / public / protected", "封装：外部只能通过方法改", "L5 · Blatt 5", "必修", ["继承"]),
     e("构造方法", "Punkt(double x, double y) { … }", "保证对象一出生就合法", "L5 · Blatt 5", "必修", []),
     e("this", "this.x = x;", "区分字段与同名参数", "L5", "必修", []),
     e("getter / setter", "getX() / setX(int x)", "受控访问，可在 setter 里校验", "L5 · Blatt 5", "必修", []),
     e("static 成员", "static int counter;", "类级共享：计数器、工具方法、main", "L5 · Blatt 6", "涉及", ["工具链"]),
     e("final", "final double PI = 3.14;", "常量、引用不可换", "L5", "涉及", ["设计"]),
     e("toString", "@Override public String toString() { … }", "打印/日志时人类可读", "Blatt 5–6", "必修", ["文本"]),
     e("equals 与 hashCode", "@Override equals(Object o)、hashCode()", "内容相等；放进 HashSet/HashMap 必须成对重写", "Blatt 6", "涉及", ["集合"]),
     e("对象组合", "class Buch { private Autor autor; }", "has-a 关系，优先于继承", "Blatt 5", "涉及", ["设计"]),
     e("内部类 / 匿名类", "new Comparator<Punkt>() { … }", "一次性小对象（Lambda 可替代）", "—", "课外", ["函数式"])])

dom("oop", "继承·抽象类·接口·多态", "Vererbung und Interface", "怎么让多个类共享行为、互相替换。",
    [e("extends 继承", "class Hund extends Tier", "is-a 复用", "L6", "必修", ["设计"]),
     e("super", "super(); super.laut();", "调父类构造/方法", "L6", "必修", []),
     e("方法重写 @Override", "同签名、换实现", "多态的基础", "L6", "必修", []),
     e("多态与动态绑定", "Tier t = new Hund(); t.laut();", "一个接口多种实现，调用处不用改", "L6", "必修", ["设计"]),
     e("抽象类 abstract", "abstract class Form { abstract double flaeche(); }", "半成品模板：有字段、有已实现方法", "L6", "必修", ["备注"]),
     e("接口 interface", "interface Zahlbar { double betrag(); }", "能力契约，一个类可多实现", "L6", "必修", ["备注"]),
     e("接口默认方法", "default void log() { … }", "给旧接口加方法不破坏实现者", "—", "课外", []),
     e("instanceof 与模式匹配", "if (t instanceof Hund h) { h.bellen(); }", "类型判断 + 自动绑定（16+）", "L6", "涉及", []),
     e("Object 根类", "toString / equals / hashCode", "所有类都继承它", "L5–L6", "必修", [])])

dom("coll", "集合与容器", "Collections", "怎么装一堆东西并高效取用。",
    [e("List / ArrayList", "new ArrayList<>()、add / get / size", "可变长序列（首选）", "L7 · Blatt 6", "必修", ["算法"]),
     e("LinkedList", "new LinkedList<>()", "频繁头尾插删", "L7", "涉及", []),
     e("Set / HashSet", "new HashSet<>()、contains", "去重、快速成员判断", "—", "课外", ["算法"]),
     e("Map / HashMap", "put / get / getOrDefault / entrySet", "键值表（词频统计）", "L7", "涉及", ["算法"]),
     e("TreeMap / TreeSet", "new TreeMap<>()", "自动按键排序，可 range 查询", "—", "课外", []),
     e("遍历方式", "for-each、Iterator、forEach", "边遍历边删要用 Iterator", "L7", "必修", []),
     e("Comparator / Comparable", "compareTo、Comparator.comparing(...)", "自定义排序规则", "L7", "涉及", ["函数式"]),
     e("Collections 工具类", "sort / reverse / max / min", "常用操作一行搞定", "L7", "涉及", []),
     e("不可变集合", "List.of(1, 2, 3)", "常量表，防被改", "—", "课外", ["设计"]),
     e("选型决策", "要顺序？要唯一？要键值？要排序？", "选错容器是性能 bug 的常见来源", "L7", "涉及", ["备注"])])

dom("gen", "泛型与类型系统", "Generics", "怎么让容器「只装某一种东西」，并且在编译期就查出来。",
    [e("泛型类 / 泛型方法", "class Box<T> { T inhalt; }", "类型安全的容器", "—", "课外", ["集合"]),
     e("类型参数", "List<String> 与 List<Integer> 不能互转", "编译期检查，省掉强制转换", "—", "课外", ["集合"]),
     e("通配符", "List<? extends Number>、? super T", "读写限制（PECS 原则）", "—", "课外", []),
     e("类型擦除", "运行时没有泛型信息", "不能 new T()、不能 instanceof List<String>", "—", "课外", ["运行时"]),
     e("泛型与数组", "new T[10] 编译不过", "用 List<T> 代替", "—", "课外", [])])

dom("exc", "异常与资源管理", "Ausnahmen", "出错时怎么办，以及怎么保证资源被释放。",
    [e("try / catch / finally", "try { … } catch (IOException e) { … } finally { … }", "捕获、兜底、必执行清理", "—", "课外", ["文件"]),
     e("throw / throws", "throw new IllegalArgumentException(\"…\");", "主动报错 / 声明可能抛", "Blatt 5–6 参数校验", "涉及", ["方法"]),
     e("受检 vs 非受检", "IOException 必须处理；NullPointerException 不必", "决定要不要写 catch", "—", "课外", ["备注"]),
     e("自定义异常", "class UngueltigeEingabe extends Exception { }", "领域错误有名字", "—", "课外", ["设计"]),
     e("try-with-resources", "try (var in = Files.newBufferedReader(p)) { … }", "自动关闭文件/流", "—", "课外", ["文件"]),
     e("读异常信息", "从最下面一行往上找、看 Caused by", "调试第一技能", "全部 Blatt", "必修", ["基础"]),
     e("断言 assert", "assert x > 0 : \"x muss positiv sein\";", "开发期自检（默认关闭）", "—", "课外", ["工具链"])])

dom("text", "文本与字符串处理", "Zeichenketten", "怎么切、查、拼、比较字符串（计算语言学的日常）。",
    [e("String 不可变", "s.toUpperCase() 返回新串", "可安全共享；循环拼接慢", "L4 · Blatt 4", "必修", ["运行时"]),
     e("常用方法", "length / charAt / substring / indexOf / split / replace / trim", "切分与查找", "L4 · Blatt 4", "必修", []),
     e("StringBuilder", "sb.append(x); sb.toString()", "循环里拼串的正确做法", "L4", "涉及", ["运行时"]),
     e("字符串比较", "equals / equalsIgnoreCase / compareTo", "内容比较，永远不用 ==", "Blatt 2 · 4", "必修", ["备注"]),
     e("格式化", "String.format(\"%.2f\", x)", "对齐表格、固定小数", "Blatt 4 · 6", "涉及", ["io"]),
     e("正则", "\"\\\\s+\".split(s)、replaceAll(\"[^A-Za-z]\", \"\")", "清洗文本（词频任务就靠它）", "—", "课外", ["算法"]),
     e("字符与编码", "char vs String、UTF-8 / UTF-16、getBytes", "德语变音符号乱码的根源", "L2 · L4", "涉及", ["文件"]),
     e("字符分类", "Character.isLetter / isDigit / toLowerCase", "判断字母数字、统一大小写", "L4", "涉及", ["类型"])])

dom("func", "函数式与 Stream", "Funktionale Programmierung", "怎么把「做什么」当参数传，少写循环。",
    [e("函数式接口", "Function / Supplier / Consumer / Predicate", "把行为当参数", "—", "课外", []),
     e("Lambda", "(a, b) -> a + b", "简短实现接口（排序最常用）", "Blatt 5–6 排序", "涉及", ["集合"]),
     e("方法引用", "String::length、System.out::println", "Lambda 的进一步简写", "—", "课外", []),
     e("Stream 管道", "list.stream().filter(…).map(…).sorted(…).toList()", "声明式处理集合", "—", "课外", ["集合"]),
     e("Optional", "Optional.ofNullable(x).orElse(0)", "显式表达「可能没有值」", "—", "课外", ["异常"]),
     e("并行 Stream", ".parallelStream()", "大数据加速（小数据更慢，慎用）", "—", "课外", ["并发"])])

dom("file", "文件与持久化", "Dateien", "怎么把数据存下来、读回来。",
    [e("Path / Files", "Path.of(\"a.txt\")、Files.readString(p)", "读写文本（显式 UTF-8）", "—", "课外", ["io"]),
     e("逐行处理", "Files.lines(p)、BufferedReader.readLine()", "大语料不爆内存", "—", "课外", ["算法"]),
     e("目录操作", "Files.list、Files.createDirectories", "批量处理、建输出目录", "—", "课外", ["工具链"]),
     e("对象序列化", "implements Serializable、ObjectOutputStream", "直接存对象（长期存储慎用）", "—", "课外", []),
     e("CSV / JSON", "手写 split 或库（Jackson）", "数据交换格式", "—", "课外", []),
     e("显式指定编码", "StandardCharsets.UTF_8", "避免平台默认编码坑", "—", "课外", ["文本"])])

dom("conc", "并发与线程", "Nebenläufigkeit", "怎么同时做多件事，以及为什么这很难。",
    [e("Thread / Runnable", "new Thread(r).start()", "并行执行", "—", "课外", []),
     e("synchronized", "synchronized void f() { … }", "互斥访问共享状态", "—", "课外", []),
     e("volatile", "volatile boolean fertig;", "保证可见性（不保证原子性）", "—", "课外", ["运行时"]),
     e("ExecutorService", "Executors.newFixedThreadPool(4)", "线程池，别手动 new 一堆", "—", "课外", []),
     e("并发集合", "ConcurrentHashMap、CopyOnWriteArrayList", "多线程共享容器", "—", "课外", ["集合"]),
     e("竞态与死锁", "先问：哪些状态是共享的？", "并发 bug 的根源", "—", "课外", ["备注"]),
     e("虚拟线程", "Thread.ofVirtual().start(r)（Java 21+）", "高并发 IO", "—", "课外", [])])

dom("rt", "内存·JVM·性能", "Laufzeit", "程序跑起来之后发生了什么。",
    [e("栈与堆", "局部变量在栈、对象在堆", "理解引用与生命周期", "—", "课外", ["类型"]),
     e("垃圾回收", "不可达对象自动回收", "不用手动 free（但不能不管内存）", "L1", "涉及", []),
     e("字节码与 .class", "javap -c HelloWorld", "看编译器到底生成了什么", "L1", "涉及", ["工具链"]),
     e("引用强度", "强 / 软 / 弱 / 虚引用", "缓存与内存敏感场景", "—", "课外", []),
     e("JVM 参数", "-Xmx512m、-Xms512m", "内存上限与初始值", "—", "课外", []),
     e("性能直觉", "先看复杂度，再看常数：拼接、装箱、IO", "先写对，再写快", "L8", "涉及", ["算法"]),
     e("内存泄漏（Java 也有）", "集合只增不删、监听器没注销", "长跑程序必查", "—", "课外", ["备注"])])

dom("tool", "工具链·测试·调试", "Werkzeuge", "怎么编译、怎么查错、怎么验证。",
    [e("javac / java", "javac -encoding UTF-8 -d build X.java；java -cp build X", "编译与运行两步", "L0 · Blatt 1", "必修", ["基础"]),
     e("包与 classpath", "package a.b;、-cp build", "类文件在哪、怎么找", "Blatt 1", "涉及", []),
     e("jar 打包", "jar --create --file x.jar -C build .", "分发可执行包", "—", "课外", []),
     e("IDE（Eclipse）", "语法高亮、自动编译、补全、向导", "提高日常效率", "L34 页", "涉及", []),
     e("构建工具", "Maven / Gradle", "依赖管理与标准目录", "—", "课外", []),
     e("单元测试 JUnit", "@Test、assertEquals", "自动验证改动没弄坏东西", "—", "课外", []),
     e("调试器", "断点、单步、看变量", "比到处 println 强", "—", "课外", []),
     e("版本管理 Git", "commit、branch、diff", "作业与项目必备", "—", "课外", []),
     e("JDK 版本", "本课用 Java 21（LTS）；--release 21", "新特性可用性、兼容性", "L0 第 11 页", "必修", ["备注"]),
     e("读报错三步", "第一行 + 行号 + 符号/标识符", "80% 的错看这三样就够", "全部", "必修", ["基础"])])

dom("algo", "数据结构与算法", "Datenstrukturen und Algorithmen", "数据怎么组织、操作要多少代价。",
    [e("数组", "随机访问 O(1)、插入删除 O(n)", "最基础的序列", "L4 · L7", "必修", []),
     e("链表", "插入删除 O(1)、查找 O(n)", "频繁增删的序列", "L7", "必修", []),
     e("栈 / 队列", "Deque、push/pop、offer/poll", "括号匹配、BFS、撤销", "L7", "涉及", []),
     e("哈希表", "HashMap 均摊 O(1)", "计数、去重、索引", "L7", "涉及", ["集合"]),
     e("树 / 二叉搜索树", "有序、查找 O(log n)", "索引、范围查询", "L7", "涉及", []),
     e("排序", "冒泡/插入/归并/快排、Arrays.sort", "排序与比较器", "L8", "必修", ["方法"]),
     e("查找", "线性查找、二分（Arrays.binarySearch）", "有序数据快速定位", "L8", "涉及", []),
     e("复杂度记号", "O(1) / O(log n) / O(n) / O(n log n) / O(n²)", "估算「输入变大十倍会怎样」", "L8", "必修", ["备注"]),
     e("递归与分治", "归并排序、二分递归", "把大问题切成同类小问题", "L8", "涉及", ["方法"])])

dom("design", "设计与建模", "Entwurf und Modellierung", "写代码之前怎么想清楚结构。",
    [e("UML 类图", "类框（字段/方法）+ 关系箭头", "先画再写，作业要交（Blatt 5）", "Blatt 5", "必修", []),
     e("封装", "private 字段 + 公开方法", "改内部实现不影响调用方", "L5", "必修", []),
     e("继承 vs 组合", "is-a 用继承；has-a 用组合", "默认选组合，继承只在真 is-a 时用", "L6", "必修", ["备注"]),
     e("单一职责", "一个类只干一件事", "可读、可测、可改", "—", "课外", []),
     e("设计模式（23 种）", "单例、工厂、观察者、策略…", "求职与大项目；现在只需知道名字", "—", "课外", ["备注"]),
     e("不可变对象", "final 字段、无 setter、防御性拷贝", "线程安全、易推理", "—", "课外", ["并发"]),
     e("接口隔离", "小而专的接口，别做胖接口", "实现方不必写空方法", "—", "课外", []),
     e("命名与可读性", "类名名词、方法动词、lowerCamelCase", "代码即文档（也是评分点）", "全部", "必修", ["基础"])])

BASE = [
    ("语句与表达式", "每条语句以分号结束；表达式有值", "`System.out.println(31-18+1);`"),
    ("变量声明与作用域", "先声明类型（或 `var`）再用；块内可见", "`int i = 0;`"),
    ("命名规范", "类 UpperCamel、方法/变量 lowerCamel、常量 UPPER_SNAKE", "`class WortZaehler`、`int maxWert`"),
    ("缩进与空白", "一般不影响语义，但影响可读性", "统一 4 空格"),
    ("注释", "`//` 行注释、`/* */` 块注释；写 why 不写 what", "`// 用 getOrDefault 避免 null`"),
    ("main 签名", "`public static void main(String[] args)` 一字不差", "JVM 只认这一个入口"),
    ("类名 = 文件名", "`public class X` 必须在 `X.java` 里", "否则编译报错"),
    ("编译 → 运行两步", "`.java` →（javac）→ `.class` →（java/JVM）→ 运行", "改了代码必须重新编译"),
    ("读编译器报错", "看第一行、行号、报错处的符号", "`';' expected` = 少了分号"),
    ("类型直觉", "8 种基本类型 + 引用类型；`int/int` 是整除", "`7/2 == 3`"),
    ("查文档", "Java API 文档、`javadoc`、IDE 里 Ctrl+点击", "别背方法名"),
    ("调试习惯", "先做最小可复现、再二分定位、别一次改五处", "—"),
]

CROSS = [
    ("String", ["类型", "文本", "集合（作键）", "文件", "输入输出"]),
    ("equals / hashCode", ["类与对象", "集合", "文本"]),
    ("值传递", ["方法", "基础通用", "类与对象"]),
    ("泛型", ["集合", "泛型", "函数式"]),
    ("try-with-resources", ["异常", "文件"]),
    ("Lambda", ["集合", "函数式", "并发"]),
    ("递归", ["方法", "数据结构与算法"]),
    ("复杂度", ["数据结构与算法", "内存·JVM·性能", "备注"]),
    ("编码 UTF-8", ["文本", "文件", "输入输出"]),
    ("多态", ["继承·接口", "设计", "集合（Comparator）"]),
    ("static", ["类与对象", "工具链（main）", "设计"]),
    ("不可变性", ["文本（String）", "设计", "并发"]),
]

NOTES = [
    ("`==` 与 `equals`", "基本类型比 `==`；对象比内容用 `equals`。`String` 用 `==` 会时对时错——这是本课最高频的错。"),
    ("determiniert 与 deterministisch", "算法两性质：同输入同结果（结果确定）≠ 步骤顺序唯一（过程确定）。随机数 +2 是前者不是后者；16/4 或 2*2 是后者不是前者。"),
    ("重载与重写", "重载（overload）= 同名不同参数，编译期选；重写（override）= 同签名换实现，运行期选。"),
    ("抽象类与接口", "抽象类可以带状态和已实现方法；接口是纯契约（可有 default 方法）。要共享代码选抽象类，要能力契约选接口。"),
    ("String 与 StringBuilder", "`String` 不可变，循环里 `+=` 是 O(n²)；循环内拼接用 `StringBuilder`。"),
    ("浮点比较", "`0.1+0.2 != 0.3`。比较小数用 `Math.abs(a-b) < 1e-9`，别用 `==`。"),
    ("整数除法与溢出", "`7/2 == 3`；`int` 最大约 21 亿，乘法前先想会不会溢出（`long` 或 `Math.multiplyExact`）。"),
    ("版本差异", "本课用 **Java 21（LTS）**。`record`(16+)、`instanceof` 模式匹配(16+)、`switch` 表达式(14+)、虚拟线程(21+) 都可用了；装 25 也能跑。"),
    ("继承优先组合", "只有真 is-a 才继承；其余用字段组合。继承层次一变，父类改动会波及所有子类。"),
    ("学习顺序", "① 能编译能跑 → ② 能读懂报错 → ③ 能把长 main 拆成方法 → ④ 能设计出 2–3 个类 → ⑤ 再上集合/泛型 → ⑥ 最后才是并发/Stream。"),
    ("本课扣分点", "类名≠文件名、main 签名写错、漏分号、命名不规范、注释只写 what。"),
    ("LLM 时代的提醒", "课程原话：LLM 能解出所有练习题，但 EiP 考的是**概念**；LLM 常生成胡话，没有概念知识就无法判断。"),
    ("现在不要碰", "Spring / MySQL / Redis / Kafka / 微服务 / 23 种设计模式——那是大三大四找实习的内容（见你 D 盘那份 xmind 的后半段）。"),
]

QUICK = [
    ("打印一张对齐的表", "输入输出 + 文本（`printf` / `String.format`）"),
    ("读文件统计词频", "输入输出 + 集合（`HashMap`）+ 文本（`split`/正则）"),
    ("建一个实体类（Book、Punkt）", "类与对象（字段/构造/getter/toString）"),
    ("存一堆对象并按某字段排序", "集合（`List`）+ 算法（`Comparator`）"),
    ("判断两次输入是否相等 / 去重", "文本（`equals`）+ 集合（`HashSet`）"),
    ("程序对非法输入崩了", "异常（校验 + `throw`）"),
    ("程序太慢", "数据结构与算法（复杂度）+ 内存·JVM（拼接/装箱）"),
    ("多个类共享行为", "继承·抽象类·接口（先想清楚是不是真 is-a）"),
    ("把程序交给别人跑", "工具链（`jar` / classpath / JDK 版本）"),
    ("作业要交 UML", "设计与建模（类图 + 关系箭头）"),
]

COURSE = [
    ("L0 Organisatorisches", ["工具链", "备注（版本、考试）"]),
    ("L1 Algorithmus und Programm", ["基础通用", "运算（优先级）", "控制流（while）", "内存·JVM（字节码）"]),
    ("L2 Datenrepräsentation und Variable", ["类型", "运算", "文本（编码）"]),
    ("L3 Kontrollfluss und Prozeduren", ["控制流", "方法"]),
    ("L4 Zusammengesetzte Datentypen", ["类型（数组）", "文本", "控制流（增强 for）"]),
    ("L5 OOP I: Klassen und Objekte", ["类与对象", "设计（UML）"]),
    ("L6 OOP II: Vererbung und Interface", ["继承·接口·多态", "方法（重载/重写）"]),
    ("L7 Dynamische Datenstrukturen", ["集合", "数据结构与算法（链表/栈/树）"]),
    ("L8 Sortieralgorithmen und Komplexität", ["数据结构与算法（排序/复杂度）", "内存·JVM（性能）"]),
    ("Blatt 1–2", ["类型", "运算", "工具链"]),
    ("Blatt 3–4", ["控制流", "方法", "类型（数组）", "文本"]),
    ("Blatt 5–6", ["类与对象", "继承·接口", "设计（UML）", "方法（double 比较）"]),
]


# ---------------------------------------------------------------- Markdown
def _c(s):
    """Markdown-Tabellenzelle: Pipes maskieren."""
    return str(s).replace("|", "\\|")


def md():
    L = []
    total = sum(len(d["entries"]) for d in D)
    L.append("# Java 知识地图 · 按功能分类\n")
    L.append("> 用途：把 Java 当成一套「工具柜」，按**你要干什么**找工具，而不是按语法书目录背。")
    L.append("> 交叉功能会在多个域里重复出现（并用「交叉」列标出它还在哪出现）；")
    L.append("> **基础通用**与**备注**各自单列在最前面/最后面。\n")
    L.append(f"统计：**{len(D)} 个功能域 · {total} 个功能条目 · {len(BASE)} 条基础通用 · {len(CROSS)} 组交叉 · {len(NOTES)} 条备注**\n")
    L.append("图例：🟩 **必修**＝本课（EiP WS26/27）讲且会考 ｜ 🟦 **涉及**＝课上提到、作业用过 ｜ ⬜ **课外**＝本课不讲，后面自学")
    L.append("课程列 `L1`＝第 1 讲（`02_EiP-01_…pdf`），`Blatt 4`＝第 4 份 Übungsblatt。\n")
    L.append("---\n")
    L.append("## 0. 两层地基 + 一张地图\n")
    L.append("```")
    L.append("第 0 层  基础通用（所有域共用）—— 语句、变量、命名、编译运行、读报错")
    L.append("第 1 层  18 个功能域（按「要做什么」分）—— 下面每节一张表")
    L.append("跨层    交叉项（同一个概念在多个域出现）+ 备注（易错点、版本、取舍）")
    L.append("```\n")
    L.append("---\n")
    L.append("## 0.5 一页提纲（先扫这个）\n")
    for i, d in enumerate(D, 1):
        names = " · ".join(en["name"] for en in d["entries"])
        L.append(f"- **{i}. {d['name']}**（{d['de']}）：{names}")
    L.append("")
    L.append("---\n")
    L.append("## 1. 基础通用（第 0 层，单列）\n")
    L.append("| 条目 | 说明 | 例子 |")
    L.append("|---|---|---|")
    for n, s, ex in BASE:
        L.append(f"| {_c(n)} | {_c(s)} | {_c(ex)} |")
    L.append("")
    L.append("---\n")
    L.append("## 2. 十八个功能域\n")
    L.append("第 2 列前面的〔〕是这一条的性质：" + " / ".join(
        f"〔{lab}〕" for _k, lab in tagkit.TAGS["java"]) +
        "——〔关键字〕是语言自带的词，〔注解〕写在类或方法上，"
        "〔标准库〕是 JDK 现成的类（查文档），〔写法〕是语法或思路，不是某个名字。\n")
    for i, d in enumerate(D, 1):
        L.append(f"### 2.{i} {d['name']}（{d['de']}）\n")
        L.append(f"**解决什么问题：**{d['goal']}\n")
        L.append("| 功能 | Java 关键字 / API | 用来做什么 | 课程 | 交叉到 |")
        L.append("|---|---|---|---|---|")
        for en in d["entries"]:
            mark = {"必修": "🟩 必修", "涉及": "🟦 涉及", "课外": "⬜ 课外"}[en["status"]]
            cross = "、".join(en["cross"]) if en["cross"] else "—"
            k = tagkit.classify("java", en["name"], en["api"])
            lab = tagkit.label("java", k)
            L.append(f"| **{_c(en['name'])}** | 〔{lab}〕`{_c(en['api'])}` | {_c(en['use'])} | {_c(en['course'])} · {mark} | {_c(cross)} |")
        L.append("")
    L.append("---\n")
    L.append("## 3. 交叉项总表（同一概念，多处出现）\n")
    L.append("| 概念 | 出现在哪些域 | 为什么交叉 |")
    L.append("|---|---|---|")
    why = {
        "String": "既是数据类型，又是文本处理对象，还常当 Map 的键、文件内容、输出单位",
        "equals / hashCode": "定义在 Object（类域），用于内容比较（文本域），HashSet/HashMap 依赖它（集合域）",
        "值传递": "语法上属方法调用，语义上决定对象能不能被「改到」，所以贯穿基础与类",
        "泛型": "集合靠它保证类型安全，函数式接口也带类型参数",
        "try-with-resources": "语法在异常域，用途是文件/流的自动关闭",
        "Lambda": "集合排序在用（Comparator），Stream 的基石，并发的任务提交也用",
        "递归": "方法的一种写法，但真正价值在分治与树/图遍历",
        "复杂度": "算法域定义，性能域测量，备注里决定「先优化哪里」",
        "编码 UTF-8": "文本域的概念，落到文件与 IO 才踩坑（德语变音符号）",
        "多态": "继承域的机制，设计域的目的，集合域里 Comparator 就是多态的应用",
        "static": "类域定义，工具链里 main 必须 static，设计上滥用会破坏可测性",
        "不可变性": "String 的天然属性，设计上的主动选择，并发里最省心的策略",
    }
    for k, v in CROSS:
        L.append(f"| **{_c(k)}** | {_c(' · '.join(v))} | {_c(why.get(k, ''))} |")
    L.append("")
    L.append("---\n")
    L.append("## 4. 备注（单列：易错点、版本、取舍、顺序）\n")
    for i, (n, s) in enumerate(NOTES, 1):
        L.append(f"- **{i}.** {n} —— {s}")
    L.append("")
    L.append("---\n")
    L.append("## 5. 反向查：我要做 X，看哪个域\n")
    L.append("| 我要…… | 去这里 |")
    L.append("|---|---|")
    for a, b in QUICK:
        L.append(f"| {_c(a)} | {_c(b)} |")
    L.append("")
    L.append("---\n")
    L.append("## 6. 与本课课件/作业的对照\n")
    L.append("| 课程单元 | 覆盖的功能域 |")
    L.append("|---|---|")
    for a, b in COURSE:
        L.append(f"| {_c(a)} | {_c(' · '.join(b))} |")
    L.append("")
    L.append("---\n")
    L.append("## 7. 怎么用这张图\n")
    L.append("1. **先看第 0 层**：这些是所有域共用的地基，卡住 90% 的初学者问题都在这一层（分号、类名、报错读法）。")
    L.append("2. **按需查域**：写作业时先问「我在做哪件事」，再去对应域找 API，不要从头读语法书。")
    L.append("3. **交叉项当复习线**：`equals`、多态、不可变这三条贯穿全图，能讲清它们，Java 就通了。")
    L.append("4. **备注当错题本**：每次被某个坑咬到，回来在这 13 条里找对应的一条。")
    L.append("5. **对照表定位进度**：老师今天讲到 L3，你就只需要点亮控制流/方法两个域，其余先当目录看。\n")
    return "\n".join(L)


# ---------------------------------------------------------------- HTML
def html_page():
    total = sum(len(d["entries"]) for d in D)
    esc = html.escape

    def h(s):
        """escape + `code` → <code> + **fett** → <b>"""
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", esc(str(s)))
        return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)

    parts = []
    parts.append("""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Java 知识地图 · 按功能分类</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0d1117;color:#c9d1d9;font:15px/1.65 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
a{color:#58a6ff;text-decoration:none}
header{padding:28px 32px 18px;border-bottom:1px solid #21262d;background:linear-gradient(180deg,#161b22,#0d1117)}
h1{margin:0 0 10px;font-size:26px;letter-spacing:.5px}
.sub{color:#8b949e;font-size:14px;max-width:900px}
.stats{margin-top:14px;display:flex;gap:10px;flex-wrap:wrap}
.stat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:6px 12px;font-size:13px;color:#8b949e}
.stat b{color:#e6edf3;font-size:15px}
.wrap{display:flex;align-items:flex-start;max-width:1500px;margin:0 auto}
nav{position:sticky;top:0;width:250px;flex:0 0 250px;max-height:100vh;overflow:auto;padding:18px 12px 60px;border-right:1px solid #21262d}
nav h2{font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#6e7681;margin:16px 8px 8px}
nav a{display:flex;justify-content:space-between;gap:8px;padding:6px 10px;border-radius:6px;color:#c9d1d9;font-size:13.5px}
nav a:hover{background:#161b22;color:#e6edf3}
nav a span{color:#6e7681;font-size:12px}
main{flex:1;min-width:0;padding:24px 32px 80px}
.search{width:100%;max-width:520px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#e6edf3;padding:9px 12px;font-size:14px;margin-bottom:22px}
.search:focus{outline:none;border-color:#1f6feb}
.sec{margin:0 0 10px;font-size:12px;text-transform:uppercase;letter-spacing:1.4px;color:#6e7681;border-bottom:1px solid #21262d;padding-bottom:8px}
.dom{margin:0 0 26px;border:1px solid #21262d;border-radius:10px;overflow:hidden;background:#0f141b}
.dom>h3{margin:0;padding:14px 16px;font-size:17px;background:#161b22;border-bottom:1px solid #21262d;display:flex;gap:12px;align-items:baseline}
.dom>h3 em{font-style:normal;font-size:12px;color:#6e7681;font-weight:400}
.goal{padding:10px 16px;color:#8b949e;font-size:13.5px;border-bottom:1px dashed #21262d}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;padding:8px 12px;color:#6e7681;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.6px;border-bottom:1px solid #21262d;background:#11161d}
td{padding:9px 12px;border-bottom:1px solid #161b22;vertical-align:top}
tr:last-child td{border-bottom:none}
tr:hover td{background:#12181f}
td.api{font-family:ui-monospace,Consolas,monospace;font-size:12.5px;color:#a5d6ff}
td.ac{display:flex;flex-wrap:wrap;gap:5px;align-items:flex-start}
td.ac .api{flex:0 1 auto;max-width:100%}
td .tag{display:inline-block;font-size:10.5px;line-height:1;padding:3px 6px;border-radius:5px;
  border:1px solid #2a3446;color:#93a2b5;background:#141b26;white-space:nowrap;margin-top:1px}
.t-kw{border-color:#3b5bdb;color:#9db4ff;background:#141d33}
.t-ann{border-color:#7048b6;color:#c9a6ff;background:#1d1630}
.t-api{border-color:#1f6f43;color:#7fe3b0;background:#0f2a1d}
.t-syn{border-color:#3a4657;color:#93a2b5;background:#161d27}
.legend{display:flex;flex-wrap:wrap;gap:16px;align-items:center;font-size:12.5px;color:#8b949e;margin-top:10px}
.legend .tag{margin-right:5px}
td.cur{white-space:nowrap;color:#8b949e;font-size:12.5px}
.badge{display:inline-block;padding:1px 7px;border-radius:20px;font-size:11.5px;margin-left:6px;border:1px solid}
.b1{color:#3fb950;border-color:#238636;background:#0f2a17}
.b2{color:#58a6ff;border-color:#1f6feb;background:#0d1d33}
.b3{color:#8b949e;border-color:#30363d;background:#161b22}
.cross{color:#d29922;font-size:12px}
.card{border:1px solid #21262d;border-radius:10px;padding:16px 18px;margin:0 0 20px;background:#0f141b}
.card h3{margin:0 0 10px;font-size:16px}
.card ul{margin:6px 0 0;padding-left:20px}
.card li{margin:7px 0}
.note b{color:#e6edf3}
code{font-family:ui-monospace,Consolas,monospace;background:#161b22;padding:1px 5px;border-radius:4px;font-size:12.5px;color:#a5d6ff}
.hint{color:#6e7681;font-size:12.5px;margin:6px 0 0}
footer{border-top:1px solid #21262d;padding:16px 32px;color:#6e7681;font-size:12.5px}
@media (max-width:900px){.wrap{flex-direction:column}nav{position:static;width:100%;flex:none;max-height:none;border-right:none;border-bottom:1px solid #21262d}main{padding:18px}}
</style></head><body>""")
    parts.append(f"""<header>
<h1>Java 知识地图 · 按功能分类</h1>
<div class="sub">按「你要干什么」找工具，而不是按语法书目录背。同一功能若跨多个域，会在多个域里重复出现，并在「交叉」列标出它还在哪出现；<b>基础通用</b>与<b>备注</b>各自单列。</div>
<div class="stats">
<div class="stat">功能域 <b>{len(D)}</b></div>
<div class="stat">功能条目 <b>{total}</b></div>
<div class="stat">基础通用 <b>{len(BASE)}</b></div>
<div class="stat">交叉概念 <b>{len(CROSS)}</b></div>
<div class="stat">备注 <b>{len(NOTES)}</b></div>
<div class="stat">课程 <b>EiP WS 26/27</b></div>
</div>
<div class="legend"><span>第 2 列的小标签表示这一条的性质：</span>
<span><span class="tag t-kw">关键字</span>语言自带的词，写代码绕不开</span>
<span><span class="tag t-ann">注解</span>写在类或方法上</span>
<span><span class="tag t-api">标准库</span>JDK 现成的类/方法，查文档</span>
<span><span class="tag t-syn">写法</span>语法或思路，不是某个名字</span>
</div></header>
<div class="wrap"><nav>
<h2>地基</h2><a href="#base">基础通用<span>{len(BASE)}</span></a>
<h2>功能域</h2>""")
    for d in D:
        parts.append(f'<a href="#{d["id"]}">{esc(d["name"])}<span>{len(d["entries"])}</span></a>')
    parts.append(f"""<h2>跨层</h2><a href="#cross">交叉项总表<span>{len(CROSS)}</span></a>
<a href="#notes">备注<span>{len(NOTES)}</span></a>
<a href="#quick">反向查</a>
<a href="#course">课件对照</a>
</nav><main>
<input class="search" id="q" placeholder="搜功能、API 或关键词……（例如 equals / 排序 / 异常）">
<div class="sec" id="base">第 0 层 · 基础通用（所有域共用）</div>
<div class="card"><table><thead><tr><th>条目</th><th>说明</th><th>例子</th></tr></thead><tbody>""")
    for n, s, ex in BASE:
        parts.append(f"<tr><td><b>{h(n)}</b></td><td>{h(s)}</td><td>{h(ex)}</td></tr>")
    parts.append("</tbody></table></div>")
    parts.append('<div class="sec" id="outline">一页提纲 · 先扫这个</div><div class="card"><ul>')
    for d in D:
        names = " · ".join(esc(en["name"]) for en in d["entries"])
        parts.append(f'<li><a href="#{d["id"]}"><b>{esc(d["name"])}</b></a>：{names}</li>')
    parts.append("</ul></div>")
    parts.append('<div class="sec">第 1 层 · 功能域</div>')
    for d in D:
        parts.append(f'<div class="dom" id="{d["id"]}"><h3>{esc(d["name"])} <em>{esc(d["de"])}</em></h3>'
                     f'<div class="goal">{esc(d["goal"])}</div>'
                     '<table><thead><tr><th>功能</th><th>Java 关键字 / API</th><th>用来做什么</th><th>课程</th><th>交叉</th></tr></thead><tbody>')
        for en in d["entries"]:
            cls = {"必修": "b1", "涉及": "b2", "课外": "b3"}[en["status"]]
            cross = "、".join(en["cross"]) if en["cross"] else "—"
            k = tagkit.classify("java", en["name"], en["api"])
            lab = tagkit.label("java", k)
            parts.append(f'<tr class="row"><td><b>{esc(en["name"])}</b></td>'
                         f'<td class="ac"><span class="tag t-{k}">{esc(lab)}</span>'
                         f'<span class="api">{esc(en["api"])}</span></td>'
                         f'<td>{h(en["use"])}</td><td class="cur">{esc(en["course"])}<span class="badge {cls}">{en["status"]}</span></td>'
                         f'<td class="cross">{esc(cross)}</td></tr>')
        parts.append("</tbody></table></div>")
    parts.append(f'<div class="sec" id="cross">跨层 A · 交叉项总表</div><div class="card"><table><thead><tr><th>概念</th><th>出现在哪些域</th><th>为什么交叉</th></tr></thead><tbody>')
    for k, v in CROSS:
        parts.append(f"<tr><td><b>{h(k)}</b></td><td>{h(' · '.join(v))}</td><td>{h(why_map.get(k, ''))}</td></tr>")
    parts.append("</tbody></table></div>")
    parts.append(f'<div class="sec" id="notes">跨层 B · 备注（易错点 / 版本 / 取舍 / 顺序）</div><div class="card">')
    for i, (n, s) in enumerate(NOTES, 1):
        parts.append(f'<div class="note" style="margin:9px 0"><b>{i}. {h(n)}</b>：{h(s)}</div>')
    parts.append("</div>")
    parts.append('<div class="sec" id="quick">反向查 · 我要做 X，看哪个域</div><div class="card"><table><thead><tr><th>我要……</th><th>去这里</th></tr></thead><tbody>')
    for a, b in QUICK:
        parts.append(f"<tr><td>{h(a)}</td><td>{h(b)}</td></tr>")
    parts.append("</tbody></table></div>")
    parts.append('<div class="sec" id="course">与本课课件 / 作业的对照</div><div class="card"><table><thead><tr><th>课程单元</th><th>覆盖的功能域</th></tr></thead><tbody>')
    for a, b in COURSE:
        parts.append(f"<tr><td><b>{h(a)}</b></td><td>{h(' · '.join(b))}</td></tr>")
    parts.append("""</tbody></table></div>
<div class="card"><h3>怎么用这张图</h3><ul>
<li><b>先看第 0 层</b>：分号、类名、报错读法——90% 的初学者问题都在这层。</li>
<li><b>按需查域</b>：写作业时先问「我在做哪件事」，再去对应域找 API。</li>
<li><b>交叉项当复习线</b>：<code>equals</code>、多态、不可变三条线贯穿全图。</li>
<li><b>备注当错题本</b>：每被某个坑咬到，回来找对应的一条。</li>
<li><b>对照表定位进度</b>：老师讲到 L3，就只点亮控制流与方法两个域。</li>
</ul></div></main></div>
<footer>生成于 2026-11-18 · 数据源：EiP WS26/27 讲义 L0–L8 + Übungsblatt 1–6 + 自写解答 · 同目录另有 <code>Java知识地图.md</code></footer>
<script>
const q = document.getElementById('q');
q.addEventListener('input', () => {
  const v = q.value.trim().toLowerCase();
  document.querySelectorAll('.dom').forEach(d => {
    let hit = 0;
    d.querySelectorAll('tr.row').forEach(r => {
      const ok = !v || r.textContent.toLowerCase().includes(v);
      r.style.display = ok ? '' : 'none';
      if (ok) hit++;
    });
    d.style.display = (!v || hit || d.querySelector('h3').textContent.toLowerCase().includes(v)) ? '' : 'none';
  });
});
</script></body></html>""")
    return "\n".join(parts)


why_map = {
    "String": "既是数据类型，又是文本处理对象，还常当 Map 的键、文件内容、输出单位",
    "equals / hashCode": "定义在 Object（类域），用于内容比较（文本域），HashSet/HashMap 依赖它（集合域）",
    "值传递": "语法上属方法调用，语义上决定对象能不能被「改到」，所以贯穿基础与类",
    "泛型": "集合靠它保证类型安全，函数式接口也带类型参数",
    "try-with-resources": "语法在异常域，用途是文件/流的自动关闭",
    "Lambda": "集合排序在用（Comparator），Stream 的基石，并发的任务提交也用",
    "递归": "方法的一种写法，但真正价值在分治与树/图遍历",
    "复杂度": "算法域定义，性能域测量，备注里决定「先优化哪里」",
    "编码 UTF-8": "文本域的概念，落到文件与 IO 才踩坑（德语变音符号）",
    "多态": "继承域的机制，设计域的目的，集合域里 Comparator 就是多态的应用",
    "static": "类域定义，工具链里 main 必须 static，设计上滥用会破坏可测性",
    "不可变性": "String 的天然属性，设计上的主动选择，并发里最省心的策略",
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "Java知识地图.md").write_text(md(), encoding="utf-8")
    (OUT / "Java知识地图.html").write_text(html_page(), encoding="utf-8")
    total = sum(len(d["entries"]) for d in D)
    print(f"md/html geschrieben: {len(D)} Domänen, {total} Einträge, "
          f"{len(BASE)} Basis, {len(CROSS)} Cross, {len(NOTES)} Notizen")
    for p in (OUT / "Java知识地图.md", OUT / "Java知识地图.html"):
        print(p, p.stat().st_size, "B")
