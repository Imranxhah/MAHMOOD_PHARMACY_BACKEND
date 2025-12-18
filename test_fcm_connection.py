import firebase_admin
from firebase_admin import credentials
import os

try:
    cred_path = 'serviceAccountKey.json'
    if not os.path.exists(cred_path):
        print(f"Error: {cred_path} not found.")
        exit(1)
        
    print(f"Found {cred_path}...")
    cred = credentials.Certificate(cred_path)
    
    # Try to initialize (this validates the JSON structure and key signature locally)
    # We use a unique name to avoid conflicts if run multiple times or in same process
    try:
        app = firebase_admin.initialize_app(cred, name='test_verification_app')
        print("SUCCESS: Credentials are valid and Firebase App initialized.")
    except Exception as e:
        print(f"ERROR: Failed to initialize Firebase App. Reason: {e}")
        exit(1)

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
