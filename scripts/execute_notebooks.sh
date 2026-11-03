#!/usr/bin/env bash
# Execute every notebook under notes/ with the MATLAB kernel and store the
# outputs in the notebook, so the published site shows them without running
# MATLAB. Run it on a machine with a licensed MATLAB, from the book folder:
#
#   .venv/bin/pip install jupyter-matlab-proxy nbconvert
#   scripts/execute_notebooks.sh
#
# The MATLAB kernel comes from MathWorks' jupyter-matlab-proxy. It starts the
# installed MATLAB (MATLAB_APP below) and uses its license.
set -euo pipefail
cd "$(dirname "$0")/.."

JUPYTER="${JUPYTER:-.venv/bin/jupyter}"
MATLAB_APP="${MATLAB_APP:-/Applications/MATLAB_R2026a.app}"
export PATH="$(cd "$(dirname "$JUPYTER")" && pwd):$MATLAB_APP/bin:$PATH"
export MWI_USE_EXISTING_LICENSE=True

find notes -name '*.ipynb' -not -path '*/_build/*' | while read -r nb; do
  echo "Executing $nb"
  "$JUPYTER" nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=600 \
    --ExecutePreprocessor.kernel_name=jupyter_matlab_kernel "$nb"
  # The kernel streams printed text in small pieces; join them into one output per cell.
  python3 - "$nb" <<'EOF'
import json, sys
path = sys.argv[1]
nb = json.load(open(path, encoding="utf-8"))
for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    merged = []
    for out in cell.get("outputs", []):
        if out.get("output_type") == "stream":
            # drop the kernel's start-up messages, keep the program's output
            original = "".join(out["text"])
            lines = [l for l in original.splitlines(keepends=True)
                     if l.strip() not in ("Starting MATLAB ...", "Executing ...")]
            out["text"] = "".join(lines)
            if original.strip() and not out["text"].strip():
                continue   # the chunk held only start-up messages
            if merged and merged[-1].get("output_type") == "stream" \
                    and merged[-1].get("name") == out.get("name"):
                merged[-1]["text"] += out["text"]
                continue
        merged.append(out)
    cell["outputs"] = merged
json.dump(nb, open(path, "w", encoding="utf-8"), indent=1)
EOF
done
echo "Done."
