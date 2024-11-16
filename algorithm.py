from flask import Flask, request, jsonify

app = Flask(__name__)

# Пример алгоритма совместимости
def calculate_compatibility(user_cosmogram, group_cosmograms):
    results = []
    for person in group_cosmograms:
        # Фиктивный расчет совместимости
        score = 42  # Пример: фиксированное значение
        results.append({"name": person.get("name", "Unknown"), "score": score})
    return results

@app.route('/algorithm', methods=['POST'])
def algorithm_endpoint():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    user_cosmogram = data.get("user_cosmogram")
    group_cosmograms = data.get("group_cosmograms")

    if not user_cosmogram or not group_cosmograms:
        return jsonify({"error": "Missing data"}), 400

    # Вызываем алгоритм
    results = calculate_compatibility(user_cosmogram, group_cosmograms)
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
