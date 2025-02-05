import os
import requests
import asyncio
from uuid import uuid4
from PIL import Image
from io import BytesIO
from datetime import datetime, timezone

from rich.console import Console
from databases import Database
from dateutil.parser import parse
import isodate

console = Console()

# create cdn directory if not exists
if not os.path.exists("/app/cdn/ytv"):
    console.log("Creating /app/cdn/ytv directory...", style="bold green")
    os.makedirs("/app/cdn/ytv")

youtube_key = os.getenv("YOUTUBE_API_KEY")

if not youtube_key:
    raise Exception("YOUTUBE_API_KEY not set")

PS_DE_CUT_OFF_DATE = datetime(2025, 2, 2, 0, 0, 0, tzinfo=timezone.utc)

channel_ids = [
    "UCqwGaUvq_l0RKszeHhZ5leA",  # PietSmiet
    "UC3wla9xMoxDu7MIZImad1kQ",  # PietSmietTV
    "UCYCQdW5rvpLA5Jd1nM6YxxA",  # PietSmietLive
    "UC5yPQPrd8h6r3mGpbbbWVFg",  # Best of PietSmiet
]
collection_url = "https://www.googleapis.com/youtube/v3/search?part=snippet&order=date&maxResults=50&channelId={}&type=video&key={}"
details_url = (
    "https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}"
)

youtube_url_template = "https://youtu.be/{}"
thumbnail_url_template = "https://img.youtube.com/vi/{}/maxresdefault.jpg"


INSERT_STATEMENT = """
    INSERT INTO ContentPiece (id  , remoteId, title, description, additionalInfo, startDate, imageUri, href, duration, importedAt, importedFrom , type) VALUES
                             (:id ,:remoteId,:title,:description, NULL          ,:startDate,:imageUri,:href,:duration, now()     , 'YouTube', 'PSVideo');"""


async def youtube():
    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Fetching yt data...")
    for channel in channel_ids:
        console.log(f"Fetching yt data for {channel}")
        yt_data = requests.get(collection_url.format(channel, youtube_key)).json()[
            "items"
        ]

        for video in yt_data:
            console.log(f"Processing youtube video '{video['snippet']['title']}'")

            yt_pbulish_date = parse(video["snippet"]["publishTime"])

            if yt_pbulish_date < PS_DE_CUT_OFF_DATE:
                console.log(
                    f"Skipping video '{video['snippet']['title']}' because it is older than {PS_DE_CUT_OFF_DATE}",
                    style="bold red",
                )
                continue

            remoteId = video["id"]["videoId"]

            query = f"SELECT * FROM IgnoreYouTubeVideos WHERE remoteId = :remoteId"
            result = await db.fetch_one(query=query, values={"remoteId": remoteId})
            if result:
                console.log(f"{remoteId} is in ignore list", style="bold red")
                continue

            query = f"SELECT * FROM ContentPiece WHERE remoteId = :remoteId AND importedFrom = 'YouTube'"
            result = await db.fetch_one(query=query, values={"remoteId": remoteId})
            if result:
                console.log(f"{remoteId} already in database", style="bold red")
                continue

            details = requests.get(details_url.format(remoteId, youtube_key)).json()[
                "items"
            ][0]

            title = video["snippet"]["title"]
            description = video["snippet"]["description"]
            href = youtube_url_template.format(video["id"]["videoId"])
            raw_duration = details["contentDetails"]["duration"]
            duration = isodate.parse_duration(raw_duration).total_seconds()

            if duration <= 300:
                insert_query = (
                    "INSERT INTO IgnoreYouTubeVideos (remoteId) VALUES (:remoteId)"
                )
                await db.execute(insert_query, values={"remoteId": remoteId})

                console.log(
                    f"Skipping video '{title}' because it is shorter than 5 minutes. Added to ignore list. Duration: {duration}",
                    style="bold red",
                )
                continue

            yt_thumbnail_url = thumbnail_url_template.format(remoteId)
            imageUri = None

            filename_id = uuid4()
            try:
                thumbnail = requests.get(yt_thumbnail_url).content
                with open(f"/app/cdn/ytv/{filename_id}.jpg", "wb") as f:
                    f.write(thumbnail)
                imageUri = f"/cdn/ytv/{filename_id}.jpg"
            except imageUri as e:
                console.log(f"Error downloading thumbnail: {e}", style="bold red")
                continue

            try:
                console.log(
                    f"Resizing thumbnail for {yt_thumbnail_url}...",
                    style="bright_magenta",
                )
                image = Image.open(BytesIO(thumbnail))
                width, height = 300, int((300 / image.width) * image.height)
                resized_300 = image.resize((width, height))
                resized_300.save(f"/app/cdn/ytv/{filename_id}-w300.jpg")

                width, height = 768, int((768 / image.width) * image.height)
                resized_768 = image.resize((width, height))
                resized_768.save(f"/app/cdn/ytv/{filename_id}-w768.jpg")
            except Exception as e:
                console.log(f"Error resizing thumbnail: {e}", style="bold red")

            await db.execute(
                INSERT_STATEMENT,
                values={
                    "id": uuid4(),
                    "remoteId": remoteId,
                    "title": title,
                    "description": description,
                    "startDate": yt_pbulish_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "imageUri": imageUri,
                    "href": href,
                    "duration": duration,
                },
            )

    await db.disconnect()
    console.log("Done")


asyncio.run(youtube())
