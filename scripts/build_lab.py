"""Build the in-browser Jupyter environment (JupyterLite with a Pyodide kernel) for exercise notebooks.

Every learning module may have a folder learn/<module-id>/notebook/ with notebooks and data files.
They are copied to <out>/lab/ under <module-id>/, so a notebook opens at

    lab/lab/index.html?path=<module-id>/<notebook>.ipynb

Everything runs in the reader's browser: no account, no server, files stay on their device.
Python packages such as numpy, pandas, scikit-learn and matplotlib are loaded from the Pyodide CDN.

Usage (after `tentopics.py site`, which writes the rest of the site):
    pip install jupyterlite-core==0.8.7 jupyterlite-pyodide-kernel==0.8.7 jupyter-server
    python scripts/build_lab.py --out _site
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "learn"
PYODIDE_KERNEL = {"name": "python", "display_name": "Python (Pyodide)", "language": "python"}
REDIRECT = '<script>location.replace("lab/index.html" + location.search + location.hash);</script>'


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(ROOT / "_site"), help="site directory; JupyterLite goes to <out>/lab")
    args = parser.parse_args()

    notebook_dirs = sorted(LEARN.glob("*/notebook"))
    if not notebook_dirs:
        print("no exercise notebooks, nothing to build")
        return
    with tempfile.TemporaryDirectory() as tmp:
        contents = Path(tmp) / "contents"
        for nb_dir in notebook_dirs:
            target = contents / nb_dir.parent.name
            shutil.copytree(nb_dir, target)
            # The downloadable notebooks ask for the usual "python3" kernel; in the browser it is Pyodide.
            for nb_file in target.glob("*.ipynb"):
                nb = json.loads(nb_file.read_text(encoding="utf-8"))
                nb.setdefault("metadata", {})["kernelspec"] = PYODIDE_KERNEL
                nb_file.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        subprocess.run(["jupyter", "lite", "build", "--contents", str(contents), "--lite-dir", tmp,
                        "--output-dir", str(Path(args.out).resolve() / "lab"), "--no-sourcemaps"],
                       cwd=tmp, check=True)
    # JupyterLite's own root page stays blank when the site is served from a subpath
    # (e.g. /ten_topics/lab/), so send visitors straight on to the JupyterLab app. The page
    # itself must stay: the apps read their configuration (jupyter-config-data) from it.
    root = Path(args.out).resolve() / "lab" / "index.html"
    root.write_text(root.read_text(encoding="utf-8").replace("<head>", "<head>\n    " + REDIRECT, 1), encoding="utf-8")
    print(f"built JupyterLite with {len(notebook_dirs)} notebook folder(s) into {Path(args.out) / 'lab'}")


if __name__ == "__main__":
    sys.exit(main())
