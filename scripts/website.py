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

SUMMARY_DE = ("Eine lebendige, kuratierte Sammlung zentraler Themen und weiterführender Literatur für den Einstieg in die "
              "Forschung der Medizinischen Informatik – von Datenschutz und Interoperabilitätsstandards (FHIR, OMOP) bis "
              "zu Datenqualität, klinischer Entscheidungsunterstützung und großen Sprachmodellen.")

# Interface texts of the site frame and the start page. Topic content stays in English.
UI = {
    "en": {
        "home": "index.html", "skip": "Skip to content", "nav_label": "Main", "topics": "Topics",
        "references": "All references", "learn": "Learn", "learn_href": "learn/index.html#en", "downloads": "Downloads",
        "cite": "How to cite", "switch": "Deutsch", "switch_lang": "de",
        "footer_license": "Content licensed under", "footer_cite": "Cite as", "and": "and",
        "footer_suggest": "Suggestions welcome", "suggest": "suggest a reference", "contribute": "contribute",
        "search_label": "Search the collection", "search_placeholder": "Search keywords, titles, journals… e.g. FHIR, federated, LLM",
        "search_aria": "Search keywords, titles and journals", "filter": "Filter by topic", "all_topics": "All topics",
        "new_in": "New in", "result_one": "1 result", "result_many": "{n} results",
        "n_refs": "references", "n_new": "new",
    },
    "de": {
        "home": "de/index.html", "skip": "Zum Inhalt springen", "nav_label": "Hauptmenü", "topics": "Themen",
        "references": "Alle Referenzen", "learn": "Lernen", "learn_href": "learn/index.html#de", "downloads": "Downloads",
        "cite": "Zitieren", "switch": "English", "switch_lang": "en",
        "footer_license": "Inhalte lizenziert unter", "footer_cite": "Zitieren als", "and": "und",
        "footer_suggest": "Vorschläge willkommen", "suggest": "Referenz vorschlagen", "contribute": "mitmachen",
        "search_label": "Sammlung durchsuchen", "search_placeholder": "Englische Stichworte suchen … z. B. FHIR, federated, LLM",
        "search_aria": "Stichworte, Titel und Zeitschriften durchsuchen", "filter": "Nach Thema filtern", "all_topics": "Alle Themen",
        "new_in": "Neu in", "result_one": "1 Treffer", "result_many": "{n} Treffer",
        "n_refs": "Referenzen", "n_new": "neu",
    },
}


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

def page(*, base, path, title, description, body, jsonld=None, alternate_md=None, current=None, extra_head="",
         lang="en", translation=None):
    """Render a full HTML page. `path` is the page's directory relative to the site root ("" or "topics/x/").

    `lang` selects the interface language. `translation` is the path (relative to the site root) of the same
    page in the other language; without it, the language switch leads to the other language's start page.
    """
    ui = UI[lang]
    other = ui["switch_lang"]
    switch_href = translation or UI[other]["home"]
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
    if translation:  # a real counterpart: tell search engines about both language versions
        other_path = translation.removesuffix("index.html")
        head.append(f'<link rel="alternate" hreflang="{lang}" href="{esc(canonical)}">')
        head.append(f'<link rel="alternate" hreflang="{other}" href="{esc(base)}/{esc(other_path)}">')
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
<a class="skip-link" href="#main">{ui["skip"]}</a>
<header class="site">
  <div class="wrap">
    <a class="brand" href="{root}{ui["home"]}">{esc(TITLE)}</a>
    <nav class="site" aria-label="{ui["nav_label"]}">
      <ul>
        {nav(ui["home"] + "#topics-heading", ui["topics"], "home")}
        {nav("references/index.html", ui["references"], "references")}
        {nav(ui["learn_href"], ui["learn"], "learn")}
        {nav(ui["home"] + "#downloads", ui["downloads"], None)}
        {nav(ui["home"] + "#cite", ui["cite"], None)}
        <li><a href="{REPO}">GitHub</a></li>
        <li><a class="lang-link" href="{root}{switch_href}" hreflang="{other}" lang="{other}">🌐 {ui["switch"]}</a></li>
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
    <p>{ui["footer_license"]} <a href="{LICENSE_URL}">CC BY 4.0</a>. {ui["footer_cite"]} <a href="https://doi.org/{CONCEPT_DOI}">doi:{CONCEPT_DOI}</a> {ui["and"]} <a href="https://doi.org/{ARTICLE_DOI}">Wolfien et al. 2023</a>.</p>
    <p>{ui["footer_suggest"]}: <a href="{REPO}/issues/new?template=suggest-reference.yml">{ui["suggest"]}</a> · <a href="{REPO}/blob/main/CONTRIBUTING.md">{ui["contribute"]}</a> · <a href="{root}llms.txt">llms.txt</a></p>
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

def home_page(lang, topics, topic_list, references, new_ids, latest, index_json, root):
    """Body and extra head of the start page in one language."""
    ui = UI[lang]
    de = lang == "de"
    options = "".join(f'<option value="{esc(t["id"])}">{esc(topic_heading(t))}</option>' for t in topic_list)
    cards = []
    for section in topics["sections"]:
        cards.append(f'<h3 class="section-title" lang="en">{esc(section["title"])}</h3>\n<ul class="grid">')
        for t in section["topics"]:
            refs = topic_refs(t)
            n_new = sum(1 for r in refs if r in new_ids)
            desc = topic_description(t, references)
            short = desc if len(desc) < 170 else desc[:167].rsplit(" ", 1)[0] + "…"
            badge = f' · <span class=badge>{n_new} {ui["n_new"]}</span>' if n_new else ""
            cards.append(f'<li class="card" lang="en"><h3><a href="{root}topics/{esc(t["id"])}/index.html">{esc(topic_heading(t))}</a></h3>'
                         f'<p>{esc(short)}</p><span class="meta" lang="{lang}">{len(refs)} {ui["n_refs"]}{badge}</span></li>')
        cards.append("</ul>")
    article = f'<a href="https://doi.org/{ARTICLE_DOI}">“Ten Topics to Get Started in Medical Informatics Research”</a>'
    if de:
        intro = (f"<p>Die Sammlung erweitert den Übersichtsartikel {article} (J Med Internet Res 2023). Sie wird von "
                 f"Forschenden kuratiert und regelmäßig aktualisiert: {len(references)} Referenzen, letzte Aktualisierung {esc(latest)}.</p>\n"
                 f'<div class="callout"><p><strong>Neu: Lernmodule.</strong> Interaktive Einheiten auf Deutsch und Englisch mit '
                 f'Quizfragen und Übungen, z. B. zur <a href="{root}learn/history/de/index.html">Geschichte der Medizinischen '
                 f'Informatik</a>. <a href="{root}learn/index.html#de">Alle Lernmodule</a></p></div>\n'
                 '<p class="muted">Die Themen und Literaturangaben der Sammlung sind englischsprachig, wie die Literatur selbst.</p>')
        downloads = f"""<ul>
  <li><a href="{root}data/references.bib">Alle Referenzen als BibTeX</a> (für Zotero, JabRef, LaTeX); jede Themenseite bietet zusätzlich eine eigene BibTeX-Datei</li>
  <li><a href="{root}data/references.json">Alle Referenzen als CSL-JSON</a></li>
  <li><a href="{root}data/topics.json">Themen und Stichpunkte als JSON</a></li>
  <li><a href="{root}llms-full.txt">Die gesamte Sammlung als Markdown</a></li>
</ul>"""
        cite = f"""<div class="callout">
  <p>Bitte zitieren Sie den Originalartikel:</p>
  <p lang="en">{esc(ARTICLE)} <a href="https://doi.org/{ARTICLE_DOI}">doi:{ARTICLE_DOI}</a></p>
  <p>Für die lebendige Sammlung: Wolfien M, Scheel J. {esc(TITLE)} [Data set]. Zenodo. <a href="https://doi.org/{CONCEPT_DOI}">doi:{CONCEPT_DOI}</a></p>
</div>"""
        contribute = (f'<h2>Mitmachen</h2>\n<p>Sie kennen einen Artikel, der hierher gehört? '
                      f'<a href="{REPO}/issues/new?template=suggest-reference.yml">Referenz vorschlagen</a> oder '
                      f'<a href="{REPO}/issues/new?template=propose-topic.yml">Thema vorschlagen</a>. Die Aufnahmekriterien stehen in den '
                      f'<a href="{REPO}/blob/main/CONTRIBUTING.md">Beitragsrichtlinien</a> (englisch).</p>')
    else:
        intro = (f"<p>The collection extends the viewpoint article {article} (J Med Internet Res 2023). It is curated by "
                 f"researchers and updated regularly: {len(references)} references, last update {esc(latest)}.</p>\n"
                 f'<div class="callout"><p><strong>New: learning modules.</strong> Interactive lessons in English and German with '
                 f'quizzes and exercises, e.g. on the <a href="{root}learn/history/en/index.html">history of medical informatics</a>. '
                 f'<a href="{root}learn/index.html#en">All learning modules</a></p></div>')
        downloads = f"""<ul>
  <li><a href="{root}data/references.bib">All references as BibTeX</a> (for Zotero, JabRef, LaTeX); each topic page also offers its own BibTeX file</li>
  <li><a href="{root}data/references.json">All references as CSL-JSON</a></li>
  <li><a href="{root}data/topics.json">Topics and keyword items as JSON</a></li>
  <li><a href="{root}llms-full.txt">The whole collection as Markdown</a></li>
</ul>"""
        cite = f"""<div class="callout">
  <p>Please cite the original article:</p>
  <p>{esc(ARTICLE)} <a href="https://doi.org/{ARTICLE_DOI}">doi:{ARTICLE_DOI}</a></p>
  <p>To cite the living collection: Wolfien M, Scheel J. {esc(TITLE)} [Data set]. Zenodo. <a href="https://doi.org/{CONCEPT_DOI}">doi:{CONCEPT_DOI}</a></p>
</div>"""
        contribute = (f'<h2>Contribute</h2>\n<p>Know a paper that belongs here? '
                      f'<a href="{REPO}/issues/new?template=suggest-reference.yml">Suggest a reference</a> or '
                      f'<a href="{REPO}/issues/new?template=propose-topic.yml">propose a topic</a>. The inclusion criteria are described in the '
                      f'<a href="{REPO}/blob/main/CONTRIBUTING.md">contribution guidelines</a>.</p>')
    body = f"""<h1>{esc(TITLE)}</h1>
<p class="lead">{esc(SUMMARY_DE if de else SUMMARY)}</p>
{intro}

<form class="search" id="search" role="search" aria-label="{esc(ui["search_label"])}">
  <div class="search-controls">
    <input type="search" id="q" name="q" placeholder="{esc(ui["search_placeholder"])}" aria-label="{esc(ui["search_aria"])}">
    <select id="topic" aria-label="{esc(ui["filter"])}"><option value="">{esc(ui["all_topics"])}</option>{options}</select>
    <label class="check"><input type="checkbox" id="new-only"> {esc(ui["new_in"])} {esc(latest)}</label>
  </div>
  <p id="search-status" class="muted" aria-live="polite" data-one="{esc(ui["result_one"])}" data-many="{esc(ui["result_many"])}" data-new="{esc(ui["n_new"])}"></p>
  <ul id="results" class="results"></ul>
</form>

<div id="topics">
<h2 id="topics-heading">{esc(ui["topics"])}</h2>
{chr(10).join(cards)}
</div>

<h2 id="downloads">{esc(ui["downloads"])}</h2>
{downloads}

<h2 id="cite">{esc(ui["cite"])}</h2>
{cite}

{contribute}
"""
    # The search index links are relative to the site root; the German start page lives one level deeper.
    extra_head = (f'<script type="application/json" id="search-index" data-root="{root}">{index_json}</script>\n'
                  f'<script src="{root}assets/search.js" defer></script>')
    return body, extra_head


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
    for lang, path in (("en", ""), ("de", "de/")):
        body, extra_head = home_page(lang, topics, topic_list, references, new_ids, latest, index_json, "../" * path.count("/"))
        if lang == "en":
            jsonld = jsonld_dataset(base, today, topics)
        else:
            jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": TITLE, "description": SUMMARY_DE,
                      "url": f"{base}/de/", "inLanguage": "de",
                      "about": {"@type": "Dataset", "name": TITLE, "url": base + "/",
                                "identifier": f"https://doi.org/{CONCEPT_DOI}"}}
        write(path + "index.html", page(
            base=base, path=path, title=TITLE, description=SUMMARY if lang == "en" else SUMMARY_DE, body=body,
            jsonld=jsonld, current="home", extra_head=extra_head, lang=lang,
            translation="de/index.html" if lang == "en" else "index.html"))

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
    urls = [f"{base}/", f"{base}/de/", f"{base}/references/"] + [f"{base}/topics/{t['id']}/" for t in topic_list] + learn_urls
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
