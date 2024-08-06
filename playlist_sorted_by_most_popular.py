from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

videos = list()
pageToken = ""

playlist_id = "PL8uoeex94UhHFRew8gzfFJHIpRFWyY4YW"

while True:

    pl_request = service.playlistItems().list(
                        part="contentDetails",
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken=pageToken
                    )

    pl_response = pl_request.execute()

    vid_ids = ",".join([item["contentDetails"]["videoId"] for item in pl_response["items"]])

    vid_request = service.videos().list(
                        part="statistics",
                        id=vid_ids,
                    )

    vid_response = vid_request.execute()

    for item in vid_response["items"]:

        vid_views = item["statistics"]["viewCount"]
        vid_id = item["id"]

        yt_link = f"https://youtu.be/{vid_id}"

        videos.append({
                    "views": int(vid_views),
                    "url": yt_link
                })

    pageToken = pl_response.get("nextPageToken")

    if not pageToken:
        break

videos.sort(key=lambda video: video["views"], reverse=True)

for video in videos:
    print(video["url"], video["views"])
