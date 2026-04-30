from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    text: str
    author: str
    topic: str
