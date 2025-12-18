# Notification API Guide

Base URL: `/api/notifications/` (Assuming main project routes `notifications/` to this app)

## 1. Register Device (FCM Token)
**Endpoint**: `POST /notifications/register-device/`

**Purpose**: Links the device's FCM token to the user account to enable push notifications.

**Request Body**:
```json
{
  "fcm_token": "YOUR_FCM_TOKEN_STRING"
}
```

**Response**:
- **200 OK**:
  ```json
  {
    "message": "Device registered successfully"
  }
  ```
- **400 Bad Request**: If `fcm_token` is missing.

---

## 2. List Notifications
**Endpoint**: `GET /notifications/`

**Purpose**: Get the history of in-app notifications for the authenticated user.

**Response**:
- **200 OK**: List of notification objects.
  ```json
  [
    {
      "id": 1,
      "title": "Order Placed",
      "body": "Your order #123 has been placed.",
      "is_read": false,
      "created_at": "2025-12-18 10:30:00"
    },
    ...
  ]
  ```

---

## 3. Mark All As Read
**Endpoint**: `PATCH /notifications/mark-all-read/`

**Purpose**: Marks all unread notifications for the user as read.

**Request Body**: None (Empty body)

**Response**:
- **200 OK**:
  ```json
  {
    "message": "All notifications marked as read"
  }
  ```

---

## 4. Mark Single Notification As Read
**Endpoint**: `PATCH /notifications/{id}/`

**Purpose**: Updates the status of a specific notification.

**Request Body**:
```json
{
  "is_read": true
}
```

**Response**:
- **200 OK**: returns the updated notification object.
  ```json
  {
    "id": 1,
    "title": "Order Placed",
    "body": "...",
    "is_read": true,
    "created_at": "..."
  }
  ```

---

## 5. Delete Notification
**Endpoint**: `DELETE /notifications/{id}/`

**Purpose**: Permanently deletes a notification from history.

**Request Body**: None

**Response**:
- **204 No Content**: On successful deletion.

---

## Real-time Notifications (FCM Payload)
When the backend triggers a notification (e.g., Order Status Change), the FCM payload received by the app is:

```json
{
  "token": "USER_FCM_TOKEN",
  "notification": {
    "title": "Order Update",
    "body": "Your order #123 is now Shipped. Items: 2x Panadol"
  },
  "data": {
    "click_action": "FLUTTER_NOTIFICATION_CLICK",
    "title": "Order Update",
    "body": "Your order #123 is now Shipped. Items: 2x Panadol",
    "type": "order_update", 
    "order_id": "123"
  },
  "android": {
    "priority": "high",
    "notification": {
        "channel_id": "high_importance_channel",
        "click_action": "FLUTTER_NOTIFICATION_CLICK"
    }
  }
}
```
