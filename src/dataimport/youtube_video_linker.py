import os
import requests
import asyncio
from datetime import timedelta
import html
import re

from rich.console import Console
from databases import Database
from dateutil.parser import parse

console = Console()

server_base_url = (
    os.getenv("YT_SERVER_BASE_URL")
    if os.getenv("YT_SERVER_BASE_URL")
    else "http://localhost:8080"
)
channel_ids = [
    "UCqwGaUvq_l0RKszeHhZ5leA",  # PietSmiet
    "UC3wla9xMoxDu7MIZImad1kQ",  # PietSmietTV
    "UCYCQdW5rvpLA5Jd1nM6YxxA",  # PietSmietLive
    "UC5yPQPrd8h6r3mGpbbbWVFg",  # Best of PietSmiet
]
collection_url = "https://yt.lemnoslife.com/noKey/search?part=snippet&order=date&maxResults=50&channelId={}&type=video"
youtube_url_template = "https://youtu.be/{}"

UPDATE_STATEMENT = "UPDATE ContentPiece SET description = :description, secondaryHref = :secondaryHref WHERE id = :id"


def replace_emojis_with_question_mark(text):
    # Regex pattern to match emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )

    # Replace emojis with "?"
    return emoji_pattern.sub("?", text)


async def youtube():
    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Fetching yt data...")
    for channel in channel_ids:
        console.log(f"Fetching yt data for {channel}")
        yt_data = requests.get(collection_url.format(channel)).json()["items"]

        for video in yt_data:
            console.log(f"Processing youtube video '{video['snippet']['title']}'")

            title = html.unescape(video["snippet"]["title"])
            yt_pbulish_date = parse(video["snippet"]["publishTime"])
            one_week_before = yt_pbulish_date - timedelta(days=7)
            one_week_after = yt_pbulish_date + timedelta(days=7)

            query = f"SELECT * FROM ContentPiece WHERE (title LIKE :title OR title LIKE :altTitle) AND startDate BETWEEN :lowerBoundary and :upperBoundary AND importedFrom = 'PietSmietDE' AND type = 'PSVideo'"
            values = {
                "title": title,
                "altTitle": replace_emojis_with_question_mark(title),
                "lowerBoundary": one_week_before.strftime("%Y-%m-%d %H:%M:%S"),
                "upperBoundary": one_week_after.strftime("%Y-%m-%d %H:%M:%S"),
            }

            result = await db.fetch_one(query=query, values=values)
            if not result:
                console.log(f"Could not find a matching video for '{title}'")
                continue
            if result.description is not None or result.secondaryHref is not None:
                console.log(
                    f"ContentPiece {result.id} already has a description or secondaryHref"
                )
                continue

            description = video["snippet"]["description"]
            secondaryHref = youtube_url_template.format(video["id"]["videoId"])

            values = {
                "id": result.id,
                "description": description,
                "secondaryHref": secondaryHref,
            }

            console.log(f"Updating {result.id} with secondaryHref {secondaryHref}")
            await db.execute(query=UPDATE_STATEMENT, values=values)

    await db.disconnect()
    console.log("Done")


asyncio.run(youtube())
