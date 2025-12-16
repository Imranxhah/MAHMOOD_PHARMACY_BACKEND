# Notification API Guide

This guide details how to integrate Push Notifications and In-App Notification History in the Flutter app.

## 1. Prerequisites
*   You must have `firebase_messaging` installed in Flutter.
*   You must have `google-services.json` in `android/app/`.

## 2. Register Device Token (Essential)
Call this endpoint **immediately after login** and **on app launch** (if logged in) to ensure the backend can push messages to this device.

*   **Endpoint**: `POST /api/notifications/register-device/`
*   **Auth**: Required (Bearer Token)
*   **Header**: `Content-Type: application/json`

**Request Body:**
```json
{
  "fcm_token": "d7x8s... (The long token from Firebase)"
}
```

**Response (200 OK):**
```json
{
  "message": "Device registered successfully"
}
```

## 3. Fetch Notification History
Use this to show a "Notification Center" list in the app.

*   **Endpoint**: `GET /api/notifications/`
*   **Auth**: Required

**Response:**
```json
[
  {
    "id": 1,
    "title": "Order Update",
    "body": "Your order #123 is now Shipped.",
    "is_read": false,
    "created_at": "2024-12-16 14:00:00"
  }
]
```

## 4. Mark All as Read (Optional)
*   **Endpoint**: `PATCH /api/notifications/mark-all-read/`
*   **Response**: `{"message": "All notifications marked as read"}`

## 5. How Testing Works
1.  **Register**: Send your token via the API above.
2.  **Trigger**: Go to Django Admin -> Orders -> Change status of an order (e.g., to "Shipped") -> Save.
3.  **Result**: 
    *   Your phone should receive a push notification.
    *   The `/api/notifications/` list should show the new entry.
