from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


FORBIDDEN_TAGS = {"script", "foreignObject"}


def validate_svg(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except ET.ParseError as exc:
        return [f"XML parse error: {exc}"]

    tag = root.tag.lower()
    if not tag.endswith("svg"):
        issues.append("Root tag is not <svg>")

    width = root.attrib.get("width")
    height = root.attrib.get("height")
    view_box = root.attrib.get("viewBox")
    if not (width and height) and not view_box:
        issues.append("Missing dimensions: add width/height or viewBox")

    for elem in root.iter():
        local_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if local_name in FORBIDDEN_TAGS:
            issues.append(f"Forbidden tag found: <{local_name}>")

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate SVG files")
    parser.add_argument("path", type=Path, help="SVG file or directory")
    args = parser.parse_args()

    files: list[Path]
    if args.path.is_dir():
        files = sorted(args.path.rglob("*.svg"))
    else:
        files = [args.path]

    has_errors = False
    for file_path in files:
        issues = validate_svg(file_path)
        if not issues:
            print(f"OK: {file_path}")
            continue
        has_errors = True
        print(f"FAIL: {file_path}")
        for issue in issues:
            print(f"  - {issue}")

    if has_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
