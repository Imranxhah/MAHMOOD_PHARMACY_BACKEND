# Complete Mahmood Pharmacy Backend API Guide

This document lists all available endpoints for the Flutter application, including Authentication, Products, Orders, and Addresses.

## Base URL
`/api/` (e.g., `https://your-domain.com/api/`)

## Authentication Headers
Most endpoints require: `Authorization: Bearer <access_token>`

---

## 1. Products & Categories (Search and Filter)

### **A. Get All Products (Filtered & Sorted)**
*   **Endpoint**: `GET /products/`
*   **Query Parameters**:
    *   `search`: Searches **Product Name** or **Category Name**.
    *   `category`: Filter by **Category ID**.
    *   `ordering`: Sort the results.
        *   `price`: Low to High
        *   `-price`: High to Low
        *   `created_at`: Oldest first
        *   `-created_at`: Newest first (Latest)
*   **Examples**:
    *   *Search "Syrup"*: `/products/?search=Syrup`
    *   *Category 5, Price Low to High*: `/products/?category=5&ordering=price`
    *   *Latest Products*: `/products/?ordering=-created_at`

### **B. Home Page Data (Hot & Categories)**
*   **Endpoint**: `GET /products/home/`
*   **Response**:
    *   `categories`: List of all categories (for horizontal list).
    *   `sections`: List of objects containing a `category` and its top 10 `products` (ordered by popularity). Use the **first section** as "Hot Products".

### **C. Get All Categories**
*   **Endpoint**: `GET /categories/`
*   **Use Case**: For the "Browse Categories" screen.

---

## 2. Orders

### **A. Checkout (Normal Order)**
*   **Endpoint**: `POST /orders/`
*   **Request Body**:
    ```json
    {
      "items": [{"product_id": 1, "quantity": 2}],
      "shipping_address": "Full Address string",
      "contact_number": "03001234567",
      "payment_method": "COD", // or "PAYED"
      "order_type": "Normal" // Optional
    }
    ```

### **B. Quick Order (Buy Now)**
*   **Endpoint**: `POST /orders/quick-order/`
*   **Request Body**:
    ```json
    {
      "product_id": 1,
      "quantity": 1,
      "shipping_address": "...",
      "contact_number": "..."
    }
    ```

### **C. Order History**
*   **Endpoint**: `GET /orders/`
*   **Response**: List of all past orders.

### **D. Validate Cart (Stock Check)**
*   **Endpoint**: `POST /cart/validate/`
*   **Request Body**: `{"items": [...]}`
*   **Response**: `{"valid": true}` or `{"valid": false, "errors": [...]}`

### **E. Get Delivery Charges (Public)**
*   **Endpoint**: `GET /delivery-charges/`
*   **Auth**: Not required (Public).
*   **Response**:
    ```json
    {
      "amount": 150.00
    }
    ```
*   **Usage**: Call this on the Cart Screen to show "Shipping Fee".
*   **Error Handling**:
    *   This endpoint is very safe. It always returns `200 OK`.
    *   If no charge is set in admin, it returns `0.00`.
    *   **500 Internal Server Error**: Extremely rare (Database down). Retry once.

---

## 3. Addresses

### **A. List Addresses**
*   **Endpoint**: `GET /addresses/`

### **B. Add Address**
*   **Endpoint**: `POST /addresses/`
*   **Request Body**: `{"address": "House 123, Street 5..."}`

### **C. Delete Address**
*   **Endpoint**: `DELETE /addresses/{id}/`

---

## 4. Authentication

## 4. Authentication (Sliding Session)

*   **Login**: `POST /auth/login/` (Returns `access` and `refresh` tokens). Store BOTH secure storage.
*   **Register**: `POST /auth/register/`
*   **Verify OTP**: `POST /auth/verify/`
*   **Resend OTP**: `POST /auth/resend-otp/`
*   **Refresh Token**: `POST /auth/refresh/`

### **Token Rotation Implementation (Critical)**
This backend uses a **Sliding Session**. Every time you refresh the token, you get a **NEW Access Token** AND a **NEW Refresh Token**.

**Logic for Interceptor (Dio/Http):**
1.  Intercept `401 Unauthorized` error.
2.  Send **current** `refresh` token to `POST /auth/refresh/`.
3.  **Response Handling:**
    *   The server returns `{ "access": "...", "refresh": "..." }`.
    *   **CRITICAL**: You MUST replace the old `refresh` token in your storage with the NEW one from the response. The old one is now dead (Blacklisted).
4.  Retry the failed request with the new access token.

**If /refresh/ fails (401)**: The session is dead (user unused app for >90 days). Force Logout.

---

## 5. Prescriptions (Upload)

*   **Upload**: `POST /prescriptions/upload/`
*   **Body**: Form-Data with `image` file and `note` (text).

---

## Flutter Error Handling Tips
1.  **400 Bad Request**: Most common. Means you sent missing fields (e.g., forgot `shipping_address` or `items`). **Start decoding `response.body`** to show the specific error message to the user.
2.  **401 Unauthorized**: Token expired. Send user to Login.
3.  **Search/Filter**: If `GET /products/` returns `[]` (empty list), show "No products found".
