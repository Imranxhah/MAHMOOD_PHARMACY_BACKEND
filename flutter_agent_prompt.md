# Flutter AI Agent Prompt: Update Prescription Upload Feature

**Context**: 
We have updated the backend for `Mahmood Pharmacy`. The prescription upload feature now requires a **Contact Number** from the user. You need to update the Flutter app's UI and API logic to handle this new field.

## 1. Endpoint Details
*   **URL**: `POST /api/prescriptions/upload/`
*   **Method**: `POST`
*   **Content-Type**: `multipart/form-data` (Required because of image upload)
*   **Auth**: Required (`Authorization: Bearer <token>`)

## 2. Request Data (What to send)
You must now send the following fields:

| Field | Type | Required? | Validation Rule | Example |
| :--- | :--- | :--- | :--- | :--- |
| `image` | File | **YES** | Image file (jpg, png) | (Binary file) |
| `contact_number` | String | **YES** | **Strict 11 Digits**. Must start with `03`. No spaces. | `03128424013` |
| `notes` | String | No | Optional text note | "Please deliver by evening" |

## 3. UI Requirements
*   Add a **Text Input Field** for "Contact Number" in the prescription upload screen.
*   **Input Validation**:
    *   Allow ONLY numbers `[0-9]`.
    *   Max length: 11.
    *   Show error if length is not 11.
    *   Show error if it doesn't start with `03`.

## 4. Response & Error Handling

### **Success (201 Created)**
*   **Meaning**: Upload successful.
*   **Action**: Show success dialog, then navigate to "My Prescriptions" or Home.

### **Error: 400 Bad Request (Validation Error)**
*   **Meaning**: The data sent was invalid (e.g., wrong phone format).
*   **Backend Response**:
    ```json
    {
      "contact_number": ["Phone number must be 11 digits and start with 03 (e.g., 03XXXXXXXXX) with no spaces or characters."]
    }
    ```
*   **Action**: 
    1.  Parse the JSON.
    2.  Check if `contact_number` key exists.
    3.  Display the error message *specifically* under the phone number input field (or show a valid SnackBar).

### **Error: 401 Unauthorized**
*   **Meaning**: Token expired or user not logged in.
*   **Action**: Redirect to Login Screen.

### **Error: 413 Payload Too Large**
*   **Meaning**: The image file is too big (e.g., > 5MB).
*   **Action**: specific error message: "Image is too large. Please upload multiple smaller code."

## 5. Task Checklist for You
1.  [ ] Update the API call in `PrescriptionService` (or equivalent) to include `contact_number` in the `FormData`.
2.  [ ] Add `TextFormField` validation logic for `03XXXXXXXXX` format.
3.  [ ] Handle `400` error specifically to show the backend validation message.
