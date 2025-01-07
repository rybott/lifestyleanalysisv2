from django.shortcuts import render
from django.http import JsonResponse
import caldav
from datetime import datetime, timedelta
import vobject
import json
import logging

logger = logging.getLogger(__name__)

USERNAME = 'rybott5000.5@gmail.com'
PASSWORD = 'evwy-hbqc-ssub-xunp'
URL = 'https://caldav.icloud.com/'

def get_calendar_data(request):
    start = request.GET.get("start")  # Expected format: "YYYY-MM-DD"
    end = request.GET.get("end")      # Expected format: "YYYY-MM-DD"

    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)
    except:
        today = datetime.today()
        if not start:
            start_date = datetime(today.year, today.month, 1)  # First day of current month
        else:
            start_date = datetime.strptime(start, "%Y-%m-%d")

        if not end:
            # Last day of the current month
            next_month = datetime(today.year, today.month, 28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
        else:
            end_date = datetime.strptime(end, "%Y-%m-%d")

    # Connect to CalDAV and fetch events
    client = caldav.DAVClient(url=URL, username=USERNAME, password=PASSWORD)
    principal = client.principal()
    calendars = principal.calendars()

    calendar = next((cal for cal in calendars if cal.name.lower() == 'home'), None)
    if not calendar:
        return JsonResponse({"error": "The 'home' calendar was not found."}, status=404)

    events = calendar.date_search(start=start_date, end=end_date)

    # Format events for FullCalendar.js
    formatted_events = []
    for event in events:
        try:
            # Parse the raw iCalendar data
            cal = vobject.readOne(event.data)

            # Extract event details
            uid = cal.vevent.uid.value
            summary = cal.vevent.summary.value
            dtstart = cal.vevent.dtstart.value
            dtend = cal.vevent.dtend.value if hasattr(cal.vevent, 'dtend') else None
            description = cal.vevent.description.value if hasattr(cal.vevent, 'description') else None
            categories = cal.vevent.categories.value if hasattr(cal.vevent, 'categories') else None
            rrule = cal.vevent.rrule.value if hasattr(cal.vevent, 'rrule') else None

            # Add the event to the list
            formatted_events.append({
                "id": uid,
                "title": summary,
                "start": dtstart.isoformat(),
                "end": dtend.isoformat() if dtend else None,
                "description": description,
                "categories":categories,
                "rrule": rrule
            })
        except Exception as e:
            print(f"Error parsing event: {e}")

    return JsonResponse(formatted_events, safe=False)

def rendercal(request):
    context = {}
    return render(request,'testcal.html',context)

def add_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Save the event to your database here
        return JsonResponse({'status': 'success'})
def update_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Update the event in your database here
        return JsonResponse({'status': 'success'})
def delete_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client = caldav.DAVClient(url=URL, username=USERNAME, password=PASSWORD)
        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            return JsonResponse({"error": "No calendars found."}, status=404)

        calendar = next((cal for cal in calendars if cal.name.lower() == 'home'), None)
        if not calendar:
            return JsonResponse({"error": "The 'home' calendar was not found."}, status=404)
        event = calendar.get_event_by_uid(data['id'])
        event.delete()

        return JsonResponse({"status": "success"})
def save_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Sync event with Apple Calendar using CalDAV
            client = caldav.DAVClient(url=URL, username=USERNAME, password=PASSWORD)
            principal = client.principal()
            calendars = principal.calendars()

            if not calendars:
                return JsonResponse({"error": "No calendars found."}, status=404)

            # Find the 'home' calendar
            calendar = next((cal for cal in calendars if cal.name.lower() == 'home'), None)
            if not calendar:
                return JsonResponse({"error": "The 'home' calendar was not found."}, status=404)

            # Prepare the event data with description
            description = data.get('description', '')  # Default to an empty string if no description is provided
            event_data = f"""
            BEGIN:VCALENDAR
            VERSION:2.0
            BEGIN:VEVENT
            UID:{data['id'] or 'NEW'}
            DTSTART:{datetime.fromisoformat(data['start']).strftime('%Y%m%dT%H%M%SZ')}
            DTEND:{datetime.fromisoformat(data['end']).strftime('%Y%m%dT%H%M%SZ')}
            SUMMARY:{data['title']}
            DESCRIPTION:{description}
            END:VEVENT
            END:VCALENDAR
            """

            # Save the event to the calendar
            event = calendar.save_event(event_data)

            return JsonResponse({"status": "success", "event_id": event.uid})
        except Exception as e:
            logger.error(f"Failed to save event: {e}")
            return JsonResponse({"error": str(e)}, status=500)
