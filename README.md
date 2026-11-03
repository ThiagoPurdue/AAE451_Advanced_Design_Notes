# AAE 490/590 Aircraft Design: Lecture Notes

Lecture notes for AAE 490/590 Aircraft Design, Purdue University, Fall 2026, built with
[Jupyter Book 2](https://jupyterbook.org) (MyST). The notes follow the AIAA 2026-27 Navy Jet
Trainer RFP.

Site: https://thiagopurdue.github.io/AAE451_Advanced_Design_Notes/

## Layout

| Path | Contents |
|---|---|
| `myst.yml` | Book configuration and table of contents |
| `notes/` | All Markdown pages of the book: `index.md`, `accessibility.md` and one folder per chapter |
| `notes/navy-rfp/` | The RFP summary page and its figures |
| `notes/lecture-NN/` | One folder per lecture: its pages and a `figures/` folder |
| `notes/_static/site.css` | Accessibility overrides for the theme |
| `notes/_parts/` | Sidebar footer text |
| `scripts/make_figures.py` | Draws every diagram in the book |
| `scripts/fix_theme_a11y.py` | Post-build fix for two theme labelling issues (WCAG 2.5.3) |
| `scripts/check_accessibility.mjs` | Runs the axe accessibility engine on the built site |
| `.github/workflows/deploy.yml` | Builds and publishes the site to GitHub Pages on every push to `main` |

## Build locally

```bash
python3 -m venv .venv
.venv/bin/pip install "jupyter-book==2.1.7"
.venv/bin/jupyter-book start          # live preview at http://localhost:3000
.venv/bin/jupyter-book build --html   # static site in _build/html
python3 scripts/fix_theme_a11y.py _build/html
```

Check accessibility with Google Chrome installed (run from any scratch folder):

```bash
npm install axe-core@4.14.0 puppeteer-core@25.16.0
node /path/to/Lecture_Notes_Book/scripts/check_accessibility.mjs /path/to/Lecture_Notes_Book/_build/html
```

The GitHub workflow runs the same build, fix and check on every push to `main`. It does not
publish the site if the check finds a WCAG 2.1 A or AA violation.

Regenerate the figures after editing the script:

```bash
python3 scripts/make_figures.py
```

## Add a lecture

1. Write the pages in `notes/lecture-NN/` and put its figures in `notes/lecture-NN/figures/`.
2. Add them to the `toc` in `myst.yml`.
3. Give every figure an `:alt:` text and a caption, and every table a caption.
4. Build, run the accessibility check, and push to `main`.
