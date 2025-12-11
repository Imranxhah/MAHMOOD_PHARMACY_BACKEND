
# Image Storage Analysis

## 1. Current Behavior (How it works now)
The backend uses Django's `ImageField` to store images. 
- In `products/models.py`, `Product` uses `upload_to='products/'` and `Category` uses `upload_to='categories/'`.
- **CRITICAL ISSUE**: Your `settings.py` is MISSING `MEDIA_ROOT` and `MEDIA_URL` configuration.

## 2. The Consequence
Because `MEDIA_ROOT` is undefined, Django is saving images relative to the "app" or project root, mixing data with code.
- **Product Images** are being saved directly inside the `products/` app folder (e.g., I found `products/panadolextrasoluble-Photoroom.webp` sitting next to `products/views.py`).
- **Category Images** are being saved in a `categories/` folder at the project root.

## 3. Why this is bad
- **Messy Codebase**: User-uploaded files are mixed with your Python source code.
- **Deployment Issues**: On a real server (like PythonAnywhere), you need a specific folder to serve media files from. Your current setup will break or require dangerous permissions on your code folders.

## 4. Required Fix
You must configure `settings.py` to direct all uploads to a dedicated `media` directory.

Add this to `config/settings.py`:
```python
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Your `urls.py` is already correctly set up to serve files from these settings if they exist:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
But because the settings themselves are missing, this code is currently doing nothing effectively or serving from the wrong place.
