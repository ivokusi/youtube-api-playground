from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import timedelta
import os
import re

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

pageToken = ""

hours_pattern = re.compile(r"(\d+)H")
minutes_pattern = re.compile(r"(\d+)M")
seconds_pattern = re.compile(r"(\d+)S")

total_seconds = 0

playlist_id = "PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU"

while True:

    pl_request = service.playlistItems().list(
                        part="contentDetails",
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken=pageToken # Empty string gives first page of results
                    )

    pl_response = pl_request.execute()

    vid_ids = ",".join([item["contentDetails"]["videoId"] for item in pl_response["items"]])

    vid_request = service.videos().list(
                        part="contentDetails",
                        id=vid_ids,
                    )

    vid_response = vid_request.execute()

    for item in vid_response["items"]:

        duration = item["contentDetails"]["duration"]
        
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
                            hours=hours,
                            minutes=minutes,
                            seconds=seconds
                        ).total_seconds()
        
        total_seconds += video_seconds

    pageToken = pl_response.get("nextPageToken")

    if not pageToken:
        break

total_seconds = int(total_seconds)
minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f"{hours}:{minutes}:{seconds}")