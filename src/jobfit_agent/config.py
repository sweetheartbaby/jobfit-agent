import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .agents.jd_parser import DIMENSIONS, DimensionConfig


@dataclass
class JobFitConfig:
    scoring: Dict[str, float] = field(default_factory=dict)
    keywords: Dict[str, List[str]] = field(default_factory=dict)
    manual_review_threshold: float = 65.0


def default_config() -> JobFitConfig:
    return JobFitConfig(
        scoring={d.name: d.weight for d in DIMENSIONS},
        keywords={d.name: list(d.keywords) for d in DIMENSIONS},
    )


def load_config(path: Optional[str]) -> JobFitConfig:
    config = default_config()
    if not path:
        return config
    raw_path = Path(path)
    if not raw_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    data = _parse_simple_config(raw_path.read_text(encoding="utf-8"))
    if isinstance(data.get("scoring"), dict):
        for key, value in data["scoring"].items():
            try:
                config.scoring[key] = float(value)
            except (TypeError, ValueError):
                continue
    if isinstance(data.get("keywords"), dict):
        for key, value in data["keywords"].items():
            if isinstance(value, list):
                config.keywords[key] = [str(v) for v in value]
    if "manual_review_threshold" in data:
        try:
            config.manual_review_threshold = float(data["manual_review_threshold"])
        except (TypeError, ValueError):
            pass
    return config


def dimensions_from_config(config: JobFitConfig) -> List[DimensionConfig]:
    by_name = {d.name: d for d in DIMENSIONS}
    dimensions = []
    for name, base in by_name.items():
        dimensions.append(DimensionConfig(
            name=name,
            label=base.label,
            weight=config.scoring.get(name, base.weight),
            keywords=config.keywords.get(name, base.keywords),
        ))
    return dimensions


def _parse_simple_config(text: str) -> Dict:
    """Parse JSON or a small YAML subset used by examples/jobfit.yaml.

    This avoids mandatory third-party dependencies for the MVP.
    """
    stripped = text.strip()
    if not stripped:
        return {}
    if stripped.startswith("{"):
        return json.loads(stripped)

    root: Dict = {}
    current_section = None
    current_list_key = None
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current_section = line[:-1].strip()
            root[current_section] = {}
            current_list_key = None
            continue
        if current_section and line.startswith("  "):
            item = line.strip()
            if item.startswith("- ") and current_list_key:
                root[current_section][current_list_key].append(item[2:].strip().strip('"\''))
                continue
            if ":" in item:
                key, value = item.split(":", 1)
                key = key.strip()
                value = value.strip()
                if value == "":
                    root[current_section][key] = []
                    current_list_key = key
                else:
                    root[current_section][key] = _coerce_value(value)
                    current_list_key = None
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            root[key.strip()] = _coerce_value(value.strip())
    return root


def _coerce_value(value: str):
    value = value.strip().strip('"\'')
    try:
        return float(value)
    except ValueError:
        return value
