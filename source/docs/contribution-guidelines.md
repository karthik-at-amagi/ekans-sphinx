# Contribution Guidelines

We use [Sphinx](https://www.sphinx-doc.org/) with the
[MyST parser](https://myst-parser.readthedocs.io/) to format and generate our
documentation site, apply the stock Alabaster theme for styling, and publish it
to our on-prem machine available at `10.0.4.244`.

Sphinx is an open-source documentation generator that reads Markdown or
reStructuredText, understands directives such as `toctree`, and emits a static
HTML site.

```{tip}
ELI5: Write what you want to share in Markdown, Sphinx figures out the structure
and spits out the HTML/CSS/JS bundle.
```

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

## Updating a single page

If you spot something that needs to change while reading the docs:

1. Open the corresponding file under `source/docs/` (every visible page maps to a `.md` file).
1. Make your edit using normal Markdown or MyST directives and save.
1. Run `make html` from the repo root to ensure Sphinx still builds cleanly.
1. Commit the change and raise a PR with at least one reviewer; once CI passes, the docs server will publish the new HTML bundle.

## Creating a new page

1. Create `source/docs/path/to/your-new-page.md` manually (no generator needed).
1. Give it a top-level heading that matches the page title and add your content.
1. Update the appropriate `index.md` toctree so the page shows up in navigation (for example, add `path/to/your-new-page` under the relevant ` ```{toctree}` block).
1. If you want custom metadata (titles, weights, etc.), add MyST front matter or use the Sphinx-friendly directives instead of the shortcodes we used in the old site.

## Previewing your changes locally

If you want to preview your changes while you work:

1. Install the Python dependencies with `uv sync` (preferred) or `pip install -e .` to get `sphinx` and `myst-parser` locally. You'll need at least **Sphinx 8.2**.
1. Run `make html` from the repository root. The generated site lands in `build/html`.
1. Open `build/html/index.html` directly in a browser or run `python -m http.server --directory build/html 8000` for a lightweight local preview.
1. For auto-reload workflows you can optionally install `sphinx-autobuild` and run `sphinx-autobuild source build/html`.
1. Continue with the usual GitHub workflow to edit files, commit them, push the changes to your fork, and open a pull request.

## Creating an issue

If you've found a problem in the docs but aren't sure how to fix it yourself, please create an issue in the ekans repository. Include the path to the Markdown file (for example `source/docs/overview.md`) and, if relevant, the Sphinx build error you are seeing.

## Useful resources

* [Sphinx documentation](https://www.sphinx-doc.org/): Configuration, theming, and directive reference.
* [MyST parser guide](https://myst-parser.readthedocs.io/): Markdown syntax that Sphinx understands out of the box.
* [GitHub Hello World!](https://guides.github.com/activities/hello-world/): Quick refresher on the GitHub workflow.
