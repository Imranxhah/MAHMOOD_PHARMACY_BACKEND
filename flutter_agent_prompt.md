# Backend API Integration Prompt for Flutter Agent

**Role:** You are an expert Flutter Developer. Your task is to integrate the following Django REST API endpoints into a Flutter application.

**Base URL:** `http://10.0.2.2:8000/api/` (Android Emulator) or `http://127.0.0.1:8000/api/` (iOS/Web).
**Authentication:** uses JWT (JSON Web Tokens). headers: `Authorization: Bearer <access_token>`

---

## 1. Authentication Module (`/auth/`)

### A. Login
*   **Endpoint:** `POST /auth/login/`
*   **Usage:** Login Screen.
*   **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "secretpassword"
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
      "refresh": "eyJ0eX...",
      "access": "eyJ0eX..."
    }
    ```
    *   **Action:** Save tokens securely (e.g., `flutter_secure_storage`). Navigate to Home.
*   **Error Responses:**
    *   **401 Unauthorized (Invalid Credentials):**
        ```json
        {
          "code": "authentication_failed",
          "message": "No account found with the given credentials."
        }
        ```
        *   **Action:** Show red snackbar: "Invalid email or password."
    *   **401 Unauthorized (Unverified Account):**
        ```json
        {
          "code": "unverified_user",
          "message": "User is not active. A new OTP has been sent."
        }
        ```
        *   **Action:** Navigate to **OTP Verification Screen**. Pass the `email` to that screen.

### B. Register
*   **Endpoint:** `POST /auth/register/`
*   **Usage:** Registration Screen.
*   **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "strongpassword",
      "first_name": "John",
      "last_name": "Doe",
      "mobile": "+923001234567"
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
      "message": "User registered successfully...",
      "email": "user@example.com"
    }
    ```
    *   **Action:** Navigate to **OTP Verification Screen**.
*   **Error Responses (400 Bad Request):**
    ```json
    {
      "email": ["User with this email already exists."],
      "password": ["This password is too common."]
    }
    ```
    *   **Action:** Map keys to InputFields and show error text under the specific field.
*   **Special Error (409 Conflict):** User exists but is unverified.
    *   **Action:** Navigate to OTP Screen.

### C. Verify OTP
*   **Endpoint:** `POST /auth/verify/`
*   **Usage:** OTP Screen (after Register or Login-Unverified).
*   **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "otp_code": "123456"
    }
    ```
*   **Success Response (200 OK):** `{"message": "Account verified successfully."}`
    *   **Action:** Navigate to Login Screen (or auto-login if you implemented that flow).
*   **Error Responses (400 Bad Request):** `{"non_field_errors": ["Invalid OTP."]}` or `{"otp_code": ["OTP has expired."]}`
    *   **Action:** Show error snackbar.

### D. Resend OTP
*   **Endpoint:** `POST /auth/resend-otp/`
*   **Body:** `{"email": "..."}`
*   **Action:** Enable a "Resend" button after 60s timer.

---

## 2. Products Module (`/products/`, `/categories/`)

### A. List Categories
*   **Endpoint:** `GET /categories/`
*   **Usage:** Home Screen (Horizontal List), Search Filter.
*   **Permission:** Public (No Token required).
*   **Success Response (200 OK):**
    ```json
    [
      {
        "id": 1,
        "name": "Medicines",
        "image": "http://.../media/categories/med.png"
      }
    ]
    ```

### B. List Products (Search & Filter)
*   **Endpoint:** `GET /products/`
*   **Usage:** Home Screen (Featured), Product Listing Screen.
*   **Permission:** Public (No Token required).
*   **Query Parameters:**
    *   `?search=panadol`: Search by name.
    *   `?category=1`: Filter by category ID.
*   **Success Response (200 OK):**
    ```json
    [
      {
        "id": 10,
        "category_name": "Medicines",
        "name": "Panadol Extra",
        "description": "For pain relief...",
        "price": "50.00",
        "stock": 100,
        "image": "http://.../img.jpg",
        "is_active": true,
        "is_favorite": false
      }
    ]
    ```
    *   **Refinement:** `is_favorite` will be `false` for guest users. If logged in, it reflects the user's status.

### C. Toggle Favorite
*   **Endpoint:** `POST /favorites/toggle/`
*   **Usage:** Heart Icon on Product Card / Detail Screen.
*   **Permission:** **Authenticated Only** (User must be logged in).
*   **Request Body:** `{"product_id": 10}`
*   **Success Response (200/201):**
    ```json
    {
      "message": "Added to favorites.",
      "is_favorite": true
    }
    ```
    *   **Action:** Update the UI Heart icon state immediately based on `is_favorite`.
*   **Error Handling (401 Unauthorized):**
    *   **Action:** If user clicks Heart icon while guest, show dialog: "Please login to add favorites." -> Redirect to Login.

### D. Get User Favorites
*   **Endpoint:** `GET /favorites/`
*   **Usage:** Wishlist Screen.
*   **Permission:** **Authenticated Only**.
*   **Success Response:** List of favorite objects containing nested product info.
    ```json
    [
      {
        "id": 5,
        "product": { "id": 10, "name": "Panadol", ... },
        "created_at": "..."
      }
    ]
    ```

---

## General Error Handling Strategy

1.  **Network Error:** (SocketException) -> Show "No Internet Connection" full-screen Widget with Retry button.
2.  **500 Internal Server Error:** -> Show generic "Something went wrong" snackbar. Do NOT show technical details to user.
3.  **401 Unauthorized (Token Expired):**
    *   Intercept the request.
    *   Call `POST /auth/refresh/` with `refresh` token.
    *   If success: Retry original request with new `access` token.
    *   If fail: Logout user and redirect to Login Screen.

---

**Implementation Notes for Flutter Agent:**
*   Use `dio` or `http` for requests.
*   Use `provider` or `flutter_bloc` for state management.
*   Create a singleton `ApiService` class.

---

## 3. Order Management (`/orders/`)

### A. Place Order
*   **Endpoint:** `POST /orders/`
*   **Permission:** Authenticated.
*   **Request Body:**
    ```json
    {
      "shipping_address": "House 123, Street 4, Islamabad",
      "contact_number": "03001234567",
      "branch_id": 1,
      "items": [
        {"product_id": "1", "quantity": 2},
        {"product_id": "5", "quantity": 1}
      ]
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
      "id": 55,
      "user": 1,
      "status": "Pending",
      "total_amount": "550.00",
      "created_at": "2025-12-10 18:00:00",
      "items": [...]
    }
    ```
*   **Error Handling:**
    *   **400 Bad Request:** `{"error": "Insufficient stock for product X. Available: 5"}` -> Show alert dialog.

### B. List My Orders
*   **Endpoint:** `GET /orders/`
*   **Usage:** Sidebar -> My Orders.
*   **Permission:** Authenticated.
*   **Success Response (200 OK):** List of orders (newest first).

### C. Get Order Detail
*   **Endpoint:** `GET /orders/{id}/`
*   **Usage:** Order History -> Tap on Order.
*   **Response:** Detailed order object with all items.

### D. Quick Order (One Click)
*   **Endpoint:** `POST /orders/quick-order/`
*   **Usage:** "Buy Now" button on Product Detail.
*   **Body:** `{"product_id": 10, "quantity": 1, "shipping_address": "..."}`
*   **Note:** If address not provided, implemented logic falls back to default if exists.

### E. Cart Validation (Optional)
*   **Endpoint:** `POST /cart/validate/`
*   **Usage:** Call this before navigating to Checkout Screen to ensure cart items are valid.
*   **Body:** `{"items": [{"product_id": 1, "quantity": 5}]}`

---

## 4. Prescriptions (`/prescriptions/`)

### A. Upload Prescription
*   **Endpoint:** `POST /prescriptions/upload/`
*   **Permission:** Authenticated.
*   **Request Type:** `multipart/form-data`
*   **Fields:**
    *   `image`: File (Required).
    *   `notes`: String (Optional).
*   **Success Response (201 Created):**
    ```json
    {
      "id": 10,
      "status": "Pending",
      "image": "http://.../media/prescriptions/img.jpg",
      "created_at": "..."
    }
    ```

### B. List My Prescriptions
*   **Endpoint:** `GET /prescriptions/`
*   **Usage:** "My Prescriptions" screen.

---

## 5. Branches (`/branches/`)

### A. List All Branches
*   **Endpoint:** `GET /branches/`
*   **Response:** List of all branches with coordinates.

### B. Find Nearest Branch
*   **Endpoint:** `GET /branches/nearest/?lat=33.68&long=73.04`
*   **Query Params:** `lat` (double), `long` (double).
*   **Success Response (200 OK):**
    ```json
    [
        {
          "id": 1,
          "name": "Blue Area Branch",
          "distance_km": 1.2,
          "google_maps_url": "https://www.google.com/maps/dir/?api=1&destination=33.7,73.1",
          ...
        },
        ...
    ]
    ```
*   **Flutter Implementation Strategy (No Google Maps API Key Needed):**
    1.  **Get Location:** Use `geolocator` package to get user's current `latitude` and `longitude`.
    2.  **Call API:** Send these coordinates to `GET /branches/nearest/`.
    3.  **Display List:** Show the list of branches returned. Display the `distance_km` field (e.g., "1.2 km away").
    4.  **Get Directions:** When user taps "Navigate" or the list item, use `url_launcher` to launch the `google_maps_url`.
    *   **Note:** Do NOT implement an embedded Google Map view to avoid API billing. Just use the list and external navigation.
*   **Error Handling:**
    *   **404 Not Found:** "No branches found."

---

## 6. Analytics & Dashboard (`/analytics/`)

### A. Dashboard Stats
*   **Endpoint:** `GET /analytics/dashboard/`
*   **Permission:** Admin Only.
*   **Response:**
    ```json
    {
      "total_sales": 5500.00,
      "total_orders": 120,
      "total_users": 50,
      "low_stock_count": 5,
      "recent_orders": [...]
    }
    ```

### B. Sales Report
*   **Endpoint:** `GET /analytics/sales/?mode=daily` (or `mode=monthly`)
*   **Permission:** Admin Only.

---

## 7. Marketing & Content (`/marketing/` or `/banners/`)

### A. Get Banners (Sliders)
*   **Endpoint:** `GET /banners/`
*   **Permission:** Public (AllowAny).
*   **Response:** List of banners.
    ```json
    [
      {
        "id": 1,
        "title": "Winter Sale",
        "image": "http://.../media/banners/sale.jpg",
        "created_at": "..."
      }
    ]
    ```

### B. Send Notification (Admin)
*   **Endpoint:** `POST /marketing/notifications/send/`
*   **Permission:** Admin Only.
*   **Body:** `{"title": "Deal Alert", "body": "50% Off today!"}`





