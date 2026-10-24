# API overview

[Back to the README](../README.md)

Local base URL: `http://127.0.0.1:8000/api/`. Paths below are relative to that prefix.

## Route map

| Area | Representative routes |
| --- | --- |
| Authentication | `auth/register/`, `auth/verify/`, `auth/login/`, `auth/refresh/` |
| Passwords | `auth/password/reset/`, `auth/password/reset/confirm/`, `auth/password/change/` |
| Account | `users/profile/`, `addresses/` |
| Catalog | `categories/`, `products/`, `products/home/` |
| Favorites | `favorites/`, `favorites/toggle/` |
| Orders | `orders/`, `cart/validate/`, `delivery-charges/` |
| Prescriptions | `prescriptions/`, `prescriptions/upload/` |
| Branches | `branches/`, `branches/nearest/` |
| Marketing | `marketing/banners/` |
| Notifications | `notifications/` |
| Analytics | `analytics/dashboard/` |

Permissions and accepted methods vary by endpoint. Catalog reads are public; protected endpoints use JWT bearer authentication. Write/admin operations require the permissions implemented in their views.

## Browse products

```bash
curl "http://127.0.0.1:8000/api/products/?search=sample&ordering=price"
```

Implemented query parameters include `search`, `category`, `min_price`, `max_price`, and `ordering`. Search covers product and category names; ordering supports `price`, `created_at`, and `stock`. Prefix an ordering field with `-` for descending order.

## Authenticate

Use an active local test account. Save this example as a local `login.json`, substituting your own test credentials:

```json
{
  "email": "developer@example.com",
  "password": "replace-with-your-local-test-password"
}
```

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login/" -H "Content-Type: application/json" --data-binary "@login.json"
```

The response contains access/refresh tokens. Do not commit the request file or share the tokens. On Windows PowerShell use `curl.exe` where `curl` resolves to a shell alias.

## Call a protected endpoint

```bash
curl "http://127.0.0.1:8000/api/users/profile/" -H "Authorization: Bearer <access-token>"
```

Refresh by posting `{"refresh":"<refresh-token>"}` to `auth/refresh/`. Current settings rotate refresh tokens; the client must store the refreshed value as well as the new access token.

## Source of truth

Start at [config/urls.py](../config/urls.py), then inspect each app's `urls.py`, `views.py`, and `serializers.py` for exact fields and permissions. This page is an orientation guide, not a complete OpenAPI contract.

The existing [Flutter guide](../flutter_api_guide.md), [prescription guide](../prescriptions_api_guide.md), and [notification guide](../notifications_api_guide.md) provide further examples; confirm them against the current source.
