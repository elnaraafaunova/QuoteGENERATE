import json
from datetime import datetime
from pathlib import Path

from models.history_entry import HistoryEntry
from models.quote import Quote


class HistoryService:
    def __init__(self, data_path: str) -> None:
        self.data_path = Path(data_path)
        self._history: list[HistoryEntry] = []

    @property
    def history(self) -> list[HistoryEntry]:
        return self._history

    def add_to_history(self, quote: Quote) -> HistoryEntry:
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = HistoryEntry(quote=quote, generated_at=generated_at)
        self._history.append(entry)
        self.save_history()
        return entry

    def save_history(self) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [entry.to_dict() for entry in self._history]
        self.data_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load_history(self) -> tuple[bool, str]:
        if not self.data_path.exists():
            self._history = []
            return True, ""

        try:
            raw = self.data_path.read_text(encoding="utf-8")
            data = json.loads(raw)
            if not isinstance(data, list):
                raise ValueError("Неверный формат JSON")
            self._history = [HistoryEntry.from_dict(item) for item in data]
            return True, ""
        except (json.JSONDecodeError, ValueError):
            self._history = []
            return False, "Ошибка загрузки данных: файл JSON поврежден."

    def clear_history(self) -> None:
        self._history = []
        self.save_history()

    def filter_history(self, author: str = "", topic: str = "") -> list[HistoryEntry]:
        author = author.strip().lower()
        topic = topic.strip().lower()

        filtered = self._history
        if author:
            filtered = [item for item in filtered if author in item.quote.author.lower()]
        if topic:
            filtered = [item for item in filtered if topic in item.quote.topic.lower()]
        return filtered
