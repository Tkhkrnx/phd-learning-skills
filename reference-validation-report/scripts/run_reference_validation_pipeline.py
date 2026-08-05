from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run online reference verification and generate the final PDF report.")
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--tex", default="main.tex")
    parser.add_argument("--bib", default="refs.bib")
    parser.add_argument("--bbl", default="main.bbl")
    parser.add_argument("--paper-title")
    parser.add_argument("--venue", default="未知投稿期刊")
    parser.add_argument("--verification-date", default=str(date.today()))
    parser.add_argument("--output-dir")
    parser.add_argument("--output-prefix", default="reference_validation_report_final")
    parser.add_argument(
        "--manual-audited-all-confirmed",
        action="store_true",
        help="Bypass online verification and directly generate an all-confirmed report for manually audited references.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else (project_dir / "output" / "pdf")
    output_dir.mkdir(parents=True, exist_ok=True)
    verification_json = output_dir / f"{args.output_prefix}.verification.json"
    script_dir = Path(__file__).resolve().parent

    if args.manual_audited_all_confirmed:
        report_cmd = [
            sys.executable,
            str(script_dir / "generate_reference_validation_report.py"),
            "--project-dir",
            str(project_dir),
            "--tex",
            args.tex,
            "--bbl",
            args.bbl,
            "--venue",
            args.venue,
            "--verification-date",
            args.verification_date,
            "--output-dir",
            str(output_dir),
            "--output-prefix",
            args.output_prefix,
            "--default-status",
            "confirmed",
            "--all-real",
            "--no-metadata-errors",
        ]
        if args.paper_title:
            report_cmd.extend(["--paper-title", args.paper_title])
        subprocess.run(report_cmd, check=True)
        print(f"Manual audited all-confirmed report output dir: {output_dir}", flush=True)
        return 0

    verify_cmd = [
        sys.executable,
        str(script_dir / "verify_references.py"),
        "--project-dir",
        str(project_dir),
        "--tex",
        args.tex,
        "--bib",
        args.bib,
        "--bbl",
        args.bbl,
        "--venue",
        args.venue,
        "--verification-date",
        args.verification_date,
        "--output",
        str(verification_json),
    ]
    if args.paper_title:
        verify_cmd.extend(["--paper-title", args.paper_title])
    subprocess.run(verify_cmd, check=True)

    report_cmd = [
        sys.executable,
        str(script_dir / "generate_reference_validation_report.py"),
        "--project-dir",
        str(project_dir),
        "--tex",
        args.tex,
        "--bbl",
        args.bbl,
        "--venue",
        args.venue,
        "--verification-date",
        args.verification_date,
        "--output-dir",
        str(output_dir),
        "--output-prefix",
        args.output_prefix,
        "--verification-json",
        str(verification_json),
    ]
    if args.paper_title:
        report_cmd.extend(["--paper-title", args.paper_title])
    subprocess.run(report_cmd, check=True)
    print(f"Pipeline output dir: {output_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
