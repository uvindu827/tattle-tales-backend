from pydantic import BaseModel, Field

class ArticleOut(BaseModel):
    id: str = Field(..., description="Unique id if the article derived from the url")
    source: str = Field(..., description="Source of the article")
    title: str = Field(..., description="Headline of the article")
    url: str = Field(..., description="Link to the original article")
    published_at: str = Field(..., description="Published time of the article in source")
    summary: str = Field(..., description="Short summary taken from the rss feed")
    fullText: str = Field(..., description="Extracted full article")
    scraped_at: str = Field(..., description="Time that article is scraped")

    class Config:
        from_attributes = True

class ScrapeResult(BaseModel):
    total_processed: int = Field(..., description="Total articles preocessed")
    new_added: int = Field(..., description="Genuinely new articles added to the storage")
    already_seen: int = Field(..., description="Articles that were alredy in the storage")

    