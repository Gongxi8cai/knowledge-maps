# Python 知识地图

> 按「你要干什么」找工具。Python 的坑不在语法而在语义：可变/不可变、默认参数的求值时机、以及「同一个对象被两个名字指着」。

**14 个功能域 · 124 个条目 · 10 条基础通用 · 7 组交叉概念 · 13 条备注**　（自学 · 第一门语言）

按「你要干什么」找工具，而不是按语法书目录背。同一个功能若跨多个域，会在多个域里重复出现，并在「交叉」列标出它还在哪出现；基础通用与备注各自单列。

## 0.5 一页提纲（先扫这个）

- **解释器与环境**：看版本与位置 · `pip` 的正确用法 · 虚拟环境 · 看装了什么 · `PYTHONPATH` · `-m` 运行模块 · 多版本共存 · REPL 与 `-i` · 重装/升级后要做什么
- **类型与变量**：基本类型 · 动态与强类型 · 不可变 vs 可变 · 类型转换 · 类型注解 · `isinstance` · 浅拷贝 vs 深拷贝 · `id` 与 `is` · f-string 里的 `=`
- **容器**：`list` · `dict` · `set` · `tuple` · 切片 · 推导式 · 排序 · 解包 · `in` 与计数 · 嵌套与共享
- **控制流**：`if / elif / else` · `for` · `range` · `while` · `break` / `continue` / `else` · `enumerate` / `zip` · `match` · `any` / `all` · 提前返回
- **函数**：定义与调用 · 默认参数的坑 · 位置与关键字 · `*args` / `**kwargs` · 作用域 LEGB · 闭包 · lambda · 装饰器 · 生成器函数
- **面向对象**：定义类 · `self` · 继承与 `super` · `property` · `dataclass` · 双下方法 · 类属性 vs 实例属性 · 组合优于继承 · `__slots__`
- **模块与包**：`import` 的三种写法 · `__name__ == "__main__"` · 包与 `__init__.py` · 模块搜索路径 · 相对导入 · 标准库地图 · 第三方包 · `dir()` 与 `help()`
- **异常处理**：`try / except` · `else` / `finally` · `raise` · 自定义异常 · 异常层次 · EAFP 风格 · 别吞异常 · `assert` · `raise ... from`
- **文件与路径**：读文件 · 逐行读大文件 · 写文件 · `pathlib` · `csv` · `json` · 编码问题 · 临时文件 · 二进制
- **文本与正则**：常用方法 · f-string · 切片与判断 · 正则基础 · 命名分组 · 贪婪 vs 非贪婪 · 规范化 · 编码转换 · 德语/中文排序
- **迭代器与生成器**：可迭代 vs 迭代器 · `yield` · 生成器表达式 · `itertools` · 能省多少内存 · 只能用一次 · `zip` 的惰性版 · 管道式写法
- **常用标准库**：`collections` · `datetime` · `random` · `argparse` · `logging` · `subprocess` · `math` / `statistics` · `os` / `sys` · `functools`
- **数据与科学计算**：`numpy` · 广播 · `pandas` · `matplotlib` · Jupyter · 三者分工 · 安装 · 中文字体
- **调试与测试**：`print` 的替代 · `breakpoint()` · pdb 命令 · `pytest` · `-x` / `--pdb` · `logging` · 计时 · 常见坑清单 · 类型检查

## 1. 基础通用（第 0 层，单列）

| 条目 | 说明 | 例子 |
|---|---|---|
| 解释执行 | `python script.py` 直接跑，没有编译步骤 | 改完立刻能跑，适合试错 |
| 缩进就是语法 | 同一块用同样的缩进（4 空格），别混 Tab | `IndentationError` 的头号来源 |
| 动态类型 | 变量只是名字，值有类型 | `x = 1` 之后 `x = 「a」` 也合法 |
| 一切皆对象 | 函数、类、模块都是对象，可以传来传去 | `f = print` 合法 |
| None 表示「没有值」 | 判断用 `is None`，不要用 `== None` | `if x is None:` |
| 真值规则 | 空容器、0、空字符串、None 都是假 | `if not items:` |
| 解释器位置很重要 | `python -V` 与 `python -m pip -V` 必须指同一个 Python | 装包装错地方 = 白装 |
| 虚拟环境隔离依赖 | 每个项目一个 `venv`，别往全局装 | `python -m venv .venv` |
| 报错从下往上读 | 最后一行是异常类型和信息，上面是调用栈 | `KeyError: 'name'` |
| `help()` / `dir()` | 交互式查对象有什么方法 | `help(str.split)` |

## 2. 功能域（第 1 层）

第 2 列前面的〔〕是这一条的性质：〔关键字〕 / 〔内置〕 / 〔模块〕 / 〔命令行〕 / 〔写法〕——〔关键字〕要自己写，其余是现成的名字（查文档 / 查手册就行）。

### 2.1 解释器与环境　<sub>Umgebung</sub>

先搞清楚「哪个 python 在跑、包装到哪了」——这比学语法更早出问题。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 看版本与位置 | 〔命令行〕`python -V`、`python -c "import sys; print(sys.executable)"` | 确认命令行里的 python 是哪一个 | 入门 | 模块 |
| `pip` 的正确用法 | 〔模块〕`python -m pip install 包名` | 别直接敲 `pip`——它可能是另一个 Python 的 | 入门 | — |
| 虚拟环境 | 〔命令行〕`python -m venv .venv` → `.venv\Scripts\activate` | 项目隔离依赖；激活后 `python`/`pip` 都指向它 | 入门 | — |
| 看装了什么 | 〔命令行〕`python -m pip list`、`pip show 包名` | 包在哪个 site-packages 一目了然 | 常用 | — |
| `PYTHONPATH` | 〔写法〕环境变量，追加模块搜索路径 | 临时调试用；长期靠包安装 | 进阶 | 模块 |
| `-m` 运行模块 | 〔命令行〕`python -m http.server`、`python -m pytest` | 用模块方式跑，路径语义更干净 | 常用 | 模块 |
| 多版本共存 | 〔命令行〕`py -0p` 列出所有解释器、`py -3.15` 指定 | Windows 上的 Python Launcher | 常用 | — |
| REPL 与 `-i` | 〔命令行〕`python -i script.py` 跑完留在交互里 | 调试小片段最快的方式 | 常用 | 调试与测试 |
| 重装/升级后要做什么 | 〔写法〕重装 Python 后重跑关联脚本与 venv | venv 里记的是旧路径，会失效 | 进阶 | — |

### 2.2 类型与变量　<sub>Typen</sub>

名字只是标签；值分可变与不可变，这一条决定了后面八成的坑。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 基本类型 | 〔内置〕`int` `float` `str` `bool` `NoneType` | `int` 任意精度，不会溢出 | 入门 | — |
| 动态与强类型 | 〔写法〕`x = 1` 后 `x = 「a」` 合法；但 `1 + 「a」` 报错 | 名字无类型，值有类型 | 入门 | — |
| 不可变 vs 可变 | 〔写法〕`int/str/tuple/frozenset` 不可变；`list/dict/set` 可变 | 不可变可作 dict 的键；可变要小心共享 | 常用 | 容器 |
| 类型转换 | 〔内置〕`int("42")`、`str(3.5)`、`float("1e3")` | 转换失败抛 `ValueError` | 入门 | 异常 |
| 类型注解 | 〔关键字〕`def f(x: int) -> str:` | 只是提示，运行时不检查；配合 mypy 才有用 | 进阶 | 函数 |
| `isinstance` | 〔内置〕`isinstance(x, (int, float))` | 比 `type(x) == int` 更能照顾继承 | 常用 | 面向对象 |
| 浅拷贝 vs 深拷贝 | 〔模块〕`copy.copy` / `copy.deepcopy` | 嵌套结构改内层要深拷贝 | 进阶 | 容器 |
| `id` 与 `is` | 〔内置〕`a is b` 比较是不是同一个对象 | 小整数与短字符串会被缓存，别拿 `is` 比内容 | 进阶 | — |
| f-string 里的 `=` | 〔写法〕`f"{x=}"` 打印 `x=1` | 调试时最省事的写法 | 常用 | 文本 |

### 2.3 容器　<sub>Container</sub>

`list` 有序可改、`dict` 查得快、`set` 去重、`tuple` 不可变——先选对容器。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `list` | 〔内置〕`a = [1, 2, 3]`；`append` `pop` `insert` `remove` | 有序、可重复、随机访问 O(1) | 入门 | — |
| `dict` | 〔内置〕`d = {"a": 1}`；`d.get(k, 默认)` | 键值映射，查找平均 O(1) | 入门 | — |
| `set` | 〔内置〕`s = {1, 2}`；`\| & -` | 去重与集合运算；元素必须可哈希 | 常用 | — |
| `tuple` | 〔内置〕`t = (1, 2)`；能当 dict 的键 | 不可变，适合固定结构（坐标、返回值） | 常用 | 类型与变量 |
| 切片 | 〔写法〕`a[1:3]`、`a[::-1]`、`a[::2]` | 返回新对象；切片赋值可替换一段 | 常用 | — |
| 推导式 | 〔写法〕`[x*x for x in a if x > 0]` | 列表/字典/集合推导，比 for+append 快且短 | 常用 | 迭代器与生成器 |
| 排序 | 〔内置〕`sorted(a)`、`a.sort(key=lambda x: -x)` | `sorted` 返回新列表；同值稳定排序 | 常用 | 函数 |
| 解包 | 〔写法〕`a, b = b, a`；`first, *rest = a` | 交换变量、取剩余项 | 常用 | — |
| `in` 与计数 | 〔关键字〕`x in a`、`a.count(x)` | list 的 `in` 是 O(n)，set/dict 是 O(1) | 入门 | — |
| 嵌套与共享 | 〔写法〕`[[0]*3]*3` 三个内层是同一个列表 | 要用 `[[0]*3 for _ in range(3)]` | 进阶 | 类型与变量 |

### 2.4 控制流　<sub>Kontrollfluss</sub>

分支与循环；Python 用缩进划块，`for` 是「遍历可迭代对象」。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `if / elif / else` | 〔关键字〕`if x > 0: … elif x == 0: … else: …` | 条件不用括号，冒号不能少 | 入门 | — |
| `for` | 〔关键字〕`for x in 可迭代对象:` | 遍历容器、字符串、文件、range | 入门 | 迭代器与生成器 |
| `range` | 〔内置〕`range(n)`、`range(1, n+1)`、`range(n-1, -1, -1)` | 左闭右开；不会真的生成整个列表（3.x） | 入门 | — |
| `while` | 〔关键字〕`while cond:` | 条件先判；要自己保证会结束 | 入门 | — |
| `break` / `continue` / `else` | 〔关键字〕`for … else: …`（没 break 才执行） | `else` 是「循环正常结束」的分支 | 进阶 | — |
| `enumerate` / `zip` | 〔内置〕`for i, x in enumerate(a)`；`for a1, b1 in zip(A, B)` | 要下标用 enumerate，别用 `range(len(a))` | 常用 | 容器 |
| `match` | 〔关键字〕`match cmd: case "go": …` | 3.10+ 的结构化模式匹配，比一长串 elif 清楚 | 进阶 | — |
| `any` / `all` | 〔内置〕`any(x > 0 for x in a)` | 把循环写成表达式，短路求值 | 常用 | 迭代器与生成器 |
| 提前返回 | 〔关键字〕`if not ok: return None` | 减少嵌套 | 常用 | 函数 |

### 2.5 函数　<sub>Funktionen</sub>

函数是对象；参数有四种玩法，默认参数只在定义时求值一次。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 定义与调用 | 〔关键字〕`def f(a, b=2): return a + b` | 返回值用 `return`，没有就是 `None` | 入门 | — |
| 默认参数的坑 | 〔关键字〕`def f(a, buf=[])` 会跨调用共享同一个列表 | 用 `None` 当默认值，函数里再建容器 | 常用 | 类型与变量 |
| 位置与关键字 | 〔写法〕`f(1, b=2)` | 关键字参数让调用更可读 | 入门 | — |
| `*args` / `**kwargs` | 〔关键字〕`def f(*args, **kwargs)` | 接收任意数量位置/关键字参数 | 常用 | 解包 |
| 作用域 LEGB | 〔写法〕Local → Enclosing → Global → Builtin | 函数里赋值会创建局部变量；改全局要 `global` | 进阶 | — |
| 闭包 | 〔写法〕内层函数记住外层的变量 | 配合 `nonlocal` 修改外层变量 | 进阶 | — |
| lambda | 〔关键字〕`key=lambda x: x[1]` | 只能写一个表达式，适合当参数 | 常用 | 容器 |
| 装饰器 | 〔模块〕`@functools.wraps` + `def deco(f)` | 不改函数体就加行为（计时、缓存、权限） | 进阶 | 模块 |
| 生成器函数 | 〔关键字〕`def gen(): yield 1` | 一次产一个值，省内存 | 进阶 | 迭代器与生成器 |

### 2.6 面向对象　<sub>Objekte</sub>

类把数据和行为捆在一起；`self`、继承、`property`、`dataclass` 是常用四件套。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 定义类 | 〔关键字〕`class Buch: def __init__(self, t): self.titel = t` | `__init__` 初始化实例 | 入门 | — |
| `self` | 〔写法〕第一个参数，指实例本身 | 调用时不用传；忘了写就变普通函数 | 入门 | — |
| 继承与 `super` | 〔关键字〕`class Roman(Buch): def __init__(...): super().__init__(...)` | 多继承按 MRO 找方法 | 常用 | — |
| `property` | 〔内置〕`@property` + `@x.setter` | 把方法当属性用，能加校验 | 进阶 | — |
| `dataclass` | 〔写法〕`@dataclass class Punkt: x: float; y: float` | 自动生成 `__init__`/`__repr__`/`__eq__` | 常用 | 类型与变量 |
| 双下方法 | 〔写法〕`__str__` `__len__` `__eq__` `__lt__` | 让你的对象能用 `print`、`len`、`==`、排序 | 进阶 | 容器 |
| 类属性 vs 实例属性 | 〔写法〕类里直接写的变量是共享的 | 可变类属性被所有实例共享——经典坑 | 进阶 | — |
| 组合优于继承 | 〔写法〕`self.motor = Motor()` | has-a 用成员，is-a 才继承 | 常用 | — |
| `__slots__` | 〔写法〕`__slots__ = ("x", "y")` | 省内存、防手滑加属性 | 进阶+ | — |

### 2.7 模块与包　<sub>Module</sub>

一个 `.py` 就是模块，一个目录（带 `__init__.py`）就是包；导入路径是新手第二大坑。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `import` 的三种写法 | 〔关键字〕`import os`、`from os import path`、`import numpy as np` | 优先整模块导入，避免名字冲突 | 入门 | — |
| `__name__ == "__main__"` | 〔关键字〕`if __name__ == "__main__": main()` | 既能被导入又能直接跑 | 常用 | — |
| 包与 `__init__.py` | 〔命令行〕目录 + `__init__.py` 就是一个包 | 3.3+ 有命名空间包，但显式写更清楚 | 常用 | — |
| 模块搜索路径 | 〔模块〕`sys.path`：当前目录 → 标准库 → site-packages | `ModuleNotFoundError` 先看这里 | 进阶 | 环境 |
| 相对导入 | 〔关键字〕`from . import util` | 只在包内部可用；脚本直接跑会失败 | 进阶 | — |
| 标准库地图 | 〔写法〕`os/sys/pathlib/json/csv/re/datetime/collections/itertools` | 九成需求不用装第三方 | 常用 | 常用标准库 |
| 第三方包 | 〔命令行〕`python -m pip install requests` | 装到当前解释器的 site-packages | 入门 | 环境 |
| `dir()` 与 `help()` | 〔内置〕`dir(mod)` 看有什么，`help(mod.f)` 看文档 | 比搜网页快 | 常用 | — |

### 2.8 异常处理　<sub>Ausnahmen</sub>

出错就抛异常；捕获要具体，别用裸 `except` 把 bug 吞掉。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `try / except` | 〔关键字〕`try: … except ValueError as e: …` | 按异常类型捕获，越具体越好 | 入门 | — |
| `else` / `finally` | 〔关键字〕`else` 没异常时跑、`finally` 一定跑 | `finally` 用来收尾（关文件、删临时） | 常用 | 文件 |
| `raise` | 〔关键字〕`raise ValueError("bad input")` | 主动报错；`raise X from e` 保留原因 | 常用 | — |
| 自定义异常 | 〔关键字〕`class ParseError(Exception): pass` | 给调用方一个可捕获的类型 | 进阶 | 面向对象 |
| 异常层次 | 〔内置〕`Exception` 是所有常规异常的基类 | 别继承 `BaseException` | 进阶 | — |
| EAFP 风格 | 〔写法〕先做、错了再处理（`try: d[k]`） | 比 `if k in d` 更 Pythonic | 进阶 | 容器 |
| 别吞异常 | 〔关键字〕`except Exception: pass` 会藏住真 bug | 至少要 `logging.exception(...)` 记下来 | 常用 | 调试与测试 |
| `assert` | 〔关键字〕`assert x > 0, "x 必须为正"` | 只在调试生效（`-O` 会关掉），别用它校验用户输入 | 常用 | 调试与测试 |
| `raise ... from` | 〔关键字〕把底层异常链上去 | 报错时能看到因果链 | 进阶 | — |

### 2.9 文件与路径　<sub>Dateien</sub>

`with open(...)` 是标准姿势；路径操作交给 `pathlib`，别手拼字符串。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 读文件 | 〔关键字〕`with open(p, encoding="utf-8") as f: text = f.read()` | `with` 保证关闭；一定要写 `encoding` | 入门 | — |
| 逐行读大文件 | 〔关键字〕`for line in f:` | 不会一次读进内存 | 常用 | 迭代器与生成器 |
| 写文件 | 〔内置〕`open(p, "w")` 覆盖、`"a"` 追加 | 写入前想清楚要不要保留原内容 | 入门 | — |
| `pathlib` | 〔模块〕`Path("d") / "a.txt"`、`.exists()`、`.glob("*.pdf")` | 跨平台路径拼接的首选 | 常用 | — |
| `csv` | 〔模块〕`csv.reader` / `csv.DictReader` | 别用 `split(",")`——引号与换行会坑你 | 常用 | 文本 |
| `json` | 〔模块〕`json.load(f)` / `json.dump(obj, f, ensure_ascii=False)` | 中文要 `ensure_ascii=False` | 常用 | — |
| 编码问题 | 〔写法〕`UnicodeDecodeError: 'gbk' codec can't decode` | 读文件显式 `encoding="utf-8"`；Windows 默认是 gbk | 常用 | 文本 |
| 临时文件 | 〔模块〕`tempfile.NamedTemporaryFile`、`Path.tempdir` | 别往当前目录乱扔中间文件 | 进阶 | — |
| 二进制 | 〔内置〕`open(p, "rb")`、`struct` 解包 | 图片、压缩包、协议数据 | 进阶 | — |

### 2.10 文本与正则　<sub>Text</sub>

字符串方法解决八成问题，剩下两成交给 `re`；编码是绕不开的一课。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 常用方法 | 〔写法〕`split` `join` `strip` `replace` `startswith` `find` | `"-".join(parts)` 是拼接的标准写法 | 入门 | — |
| f-string | 〔写法〕`f"{name}: {wert:.2f}"` | 格式化首选；`:.2f` 两位小数、`:,` 千分位 | 入门 | — |
| 切片与判断 | 〔写法〕`s[:3]`、`s.isdigit()`、`s.upper()` | 字符串不可变，方法都返回新串 | 入门 | 类型与变量 |
| 正则基础 | 〔模块〕`re.search(r"\d+", s)`、`re.findall`、`re.sub` | 用原始字符串 `r"..."`，避免反斜杠二次转义 | 常用 | — |
| 命名分组 | 〔写法〕`(?P<name>\w+)` + `m.group("name")` | 比数字下标可读 | 进阶 | — |
| 贪婪 vs 非贪婪 | 〔写法〕`.*` 贪婪、`.*?` 非贪婪 | 截取标签内容时最容易踩 | 进阶 | — |
| 规范化 | 〔模块〕`unicodedata.normalize("NFC", s)` | 德语变音符号、组合字符比较前先归一 | 进阶+ | — |
| 编码转换 | 〔写法〕`s.encode("utf-8")`、`b.decode("utf-8", errors="replace")` | 文件/网络边界上最容易出问题 | 进阶 | 文件与路径 |
| 德语/中文排序 | 〔内置〕`sorted(words, key=str.lower)` | 默认按码点排，大小写会乱 | 常用 | 容器 |

### 2.11 迭代器与生成器　<sub>Iteratoren</sub>

惰性求值是 Python 处理大数据的核心技巧：一次只算一个。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 可迭代 vs 迭代器 | 〔内置〕`iter(x)` 得到迭代器，`next(it)` 取下一个 | `for` 就是这套协议的语法糖 | 进阶 | 控制流 |
| `yield` | 〔关键字〕`def gen(): for i in range(3): yield i` | 函数变成生成器，调用时不执行、取时才执行 | 进阶 | 函数 |
| 生成器表达式 | 〔内置〕`sum(x*x for x in a)` | 括号版推导式，不建中间列表 | 常用 | 容器 |
| `itertools` | 〔模块〕`chain` `islice` `groupby` `product` `count` | 组合、切片、笛卡尔积的现成工具 | 进阶 | 常用标准库 |
| 能省多少内存 | 〔写法〕1000 万行文件用生成器只占常数内存 | 读日志、跑管道时尤其重要 | 常用 | 文件与路径 |
| 只能用一次 | 〔写法〕生成器耗尽就空了 | 要复用就存成 list 或重新创建 | 进阶 | — |
| `zip` 的惰性版 | 〔内置〕`itertools.zip_longest` | 长度不等时不丢数据 | 进阶+ | — |
| 管道式写法 | 〔写法〕`(f(x) for x in gen if pred(x))` | 把处理串成流水线，可读且省内存 | 进阶 | 函数 |

### 2.12 常用标准库　<sub>Standardbibliothek</sub>

这些「不用装就能用」的模块覆盖了日常八成任务。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `collections` | 〔模块〕`Counter` `defaultdict` `deque` `namedtuple` | 计数、带默认值的字典、双端队列 | 常用 | 容器 |
| `datetime` | 〔模块〕`datetime.now()`、`timedelta(days=7)`、`strftime` | 日期计算与格式化；时区要显式 | 常用 | — |
| `random` | 〔模块〕`random.random()`、`randint`、`choice`、`shuffle` | 要可复现就 `random.seed(42)` | 入门 | — |
| `argparse` | 〔模块〕`parser.add_argument("--n", type=int)` | 写命令行工具的标准姿势 | 常用 | — |
| `logging` | 〔模块〕`logging.basicConfig(level=logging.INFO)` | 比 `print` 更适合长期运行的程序 | 常用 | 调试与测试 |
| `subprocess` | 〔模块〕`subprocess.run(["ls"], capture_output=True, text=True)` | 调外部命令；别用 `os.system` | 进阶 | — |
| `math` / `statistics` | 〔模块〕`math.sqrt`、`statistics.mean/median/stdev` | 基础统计量不用装 numpy | 常用 | 数据与科学计算 |
| `os` / `sys` | 〔模块〕`os.environ`、`sys.argv`、`sys.exit(1)` | 环境变量、命令行参数、退出码 | 常用 | 环境 |
| `functools` | 〔模块〕`lru_cache`、`partial`、`wraps` | 缓存与函数包装 | 进阶 | 函数 |

### 2.13 数据与科学计算　<sub>Daten</sub>

numpy 管数组、pandas 管表格、matplotlib 画图；课程作业基本就这三件。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `numpy` | 〔命令行〕`np.array([1,2,3])`、`a.mean()`、`a[a > 0]` | 向量化运算比 for 快几十倍 | 常用 | — |
| 广播 | 〔写法〕`a + b` 形状不同也能算（按规则扩展） | 写不出循环时的救星，也是报错来源 | 进阶 | — |
| `pandas` | 〔模块〕`pd.read_csv`、`df.groupby(...).agg(...)` | 表格的筛选、分组、连接、透视 | 常用 | — |
| `matplotlib` | 〔模块〕`plt.plot(x, y)`、`plt.savefig("a.png", dpi=150)` | `savefig` 要在 `show` 之前 | 常用 | — |
| Jupyter | 〔命令行〕`.ipynb` 单元格执行、`%timeit`、`!pip` | 边看结果边写，适合探索 | 常用 | 调试与测试 |
| 三者分工 | 〔写法〕numpy 数值、pandas 表格、matplotlib 图形 | 别用 pandas 干 numpy 的活（慢） | 入门 | — |
| 安装 | 〔命令行〕`python -m pip install numpy pandas matplotlib` | 装到当前解释器；venv 里更干净 | 入门 | 环境 |
| 中文字体 | 〔模块〕`plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]` | 图上中文变方块时加这行 | 进阶 | — |

### 2.14 调试与测试　<sub>Debugging</sub>

先能看见发生了什么，再谈修：断点、日志、测试，三层手段。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `print` 的替代 | 〔内置〕`print(repr(x))`、`pprint.pprint`、f-string 的 `{x=}` | `repr` 能看清引号与 `None` | 入门 | — |
| `breakpoint()` | 〔写法〕代码里插一行，运行到这里进 `pdb` | 3.7+ 内置，不用记 `import pdb` | 常用 | — |
| pdb 命令 | 〔写法〕`n` 下一步、`s` 进入、`c` 继续、`p x` 打印、`l` 看上下文 | `q` 退出 | 常用 | — |
| `pytest` | 〔命令行〕`def test_add(): assert add(1,2) == 3`；`python -m pytest -q` | 函数名以 `test_` 开头就自动被发现 | 常用 | — |
| `-x` / `--pdb` | 〔写法〕第一个失败就停 / 失败直接进调试器 | 定位问题更快 | 进阶 | — |
| `logging` | 〔模块〕`logging.exception("msg")` 打印异常+栈 | 比 `print` 可控（级别、文件、时间戳） | 常用 | 常用标准库 |
| 计时 | 〔模块〕`time.perf_counter()`、`%timeit`、`python -m timeit` | 先量再优化 | 常用 | — |
| 常见坑清单 | 〔写法〕可变默认参数、浅拷贝、`==` vs `is`、闭包延迟绑定 | 这四条能解释大部分「为什么和我预期不一样」 | 进阶 | 函数 |
| 类型检查 | 〔命令行〕`mypy script.py` | 注解写了就跑一遍，能提前抓一堆拼写错误 | 进阶 | 类型与变量 |

## 3. 交叉项总表（同一概念出现在多个域）

| 概念 | 出现在 | 为什么重复出现 |
|---|---|---|
| 可变 vs 不可变 | 类型与变量「不可变 vs 可变」 · 容器「嵌套与共享」 · 函数「默认参数的坑」 · 面向对象「类属性 vs 实例属性」 | 「两个名字指同一个可变对象」是 Python 最深的坑，四个域各有一个典型现场 |
| 名字与对象 | 类型与变量「`id` 与 `is`」 · 函数「作用域 LEGB」 · 面向对象「`self`」 | Python 的变量是标签不是盒子；理解这一点，传参、闭包、`is` 全都通了 |
| 惰性求值 | 迭代器与生成器「生成器表达式」 · 文件与路径「逐行读大文件」 · 控制流「`any` / `all`」 · 容器「推导式」 | 都是「不要一次算完」：省内存、能短路、能处理无限序列 |
| 编码 | 文件与路径「编码问题」 · 文本与正则「编码转换」 · 文本与正则「规范化」 | 读文件 → 处理字符串 → 输出，每个环节都可能因为编码报错；显式 `encoding="utf-8"` 能挡掉大半 |
| 环境与导入 | 环境「看版本与位置」 · 模块「模块搜索路径」 · 环境「虚拟环境」 | `ModuleNotFoundError` 九成不是「没装」，而是「装到另一个 Python 里了」 |
| 函数是一等对象 | 函数「闭包」 · 函数「装饰器」 · 常用标准库「`functools`」 · 容器「排序」 | 能传能存能返回，才有 lambda 当 key、装饰器、回调这些写法 |
| 异常与错误处理 | 异常处理「别吞异常」 · 调试与测试「`logging`」 · 文件与路径「`with open`」 | `with` 保证释放、`logging.exception` 保留现场、`except` 别吞——三件事凑成一个可靠程序 |

## 4. 备注（易错点 / 取舍 / 顺序）

1. **默认参数只在定义时求值一次**：`def f(a, buf=[])` 的 `buf` 是所有调用共享的同一个列表；用 `buf=None`。
2. **`==` 比内容，`is` 比身份**：只有和 `None`/`True`/`False` 比较时才用 `is`。
3. **`[[0]*3]*3` 不是二维数组**：三个内层是同一个列表；要 `[[0]*3 for _ in range(3)]`。
4. **`list.sort()` 返回 None**：它就地排序；要新列表用 `sorted()`。
5. **遍历时别改列表**：用 `for x in a[:]` 或新建列表；否则会跳过元素。
6. **`except:` 会连 Ctrl+C 一起吞**：至少写 `except Exception:`，最好指明类型。
7. **读文件一定写 `encoding="utf-8"`**：Windows 默认 gbk，德语变音符号与 emoji 会炸。
8. **`import` 只在第一次执行**：模块级代码会被缓存；要刷新用 `importlib.reload`（调试才用）。
9. **浮点不要 `==`**：`abs(a-b) < 1e-9`；要精确小数用 `decimal`。
10. **字符串拼接别用 `+=` 循环**：O(n²)；用 `"".join(parts)`。
11. **学 Python 的顺序**：①容器与循环 ②函数与参数 ③文件与异常 ④类 ⑤模块与 venv ⑥生成器与装饰器。
12. **Python 不是「慢」，是「你写慢了」**：热点用 numpy / 内置函数 / 生成器，别急着上 C 扩展。
13. **先确认 `python` 跑的是哪一个**：`where python` 列出全部候选；装包用 `python -m pip` 而不是裸 `pip`，否则可能装到另一个解释器上。

## 5. 反向查：我要做 X，去哪个域

| 我要…… | 去这里 |
|---|---|
| 读一个 CSV 并统计 | 文件与路径（`csv`）+ 容器（`Counter`） |
| 把一堆字典按某字段排序 | 容器（`sorted(key=...)`）+ 函数（lambda） |
| 处理很大的文件而不爆内存 | 文件与路径（逐行读）+ 迭代器与生成器 |
| 命令行工具带参数 | 常用标准库（`argparse`） |
| 抓一段文本里的数字 | 文本与正则（`re.findall`） |
| 装了个包但 import 不到 | 环境（`python -m pip`）+ 模块（`sys.path`） |
| 程序报 `UnicodeDecodeError` | 文件与路径（`encoding="utf-8"`） |
| 画个折线图存成 PNG | 数据与科学计算（matplotlib `savefig`） |
| 给函数加缓存/计时 | 函数（装饰器）+ 常用标准库（`functools`） |
| 写自动化测试 | 调试与测试（pytest） |

---

*由 `mapkit.py` 生成（单一数据源，Markdown 与 HTML 内容一致）。共 124 条。*
