from typing import Optional
from pydantic import BaseModel, Field

class StartSessionRequest(BaseModel):
    script_id:str = Field(..., description="Id of the narrationScript to narrate")

class AskQuestionRequest(BaseModel):
    question:str = Field(..., description="Question to be answered")

class NarratorStepResult(BaseModel):
    thread_id:str = Field(..., description="Identifies the session")
    finished:bool = Field(..., description="True when every segment narrated")

    type:Optional[str] = Field(None, description="segment or explanation")

    #populated when type is "segment"
    segment_idx: Optional[int] = None
    text: Optional[str] = None
    audio_url: Optional[str] = None
    is_last_segment: Optional[bool] = None

    #populated when type is "explanation"
    question: Optional[str] = None
    answer: Optional[str] = None
    source_title: Optional[str] = None
    source_url: Optional[str] = None
