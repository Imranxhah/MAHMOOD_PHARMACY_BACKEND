# Firebase Setup Guide for Mahmood Pharmacy

Follow these steps to set up the Firebase project exactly as needed for our backend notification system.

## Phase 1: Create Project & Android App

1.  **Go to Console**: Open [Firebase Console](https://console.firebase.google.com/).
2.  **Create Project**: Click **"Add project"** -> Name it `Mahmood Pharmacy` -> Continue -> (Analytics is optional) -> **Create Project**.
3.  **Add Android App**:
    *   Click the **Android Icon** (robot) in the project overview.
    *   **Package Name**: Open your Flutter project on your computer. Look at `android/app/build.gradle`. Find `applicationId`. It usually looks like `com.example.mahmood_pharmacy`. **Copy this exactly.**
    *   **Register App**.
    *   **Download config file**: Download `google-services.json`.
    *   **Action**: Move this file to your Flutter app folder: `mahmood_pharmacy_app/android/app/google-services.json` (This is for the Frontend).

## Phase 2: Generate Backend Credentials (CRUTICAL)

This is the part I (the backend agent) need to send messages.

1.  In Firebase Console, click the **Gear Icon (Settings)** > **Project settings**.
2.  Go to the **Service accounts** tab.
3.  Click **Generate new private key**.
4.  Confirm by clicking **Generate key**.
5.  A file (JSON) will download. It will have a long name like `mahmood-pharmacy-firebase-adminsdk-xxxxx.json`.
6.  **Rename** this file to: `serviceAccountKey.json`.
7.  **Move** this file to your **Django Project Root** (the same folder where `manage.py` is).
    *   Location: `c:\Users\kpk laptops\Desktop\MAHMOOD_PHARMACY_BACKEND\serviceAccountKey.json`

## Phase 3: Configure Environment (.env)

I need to know where this file is.

1.  Open your `.env` file in the backend folder.
2.  Add this line at the bottom:

```env
FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json
```

## Checklist before we code:
- [ ] Created Firebase Project.
- [ ] Downloaded `google-services.json` (for Flutter).
- [ ] Downloaded and renamed `serviceAccountKey.json` (for Django).
- [ ] Placed `serviceAccountKey.json` in `c:\Users\kpk laptops\Desktop\MAHMOOD_PHARMACY_BACKEND\`.
- [ ] Added `FIREBASE_CREDENTIALS_PATH` to `.env`.

**Once you have placed the `serviceAccountKey.json` file in the folder, let me know, and I will write the code to use it.**
