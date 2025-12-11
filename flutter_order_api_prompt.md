# Backend Order Module Documentation for Flutter Integration

## Overview
This document guides the Flutter AI Agent on how to integrate with the `orders` module of the Mahmood Pharmacy Backend. It details endpoints, data contracts, and error handling strategies.

## Base URL
`/api/` (e.g., `https://your-domain.com/api/`)

## Authentication
All endpoints require a valid JWT Access Token in the header:
`Authorization: Bearer <access_token>`

---

## 1. Checkout (Create Normal Order)
**Endpoint**: `POST /orders/`

### Description
Creates a standard order from the shopping cart.

### Request Body (JSON)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `items` | List[Object] | **YES** | A list of items. Format: `[{"product_id": 1, "quantity": 2}, ...]` |
| `shipping_address` | String | **YES** | Full delivery address. |
| `contact_number` | String | **YES** | Phone number for delivery contact. |
| `branch_id` | Integer | No | ID of the specific branch to order from (optional). |
| `payment_method` | String | No | `'COD'` (default) or `'PAYED'`. |
| `order_type` | String | No | Defaults to `'Normal'`. |

**Example Payload**:
```json
{
  "shipping_address": "House 12, Street 3, G-10, Islamabad",
  "contact_number": "03001234567",
  "items": [
    { "product_id": 15, "quantity": 1 },
    { "product_id": 22, "quantity": 3 }
  ]
}
```

### Success Response (201 Created)
Returns the created Order object.
```json
{
    "id": 101,
    "status": "Pending",
    "total_amount": "1500.00",
    "order_type": "Normal",
    "created_at": "2025-12-11 21:00:00",
    "items": [...]
}
```

### Flutter Handling (Fixing 400 Bad Request)
- **Problem**: If you get `400 Bad Request`, you likely forgot `items`, `shipping_address`, or `contact_number`.
- **Action**: Ensure your Provider/Bloc collects these inputs *before* calling the API. Validate that `items` is not empty.

---

## 2. Quick Order (Buy Now)
**Endpoint**: `POST /orders/quick-order/`

### Description
Instantly purchases a single product, skipping the cart.

### Request Body (JSON)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | Integer | **YES** | The ID of the product to buy. |
| `quantity` | Integer | No | Defaults to `1`. |
| `shipping_address` | String | No* | Uses user profile default if omitted, but recommended to send. |
| `contact_number` | String | No* | Uses user profile default if omitted. |

**Example Payload**:
```json
{
  "product_id": 55,
  "quantity": 2,
  "shipping_address": "Office no 5...",
  "contact_number": "0321..."
}
```

### Success Response (201 Created)
Returns the created Order object with `order_type: "Quick"`.

---

## 3. Validate Cart (Stock Check)
**Endpoint**: `POST /cart/validate/`

### Description
Checks if items in the local cart are still available in stock before proceeding to checkout.

### Request Body
```json
{
  "items": [ { "product_id": 15, "quantity": 100 } ]
}
```

### Response (200 OK)
**Valid Case**:
```json
{ "valid": true }
```

**Invalid Case** (Stock issue):
```json
{
  "valid": false,
  "errors": [ "Panadol: Only 5 left." ]
}
```

### Flutter Handling
- **Action**: Call this when the user clicks "Checkout".
-If `valid: false`, show `errors` in a dialog and usually require the user to adjust items or remove them.
- If `valid: true`, proceed to the Address Selection screen.

---

## Error Handling Guide

| Status Code | Meaning | Flutter Action |
| :--- | :--- | :--- |
| **400 Bad Request** | **Validation Error**. Data is missing or invalid. | **CRITICAL**: Decode `response.body`. It contains the exact field error (e.g., `{"items": ["Order must contain at least one item."]}`). specific details. **Display this error to the user.** |
| **401 Unauthorized** | **Token issues**. Invalid or expired token. | Redirect user to Login Screen. Do NOT retry blindly. |
| **403 Forbidden** | **Permission denied**. | "You do not have permission to do this." |
| **404 Not Found** | **Invalid Resource**. Product/Branch ID does not exist. | "Item no longer available." Remove it from the cart. |
| **500 Server Error** | **Backend Crash**. | Show generic "Service unavailable" message. |
