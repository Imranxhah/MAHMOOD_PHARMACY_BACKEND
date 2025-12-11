# Product Search & Filtering API Guide

This document details only the endpoints required for searching, filtering, and sorting products in the Flutter app.

## Base URL
`/api/`

---

## 1. Get Products (Main Search & Filter Endpoint)

**Endpoint**: `GET /products/`

This single endpoint handles searching, category filtering, and sorting. You can combine multiple parameters.

### Query Parameters
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `search` | String | Searches within **Product Name** AND **Category Name**. |
| `category` | Integer | ID of the Category to filter by. |
| `min_price` | Decimal | Minimum price to filter by (e.g., `100.00`). |
| `max_price` | Decimal | Maximum price to filter by (e.g., `5000.00`). |
| `ordering` | String | Sorts the result. Options below. |

### Sorting Options (`ordering` values)
- **Price: Low to High** -> `ordering=price`
- **Price: High to Low** -> `ordering=-price`
- **Newest First** -> `ordering=-created_at`
- **Oldest First** -> `ordering=created_at`
- **Stock: Low to High** -> `ordering=stock`

### Usage Examples
1.  **Global Search** (e.g., user types "Syrup"):
    `GET /products/?search=Syrup`
2.  **Filter by Category** (e.g., Category ID 5):
    `GET /products/?category=5`
3.  **Price Range** (e.g., items between 500 and 2000):
    `GET /products/?min_price=500&max_price=2000`
4.  **Complex Filter** (Search "Panadol" in Category 2, sorted by Price):
    `GET /products/?search=Panadol&category=2&ordering=price`

### Response Format (JSON)
Returns a list of product objects.
```json
[
  {
    "id": 10,
    "name": "Panadol Extra",
    "description": "For effective pain relief...",
    "price": "50.00",
    "stock": 100,
    "image": "http://domain.com/media/products/panadol.jpg",
    "category": 2, // Category ID
    "is_active": true,
    "created_at": "2025-12-10T12:00:00Z"
  },
  {
    "id": 15,
    "name": "Brufen",
    "description": "Anti-inflammatory...",
    "price": "120.00",
    "stock": 50,
    "image": null,
    "category": 2,
    "is_active": true,
    "created_at": "2025-12-09T10:30:00Z"
  }
]
```

### Flutter Handling
- **Empty List**: If `[]` is returned, show "No products found."
- **Pagination**: (Currently not enabled, returns all matches).

---

## 2. Get Categories (For Filter UI)

**Endpoint**: `GET /categories/`

Use this to populate your "Filter by Category" chips or dropdown.

### Response Format
```json
[
  {
    "id": 1,
    "name": "Medicines",
    "image": "http://domain.com/media/categories/meds.jpg"
  },
  {
    "id": 2,
    "name": "Personal Care",
    "image": null
  }
]
```
