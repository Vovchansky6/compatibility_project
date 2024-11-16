from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# URL вашего REST API (на Go)
API_URL = "http://localhost:8080/api/compatibility"

# Главная страница с формой для отправки данных
@app.route('/')
def index():
    return '''
        <h1>Тестирование API</h1>
        <form action="/send" method="post">
            <label>Космограмма пользователя (JSON):</label><br>
            <textarea name="user_cosmogram" rows="4" cols="50">{
    "birth_date": "2000-01-01",
    "location": "Moscow"
}</textarea><br><br>
            <label>Космограммы группы (JSON):</label><br>
            <textarea name="group_cosmograms" rows="4" cols="50">[
    {
        "name": "Alice",
        "birth_date": "1995-06-15",
        "location": "Berlin"
    },
    {
        "name": "Bob",
        "birth_date": "1990-03-22",
        "location": "Paris"
    }
]</textarea><br><br>
            <button type="submit">Отправить</button>
        </form>
    '''

# Обработчик отправки данных
@app.route('/send', methods=['POST'])
def send_request():
    # Получаем данные из формы
    user_cosmogram = request.form.get("user_cosmogram")
    group_cosmograms = request.form.get("group_cosmograms")

    # Проверяем, что данные заполнены
    if not user_cosmogram or not group_cosmograms:
        return "Пожалуйста, заполните оба поля.", 400

    try:
        # Преобразуем строки JSON в Python-объекты
        user_cosmogram = eval(user_cosmogram)
        group_cosmograms = eval(group_cosmograms)
    except Exception as e:
        return f"Ошибка обработки JSON: {e}", 400

    # Отправляем данные к REST API
    try:
        response = requests.post(API_URL, json={
            "user_cosmogram": user_cosmogram,
            "group_cosmograms": group_cosmograms
        })

        # Проверяем статус ответа
        if response.status_code != 200:
            return f"Ошибка API: {response.status_code} - {response.text}", 500

        # Возвращаем результат на страницу
        result = response.json()
        return jsonify(result)

    except Exception as e:
        return f"Ошибка запроса к API: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)  # Flask-приложение работает на порту 5001
