from django.test import TestCase

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import CalendarEvent

def calendar_webhook(request):
    if request.method == "POST":
        # Parse the request data to extract the event information
        event_type = request.POST.get("event_type")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        event_name = request.POST.get("event_name")
        event_description = request.POST.get("event_description")
        
        if event_type == "cancel":
            # The event has been cancelled, so delete the corresponding reminder
            CalendarEvent.objects.filter(
                start_time=start_time,
                end_time=end_time,
                event_name=event_name,
                event_description=event_description
            ).delete()
        else:
            # The event has not been cancelled, so create a new calendar event and reminder
            event = CalendarEvent.objects.create(
                start_time=start_time,
                end_time=end_time,
                event_name=event_name,
                event_description=event_description
            )
            event.create_reminder()
        
        return HttpResponse("OK")
    else:
        return HttpResponse("Invalid request method")

# def create_event(request):
#     if request.method == "POST":
#         #
