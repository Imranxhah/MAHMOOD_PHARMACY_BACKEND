# Prescription API Guide for Flutter Agent

This guide details the `Prescription` model endpoints, data structures, and specifically how to handle **Branch Selection**.

## 1. Base URL
All endpoints are relative to your base API URL (e.g., `https://your-domain.com/api/`).

## 2. Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/prescriptions/` | List all prescriptions for the logged-in user. |
| **POST** | `/prescriptions/` | Create/Upload a new prescription. |
| **POST** | `/prescriptions/upload/` | Alias for Create (same as above). |
| **GET** | `/prescriptions/{id}/` | Get details of a specific prescription. |
| **PATCH** | `/prescriptions/{id}/` | Update a prescription (usually for admin, but user might update notes). |
| **DELETE** | `/prescriptions/{id}/` | Delete a prescription. |

---

## 3. Branch Selection Implementation

### **How to Submit Branch (POST Request)**
When the user uploads a prescription, they should select a branch. You need to send the **ID** of the selected branch.

**Endpoint:** `POST /api/prescriptions/` (or `/upload/`)
**Content-Type:** `multipart/form-data`

**Payload Fields:**

| Field | Type | Required? | Description |
| :--- | :--- | :--- | :--- |
| `image` | File | **YES** | The prescription image file. |
| `contact_number` | String | **YES** | Phone number (e.g., `03128424013`). |
| `branch` | Integer | **Recommended** | The **ID** of the selected branch (e.g., `1`, `2`). |
| `notes` | String | No | Optional user notes. |

**Example Flutter Code Snippet (dio/http):**
```dart
FormData formData = FormData.fromMap({
  "image": await MultipartFile.fromFile(imagePath),
  "contact_number": "03123456789",
  "branch": selectedBranchId, // e.g., 5
  "notes": "Deliver urgent",
});
```

---

### **How to Get Branch Back (GET Request)**
When fetching the list or details of prescriptions, the backend will return the `branch` field as an **Integer ID**.

**Endpoint:** `GET /api/prescriptions/`

**Response Example:**
```json
[
  {
    "id": 10,
    "user": 5,
    "branch": 2,  // <--- This is the Branch ID
    "image": "http://.../media/prescriptions/img.jpg",
    "notes": "Urgent",
    "contact_number": "03123456789",
    "status": "Pending",
    "admin_feedback": "",
    "created_at": "2024-12-15 10:00:00"
  }
]
```

**Flutter Handling:**
*   You will receive the `branch` ID (int).
*   If you need to show the Branch **Name** in the UI (e.g., "History" screen), you must match this ID with your locally cached list of Branches (fetched from `/api/branches/`) or fetch the branch details separately if needed. Currently, the API returns the ID only.

---

## 4. Full Data Structures

### **Prescription Model Fields**

| Field Name | Type | Read/Write | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Read Only | Unique ID. |
| `user` | Integer | Read Only | User ID (automatically set by token). |
| `branch` | Integer | **Read/Write** | ID of the Branch. |
| `image` | String (URL) | Read/Write | URL to image (Read) / File (Write). |
| `notes` | String | Read/Write | User notes. |
| `contact_number`| String | Read/Write | Validated phone number. |
| `status` | String | Read Only | `Pending`, `Approved`, `Rejected`. |
| `admin_feedback`| String | Read Only | Admin's response/reason. |
| `created_at` | DateTime | Read Only | Creation timestamp. |

---

## 5. Summary for "AI Agent Builder"

1.  **To Submit**: Add a field `branch` to your multipart request containing the `branch_id`.
2.  **To Display**: Parse `branch` (int) from the JSON response.
3.  **UI**: Ensure the user picks a branch *before* uploading. Use the correct endpoint `POST /api/prescriptions/`.
