import json
from pathlib import Path
from typing import Any


def load_json(file_path: Path) -> Any:
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)
