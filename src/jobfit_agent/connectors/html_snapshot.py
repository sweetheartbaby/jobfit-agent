import re
from html.parser import HTMLParser
from pathlib import Path
from typing import List

from ..schemas import Job


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.parts.append(text)

    def text(self) -> str:
        return "\n".join(self.parts)


class HTMLSnapshotLoader:
    def load(self, html_dir: str) -> List[Job]:
        root = Path(html_dir)
        jobs = []
        for path in sorted(root.iterdir()):
            if path.suffix.lower() not in {".html", ".htm"}:
                continue
            parser = _TextExtractor()
            parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
            text = re.sub(r"\n{2,}", "\n", parser.text()).strip()
            if len(text) < 20:
                continue
            lines = [line.strip("# ：: \t") for line in text.splitlines() if line.strip()]
            title = lines[0] if lines else path.stem
            company = "Unknown"
            for line in lines[:10]:
                if line.startswith("公司"):
                    company = re.sub(r"^公司[:：]?", "", line).strip() or company
                if line.startswith("岗位"):
                    title = re.sub(r"^岗位[:：]?", "", line).strip() or title
            jobs.append(Job(path.stem, title, company, str(path), text))
        return jobs
