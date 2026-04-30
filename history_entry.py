from dataclasses import dataclass

from models.quote import Quote


@dataclass(frozen=True)
class HistoryEntry:
    quote: Quote
    generated_at: str

    def to_dict(self) -> dict:
        return {
            "text": self.quote.text,
            "author": self.quote.author,
            "topic": self.quote.topic,
            "generated_at": self.generated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "HistoryEntry":
        quote = Quote(
            text=data.get("text", ""),
            author=data.get("author", ""),
            topic=data.get("topic", ""),
        )
        return cls(quote=quote, generated_at=data.get("generated_at", ""))
