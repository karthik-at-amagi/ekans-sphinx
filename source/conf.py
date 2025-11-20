from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "EKANS"
copyright = "2025, Data Science Team"
author = "Data Science Team"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinxcontrib.confluencebuilder"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_permalinks_icon = "<span>#</span>"
html_theme = "sphinxawesome_theme"
html_static_path = ["_static"]
html_logo = "_static/ekans.png"
html_css_files = ["custom.css"]

# -- Confluence Integration ---------------------------------------------------
#
confluence_publish = True
confluence_space_key = "TESTSPHINX"
confluence_ask_password = False
confluence_disable_ssl_validation = False
# (for Confluence Cloud)
confluence_server_url = "https://amagiengg.atlassian.net/wiki/"
confluence_server_user = "dulam.karthik@amagi.com"
confluence_publish_dry_run = True
confluence_api_token = os.getenv("CONFLUENCE_API_TOKEN")


# ---- Auto index pages that include _index.md and keep nav hidden ----------------
AUTO_INDEX_FILENAME = "index.md"  # change to "index.rst" to emit RST instead
AUTO_INDEX_SOURCE = "_index.md"  # what each folder writes its visible content in
AUTO_INDEX_MAXDEPTH = 2
AUTO_INDEX_OVERWRITE_ROOT = (
    True  # set False if you want to keep a hand-written root index
)


def _render_index_md(dir_path: Path) -> str:
    # Visible content comes from _index.md (if present)
    parts: list[str] = []
    src = dir_path / AUTO_INDEX_SOURCE
    if src.exists():
        parts += [f"```{{include}} {AUTO_INDEX_SOURCE}", "```", ""]

    # Collect entries for sidebar (hidden toctree)
    entries: list[str] = []
    for p in sorted(dir_path.glob("*.md")):
        if p.name in {AUTO_INDEX_FILENAME, AUTO_INDEX_SOURCE}:
            continue
        if p.name.startswith(("_", ".")):
            continue
        entries.append(p.stem)  # sibling docs

    # Include subfolders' index pages if they exist (created earlier in this run)
    for sd in sorted(
        d
        for d in dir_path.iterdir()
        if d.is_dir() and not d.name.startswith(("_", "."))
    ):
        if (sd / "index.md").exists() or (sd / "index.rst").exists():
            entries.append(f"{sd.name}/index")

    if entries:
        parts += [
            "```{toctree}",
            ":hidden:",
            f":maxdepth: {AUTO_INDEX_MAXDEPTH}",
            "",
            *entries,
            "```",
            "",
        ]
    # No heading here — `_index.md` should provide any heading it wants.
    return "\n".join(parts)


def _render_index_rst(dir_path: Path) -> str:
    # RST variant if you prefer .rst index files
    parts: list[str] = []
    src = dir_path / AUTO_INDEX_SOURCE
    if src.exists():
        parts += [f".. include:: {AUTO_INDEX_SOURCE}", ""]  # visible content

    entries: list[str] = []
    for p in sorted(dir_path.glob("*.md")):
        if p.name in {AUTO_INDEX_FILENAME, AUTO_INDEX_SOURCE}:
            continue
        if p.name.startswith(("_", ".")):
            continue
        entries.append(p.stem)

    for sd in sorted(
        d
        for d in dir_path.iterdir()
        if d.is_dir() and not d.name.startswith(("_", "."))
    ):
        if (sd / "index.md").exists() or (sd / "index.rst").exists():
            entries.append(f"{sd.name}/index")

    if entries:
        joined = "\n   ".join(entries)
        parts += [
            ".. toctree::",
            f"   :maxdepth: {AUTO_INDEX_MAXDEPTH}",
            "   :hidden:",
            "",
            f"   {joined}",
            "",
        ]
    return "\n".join(parts)


def _write_index(dir_path: Path, is_root: bool):
    if (
        not AUTO_INDEX_OVERWRITE_ROOT
        and is_root
        and (dir_path / AUTO_INDEX_FILENAME).exists()
    ):
        return
    if AUTO_INDEX_FILENAME.endswith(".rst"):
        content = _render_index_rst(dir_path)
    else:
        content = _render_index_md(dir_path)
    # If nothing to write (no _index.md and no entries), skip creating an empty page
    if not content.strip():
        return
    (dir_path / AUTO_INDEX_FILENAME).write_text(content, encoding="utf-8")


def _autogen_indexes(_app) -> None:
    src = Path(_app.srcdir)
    # Walk subdirs first so parents can link only to subdirs that actually produced an index
    all_dirs = sorted(
        [p for p in [src] + list(src.rglob("*")) if p.is_dir()],
        key=lambda p: len(p.parts),
        reverse=True,
    )
    for d in all_dirs:
        _write_index(d, is_root=(d == src))


def setup(app):
    app.connect("builder-inited", _autogen_indexes)
    return {"version": "0.2", "parallel_read_safe": True}
