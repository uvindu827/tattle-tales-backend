from dataclasses import dataclass, asdict

@dataclass
class Explanation:
    question: str
    answer_text: str
    source_title: str
    found: bool

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data:dict) -> "Explanation":
        return cls(**data)

    