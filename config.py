import os

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = 'int16'

# VAD settings
SEGMENT_DURATION = 0.02  # 20 ms for VAD
SEGMENT_SAMPLES = int(SAMPLE_RATE * SEGMENT_DURATION)
MIN_SPEECH_CHUNKS = 10     # minimum consecutive voice segments
SILENCE_TIMEOUT = 1.5      # seconds to wait before new line

# Whisper model
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'medium')

# LLM server
LLM_URL = os.getenv('LLM_URL', 'http://localhost:1234/v1/chat/completions')

# Theme
DEFAULT_THEME = 'light'