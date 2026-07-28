from pydantic import BaseModel, Field

class NarrationSegmentOut(BaseModel):
    idx: int = Field(..., description="Position of this segment in the narration")
    text: str = Field(..., description="The sentence to speak")
    safe_pause_point: bool = Field(..., description="Is narration can safely paused in this segment")

    class Config:
        from_attributes = True

class NarrationScriptOut(BaseModel):
    id: str = Field(..., description="Same id as source MergedNews")
    headline: str = Field(..., description="Headline from the merged news")
    category: str = Field(..., description="News category from the merged news")
    source_names: list[str] = Field(..., description="Sources contributed to the story")
    segments: list[NarrationSegmentOut] = Field(..., description="The segmented narration script")
    created_at: str = Field(..., description="Time the scripts generated")

    class Config:
        from_attributes = True

class NarrationResults(BaseModel):
    total_processed: int = Field("Total narrations produced")
    new_added: int = Field("Newly added narrations")
    already_seen: int = Field("Narrations already was in the store")