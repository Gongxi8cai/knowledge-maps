# 生成器（数据源）

这个目录是「知识地图」的**唯一数据源**：改这里的 Python，网页就跟着变。

## 文件

| 文件 | 作用 |
|---|---|
| `mapkit.py` | 渲染器：一份数据 → Markdown + HTML（深色卡片、左侧导航、实时搜索） |
| `tagkit.py` | 第 2 列的标签判别（关键字 / 库 / 命令行 / 写法…），按语言各一套规则 |
| `md_c.py` `md_cpp.py` `md_py.py` `md_mysql.py` `md_linux.py` `md_html.py` | 六份地图的数据 |
| `java_map.py` | Java 地图的数据 + 渲染（历史原因单独一份，产出同名文件） |
| `build_maps.py` | 跑全流程，最后生成总入口 `index.html` |

## 本地重建

```bash
python src/java_map.py     # 生成 Java知识地图.html/.md
python src/build_maps.py   # 生成其余六份 + index.html
```

Windows 上默认输出到 `D:\02_学业\知识地图\` 与 `D:\02_学业\编程四门课\01_Java\`；
想换位置就设环境变量：

```powershell
$env:MAPS_OUT = "D:\somewhere"
$env:JAVA_OUT = "D:\somewhere"
```

## 自动化

`.github/workflows/build.yml`：向 `main` 推送改动后，自动在云端跑上面两条命令，
有差异就提交一个 `auto: rebuild knowledge maps` 的 commit。
因为这类 commit 只改 `.html` / `.md`，而 workflow 的 `paths-ignore` 排除了它们，所以不会无限循环。

## 怎么改内容

| 想改什么 | 改哪个文件 |
|---|---|
| 某条功能的名字 / 说明 / 例子 | 对应语言的 `md_*.py` |
| 加一个新功能域 | `md_*.py` 的 `domains` 列表 |
| 标签判错了 | `tagkit.py` 里的 `OVERRIDES`（`(语言, 条目名): 标签`） |
| 配色、字号、表格样式 | `mapkit.py` 的 `HTML_HEAD` |
| 总入口的卡片文案 | `build_maps.py` 的 `hub()` |
