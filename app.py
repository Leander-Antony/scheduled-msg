from flask import Flask, render_template, request, redirect, url_for
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
from dotenv import load_dotenv
import os

app = Flask(__name__)
scheduler = BackgroundScheduler()

load_dotenv()

api_key = os.getenv('API_KEY')

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['apiKey'] = api_key 


api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

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
        print(api_response)  
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")


if __name__ == '__main__':
    app.run(debug=True)
