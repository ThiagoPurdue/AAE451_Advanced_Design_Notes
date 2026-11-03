# AAE 451 Advanced Aircraft Design: Lecture Notes

Lecture notes for AAE 451 Advanced Aircraft Design, Purdue University, built with
[Jupyter Book 2](https://jupyterbook.org) (MyST). The notes follow the AIAA 2026-27 Navy Jet
Trainer RFP.

Site: https://thiagopurdue.github.io/AAE451_Advanced_Design_Notes/

## Layout

| Path | Contents |
|---|---|
| `myst.yml` | Book configuration and table of contents |
| `notes/` | All Markdown pages of the book: `index.md`, `accessibility.md` and one folder per chapter |
| `notes/navy-rfp/` | The RFP summary page and its figures |
| `notes/lecture-NN/` | One folder per lecture: its pages and a `figures/` folder. Diagrams drawn in draw.io keep their `.drawio` source there |
| `notes/_static/site.css` | Accessibility overrides for the theme |
| `notes/_parts/` | Sidebar footer text |
| `scripts/make_figures.py` | Draws every figure except the draw.io diagrams |
| `scripts/export_drawio.py` | Exports every `.drawio` file under `notes/` to SVG (needs the draw.io desktop app) |
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

Regenerate the figures after editing the script, and the draw.io diagrams after editing them in draw.io:

```bash
python3 scripts/make_figures.py
python3 scripts/export_drawio.py
```

## Code in the notes

MATLAB code appears in two forms.

- A **notebook page** (`notes/lecture-NN/*.ipynb`) with the MATLAB kernel. Its outputs are
  stored in the notebook, so GitHub builds the page without MATLAB. Execute the notebooks on a
  machine with a licensed MATLAB before committing:

  ```bash
  .venv/bin/pip install jupyter-matlab-proxy nbconvert
  scripts/execute_notebooks.sh        # uses /Applications/MATLAB_R2026a.app; set MATLAB_APP to change
  ```

- A **script** (`notes/lecture-NN/code/*.m`) offered for download through the `downloads`
  entry in a page's front matter. Its output, when shown, is a text file next to it:

  ```bash
  cd notes/lecture-02/code
  /Applications/MATLAB_R2026a.app/bin/matlab -batch "run('sizing_loop.m')" | tee sizing_loop_output.txt
  ```

Readers can run a script in their browser through the "Open in MATLAB Online" link, which
needs a MATLAB license (Purdue students have one).

## Add a lecture

1. Write the pages in `notes/lecture-NN/` and put its figures in `notes/lecture-NN/figures/`.
2. Add them to the `toc` in `myst.yml`.
3. Give every figure an `:alt:` text and a caption, and every table a caption.
4. Build, run the accessibility check, and push to `main`.
