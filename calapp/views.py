# views.py
from pyexpat.errors import messages

from django.shortcuts import redirect, render
from .models import CalendarEvent

def create_event(request):
    if request.method == "POST":
        # Create a new CalendarEvent object with the form data
        event = CalendarEvent.objects.create(
            user=request.user,
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
            event_name=request.POST["event_name"],
            event_description=request.POST["event_description"]
        )
        
        # Create an appointment reminder for the event
        if event.create_reminder():
            messages.success(request, "Event and reminder created successfully!")
        else:
            messages.error(request, "There was an error creating the event or reminder.")
            
        return redirect("calendar")
    else:
        # Render the create event form template
        return render(request, "create_event.html")
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
