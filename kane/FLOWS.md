# Kane CLI verification flows

Plain-English objectives, run with `kane-cli run` against the live deployment.
`verify.sh` in this directory runs the whole suite and aggregates the NDJSON
verdicts. Each flow is independent and starts from the home page.

The app under test: https://dannytungadi5.github.io/fraud-triage-desk/

## F01 - dashboard loads with a populated queue

> Load the page. Verify the heading "FLAGLINE" is visible, the KPI strip shows
> 172 transactions and 5 flags raised, and the flag queue table lists case
> FLAG-0001 with rule STRUCT-01.

## F02 - triage a case end to end

> Open case FLAG-0001 from the queue. Verify the case detail shows account
> A-1042 and four cash deposit transactions. Type the note "confirmed
> structuring pattern" into the analyst note field, then click "Confirm fraud".
> Verify the case status chip changes to "confirmed", the Confirmed Fraud KPI
> becomes 1, and a draft suspicious-activity narrative mentioning A-1042
> appears.

## F03 - malformed CSV is rejected

> Upload a CSV file with a broken amount column (see kane/fixtures/bad.csv).
> Verify an error banner appears saying the upload failed and naming the bad
> row, and the queue still shows the 5 built-in flags.

## F04 - export report contains the confirmed case

> After confirming case FLAG-0001, click "Export report". Verify the report
> modal appears with JSON that includes FLAG-0001, status "confirmed", and a
> "sar" field, and that a Download JSON button is visible.

## F05 - rule toggles rescan the queue

> Open the Rules panel, turn off GEO-05, and apply. Verify the queue now shows
> 4 open cases and the flags-by-rule chart shows 0 for GEO-05. Then turn GEO-05
> back on, apply, and verify 5 open cases are back.
