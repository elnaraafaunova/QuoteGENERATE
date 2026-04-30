import customtkinter as ctk
from tkinter import messagebox

from services.history_service import HistoryService
from services.quote_service import QuoteService


class QuoteGeneratorApp(ctk.CTk):
    def __init__(self, quote_service: QuoteService, history_service: HistoryService) -> None:
        super().__init__()
        self.quote_service = quote_service
        self.history_service = history_service

        self.title("Генератор случайных цитат")
        self.geometry("980x680")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self._build_ui()
        self._load_history()

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.quote_frame = ctk.CTkFrame(self)
        self.quote_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=12, pady=12)
        self.quote_frame.grid_columnconfigure(0, weight=1)

        self.quote_text_label = ctk.CTkLabel(
            self.quote_frame, text="Цитата: —", font=ctk.CTkFont(size=18, weight="bold"), wraplength=900, justify="left"
        )
        self.quote_text_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.quote_author_label = ctk.CTkLabel(self.quote_frame, text="Автор: —", font=ctk.CTkFont(size=15))
        self.quote_author_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.quote_topic_label = ctk.CTkLabel(self.quote_frame, text="Тема: —", font=ctk.CTkFont(size=15))
        self.quote_topic_label.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))

        self.generate_button = ctk.CTkButton(self, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_button.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        self.clear_history_button = ctk.CTkButton(self, text="Очистить историю", command=self.clear_history)
        self.clear_history_button.grid(row=1, column=1, sticky="ew", padx=12, pady=(0, 10))

        self.filters_frame = ctk.CTkFrame(self)
        self.filters_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 10))
        self.filters_frame.grid_columnconfigure((1, 3, 4), weight=1)

        ctk.CTkLabel(self.filters_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.author_filter_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="Введите автора")
        self.author_filter_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        ctk.CTkLabel(self.filters_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.topic_filter_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="Введите тему")
        self.topic_filter_entry.grid(row=0, column=3, padx=8, pady=8, sticky="ew")

        self.apply_filter_button = ctk.CTkButton(self.filters_frame, text="Применить фильтр", command=self.apply_filters)
        self.apply_filter_button.grid(row=0, column=4, padx=8, pady=8, sticky="ew")

        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=12, pady=(0, 10))
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(1, weight=1)

        self.history_count_label = ctk.CTkLabel(self.history_frame, text="Сгенерировано цитат: 0")
        self.history_count_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.history_textbox = ctk.CTkTextbox(self.history_frame, state="disabled", wrap="word")
        self.history_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.add_quote_frame = ctk.CTkFrame(self)
        self.add_quote_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))
        self.add_quote_frame.grid_columnconfigure((1, 3, 5), weight=1)

        ctk.CTkLabel(self.add_quote_frame, text="Новая цитата:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.new_text_entry = ctk.CTkEntry(self.add_quote_frame, placeholder_text="Текст цитаты")
        self.new_text_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        ctk.CTkLabel(self.add_quote_frame, text="Автор:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.new_author_entry = ctk.CTkEntry(self.add_quote_frame, placeholder_text="Имя автора")
        self.new_author_entry.grid(row=0, column=3, padx=8, pady=8, sticky="ew")

        ctk.CTkLabel(self.add_quote_frame, text="Тема:").grid(row=0, column=4, padx=8, pady=8, sticky="w")
        self.new_topic_entry = ctk.CTkEntry(self.add_quote_frame, placeholder_text="Тема цитаты")
        self.new_topic_entry.grid(row=0, column=5, padx=8, pady=8, sticky="ew")

        self.add_quote_button = ctk.CTkButton(self.add_quote_frame, text="Добавить цитату", command=self.add_quote)
        self.add_quote_button.grid(row=0, column=6, padx=8, pady=8)

    def _load_history(self) -> None:
        ok, error_message = self.history_service.load_history()
        if not ok:
            messagebox.showerror("Ошибка", error_message)
        self.render_history(self.history_service.history)

    def generate_quote(self) -> None:
        quote = self.quote_service.get_random_quote()
        self.quote_text_label.configure(text=f"Цитата: {quote.text}")
        self.quote_author_label.configure(text=f"Автор: {quote.author}")
        self.quote_topic_label.configure(text=f"Тема: {quote.topic}")
        self.history_service.add_to_history(quote)
        self.render_history(self.history_service.filter_history(
            author=self.author_filter_entry.get(),
            topic=self.topic_filter_entry.get(),
        ))

    def add_quote(self) -> None:
        try:
            quote = self.quote_service.add_quote(
                text=self.new_text_entry.get(),
                author=self.new_author_entry.get(),
                topic=self.new_topic_entry.get(),
            )
            messagebox.showinfo("Успех", "Цитата успешно добавлена.")
            self.new_text_entry.delete(0, "end")
            self.new_author_entry.delete(0, "end")
            self.new_topic_entry.delete(0, "end")
            self.quote_text_label.configure(text=f"Цитата: {quote.text}")
            self.quote_author_label.configure(text=f"Автор: {quote.author}")
            self.quote_topic_label.configure(text=f"Тема: {quote.topic}")
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))

    def apply_filters(self) -> None:
        filtered = self.history_service.filter_history(
            author=self.author_filter_entry.get(),
            topic=self.topic_filter_entry.get(),
        )
        self.render_history(filtered)

    def clear_history(self) -> None:
        self.history_service.clear_history()
        self.render_history([])
        messagebox.showinfo("Информация", "История очищена.")

    def render_history(self, entries) -> None:
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")

        for index, entry in enumerate(entries, start=1):
            row = (
                f"{index}. {entry.quote.text}\n"
                f"   Автор: {entry.quote.author}\n"
                f"   Тема: {entry.quote.topic}\n"
                f"   Время: {entry.generated_at}\n"
                "----------------------------------------\n"
            )
            self.history_textbox.insert("end", row)

        self.history_textbox.configure(state="disabled")
        self.history_count_label.configure(text=f"Сгенерировано цитат: {len(self.history_service.history)}")
