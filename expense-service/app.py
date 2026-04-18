from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os
from datetime import datetime

app = Flask(__name__)
CORS(app)

EXPENSES_FILE = 'expenses.json'

def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return {}
    with open(EXPENSES_FILE, 'r') as f:
        return json.load(f)

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses, f)

@app.route('/add', methods=['POST'])
def add_expense():
    data = request.json
    expenses = load_expenses()
    email = data['email']
    if email not in expenses:
        expenses[email] = []
    expense = {
        'id': len(expenses[email]) + 1,
        'title': data['title'],
        'amount': data['amount'],
        'category': data['category'],
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    expenses[email].append(expense)
    save_expenses(expenses)
    return jsonify({'message': 'Expense added!', 'expense': expense})

@app.route('/get/<email>', methods=['GET'])
def get_expenses(email):
    expenses = load_expenses()
    return jsonify({'expenses': expenses.get(email, [])})

@app.route('/delete/<email>/<int:expense_id>', methods=['DELETE'])
def delete_expense(email, expense_id):
    expenses = load_expenses()
    if email in expenses:
        expenses[email] = [e for e in expenses[email] if e['id'] != expense_id]
        save_expenses(expenses)
    return jsonify({'message': 'Deleted!'})

@app.route('/total/<email>', methods=['GET'])
def get_total(email):
    expenses = load_expenses()
    user_expenses = expenses.get(email, [])
    total = sum(e['amount'] for e in user_expenses)
    return jsonify({'total': total, 'expenses': user_expenses})

if __name__ == '__main__':
    app.run(port=5002, debug=True)