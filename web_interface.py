from flask import Flask, render_template, request, jsonify
import threading
import time
import conversation_history

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница с интерфейсом"""
    return render_template('index.html')

@app.route('/api/history', methods=['GET'])
def get_history():
    """Получить историю разговоров"""
    return jsonify(conversation_history.history.history[-10:])  # Последние 10 записей

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Отправить текстовое сообщение и получить ответ"""
    data = request.json
    user_text = data.get('message', '').strip()
    if not user_text:
        return jsonify({'error': 'Сообщение не может быть пустым'}), 400
    
    # Импортировать функцию генерации ответа
    import pers_assist
    response = pers_assist.generate_response(user_text)
    return jsonify({'response': response})

def run_web_interface(port: int = 5000):
    """Запустить веб-интерфейс в отдельном потоке"""
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# Запуск веб-интерфейса
def start_web_interface(port: int = 5000):
    thread = threading.Thread(target=run_web_interface, args=(port,), daemon=True)
    thread.start()
    print(f"Веб-интерфейс запущен на http://localhost:{port}")

if __name__ == '__main__':
    start_web_interface()