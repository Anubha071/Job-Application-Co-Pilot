"""
NEW FEATURE: Calendar Integration Helper
Provides follow-up reminder scheduling for job applications.
Simulates calendar integration - in production, this would use Google Calendar API, etc.
Generates ICS files and reminder tracking.
"""
import os
import json
from datetime import datetime, timedelta
from typing import Optional
from icalendar import Calendar, Event
from dateutil import rrule


# BROKEN CODE: existing code had no calendar integration at all.
# This is a new feature for follow-up reminders after applying.


def generate_follow_up_ics(
    company_name: str,
    job_title: str,
    application_date: Optional[datetime] = None,
    reminder_days: int = 7
) -> str:
    """
    Generate an .ics calendar file for a follow-up reminder.
    
    Args:
        company_name: The company name
        job_title: The job title
        application_date: When the application was submitted (defaults to now)
        reminder_days: Days after application to send reminder (default: 7)
    
    Returns:
        File path to the generated .ics file
    """
    if application_date is None:
        application_date = datetime.utcnow()
    
    follow_up_date = application_date + timedelta(days=reminder_days)
    
    cal = Calendar()
    cal.add('prodid', '-//Job Application Co-Pilot//Follow Up//EN')
    cal.add('version', '2.0')
    
    event = Event()
    event.add('summary', f'Follow up: {job_title} at {company_name}')
    event.add('description', 
        f'Follow up on your job application for {job_title} at {company_name}.\n\n'
        f'Application submitted: {application_date.strftime("%Y-%m-%d")}\n\n'
        f'Suggested actions:\n'
        f'1. Send a polite follow-up email to the hiring manager\n'
        f'2. Check application status on company portal\n'
        f'3. Review your interview notes and preparation materials\n'
        f'4. Consider connecting with employees on LinkedIn'
    )
    event.add('dtstart', follow_up_date.date())
    event.add('dtend', follow_up_date.date() + timedelta(days=1))
    event.add('dtstamp', datetime.utcnow())
    event.add('priority', 5)
    
    cal.add_component(event)
    
    # Ensure directory exists
    ics_dir = os.path.join("generated", "calendars")
    os.makedirs(ics_dir, exist_ok=True)
    
    # Create safe filename
    safe_company = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in company_name)
    safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in job_title)
    filename = f"follow_up_{safe_company}_{safe_title}_{application_date.strftime('%Y%m%d')}.ics"
    file_path = os.path.join(ics_dir, filename)
    
    with open(file_path, 'wb') as f:
        f.write(cal.to_ical())
    
    return file_path


def get_reminder_suggestions() -> list:
    """
    Get suggested follow-up reminder intervals.
    """
    return [
        {"label": "3 days", "days": 3},
        {"label": "1 week", "days": 7},
        {"label": "2 weeks", "days": 14},
        {"label": "1 month", "days": 30},
    ]


def calculate_follow_up_status(application_date: datetime) -> dict:
    """
    Calculate the follow-up status for an application.
    
    Returns:
        dict with: days_since_application, should_follow_up, suggested_action
    """
    now = datetime.utcnow()
    days_since = (now - application_date).days
    
    if days_since < 3:
        return {
            "days_since": days_since,
            "should_follow_up": False,
            "suggested_action": "Wait at least 3-5 business days before following up.",
            "urgency": "low"
        }
    elif 3 <= days_since <= 7:
        return {
            "days_since": days_since,
            "should_follow_up": True,
            "suggested_action": "Good time to send a brief, polite follow-up email expressing continued interest.",
            "urgency": "medium"
        }
    elif 7 < days_since <= 14:
        return {
            "days_since": days_since,
            "should_follow_up": True,
            "suggested_action": "Send a follow-up email mentioning the date you applied and re-express interest.",
            "urgency": "medium"
        }
    else:
        return {
            "days_since": days_since,
            "should_follow_up": True,
            "suggested_action": "Consider sending a final check-in email or moving on to other opportunities.",
            "urgency": "high"
        }