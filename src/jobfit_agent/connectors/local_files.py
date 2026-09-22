import re
from pathlib import Path
from typing import List

from ..schemas import Job
from ..tools.text_utils import read_text


def _guess_title_and_company(path: Path, text: str):
    lines = [line.strip("# ：: \t") for line in text.splitlines() if line.strip()]
    title = lines[0] if lines else path.stem
    company = "Unknown"
    for line in lines[:8]:
        m = re.search(r"公司[:：]\s*(.+)", line)
        if m:
            company = m.group(1).strip()
        m = re.search(r"岗位[:：]\s*(.+)", line)
        if m:
            title = m.group(1).strip()
    return title, company


class JobLoaderAgent:
    def load(self, jobs_dir: str) -> List[Job]:
        root = Path(jobs_dir)
        jobs = []
        for path in sorted(root.iterdir()):
            if path.suffix.lower() not in {".txt", ".md"}:
                continue
            text = read_text(path)
            if len(text) < 20:
                continue
            title, company = _guess_title_and_company(path, text)
            jobs.append(Job(job_id=path.stem, title=title, company=company, source_file=str(path), text=text))
        return jobs
