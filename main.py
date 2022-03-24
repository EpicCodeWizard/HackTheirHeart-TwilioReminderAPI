# Imports.
"""
flask - API
twilio - Send Messages
replit - Database Management
os - Store/Fetch Secrets
"""
from flask import Flask, request
from twilio.rest import Client
from replit import db
import os

app = Flask(__name__, template_folder="", static_folder="")
client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

@app.route("/date/create", methods=["POST"])
def createDate():
    data = request.json
    # Send a message to both phone numbers.
    client.messages.create(messaging_service_sid=os.environ["TWILIO_MESSAGING_SERVICE_SID"], body="Don't miss your date in 10 minutes!", send_at=data["date"]+":00Z", schedule_type="fixed", to="+"+str(data["phone1"]))
    client.messages.create(messaging_service_sid=os.environ["TWILIO_MESSAGING_SERVICE_SID"], body="Don't miss your date in 10 minutes!", send_at=data["date"]+":00Z", schedule_type="fixed", to="+"+str(data["phone2"]))
    db['dates'].append(data)
    return ('', 204)

@app.route("/date/info/<phone1>/<phone2>", methods=["GET"])
def getDate(phone1, phone2):
    for date in db['dates']:
        tempdate = dict(date)
        if tempdate['phone1'] == int(phone1) and tempdate['phone2'] == int(phone2):
            return tempdate
    return ('', 204)

app.run(host="0.0.0.0")
