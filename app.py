from flask import Flask, render_template, request, redirect, url_for
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
from dotenv import load_dotenv
import os

load_dotenv()
# Initialize Flask app and scheduler
app = Flask(__name__)
scheduler = BackgroundScheduler()

SENDINBLUE_API_KEY = os.getenv('API_KEY')
print(SENDINBLUE_API_KEY)
# Brevo (Sendinblue) API setup
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = SENDINBLUE_API_KEY   # Replace with your Brevo API key

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# Ensure the scheduler starts only once
def start_scheduler():
    if not scheduler.running:
        scheduler.start()

# Call start_scheduler manually when the app is run
start_scheduler()

# Route for the home page (email form)
@app.route('/')
def index():
    return render_template('index.html')

# Route for scheduling the email
@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    email = request.form['email']
    message = request.form['message']
    datetime_str = request.form['datetime']

    # Convert the datetime from the form to a datetime object
    send_time = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

    # Schedule the job
    scheduler.add_job(
        send_email,
        'date',
        run_date=send_time,
        args=[email, message]
    )

    return redirect(url_for('index'))  # Redirect back to home page

# Function to send email using Brevo
def send_email(email, message):
    subject = "I am your past"
    sender = {"name": "Your Past", "email": "yourpastishereforyou@gmail.com"}
    reply_to = {"name": "Your Past", "email": "yourpastishereforyou@gmail.com"}
    html_content = f"<html><body><h1>{message}</h1></body></html>"
    to = [{"email": email}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        reply_to=reply_to,
        html_content=html_content,
        sender=sender,
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent to {email}")
        print(api_response)  # Print the response from Brevo
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
