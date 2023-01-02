import base64
from collections import UserDict
from datetime import timedelta
from django.db import models

# Create your models here.
# models.py
# models.py
import requests
import scheduler

class CalendarEvent(models.Model):
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_name = models.CharField(max_length=255)
    event_description = models.TextField()
    
    def create_reminder(self):
        # Make a POST request to the Calendly API to create an appointment reminder
        api_token = "YOUR_API_TOKEN"
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
        data = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "event_name": self.event_name,
            "event_description": self.event_description
        }
        response = requests.post(
            "https://calendly.com/api/v1/appointment_reminders",
            headers=headers,
            data=data
        )
        
        # Check the response status code to see if the request was successful
        if response.status_code == 201:
            # The reminder was successfully created, so schedule an SMS message to be sent 15 minutes before the event
            reminder_time = self.start_time - timedelta(minutes=15)
            scheduler.schedule(
                reminder_time,
                send_sms_reminder,
                (self.user, self.event_name)
            )
            return True
        else:
            # There was an error creating the reminder
            return False

def send_sms_reminder(user, event_name):
    # Get the user's phone number and country code from the database or CSV file
    phone_number = user.phone_number
    country_code = user.country_code
    
    # Use a third-party SMS API to send the reminder message
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    message = f"This is a reminder that you have an event coming up at {event_name} in 15 minutes."
    send_sms(api_key, api_secret, message, phone_number, country_code)

def send_sms(api_key, api_secret, message, phone_number, country_code):
    # Use the API key and secret to authenticate the request
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{api_key}:{api_secret}'.encode()).decode()}"
    }
    
    # Set up the SMS payloadc:\Users\hp\AppData\Local\Programs\Microsoft VS Code\resources\app\out\vs\code\electron-sandbox\workbench\workbench.html
    data = {
        "from": "Calendar",
        "to": f"{country_code}{phone_number}",
        "text": message
    }
    
    # Make a POST request to the SMS API to send the message
    # response = requests.post(
    #     "https://
