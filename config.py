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

def validate_config():
    """Валидация конфигурации"""
    errors = []
    
    if SAMPLE_RATE not in [8000, 16000, 22050, 44100]:
        errors.append(f"Неподдерживаемая частота дискретизации: {SAMPLE_RATE}")
    
    if CHANNELS not in [1, 2]:
        errors.append(f"Неподдерживаемое количество каналов: {CHANNELS}")
    
    if WHISPER_MODEL not in ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo']:
        errors.append(f"Неподдерживаемая модель Whisper: {WHISPER_MODEL}")
    
    if DEFAULT_THEME not in ['light', 'dark']:
        errors.append(f"Неподдерживаемая тема: {DEFAULT_THEME}")
    
    if errors:
        raise ValueError("Ошибки конфигурации:\n" + "\n".join(errors))
    
    return True