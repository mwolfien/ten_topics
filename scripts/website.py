"""Static website for "Ten Topics for Medical Informatics".

Builds a self-contained site from data/topics.yaml and data/references.yaml:

  index.html                    overview, search and topic cards
  topics/<id>/index.html        one page per topic (+ index.md, references.bib)
  references/index.html         all references in one table
  data/                         machine-readable exports (CSL-JSON, BibTeX, topics JSON)
  llms.txt, llms-full.txt       entry points for LLMs (https://llmstxt.org)
  sitemap.xml, 404.html

Pages carry schema.org JSON-LD, canonical URLs and Open Graph metadata.
Internal links are relative, so the site also works when opened from disk.

Called via `python scripts/tentopics.py site`.
"""

import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "templates" / "site"

TITLE = "Ten Topics for Medical Informatics"
SUMMARY = ("A living, curated collection of key topics and in-depth literature to get started in "
           "Medical Informatics research, from privacy and interoperability standards (FHIR, OMOP) "
           "to data quality, clinical decision support and large language models.")
REPO = "https://github.com/mwolfien/ten_topics"
CONCEPT_DOI = "10.5281/zenodo.23047297"
ARTICLE_DOI = "10.2196/45948"
ARTICLE = ("Wolfien M, Ahmadi N, Fitzer K, Grummt S, Heine KL, Jung IC, Krefting D, Kühn A, Peng Y, "
           "Reinecke I, Scheel J, Schmidt T, Schmücker P, Schüttler C, Waltemath D, Zoch M, Sedlmayr M. "
           "Ten Topics to Get Started in Medical Informatics Research. J Med Internet Res 2023;25:e45948.")
AUTHORS = [("Markus", "Wolfien"), ("Julia", "Scheel")]
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
KEYWORDS = ["medical informatics", "health informatics", "privacy", "electronic health records",
            "data provenance", "FAIR", "federated learning", "ETL", "FHIR", "OMOP", "OHDSI",
            "data quality", "clinical decision support", "large language models", "visualization",
            "disease maps", "living review", "reading list"]

CITE = re.compile(r"\[@([a-z0-9-]+)\]")


# --------------------------------------------------------------------------- helpers

def esc(text):
    return html.escape(str(text), quote=True)


def ref_url(ref):
    return f"https://doi.org/{ref['doi']}" if "doi" in ref else ref["url"]


def plain(text, references):
    """Text with citations replaced by their labels (for descriptions and search)."""
    return CITE.sub(lambda m: references[m.group(1)]["label"], text)


def cited_ids(text):
    return CITE.findall(text)


def added_key(value):
    value = str(value)
    return value if "-" in value else f"{value}-00"


def all_topics(topics):
    for section in topics["sections"]:
        for topic in section["topics"]:
            yield section, topic


def topic_heading(topic):
    return f"Topic {topic['number']}: {topic['title']}" if topic.get("number") else topic["title"]


def topic_refs(topic):
    """Reference ids of a topic, in order of first citation."""
    seen = []
    for block in topic["body"]:
        texts = block["items"] if isinstance(block, dict) else [block]
        for text in texts:
            for rid in cited_ids(text):
                if rid not in seen:
                    seen.append(rid)
    return seen


def topic_description(topic, references):
    paragraphs = [b for b in topic["body"] if not isinstance(b, dict)]
    if paragraphs:
        text = plain(paragraphs[0], references)
        text = re.sub(r"\s*\([^()]*\d{4}[a-z]?\)", "", text)  # drop "(Author et al. 2020)"
    else:
        items = [i for b in topic["body"] if isinstance(b, dict) for i in b["items"]]
        text = f"Key literature on {topic['title']}: " + "; ".join(
            re.sub(r"\s*-\s*\[@.*$", "", i) for i in items[:3]) + "."
    return text.strip()


def first_author(label):
    """Split a label like "Meurers et al. 2021" into author names and an et-al flag."""
    names = re.sub(r",?\s*\d{4}[a-z]?$", "", label).strip()
    et_al = names.endswith("et al.")
    names = names[: -len("et al.")].strip() if et_al else names
    return [n.strip() for n in names.split(" and ") if n.strip()], et_al


# --------------------------------------------------------------------------- exports

def csl_item(rid, ref):
    item = {"id": rid, "type": {"article": "article-journal", "preprint": "article",
                                "book": "book", "resource": "webpage", "website": "webpage"}[ref["type"]]}
    item["title"] = ref.get("title", ref["label"])
    if ref.get("journal"):
        item["container-title"] = ref["journal"]
    if ref.get("year"):
        item["issued"] = {"date-parts": [[ref["year"]]]}
        names, et_al = first_author(ref["label"])
        item["author"] = [{"literal": n} if len(n.split()) > 2 else {"family": n} for n in names]
        if et_al:
            item["note"] = "First author only; see DOI for the full author list."
    if "doi" in ref:
        item["DOI"] = ref["doi"]
    item["URL"] = ref_url(ref)
    if ref.get("pmid"):
        item["PMID"] = str(ref["pmid"])
    return item


def bibtex_entry(rid, ref):
    kind = {"article": "article", "preprint": "misc", "book": "book",
            "resource": "misc", "website": "misc"}[ref["type"]]

    def val(text):
        return "{" + str(text).replace("{", "").replace("}", "") + "}"

    fields = [("title", "{" + val(ref.get("title", ref["label"])) + "}")]
    if ref.get("year"):
        names, et_al = first_author(ref["label"])
        names = ["{" + n + "}" if len(n.split()) > 2 else n for n in names]
        fields.append(("author", val(" and ".join(names + (["others"] if et_al else [])))))
        fields.append(("year", val(ref["year"])))
    if ref.get("journal"):
        fields.append(("journal", val(ref["journal"])))
    if "doi" in ref:
        fields.append(("doi", val(ref["doi"])))
    fields.append(("url", val(ref_url(ref))))
    if ref.get("pmid"):
        fields.append(("pmid", val(ref["pmid"])))
    body = ",\n".join(f"  {k} = {v}" for k, v in fields)
    return f"@{kind}{{{rid},\n{body}\n}}\n"


def bibtex(ids, references):
    return "\n".join(bibtex_entry(rid, references[rid]) for rid in ids)


# --------------------------------------------------------------------------- JSON-LD

def jsonld_article(ref):
    node = {"@type": "ScholarlyArticle" if ref["type"] in ("article", "preprint") else "CreativeWork",
            "name": ref.get("title", ref["label"]), "url": ref_url(ref)}
    if "doi" in ref:
        node["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": ref["doi"]}
    if ref.get("year"):
        node["datePublished"] = str(ref["year"])
    if ref.get("journal"):
        node["isPartOf"] = {"@type": "Periodical", "name": ref["journal"]}
    return node


def jsonld_dataset(base, today, topics):
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": TITLE,
        "description": SUMMARY,
        "url": base + "/",
        "sameAs": [REPO, f"https://doi.org/{CONCEPT_DOI}"],
        "identifier": f"https://doi.org/{CONCEPT_DOI}",
        "license": LICENSE_URL,
        "isAccessibleForFree": True,
        "inLanguage": "en",
        "keywords": KEYWORDS,
        "dateModified": today,
        "creator": [{"@type": "Person", "givenName": g, "familyName": f, "name": f"{g} {f}"}
                    for g, f in AUTHORS],
        "citation": {"@type": "ScholarlyArticle", "name": "Ten Topics to Get Started in Medical Informatics Research",
                     "identifier": f"https://doi.org/{ARTICLE_DOI}", "url": f"https://doi.org/{ARTICLE_DOI}"},
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/vnd.citationstyles.csl+json",
             "contentUrl": base + "/data/references.json"},
            {"@type": "DataDownload", "encodingFormat": "application/x-bibtex",
             "contentUrl": base + "/data/references.bib"},
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": base + "/data/topics.json"},
        ],
        "hasPart": [{"@type": "CollectionPage", "name": topic_heading(t), "url": f"{base}/topics/{t['id']}/"}
                    for _, t in all_topics(topics)],
    }


# --------------------------------------------------------------------------- HTML

def page(*, base, path, title, description, body, jsonld=None, alternate_md=None, current=None, extra_head="", lang="en"):
    """Render a full HTML page. `path` is the page's directory relative to the site root ("" or "topics/x/")."""
    root = "../" * path.count("/")
    canonical = f"{base}/{path}"
    full_title = title if title == TITLE else f"{title} – {TITLE}"

    def nav(href, label, key):
        cur = ' aria-current="page"' if key and key == current else ""
        return f'<li><a href="{root}{href}"{cur}>{label}</a></li>'

    head = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(full_title)}</title>",
        f'<meta name="description" content="{esc(description)}">',
        f'<link rel="canonical" href="{esc(canonical)}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{esc(TITLE)}">',
        f'<meta property="og:title" content="{esc(full_title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:url" content="{esc(canonical)}">',
        '<meta name="twitter:card" content="summary">',
        f'<link rel="stylesheet" href="{root}assets/style.css">',
        f'<link rel="alternate" type="text/plain" title="llms.txt" href="{root}llms.txt">',
    ]
    if alternate_md:
        head.append(f'<link rel="alternate" type="text/markdown" href="{alternate_md}">')
    if jsonld:
        data = json.dumps(jsonld, ensure_ascii=False, indent=1).replace("</", "<\\/")
        head.append(f'<script type="application/ld+json">\n{data}\n</script>')
    head.append(extra_head)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{chr(10).join(h for h in head if h)}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site">
  <div class="wrap">
    <a class="brand" href="{root}index.html">{esc(TITLE)}</a>
    <nav class="site" aria-label="Main">
      <ul>
        {nav("index.html#topics-heading", "Topics", "home")}
        {nav("references/index.html", "All references", "references")}
        {nav("learn/index.html", "Learn", "learn")}
        {nav("index.html#downloads", "Downloads", None)}
        {nav("index.html#cite", "How to cite", None)}
        <li><a href="{REPO}">GitHub</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main">
  <div class="wrap">
{body}
  </div>
</main>
<footer class="site">
  <div class="wrap">
    <p>Content licensed under <a href="{LICENSE_URL}">CC BY 4.0</a>. Cite as <a href="https://doi.org/{CONCEPT_DOI}">doi:{CONCEPT_DOI}</a> and <a href="https://doi.org/{ARTICLE_DOI}">Wolfien et al. 2023</a>.</p>
    <p>Suggestions welcome: <a href="{REPO}/issues/new?template=suggest-reference.yml">suggest a reference</a> · <a href="{REPO}/blob/main/CONTRIBUTING.md">contribute</a> · <a href="{root}llms.txt">llms.txt</a></p>
  </div>
</footer>
</body>
</html>
"""


def cite_html(references, new_ids, root):
    def cite(match):
        rid = match.group(1)
        ref = references[rid]
        title = f' title="{esc(ref["title"])}"' if ref.get("title") else ""
        badge = ' <span class="badge">new</span>' if rid in new_ids else ""
        return f'<a href="{esc(ref_url(ref))}"{title}>{esc(ref["label"])}</a>{badge}'

    return lambda text: CITE.sub(cite, esc(text))


def ref_line_html(ref, new):
    parts = [f'<a href="{esc(ref_url(ref))}">{esc(ref["label"])}</a>']
    if ref.get("title"):
        parts.append(f'<span class="title">{esc(ref["title"])}</span>')
    if ref.get("journal"):
        parts.append(f"<em>{esc(ref['journal'])}</em>")
    if "doi" in ref:
        parts.append(f'<span class="muted">doi:{esc(ref["doi"])}</span>')
    return ". ".join(parts) + (' <span class="badge">new</span>' if new else "")


# --------------------------------------------------------------------------- Markdown

def topic_markdown(topic, references, base):
    def cite(match):
        ref = references[match.group(1)]
        return f"[{ref['label']}]({ref_url(ref)})"

    out = [f"# {topic_heading(topic)}", ""]
    for block in topic["body"]:
        if isinstance(block, dict):
            out += [f"- {CITE.sub(cite, item)}" for item in block["items"]]
        else:
            out.append(CITE.sub(cite, block))
        out.append("")
    out += ["## References", ""]
    for rid in topic_refs(topic):
        ref = references[rid]
        line = f"- [{ref['label']}]({ref_url(ref)})"
        if ref.get("title"):
            line += f". {ref['title']}"
        if ref.get("journal"):
            line += f". *{ref['journal']}*"
        out.append(line)
    out += ["", f"Source: {TITLE}, {base}/topics/{topic['id']}/ (CC BY 4.0, doi:{CONCEPT_DOI})", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- build

def build(topics, references, out, base):
    base = base.rstrip("/")
    today = date.today().isoformat()
    latest = max((str(r["added"]) for r in references.values()), key=added_key)
    new_ids = {rid for rid, r in references.items() if str(r["added"]) == latest}
    topic_list = [t for _, t in all_topics(topics)]

    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    shutil.copy(ASSETS / "style.css", out / "assets" / "style.css")
    shutil.copy(ASSETS / "search.js", out / "assets" / "search.js")
    (out / ".nojekyll").write_text("")

    def write(rel, text):
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    # ---- data exports
    all_ids = list(references)
    write("data/references.json", json.dumps([csl_item(r, references[r]) for r in all_ids],
                                             ensure_ascii=False, indent=1) + "\n")
    write("data/references.bib", bibtex(all_ids, references))
    topics_json = {"title": TITLE, "doi": CONCEPT_DOI, "license": "CC-BY-4.0", "sections": []}
    for section in topics["sections"]:
        sec = {"title": section["title"], "topics": []}
        for t in section["topics"]:
            sec["topics"].append({
                "id": t["id"], "number": t.get("number"), "title": t["title"],
                "url": f"{base}/topics/{t['id']}/",
                "introduction": [plain(b, references) for b in t["body"] if not isinstance(b, dict)],
                "items": [{"text": plain(i, references), "references": cited_ids(i)}
                          for b in t["body"] if isinstance(b, dict) for i in b["items"]],
            })
        topics_json["sections"].append(sec)
    write("data/topics.json", json.dumps(topics_json, ensure_ascii=False, indent=1) + "\n")

    # ---- topic pages
    for n, topic in enumerate(topic_list):
        path = f"topics/{topic['id']}/"
        root = "../../"
        cite = cite_html(references, new_ids, root)
        refs = topic_refs(topic)
        desc = topic_description(topic, references)
        body = [f'<p class="eyebrow">{esc(next(s["title"] for s, t in all_topics(topics) if t is topic))}</p>',
                f"<h1>{esc(topic_heading(topic))}</h1>"]
        for block in topic["body"]:
            if isinstance(block, dict):
                body.append('<ul class="keywords">' +
                            "".join(f"<li>{cite(i)}</li>" for i in block["items"]) + "</ul>")
            else:
                body.append(f"<p>{cite(block)}</p>")
        body.append(f'<h2 id="references">References ({len(refs)})</h2>')
        body.append('<ol class="refs">' + "".join(
            f"<li>{ref_line_html(references[r], r in new_ids)}</li>" for r in refs) + "</ol>")
        body.append(f'<p class="muted">Download: <a href="references.bib">BibTeX</a> · '
                    f'<a href="index.md">Markdown</a> · '
                    f'<a href="{REPO}/issues/new?template=suggest-reference.yml">Suggest a reference</a></p>')
        prev_t = topic_list[n - 1] if n > 0 else None
        next_t = topic_list[n + 1] if n + 1 < len(topic_list) else None
        body.append('<nav class="pager" aria-label="Topics">' +
                    (f'<a href="{root}topics/{prev_t["id"]}/index.html" rel="prev">← {esc(topic_heading(prev_t))}</a>' if prev_t else "<span></span>") +
                    (f'<a href="{root}topics/{next_t["id"]}/index.html" rel="next">{esc(topic_heading(next_t))} →</a>' if next_t else "<span></span>") +
                    "</nav>")
        jsonld = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": topic_heading(topic),
            "description": desc,
            "url": f"{base}/{path}",
            "inLanguage": "en",
            "license": LICENSE_URL,
            "isPartOf": {"@type": "Dataset", "name": TITLE, "url": base + "/",
                         "identifier": f"https://doi.org/{CONCEPT_DOI}"},
            "mainEntity": {"@type": "ItemList", "numberOfItems": len(refs), "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": jsonld_article(references[r])}
                for i, r in enumerate(refs)]},
        }
        write(path + "index.html", page(base=base, path=path, title=topic_heading(topic), description=desc,
                                        body="\n".join(body), jsonld=jsonld, alternate_md="index.md"))
        write(path + "index.md", topic_markdown(topic, references, base))
        write(path + "references.bib", bibtex(refs, references))

    # ---- all references
    where = {}
    for topic in topic_list:
        for rid in topic_refs(topic):
            where.setdefault(rid, []).append(topic)
    rows = []
    for rid in sorted(references, key=lambda r: (-(references[r].get("year") or 0), references[r]["label"])):
        ref = references[rid]
        tlinks = ", ".join(f'<a href="../topics/{t["id"]}/index.html">{esc(topic_heading(t))}</a>'
                           for t in where.get(rid, []))
        title = esc(ref.get("title", ""))
        rows.append(f'<tr><td><a href="{esc(ref_url(ref))}">{esc(ref["label"])}</a>'
                    f'{" <span class=badge>new</span>" if rid in new_ids else ""}</td>'
                    f"<td>{title}{'<br><em>' + esc(ref['journal']) + '</em>' if ref.get('journal') else ''}</td>"
                    f"<td>{tlinks}</td></tr>")
    body = (f"<h1>All references</h1>\n<p class=\"lead\">{len(references)} references across "
            f"{len(topic_list)} topics, newest first. Download as "
            f'<a href="../data/references.bib">BibTeX</a> or <a href="../data/references.json">CSL-JSON</a>.</p>\n'
            '<div class="table-wrap"><table><thead><tr><th scope="col">Reference</th><th scope="col">Title</th>'
            '<th scope="col">Topic</th></tr></thead><tbody>\n' + "\n".join(rows) + "\n</tbody></table></div>")
    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "All references",
              "url": f"{base}/references/", "isPartOf": {"@type": "Dataset", "name": TITLE, "url": base + "/"},
              "mainEntity": {"@type": "ItemList", "numberOfItems": len(references), "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "item": jsonld_article(references[r])}
                  for i, r in enumerate(references)]}}
    write("references/index.html", page(base=base, path="references/", title="All references",
                                        description=f"All {len(references)} references of {TITLE}.",
                                        body=body, jsonld=jsonld, current="references"))

    # ---- home page with search
    search_items = []
    for topic in topic_list:
        for block in topic["body"]:
            if not isinstance(block, dict):
                continue
            for item in block["items"]:
                search_items.append({
                    "topic": topic_heading(topic), "topicId": topic["id"],
                    "topicUrl": f"topics/{topic['id']}/index.html",
                    "text": plain(item, references),
                    "refs": [{"label": references[r]["label"], "url": ref_url(references[r]),
                              "title": references[r].get("title"), "journal": references[r].get("journal"),
                              "year": references[r].get("year"), "isNew": r in new_ids}
                             for r in cited_ids(item)],
                })
    index_json = json.dumps({"items": search_items}, ensure_ascii=False).replace("</", "<\\/")
    options = "".join(f'<option value="{esc(t["id"])}">{esc(topic_heading(t))}</option>' for t in topic_list)
    cards = []
    for section in topics["sections"]:
        cards.append(f'<h3 class="section-title">{esc(section["title"])}</h3>\n<ul class="grid">')
        for t in section["topics"]:
            refs = topic_refs(t)
            n_new = sum(1 for r in refs if r in new_ids)
            desc = topic_description(t, references)
            short = desc if len(desc) < 170 else desc[:167].rsplit(" ", 1)[0] + "…"
            cards.append(f'<li class="card"><h3><a href="topics/{esc(t["id"])}/index.html">{esc(topic_heading(t))}</a></h3>'
                         f"<p>{esc(short)}</p><span class=\"meta\">{len(refs)} references"
                         f"{f' · <span class=badge>{n_new} new</span>' if n_new else ''}</span></li>")
        cards.append("</ul>")
    body = f"""<h1>{esc(TITLE)}</h1>
<p class="lead">{esc(SUMMARY)}</p>
<p>The collection extends the viewpoint article <a href="https://doi.org/{ARTICLE_DOI}">“Ten Topics to Get Started in Medical Informatics Research”</a> (J Med Internet Res 2023). It is curated by researchers and updated regularly: {len(references)} references, last update {esc(latest)}.</p>

<form class="search" id="search" role="search" aria-label="Search the collection">
  <div class="search-controls">
    <input type="search" id="q" name="q" placeholder="Search keywords, titles, journals… e.g. FHIR, federated, LLM" aria-label="Search keywords, titles and journals">
    <select id="topic" aria-label="Filter by topic"><option value="">All topics</option>{options}</select>
    <label class="check"><input type="checkbox" id="new-only"> New in {esc(latest)}</label>
  </div>
  <p id="search-status" class="muted" aria-live="polite"></p>
  <ul id="results" class="results"></ul>
</form>

<div id="topics">
<h2 id="topics-heading">Topics</h2>
{chr(10).join(cards)}
</div>

<h2 id="downloads">Downloads</h2>
<ul>
  <li><a href="data/references.bib">All references as BibTeX</a> (for Zotero, JabRef, LaTeX); each topic page also offers its own BibTeX file</li>
  <li><a href="data/references.json">All references as CSL-JSON</a></li>
  <li><a href="data/topics.json">Topics and keyword items as JSON</a></li>
  <li><a href="llms-full.txt">The whole collection as Markdown</a></li>
</ul>

<h2 id="cite">How to cite</h2>
<div class="callout">
  <p>Please cite the original article:</p>
  <p>{esc(ARTICLE)} <a href="https://doi.org/{ARTICLE_DOI}">doi:{ARTICLE_DOI}</a></p>
  <p>To cite the living collection: Wolfien M, Scheel J. {esc(TITLE)} [Data set]. Zenodo. <a href="https://doi.org/{CONCEPT_DOI}">doi:{CONCEPT_DOI}</a></p>
</div>

<h2>Contribute</h2>
<p>Know a paper that belongs here? <a href="{REPO}/issues/new?template=suggest-reference.yml">Suggest a reference</a> or <a href="{REPO}/issues/new?template=propose-topic.yml">propose a topic</a>. The inclusion criteria are described in the <a href="{REPO}/blob/main/CONTRIBUTING.md">contribution guidelines</a>.</p>
"""
    extra_head = f'<script type="application/json" id="search-index">{index_json}</script>\n<script src="assets/search.js" defer></script>'
    write("index.html", page(base=base, path="", title=TITLE, description=SUMMARY, body=body,
                             jsonld=jsonld_dataset(base, today, topics), current="home", extra_head=extra_head))

    # ---- 404
    write("404.html", page(base=base, path="", title="Page not found", description="Page not found.",
                           body='<h1>Page not found</h1><p>Go to the <a href="index.html">overview of all topics</a>.</p>'))

    # ---- llms.txt and llms-full.txt
    lines = [f"# {TITLE}", "", f"> {SUMMARY}", "",
             f"Curated by researchers, extending the article \"Ten Topics to Get Started in Medical Informatics "
             f"Research\" (J Med Internet Res 2023;25:e45948, https://doi.org/{ARTICLE_DOI}). "
             f"{len(references)} references, last update {latest}. License: CC BY 4.0. "
             f"Cite as https://doi.org/{CONCEPT_DOI}.", ""]
    for section in topics["sections"]:
        lines += [f"## {section['title']}", ""]
        for t in section["topics"]:
            lines.append(f"- [{topic_heading(t)}]({base}/topics/{t['id']}/index.md): "
                         f"{topic_description(t, references)}")
        lines.append("")
    lines += ["## Data", "",
              f"- [All references (CSL-JSON)]({base}/data/references.json): titles, journals, years, DOIs",
              f"- [All references (BibTeX)]({base}/data/references.bib)",
              f"- [Topics and keyword items (JSON)]({base}/data/topics.json)", "",
              "## Learning modules", "",
              f"- [Interactive learning modules (German and English)]({base}/learn/): lessons with quizzes and exercises", "",
              "## Optional", "",
              f"- [Full collection as one Markdown file]({base}/llms-full.txt)",
              f"- [Source repository]({REPO})", ""]
    write("llms.txt", "\n".join(lines))
    full = [f"# {TITLE}", "", SUMMARY, "", f"License: CC BY 4.0. Cite as https://doi.org/{CONCEPT_DOI}.", ""]
    for t in topic_list:  # demote headings by one level below the collection title
        full.append(re.sub(r"^(#+) ", r"#\1 ", topic_markdown(t, references, base), flags=re.M))
    write("llms-full.txt", "\n".join(full))

    # ---- learning modules
    import learn
    shutil.copy(ASSETS / "learn.js", out / "assets" / "learn.js")
    learn_urls = learn.build(write, page, learn.load_modules(), references, ref_url,
                             {t["id"]: topic_heading(t) for t in topic_list}, base)

    # ---- sitemap
    urls = [f"{base}/", f"{base}/references/"] + [f"{base}/topics/{t['id']}/" for t in topic_list] + learn_urls
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{esc(u)}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) +
          "</urlset>\n")

    return check_internal_links(out)


def check_internal_links(out):
    """Return a list of relative href/src targets that do not exist in the built site."""
    broken = []
    for page_file in out.rglob("*.html"):
        text = page_file.read_text(encoding="utf-8")
        for target in re.findall(r'(?:href|src)="([^"]+)"', text):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#")[0].split("?")[0]
            if not path:
                continue
            resolved = (page_file.parent / path).resolve()
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.exists():
                broken.append(f"{page_file.relative_to(out)} -> {target}")
    return broken
