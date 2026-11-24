# AGENTS.md - how to work on this repo with an agent + Kane CLI loop

This repo is built and verified by an AI coding agent working in a closed loop
with Kane CLI. If you are an agent picking this repo up, keep the loop intact:

1. Make your edit to `index.html` (single-file app; data embedded) or
   `data/northbridge-march.csv` (regenerate with `python3 gen_data.py` and
   re-embed the CSV into the `<script id="embedded-csv">` block).
2. Deploy (GitHub Pages serves the repo root) or set
   `FLAGLINE_URL` to a local server for a pre-deploy check.
3. Run `./kane/verify.sh`. It executes the flows in `kane/FLOWS.md`
   headlessly and exits non-zero on the first red suite.
4. Read the NDJSON run logs it leaves in its output directory. Each
   `run_end` line carries a structured verdict: what was expected, what the
   browser actually showed, and a root-cause note. Fix against that, not by
   guessing.
5. Append what Kane caught and what you changed to `VERIFY-LOG.md`.

Rules of the loop: Kane's verdict is the source of truth for "does it work".
A flow you have not run does not exist. Never weaken a flow objective to make
it pass; fix the app instead.
