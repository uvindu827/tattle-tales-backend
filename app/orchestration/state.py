from typing import TypedDict, Annotated
import operator

class PipelineState(TypedDict):
    articles_scraped: int
    new_articles: int

    stories_merged: int
    new_stories: int

    scripts_narrated: int
    new_scripts: int

    log: Annotated[list[str], operator.add]

    