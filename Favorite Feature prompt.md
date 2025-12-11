# Flutter AI Agent Prompt: Implement Favorite Toggle

**Objective**: Implement a "Heart" icon button on every `ProductCard` that allows authenticated users to toggle a product as a favorite.

## 1. Description
*   **UI**: Add a Heart Icon (`Icons.favorite_border` vs `Icons.favorite`) to the top-right corner of the `ProductCard` widget.
*   **Behavior**:
    1.  **Display**: If `product.is_favorite` is true, show a RED filled heart. If false, show a GREY outline heart.
    2.  **Action**: When tapped:
        *   **Check Auth**: Check if the user is logged in (token exists).
        *   **If Guest**: Show a `SnackBar` or `AlertDialog`: "Please login to add favorites."
        *   **If Logged In**: Send an API request to toggle the favorite status.
    3.  **Optimistic Update**: Immediately toggle the icon visual state (Red <-> Grey) *before* the API call completes to make it feel snappy. Revert if the API fails.

## 2. API Integration Details

### Endpoint
*   **URL**: `POST /available-host/api/favorites/toggle/`
*   **Base URL**: `http://10.0.2.2:8000/api/` (Android Emulator).
*   **Method**: `POST`
*   **Auth**: **REQUIRED** (Bearer Token header).

### Request Body
```json
{
  "product_id": 123
}
```

### Responses
| Scenario | HTTP Code | Response JSON | Action |
| :--- | :--- | :--- | :--- |
| **Added** | `201 Created` | `{ "message": "Added...", "is_favorite": true }` | Ensure icon is Red. Show toast "Added to Favorites". |
| **Removed** | `200 OK` | `{ "message": "Removed...", "is_favorite": false }` | Ensure icon is Grey. Show toast "Removed from Favorites". |
| **Unauthorized** | `401` | N/A | Redirect to Login or show "Session expired". |
| **Error** | `400/404/500` | `{ "error": "..." }` | Show error toast and **REVERT** the icon state. |

## 3. Implementation Steps for Agent
1.  **Repository**: Add `toggleFavorite(int productId)` method to `ProductRepository`.
2.  **Provider/BLoC**: Add a method to handle the logic (Optimistic update \u2192 API Call \u2192 Revert on failure).
3.  **UI**: Update `ProductCard` to include the `IconButton`.
    *   **Icon Color**: `Colors.red` (active), `Colors.grey` (inactive).
    *   **Animation**: Optional: Add a small scale animation on tap.
