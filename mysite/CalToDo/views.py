from django.shortcuts import render
from django.http import JsonResponse
import caldav
from datetime import datetime, timedelta
import vobject

USERNAME = 'rybott5000.5@gmail.com'
PASSWORD = 'evwy-hbqc-ssub-xunp'
URL = 'https://caldav.icloud.com/'

def get_calendar_data(request):
    start = request.GET.get("start")  # Expected format: "YYYY-MM-DD"
    end = request.GET.get("end")      # Expected format: "YYYY-MM-DD"

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
    return render(request,'test.html',context)
