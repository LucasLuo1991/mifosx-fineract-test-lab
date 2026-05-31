from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, TypeAlias, TypeVar, cast

from sqlalchemy.engine import RowMapping
from utils.json_loader import load_json

SeedItem: TypeAlias = Mapping[str, Any]
Normalizer: TypeAlias = Callable[[Any, SeedItem], Any]
_SeedItemT = TypeVar("_SeedItemT", bound=Mapping[str, Any])


@dataclass(frozen=True)
class SeedFieldMapping:
    """Mapping from a seed JSON field to the column used to verify it in SQL."""

    json_key: str
    db_column: str
    normalizer: Normalizer | None = None


def load_seed_data(data_dir: Path, file_name: str) -> list[SeedItem]:
    """Load a seed JSON file from a test data directory."""
    return cast(list[SeedItem], load_json(data_dir / file_name))


def create_missing_items(
    items: Iterable[_SeedItemT],
    existing_names: set[str],
    create_item: Callable[[_SeedItemT], object],
    name_key: str = "name",
) -> None:
    """Create seed items whose identity value is not already in the database."""
    for item in items:
        item_name = str(item[name_key])

        if item_name not in existing_names:
            create_item(item)
            existing_names.add(item_name)


def assert_items_present(
    expected_names: set[str],
    actual_names: set[str],
    label: str,
) -> None:
    """Assert that all expected names are present in a set of actual names."""
    missing_names = expected_names - actual_names

    assert not missing_names, (
        f"Missing {label}: {sorted(missing_names)}. "
        f"Actual values: {sorted(actual_names)}"
    )


def normalize_decimal(value: Any, _: SeedItem) -> Decimal | None:
    """Convert a JSON numeric value to Decimal while preserving nulls."""
    if value is None:
        return None

    return Decimal(str(value))


def normalize_optional_int(value: Any, _: SeedItem) -> int | None:
    """Convert an optional JSON value to int while preserving nulls."""
    if value is None:
        return None

    return int(value)


def normalize_optional_zero_decimal(value: Any, _: SeedItem) -> Decimal | None:
    """Convert JSON zero and null values to None, otherwise to Decimal."""
    if value is None or Decimal(str(value)) == Decimal("0"):
        return None

    return Decimal(str(value))


def normalize_seed_date(value: Any, item: SeedItem) -> date | None:
    """Parse a seeded date using the item's Fineract-style dateFormat field."""
    if value is None:
        return None

    date_format = item["dateFormat"]
    return datetime.strptime(str(value), _python_date_format(str(date_format))).date()


def normalize_fee_month_day_day(value: Any, item: SeedItem) -> int | None:
    """Extract the day number from a seeded month-day fee value."""
    parsed_date = _normalize_month_day(value, item)
    return parsed_date.day if parsed_date is not None else None


def normalize_fee_month_day_month(value: Any, item: SeedItem) -> int | None:
    """Extract the month number from a seeded month-day fee value."""
    parsed_date = _normalize_month_day(value, item)
    return parsed_date.month if parsed_date is not None else None


def assert_seed_items_match_db(
    expected_items: Iterable[SeedItem],
    actual_rows: Iterable[RowMapping],
    label: str,
    identity_json_key: str = "name",
    identity_db_column: str | None = None,
    field_mappings: Iterable[SeedFieldMapping] = (),
) -> None:
    """Assert that seeded items exist in the database with matching fields."""
    identity_column = identity_db_column or identity_json_key
    expected_by_identity = {
        str(item[identity_json_key]): item for item in expected_items
    }
    actual_by_identity = {str(row[identity_column]): row for row in actual_rows}

    assert_items_present(
        expected_names=set(expected_by_identity),
        actual_names=set(actual_by_identity),
        label=label,
    )

    mismatches: list[str] = []

    for identity, expected_item in expected_by_identity.items():
        actual_row = actual_by_identity[identity]

        for field_mapping in field_mappings:
            if field_mapping.json_key not in expected_item:
                expected_value = None
            else:
                expected_value = expected_item[field_mapping.json_key]

            if field_mapping.normalizer is not None:
                expected_value = field_mapping.normalizer(expected_value, expected_item)

            actual_value = _normalize_db_value(actual_row[field_mapping.db_column])

            if actual_value != expected_value:
                mismatches.append(
                    f"{label} '{identity}' field '{field_mapping.json_key}' "
                    f"expected {expected_value!r}, actual {actual_value!r}"
                )

    assert not mismatches, "Seed field mismatches:\n" + "\n".join(mismatches)


def _normalize_db_value(value: Any) -> Any:
    """Normalize database values before comparing them to JSON seed values."""
    if isinstance(value, Decimal):
        return value.normalize()

    return value


def _normalize_month_day(value: Any, item: SeedItem) -> date | None:
    """Parse a month-day value using the item's monthDayFormat field."""
    if value is None:
        return None

    month_day_format = str(item["monthDayFormat"])
    return datetime.strptime(
        f"{value} 2000",
        f"{_python_date_format(month_day_format)} %Y",
    ).date()


def _python_date_format(date_format: str) -> str:
    """Translate Fineract date format tokens to Python strptime tokens."""
    return (
        date_format.replace("yyyy", "%Y")
        .replace("MMMM", "%B")
        .replace("MMM", "%b")
        .replace("dd", "%d")
    )
