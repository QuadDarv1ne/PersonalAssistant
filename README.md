# 🎙️ Voice Assistant with Real-Time Speech Recognition and Response

This is a real-time voice assistant built in Python using [OpenAI Whisper](https://github.com/openai/whisper), [WebRTC Voice Activity Detection (VAD)](https://github.com/wiseman/py-webrtcvad), and a local LLM server for generating responses. The assistant listens for speech when you press the spacebar, transcribes it using Whisper, sends the transcribed text to a chatbot endpoint, and optionally speaks the response aloud using gTTS.

## Features

- Real-time microphone input and recording
- On-device Whisper speech-to-text transcription
- Voice activity detection (VAD) for intelligent segmentation
- Chatbot response via local LLM API
- Text-to-speech response using `gTTS_module`
- Terminal theming (light/dark)
- Multithreaded design for responsive interaction
- **Conversation history** with context awareness
- **Web interface** for monitoring conversations
- **Multi-language support** for Whisper and TTS
- **Comprehensive logging** system
- **Configurable settings** via environment variables

## 📦 Dependencies

Install required libraries via pip:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install numpy sounddevice keyboard openai-whisper torch webrtcvad requests colorama gtts pygame flask
```

> You also need a working `gTTS_module.py` in the same directory with a function:  
> `text_to_speech_withEsc(text: str)` that plays audio and exits on `Esc`.

## 🛠️ Usage

1. **Run the script**:
   ```bash
   python pers_assist.py
   ```

2. **Press the `Space` key** to toggle voice recording.

3. **Speak** into your microphone. When you stop talking, the assistant transcribes your speech and responds.

4. The assistant **prints the response** in the terminal and **speaks it aloud**.

5. **Web interface** is available at `http://localhost:5000` for viewing conversation history.

## 📡 LLM Chatbot Backend

You can use this assistant with a local language model by installing [LM Studio](https://lmstudio.ai), which provides an easy interface for running models locally.

For example, you can load and serve the model [`google/gemma-3-4b`] in LM Studio.

Make sure LM Studio is configured to serve an OpenAI-compatible API at:

```
http://localhost:1234/v1/chat/completions
```

This assistant expects a local language model server running at:

```
http://localhost:1234/v1/chat/completions
```

The request format sent is:
```json
{
  "messages": [{"role": "user", "content": "your question"}]
}
```

Make sure your backend server supports this structure (e.g. OpenAI-compatible).

## 🧠 Model Selection

Whisper models supported:
- `tiny`, `base`, `small`, `medium`, `large`, etc.
- `.en` suffix for English-only variants, etc.

## 🎨 Themes

Two terminal color themes are available:
- `"light"` (default)
- `"dark"`

You can switch by changing:
```python
THEME = THEMES["light"]
```

## 🧩 File Structure
```
├── pers_assist.py         # Main application
├── gTTS_module.py         # Text-to-speech utility
├── config.py              # Configuration settings
├── logger.py              # Logging system
├── conversation_history.py # Conversation history management
├── web_interface.py       # Web interface with Flask
├── test_pers_assist.py    # Unit tests
├── requirements.txt       # Python dependencies
├── conversation_history.json # Saved conversation history
├── assistant.log          # Log file
├── templates/
│   └── index.html         # Web interface template
├── README.md              # This file
└── LICENSE                # License file
```

## ⚙️ Configuration

Settings can be customized in `config.py`:

- `SAMPLE_RATE`: Audio sample rate (default: 16000)
- `WHISPER_MODEL`: Whisper model size (default: "medium")
- `LLM_URL`: Local LLM server URL
- `DEFAULT_THEME`: Terminal theme ("light" or "dark")
- `LANGUAGE`: Language for Whisper transcription (default: "en")
- `TTS_LANGUAGE`: Language for text-to-speech (default: "en")

You can also set environment variables:
- `WHISPER_MODEL`: Override Whisper model
- `LLM_URL`: Override LLM server URL
- `LANGUAGE`: Override transcription language
- `TTS_LANGUAGE`: Override TTS language
- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Set log file path
## 🧪 Testing

Run unit tests:

```bash
python -m unittest test_pers_assist.py
```

## 📄 License

General Public License. See `LICENSE` file for details.

---
Join and have fun!

