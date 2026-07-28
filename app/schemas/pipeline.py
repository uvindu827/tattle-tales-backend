from pydantic import BaseModel, Field

class PipelineResults(BaseModel):
    thread_id: str = Field(..., description="Unique ID for the pipeline run")

    articles_scraped: int = Field(..., description="Total articles processed during scraping")
    new_articles: int = Field(..., description="Genuinely new articles scraped")

    stories_merged: int = Field(..., description="Total merged stories produced in merging")
    new_stories: int = Field(..., description="Genuinely new merged stories")

    scripts_narrated: int = Field(..., description="Total scripts made in the making of scripts")
    new_scripts: int = Field(..., description="Genuinnely new scripts")

    log: list[str] = Field(..., description="Ordered status messages, One per pipelinne stage")