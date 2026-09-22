import re
from pathlib import Path
from typing import Iterable, List


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"[。；;\n.!?？]", text)
    return [p.strip() for p in parts if p.strip()]


def find_keywords(text: str, keywords: Iterable[str]) -> List[str]:
    hits = []
    for keyword in keywords:
        if re.search(re.escape(keyword), text, re.IGNORECASE):
            hits.append(keyword)
    return hits


def find_evidence(text: str, keywords: Iterable[str], limit: int = 3) -> List[str]:
    evidence = []
    for sentence in split_sentences(text):
        if any(re.search(re.escape(keyword), sentence, re.IGNORECASE) for keyword in keywords):
            evidence.append(sentence)
    return evidence[:limit]
