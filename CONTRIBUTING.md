# Contributing to "Ten Topics for Medical Informatics"

Thank you for helping to keep this collection up to date! It is a *curated* resource: every reference is chosen by a person for a reason, and we would like to keep it that way.

## Ways to contribute

- **Suggest a reference:** open a [reference suggestion](https://github.com/mwolfien/ten_topics/issues/new?template=suggest-reference.yml). No Git knowledge needed.
- **Propose a topic:** open a [topic proposal](https://github.com/mwolfien/ten_topics/issues/new?template=propose-topic.yml).
- **Edit directly:** fork the repository, make your change as described below, and open a pull request. Add yourself to the contributors list in `templates/README.md.in`.

## Inclusion criteria

A new reference should meet the following criteria. Exceptions (e.g., landmark papers, widely used tools, tutorials) are possible but should be explained in the pull request or issue.

1. It fits one of the existing topics. Please stick to the original ten topics as much as possible; new topics can be proposed via an issue.
2. It is a peer-reviewed article in a journal ranked Q1 in its field (JCR or SJR), **or** it has more than 20 citations. Preprints and grey literature only in justified cases.
3. For literature updates, it was published recently (the 2026 update covered 2024 and later).
4. It adds something the topic does not cover yet: prefer reviews, landmark studies and practical resources over further examples of the same point.
5. The DOI resolves and the metadata (first author, year) is correct.

## How the content is organized

The README is **generated**. Please do not edit `README.md` directly; edit these files instead:

| File | Content |
|---|---|
| `data/references.yaml` | all references, keyed by a short id |
| `data/topics.yaml` | sections, topics, introductory text and keyword items |
| `templates/README.md.in` | the text around the topics (introduction, citation, contributors) |

### Adding a reference

1. Add an entry to `data/references.yaml`:

   ```yaml
     smith2025:
       label: "Smith et al. 2025"     # link text shown in the README
       year: 2025
       doi: "10.1234/abcd.5678"       # without https://doi.org/; use `url:` only if there is no DOI
       type: article                  # article | preprint | book | resource | website
       added: "2026-10"               # when it was added to this collection (YYYY-MM)
   ```

   The id is the first author's surname and the year, in lowercase, with a letter suffix if needed (`smith2025b`). The optional fields `title`, `journal` and `note` may be added as well.

2. Cite it in `data/topics.yaml` with `[@smith2025]`, either in an existing keyword item or in a new one:

   ```yaml
           - items:
               - "Federated learning governance - [@eden2025], [@smith2025]"
   ```

3. Validate the data and regenerate the README:

   ```sh
   pip install pyyaml
   python scripts/tentopics.py validate
   python scripts/tentopics.py build
   python scripts/tentopics.py links   # optional: checks that DOIs and URLs resolve
   ```

4. Commit the changed data files **and** the regenerated `README.md`, then open a pull request.

The validation rejects, for example, unknown or unused reference ids, duplicate DOIs, malformed DOIs, and inline Markdown links in `topics.yaml` (all links belong in `references.yaml`).

## Review and releases

- Pull requests are checked automatically (data validation, README up to date, DOIs and links) and reviewed by a maintainer before merging.
- Links and DOIs are additionally checked once a month; broken ones are reported in an issue.
- Larger updates are released as new versions and noted in the [CHANGELOG](CHANGELOG.md), so that each version can be cited.

## License

By contributing, you agree that your contributions are licensed under the [CC BY 4.0 license](LICENSE) of this repository.
