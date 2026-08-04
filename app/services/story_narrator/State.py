from typing import TypedDict, Optional

class NarrationSessionState(TypedDict):
    script_id: str
    headline: str
    source_names: list[str]

    segments: list[dict]
    current_segment_idx: int
    total_segments: int
    is_finished: bool

    last_sudio_path: Optional[str]
    last_explation: Optional[str]