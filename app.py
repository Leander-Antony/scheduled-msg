from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
scheduler = BackgroundScheduler()

# Get SendGrid API SMTP settings from environment variables
SENDGRID_SMTP_SERVER = 'smtp.sendgrid.net'
SENDGRID_SMTP_PORT = 587  # Use 587 for TLS
SENDGRID_USERNAME = 'apikey'  # SendGrid username is 'apikey'
SENDGRID_PASSWORD = '##'  # SendGrid API key as password

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
    sender = 'yourpastishereforyou@gmail.com'  # Replace with your sender email
    to_email = email
    html_content = f"<html><body><h1>{message}</h1></body></html>"

    msg = MIMEText(html_content, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    try:
        # Connect to SendGrid SMTP server
        with smtplib.SMTP(SENDGRID_SMTP_SERVER, SENDGRID_SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDGRID_USERNAME, SENDGRID_PASSWORD)
            server.sendmail(sender, [to_email], msg.as_string())
            print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
