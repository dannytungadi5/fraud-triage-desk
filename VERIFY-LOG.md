# VERIFY-LOG - what Kane CLI actually ran

Every entry below is a real `kane-cli run` (headless, agent mode) against the
live deployment https://dannytungadi5.github.io/fraud-triage-desk/, executed by
the coding agent during the build. Statuses and summaries are taken from the
run_end NDJSON records. Raw logs are reproducible with `kane/verify.sh`.

## 2026-11-24, suite run 1 (commit 2979456)

| Flow | Status | Kane's summary (abridged) |
|------|--------|---------------------------|
| F01 dashboard loads | PASSED | Page shows 172 transactions, 5 flags raised, queue lists FLAG-0001 / STRUCT-01. |
| F02 triage end to end | PASSED | Opened FLAG-0001, saw account A-1042 and four cash deposits, note added, Confirm fraud flipped the chip to Confirmed, Confirmed Fraud KPI became 1, SAR narrative mentioning A-1042 appeared. |
| F04 export report | PASSED | Report modal showed JSON containing FLAG-0001 and a Download JSON button; modal closed cleanly. |
| F05 rule toggles | PASSED | Unchecking GEO-05 dropped the queue to 4 open cases; re-checking restored 5. |
| F03 malformed CSV | FAILED | "Clicking the Upload CSV button opened the upload control, but the run did not select or submit bad.csv." Kane could not act on the file input. |

## The F03 investigation (six failed runs, three real defects found)

F03 became a genuine debugging loop. Each Kane failure was read from its
evidence pack (screenshots, HAR, action log) and drove one fix:

1. **File input was `display:none`.** Kane could not act on it, and neither can
   keyboards or assistive tech. Fix (5b5202f): visually-hidden but present
   `sr-only` input. Kane still could not attach files - agent mode has no
   file-chooser action - so the upload path gained alternatives.
2. **Subresource bodies stall under Kane's runner.** A "Load CSV from URL"
   feature was added; Kane's HAR showed `GET bad.csv -> 200` but the fetch/XHR
   continuation never ran. Timers (a 400ms watcher) also never fired in that
   environment, while synchronous click handlers worked.
3. **Root cause of the silent banner: CSS.** Instrumented runs showed the
   validation handler firing on every click, `parseCSV` throwing
   `row 2: bad amount 'not_a_number'`, and `banner("error", ...)` setting
   class `error` - while `getComputedStyle` still reported `display:none`.
   The `role="alert"` banner was being hidden in that browser profile. Fix:
   `banner()` now also sets inline `style.display="block"`, so no stylesheet
   can suppress validation feedback. Commit "Banner: inline display...".
   F03 passed immediately after, locally and against the live URL.

The user-facing flow also changed for the better during the hunt: the malformed
sample is now a first-class "Try malformed CSV" header action that exercises
the same parser and validator with no file dialog at all.

## 2026-11-24, suite run 2 (case-file redesign, banner fix)

Full suite re-run against the live URL after the visual redesign and the
banner fix:

| Flow | Status |
|------|--------|
| F01 dashboard loads | PASSED |
| F02 triage end to end | PASSED |
| F03 malformed CSV | PASSED |
| F04 export report | PASSED |
| F05 rule toggles | PASSED |

## Closed loop

The loop used throughout: agent edits code -> push -> Pages deploys ->
`kane/verify.sh` runs the suite headless -> agent reads the NDJSON verdicts
-> next edit. The agent never opened the page in a browser itself; Kane's
verdict was the only acceptance signal. See AGENTS.md.
