#!/usr/bin/env python3
"""Convert generic crawler output into JobFit Agent JSONL.

This adapter is intentionally conservative: it does not crawl websites. It only
converts data that the user already collected and is authorized to process.
"""

import argparse
import json
from pathlib import Path


def pick(row, *keys, default=""):
    for key in keys:
        if isinstance(row, dict) and row.get(key):
            return row[key]
    return default


def iter_rows(data):
    if isinstance(data, list):
        yield from data
    elif isinstance(data, dict):
        for key in ["items", "data", "jobs", "results"]:
            if isinstance(data.get(key), list):
                yield from data[key]
                return
        yield data


def convert(input_path: Path, output_path: Path):
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as f:
        for index, row in enumerate(iter_rows(data), 1):
            jd_text = pick(row, "jd_text", "description", "content", "desc", "岗位描述")
            if len(str(jd_text).strip()) < 20:
                continue
            item = {
                "job_id": str(pick(row, "job_id", "id", default=f"crawler-{index}")),
                "company": str(pick(row, "company", "company_name", "公司", default="Unknown")),
                "title": str(pick(row, "title", "job_title", "岗位", default=f"job-{index}")),
                "location": str(pick(row, "location", "city", "城市", default="")),
                "salary": str(pick(row, "salary", "薪资", default="")),
                "source_url": str(pick(row, "source_url", "url", "link", default="")),
                "jd_text": str(jd_text).strip(),
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description="Convert crawler JSON output to JobFit JSONL")
    parser.add_argument("--input", required=True, help="Input crawler JSON file")
    parser.add_argument("--output", required=True, help="Output JobFit JSONL file")
    args = parser.parse_args()
    count = convert(Path(args.input), Path(args.output))
    print(f"Exported {count} jobs to {args.output}")


if __name__ == "__main__":
    main()
