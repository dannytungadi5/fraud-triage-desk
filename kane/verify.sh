#!/usr/bin/env bash
# Flagline verification loop: run every Kane CLI flow and aggregate verdicts.
# Exits non-zero if any flow fails. An agent (or CI) reads the NDJSON on
# stdout; humans read the summary at the end.
set -u
URL="${FLAGLINE_URL:-https://dannytungadi5.github.io/fraud-triage-desk/}"
OUT="${1:-/tmp/flagline-verify-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$OUT"
declare -a FLOWS=(
  "F01|Load the page. Verify the heading FLAGLINE is visible, the KPI strip shows 172 transactions and 5 flags raised, and the flag queue table lists case FLAG-0001 with rule STRUCT-01."
  "F02|Open case FLAG-0001 from the queue. Verify the case detail shows account A-1042 and lists four cash deposit transactions. Type the note 'confirmed structuring pattern' into the analyst note field, then click the Confirm fraud button. Verify the case status chip changes to confirmed, the Confirmed Fraud KPI becomes 1, and a draft suspicious-activity narrative mentioning A-1042 appears."
  "F03|Click the Try malformed CSV button in the header. Verify an error banner appears mentioning row 2, and the flag queue still shows 5 cases."
  "F04|Open case FLAG-0001, click Confirm fraud, then click Export report. Verify the report modal appears with JSON that includes FLAG-0001, status confirmed, and a sar field, and that a Download JSON button is visible."
  "F05|Open the Rules panel, uncheck the GEO-05 rule, and click Apply and rescan. Verify the queue now shows 4 open cases. Then open the Rules panel again, re-check GEO-05, apply, and verify the queue shows 5 open cases again."
)
fail=0
for entry in "${FLOWS[@]}"; do
  id="${entry%%|*}"; objective="${entry#*|}"
  echo "=== $id ==="
  kane-cli run --url "$URL" "$objective" --headless --agent > "$OUT/$id.ndjson" 2>&1
  status=$(tail -20 "$OUT/$id.ndjson" | grep -o '"type":"run_end","status":"[a-z]*"' | head -1 | cut -d'"' -f8)
  echo "$id: ${status:-unknown}"
  [ "$status" = "passed" ] || fail=1
done
echo "----"
if [ "$fail" -eq 0 ]; then echo "ALL FLOWS PASSED"; else echo "SOME FLOWS FAILED (see $OUT)"; fi
exit $fail
