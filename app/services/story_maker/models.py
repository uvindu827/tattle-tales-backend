from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class NarrationSegment:
    idx: int
    text: str
    safe_pause_point: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "NarrationSegment":
        return cls(**data)

@dataclass
class NarrationScript:
    id: str
    headline: str
    category: str
    source_names: list[str]
    segments: list[NarrationSegment]
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "NarrationScript":
        segments = [NarrationSegment.from_dict(s) for s in data["segments"]]

        return cls(
            id = data["id"],
            headline = data["headline"],
            category= data["category"],
            source_names = data["source_names"],
            segments = segments,
            created_at = data["created_at"],
        )

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

    