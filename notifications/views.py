from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Notification, BroadcastNotification
from .serializers import NotificationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated] # Moved to get_permissions
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Notification.objects.filter(user=self.request.user).order_by('-created_at')
        return Notification.objects.none()

    def list(self, request, *args, **kwargs):
        # 1. Fetch Broadcast Notifications (for everyone)
        broadcasts = BroadcastNotification.objects.all().order_by('-created_at')
        broadcast_data = []
        for b in broadcasts:
            broadcast_data.append({
                "id": -b.id, # Use negative ID to distinguish from user notifications and avoid collision
                "title": b.title,
                "body": b.body,
                "is_read": False, # Broadcasts are effectively read-only/unread
                "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        # 2. Fetch User Notifications (if auth)
        user_data = []
        if request.user.is_authenticated:
            user_notifs = self.get_queryset()
            serializer = self.get_serializer(user_notifs, many=True)
            user_data = serializer.data
        
        # 3. Combine and Sort
        combined_data = broadcast_data + user_data
        # Sort by created_at descending (string comparison works for YYYY-MM-DD HH:MM:SS)
        combined_data.sort(key=lambda x: x['created_at'], reverse=True)

        return Response(combined_data)

    @action(detail=False, methods=['post'], url_path='register-device')
    def register_device(self, request):
        """
        Endpoint to register FCM Token.
        Payload: { "fcm_token": "..." }
        """
        fcm_token = request.data.get('fcm_token')
        if not fcm_token:
            return Response({"error": "fcm_token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.fcm_token = fcm_token
        user.save()
        
        return Response({"message": "Device registered successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='mark-all-read')
    def mark_all_read(self, request):
        """
        Mark all notifications as read.
        """
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"message": "All notifications marked as read"}, status=status.HTTP_200_OK)
