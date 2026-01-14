import os

# Настройки аудио
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = 'int16'

# Настройки VAD
SEGMENT_DURATION = 0.02  # 20 мс для VAD
SEGMENT_SAMPLES = int(SAMPLE_RATE * SEGMENT_DURATION)
SILENCE_TIMEOUT = 1.5      # секунды ожидания перед новой строкой

# Модель Whisper
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'medium')

# Сервер LLM
LLM_URL = os.getenv('LLM_URL', 'http://localhost:1234/v1/chat/completions')

# Тема
DEFAULT_THEME = 'light'

# Язык для Whisper и TTS
LANGUAGE = os.getenv('LANGUAGE', 'en')  # 'en', 'ru', etc.
TTS_LANGUAGE = os.getenv('TTS_LANGUAGE', 'en')