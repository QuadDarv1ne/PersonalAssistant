import json
import os
from datetime import datetime
from typing import List, Dict, Any

HISTORY_FILE = 'conversation_history.json'

class ConversationHistory:
    def __init__(self, max_entries: int = 100):
        self.max_entries = max_entries
        self.history: List[Dict[str, Any]] = []
        self.load_history()

    def load_history(self):
        """Загрузить историю из файла"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка загрузки истории: {e}")
                self.history = []

    def save_history(self):
        """Сохранить историю в файл"""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history[-self.max_entries:], f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения истории: {e}")

    def add_entry(self, user_text: str, assistant_response: str):
        """Добавить новую запись в историю"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user_text,
            'assistant': assistant_response
        }
        self.history.append(entry)
        self.save_history()

    def get_recent_context(self, num_entries: int = 5) -> str:
        """Получить недавний контекст для LLM"""
        recent = self.history[-num_entries:]
        context = ""
        for entry in recent:
            context += f"Пользователь: {entry['user']}\nАссистент: {entry['assistant']}\n\n"
        return context.strip()

# Глобальный экземпляр истории
history = ConversationHistory()