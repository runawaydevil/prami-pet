from dataclasses import dataclass, field


@dataclass
class Result:
    text: str
    visibility: str
    accepted: bool
    favourite: bool = False
    boost: bool = False
    milestones: list = field(default_factory=list)
