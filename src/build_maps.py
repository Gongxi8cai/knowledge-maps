# -*- coding: utf-8 -*-
"""生成六份知识地图 + 总入口 index.html。"""
import importlib
import html
import shutil
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import mapkit  # noqa: E402

OUT = pathlib.Path(os.environ.get("MAPS_OUT", r"D:\02_学业\知识地图"))
MODULES = [
    ("md_c", "c"),
    ("md_cpp", "cpp"),
    ("md_py", "py"),
    ("md_mysql", "mysql"),
    ("md_linux", "linux"),
    ("md_html", "html"),
]

JAVA_DIR = pathlib.Path(os.environ.get("JAVA_OUT", r"D:\02_学业\编程四门课\01_Java"))
JAVA_HTML = JAVA_DIR / "Java知识地图.html"

HUB_CSS = """
:root{--bg:#0d1117;--panel:#161b22;--panel2:#1c2330;--line:#2a3446;
--fg:#e6edf3;--dim:#8b98a9;--code:#9cd0ff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.75 -apple-system,"Segoe UI","Noto Sans SC",system-ui,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:52px 28px 80px}
h1{font-size:30px;line-height:1.3;margin:0 0 10px;letter-spacing:.3px}
.lead{color:var(--dim);margin:0 0 8px;font-size:15px}
.stats{color:var(--dim);font-size:13px;margin:18px 0 34px}
.stats b{color:var(--fg)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:20px 22px 16px;position:relative;overflow:hidden;
display:flex;flex-direction:column}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--ac)}
.card h2{font-size:18px;margin:0 0 6px;letter-spacing:.2px}
.card h2 .de{color:var(--dim);font-size:12px;font-weight:400;margin-left:8px}
.card p{color:var(--dim);font-size:13.5px;margin:0 0 14px;line-height:1.7}
.card .meta{font-size:12.5px;color:var(--dim);margin:0 0 14px}
.card .meta b{color:var(--fg);font-weight:600}
.card .meta span{white-space:nowrap}
.card .meta i{font-style:normal;color:var(--line);margin:0 5px}
.links{display:flex;gap:10px;flex-wrap:wrap;margin-top:auto}
.links a{color:var(--fg);text-decoration:none;font-size:13px;
border:1px solid var(--line);background:var(--panel2);
padding:5px 12px;border-radius:7px}
.links a:hover{border-color:var(--ac);color:var(--code)}
.foot{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);
color:var(--dim);font-size:13px}
.foot code{background:var(--panel2);padding:2px 6px;border-radius:5px;color:var(--code)}
"""


def hub(rendered):
    total_dom = sum(r["domains"] for r in rendered)
    total_ent = sum(r["entries"] for r in rendered)
    cards = []
    for r in rendered:
        s = r["subj"]
        cards.append(f"""
<article class="card" style="--ac:{s['accent']}">
  <h2>{html.escape(s['title'])}<span class="de">{html.escape(s['scope'])}</span></h2>
  <p>{html.escape(s['tagline'])}</p>
  <div class="meta"><span><b>{r['domains']}</b> 个功能域</span><i>·</i><span><b>{r['entries']}</b> 条功能</span><i>·</i>
    <span>基础通用 <b>{len(s['base'])}</b></span><i>·</i><span>交叉 <b>{len(s['cross'])}</b></span><i>·</i><span>备注 <b>{len(s['notes'])}</b></span></div>
  <div class="links">
    <a href="{html.escape(s['file'])}.html">打开互动版</a>
    <a href="{html.escape(s['file'])}.md">Markdown 版</a>
  </div>
</article>""")

    java_card = f"""
<article class="card" style="--ac:#ffcb8a">
  <h2>Java 知识地图<span class="de">第一学期 P1 · EiP</span></h2>
  <p>第一学期 P1（EiP）那份，同内容也放在这里，方便一起发到线上。
     18 个功能域、144 条功能，带课程位置标注（L3 / Blatt 4）与一页提纲。</p>
  <div class="meta"><span><b>18</b> 个功能域</span><i>·</i><span><b>144</b> 条功能</span><i>·</i>
    <span>基础通用 <b>12</b></span><i>·</i><span>交叉 <b>12</b></span><i>·</i><span>备注 <b>13</b></span></div>
  <div class="links">
    <a href="Java知识地图.html">打开互动版</a>
    <a href="Java知识地图.md">Markdown 版</a>
  </div>
</article>"""

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>编程知识地图 · 总入口</title>
<style>{HUB_CSS}</style>
</head>
<body>
<div class="wrap">
  <h1>编程知识地图 · 总入口</h1>
  <p class="lead">六门语言与技术，一个模子：第 0 层是通用常识，第 1 层按「你要干什么」分域，
    跨层把互相印证的条目串起来，最后单列备注与反向查。</p>
  <p class="stats">共 <b>{len(rendered) + 1}</b> 份地图 · <b>{total_dom + 18}</b> 个功能域 ·
    <b>{total_ent + 144}</b> 条功能 · 生成于 2026-11-18</p>
  <div class="grid">{''.join(cards)}{java_card}
  </div>
  <div class="foot">
    <p>每份都有两种形态：<code>.html</code> 带左侧导航与实时搜索（输 <code>equals</code>、
    <code>索引</code>、<code>管道</code> 试试）；<code>.md</code> 同内容，方便打印与 diff。</p>
    <p>阶段列：<b>入门</b> = 先学这个 · <b>常用</b> = 天天用 · <b>进阶</b> = 会用就行 ·
    <b>进阶+</b> = 知道有这回事即可。交叉列标出这个条目还在哪个域出现。</p>
  </div>
</div>
</body>
</html>
"""
    p = OUT / "index.html"
    p.write_text(doc, encoding="utf-8")
    return p


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rendered = []
    for mod, sid in MODULES:
        m = importlib.import_module(mod)
        s = m.SUBJ
        assert s["id"] == sid, f"{mod} id 不符: {s['id']} != {sid}"
        md, ht = mapkit.render(s, OUT)
        rendered.append({
            "subj": s,
            "domains": len(s["domains"]),
            "entries": sum(len(d["entries"]) for d in s["domains"]),
            "md": md,
            "html": ht,
        })
    hubp = hub(rendered)
    print("\n=== 汇总 ===")
    tdom = tent = 0
    for r in rendered:
        tdom += r["domains"]
        tent += r["entries"]
        print(f"{r['subj']['title']:<14} {r['domains']:>2} 域  {r['entries']:>3} 条  "
              f"{r['html'].stat().st_size:>7,} B")
    print(f"{'合计':<14} {tdom:>2} 域  {tent:>3} 条")
    print(f"\n总入口: {hubp}  ({hubp.stat().st_size:,} B)")
    # 把 Java 地图复制进来，让总入口的相对链接在本地和线上都成立
    if JAVA_HTML.exists():
        for src in (JAVA_HTML, JAVA_HTML.with_suffix(".md")):
            dst = OUT / src.name
            if src.resolve() != dst.resolve():
                shutil.copy2(src, dst)
            print(f"Java 地图: {src.name}  {dst.stat().st_size:,} B")


if __name__ == "__main__":
    main()
