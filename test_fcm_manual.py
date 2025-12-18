import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from firebase_admin import messaging
from notifications.models import Notification

User = get_user_model()

def send_test_push(user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        print(f"User {user_id} not found.")
        return

    if not user.fcm_token:
        print(f"User {user.email} has no FCM token.")
        return

    print(f"Sending test notification to {user.email} (Token: {user.fcm_token[:10]}...)")

    try:
        # Mimic the exact payload from signals.py
        message = messaging.Message(
            notification=messaging.Notification(
                title="Test Notification", 
                body="This is a direct test message from the backend script."
            ),
            data={
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "title": "Test Notification",
                "body": "This is a direct test message from the backend script.",
                "type": "test_message", 
                "order_id": "0",
                "badge": "1",
            },
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    channel_id='high_importance_channel',
                    click_action='FLUTTER_NOTIFICATION_CLICK',
                ),
            ),
            token=user.fcm_token,
        )
        response = messaging.send(message)
        print(f"Successfully sent push: {response}")
    except Exception as e:
        print(f"Error sending push: {e}")

if __name__ == "__main__":
    # Default to User 13 as seen in logs, or take arg
    target_id = 13
    if len(sys.argv) > 1:
        target_id = int(sys.argv[1])
    
    send_test_push(target_id)
