import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

users_with_token = User.objects.exclude(fcm_token__isnull=True).exclude(fcm_token__exact='')
print(f"Total users with FCM token: {users_with_token.count()}")
for user in users_with_token:
    print(f"User: {user.email}, Token: {user.fcm_token[:20]}...")
