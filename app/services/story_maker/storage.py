import json
import os
import logging

from .models import NarrationScript

logger = logging.getLogger(__name__)

DEFAULT_STORE_PATH = os.path.join("data", "narration_scripts.json")

def load_existing(path: str = DEFAULT_STORE_PATH) -> dict[str, dict]:
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)

            return {
                item["id"]: item for item in data
            }
        except json.JSONDecodeError:
            logger.warning("Existing store at %s in corrupted, starting fresh", path)

            return {}

def save_narrations(new_scripts: list[NarrationScript], path: str = DEFAULT_STORE_PATH) -> int:
    existing = load_existing()
    added = 0

    for script in new_scripts:
        if script.id in existing:
            continue

        existing[script.id] = script.to_dict()
        added += 1

    parent_dir = os.path.dirname(path)

    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            list(existing.values()),
            f,
            indent=2,
            ensure_ascii=False
        )

    logger.info("Saved %d new narration scripts, total scripts: %d", added, len(existing))

    return added