import json
from pathlib import Path
from typing import Any


def load_json(file_path: Path) -> Any:
    """Read and decode a UTF-8 JSON file."""
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)
