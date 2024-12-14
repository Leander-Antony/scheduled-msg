from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import threading
from time import sleep
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')  # Ensure your SendGrid API key is in the .env file

def send_email_after_delay(email, message, delay):
    """Function to send email after the specified delay"""
    sleep(delay)  # Wait for the delay time in seconds
    send_email(email, message)

def send_email(email, message):
    """Function to send the email using SendGrid"""
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    email = request.form['email']
    message = request.form['message']
    datetime_str = request.form['datetime']

    # Convert the user-provided time to a datetime object
    send_time = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

    # Calculate the delay in seconds (current time to the user-selected time)
    delay = (send_time - datetime.now()).total_seconds()

    if delay > 0:
        # Schedule the email using a background thread
        threading.Thread(target=send_email_after_delay, args=(email, message, delay)).start()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
