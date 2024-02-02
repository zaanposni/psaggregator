import requests
import os
import json
import asyncio
from uuid import uuid4

from rich.console import Console
from databases import Database
import dateutil.parser
from seleniumwire import webdriver
from seleniumwire.utils import decode


console = Console()

# create cdn directory if not exists
if not os.path.exists("/app/cdn/psde"):
    console.log("Creating /app/cdn/psde directory...", style="bold green")
    os.makedirs("/app/cdn/psde")


async def stuff() -> asyncio.coroutine:
    console.log("Starting...")

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    browser = webdriver.Firefox(
        options=options,
        seleniumwire_options={
            "disable_encoding": True,
        },
    )

    console.log("Loading page...")

    browser.get("https://www.pietsmiet.de/videos")
    browser.implicitly_wait(10)

    assert "Videos" in browser.title

    console.log("Loading data...")

    videos = None
    for request in browser.requests:
        if request.response:
            if request.url.startswith("https://www.pietsmiet.de/api/v1/videos"):
                body = decode(
                    request.response.body,
                    request.response.headers.get("Content-Encoding", "identity"),
                )
                videos = json.loads(body)
                break

    if not videos or "data" not in videos:
        raise Exception("data not found")
    videos = videos["data"]

    console.log(f"Found {len(videos)} entries")
    console.log("Closing browser...")

    browser.quit()

    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)

    console.log("Dumped data to videos.json")
    console.log("Parsing data...")

    data = []
    for video in videos:
        if not video.get("id") or not video.get("title"):
            continue
        uri = None
        imageUri = None
        publish_date = None
        if video.get("short_url"):
            uri = video["short_url"]
        if video.get("thumbnail"):
            try:
                imageUri = video["thumbnail"]["variations"][0]["url"]
            except KeyError:
                pass
            except IndexError:
                pass
        if video.get("publish_date"):
            publish_date = dateutil.parser.parse(video["publish_date"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        data.append(
            {
                "remoteId": video["id"],
                "title": video["title"],
                "duration": video["duration"],
                "uri": uri,
                "imageUri": imageUri,
                "publish_date": publish_date,
            }
        )

    console.log("Connecting to database...")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    INSERT_STATEMENT = """
    INSERT INTO ContentPiece (id  , remoteId, title, description, additionalInfo, startDate, imageUri, href, duration, importedAt, importedFrom , type) VALUES
                             (:id ,:remoteId,:title, NULL       , NULL          ,:startDate,:imageUri,:href,:duration, now()     , 'PietSmietDE', 'PSVideo');"""

    UPDATE_STATEMENT = """
    UPDATE ContentPiece SET href=:href, title=:title, duration=:duration, imageUri=:imageUri WHERE id=:id;"""

    console.log("Checking for existing entries...")
    for content in data:
        result = await db.fetch_one(
            "SELECT * FROM ContentPiece WHERE remoteId = :remoteId AND importedFrom = 'PietSmietDE'",
            values={"remoteId": content["remoteId"]},
        )
        if result:
            console.log(
                f"Found existing entry for {content['remoteId']}. Updating...",
                style="bright_magenta",
            )

            newImageUri = result.imageUri
            if result.imageUri is None and content["imageUri"] != None:
                console.log(
                    f"Try redownloading thumbnail for {content['remoteId']}...",
                    style="bright_magenta",
                )
                try:
                    thumbnail = requests.get(content["imageUri"]).content
                    filename = f"{uuid4()}.jpg"
                    with open(f"/app/cdn/psde/{filename}", "wb") as f:
                        f.write(thumbnail)
                    newImageUri = f"/cdn/psde/{filename}"
                except Exception as e:
                    console.log(f"Error downloading thumbnail: {e}", style="bold red")

            await db.execute(
                UPDATE_STATEMENT,
                values={
                    "href": content["uri"],
                    "title": content["title"],
                    "duration": content["duration"],
                    "id": result.id,
                    "imageUri": newImageUri,
                },
            )

            console.log(f"Updated entry for {content['remoteId']}.")
        else:
            console.log(
                f"Adding {content['remoteId']} to database...",
                style="bold green",
            )

            if content["imageUri"] != None:
                try:
                    thumbnail = requests.get(content["imageUri"]).content
                    filename = f"{uuid4()}.jpg"
                    with open(f"/app/cdn/psde/{filename}", "wb") as f:
                        f.write(thumbnail)
                    content["imageUri"] = f"/cdn/psde/{filename}"
                except Exception as e:
                    console.log(f"Error downloading thumbnail: {e}", style="bold red")
                    content["imageUri"] = content["imageUri"]

            await db.execute(
                INSERT_STATEMENT,
                values={
                    "id": uuid4(),
                    "remoteId": content["remoteId"],
                    "title": content["title"],
                    "startDate": content["publish_date"],
                    "imageUri": content["imageUri"],
                    "href": content["uri"],
                    "duration": content["duration"],
                },
            )

    await db.disconnect()
    console.log("Done!")


asyncio.run(stuff())
