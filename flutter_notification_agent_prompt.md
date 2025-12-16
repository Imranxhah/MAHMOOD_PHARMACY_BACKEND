# Flutter Agent Prompt: Implement Notification System

**Role**: You are an expert Flutter Developer building a production-ready notification system for the "Mahmood Pharmacy" app.

**Context**: 
We have a Django backend with Firebase Admin SDK configured.
The `google-services.json` file is ALREADY placed in `android/app/`.
Your goal is to implement the frontend logic to receive Push Notifications (FCM) and display a Notification History screen.

---

## 1. Technical Requirements (Dependencies)
Add these packages to `pubspec.yaml`:
*   `firebase_core`: (Latest)
*   `firebase_messaging`: (Latest)
*   `flutter_local_notifications`: (Latest - Required to show heads-up notifications when app is in **Foreground**)

---

## 2. API Endpoints Implementation

You must implement a service class (e.g., `NotificationService` or `Repository`) to handle these interactions.

### A. Register Device Token (CRITICAL)
**Goal**: Link the user's phone to their account so the backend can send messages.
**Topic Subscription (For Guests & Broadcasts)**:
*   IMMEDIATELY upon app launch (in `main.dart`), subscribe to the topic: `all_users`.
    ```dart
    FirebaseMessaging.instance.subscribeToTopic("all_users");
    ```
*   This ensures even guests receive "Broadcast" notifications.

**Device Registration (Logged-in only)**:
**When to call**: 
1.  Immediately after **Login** success.
2.  On **App Launch** (if user is already logged in).
3.  On **Token Refresh** (listen to `FirebaseMessaging.instance.onTokenRefresh`).

*   **URL**: `POST /api/notifications/register-device/`
*   **Headers**: `Authorization: Bearer <access_token>`, `Content-Type: application/json`
*   **Body**:
    ```json
    {
      "fcm_token": "current_fcm_token_string"
    }
    ```
*   **Response Handling**:
    *   **200 OK**: Success. Log it ("Device Registered").
    *   **401 Unauthorized**: User token expired. Redirect to Login.
    *   **400 Bad Request**: Token missing. Handle gracefully (don't crash).

### B. Fetch Notification History
**Goal**: Show a list of past notifications (Order updates, etc.).

*   **URL**: `GET /api/notifications/`
*   **Response Structure**:
    ```json
    [
      {
        "id": 10,
        "title": "Order Shipped",
        "body": "Your order #105 has been shipped via TCS.",
        "is_read": false,
        "created_at": "2025-12-16 14:30:00"
      },
      ...
    ]
    ```
*   **UI Implementation**:
    *   Create `NotificationScreen`.
    *   Use a `ListView.builder`.
    *   Show "No notifications" if list is empty.
    *   Highlight unread items (e.g., bold text or different background).

### C. Mark All Read
**Goal**: Clear the "unread" status.
*   **Trigger**: When user opens the `NotificationScreen` or clicks a "Mark all read" button.
*   **URL**: `PATCH /api/notifications/mark-all-read/`

---

## 3. The "Efficient" Logic Flow (FCM Integration)

To make the app efficient and responsive, follow this exact lifecycle flow:

1.  **Main/Initialization**:
    *   Initialize `Firebase.initializeApp()`.
    *   Request Permission: `FirebaseMessaging.instance.requestPermission()`.

2.  **Foreground Handling (App is Open)**:
    *   **Problem**: Firebase does NOT show a notification UI when app is in foreground by default.
    *   **Solution**: Listen to `FirebaseMessaging.onMessage`.
    *   **Action**: Use `flutter_local_notifications` to display a high-priority "Heads-up" notification so the user sees it immediately without pulling data.

3.  **Background/Terminated Handling**:
    *   **Background Tap**: Use `FirebaseMessaging.onMessageOpenedApp`. Navigate the user to the `OrderDetails` screen or `NotificationScreen` based on payload.
    *   **Terminated Launch**: Use `FirebaseMessaging.instance.getInitialMessage()`. If not null, handle navigation.

---

## 4. Error Handling Strategy

1.  **Network Errors (SocketException)**:
    *   Since notifications are secondary, **fail silently** for background registration. Do not show a popup "Failed to register device" as it annoys users. Just log error to console.
    *   For the **Notification Screen**, show a "Connection Error, Retry" button.

2.  **Auth Errors (401)**:
    *   If `register-device` returns 401, immediately logout the user locally and redirect to Login Screen.

3.  **Permission Denied**:
    *   If user denies permission, gracefully downgrade. Do not keep asking. Just don't call `register-device` or set a flag.

---

## 5. Summary Checklist for Agent
1.  [ ] Setup Firebase SDK in `main.dart`.
2.  [ ] Create `NotificationService` singleton.
3.  [ ] Implement `registerDevice(token)` API call.
4.  [ ] Setup `onMessage` listener for Foreground notifications.
5.  [ ] Build `NotificationScreen` fetching data from `GET /api/notifications/`.
