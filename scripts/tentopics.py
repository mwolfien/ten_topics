#!/usr/bin/env python3
"""Maintenance tool for "Ten Topics for Medical Informatics".

The curated content lives in two files:

  data/topics.yaml       sections, topics and their keyword items
  data/references.yaml   every cited reference, keyed by a short id

README.md is generated from these files and templates/README.md.in.

Usage:
  python scripts/tentopics.py validate        check the data files
  python scripts/tentopics.py build           regenerate README.md
  python scripts/tentopics.py build --check   fail if README.md is out of date
  python scripts/tentopics.py links           check that DOIs and URLs resolve
  python scripts/tentopics.py release-notes   summarize references added since the last release
"""

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "data" / "topics.yaml"
REFERENCES = ROOT / "data" / "references.yaml"
TEMPLATE = ROOT / "templates" / "README.md.in"
README = ROOT / "README.md"

CITE = re.compile(r"\[@([a-z0-9-]+)\]")
DOI = re.compile(r"^10\.\d{4,9}/\S+$")
ADDED = re.compile(r"^\d{4}(-\d{2})?$")
TYPES = {"article", "preprint", "book", "resource", "website"}
REF_FIELDS = {"label", "year", "doi", "url", "type", "added", "title", "journal", "note"}
USER_AGENT = "ten-topics-link-check (+https://github.com/mwolfien/ten_topics)"


class UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys instead of silently overwriting."""


def _construct_mapping(loader, node, deep=False):
    keys = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in keys:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", key_node.start_mark)
        keys.add(key)
    return loader.construct_mapping(node, deep)


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load():
    with open(TOPICS, encoding="utf-8") as f:
        topics = yaml.load(f, Loader=UniqueKeyLoader)
    with open(REFERENCES, encoding="utf-8") as f:
        references = yaml.load(f, Loader=UniqueKeyLoader)["references"]
    return topics, references


def texts(topics):
    """Yield (location, text) for every piece of prose in topics.yaml."""
    for section in topics["sections"]:
        for topic in section["topics"]:
            for block in topic["body"]:
                if isinstance(block, dict):
                    for item in block["items"]:
                        yield topic["id"], item
                else:
                    yield topic["id"], block


def link(ref):
    return f"https://doi.org/{ref['doi']}" if "doi" in ref else ref["url"]


# --------------------------------------------------------------------------- validate

def validate(topics, references):
    errors = []

    seen_dois = {}
    for rid, ref in references.items():
        where = f"references.yaml: {rid}"
        if not re.fullmatch(r"[a-z0-9-]+", rid):
            errors.append(f"{where}: id must be lowercase letters, digits and dashes")
        if not isinstance(ref, dict):
            errors.append(f"{where}: entry must be a mapping")
            continue
        unknown = set(ref) - REF_FIELDS
        if unknown:
            errors.append(f"{where}: unknown field(s) {sorted(unknown)}")
        if not ref.get("label"):
            errors.append(f"{where}: missing label")
        if ("doi" in ref) == ("url" in ref):
            errors.append(f"{where}: needs exactly one of doi or url")
        if "doi" in ref:
            doi = str(ref["doi"])
            if not DOI.match(doi):
                errors.append(f"{where}: malformed DOI {doi!r} (write it without https://doi.org/)")
            key = doi.lower()
            if key in seen_dois:
                errors.append(f"{where}: same DOI as {seen_dois[key]}")
            seen_dois[key] = rid
        if "url" in ref and not str(ref["url"]).startswith("https://"):
            errors.append(f"{where}: url must start with https://")
        if ref.get("type") not in TYPES:
            errors.append(f"{where}: type must be one of {sorted(TYPES)}")
        if ref.get("type") != "resource" and not isinstance(ref.get("year"), int):
            errors.append(f"{where}: missing or non-numeric year")
        if not ADDED.match(str(ref.get("added", ""))):
            errors.append(f"{where}: added must be YYYY or YYYY-MM (as a quoted string)")

    topic_ids, used = set(), set()
    for section in topics["sections"]:
        for topic in section["topics"]:
            if topic["id"] in topic_ids:
                errors.append(f"topics.yaml: duplicate topic id {topic['id']!r}")
            topic_ids.add(topic["id"])
    for where, text in texts(topics):
        if re.search(r"\]\(https?://", text):
            errors.append(f"topics.yaml: {where}: inline link found; add it to references.yaml "
                          f"and cite it as [@id]: {text[:60]}...")
        for rid in CITE.findall(text):
            used.add(rid)
            if rid not in references:
                errors.append(f"topics.yaml: {where}: unknown reference [@{rid}]")
    for rid in sorted(set(references) - used):
        errors.append(f"references.yaml: {rid} is never cited in topics.yaml")

    return errors


# --------------------------------------------------------------------------- build

def render_topics(topics, references):
    def cite(match):
        ref = references[match.group(1)]
        return f"[{ref['label']}]({link(ref)})"

    out = []
    for section in topics["sections"]:
        out += [f"## {section['title']}", ""]
        for topic in section["topics"]:
            prefix = f"Topic {topic['number']}: " if topic.get("number") else ""
            out += [f"### {prefix}{topic['title']}"]
            for block in topic["body"]:
                if isinstance(block, dict):
                    out += [f"* {CITE.sub(cite, item)}" for item in block["items"]]
                else:
                    out += [CITE.sub(cite, block)]
                out += [""]
    return "\n".join(out).rstrip() + "\n"


def render_readme(topics, references):
    template = TEMPLATE.read_text(encoding="utf-8")
    n_refs = len(references)
    latest = max(str(r["added"]) for r in references.values())
    return (template
            .replace("{{TOPICS}}", render_topics(topics, references).rstrip())
            .replace("{{N_REFERENCES}}", str(n_refs))
            .replace("{{LAST_UPDATE}}", latest.replace("-", "--")))  # shields.io escapes dashes


# --------------------------------------------------------------------------- links

def _request(url, method):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read() if method == "GET" else b""


def check_one(rid, ref):
    """Return (rid, status, message) with status in ok | warn | fail."""
    if "doi" in ref:
        # The DOI handle API tells whether a DOI is registered, without hitting
        # publisher sites that often block automated requests.
        api = "https://doi.org/api/handles/" + urllib.parse.quote(str(ref["doi"]), safe="/")
        try:
            _request(api, "GET")
            return rid, "ok", ref["doi"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return rid, "fail", f"DOI not registered: {ref['doi']}"
            return rid, "warn", f"DOI check returned HTTP {e.code}: {ref['doi']}"
        except Exception as e:  # network trouble is not the reference's fault
            return rid, "warn", f"DOI check failed ({e}): {ref['doi']}"
    url = ref["url"]
    try:
        try:
            _request(url, "HEAD")
        except urllib.error.HTTPError as e:
            if e.code not in (403, 405, 501):
                raise
            _request(url, "GET")
        return rid, "ok", url
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return rid, "fail", f"HTTP {e.code}: {url}"
        return rid, "warn", f"HTTP {e.code}: {url}"
    except Exception as e:
        return rid, "warn", f"{e}: {url}"


def check_links(references):
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda item: check_one(*item), references.items()))
    for rid, status, message in results:
        if status != "ok":
            print(f"{status.upper():4}  {rid}: {message}")
    fails = sum(1 for _, s, _ in results if s == "fail")
    warns = sum(1 for _, s, _ in results if s == "warn")
    print(f"checked {len(results)} references: {fails} broken, {warns} warnings")
    if results and warns == len(results):
        print("every check failed: the network is probably unavailable")
        return 1
    return fails


# --------------------------------------------------------------------------- release notes

def _added_key(value):
    """Sortable key for `added` values: "2023" sorts before "2023-01"."""
    return str(value) if "-" in str(value) else f"{value}-00"


def release_notes(topics, references, since=None):
    """Markdown summary of the references added since `since` (default: the latest `added`)."""
    since = since or max((str(r["added"]) for r in references.values()), key=_added_key)
    new = {rid for rid, ref in references.items() if _added_key(ref["added"]) >= _added_key(since)}

    def cite(match):
        ref = references[match.group(1)]
        text = f"[{ref['label']}]({link(ref)})"
        return f"**{text}**" if match.group(1) in new else text

    out, listed = [], set()
    for section in topics["sections"]:
        for topic in section["topics"]:
            items = [item for block in topic["body"] if isinstance(block, dict) for item in block["items"]]
            items = [item for item in items if set(CITE.findall(item)) & new]
            if not items:
                continue
            prefix = f"Topic {topic['number']}: " if topic.get("number") else ""
            out += [f"### {prefix}{topic['title']}"]
            out += [f"- {CITE.sub(cite, item)}" for item in items]
            out += [""]
            listed |= {rid for item in items for rid in CITE.findall(item)} & new
    n_topics = sum(1 for line in out if line.startswith("### "))
    head = [f"## What's new since {since}", "",
            f"{len(new)} new references in {n_topics} topics "
            f"({len(references)} references in total). New references are shown in bold.", ""]
    missing = new - listed  # e.g. cited only in introductory text
    if missing:
        out += ["### Also added", ""]
        out += [f"- [{references[r]['label']}]({link(references[r])})" for r in sorted(missing)] + [""]
    return "\n".join(head + out).rstrip() + "\n"


# --------------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="check the data files")
    build = sub.add_parser("build", help="regenerate README.md")
    build.add_argument("--check", action="store_true", help="fail if README.md is out of date")
    sub.add_parser("links", help="check that DOIs and URLs resolve")
    notes = sub.add_parser("release-notes", help="summarize references added since the last release")
    notes.add_argument("--since", help="YYYY or YYYY-MM (default: the most recent `added` value)")
    args = parser.parse_args()

    try:
        topics, references = load()
    except yaml.YAMLError as e:
        sys.exit(f"invalid YAML: {e}")

    errors = validate(topics, references)
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s) found in data/")

    if args.command == "validate":
        print(f"ok: {len(references)} references")
    elif args.command == "build":
        readme = render_readme(topics, references)
        if args.check:
            if README.read_text(encoding="utf-8") != readme:
                sys.exit("README.md is out of date: run `python scripts/tentopics.py build` and commit the result")
            print("README.md is up to date")
        else:
            README.write_text(readme, encoding="utf-8")
            print(f"wrote {README.relative_to(ROOT)}")
    elif args.command == "links":
        sys.exit(1 if check_links(references) else 0)
    elif args.command == "release-notes":
        if args.since and not ADDED.match(args.since):
            sys.exit("--since must be YYYY or YYYY-MM")
        print(release_notes(topics, references, args.since), end="")


if __name__ == "__main__":
    main()
