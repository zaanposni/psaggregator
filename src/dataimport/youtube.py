import os
import requests
import asyncio
import re
from uuid import uuid4
from datetime import datetime, timedelta

from rich.console import Console
from databases import Database


console = Console()

# create cdn directory if not exists
if not os.path.exists("/app/cdn/yt"):
    console.log("Creating /app/cdn/yt directory...", style="bold green")
    os.makedirs("/app/cdn/yt")

server_base_url = (
    os.getenv("YT_SERVER_BASE_URL")
    if os.getenv("YT_SERVER_BASE_URL")
    else "http://localhost:8080"
)
channel_id = "UCqwGaUvq_l0RKszeHhZ5leA"
collection_url = (
    f"{server_base_url}/channels?part=community&id={channel_id}&include=snippet"
)
ressource_url = server_base_url + "/community?part=snippet&id={}"
direct_url = "https://www.youtube.com/channel/" + channel_id + "/community?lb={}"

INSERT_STATEMENT = """
    INSERT INTO Information (id  , remoteId, text, imageUri, href, date, importedAt, analyzedAt, importedFrom)
                    VALUES  (:id, :remoteId, :text, :imageUri, :href, :date, now() , NULL, 'YouTube')"""

DAY_REGEX = re.compile(r"(\d+) days? ago")
MONTH_REGEX = re.compile(r"(\d+) months? ago")


async def youtube():
    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Fetching yt data...")
    yt_data = requests.get(collection_url).json()["items"][0]["community"]

    for yt in yt_data:
        query = f"SELECT * FROM Information WHERE remoteId = :remoteId AND importedFrom = :importedFrom"
        result = await db.fetch_one(
            query=query, values={"remoteId": yt["id"], "importedFrom": "YouTube"}
        )
        if result:
            console.log(f"{yt['id']} already in database", style="bold red")
            continue

        details = requests.get(ressource_url.format(yt["id"])).json()["items"][0][
            "snippet"
        ]

        text = ""
        thumbnailUri = None
        date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        for content in yt["contentText"]:
            if "text" in content:
                text += content["text"]

        # the inofficial youtube api does not return precise dates so we have to calculate estimates
        if match := DAY_REGEX.search(yt["date"]):
            days = int(match.group(1))
            date = (datetime.utcnow() - timedelta(days=days)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        elif match := MONTH_REGEX.search(yt["date"]):
            months = int(match.group(1))
            date = (datetime.utcnow() - timedelta(days=months * 30)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        if "images" in details:
            try:
                thumbnailUri = details["images"][0]["thumbnails"][-1]["url"]
            except IndexError:
                pass
            except KeyError:
                pass

        if thumbnailUri != None:
            # download thumbnail and store it in /app/cdn/yt/
            console.log(f"Downloading thumbnail for {yt['id']}")
            try:
                thumbnail = requests.get(thumbnailUri).content
                filename = f"{uuid4()}.jpg"
                with open(f"/app/cdn/yt/{filename}", "wb") as f:
                    f.write(thumbnail)
                thumbnailUri = f"/cdn/yt/{filename}"
            except Exception as e:
                console.log(f"Error downloading thumbnail: {e}", style="bold red")
                thumbnailUri = None

        values = {
            "id": uuid4(),
            "remoteId": yt["id"],
            "text": text,
            "imageUri": thumbnailUri,
            "href": direct_url.format(yt["id"]),
            "date": date,
        }

        console.log(f"Insert {yt['id']} into database", style="bold green")
        await db.execute(query=INSERT_STATEMENT, values=values)

    await db.disconnect()
    console.log("Done")


asyncio.run(youtube())
