import logging

from .narration import create_narration_script
from .storage import save_narrations
from .models import NarrationScript
from ..news_merger.models import MergedNews
from ..news_merger.storage import load_existing as load_merged_sories

logger = logging.getLogger(__name__)

def make_all_narrations() -> list[NarrationScript]:
    merged_stories_dict = load_merged_sories()

    if not merged_stories_dict:
        logger.info("No merged stories found in storage - nothing to narrate.")

        return []

    scripts = []
    total = len(merged_stories_dict)

    for i, (story_id, story_data) in enumerate(merged_stories_dict.items(), start=1):
        story = MergedNews.from_dict(story_data)

        logger.info("Narrating story %d/%d: %s", i, total, story.headline)

        script = create_narration_script(story)
        scripts.append(script)

        return scripts

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    scripts = make_all_narrations()
    added = save_narrations(scripts)

    print(f"\nDone. Produced {len(scripts)} narration scripts this run, {added} were new.")