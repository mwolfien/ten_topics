"""Interactive learning modules for "Ten Topics for Medical Informatics".

A module is a folder learn/<module-id>/ with one Markdown file per language
(de.md, en.md). Each file starts with a YAML front matter block and uses a few
fenced blocks for interactive elements (see learn/README.md):

  ```quiz      one question, answer chosen from a dropdown, instant feedback
  ```match     several items, each matched to an option from a dropdown
  ```reflect   open question with a hidden sample answer
  ```persona   "Why this matters for you" box for one audience
  ```timeline  a vertical timeline
  ```include   inline an SVG file from the module folder (theme-aware)

References are cited with [@id] (ids from data/references.yaml), as in topics.yaml.
Everything runs in the browser; nothing is stored on a server.
"""

import html
import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "learn"
CITE = re.compile(r"\[@([a-z0-9-]+)\]")
FENCE = re.compile(r"^```(quiz|match|reflect|persona|timeline|include)[ \t]*([^\n]*)\n(.*?)^```[ \t]*$", re.M | re.S)
BLOCK_TYPES = {"quiz", "match", "reflect", "persona", "timeline", "include"}

AUDIENCES = {
    "med": {"de": "Medizinstudierende", "en": "Medical students"},
    "cs": {"de": "Informatikstudierende", "en": "Computer science students"},
    "clin": {"de": "Ärzt:innen & Pflege", "en": "Clinicians & nurses"},
    "tech": {"de": "Informatiker:innen", "en": "Computer scientists"},
    "pat": {"de": "Patient:innen & Interessierte", "en": "Patients & the public"},
}

UI = {
    "de": {
        "choose": "– Antwort wählen –", "correct": "Richtig!", "wrong": "Noch nicht ganz.",
        "check": "Prüfen", "reveal": "Mögliche Antworten anzeigen", "your_notes": "Ihre Gedanken (werden nicht gespeichert)",
        "persona_label": "Ich bin …", "persona_all": "alle Perspektiven anzeigen", "why": "Warum das für Sie relevant ist",
        "score": "Richtig beantwortet", "objectives": "Lernziele", "duration": "Dauer", "level": "Niveau",
        "readings": "Weiterlesen", "related": "Passende Themen der Sammlung", "source": "Grundlage",
        "other_lang": "English version", "modules": "Lernmodule", "all_modules": "Alle Lernmodule",
        "matched": "von", "reset": "Zurücksetzen", "learn_nav": "Lernen",
        "intro": "Interaktive Lernmodule zu den Themen der Sammlung – mit kurzen Quizfragen, Übungen und Reflexionsfragen. Ohne Anmeldung, nichts wird gespeichert.",
    },
    "en": {
        "choose": "– choose an answer –", "correct": "Correct!", "wrong": "Not quite.",
        "check": "Check", "reveal": "Show possible answers", "your_notes": "Your thoughts (not stored)",
        "persona_label": "I am …", "persona_all": "show all perspectives", "why": "Why this matters for you",
        "score": "Answered correctly", "objectives": "Learning objectives", "duration": "Duration", "level": "Level",
        "readings": "Further reading", "related": "Related topics in the collection", "source": "Based on",
        "other_lang": "Deutsche Version", "modules": "Learning modules", "all_modules": "All learning modules",
        "matched": "of", "reset": "Reset", "learn_nav": "Learn",
        "intro": "Interactive learning modules on the topics of the collection – with short quizzes, exercises and reflection questions. No login, nothing is stored.",
    },
}


def esc(text):
    return html.escape(str(text), quote=True)


def load_modules():
    """Return {module_id: {lang: module}} for all modules in learn/."""
    modules = {}
    for path in sorted(LEARN.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            raise ValueError(f"{path}: missing YAML front matter")
        meta = yaml.safe_load(m.group(1))
        meta["body"] = m.group(2)
        meta["path"] = path
        meta.setdefault("id", path.parent.name)
        meta.setdefault("lang", path.stem)
        modules.setdefault(meta["id"], {})[meta["lang"]] = meta
    return modules


def blocks(module):
    """Yield (kind, arg, parsed_yaml_or_text) for each interactive block."""
    for m in FENCE.finditer(module["body"]):
        kind, arg, content = m.group(1), m.group(2).strip(), m.group(3)
        if kind in ("persona", "include"):
            yield kind, arg, content
        else:
            yield kind, arg, yaml.safe_load(content)


def validate(modules, references, topic_ids):
    errors = []
    for mid, langs in modules.items():
        for lang, mod in langs.items():
            where = f"learn/{mid}/{lang}.md"
            if lang not in UI:
                errors.append(f"{where}: unsupported language {lang!r}")
            for field in ("title", "summary", "objectives", "duration_minutes", "level", "audiences"):
                if field not in mod:
                    errors.append(f"{where}: missing front matter field {field!r}")
            for a in mod.get("audiences", []):
                if a not in AUDIENCES:
                    errors.append(f"{where}: unknown audience {a!r} (use {sorted(AUDIENCES)})")
            for rid in CITE.findall(mod["body"]) + list(mod.get("readings", [])):
                if rid not in references:
                    errors.append(f"{where}: unknown reference {rid!r}")
            for tid in mod.get("related_topics", []):
                if tid not in topic_ids:
                    errors.append(f"{where}: unknown topic id {tid!r}")
            try:
                for kind, arg, data in blocks(mod):
                    if kind == "quiz":
                        if not isinstance(data, dict) or data.get("answer") not in data.get("options", []):
                            errors.append(f"{where}: quiz {str(data)[:40]!r}: `answer` must be one of `options`")
                    elif kind == "match":
                        opts = data.get("options", []) if isinstance(data, dict) else []
                        for row in (data or {}).get("items", []):
                            if row.get("answer") not in opts:
                                errors.append(f"{where}: match item {row.get('item')!r}: answer not in options")
                    elif kind == "persona" and arg not in AUDIENCES:
                        errors.append(f"{where}: persona block for unknown audience {arg!r}")
                    elif kind == "include" and not (mod["path"].parent / arg).exists():
                        errors.append(f"{where}: include file {arg!r} not found")
            except yaml.YAMLError as e:
                errors.append(f"{where}: invalid YAML in a block: {e}")
        if len(langs) > 1 and len({tuple(sorted(m.get("audiences", []))) for m in langs.values()}) > 1:
            errors.append(f"learn/{mid}: languages list different audiences")
    return errors


def cited(modules):
    ids = set()
    for langs in modules.values():
        for mod in langs.values():
            ids |= set(CITE.findall(mod["body"])) | set(mod.get("readings", []))
    return ids


# --------------------------------------------------------------------------- rendering

def _md(text, cite):
    html_out = markdown.markdown(text, extensions=["tables", "sane_lists"])
    return cite(html_out)


def render_body(mod, references, ref_url):
    lang = mod["lang"]
    ui = UI[lang]
    counter = {"n": 0}

    def cite(text):
        def one(m):
            ref = references[m.group(1)]
            return f'<a href="{esc(ref_url(ref))}">{esc(ref["label"])}</a>'
        return CITE.sub(one, text)

    def uid():
        counter["n"] += 1
        return f"{mod['id']}-{lang}-{counter['n']}"

    def inline(text):
        return cite(markdown.markdown(str(text)).removeprefix("<p>").removesuffix("</p>"))

    def render_block(kind, arg, data):
        if kind == "quiz":
            i = uid()
            opts = "".join(f'<option value="{esc(o)}">{esc(o)}</option>' for o in data["options"])
            return (f'<div class="quiz" data-kind="quiz" data-answer="{esc(data["answer"])}">'
                    f'<label for="{i}" class="q">{inline(data["question"])}</label>'
                    f'<select id="{i}"><option value="">{esc(ui["choose"])}</option>{opts}</select>'
                    f'<p class="feedback" aria-live="polite" hidden></p>'
                    f'<div class="explain" hidden>{inline(data.get("explain", ""))}</div></div>')
        if kind == "match":
            rows = []
            for row in data["items"]:
                i = uid()
                opts = "".join(f'<option value="{esc(o)}">{esc(o)}</option>' for o in data["options"])
                rows.append(f'<tr data-answer="{esc(row["answer"])}"><td><label for="{i}">{inline(row["item"])}</label></td>'
                            f'<td><select id="{i}"><option value="">{esc(ui["choose"])}</option>{opts}</select>'
                            f'<span class="mark" aria-hidden="true"></span></td></tr>')
            return (f'<div class="quiz match" data-kind="match">'
                    f'<p class="q">{inline(data["question"])}</p>'
                    f'<div class="table-wrap"><table><tbody>{"".join(rows)}</tbody></table></div>'
                    f'<p class="feedback" aria-live="polite" hidden></p>'
                    f'<div class="explain" hidden>{inline(data.get("explain", ""))}</div></div>')
        if kind == "reflect":
            i = uid()
            answers = "".join(f"<li>{inline(a)}</li>" for a in data.get("answers", []))
            return (f'<div class="reflect"><label for="{i}" class="q">💬 {inline(data["question"])}</label>'
                    f'<textarea id="{i}" rows="3" placeholder="{esc(ui["your_notes"])}"></textarea>'
                    f'<details><summary>{esc(ui["reveal"])}</summary>'
                    f'{"<p>" + inline(data["intro"]) + "</p>" if data.get("intro") else ""}<ul>{answers}</ul></details></div>')
        if kind == "persona":
            name = AUDIENCES[arg][lang]
            return (f'<aside class="persona" data-persona="{esc(arg)}"><p class="persona-name">{esc(name)}</p>'
                    f'{_md(data, cite)}</aside>')
        if kind == "timeline":
            items = "".join(f'<li><span class="when">{esc(e["when"])}</span><span class="what">{inline(e["what"])}</span></li>'
                            for e in data["events"])
            title = f'<p class="q">{inline(data["title"])}</p>' if data.get("title") else ""
            if data.get("collapsed"):  # e.g. the solution of a preceding exercise
                return (f'<details class="timeline"><summary>{inline(data["collapsed"])}</summary>'
                        f'{title}<ol>{items}</ol></details>')
            return f'<div class="timeline">{title}<ol>{items}</ol></div>'
        if kind == "include":
            svg = (mod["path"].parent / arg).read_text(encoding="utf-8")
            return f'<figure class="diagram">{svg}</figure>'
        raise ValueError(kind)

    # Replace blocks by placeholders, render Markdown, then put the HTML back.
    parts = {}

    def stash(m):
        kind, arg, content = m.group(1), m.group(2).strip(), m.group(3)
        data = content if kind in ("persona", "include") else yaml.safe_load(content)
        key = f"BLOCK{len(parts)}X"
        parts[key] = render_block(kind, arg, data)
        return f"\n\n{key}\n\n"

    body = FENCE.sub(stash, mod["body"])
    out = _md(body, cite)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    for key, value in parts.items():
        out = out.replace(f"<p>{key}</p>", value)
    # Group persona boxes that follow each other into one strip.
    out = re.sub(r"((?:<aside class=\"persona\".*?</aside>\s*){2,})",
                 lambda m: f'<div class="personas">{m.group(1)}</div>', out, flags=re.S)
    return out


def module_jsonld(mod, base, url, other_url, references, ref_url):
    lang = mod["lang"]
    node = {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": mod["title"],
        "description": mod["summary"],
        "url": url,
        "inLanguage": lang,
        "learningResourceType": ["lesson", "quiz"],
        "educationalLevel": mod["level"],
        "timeRequired": f"PT{int(mod['duration_minutes'])}M",
        "teaches": mod["objectives"],
        "audience": [{"@type": "EducationalAudience", "educationalRole": AUDIENCES[a]["en"]} for a in mod["audiences"]],
        "isAccessibleForFree": True,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "isPartOf": {"@type": "Dataset", "name": "Ten Topics for Medical Informatics", "url": base + "/"},
        "citation": [{"@type": "CreativeWork", "name": references[r].get("title", references[r]["label"]),
                      "url": ref_url(references[r])} for r in mod.get("readings", [])],
    }
    if mod.get("author"):
        node["author"] = {"@type": "Person", "name": mod["author"]}
    if other_url:
        node["workTranslation" if lang == "de" else "translationOfWork"] = {"@type": "LearningResource", "url": other_url}
    return node


def module_html(mod, references, ref_url, topic_lookup, root, other=None, other_link=None):
    """The complete, self-contained HTML of one module in one language (an <article class="module">)."""
    lang, mid, ui = mod["lang"], mod["id"], UI[mod["lang"]]
    pick = f"persona-{mid}-{lang}"
    body = [
        f'<article class="module" lang="{lang}" data-correct="{esc(ui["correct"])}" data-wrong="{esc(ui["wrong"])}">',
        f'<p class="eyebrow"><a href="{root}learn/index.html#{lang}">{esc(ui["modules"])}</a></p>',
        f'<h1>{esc(mod["title"])}</h1>',
        f'<p class="lead">{esc(mod["summary"])}</p>',
        '<div class="module-meta">'
        f'<span>⏱ {esc(ui["duration"])}: {int(mod["duration_minutes"])} min</span>'
        f'<span>📶 {esc(ui["level"])}: {esc(mod["level"])}</span>'
        + (f'<a class="other-lang" hreflang="{other}" lang="{other}" href="{other_link}">🌐 {esc(ui["other_lang"])}</a>' if other else "")
        + "</div>",
        '<div class="persona-picker" hidden>'
        f'<label for="{pick}">{esc(ui["persona_label"])}</label>'
        f'<select id="{pick}"><option value="">{esc(ui["persona_all"])}</option>'
        + "".join(f'<option value="{a}">{esc(AUDIENCES[a][lang])}</option>' for a in mod["audiences"])
        + "</select></div>",
        f'<div class="callout"><p><strong>{esc(ui["objectives"])}</strong></p><ul>'
        + "".join(f"<li>{esc(o)}</li>" for o in mod["objectives"]) + "</ul></div>",
        render_body(mod, references, ref_url),
    ]
    if mod.get("readings"):
        body.append(f'<h2>{esc(ui["readings"])}</h2><ul class="refs">')
        for rid in mod["readings"]:
            ref = references[rid]
            title = f". {esc(ref['title'])}" if ref.get("title") else ""
            journal = f". <em>{esc(ref['journal'])}</em>" if ref.get("journal") else ""
            body.append(f'<li><a href="{esc(ref_url(ref))}">{esc(ref["label"])}</a>{title}{journal}</li>')
        body.append("</ul>")
    if mod.get("related_topics"):
        body.append(f'<p>{esc(ui["related"])}: ' + " · ".join(
            f'<a href="{root}topics/{t}/index.html">{esc(topic_lookup[t])}</a>' for t in mod["related_topics"]) + "</p>")
    if mod.get("source"):
        body.append(f'<p class="muted">{esc(ui["source"])}: {esc(mod["source"])}</p>')
    body.append(f'<div class="scorebar" hidden><span>{esc(ui["score"])}: <strong class="score">0</strong> '
                f'{esc(ui["matched"])} <span class="total">0</span></span>'
                f'<button type="button" class="reset">{esc(ui["reset"])}</button></div>')
    body.append("</article>")
    return "\n".join(body)


def build(write, page, modules, references, ref_url, topic_lookup, base):
    """Write learn/ pages via the site's `write` and `page` helpers. Returns sitemap URLs."""
    urls = []
    cards = {"de": [], "en": []}
    for mid, langs in sorted(modules.items()):
        for lang, mod in langs.items():
            path = f"learn/{mid}/{lang}/"
            root = "../../../"
            other = next((l for l in langs if l != lang), None)
            other_url = f"{base}/learn/{mid}/{other}/" if other else None
            other_link = f"{root}learn/{mid}/{other}/index.html" if other else None
            body = [module_html(mod, references, ref_url, topic_lookup, root, other, other_link)]
            alt = f'<link rel="alternate" hreflang="{lang}" href="{base}/{path}">'
            if other:
                alt += f'\n<link rel="alternate" hreflang="{other}" href="{other_url}">'
            extra = alt + f'\n<script src="{root}assets/learn.js" defer></script>'
            write(path + "index.html", page(
                base=base, path=path, title=mod["title"], description=mod["summary"], body="\n".join(body),
                jsonld=module_jsonld(mod, base, f"{base}/{path}", other_url, references, ref_url),
                current="learn", extra_head=extra, lang=lang))
            urls.append(f"{base}/{path}")
            cards[lang].append(
                f'<li class="card"><h3><a href="{mid}/{lang}/index.html" hreflang="{lang}">{esc(mod["title"])}</a></h3>'
                f'<p>{esc(mod["summary"])}</p><span class="meta">{int(mod["duration_minutes"])} min · {esc(mod["level"])}</span></li>')

    sections = []
    for lang, heading in (("de", "Deutsch"), ("en", "English")):
        if cards[lang]:
            sections.append(f'<section lang="{lang}"><h2 id="{lang}">{heading}</h2>'
                            f'<p class="muted">{esc(UI[lang]["intro"])}</p><ul class="grid">{"".join(cards[lang])}</ul></section>')
    write("learn/index.html", page(
        base=base, path="learn/", title="Learning modules / Lernmodule",
        description="Interactive, bilingual learning modules on medical informatics with quizzes and exercises.",
        body="<h1>Learning modules · Lernmodule</h1>\n" + "\n".join(sections), current="learn"))
    urls.append(f"{base}/learn/")
    return urls
