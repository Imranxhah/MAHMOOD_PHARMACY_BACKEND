import os
import django
import sys

sys.path.append(r'C:\Users\kpk laptops\Desktop\MAHMOOD_PHARMACY_BACKEND')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
users_with_token = User.objects.exclude(fcm_token__isnull=True).exclude(fcm_token='').count()

with open("token_count.txt", "w") as f:
    f.write(f"Users with FCM token: {users_with_token}\n")
    if users_with_token == 0:
        f.write("WARNING: No users have an FCM token registered.\n")
