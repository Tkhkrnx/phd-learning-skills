# Commands and input modes

## Normal pipeline

```powershell
$env:PYTHONUTF8='1'
python scripts/run_reference_validation_pipeline.py `
  --project-dir "C:\path\to\paper" `
  --tex "main.tex" `
  --bib "refs.bib" `
  --bbl "main.bbl" `
  --paper-title "Paper Title" `
  --venue "Target Venue" `
  --verification-date "2026-09-13" `
  --output-dir "C:\path\to\paper\output\pdf"
```

Expected outputs:

- `reference_validation_report_final.verification.json`
- `reference_validation_report_final.html`
- `reference_validation_report_final.pdf`

## Manual attestation

Use `--manual-audited-all-confirmed` only when the user explicitly states that every reference has already been manually verified and requests report generation from that attestation. Preserve that provenance in the report; do not present it as tool-based verification.

```powershell
python scripts/run_reference_validation_pipeline.py `
  --project-dir "C:\path\to\paper" `
  --tex "main.tex" `
  --bib "refs.bib" `
  --bbl "main.bbl" `
  --paper-title "Paper Title" `
  --venue "Target Venue" `
  --verification-date "2026-09-13" `
  --output-dir "C:\path\to\paper\output\pdf" `
  --manual-audited-all-confirmed
```

## Supported local inputs

- standard `.bbl`;
- Elsevier-style `\bibitem[...]{key}` `.bbl`;
- inline `thebibliography` and `\bibitem` blocks in `.tex`.

If the project omits an input, inspect the actual bibliography setup and pass only supported arguments. Do not fabricate placeholder files.
