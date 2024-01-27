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


async def stuff() -> asyncio.coroutine:
    console.log("Starting...", style="bold green")

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    browser = webdriver.Firefox(
        options=options,
        seleniumwire_options={
            "disable_encoding": True,
        },
    )

    console.log("Loading page...", style="bold green")

    browser.get("https://www.pietsmiet.de/videos")
    browser.implicitly_wait(10)

    assert "Videos" in browser.title

    console.log("Loading data...", style="bold green")

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
    console.log("Closing browser...", style="bold green")

    browser.quit()

    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)

    console.log("Dumped data to videos.json", style="bold green")
    console.log("Parsing data...", style="bold green")

    data = []
    for video in videos:
        if not video.get("id") or not video.get("title"):
            continue
        uri = "NULL"
        imageUri = "NULL"
        publish_date = "NULL"
        if video.get("short_url"):
            uri = f"'{video['short_url']}'"
        if video.get("thumbnail"):
            try:
                imageUri = f"'{video['thumbnail']['variations'][0]['url']}'"
            except KeyError:
                pass
            except IndexError:
                pass
        if video.get("publish_date"):
            publish_date = f"'{dateutil.parser.parse(video['publish_date']).strftime('%Y-%m-%d %H:%M:%S')}'"

        data.append(
            {
                "remoteId": video["id"],
                "title": video["title"].replace("'", "\\'"),
                "duration": video["duration"],
                "uri": uri,
                "imageUri": imageUri,
                "publish_date": publish_date,
            }
        )

    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    INSERT_STATEMENT = """
    INSERT INTO ContentPiece (id  , remoteId, title, description, additionalInfo, startDate, imageUri, href, duration, importedAt, importedFrom , type) VALUES
                             ('{}', '{}'    , '{}' , NULL       , NULL          , {}       , {}      , {}  , {}      , now()     , 'PietSmietDE', 'PSVideo');"""
    UPDATE_STATEMENT = """
    UPDATE ContentPiece SET href={}, title='{}', duration={} WHERE id='{}';"""

    console.log("Checking for existing entries...", style="bold green")
    for content in data:
        query = "SELECT * FROM ContentPiece WHERE remoteId = '{}' AND importedFrom = 'PietSmietDE'".format(
            content["remoteId"]
        )
        result = await db.fetch_all(query)
        if len(result) > 0:
            console.log(
                f"Found existing entry for {content['remoteId']}. Updating...",
                style="bold yellow",
            )

            query = UPDATE_STATEMENT.format(
                content["uri"],
                content["title"],
                content["duration"],
                result[0]["id"],
            )
            await db.execute(query)
            console.log(f"Updated entry for {content['remoteId']}.")
        else:
            console.log(
                f"Adding {content['remoteId']} to database...",
                style="bold yellow",
            )

            if content["imageUri"] != "NULL":
                try:
                    thumbnail = requests.get(content["imageUri"]).content
                    filename = f"{uuid4()}.jpg"
                    with open(f"/app/cdn/psde/{filename}", "wb") as f:
                        f.write(thumbnail)
                    content["imageUri"] = f"/cdn/psde/{filename}"
                except Exception as e:
                    console.log(f"Error downloading thumbnail: {e}", style="bold red")

            query = INSERT_STATEMENT.format(
                uuid4(),
                content["remoteId"],
                content["title"],
                content["publish_date"],
                content["imageUri"],
                content["uri"],
                content["duration"],
            )
            await db.execute(query)

    await db.disconnect()
    console.log("Done!", style="bold green")


asyncio.run(stuff())
