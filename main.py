from services.history_service import HistoryService
from services.quote_service import QuoteService
from ui.app import QuoteGeneratorApp


def main() -> None:
    quote_service = QuoteService()
    history_service = HistoryService(data_path="data/data.json")
    app = QuoteGeneratorApp(quote_service=quote_service, history_service=history_service)
    app.mainloop()


if __name__ == "__main__":
    main()
