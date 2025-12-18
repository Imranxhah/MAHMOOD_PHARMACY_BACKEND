import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
users = User.objects.all()

print(f"Total Users: {users.count()}")
print("-" * 50)
for user in users:
    print(f"User: {user.email} (ID: {user.id})")
    print(f"FCM Token: {user.fcm_token[:20]}..." if user.fcm_token else "FCM Token: None")
    print("-" * 50)
