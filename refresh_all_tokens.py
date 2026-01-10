#!/usr/bin/env python3
import os
import json
import logging
from google_auth_oauthlib.flow import InstalledAppFlow

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- CONFIGURATION ---

# Base Directory (Repo Root)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. GMAIL (PLAUD)
GMAIL_CREDENTIALS = os.path.join(REPO_ROOT, 'plaud', 'credentials.json')
GMAIL_TOKEN = os.path.join(REPO_ROOT, 'plaud', 'token.json')
GMAIL_SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly', 
    'https://www.googleapis.com/auth/gmail.modify'
]

# 2. DRIVE (AI SORTER)
DRIVE_CREDENTIALS = os.path.join(REPO_ROOT, 'toolbox', 'google-drive', 'credentials.json')
DRIVE_TOKEN = os.path.join(REPO_ROOT, 'toolbox', 'google-drive', 'token_full_drive.json')
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']


def refresh_token(name, credentials_path, token_path, scopes):
    print(f"\n{'='*60}")
    print(f"Refreshing Token: {name}")
    print(f"{'='*60}")

    if not os.path.exists(credentials_path):
        logging.error(f"Credentials file not found: {credentials_path}")
        return False

    try:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
        
        # Use OOB flow for headless/remote execution
        flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        
        print(f"\n1. Visit this URL in your browser:\n\n{auth_url}\n")
        print("2. Authorize the application.")
        code = input("3. Enter the authorization code here: ").strip()
        
        if not code:
            logging.error("No code provided.")
            return False

        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Save token
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
            
        logging.info(f"SUCCESS: Token saved to {token_path}")
        return True

    except Exception as e:
        logging.error(f"Failed to refresh {name}: {e}")
        return False

def main():
    print("Multi-Service Token Refresher")
    print("-----------------------------")
    
    success_gmail = refresh_token("Gmail (Plaud)", GMAIL_CREDENTIALS, GMAIL_TOKEN, GMAIL_SCOPES)
    success_drive = refresh_token("Google Drive (AI Sorter)", DRIVE_CREDENTIALS, DRIVE_TOKEN, DRIVE_SCOPES)
    
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    print(f"Gmail (Plaud):      {'[PASS]' if success_gmail else '[FAIL]'}")
    print(f"Drive (AI Sorter):  {'[PASS]' if success_drive else '[FAIL]'}")
    
    if success_gmail and success_drive:
        print("\nAll tokens refreshed successfully!")
    else:
        print("\nWarning: Some tokens failed to refresh.")

if __name__ == '__main__':
    main()
