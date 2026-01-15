from flask import Flask, render_template
import json
from email.message import EmailMessage
import os
import smtplib
from datetime import datetime


app = Flask(__name__)


EMAIL_ADDRESS = 'youremail@example.com' # replace with your email
EMAIL_PASSWORD = 'yourpassword' # replace with your email password


def load_json(name):
with open(name, 'r') as f:
return json.load(f)


def send_email(to_email, subject, body):
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = EMAIL_ADDRESS
msg['To'] = to_email
msg.set_content(body)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
smtp.send_message(msg)


def get_payment_status():
tenants = load_json('tenants.json')
transactions = load_json('transactions.json')
paid_ibans = {t['iban'] for t in transactions}
for tenant in tenants:
tenant['paid'] = tenant['iban'] in paid_ibans
return tenants


@app.route('/')
def dashboard():
tenants = get_payment_status()
return render_template('dashboard.html', tenants=tenants)


@app.route('/send_all_reminders')
def send_all_reminders():
tenants = get_payment_status()
unpaid_tenants = [t for t in tenants if not t['paid']]
count = 0
for tenant in unpaid_tenants:
try:
send_email(tenant['email'], "Rent Payment Reminder",
"Dear tenant,\n\nThis is a reminder to pay your rent.\n\nThank you!")
count += 1
except:
pass
return f"Reminders sent to {count} tenants."


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)