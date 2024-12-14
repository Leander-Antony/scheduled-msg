from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
scheduler = BackgroundScheduler()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.getenv('SMTP_USER')  
SMTP_PASS = os.getenv('SMTP_PASS')

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

start_scheduler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    email = request.form['email']
    message = request.form['message']
    datetime_str = request.form['datetime']

    send_time = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

    scheduler.add_job(
        send_email,
        'date',
        run_date=send_time,
        args=[email, message]
    )

    return redirect(url_for('index'))


def send_email(email, message):
    subject = "I am your past"
    sender = SMTP_USER
    html_content = f"<html><body><h1>{message}</h1></body></html>"

    try:
        msg = MIMEText(html_content, 'html')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(sender, [email], msg.as_string())
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
