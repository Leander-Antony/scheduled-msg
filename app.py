from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

app = Flask(__name__)
scheduler = BackgroundScheduler()

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')  # Ensure your SendGrid API key is in the .env file

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

    # Schedule the email to be sent at the specified time
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
    html_content = f"<html><body><h1>{message}</h1></body></html>"

    # Create a SendGrid Mail object
    message = Mail(
        from_email=sender,
        to_emails=email,
        subject=subject,
        html_content=html_content
    )

    try:
        # Send email using SendGrid API
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        # Print SendGrid response for debugging
        print(f"Email sent to {email}")
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
