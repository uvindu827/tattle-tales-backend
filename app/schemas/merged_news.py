from pydantic import BaseModel, Field

class MergedNewsOut(BaseModel):
    id: str = Field(..., description="Stable identifier derived from the set of srticle ids")
    headline: str = Field(..., description="Synthesized headline for the merged event")
    merged_summary: str = Field(..., description="Summary of the merged news")
    source_article_ids: list[str] = Field("ids of contributing raw articles")
    source_names: list[str] = Field("Names of the contributing sources")
    category: str = Field("Topic tag of the contributing articles")
    earliest_published: str = Field("Earliest published date amoung sources")
    latest_ppublished: str = Field("latest published amoung sources")
    merged_at: str = Field("Merged time")

    class Config:
        from_attributes = True

class MergeResult(BaseModel):
    total_processed: int = Field("Total merged news produced")
    new_added: int = Field("Newly added merged news")
    already_seen: int = Field("Merged news already was in the store")