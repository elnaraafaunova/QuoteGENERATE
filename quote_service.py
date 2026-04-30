import random

from models.quote import Quote


class QuoteService:
    def __init__(self) -> None:
        self._quotes = [
            Quote("Знание — сила", "Фрэнсис Бэкон", "Образование"),
            Quote("Делай сегодня то, что другие не хотят, завтра будешь жить так, как другие не могут.", "Джаред Лето", "Мотивация"),
            Quote("Счастье зависит от нас самих.", "Аристотель", "Жизнь"),
            Quote("Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "Уинстон Черчилль", "Успех"),
            Quote("Не ошибается только тот, кто ничего не делает.", "Теодор Рузвельт", "Развитие"),
            Quote("Воображение важнее знания.", "Альберт Эйнштейн", "Наука"),
            Quote("Будьте изменением, которое хотите видеть в мире.", "Махатма Ганди", "Общество"),
            Quote("Лучший способ предсказать будущее — создать его.", "Питер Друкер", "Будущее"),
        ]

    @property
    def quotes(self) -> list[Quote]:
        return self._quotes

    def get_random_quote(self) -> Quote:
        return random.choice(self._quotes)

    def add_quote(self, text: str, author: str, topic: str) -> Quote:
        text = text.strip()
        author = author.strip()
        topic = topic.strip() or "Без темы"

        if not text:
            raise ValueError("Цитата не может быть пустой")
        if not author:
            raise ValueError("Автор не может быть пустым")

        quote = Quote(text=text, author=author, topic=topic)
        self._quotes.append(quote)
        return quote
