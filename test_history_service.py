from models.quote import Quote
from services.history_service import HistoryService


def test_save_and_load_history(tmp_path):
    data_file = tmp_path / "data.json"
    service = HistoryService(str(data_file))
    quote = Quote(text="Тестовая цитата", author="Тестовый автор", topic="Тестовая тема")
    service.add_to_history(quote)

    loaded_service = HistoryService(str(data_file))
    ok, error = loaded_service.load_history()

    assert ok is True
    assert error == ""
    assert len(loaded_service.history) == 1
    assert loaded_service.history[0].quote.text == "Тестовая цитата"


def test_load_corrupted_json(tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("{bad json", encoding="utf-8")

    service = HistoryService(str(data_file))
    ok, error = service.load_history()

    assert ok is False
    assert error == "Ошибка загрузки данных: файл JSON поврежден."
    assert service.history == []


def test_filter_history_by_author_and_topic(tmp_path):
    data_file = tmp_path / "data.json"
    service = HistoryService(str(data_file))

    quote_1 = Quote(text="Первая", author="Лев Толстой", topic="Литература")
    quote_2 = Quote(text="Вторая", author="Антон Чехов", topic="Литература")
    quote_3 = Quote(text="Третья", author="Лев Толстой", topic="Жизнь")

    service.add_to_history(quote_1)
    service.add_to_history(quote_2)
    service.add_to_history(quote_3)

    by_author = service.filter_history(author="толстой")
    by_topic = service.filter_history(topic="литература")
    combined = service.filter_history(author="толстой", topic="жизнь")

    assert len(by_author) == 2
    assert len(by_topic) == 2
    assert len(combined) == 1
    assert combined[0].quote.text == "Третья"
