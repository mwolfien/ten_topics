# Releasing a new version

Each GitHub release is archived on Zenodo and gets its own version DOI. The concept DOI [10.5281/zenodo.23047297](https://doi.org/10.5281/zenodo.23047297) always resolves to the latest version.

Versions are named after the month of the update: `vYYYY.MM` (e.g. `v2026.09`).

## Checklist

1. **Make sure `main` is complete and green.** All planned changes are merged and the "Checks" workflow passes.
2. **Check links once more:**
   ```sh
   python scripts/tentopics.py links
   ```
3. **Generate the release notes.** They list every reference added since the last release, grouped by topic:
   ```sh
   python scripts/tentopics.py release-notes                 # since the most recent `added` value
   python scripts/tentopics.py release-notes --since 2026-10 # or since a given month
   ```
4. **Update `CHANGELOG.md`.** Add a section for the new version with a short summary (content and structural changes). Merge it via a pull request.
5. **If the topic structure changed** (topics renamed, merged, split or renumbered), say so in the CHANGELOG, and keep a note such as "formerly Topic 7" in the topic introduction, so that readers of the 2023 article can still find their topic.
6. **Update the contributors** in `templates/README.md.in` and, for people who should appear as authors of the Zenodo record, in `CITATION.cff`. Then regenerate the README (`python scripts/tentopics.py build`).
7. **Create the release on GitHub.** Choose "Draft a new release", create the tag `vYYYY.MM` on `main`, use the title "Ten Topics for Medical Informatics – YYYY-MM update", and paste the CHANGELOG section plus the generated release notes as the description. Publish it.
8. **Check the Zenodo record.** Zenodo archives the release automatically within a few minutes. Check authors, license and the related identifier (the JMIR article, `10.2196/45948`, "is supplement to").
