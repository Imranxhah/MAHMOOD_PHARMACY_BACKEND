# Notification System Design for Mahmood Pharmacy

To implement notifications for your Flutter app, the **industry standard** and best approach is a **Hybrid Architecture**:
1.  **Push Notifications (FCM)**: Use **Firebase Cloud Messaging** to wake up the phone and show a system-tray notification when the app is closed.
2.  **In-App History (Database)**: Store notifications in your Django database so users can see a "Notification Center" inside the app (like "Order #123 has been shipped").

---

## 🏗️ 1. Architecture Overview

### **A. Backend (Django)**
*   **Packet**: `firebase-admin` SDK.
*   **Models**: 
    *   **User Model**: Needs to store `fcm_token` (the ID of the user's phone).
    *   **Notification Model**: Stores history (`title`, `body`, `is_read`, `timestamp`).
*   **Triggers**: Use **Django Signals** (`post_save`) on `Order` and `Prescription` models to automatically send notifications when status changes.

### **B. Frontend (Flutter)**
*   **Plugin**: `firebase_messaging`.
*   **Logic**:
    1.  On App Start: Get `fcm_token` from Firebase.
    2.  Send this token to Backend API (`POST /api/notifications/register-device/`).
    3.  Listen for incoming messages.

---

## 🛠️ 2. Implementation Steps

### **Step 1: Firebase Setup (Console)**
1.  Go to [Firebase Console](https://console.firebase.google.com/).
2.  Create a project "Mahmood Pharmacy".
3.  Add an **Android App** (package name must match your Flutter `android/app/build.gradle`).
4.  Download `google-services.json` and put it in `android/app/`.
5.  Go to **Project Settings > Service Accounts**.
6.  Generate **New Private Key**. Download the JSON file (e.g., `serviceAccountKey.json`).
7.  **IMPORTANT**: Place this JSON file in your Django project root (add to `.gitignore`!).

### **Step 2: Backend Dependencies**
Install the Firebase Admin SDK:
```bash
pip install firebase-admin
```

### **Step 3: Database Changes**

#### **1. Update User Model (or Profile)**
You need a place to save the mobile device token.
*Option A (Simple)*: Add `fcm_token` to `User`.
*Option B (Robust)*: Create a `Device` model (allows one user to have multiple phones).
*Recommendation*: Start with **Option A** for simplicity if users mostly use one phone.

#### **2. Create Notification Model**
```python
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional: Link to related object
    # order = models.ForeignKey('orders.Order', null=True, blank=True...)
```

### **Step 4: API Endpoints**

You need two new endpoints:

1.  **`POST /api/notifications/register-token/`**
    *   **Input**: `{ "fcm_token": "d7x8s..." }`
    *   **Action**: Save this token to the `User` model.
    

2.  **`GET /api/notifications/`**
    *   **Response**: List of past notifications for the user.
    *   **Action**: Backend returns list, App displays in "Notification Center".

### **Step 5: The "Signal" (Automation Logic)**

In `orders/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging
from .models import Order

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    if not created: # Only on updates
        # Check if status changed (logic requires tracking previous state)
        # Assuming we just notify on every save for now:
        
        user = instance.user
        if user.fcm_token:
            title = "Order Update"
            body = f"Your order #{instance.id} is now {instance.status}."
            
            # 1. Send to Firebase
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                token=user.fcm_token,
            )
            messaging.send(message)
            
            # 2. Save to Database
            Notification.objects.create(user=user, title=title, body=body)
```

---

## 🚀 Summary of Work Required
1.  **Firebase**: Create project & get credentials.
2.  **Django**: Install SDK, add Models, create `signals.py`, make API ViewSets.
3.  **Flutter**: Implement `firebase_messaging` and call the register-token API.

**Shall I proceed with implementing the Backend portion (Models + API + Signals)?**
