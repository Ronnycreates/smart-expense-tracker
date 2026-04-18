from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)


import os
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "susundrerohan@gmail.com")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "ojka qzrl wplj buqh")

def send_email(to_email, name, total, budget):
    subject = "⚠️ Budget Alert - Smart Expense Tracker"
    percent = round((total / budget) * 100)
    body = f"""
    Hi {name},

    This is an automated alert from your Smart Expense Tracker.

    📊 Budget Summary:
    - Monthly Budget : ₹{budget}
    - Total Spent    : ₹{total}
    - Used           : {percent}%
    - Remaining      : ₹{budget - total}

    {'🚨 WARNING: You have EXCEEDED your budget!' if total > budget else '⚠️ You are close to your budget limit!'}

    Please review your expenses.

    - Smart Expense Tracker (Cloud Microservice Alert System)
    """
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

@app.route('/check-budget', methods=['POST'])
def check_budget():
    data = request.json
    email = data['email']
    name = data['name']
    total = data['total']
    budget = data['budget']

    if total >= budget * 0.8:  # Alert when 80% budget used
        sent = send_email(email, name, total, budget)
        if sent:
            return jsonify({'alert': True, 'message': 'Budget alert email sent!'})
        else:
            return jsonify({'alert': True, 'message': 'Alert triggered but email failed. Check credentials.'})
    return jsonify({'alert': False, 'message': 'Budget is under control.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5003)))