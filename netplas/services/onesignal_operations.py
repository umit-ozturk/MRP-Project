from requests.exceptions import HTTPError
from .onesignal.app_client import OneSignalAppClient
from .onesignal.notification import Notification
from django.conf import settings
import json


def send_push_to_devices(content, devices):
    """
    Initializes the OneSignal Client.

    :param content: Push notification text
    :type content: string
    :param devices: Player IDs array
    :type devices: list

    """
    client = OneSignalAppClient(app_api_key=settings.ONESIGNAL_REST_API_KEY)

    notification = Notification(settings.ONESIGNAL_APP_ID, Notification.DEVICES_MODE)
    notification.include_player_ids = list(devices)  # Must be a list!
    notification.content_available = True
    content_json = {}
    content_json['en'] = content

    notification.contents = json.dumps(content_json)

    try:
        result = client.create_notification(notification)
    except HTTPError as e:
        result = e.response.json()

    print(result)
# Success: {'id': '1d63fa3a-2205-314f-a734-a1de7e27cc2a', 'recipients': 1}
# Error:   {'errors': ['Invalid app_id format']} - or any other message
