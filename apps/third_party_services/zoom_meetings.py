import json
import requests
import base64
from django.conf import settings
from django.core.cache import cache


token_url = 'https://zoom.us/oauth/token'
account_id = settings.ZOOM_ACCOUNT_ID
client_id = settings.ZOOM_CLIENT_ID
client_secret = settings.ZOOM_CLIENT_SECRET


def get_zoom_access_token():
    access_token = cache.get('zoom_access_token')
    if access_token:
        print(f'Access token from cache: {access_token}')
        return access_token
    credentials = f'{client_id}:{client_secret}'
    base64_credentials = base64.b64encode(credentials.encode()).decode()
    data = {
        'grant_type': 'account_credentials',
        'account_id': account_id,
    }
    headers = {
        'Host': 'zoom.us',
        'Authorization': f'Basic {base64_credentials}',
    }
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        print(f'Access token from request: {access_token}')
        safety_margin = 60
        timeout = response.json()['expires_in'] - safety_margin
        cache.set('zoom_access_token', access_token, timeout=timeout)
        return access_token
    else:
        print(f'Zoom access token retrival error: {response.status_code} - {response.text}')


def create_zoom_meeting(topic: str, start_time: str, duration: int, service_slug: str):
    from apps.groupdiscussions.models import GroupDiscussion

    url = "https://api.zoom.us/v2/users/me/meetings"
    payload = json.dumps({
    "topic": f"{topic}",
    "type": 2,
    "start_time": f"{start_time}",
    "duration": duration,
    "settings": {
        "join_before_host": True,
        "jbh_time":5,
        "waiting_room":True  # waiting room enabled
        }
    })
    headers = {
    'Authorization': 'Bearer {}'.format(get_zoom_access_token()),
    'Content-Type': 'application/json',
    }
    print("slug is ",service_slug)
    print("payload is",payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print("created the meeting",response.json())
    meeting = {
        'meeting_id': response.json()['id'],
        'meeting_url': response.json()['join_url'],
        'meeting_password': response.json().get('password', ''),
    }
    return meeting


