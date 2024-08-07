from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

credentials = None

if os.path.exists("token.pickle"):
    print("Loading Credentials From File...")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    
    if credentials and credentials.expired and credentials.refresh_token:
        
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    
    else:
        
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secrets.json",
                    scopes=["https://www.googleapis.com/auth/youtube.readonly"]
                )

        flow.run_local_server(
                port=8080, 
                prompt="consent", 
                authorization_prompt_message=""
            )

        credentials = flow.credentials

        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

service = build("youtube", "v3", credentials=credentials)

request = service.playlistItems().list(
                part="status",
                playlistId=""
            )

response = request.execute()

print(response)
