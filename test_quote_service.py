from models.quote import Quote
from services.quote_service import QuoteService


def test_random_selection_returns_expected_quote(monkeypatch):
    service = QuoteService()
    expected = Quote("Тест", "Автор", "Тема")
    service.quotes.append(expected)

    monkeypatch.setattr("services.quote_service.random.choice", lambda quotes: expected)
    result = service.get_random_quote()

    assert result == expected


def test_add_quote_validation():
    service = QuoteService()

    try:
        service.add_quote(text="", author="Автор", topic="Тема")
        assert False, "Ожидалась ошибка для пустой цитаты"
    except ValueError as exc:
        assert str(exc) == "Цитата не может быть пустой"

    try:
        service.add_quote(text="Текст", author="", topic="Тема")
        assert False, "Ожидалась ошибка для пустого автора"
    except ValueError as exc:
        assert str(exc) == "Автор не может быть пустым"
