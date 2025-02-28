from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin access

def get_due_date(send_date_str):
    send_date = datetime.strptime(send_date_str, "%Y-%m-%d")
    weekday = send_date.weekday()  # Monday = 0, Sunday = 6

    if weekday == 4:  # Friday send → Due Monday
        due_date = send_date + timedelta(days=3)
    elif weekday in [5, 6, 0]:  # Sat, Sun, Mon send → Due Tuesday
        due_date = send_date + timedelta(days=(1 if weekday == 0 else 2))
    elif weekday == 1:  # Tuesday send → Due Wednesday
        due_date = send_date + timedelta(days=1)
    elif weekday == 2:  # Wednesday send → Due Thursday
        due_date = send_date + timedelta(days=1)
    elif weekday == 3:  # Thursday send → Due Friday
        due_date = send_date + timedelta(days=1)

    preceding_due_date = due_date - timedelta(days=7)
    return preceding_due_date.strftime("%Y-%m-%d")

@app.route('/calculate_due_date', methods=['GET'])
def calculate_due_date():
    send_date = request.args.get('send_date')
    if not send_date:
        return jsonify({"error": "Missing send_date parameter"}), 400

    due_date = get_due_date(send_date)
    return jsonify({"send_date": send_date, "due_date": due_date})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
