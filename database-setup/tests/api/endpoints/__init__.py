import importlib
import inspect
import pkgutil
import re
from collections.abc import Iterator

from api.base_endpoint import BaseEndpoint


def _attribute_name(endpoint_class_name: str) -> str:
    """Convert an endpoint class name to the client attribute name."""
    name = endpoint_class_name.removesuffix("Endpoint")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _discover_endpoint_classes() -> Iterator[tuple[str, type[BaseEndpoint]]]:
    """Discover endpoint classes exported by modules in this package."""
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(f"{__name__}.{module_info.name}")
        for _, endpoint_class in inspect.getmembers(module, inspect.isclass):
            if (
                endpoint_class is not BaseEndpoint
                and issubclass(endpoint_class, BaseEndpoint)
                and endpoint_class.__module__ == module.__name__
            ):
                yield _attribute_name(endpoint_class.__name__), endpoint_class


_ENDPOINT_CLASSES = tuple(_discover_endpoint_classes())

for _, endpoint_class in _ENDPOINT_CLASSES:
    globals()[endpoint_class.__name__] = endpoint_class


def endpoint_classes() -> Iterator[tuple[str, type[BaseEndpoint]]]:
    """Return discovered endpoint attribute names and classes."""
    return iter(_ENDPOINT_CLASSES)


__all__ = [
    "endpoint_classes",
    *(endpoint_class.__name__ for _, endpoint_class in _ENDPOINT_CLASSES),
] # type: ignore
