# -*- coding: utf-8 -*-
"""给知识地图的「关键字 / API」列打标记：这一条到底是语言规定的词、现成能借的东西，还是写法骨架。

用法：
    import tagkit
    tagkit.classify("java", "System.out.println")   -> "api"
    tagkit.label("java", "api")                     -> "标准库"
"""
import re

# ── 每种语言自己的分类（顺序即图例顺序）────────────────────────────────
TAGS = {
    "java": [("kw", "关键字"), ("ann", "注解"), ("api", "标准库"), ("syn", "写法")],
    "c": [("kw", "关键字"), ("lib", "C 库"), ("cli", "命令行"), ("syn", "写法")],
    "cpp": [("kw", "关键字"), ("stl", "STL/库"), ("cli", "命令行"), ("syn", "写法")],
    "py": [("kw", "关键字"), ("bi", "内置"), ("mod", "模块"), ("cli", "命令行"), ("syn", "写法")],
    "mysql": [("kw", "SQL 关键字"), ("fn", "函数"), ("cli", "命令"), ("syn", "写法")],
    "linux": [("cmd", "命令"), ("opt", "选项/语法"), ("cfg", "配置/路径")],
    "html": [("tag", "标签"), ("attr", "属性"), ("syn", "写法")],
}

# ── 关键字表 ──────────────────────────────────────────────────────
JAVA_KW = set("""abstract assert boolean break byte case catch char class const continue
default do double else enum extends final finally float for goto if implements import
instanceof int interface long native new package private protected public record return
sealed short static strictfp super switch synchronized this throw throws transient try
var void volatile while yield permits""".split())
JAVA_LITERALS = {"true", "false", "null"}

C_KW = set("""auto break case char const continue default do double else enum extern float
for goto if inline int long register restrict return short signed sizeof static struct
switch typedef union unsigned void volatile while _Bool _Complex _Imaginary _Alignas
_Alignof _Atomic _Generic _Noreturn _Static_assert _Thread_local""".split())

CPP_KW = C_KW | set("""alignas alignof and and_eq asm bitand bitor bool catch char8_t char16_t
char32_t class compl concept consteval constexpr constinit const_cast co_await co_return
co_yield decltype delete dynamic_cast explicit export false friend mutable namespace
new noexcept not not_eq nullptr operator or or_eq private protected public
reinterpret_cast requires static_assert static_cast template this thread_local throw true
try typeid typename using virtual wchar_t xor xor_eq override final""".split())

PY_KW = set("""False None True and as assert async await break class continue def del elif
else except finally for from global if import in is lambda nonlocal not or pass raise
return try while with yield match case""".split())
PY_BUILTIN = set("""print len range sorted sum min max abs round open input int float str bool
list dict set tuple type isinstance issubclass enumerate zip map filter reversed any all
repr hash id dir vars getattr setattr hasattr iter next sorted format chr ord divmod pow
hex bin oct id callable super property staticmethod classmethod object Exception
ValueError TypeError KeyError IndexError FileNotFoundError ZeroDivisionError""".split())
PY_MODULE = set("""os os.path sys pathlib re csv json math random collections itertools
functools datetime time argparse subprocess shutil glob io string textwrap unicodedata
sqlite3 urllib statistics decimal fractions logging threading asyncio venv pip
dataclasses typing enum hashlib base64 zipfile tarfile tempfile unittest""".split())
PY_MODULE_PREFIX = ("sqlite3.", "urllib.", "os.", "re.", "json.", "csv.", "pathlib.",
                    "itertools.", "functools.", "collections.", "datetime.", "math.",
                    "random.", "subprocess.", "shutil.", "glob.")

JAVA_JDK = set("""String StringBuilder StringBuffer Object System Math Integer Long Double
Boolean Character Arrays Objects Collections List ArrayList LinkedList Map HashMap
LinkedHashMap TreeMap Set HashSet LinkedHashSet TreeSet Queue Deque ArrayDeque Stack
Optional Stream Collectors Comparator Comparable Iterator Iterable Files Path Paths
Scanner BufferedReader BufferedWriter InputStreamReader OutputStreamWriter PrintWriter
Exception RuntimeException IOException IllegalArgumentException File FileReader
FileWriter Thread Runnable ExecutorService Executors ConcurrentHashMap
CopyOnWriteArrayList AtomicInteger LocalDate LocalDateTime Duration Instant
Pattern Matcher BigDecimal BigInteger Random UUID Properties""".split())

CLI_TOOLS = set('''gcc g++ cc c++ clang clang++ make cmake ninja gdb lldb valgrind objdump nm ld ar strip pkg-config git javac java python pip py'''.split())

C_LIB = set("""printf scanf puts gets putchar getchar malloc calloc realloc free strlen
strcpy strncpy strcat strncat strcmp strncmp strstr strchr strtok memcpy memmove memset
memcmp fopen fclose fprintf fscanf fgets fputs fread fwrite fseek ftell rewind perror
errno assert exit atoi atof atol strtol strtod qsort bsearch snprintf sprintf sscanf
time rand srand abs sqrt pow toupper tolower isdigit isalpha""".split())

CPP_STL = set("""std vector string map unordered_map set unordered_set list deque array
queue stack priority_queue pair tuple optional variant any function bind unique_ptr
shared_ptr weak_ptr make_unique make_shared move forward cout cin cerr endl getline
stringstream istringstream ostringstream sort stable_sort find find_if count count_if
accumulate transform for_each remove_if unique reverse min max clamp swap to_string
stoi stod substr size length push_back emplace_back begin end cbegin cend at front back
""".split())

MYSQL_KW = set("""SELECT INSERT UPDATE DELETE CREATE DROP ALTER TABLE DATABASE INDEX VIEW
TRIGGER PROCEDURE FUNCTION EVENT FROM WHERE GROUP BY HAVING ORDER LIMIT OFFSET JOIN INNER
LEFT RIGHT OUTER CROSS ON USING AS AND OR NOT NULL IS IN BETWEEN LIKE EXISTS UNION ALL
DISTINCT CASE WHEN THEN ELSE END SET VALUES INTO PRIMARY KEY FOREIGN REFERENCES UNIQUE
CHECK DEFAULT AUTO_INCREMENT ENGINE CHARSET CHARACTER COLLATE START TRANSACTION COMMIT
ROLLBACK SAVEPOINT GRANT REVOKE CREATE USER SHOW DESCRIBE EXPLAIN USE BEGIN DECLARE
CASCADE RESTRICT TRUNCATE REPLACE WITH ROLLUP FOR UPDATE LOCK IN SHARE MODE
READ UNCOMMITTED COMMITTED REPEATABLE SERIALIZABLE IF DELIMITER CALL RETURNS RETURN
AFTER BEFORE EACH ROW SCHEDULE EVERY STARTS ENDS ENABLE DISABLE""".split())
MYSQL_FN = set("""COUNT SUM AVG MAX MIN COALESCE IFNULL NULLIF NOW CURDATE CURTIME DATE_FORMAT
DATEDIFF TIMESTAMPDIFF YEAR MONTH DAY HOUR CONCAT CONCAT_WS SUBSTRING TRIM UPPER LOWER
LENGTH CHAR_LENGTH REPLACE ROUND CEIL FLOOR ABS CAST CONVERT JSON_EXTRACT JSON_OBJECT
GROUP_CONCAT ROW_COUNT LAST_INSERT_ID RAND UUID VERSION DATABASE USER CURRENT_USER
MD5 SHA2 REGEXP LIKE""".split())
MYSQL_CLI = set("""mysql mysqld mysqladmin mysqldump mysqlimport mysqlbinlog mysqld_safe
workbench dbeaver navicat source tee explain analyze""".split())

LINUX_CMD = set("""ls cd pwd mkdir rmdir touch cp mv rm ln find grep egrep sed awk cut sort
uniq wc tr tee xargs head tail cat less more nano vim vi emacs file diff patch chmod chown
chgrp umask sudo su ps top htop kill pkill killall jobs fg bg nohup screen tmux ssh scp
rsync sftp curl wget ping dig nslookup ss netstat lsof tar gzip gunzip zip unzip df du
free mount umount lsblk uname uptime date timedatectl hostnamectl reboot shutdown systemctl
journalctl apt apt-get dpkg dnf yum pacman make cmake gcc g++ python python3 pip bash sh
zsh source export alias history echo printf type which command man info apropos strace
crontab cron env printenv locale chmod tee split basename dirname realpath stat md5sum
sha256sum ln useradd usermod passwd groupadd id whoami who w last dmesg nice renice
""".split())
LINUX_OPT = set("""-l -a -h -r -f -i -n -v -R -p -t -u -s -c -d -e -o -q -w -x -A -B -C -L -P -S
-k -m -g -j -F -I -0 -9 --help --version 2>&1 > >> < | || && ; $? $! $$ $@ $# \
/dev/null /dev/sda /proc stdin stdout stderr SIGTERM SIGKILL SIGINT
Ctrl+C Ctrl+D Ctrl+L Ctrl+R Ctrl+Z Tab""".split())

HTML_TAG = set("""a abbr address area article aside audio b base bdi bdo blockquote body br
button canvas caption cite code col colgroup data datalist dd del details dfn dialog div dl
dt em embed fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head header hgroup hr
html i iframe img input ins kbd label legend li link main map mark menu meta meter nav
noscript object ol optgroup option output p picture pre progress q rp rt ruby s samp script
section select slot small source span strong style sub summary sup table tbody td template
textarea tfoot th thead time title tr track u ul var video wbr doctype""".split())

HTML_ATTR = set("""href src alt title class id style target rel type name value placeholder
required pattern min max maxlength minlength readonly disabled checked selected multiple
size rows cols action method enctype accept accept-charset autocomplete autofocus form
for colspan rowspan scope headers caption lang tabindex hidden draggable contenteditable
loading decoding controls autoplay loop muted poster preload width height srcset sizes
defer async crossorigin integrity charset content http-equiv property media datetime
open download role aria-label aria-hidden aria-expanded aria-describedby aria-live
data-id data- xlink persist novalidate spellcheck translate dir cite start reversed
""".split())

# ── 人工修正：自动判断不合适的条目 ───────────────────────────────────
OVERRIDES = {
    # (语言, 条目名): 标记
    ("java", "类与实例"): "kw",
    ("java", "控制台输入"): "api",
    ("java", "数组"): "kw",
    ("java", "二维数组"): "kw",
    ("java", "带标签跳转"): "kw",
    ("java", "break / continue"): "kw",
    ("java", "三元运算符"): "kw",
    ("java", "if / else if / else"): "kw",
    ("java", "switch 与 switch 表达式"): "kw",
    ("java", "equals 与 hashCode"): "ann",
    ("java", "toString"): "ann",
    ("java", "字符串比较"): "api",
    ("java", "枚举 enum"): "kw",
    ("java", "记录类 record"): "kw",
    ("java", "局部类型推断"): "kw",
    ("java", "字面量与后缀"): "syn",
    ("java", "算术运算"): "syn",
    ("java", "关系与逻辑"): "syn",
    ("java", "位运算"): "syn",
    ("java", "自增自减"): "syn",
    ("java", "优先级与括号"): "syn",
    ("java", "整除与取余的坑"): "syn",
    ("java", "浮点误差"): "syn",
    ("java", "递归"): "syn",
    ("java", "getter / setter"): "syn",
    ("java", "可变参数"): "syn",
    ("java", "构造方法"): "syn",
    ("java", "接口默认方法"): "kw",
    ("c", "编译 → 运行两步"): "syn",
    ("c", "字符串 = 字符数组 + \\0"): "syn",
    ("c", "未定义行为（UB）"): "syn",
    ("c", "下标从 0 开始"): "syn",
    ("cpp", "编译 → 运行两步"): "syn",
    ("cpp", "值语义与引用语义"): "syn",
    ("py", "缩进即语法"): "kw",
    ("py", "`if __name__ == \"__main__\"`"): "kw",
    ("mysql", "默认端口"): "syn",
    ("mysql", "SQL 的四类语句"): "kw",
    ("linux", "四个救命快捷键"): "opt",
    ("linux", "三种引号"): "opt",
    ("html", "`<!DOCTYPE html>`"): "tag",
    ("html", "标题"): "tag",
}


def tagset(sid):
    return TAGS.get(sid, [])


def label(sid, key):
    for k, lab in TAGS.get(sid, []):
        if k == key:
            return lab
    return key


def _first_token(text):
    t = text.strip().strip("`").strip()
    t = re.sub(r"^new\s+", "", t)
    t = re.sub(r"^@", "", t)
    t = re.split(r"[\s(<{,\[;:.]", t)[0]
    return t.strip("`\"'()[]{}")


def _has_code_shape(text):
    """像一段代码骨架，而不是一个词。"""
    return bool(re.search(r"[={}<>]|\bnew\b|\breturn\b", text)) and "(" in text


def _bare(s):
    return (s or "").strip().strip("`").strip()


def _name_tag(sid, name):
    """先看条目名本身——很多行的「名字」就是一个关键字/库函数名。"""
    n = _bare(name)
    n = re.sub(r"[（(].*?[)）]", "", n).strip().strip("`").strip()
    if not n:
        return None
    tok = re.split(r"[\s、,/·]", n)[0].strip("`").strip()
    tok = tok.rstrip("=").strip()

    if sid == "java":
        if n.startswith("@"):
            return "ann"
        if tok in JAVA_KW or tok in JAVA_LITERALS:
            return "kw"
        if any(t.strip("`") in JAVA_JDK for t in re.split(r"[\s、,/·（）()]", n) if t.strip("`")):
            return "api"
    elif sid == "c":
        if tok in C_KW:
            return "kw"
        if tok in C_LIB:
            return "lib"
    elif sid == "cpp":
        if tok in CPP_KW:
            return "kw"
        if tok in CPP_STL:
            return "stl"
    elif sid == "py":
        if tok in PY_KW:
            return "kw"
        if tok in PY_BUILTIN:
            return "bi"
        if tok in PY_MODULE:
            return "mod"
        if re.search(r"(python|pip|py|venv|mypy|pytest|jupyter|black|ruff)\b", n, re.I):
            return "cli"
    elif sid == "mysql":
        if tok.upper() in MYSQL_KW:
            return "kw"
        if tok.upper() in MYSQL_FN:
            return "fn"
        if tok.lower() in MYSQL_CLI:
            return "cli"
    elif sid == "linux":
        if tok in LINUX_CMD:
            return "cmd"
        if tok in LINUX_OPT:
            return "opt"
    elif sid == "html":
        if tok.lower().strip("<>") in HTML_TAG:
            return "tag"
        if tok.lower() in HTML_ATTR:
            return "attr"
    return None


def classify(sid, name, api):
    """返回 tag key（该语言 tags 里的某一个）。"""
    ov = OVERRIDES.get((sid, name))
    if ov:
        return ov
    nt = _name_tag(sid, name)
    if nt:
        return nt

    text = (api or "").strip()
    if not text or text in ("—", "-"):
        return (TAGS.get(sid) or [("syn", "")])[-1][0]
    bare = _bare(text)
    tok = _first_token(bare)

    if sid == "java":
        if bare.startswith("@"):
            return "ann"
        if tok in JAVA_KW or tok in JAVA_LITERALS:
            return "kw"
        if not re.search(r"[A-Za-z_]{2,}", bare):
            return "syn"
        first = re.split(r"[\s(、,.<]", bare)[0]
        if first[:1].isupper():
            return "api"
        if _has_code_shape(bare) and "System." not in bare:
            return "syn"
        return "api"

    if sid == "c":
        if bare.startswith("-"):
            return "cli"
        if tok in CLI_TOOLS:
            return "cli"
        if tok in C_KW:
            return "kw"
        if tok in C_LIB:
            return "lib"
        if not re.search(r"[A-Za-z_]{2,}", bare):
            return "syn"
        if _has_code_shape(bare):
            return "syn"
        return "lib"

    if sid == "cpp":
        if bare.startswith("-"):
            return "cli"
        if tok in CLI_TOOLS:
            return "cli"
        if tok in CPP_KW:
            return "kw"
        if tok in CPP_STL:
            return "stl"
        if bare.startswith("std::"):
            return "stl"
        if not re.search(r"[A-Za-z_]{2,}", bare):
            return "syn"
        if _has_code_shape(bare):
            return "syn"
        return "stl"

    if sid == "py":
        if tok in PY_KW:
            return "kw"
        if tok in PY_BUILTIN:
            return "bi"
        if bare.startswith(PY_MODULE_PREFIX) or tok in PY_MODULE:
            return "mod"
        if re.match(r"^(python|pip|py|mypy|pytest|jupyter|black|ruff)\b", bare):
            return "cli"
        if re.match(r"^(numpy|pandas|matplotlib|np|pd|plt|copy|pdb|os|sys|re|json|csv|"
                    r"pathlib|itertools|collections|datetime|math|random)\.", bare):
            return "mod"
        if not re.search(r"[A-Za-z_]{2,}", bare):
            return "syn"
        if re.match(r"^(import|from|with|for|while|if|try|def|class|raise|assert|del|yield|"
                    r"async|await|global|nonlocal|lambda|pass|break|continue|return|else|"
                    r"elif|except|finally|in|is|not|and|or)\b", bare):
            return "kw"
        if _has_code_shape(bare):
            return "syn"
        return "syn"

    if sid == "mysql":
        up = bare.upper()
        if tok.upper() in MYSQL_KW:
            return "kw"
        if tok.upper() in MYSQL_FN:
            return "fn"
        if tok.lower() in MYSQL_CLI:
            return "cli"
        if re.search(r"^(INSERT|SELECT|UPDATE|DELETE|CREATE|ALTER|DROP|SHOW|EXPLAIN|GRANT|"
                     r"REVOKE|START|COMMIT|ROLLBACK|USE)\b", up):
            return "kw"
        if not re.search(r"[A-Za-z]{2,}", bare):
            return "syn"
        if _has_code_shape(bare):
            return "syn"
        return "fn"

    if sid == "linux":
        if bare in LINUX_OPT:
            return "opt"
        if re.search(r"^\s*(\||>|>>|2>&1|&&|\|\||;|&|\$)", bare):
            return "opt"
        if tok in LINUX_CMD:
            return "cmd"
        if bare.startswith("/") or bare.startswith("~/") or bare.startswith("."):
            return "cfg"
        if not re.search(r"[A-Za-z_]{2,}", bare):
            return "opt"
        if _has_code_shape(bare):
            return "syn"
        return "cmd"

    if sid == "html":
        low = bare.lower()
        if low.startswith("<"):
            first = re.split(r"[\s>/]", low.lstrip("<"))[0]
            if first in HTML_TAG:
                return "tag"
            return "syn"
        if tok.lower() in HTML_ATTR or tok.lower().rstrip("=") in HTML_ATTR:
            return "attr"
        if tok.lower() in HTML_TAG:
            return "tag"
        if _has_code_shape(bare) or not re.search(r"[A-Za-z]{2,}", bare):
            return "syn"
        return "syn"

    return "syn"

HINTS = {
    "kw": "语言自带的词，写代码绕不开",
    "ann": "注解，写在类或方法上",
    "api": "JDK 现成的类/方法，查文档",
    "lib": "C 标准库函数，include 就能用",
    "stl": "C++ 标准库，include 就能用",
    "mod": "Python 模块，import 就能用",
    "bi": "Python 内置，不用 import",
    "cli": "在终端里敲的命令",
    "cmd": "要敲的命令",
    "opt": "符号 / 选项 / 语法形式",
    "cfg": "路径 / 配置文件",
    "fn": "SQL 里调用的函数",
    "tag": "HTML 标签",
    "attr": "HTML 属性",
    "syn": "写法或思路，不是某个名字",
}


def legend_hint(sid, key):
    return HINTS.get(key, "")