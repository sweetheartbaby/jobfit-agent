import json
from pathlib import Path
from typing import List

from ..schemas import Job


class JSONLJobLoader:
    """Load jobs from a line-delimited JSON file.

    Expected fields are flexible to make crawler/export integration easier:
    - title or job_title or 岗位
    - company or company_name or 公司
    - jd_text or description or content or 岗位描述
    """

    def load(self, jsonl_path: str) -> List[Job]:
        jobs = []
        path = Path(jsonl_path)
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            title = row.get("title") or row.get("job_title") or row.get("岗位") or f"job-{index}"
            company = row.get("company") or row.get("company_name") or row.get("公司") or "Unknown"
            text = row.get("jd_text") or row.get("description") or row.get("content") or row.get("岗位描述") or ""
            if len(str(text).strip()) < 20:
                continue
            jobs.append(Job(
                job_id=str(row.get("job_id") or row.get("id") or f"jsonl-{index}"),
                title=str(title).strip(),
                company=str(company).strip(),
                source_file=str(path),
                text=str(text).strip(),
            ))
        return jobs
