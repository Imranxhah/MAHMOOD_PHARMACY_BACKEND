# Flutter AI Agent Prompt: Home Page Overhaul

**Objective**: Update the existing `HomeScreen` to become dynamic, data-driven, and structurally aligned with the new backend logic.

## 1. Context & Goal
The current Home Page uses hardcoded or limited layouts ("Shop by Category" grid, single "Popular Products" list). We need to refactor this to consume a SINGLE new API endpoint (`/api/products/home/`) that provides *all* the data needed for the page structure.

**Key Requirement**:
- **Preserve**: The "Promotional Banner" (keep it exactly as is).
- **Update**: "Shop by Category" must now display ALL categories dynamically.
- **Replace**: The single "Popular Products" section must be replaced by **multiple dynamic sections** based on "Hot Categories" returned by the API.

## 2. API Integration Details

### Endpoint
*   **Base URL**: `http://10.0.2.2:8000/api/` (Android Emulator Localhost).
*   **Full URL**: `http://10.0.2.2:8000/api/products/home/`
*   **Note**: Ensure your `Dio` or `Http` client is configured with this base URL for development.
*   **Method**: `GET`
*   **Auth**: Public (No token required, but if token is sent, `is_favorite` fields will be accurate).

### Request format
*   **Headers**: `Content-Type: application/json`
*   **Body**: None.

### Response Data Structure
The API returns a JSON object with two main keys: `categories` and `sections`.

```json
{
  "categories": [
    {
      "id": 1,
      "name": "Medicine",
      "image": "http://.../media/categories/meds.png",
      "created_at": "..."
    },
    ...
  ],
  "sections": [
    {
      "category": {
        "id": 2,
        "name": "Skincare",
        "image": "..."
      },
      "products": [
        {
          "id": 101,
          "name": "Face Wash",
          "price": "500.00",
          "image": "http://.../products/fw.jpg",
          "is_favorite": false,
          ...
        },
        ... (up to 10 products)
      ]
    },
    ... (more sections sorted by popularity)
  ]
}
```

## 3. UI Implementation Plan

### Screen Structure (CustomScrollView)
Maintain the `CustomScrollView` structure. The slivers should be ordered as follows:

1.  **SliverAppBar**: Keep existing (Location Header & Cart Action).
2.  **SliverToBoxAdapter (Search)**: Keep existing.
3.  **SliverToBoxAdapter (Banner)**: **KEEP EXISTING**. The user specifically requested to keep the "Special Offer" banner.
4.  **SliverToBoxAdapter (Categories Header)**: "Shop by Category" (or simple "Categories").
5.  **SliverToBoxAdapter (Categories List)**:
    *   **Old**: 4-column Grid.
    *   **New**: A **Horizontal ListView** (h= ~100px) displaying `response['categories']`.
    *   **Item**: Circular image + Name.
    *   **Action**: Tap \u2192 Navigate to `ProductListScreen(categoryId: id)`.
6.  **Dynamic Sections Loop**:
    *   Iterate through `response['sections']`.
    *   For each section:
        *   **Header**: Row with `section['category']['name']` (Bold, Left) and "View All" (Right). "View All" \u2192 `ProductListScreen(categoryId: section['category']['id'])`.
        *   **List**: Horizontal ListView of `section['products']`.
        *   **Card**: Use existing `ProductCard`.

## 4. Error Handling & State Management

Since this is the main landing page, error handling must be graceful.

| Scenario | HTTP Code | Meaning | App Behavior |
| :--- | :--- | :--- | :--- |
| **Success** | `200 OK` | Data received. | Render the full UI. |
| **Network Error** | `N/A` | No internet/Server unreachable. | Show a "No Connection" full-screen state with a **"Retry"** button. |
| **Server Error** | `500` | Backend crash. | Show "Something went wrong" with a **"Retry"** button. |
| **Empty Data** | `200` | `categories` or `sections` empty. | If categories empty, show "No categories found". If sections empty, show "No products featured". |
| **Malformed** | `200` | JSON missing keys. | Catch `valid JSON` but missing fields errors, log them, and show generic error/retry. |

### Loading State
*   Show a `Shimmer` effect skeleton matching the layout (Banner placeholder + Circle placeholders + Rectangular Card placeholders) while fetching.


## 5. State Persistence & Caching (CRITICAL)
**Requirement**: The Home Page data MUST be cached in memory.
*   **Behavior**:
    *   **Tab Switching**: When the user switches tabs (e.g., Home -> Search -> Home), the Home Page **MUST NOT** reload. It should show the previously fetched data instantly.
    *   **App Restart**: Data is fetched when the app is opened (or "cold start").
    *   **Manual Refresh**: The ONLY time the data updates while the app is open is if the user performs a **Pull-to-Refresh** action.
*   **Implementation**:
    *   Use a state management solution (Provider, Riverpod, or BLoC) to store the `HomeData` object in a Repository or Global Provider.
    *   In `HomeScreen`, check if data exists. If yes, display it. If no, fetch it.
    *   Wrap the `CustomScrollView` in a `RefreshIndicator` to allow the user to manually trigger a data update.

## 6. Cart Icon Badge
**Requirement**: The Cart icon in the AppBar must display the number of items currently in the cart.
*   **UI**: Use a Red Badge (Circle) with white text on the top-right corner of the Cart Icon.
*   **Logic**:
    *   Bind this badge to your `CartProvider` / `CartBloc`.
    *   If the cart is empty (count == 0), hide the badge.
    *   If the cart has items, show the count (e.g., "3").

## 7. Summary of Changes for Agent
1.  **Create** a repository method `fetchHomeData()` that hits the endpoint.
2.  **Modify** `HomeScreen` state to fetch this data on `initState` ONLY if not already cached in your State Provider.
3.  **Implement** `RefreshIndicator` for manual reloading.
4.  **Refactor** the `build` method:
    *   **AppBar**: Wrap the Cart Icon with a `Badge` widget listening to Cart State.
    *   **Body**: Keep Search & Banner. Replace hardcoded Category Grid with dynamic Horizontal List. Replace single "Popular" section with a `for` loop generating widgets from `data.sections`.

    