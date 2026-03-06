#!/usr/bin/env python3
"""
Google Calendar MCP Server — WaheedAI Solutions
Tools: create_event, get_events, check_availability, create_reminder
Uses same Gmail OAuth credentials
"""
import json
import os
import pickle
import sys
from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Calendar scope — add to existing Gmail scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
]

CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
TOKEN_PATH = os.getenv('GOOGLE_TOKEN_PATH', 'watchers/token.pickle')
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'

app = Server("calendar-mcp")


def get_calendar_service():
    """Get authenticated Google Calendar service"""
    creds = None

    if Path(TOKEN_PATH).exists():
        with open(TOKEN_PATH, 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)

    return build('calendar', 'v3', credentials=creds)


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_event",
            description="Create a Google Calendar event for client meetings or project deadlines",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Event title"},
                    "start_datetime": {"type": "string", "description": "Start datetime ISO format: 2026-03-10T10:00:00"},
                    "end_datetime": {"type": "string", "description": "End datetime ISO format: 2026-03-10T11:00:00"},
                    "description": {"type": "string", "description": "Event description or agenda"},
                    "attendee_email": {"type": "string", "description": "Client email to invite (optional)"},
                },
                "required": ["title", "start_datetime", "end_datetime"],
            },
        ),
        Tool(
            name="get_events",
            description="Get upcoming calendar events for CEO Briefing or schedule overview",
            inputSchema={
                "type": "object",
                "properties": {
                    "days_ahead": {"type": "integer", "description": "How many days ahead to fetch (default: 7)"},
                    "max_results": {"type": "integer", "description": "Max number of events to return (default: 10)"},
                },
                "required": [],
            },
        ),
        Tool(
            name="check_availability",
            description="Check free/busy slots before scheduling a meeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date to check availability: 2026-03-10"},
                    "duration_minutes": {"type": "integer", "description": "Meeting duration in minutes (default: 60)"},
                },
                "required": ["date"],
            },
        ),
        Tool(
            name="create_reminder",
            description="Create a reminder event for invoice follow-ups or task deadlines",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Reminder title"},
                    "remind_at": {"type": "string", "description": "Reminder datetime ISO format: 2026-03-17T09:00:00"},
                    "note": {"type": "string", "description": "Additional note for the reminder"},
                },
                "required": ["title", "remind_at"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "create_event":
        return await _create_event(arguments)
    elif name == "get_events":
        return await _get_events(arguments)
    elif name == "check_availability":
        return await _check_availability(arguments)
    elif name == "create_reminder":
        return await _create_reminder(arguments)
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def _create_event(args: dict) -> list[TextContent]:
    if DRY_RUN:
        return [TextContent(type="text", text=
            f"[DRY RUN] Would create event: {args['title']} "
            f"from {args['start_datetime']} to {args['end_datetime']}"
        )]

    try:
        service = get_calendar_service()
        event = {
            'summary': args['title'],
            'description': args.get('description', ''),
            'start': {'dateTime': args['start_datetime'], 'timeZone': 'Asia/Karachi'},
            'end': {'dateTime': args['end_datetime'], 'timeZone': 'Asia/Karachi'},
        }

        if args.get('attendee_email'):
            event['attendees'] = [{'email': args['attendee_email']}]

        result = service.events().insert(
            calendarId='primary', body=event, sendUpdates='all'
        ).execute()

        return [TextContent(type="text", text=
            f"✅ Event created: {result['summary']}\n"
            f"Link: {result.get('htmlLink', 'N/A')}\n"
            f"Event ID: {result['id']}"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error creating event: {e}")]


async def _get_events(args: dict) -> list[TextContent]:
    try:
        service = get_calendar_service()
        days_ahead = args.get('days_ahead', 7)
        max_results = args.get('max_results', 10)

        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return [TextContent(type="text", text=f"No events in next {days_ahead} days")]

        output = f"📅 Upcoming events (next {days_ahead} days):\n\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            output += f"• {event['summary']}\n  Start: {start}\n\n"

        return [TextContent(type="text", text=output)]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error fetching events: {e}")]


async def _check_availability(args: dict) -> list[TextContent]:
    try:
        service = get_calendar_service()
        date = args['date']
        duration = args.get('duration_minutes', 60)

        # Check 9 AM to 6 PM
        day_start = f"{date}T00:00:00Z"
        day_end = f"{date}T23:59:59Z"

        body = {
            "timeMin": day_start,
            "timeMax": day_end,
            "items": [{"id": "primary"}]
        }

        result = service.freebusy().query(body=body).execute()
        busy_slots = result['calendars']['primary']['busy']

        if not busy_slots:
            return [TextContent(type="text", text=
                f"✅ {date} is fully free! You can schedule a {duration}-minute meeting anytime."
            )]

        output = f"📅 Busy slots on {date}:\n"
        for slot in busy_slots:
            output += f"• {slot['start']} → {slot['end']}\n"
        output += f"\nSchedule meeting in any gap of {duration}+ minutes."

        return [TextContent(type="text", text=output)]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error checking availability: {e}")]


async def _create_reminder(args: dict) -> list[TextContent]:
    if DRY_RUN:
        return [TextContent(type="text", text=
            f"[DRY RUN] Would create reminder: {args['title']} at {args['remind_at']}"
        )]

    try:
        service = get_calendar_service()
        remind_dt = args['remind_at']

        # Reminder is a 15-minute event
        start = datetime.fromisoformat(remind_dt)
        end = start + timedelta(minutes=15)

        event = {
            'summary': f"⏰ REMINDER: {args['title']}",
            'description': args.get('note', ''),
            'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Karachi'},
            'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Karachi'},
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 0},
                    {'method': 'email', 'minutes': 30},
                ],
            },
        }

        result = service.events().insert(
            calendarId='primary', body=event
        ).execute()

        return [TextContent(type="text", text=
            f"✅ Reminder created: {args['title']}\n"
            f"At: {remind_dt}\n"
            f"Link: {result.get('htmlLink', 'N/A')}"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error creating reminder: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
