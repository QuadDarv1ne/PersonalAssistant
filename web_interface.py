from flask import Flask, render_template, request, jsonify
import threading
import time
import conversation_history

app = Flask(__name__)

@app.route('/settings')
def settings():
    """Страница настроек"""
    return render_template('settings.html')

@app.route('/api/history', methods=['GET'])
def get_history():
    """Получить историю разговоров"""
    return jsonify(conversation_history.history.history[-10:])  # Последние 10 записей

@app.route('/api/settings', methods=['POST'])
def save_settings():
    """Сохранение настроек"""
    data = request.json
    # В будущем можно сохранить в файл или переменные окружения
    # Пока просто возвращаем успех
    return jsonify({'status': 'success'})

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