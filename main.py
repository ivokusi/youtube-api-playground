from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

request = service.channels().list(
                part="statistics",
                forUsername="sentdex"
            )

response = request.execute()
print(response)

service.close()
