from __future__ import annotations

import argparse
import importlib
import pkgutil
from types import ModuleType
from typing import Type


def _is_concrete_scraper_class(candidate: object, module: ModuleType) -> bool:
    if not isinstance(candidate, type):
        return False
    if candidate.__module__ != module.__name__:
        return False
    if candidate.__name__ == "BaseGeographyScraper":
        return False

    base_module = importlib.import_module("scrapers.template.scraper_template")
    base_cls = getattr(base_module, "BaseGeographyScraper")
    return issubclass(candidate, base_cls)


def discover_scrapers() -> list[str]:
    results: list[str] = []
    package_name = "scrapers.regions"
    package = importlib.import_module(package_name)

    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if module.ispkg:
            continue
        if module.name.endswith(".__init__"):
            continue
        results.append(module.name.removeprefix("scrapers."))

    return sorted(results)


def load_scraper(scraper_path: str):
    module = importlib.import_module(f"scrapers.{scraper_path}")
    concrete_classes: list[Type[object]] = []

    for attr_name in dir(module):
        attr = getattr(module, attr_name)

        if _is_concrete_scraper_class(attr, module):
            concrete_classes.append(attr)

    if len(concrete_classes) == 1:
        return concrete_classes[0]()

    if len(concrete_classes) > 1:
        class_names = ", ".join(cls.__name__ for cls in concrete_classes)
        raise ValueError(
            f"Multiple scraper classes found in {scraper_path}: {class_names}. Keep exactly one."
        )

    raise ValueError(f"No scraper class found in {scraper_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="UniExplorer scraper runner")
    parser.add_argument("--list", action="store_true", help="List available scrapers")
    parser.add_argument("--all", action="store_true", help="Run all discovered scrapers")
    parser.add_argument("--scraper", type=str, help="Run scraper module path, e.g. regions.europe.germany")
    args = parser.parse_args()

    if args.list:
        for scraper in discover_scrapers():
            print(scraper)
        return

    if args.scraper:
        instance = load_scraper(args.scraper)
        instance.run()
        return

    if args.all:
        for scraper_path in discover_scrapers():
            print(f"Running {scraper_path}")
            try:
                load_scraper(scraper_path).run()
            except Exception as exc:
                print(f"Failed {scraper_path}: {exc}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
