#!/usr/bin/env python3
"""Write the lecture quizzes: scripts/quizzes/lecture-NN.json -> quickcheck/quiz-lecture-NN.html.

One self-contained HTML widget per lecture, shown on the last page of the lecture in an
iframe, like the quick checks. A quiz shows its questions one at a time, gives the
explanation after each answer, and ends with a score and the sections to review.

Run from the book folder:   python3 scripts/make_quizzes.py            (all lectures)
                            python3 scripts/make_quizzes.py 3 7        (some)
                            python3 scripts/make_quizzes.py --check    (validate only)

Question data (one file per lecture):
  {"lecture": 7, "questions": [{"id": "L07-q1", "page": "parasite-drag",
    "section": "Wetted area and form factor", "question": "...",
    "options": ["correct", "wrong", "wrong", "wrong"], "explanation": "..."}]}
options[0] is the correct answer; the widget shuffles the order. Strings are HTML
fragments with <i>, <sub>, <sup> and <strong> only. The script stops on a question whose
page or section heading does not exist, on a tag outside that list, and on a dash.
"""
import json
import re
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
DATA = BOOK / "scripts" / "quizzes"
OUT = BOOK / "quickcheck"
QUESTIONS = 8
ALLOWED_TAG = re.compile(r"</?(?:i|sub|sup|strong)>")


def lecture_titles():
    """Lecture number -> title, from the toc of myst.yml."""
    titles = {}
    for m in re.finditer(r'title:\s*"?Lecture (\d+): ([^"\n]+)"?', (BOOK / "myst.yml").read_text(encoding="utf-8")):
        titles[int(m.group(1))] = m.group(2).strip()
    return titles


def page_info(lecture, page):
    """Short title and the set of '## ' headings of a lecture page (.md or .ipynb)."""
    folder = BOOK / "notes" / f"lecture-{lecture:02d}"
    md = folder / f"{page}.md"
    nb = folder / f"{page}.ipynb"
    if md.exists():
        text = md.read_text(encoding="utf-8")
        front = re.match(r"---\n(.*?)\n---\n", text, re.S)
        title = None
        if front:
            for key in ("short_title", "title"):
                m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', front.group(1), re.M)
                if m:
                    title = m.group(1)
                    break
    elif nb.exists():
        cells = json.loads(nb.read_text(encoding="utf-8"))["cells"]
        text = "\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "markdown")
        m = re.search(r"^# (.+)$", text, re.M)
        title = m.group(1).strip() if m else None
    else:
        return None, set()
    headings = {h.strip() for h in re.findall(r"^## (.+)$", text, re.M)}
    return title, headings


def validate(data, lecture):
    errors, warnings = [], []
    qs = data.get("questions", [])
    if data.get("lecture") != lecture:
        errors.append(f'"lecture" is {data.get("lecture")}, expected {lecture}')
    if len(qs) != QUESTIONS:
        errors.append(f"{len(qs)} questions, expected {QUESTIONS}")
    ids = [q.get("id") for q in qs]
    if len(set(ids)) != len(ids):
        errors.append("duplicate question ids")
    longest = 0
    for q in qs:
        qid = q.get("id", "?")
        for key in ("id", "page", "section", "question", "options", "explanation"):
            if key not in q:
                errors.append(f"{qid}: missing {key}")
        if any(k not in q for k in ("page", "section", "question", "options", "explanation")):
            continue
        title, headings = page_info(lecture, q["page"])
        if title is None:
            errors.append(f'{qid}: page "{q["page"]}" not found in lecture-{lecture:02d}')
        elif q["section"] not in headings:
            errors.append(f'{qid}: no heading "## {q["section"]}" on page {q["page"]}')
        q["pageTitle"] = title or q["page"]
        opts = q["options"]
        if not (isinstance(opts, list) and len(opts) == 4):
            errors.append(f"{qid}: needs exactly four options")
            continue
        plain = [re.sub(r"\s+", " ", ALLOWED_TAG.sub("", o)).strip().lower() for o in opts]
        if len(set(plain)) != 4:
            errors.append(f"{qid}: two options read the same")
        for name, text in [("question", q["question"]), ("explanation", q["explanation"])] + \
                [(f"option {i + 1}", o) for i, o in enumerate(opts)]:
            rest = ALLOWED_TAG.sub("", text)
            if "<" in rest or ">" in rest:
                errors.append(f"{qid} {name}: tag or bare < > outside i, sub, sup, strong")
            if "—" in text or "–" in text:
                errors.append(f"{qid} {name}: em-dash or en-dash")
            if "\n" in text:
                errors.append(f"{qid} {name}: line break")
            if re.search(r"\b(all|none) of the above\b|\bboth [AaBb] and\b", rest, re.I):
                errors.append(f"{qid} {name}: refers to other options")
        if len(plain[0]) == max(len(p) for p in plain) and len(plain[0]) > 1.25 * sorted(len(p) for p in plain)[-2]:
            longest += 1
    if longest > 2:
        warnings.append(f"the correct option is clearly the longest in {longest} questions")
    return errors, warnings


def overbar(text):
    """A letter with a combining macron (x\u0304, c\u0304) becomes an overlined span: in the
    system italic font the combining mark is drawn beside the letter, not above it."""
    return re.sub("(\\w)\u0304", r'<span class="ov">\1</span>', text)


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  /* The color variables match the quick checks (quickcheck/*.html). Change them together. */
  :root {
    --bg: #ffffff; --fg: #1f2937; --muted: #4b5563; --card: #ffffff; --border: #d9d6ce;
    --head-bg: #f7f5f0; --head-fg: #111827; --accent: #6f5630; --accent-border: #cfb991;
    --input-bg: #ffffff; --input-border: #6b7280; --ok: #0a6b3d; --bad: #b42318;
    --button: #111827; --button-fg: #ffffff; --sol-bg: #f7f5f0;
    --link: #1d4ed8; --focus: #1d4ed8;
  }
  html.dark {
    --bg: #1c1917; --fg: #e5e7eb; --muted: #b7bcc6; --card: #292524; --border: #44403c;
    --head-bg: #363231; --head-fg: #ffffff; --accent: #cfb991; --accent-border: #cfb991;
    --input-bg: #1c1917; --input-border: #9ca3af; --ok: #6ee7b7; --bad: #fca5a5;
    --button: #cfb991; --button-fg: #000000; --sol-bg: #363231;
    --link: #93c5fd; --focus: #93c5fd;
  }
  html.dark { color-scheme: dark; }   /* native radio buttons drawn for a dark page */
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--fg);
         font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  .card { border: 1px solid var(--border); border-left: 5px solid var(--accent-border); border-radius: 8px;
          background: var(--card); overflow: hidden; }
  .head { background: var(--head-bg); color: var(--head-fg); padding: 10px 16px; font-weight: 700; font-size: 1.15em;
          display: flex; align-items: center; gap: 10px; }
  .head svg { width: 22px; height: 22px; flex: none; }
  .body { padding: 16px; }
  i { font-style: italic; }
  sub, sup { font-size: 0.75em; }
  .ov { text-decoration: overline; }
  .progress { margin: 0 0 6px; color: var(--muted); font-size: 0.95em; }
  .progress:focus { outline: none; }
  .bar { height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; margin: 0 0 14px; }
  .bar span { display: block; height: 100%; width: 0; background: var(--accent-border); }
  fieldset { border: 0; margin: 0; padding: 0; min-width: 0; }
  legend { padding: 0; margin: 0 0 4px; font-size: 1.08em; font-weight: 600; color: var(--head-fg); }
  .opt { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 4px 10px; padding: 10px 12px; margin: 8px 0 0;
         border: 1px solid var(--input-border); border-radius: 6px; background: var(--input-bg); cursor: pointer; }
  .opt input { flex: none; width: 1.05em; height: 1.05em; margin: 0.25em 0 0; accent-color: var(--button); }
  .opt .text { flex: 1 1 12em; }
  .opt .tag { flex: none; font-weight: 600; font-size: 0.92em; }
  .opt:hover { border-color: var(--fg); }
  .opt:has(input:checked) { border-color: var(--fg); box-shadow: inset 0 0 0 1px var(--fg); }
  .opt:has(input:focus-visible) { outline: 3px solid var(--focus); outline-offset: 1px; }
  .locked .opt { cursor: default; }
  .locked .opt:hover { border-color: var(--input-border); }
  .locked .opt.right, .locked .opt.right:hover { border-color: var(--ok); box-shadow: inset 0 0 0 1px var(--ok); }
  .locked .opt.wrong, .locked .opt.wrong:hover { border-color: var(--bad); box-shadow: inset 0 0 0 1px var(--bad); }
  .opt.right .tag { color: var(--ok); }
  .opt.wrong .tag { color: var(--bad); }
  .feedback { margin: 14px 0 0; }
  .feedback.show { border: 1px solid var(--border); border-left: 4px solid var(--accent-border); border-radius: 6px;
                   background: var(--sol-bg); padding: 10px 14px; }
  .verdict { font-weight: 700; }
  .verdict.ok { color: var(--ok); }
  .verdict.bad { color: var(--bad); }
  .buttons { display: flex; gap: 12px; margin: 16px 0 0; }
  button { font: inherit; font-weight: 600; padding: 9px 20px; border-radius: 6px; cursor: pointer; }
  button:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
  .primary { background: var(--button); color: var(--button-fg); border: 1px solid var(--button); }
  .score { margin: 0 0 8px; font-size: 1.15em; font-weight: 700; color: var(--head-fg); }
  .score:focus { outline: none; }
  .result p { margin: 8px 0; }
  .result ul { margin: 8px 0 0; padding-left: 1.3em; }
  .result li { margin: 4px 0; }
  a { color: var(--link); }
  a:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
  [hidden] { display: none !important; }
</style>
</head>
<body>
<div class="card">
  <div class="head">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4.5h6M9 10l1.5 1.5L13.5 8.5M9 16h6"/></svg>
    __TITLE__
  </div>
  <div class="body">
    <noscript><p>The quiz needs JavaScript.</p></noscript>
    <p class="progress" id="progress" tabindex="-1"></p>
    <div class="bar" aria-hidden="true"><span id="fill"></span></div>
    <form id="quiz" novalidate>
      <fieldset>
        <legend id="legend"></legend>
        <div id="opts"></div>
      </fieldset>
      <div class="feedback" id="feedback" role="status"></div>
      <div class="buttons">
        <button type="submit" class="primary" id="go">Check answer</button>
      </div>
    </form>
    <div class="result" id="result" hidden>
      <p class="score" id="score" tabindex="-1"></p>
      <p id="reviewIntro">Review these sections, then start over:</p>
      <ul id="review"></ul>
      <div class="buttons">
        <button type="button" class="primary" id="again">Start over</button>
      </div>
    </div>
  </div>
</div>
<script type="application/json" id="data">__DATA__</script>
<script>
(function () {
  function syncTheme() {
    var dark = false;
    try { dark = window.parent.document.documentElement.classList.contains("dark"); }
    catch (e) { dark = window.matchMedia("(prefers-color-scheme: dark)").matches; }
    document.documentElement.classList.toggle("dark", dark);
  }
  syncTheme();
  try { new MutationObserver(syncTheme).observe(window.parent.document.documentElement, { attributes: true }); } catch (e) {}
  function fit() {
    try {
      var fe = window.frameElement;
      if (fe && fe.parentElement) fe.parentElement.style.height = (Math.ceil(document.body.getBoundingClientRect().height) + 2) + "px";
    } catch (e) {}
  }
  try { new ResizeObserver(fit).observe(document.body); } catch (e) {}
  window.addEventListener("load", fit);

  var Q = JSON.parse(document.getElementById("data").textContent).questions;
  var n = Q.length, i = 0, answered = false, right = [];
  var el = {};
  ["progress", "fill", "quiz", "legend", "opts", "feedback", "go", "result", "score", "reviewIntro", "review", "again"]
    .forEach(function (id) { el[id] = document.getElementById(id); });

  function shuffle(a) {
    for (var j = a.length - 1; j > 0; j--) {
      var k = Math.floor(Math.random() * (j + 1)), t = a[j]; a[j] = a[k]; a[k] = t;
    }
    return a;
  }

  // Show question i. The options are drawn in a new order each time; option 0 is the correct one.
  function show(moveFocus) {
    var q = Q[i];
    answered = false;
    el.progress.textContent = "Question " + (i + 1) + " of " + n;
    el.fill.style.width = (100 * i / n) + "%";
    el.legend.innerHTML = q.question;
    el.opts.innerHTML = "";
    el.opts.className = "";
    shuffle([0, 1, 2, 3]).forEach(function (k) {
      var label = document.createElement("label"), input = document.createElement("input"),
          text = document.createElement("span"), tag = document.createElement("span");
      label.className = "opt";
      input.type = "radio"; input.name = "answer"; input.value = String(k);
      text.className = "text"; text.innerHTML = q.options[k];
      tag.className = "tag";
      label.appendChild(input); label.appendChild(text); label.appendChild(tag);
      el.opts.appendChild(label);
    });
    el.feedback.className = "feedback";
    el.feedback.textContent = "";
    el.go.textContent = "Check answer";
    el.result.hidden = true;
    el.quiz.hidden = false;
    if (moveFocus) el.progress.focus();
  }

  function check() {
    var chosen = el.quiz.querySelector("input[name=answer]:checked");
    if (!chosen) {
      el.feedback.className = "feedback show";
      el.feedback.textContent = "Choose an answer first.";
      return;
    }
    answered = true;
    right[i] = chosen.value === "0";
    Array.prototype.forEach.call(el.opts.querySelectorAll("label"), function (label) {
      var input = label.querySelector("input"), tag = label.querySelector(".tag");
      if (input.value === "0") { label.classList.add("right"); tag.textContent = "✓ correct answer"; }
      else if (input.checked) { label.classList.add("wrong"); tag.textContent = "✗ your answer"; }
      input.disabled = true;
    });
    el.opts.className = "locked";
    el.feedback.className = "feedback show";
    el.feedback.innerHTML = '<span class="verdict ' + (right[i] ? "ok" : "bad") + '">' +
      (right[i] ? "Correct." : "Not correct.") + "</span> " + Q[i].explanation;
    el.go.textContent = i + 1 < n ? "Next question" : "See your score";
    el.go.focus();
  }

  function finish() {
    var count = right.filter(Boolean).length;
    el.progress.textContent = "Result";
    el.fill.style.width = "100%";
    el.score.textContent = count === n ? "All " + n + " correct." : count + " of " + n + " correct.";
    el.review.innerHTML = "";
    el.reviewIntro.hidden = count === n;
    Q.forEach(function (q, j) {
      if (right[j]) return;
      var li = document.createElement("li"), a = document.createElement("a");
      a.href = "../" + q.page + "/"; a.target = "_top"; a.textContent = q.pageTitle;
      li.appendChild(document.createTextNode("Question " + (j + 1) + ": "));
      li.appendChild(a);
      li.appendChild(document.createTextNode(", section “" + q.section + "”"));
      el.review.appendChild(li);
    });
    el.quiz.hidden = true;
    el.result.hidden = false;
    el.score.focus();
  }

  el.quiz.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!answered) { check(); return; }
    i++;
    if (i < n) show(true); else finish();
  });
  el.again.addEventListener("click", function () { i = 0; right = []; show(true); });
  show(false);
})();
</script>
</body>
</html>
"""


def build(lecture, titles, write=True):
    src = DATA / f"lecture-{lecture:02d}.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    errors, warnings = validate(data, lecture)
    for w in warnings:
        print(f"lecture {lecture:02d}: warning: {w}")
    if errors:
        for e in errors:
            print(f"lecture {lecture:02d}: ERROR: {e}")
        return False
    if write:
        title = f"Quiz: Lecture {lecture}, {titles[lecture]}"
        payload = {"questions": [{"page": q["page"], "pageTitle": q["pageTitle"], "section": q["section"],
                                  "question": overbar(q["question"]), "options": [overbar(o) for o in q["options"]],
                                  "explanation": overbar(q["explanation"])} for q in data["questions"]]}
        # "</" would end the script element early; "\/" is a valid JSON escape.
        blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
        html = TEMPLATE.replace("__TITLE__", title).replace("__DATA__", blob)
        (OUT / f"quiz-lecture-{lecture:02d}.html").write_text(html, encoding="utf-8")
        print(f"lecture {lecture:02d}: wrote quickcheck/quiz-lecture-{lecture:02d}.html")
    else:
        print(f"lecture {lecture:02d}: ok")
    return True


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--check" not in sys.argv
    titles = lecture_titles()
    wanted = [int(a) for a in args] or sorted(int(p.stem.split("-")[1]) for p in DATA.glob("lecture-*.json"))
    ok = all([build(n, titles, write) for n in wanted])
    sys.exit(0 if ok else 1)
