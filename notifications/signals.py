from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging
from .models import Notification, BroadcastNotification
import logging

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('notification_debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@receiver(post_save, sender=Notification)
def send_push_on_notification_creation(sender, instance, created, **kwargs):
    """
    Trigger a Firebase Push Notification whenever a Notification object is created.
    """
    if created:
        logger.info(f"Notification created: {instance.title} for user {instance.user.id}")
        if instance.user.fcm_token:
            logger.info(f"User has FCM token: {instance.user.fcm_token[:10]}...")
            
            # Calculate unread count for badge
            unread_count = Notification.objects.filter(user=instance.user, is_read=False).count()
            
            try:
                # Create the message with Android-specific configuration
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=instance.title, 
                        body=instance.body
                    ),
                    data={
                        "click_action": "FLUTTER_NOTIFICATION_CLICK",
                        "title": str(instance.title),
                        "body": str(instance.body),
                        "type": "order_update", 
                        "order_id": str(instance.id),
                        "badge": str(unread_count), # Send current unread count
                    },
                    android=messaging.AndroidConfig(
                        priority='high',
                        notification=messaging.AndroidNotification(
                            channel_id='high_importance_channel',
                            click_action='FLUTTER_NOTIFICATION_CLICK',
                        ),
                    ),
                    token=instance.user.fcm_token,
                )
                response = messaging.send(message)
                logger.info(f"Successfully sent push: {response}")
            
            except messaging.UnregisteredError:
                logger.warning(f"Token {instance.user.fcm_token[:10]}... is invalid/unregistered. Removing from user.")
                instance.user.fcm_token = None
                instance.user.save()
            except messaging.SenderIdMismatchError:
                logger.warning(f"Token {instance.user.fcm_token[:10]}... mismatch. Removing from user.")
                instance.user.fcm_token = None
                instance.user.save()
            except Exception as e:
                logger.error(f"Error sending custom push: {e}", exc_info=True)
        else:
            logger.warning(f"User {instance.user.id} has no FCM token.")

@receiver(post_save, sender=BroadcastNotification)
def send_broadcast_push(sender, instance, created, **kwargs):
    """
    Trigger a Firebase TOPIC Push Notification when a BroadcastNotification is created.
    Topic: 'all_users'
    """
    if created:
        logger.info(f"BroadcastNotification created: {instance.title}")
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=instance.title, 
                    body=instance.body
                ),
                topic='all_users',
            )
            response = messaging.send(message)
            logger.info(f"Successfully sent broadcast: {response}")

            # Persist to database for all users so it appears in history
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users = User.objects.all()
            
            notifications_to_create = [
                Notification(
                    user=user, 
                    title=instance.title, 
                    body=instance.body
                ) for user in users
            ]
            
            # Use bulk_create for performance
            Notification.objects.bulk_create(notifications_to_create)
            logger.info(f"Created {len(notifications_to_create)} database notifications for broadcast.")

        except Exception as e:
            logger.error(f"Error sending broadcast push: {e}", exc_info=True)
