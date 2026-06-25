"""
load_dataset.py

Utility for loading and inspecting the Label Studio export
(`dataset_cartazes.json`) used to build the position heatmap and
layout-generation logic for the "Gerador de Cartazes para Festas da
Terrinha" project.

Usage:
    python3 load_dataset.py

This will print a summary of the dataset and verify that every
referenced image exists in images/.
"""

import json
import os
import unicodedata
from pathlib import Path

JSON_PATH = Path(__file__).parent / "dataset_cartazes.json"
IMAGES_DIR = Path(__file__).parent / "images"


def normalize_label(label: str) -> str:
    """
    Label Studio exported some rectanglelabels with invisible
    WORD JOINER characters (U+2060) mixed into the text, e.g.
    "\u2060\u2060\u2060Patrocínios" instead of "Patrocínios".

    This strips those out so labels can be compared/filtered reliably.
    """
    return "".join(ch for ch in label if unicodedata.category(ch) != "Cf")


def load_tasks():
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def image_filename(task: dict) -> str:
    """
    Returns the actual image filename (e.g. 'Frame_1.png'), stripping
    the Label Studio upload hash prefix from file_upload
    (e.g. '2f3f8fcb-Frame_1.png' -> 'Frame_1.png').
    """
    raw = task.get("file_upload", "")
    if "-" in raw:
        return raw.split("-", 1)[1]
    return raw


def main():
    tasks = load_tasks()
    print(f"Total tasks: {len(tasks)}")

    label_counts = {}
    missing_images = []

    for task in tasks:
        fname = image_filename(task)
        if not (IMAGES_DIR / fname).exists():
            missing_images.append(fname)

        for ann in task.get("annotations", []):
            for region in ann.get("result", []):
                for raw_label in region.get("value", {}).get("rectanglelabels", []):
                    label = normalize_label(raw_label)
                    label_counts[label] = label_counts.get(label, 0) + 1

    print("\nRegion counts per label (normalized):")
    for label, count in sorted(label_counts.items()):
        print(f"  {label:<30} {count}")

    print(f"\nImages referenced: {len(tasks)}")
    print(f"Images found in images/: {len(tasks) - len(missing_images)}")
    if missing_images:
        print(f"Missing images ({len(missing_images)}):")
        for m in missing_images[:10]:
            print(f"  - {m}")
        if len(missing_images) > 10:
            print(f"  ... and {len(missing_images) - 10} more")


if __name__ == "__main__":
    main()
