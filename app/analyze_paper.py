from __future__ import annotations

import argparse
import json
import os
import sys

from app.rag.pipeline import RagAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Analyze a research PDF with RAG")
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("--output", "-o", help="Path to JSON output", default="result.json")
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    analyzer = RagAnalyzer()
    result = analyzer.analyze(args.pdf)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()