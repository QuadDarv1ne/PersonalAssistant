import io, os, contextlib
from gtts import gTTS
# Подавить вывод
with open(os.devnull, 'w') as devnull, contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
    from playsound import playsound
from threading import Thread
import keyboard  # Для отслеживания клавиш


# Глобальная переменная для остановки воспроизведения
_playing = False


def text_to_speech(text: str, lang: str = 'en'):
    """
    Преобразует текст в речь и воспроизводит его.
    Можно остановить, вызвав stop_sound().
    """
    global _playing

    try:
        # Генерировать аудио в памяти
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Инициализировать Pygame и загрузить аудио из памяти
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()

        _playing = True

        # Ждать завершения воспроизведения или остановки
        while pygame.mixer.music.get_busy() and _playing:
            continue

        pygame.mixer.quit()

    except Exception as e:
        print(f"Ошибка во время синтеза речи: {e}")
    finally:
        _playing = False


def text_to_speech_withEsc(text: str, lang: str = 'en'):
    """
    Преобразует текст в речь и воспроизводит его.
    Воспроизведение можно остановить, нажав Esc.
    """
    try:
        # Генерировать аудио в памяти
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Инициализировать Pygame и загрузить аудио из памяти
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()

        # Воспроизводить до завершения или нажатия Esc
        while pygame.mixer.music.get_busy():
            if keyboard.is_pressed('esc'):
                pygame.mixer.music.stop()
                print("Воспроизведение остановлено (Esc)")
                break

        pygame.mixer.quit()

    except Exception as e:
        print(f"Ошибка во время синтеза речи: {e}")
    finally:
        pass


def speak_async(text: str, lang: str = 'ru'):
    """Воспроизводит речь асинхронно в отдельном потоке"""
    Thread(target=text_to_speech, args=(text, lang), daemon=True).start()


def stop_sound():
    """Останавливает текущее воспроизведение"""
    global _playing
    if _playing:
        pygame.mixer.music.stop()
        _playing = False
        print("Воспроизведение остановлено")


def listen_for_stop_key():
    """Начинает прослушивание клавиши Esc для остановки воспроизведения"""
    def key_listener():
        keyboard.wait('esc')  # Ждёт нажатия Esc
        stop_sound()

    Thread(target=key_listener, daemon=True).start()