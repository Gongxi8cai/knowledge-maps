# -*- coding: utf-8 -*-
"""
mapkit — 一个数据源同时生成 Markdown 与 HTML 的「知识地图」渲染器。

用法（见 build_maps.py）：
    from mapkit import render
    render(SUBJ, outdir)   # 生成 <outdir>/<SUBJ.id>知识地图.md 和 .html

数据结构（SUBJ 字典）：
    id        文件名用的短标识，如 "c"
    title     标题，如 "C 语言知识地图"
    tagline   一句话说明
    accent    主题色（十六进制）
    scope     右上角小标签，如 "自学 · 基础"
    level_h   第五列表头，默认 "阶段"
    base      [(条目, 说明, 例子), ...]                  第 0 层：基础通用
    domains   [ {id, name, de, goal, entries: [(名称, 关键字/API, 用途, 阶段, 交叉)]}, ... ]
    cross     [(概念, [(域, 条目), ...], 为什么), ...]     跨域重复
    notes     [(标题, 说明), ...]
    quick     [(我想……, 去哪个域), ...]
"""
import html
import pathlib
import re

import tagkit

# --------------------------------------------------------------------------- #
#  Markdown
# --------------------------------------------------------------------------- #


def _c(s):
    """Tabellenzelle: Pipes maskieren, Zeilenumbrueche zu Leerzeichen."""
    return str(s).replace("|", "\\|").replace("\n", " ")


def _md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(_c(x) for x in r) + " |")
    return "\n".join(out)


def to_markdown(s):
    L = []
    n_entries = sum(len(d["entries"]) for d in s["domains"])
    L.append(f"# {s['title']}\n")
    L.append(f"> {s['tagline']}\n")
    L.append(
        f"**{len(s['domains'])} 个功能域 · {n_entries} 个条目 · "
        f"{len(s['base'])} 条基础通用 · {len(s['cross'])} 组交叉概念 · "
        f"{len(s['notes'])} 条备注**　（{s.get('scope', '')}）\n"
    )
    L.append("按「你要干什么」找工具，而不是按语法书目录背。同一个功能若跨多个域，"
             "会在多个域里重复出现，并在「交叉」列标出它还在哪出现；基础通用与备注各自单列。\n")

    # 一页提纲
    L.append("## 0.5 一页提纲（先扫这个）\n")
    for d in s["domains"]:
        names = " · ".join(e[0] for e in d["entries"])
        L.append(f"- **{d['name']}**：{names}")
    L.append("")

    L.append("## 1. 基础通用（第 0 层，单列）\n")
    L.append(_md_table(["条目", "说明", "例子"], s["base"]))
    L.append("")

    L.append("## 2. 功能域（第 1 层）\n")
    L.append("第 2 列前面的〔〕是这一条的性质：" +
             " / ".join(f"〔{lab}〕" for _k, lab in tagkit.TAGS.get(s["id"], [])) +
             "——〔" + (tagkit.TAGS.get(s["id"], [("", "")])[0][1]) +
             "〕要自己写，其余是现成的名字（查文档 / 查手册就行）。\n")
    for i, d in enumerate(s["domains"], 1):
        sub = f"　<sub>{d['de']}</sub>" if d.get("de") else ""
        L.append(f"### 2.{i} {d['name']}{sub}\n")
        L.append(f"{d['goal']}\n")
        rows = []
        for e in d["entries"]:
            k = tagkit.classify(s["id"], e[0], e[1])
            lab = tagkit.label(s["id"], k)
            rows.append((e[0], f"〔{lab}〕{e[1]}", e[2], e[3], e[4] or "—"))
        L.append(_md_table(["功能", "关键字 / API", "用来做什么", s.get("level_h", "阶段"), "交叉"], rows))
        L.append("")

    L.append("## 3. 交叉项总表（同一概念出现在多个域）\n")
    rows = []
    for concept, places, why in s["cross"]:
        where = " · ".join(f"{d}「{e}」" for d, e in places)
        rows.append((concept, where, why))
    L.append(_md_table(["概念", "出现在", "为什么重复出现"], rows))
    L.append("")

    L.append("## 4. 备注（易错点 / 取舍 / 顺序）\n")
    for i, (t, txt) in enumerate(s["notes"], 1):
        L.append(f"{i}. **{t}**：{txt}")
    L.append("")

    L.append("## 5. 反向查：我要做 X，去哪个域\n")
    L.append(_md_table(["我要……", "去这里"], s["quick"]))
    L.append("")
    L.append("---\n")
    L.append(f"*由 `mapkit.py` 生成（单一数据源，Markdown 与 HTML 内容一致）。共 "
             f"{n_entries} 条。*\n")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
#  HTML
# --------------------------------------------------------------------------- #

HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --bg:#0d1117; --panel:#161b22; --panel2:#1c2330; --line:#2a3446;
  --fg:#e6edf3; --dim:#8b98a9; --accent:{accent}; --code:#9cd0ff;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--bg); color:var(--fg);
  font:15px/1.65 -apple-system,"Segoe UI","Microsoft YaHei",Roboto,sans-serif;
}}
a {{ color:var(--accent); text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
header {{
  padding:34px 40px 22px; border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,#121926 0%,var(--bg) 100%);
}}
h1 {{ margin:0 0 8px; font-size:27px; letter-spacing:.4px; }}
h1 .dot {{ color:var(--accent); }}
.tagline {{ color:var(--dim); font-size:14px; max-width:960px; }}
.chips {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }}
.chip {{
  font-size:12.5px; color:var(--dim); border:1px solid var(--line);
  border-radius:999px; padding:4px 11px; background:var(--panel);
}}
.chip b {{ color:var(--fg); font-weight:600; }}
.wrap {{ display:grid; grid-template-columns:236px 1fr; align-items:start; }}
nav {{
  position:sticky; top:0; max-height:100vh; overflow:auto;
  padding:20px 12px 40px; border-right:1px solid var(--line);
}}
nav .grp {{ font-size:11.5px; color:#6c7a8d; text-transform:uppercase;
  letter-spacing:1px; margin:16px 8px 6px; }}
nav a {{ display:flex; justify-content:space-between; gap:8px; color:#c3ccd8;
  font-size:13.5px; padding:5px 8px; border-radius:6px; }}
nav a:hover {{ background:var(--panel2); text-decoration:none; }}
nav a.on {{ background:var(--panel2); color:var(--accent); }}
nav .n {{ color:#5d6b7e; font-size:12px; }}
main {{ padding:26px 40px 80px; max-width:1180px; }}
.search {{ position:sticky; top:0; z-index:5; padding:12px 0 14px; background:var(--bg); }}
.search input {{
  width:100%; max-width:430px; padding:10px 13px; border-radius:8px;
  border:1px solid var(--line); background:var(--panel); color:var(--fg);
  font-size:14px; outline:none;
}}
.search input:focus {{ border-color:var(--accent); }}
.search .hint {{ color:#6c7a8d; font-size:12.5px; margin-left:10px; }}
h2 {{
  font-size:19px; margin:38px 0 14px; padding-bottom:8px;
  border-bottom:1px solid var(--line);
}}
h2:first-of-type {{ margin-top:10px; }}
.card {{
  background:var(--panel); border:1px solid var(--line); border-radius:12px;
  padding:18px 20px 10px; margin:16px 0;
}}
.card h3 {{ margin:0 0 4px; font-size:16.5px; }}
.card h3 .de {{ color:#6c7a8d; font-weight:400; font-size:12.5px; margin-left:8px; }}
.card .goal {{ color:var(--dim); font-size:13.5px; margin:0 0 12px; }}
table {{ width:100%; border-collapse:collapse; font-size:13.5px; }}
th {{
  text-align:left; color:#7f8da0; font-weight:600; font-size:12px;
  text-transform:uppercase; letter-spacing:.6px;
  padding:6px 10px; border-bottom:1px solid var(--line); white-space:nowrap;
}}
td {{ padding:8px 10px; border-bottom:1px solid #1e2634; vertical-align:top; }}
tr:last-child td {{ border-bottom:none; }}
td.k {{ font-weight:600; color:#dbe6f3; }}
td .api {{
  font-family:ui-monospace,Consolas,"Cascadia Mono",monospace; font-size:12.5px;
  color:var(--code); background:#0f1621; border:1px solid #1f2a3a;
  border-radius:5px; padding:1px 5px; display:inline-block; word-break:break-word;
}}
td .tag {{
  display:inline-block; font-size:10.5px; line-height:1; padding:3px 6px; margin-right:6px;
  border-radius:5px; border:1px solid var(--line); color:var(--dim); background:#141b26;
  vertical-align:1px; white-space:nowrap;
}}
td.ac {{ display:flex; flex-wrap:wrap; gap:5px; align-items:flex-start; }}
td.ac .tag {{ margin-right:0; margin-top:1px; }}
td.ac .api {{ flex:0 1 auto; max-width:100%; }}
.t-kw  {{ border-color:#3b5bdb; color:#9db4ff; background:#141d33; }}
.t-ann {{ border-color:#7048b6; color:#c9a6ff; background:#1d1630; }}
.t-api {{ border-color:#1f6f43; color:#7fe3b0; background:#0f2a1d; }}
.t-lib {{ border-color:#1f6f43; color:#7fe3b0; background:#0f2a1d; }}
.t-stl {{ border-color:#1f6f43; color:#7fe3b0; background:#0f2a1d; }}
.t-mod {{ border-color:#1f6f43; color:#7fe3b0; background:#0f2a1d; }}
.t-bi  {{ border-color:#2a6f7a; color:#8fe4ef; background:#0d2328; }}
.t-cli {{ border-color:#7a5220; color:#f0b866; background:#2a1f0f; }}
.t-cmd {{ border-color:#2a6f7a; color:#8fe4ef; background:#0d2328; }}
.t-opt {{ border-color:#7a5220; color:#f0b866; background:#2a1f0f; }}
.t-cfg {{ border-color:#7a2f3c; color:#ff8fa3; background:#2a121a; }}
.t-fn  {{ border-color:#7a5220; color:#f0b866; background:#2a1f0f; }}
.t-tag {{ border-color:#2a6f7a; color:#8fe4ef; background:#0d2328; }}
.t-attr {{ border-color:#7048b6; color:#c9a6ff; background:#1d1630; }}
.t-syn {{ border-color:#3a4657; color:#93a2b5; background:#161d27; }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; align-items:center; color:var(--dim);
  font-size:12.5px; margin:6px 0 2px; }}
.legend .tag {{ margin-right:5px; }}
td.why {{ color:#aab6c4; }}
.lvl {{
  font-size:11.5px; border-radius:999px; padding:1px 8px; white-space:nowrap;
  border:1px solid var(--line); color:var(--dim);
}}
.lvl.g {{ border-color:#1f6f43; color:#5ddb9b; background:#0f2a1d; }}
.lvl.b {{ border-color:#24507f; color:#7bb8ff; background:#0f1e2e; }}
.lvl.o {{ border-color:#7a5220; color:#f0b866; background:#2a1f0f; }}
.lvl.r {{ border-color:#7a2f3c; color:#ff8fa3; background:#2a121a; }}
.x {{ color:var(--accent); font-size:12.5px; }}
.note {{ display:flex; gap:12px; padding:10px 0; border-bottom:1px solid #1e2634; }}
.note:last-child {{ border-bottom:none; }}
.note .i {{
  flex:0 0 26px; height:26px; border-radius:8px; background:var(--panel2);
  color:var(--accent); font-size:12.5px; display:grid; place-items:center;
}}
.note .t {{ font-weight:600; }}
.note .d {{ color:#aab6c4; font-size:13.5px; }}
.outline li {{ margin:3px 0; }}
.outline .dn {{ color:var(--fg); font-weight:600; }}
.outline .en {{ color:var(--dim); }}
code {{
  font-family:ui-monospace,Consolas,"Cascadia Mono",monospace; font-size:12.5px;
  color:var(--code); background:#0f1621; border:1px solid #1f2a3a;
  border-radius:5px; padding:1px 5px;
}}
.hidden {{ display:none !important; }}
footer {{ color:#5d6b7e; font-size:12.5px; padding:30px 40px 60px; border-top:1px solid var(--line); }}
@media (max-width:900px) {{
  .wrap {{ grid-template-columns:1fr; }}
  nav {{ position:static; max-height:none; border-right:none; border-bottom:1px solid var(--line); }}
  main, header, footer {{ padding-left:20px; padding-right:20px; }}
}}
</style>
</head>
<body>
"""

HTML_JS = """
<script>
(function () {
  var box = document.getElementById('q');
  var hint = document.getElementById('hint');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card, .note-block'));
  var total = document.querySelectorAll('table tbody tr').length;

  function norm(s) { return (s || '').toLowerCase(); }

  box.addEventListener('input', function () {
    var q = norm(box.value.trim());
    var hits = 0;
    cards.forEach(function (card) {
      var rows = Array.prototype.slice.call(card.querySelectorAll('tbody tr'));
      if (!rows.length) { return; }
      var shown = 0;
      rows.forEach(function (tr) {
        var ok = !q || norm(tr.textContent).indexOf(q) >= 0;
        tr.classList.toggle('hidden', !ok);
        if (ok) { shown++; }
      });
      card.classList.toggle('hidden', shown === 0);
      hits += shown;
    });
    hint.textContent = q ? (hits + ' 条命中') : (total + ' 条');
  });

  // aktiven Navigationspunkt hervorheben
  var links = Array.prototype.slice.call(document.querySelectorAll('nav a[href^="#"]'));
  var targets = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  var obs = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) { return; }
      links.forEach(function (a) { a.classList.remove('on'); });
      var i = targets.indexOf(e.target);
      if (i >= 0) { links[i].classList.add('on'); }
    });
  }, { rootMargin: '-15% 0px -75% 0px' });
  targets.forEach(function (t) { if (t) { obs.observe(t); } });
})();
</script>
</body>
</html>
"""

LVL_CLASS = {"入门": "g", "常用": "b", "进阶": "o", "进阶+": "r",
            "基础": "g", "核心": "b", "高级": "o"}


def _h(s):
    """Text -> HTML: escapen, dann `code` und **fett** auszeichnen."""
    s = html.escape(str(s), quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s


def _lvl(v):
    cls = LVL_CLASS.get(v, "")
    return f'<span class="lvl {cls}">{_h(v)}</span>' if v and v != "—" else '<span style="color:#4d5a6b">—</span>'


def to_html(s):
    n_entries = sum(len(d["entries"]) for d in s["domains"])
    P = [HTML_HEAD.format(title=html.escape(s["title"]), accent=s["accent"])]

    P.append("<header>")
    parts = s["title"].split("知识地图")
    h1 = _h(parts[0]) + '<span class="dot">·</span>知识地图' + _h("知识地图".join(parts[1:]))
    P.append(f"<h1>{h1}</h1>")
    P.append(f'<div class="tagline">{_h(s["tagline"])}</div>')
    P.append('<div class="chips">')
    P.append(f'<span class="chip">功能域 <b>{len(s["domains"])}</b></span>')
    P.append(f'<span class="chip">功能条目 <b>{n_entries}</b></span>')
    P.append(f'<span class="chip">基础通用 <b>{len(s["base"])}</b></span>')
    P.append(f'<span class="chip">交叉概念 <b>{len(s["cross"])}</b></span>')
    P.append(f'<span class="chip">备注 <b>{len(s["notes"])}</b></span>')
    if s.get("scope"):
        P.append(f'<span class="chip">{_h(s["scope"])}</span>')
    P.append("</div>")
    P.append('<div class="legend"><span>第 2 列的小标签表示这一条的性质：</span>')
    for k, lab in tagkit.TAGS.get(s["id"], []):
        P.append(f'<span><span class="tag t-{k}">{_h(lab)}</span>{_h(tagkit.legend_hint(s["id"], k))}</span>')
    P.append("</div></header>")

    P.append('<div class="wrap"><nav>')
    P.append('<div class="grp">地基</div>')
    P.append(f'<a href="#base">基础通用 <span class="n">{len(s["base"])}</span></a>')
    P.append(f'<a href="#outline">一页提纲 <span class="n">{len(s["domains"])}</span></a>')
    P.append('<div class="grp">功能域</div>')
    for d in s["domains"]:
        P.append(f'<a href="#{d["id"]}">{_h(d["name"])} <span class="n">{len(d["entries"])}</span></a>')
    P.append('<div class="grp">跨层</div>')
    P.append(f'<a href="#cross">交叉项总表 <span class="n">{len(s["cross"])}</span></a>')
    P.append(f'<a href="#notes">备注 <span class="n">{len(s["notes"])}</span></a>')
    P.append(f'<a href="#quick">反向查 <span class="n">{len(s["quick"])}</span></a>')
    P.append("</nav><main>")

    P.append('<div class="search"><input id="q" type="search" '
             'placeholder="搜功能、API 或关键词……（例如 指针 / 索引 / 管道）" autocomplete="off">'
             f'<span class="hint" id="hint">{n_entries + len(s["base"]) + len(s["cross"]) + len(s["quick"])} 条</span></div>')

    # 基础通用
    P.append('<h2 id="base">第 0 层 · 基础通用（所有域共用）</h2>')
    P.append('<div class="card"><table><thead><tr><th style="width:16%">条目</th>'
             '<th style="width:38%">说明</th><th>例子</th></tr></thead><tbody>')
    for name, desc, ex in s["base"]:
        P.append(f'<tr><td class="k">{_h(name)}</td><td>{_h(desc)}</td>'
                 f'<td><span class="api">{_h(ex)}</span></td></tr>')
    P.append("</tbody></table></div>")

    # 一页提纲
    P.append('<h2 id="outline">一页提纲 · 先扫这个</h2>')
    P.append('<div class="card outline"><ul style="margin:0;padding-left:18px">')
    for d in s["domains"]:
        names = " · ".join(f'<span class="en">{_h(e[0])}</span>' for e in d["entries"])
        P.append(f'<li><span class="dn">{_h(d["name"])}</span>：{names}</li>')
    P.append("</ul></div>")

    # 功能域
    for d in s["domains"]:
        de = f'<span class="de">{_h(d["de"])}</span>' if d.get("de") else ""
        P.append(f'<div class="card" id="{d["id"]}"><h3>{_h(d["name"])}{de}</h3>')
        P.append(f'<p class="goal">{_h(d["goal"])}</p>')
        P.append('<table><thead><tr><th style="width:15%">功能</th>'
                 '<th style="width:27%">关键字 / API</th><th style="width:33%">用来做什么</th>'
                 f'<th style="width:10%">{_h(s.get("level_h", "阶段"))}</th>'
                 '<th style="width:15%">交叉</th></tr></thead><tbody>')
        for name, api, use, lvl, cross in d["entries"]:
            k = tagkit.classify(s["id"], name, api)
            lab = tagkit.label(s["id"], k)
            P.append(f'<tr><td class="k">{_h(name)}</td>'
                     f'<td class="ac"><span class="tag t-{k}">{_h(lab)}</span>'
                     f'<span class="api">{_h(api)}</span></td>'
                     f'<td>{_h(use)}</td><td>{_lvl(lvl)}</td>'
                     f'<td class="x">{_h(cross) if cross else "—"}</td></tr>')
        P.append("</tbody></table></div>")

    # 交叉
    P.append('<h2 id="cross">交叉项总表 · 同一概念出现在多个域</h2>')
    P.append('<div class="card"><table><thead><tr><th style="width:18%">概念</th>'
             '<th style="width:42%">出现在</th><th>为什么重复出现</th></tr></thead><tbody>')
    for concept, places, why in s["cross"]:
        where = " · ".join(f'{_h(d)}「{_h(e)}」' for d, e in places)
        P.append(f'<tr><td class="k">{_h(concept)}</td><td>{where}</td>'
                 f'<td class="why">{_h(why)}</td></tr>')
    P.append("</tbody></table></div>")

    # 备注
    P.append('<h2 id="notes">备注 · 易错点 / 取舍 / 顺序</h2>')
    P.append('<div class="card note-block">')
    for i, (t, txt) in enumerate(s["notes"], 1):
        P.append(f'<div class="note"><div class="i">{i}</div><div>'
                 f'<div class="t">{_h(t)}</div><div class="d">{_h(txt)}</div></div></div>')
    P.append("</div>")

    # 反向查
    P.append('<h2 id="quick">反向查 · 我要做 X，去哪个域</h2>')
    P.append('<div class="card"><table><thead><tr><th style="width:45%">我要……</th>'
             '<th>去这里</th></tr></thead><tbody>')
    for task, where in s["quick"]:
        P.append(f'<tr><td class="k">{_h(task)}</td><td>{_h(where)}</td></tr>')
    P.append("</tbody></table></div>")

    P.append("</main></div>")
    P.append(f'<footer>{_h(s["title"])} · 共 {n_entries} 个条目 · '
             f'由 <code>mapkit.py</code> 从同一份数据生成（Markdown 版内容一致）</footer>')
    P.append(HTML_JS)
    return "\n".join(P)


# --------------------------------------------------------------------------- #
#  Ausgabe
# --------------------------------------------------------------------------- #


def render(s, outdir):
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    base = f"{s['id']}知识地图" if not s["id"].endswith("map") else s["id"]
    stem = s.get("file", f"{s['title']}")
    md_path = out / f"{stem}.md"
    html_path = out / f"{stem}.html"
    md_path.write_text(to_markdown(s), encoding="utf-8")
    html_path.write_text(to_html(s), encoding="utf-8")
    n = sum(len(d["entries"]) for d in s["domains"])
    print(f"  {s['title']:<14} {n:>4} 条  {len(s['domains']):>2} 域  "
          f"md {md_path.stat().st_size:>7,} B   html {html_path.stat().st_size:>7,} B")
    return md_path, html_path
