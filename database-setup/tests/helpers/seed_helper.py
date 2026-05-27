from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Any, TypeVar, cast

from utils.json_loader import load_json

SeedItem = TypeVar("SeedItem", bound=Mapping[str, Any])


def load_seed_data(data_dir: Path, file_name: str) -> list[SeedItem]: # type: ignore
    return cast(list[SeedItem], load_json(data_dir / file_name))


def create_missing_items(
    items: Iterable[SeedItem],
    existing_names: set[str],
    create_item: Callable[[SeedItem], object],
    name_key: str = "name",
) -> None:
    for item in items:
        item_name = item[name_key]

        if item_name not in existing_names:
            create_item(item)
            existing_names.add(item_name)


def assert_items_present(
    expected_names: set[str],
    actual_names: set[str],
    label: str,
) -> None:
    missing_names = expected_names - actual_names

    assert not missing_names, (
        f"Missing {label}: {sorted(missing_names)}. "
        f"Actual values: {sorted(actual_names)}"
    )
