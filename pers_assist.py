import numpy as np
import sounddevice as sd
import keyboard
import whisper
import threading
import time
import torch
import webrtcvad
import requests
from colorama import Fore, Style, init
import re
import gTTS_module
from typing import List, Dict, Any, Optional
import config
import logger
import conversation_history
import web_interface
import os


# Инициализация colorama для цветного вывода в терминал
init(autoreset=True)

# === Цветовые темы ===
THEMES: Dict[str, Dict[str, str]] = {
    "light": {  
        "user": Fore.BLUE,
        "assistant": Fore.LIGHTBLACK_EX,
        "thinking": Fore.MAGENTA,
        "background": Style.BRIGHT,
        "prompt": "Light"
    },
    "dark": {
        "user": Fore.CYAN,
        "assistant": Fore.LIGHTGREEN_EX,
        "thinking": Fore.YELLOW,
        "background": Style.DIM,
        "prompt": "Dark"
    }
}

THEME: Dict[str, str] = THEMES[config.DEFAULT_THEME]
# print(f"\n✅ {THEME['prompt']} theme is active\n")

# --- Настройки ---
SAMPLE_RATE = config.SAMPLE_RATE
CHANNELS = config.CHANNELS
DTYPE = np.dtype(config.DTYPE)

SEGMENT_DURATION = config.SEGMENT_DURATION  # 20 мс для VAD
SEGMENT_SAMPLES = config.SEGMENT_SAMPLES

SILENCE_TIMEOUT = config.SILENCE_TIMEOUT      # секунды ожидания перед новой строкой

# ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo']
# --- Инициализация модели Whisper с поддержкой CUDA ---
device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"[Device used]: {device.upper()}")
model = whisper.load_model(config.WHISPER_MODEL).to(device)  # Можно также указать устройство: whisper.load_model("small", device="cpu")

# --- Инициализация VAD ---
vad = webrtcvad.Vad()
vad.set_mode(3)  # чувствительность 0 - высокая, 3 - низкая

def is_speech(frame_bytes: bytes) -> bool:
    try:
        return vad.is_speech(frame_bytes, SAMPLE_RATE)
    except:
        return False

# --- Глобальные переменные ---
recording = False
audio_buffer = []
buffer_index = 0
lock = threading.Lock()
last_speech_time = None

# --- Callback для записи ---
def callback(indata: np.ndarray, frames: int, time: Any, status: Any) -> None:
    if recording:
        with lock:
            audio_buffer.extend(indata.copy().flatten())

# --- Управление записью аудио ---
def record_audio():
    global recording
    logger.log_with_color('INFO', "Нажмите Пробел для начала записи, Q для выхода, C для очистки истории...", logger.Colors.CYAN)
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=DTYPE, callback=callback):
        while True:
            if keyboard.is_pressed('space'):
                toggle_recording()
                while keyboard.is_pressed('space'):
                    pass
            elif keyboard.is_pressed('q'):
                logger.log_with_color('INFO', "Выход по команде пользователя.", logger.Colors.YELLOW)
                os._exit(0)  # Принудительный выход
            elif keyboard.is_pressed('c'):
                conversation_history.history.history.clear()
                conversation_history.history.save_history()
                logger.log_with_color('INFO', "История очищена.", logger.Colors.GREEN)
                while keyboard.is_pressed('c'):
                    pass
            time.sleep(0.1)

def toggle_recording():
    global recording, audio_buffer, buffer_index
    global speech_segment, speech_started, new_line_pending, current_pause, last_speech_time

    recording = not recording
    if recording:
        logger.log_with_color('INFO', "[Запись начата...]", logger.Colors.GREEN)
        audio_buffer.clear()
        buffer_index = 0

        # Сброс состояния VAD
        speech_segment = []
        speech_started = False
        new_line_pending = False
        current_pause = 0.0
        last_speech_time = time.time()  # ← обновить время начала
    else:
        logger.log_with_color('INFO', "[Запись остановлена.]", logger.Colors.YELLOW)

def generate_response(text: str) -> str:
    try:
        # Получить контекст из истории
        context = conversation_history.history.get_recent_context(3)
        full_prompt = f"{context}\n\nПользователь: {text}\nАссистент:" if context else text

        data = {
            "messages": [
                {"role": "user", "content": full_prompt}
            ],
            # "temperature": 0.0,        # минимальная случайность
            # "max_tokens": 10,          # минимальное количество токенов
            # "stream": False,           # отключить потоковую передачу
            # "stop": ["\n"]             # остановка после первой строки
        }

        response = requests.post(
            config.LLM_URL,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        assist_reply = response.json()['choices'][0]['message']['content']
        # Удалить теги и содержимое между ними
        # cleaned_text = re.sub(r'\<think\>.*?<\</think\>', '', assist_reply, flags=re.DOTALL)
        # print("Assistant response:", assist_reply)

        # Сохранить в историю
        conversation_history.history.add_entry(text, assist_reply)

        return assist_reply
    except requests.RequestException as e:
        logger.log_with_color('ERROR', f"Не удалось получить ответ от сервера LLM: {e}")
        return "Извините, я не смог сгенерировать ответ прямо сейчас."
    except (KeyError, IndexError) as e:
        logger.log_with_color('ERROR', f"Неожиданный формат ответа: {e}")
        return "Извините, я получил неожиданный ответ."

# === Анимация загрузки ===
def loading_animation(duration: float = 1, text: str = "Думаю") -> None:
    symbols = ['⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽', '⣾']
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        print(f"\r{THEME['thinking']}[{symbols[idx % len(symbols)]}] {text}{Style.RESET_ALL}", end="")
        idx += 1
        time.sleep(0.1)
    print(" " * (len(text) + 6), end="\r")  # Очистить строку

def process_stream():
    global last_speech_time, buffer_index
    global speech_segment, speech_started, new_line_pending, current_pause
    global recording

    while True:
        if not recording:
            time.sleep(0.5)
            continue
        question_text = ""
        with lock:
            available = len(audio_buffer)

        while buffer_index + SEGMENT_SAMPLES <= available:
            segment = audio_buffer[buffer_index:buffer_index + SEGMENT_SAMPLES]
            buffer_index += SEGMENT_SAMPLES

            segment_np = np.array(segment, dtype=np.int16)
            frame_bytes = segment_np.tobytes()

            try:
                is_silence = not is_speech(frame_bytes)

                if not is_silence:
                    speech_segment.extend(segment)
                    speech_started = True
                    new_line_pending = False
                    last_speech_time = time.time()  # ← обновить время речи
                elif speech_started:
                    current_pause = time.time() - last_speech_time

                    if current_pause > SILENCE_TIMEOUT:
                        if speech_segment:
                            # Транскрибировать и вывести
                            audio_float = np.array(speech_segment, dtype=np.float32) / 32768.0
                            result = model.transcribe(audio_float, language=config.LANGUAGE, verbose=None)

                            text = result["text"].strip()
                            if text.startswith("Subtitle Editor"):  # Ошибка Whisper: реагирует на шум
                                text = ""
                                continue
                            question_text += " " + text
                            if text:
                                print(f"{THEME['user']}Вы: {Style.RESET_ALL}{text}", end=" ", flush=True)

                            speech_segment = []

                        print()  # Новая строка
                        speech_segment = []
                        speech_started = False
                        new_line_pending = False
                        # Генерировать ответ
                        loading_animation(text="Генерация ответа...")
                        response = generate_response(question_text)
                        print(f"{THEME['assistant']}Ассистент: {response}{Style.RESET_ALL}")
                        question_text = ""
                        recording = False
                        gTTS_module.text_to_speech_withEsc(response, lang=config.TTS_LANGUAGE)
                        recording = True

            except Exception as e:
                logger.log_with_color('ERROR', f"Ошибка в обработке потока: {e}")

        time.sleep(0.05)

# --- Точка входа ---
if __name__ == "__main__":
    try:
        config.validate_config()
        logger.log_with_color('INFO', "[Конфигурация валидна.]", logger.Colors.GREEN)
    except ValueError as e:
        logger.log_with_color('ERROR', f"Ошибка конфигурации: {e}")
        exit(1)
    
    logger.log_with_color('INFO', "[Приложение голосового ассистента запущено.]", logger.Colors.GREEN)

    # Запустить веб-интерфейс
    web_interface.start_web_interface(port=5000)

    threading.Thread(target=record_audio, daemon=True).start()
    threading.Thread(target=process_stream, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.log_with_color('INFO', "Выход.", logger.Colors.YELLOW)