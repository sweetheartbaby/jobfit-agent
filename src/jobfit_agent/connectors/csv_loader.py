import csv
from pathlib import Path
from typing import List

from ..schemas import Job


class CSVJobLoader:
    def load(self, csv_path: str) -> List[Job]:
        jobs = []
        with Path(csv_path).open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader, 1):
                title = row.get("title") or row.get("岗位") or f"job-{index}"
                company = row.get("company") or row.get("公司") or "Unknown"
                jd_text = row.get("jd_text") or row.get("jd") or row.get("岗位描述") or ""
                if len(jd_text.strip()) < 20:
                    continue
                jobs.append(Job(
                    job_id=row.get("job_id") or f"csv-{index}",
                    title=title.strip(),
                    company=company.strip(),
                    source_file=str(csv_path),
                    text=jd_text.strip(),
                ))
        return jobs
