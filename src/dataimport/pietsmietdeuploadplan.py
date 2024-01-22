import os
import asyncio
import json
import re
from datetime import datetime
from uuid import uuid4
from typing import List

from rich.console import Console
from databases import Database
import dateutil.parser
from seleniumwire import webdriver
from seleniumwire.utils import decode


console = Console()


class ContentPiece:
    def __init__(
        self,
        remoteId: str,
        duration: int,
        title: str,
        time: datetime,
        uri: str,
        secondaryUri: str,
        type="PSVideo",
    ):
        self.id = uuid4()
        self.remoteId = remoteId
        self.duration = duration
        self.title = title
        self.time = time
        self.uri = uri
        self.secUri = secondaryUri
        self.type = type


def remove_html_tags(text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


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

    browser.get("https://www.pietsmiet.de/uploadplan")
    browser.implicitly_wait(10)

    assert "Uploadplan" in browser.title

    console.log("Loading data...", style="bold green")

    uploadplan = None
    upcoming_events = None
    for request in browser.requests:
        if request.response:
            if request.url == "https://www.pietsmiet.de/api/v1/schedules":
                body = decode(
                    request.response.body,
                    request.response.headers.get("Content-Encoding", "identity"),
                )
                uploadplan = json.loads(body)
            if request.url == "https://www.pietsmiet.de/api/v1/schedules/upcoming":
                body = decode(
                    request.response.body,
                    request.response.headers.get("Content-Encoding", "identity"),
                )
                upcoming_events = json.loads(body)

    console.log("Closing browser...", style="bold green")

    browser.quit()

    if not uploadplan:
        raise Exception("Uploadplan not found")

    console.log(f"Found uploadplan for date {uploadplan['data'][0]['date']}")
    console.log(f"Found {len(uploadplan['data'][0]['items'])} entries")

    if upcoming_events:
        console.log(f"Found {len(upcoming_events['data'])} upcoming events")

    information = None
    information_default_texts = [
        x.strip().lower()
        for x in [
            "Alle Angaben ohne Gewähr.",
            "Alle Angaben ohne Gewähr. Kurzfristige Änderungen möglich.",
        ]
    ]
    if information_text := uploadplan["data"][0]["description"]:
        information_text = remove_html_tags(information_text).strip()
        if information_text.lower() not in information_default_texts:
            information = information_text.replace("'", "\\'")
            console.log(f"Found information: {information}")

    with open("uploadplan.json", "w", encoding="utf-8") as f:
        json.dump(uploadplan, f, ensure_ascii=False, indent=4)

    if upcoming_events:
        with open("upcoming.json", "w", encoding="utf-8") as f:
            json.dump(upcoming_events, f, ensure_ascii=False, indent=4)

    console.log("Dumped data to uploadplan.json and upcoming.json", style="bold green")
    console.log("Parsing data...", style="bold green")

    if not uploadplan["success"]:
        raise Exception("Uploadplan not successful")

    data: List[ContentPiece] = []
    for content in uploadplan["data"][0]["items"]:
        uri = "NULL"
        remoteId = "NULL"
        secondaryUri = "NULL"
        duration = "NULL"
        if content["video"]:
            uri = f"'{content['video']['short_url']}'"
            remoteId = f"'{content['video']['id']}'"
            duration = content["video"]["duration"]
        if content["external_url"]:
            secondaryUri = f"'{content['external_url']}'"

        if uri == "NULL" and secondaryUri != "NULL":
            uri = secondaryUri
            secondaryUri = "NULL"

        time = content["publish_date"]
        time = dateutil.parser.parse(time)

        content_type = "PSVideo"
        if content.get("external_url_platform") == "twitch":
            content_type = "TwitchStream"

        data.append(
            ContentPiece(
                remoteId,
                duration,
                content["title"],
                time,
                uri,
                secondaryUri,
                type=content_type,
            )
        )

    if upcoming_events and upcoming_events["data"]:
        for index in upcoming_events["data"]:
            for content in index["items"]:
                uri = "NULL"
                if content["video"]:
                    uri = f"'{content['video']['short_url']}'"
                    duration = content["video"]["duration"]
                if content["external_url"]:
                    uri = f"'{content['external_url']}'"

                time = content["publish_date"]
                time = dateutil.parser.parse(time)

                data.append(
                    ContentPiece(
                        remoteId="NULL",
                        duration="NULL",
                        title=content["title"].replace("'", "\\'"),
                        time=time,
                        uri=uri,
                        secondaryUri="NULL",
                        type="TwitchStream",
                    )
                )

    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    INSERT_STATEMENT = """
    INSERT INTO ScheduledContentPiece (id  , remoteId, title, description, additionalInfo, startDate, imageUri, href, secondaryHref, duration, importedAt, importedFrom , type) VALUES
                                      ('{}', {}      , '{}' , NULL       , NULL          , '{}'     , NULL    , {}  , {}           , {}      , now()     , 'PietSmietDE', '{}');"""
    UPDATE_STATEMENT = """
    UPDATE ScheduledContentPiece SET startDate='{}', href={}, secondaryHref={}, remoteId={}, duration={} WHERE id='{}';"""

    EXISTING_FOR_DATE = "SELECT * FROM ScheduledContentPiece WHERE DATE(startDate) = '{}' AND importedFrom = 'PietSmietDE' AND type = 'Video'"
    existing_imports_for_today = await db.fetch_all(
        EXISTING_FOR_DATE.format(uploadplan["data"][0]["date"])
    )

    console.log("Checking for existing entries...", style="bold green")
    for content in data:
        query = "SELECT * FROM ScheduledContentPiece WHERE title = '{}' AND DATE(startDate) = '{}' AND type = '{}'".format(
            content.title, content.time.strftime("%Y-%m-%d"), content.type
        )
        result = await db.fetch_all(query)

        if len(result) > 0:
            console.log(
                f"Found existing entry for {content.title} on {content.time}. Updating...",
                style="bold yellow",
            )

            query = UPDATE_STATEMENT.format(
                content.time.strftime("%Y-%m-%d %H:%M:%S"),
                content.uri,
                content.secUri,
                content.remoteId,
                content.duration,
                result[0]["id"],
            )
            await db.execute(query)
            console.log(f"Updated entry for {content.title} on {content.time}.")
        elif content.type == "TwitchStream" or not existing_imports_for_today:
            if content.type == "TwitchStream":
                query = "SELECT * FROM ScheduledContentPiece WHERE startDate = '{}' AND type = 'TwitchStream'".format(
                    content.time.strftime("%Y-%m-%d %H:%M:%S")
                )
                result = await db.fetch_all(query)
                if len(result) > 0:
                    console.log(
                        f"Found existing entry for stream {content.title} on {content.time}. Skipping...",
                        style="bold yellow",
                    )
                    continue

            console.log(
                f"Adding {content.title} on {content.time} to database...",
                style="bold yellow",
            )

            query = INSERT_STATEMENT.format(
                content.id,
                content.remoteId,
                content.title,
                content.time.strftime("%Y-%m-%d %H:%M:%S"),
                content.uri,
                content.secUri,
                content.duration,
                content.type,
            )
            await db.execute(query)
        else:
            console.log(
                f"Skipping {content.title} on {content.time} as there is already an import for today.",
                style="bold yellow",
            )

    if information:
        console.log("Checking for existing information")
        query = f"SELECT * FROM Information WHERE importedFrom = 'PietSmietDE' AND DATE(date) = '{uploadplan['data'][0]['date']}'"
        result = await db.fetch_all(query)
        if len(result) > 0:
            console.log("Found existing information. Updating...")
            query = f"UPDATE Information SET text = '{information}' WHERE id = '{result[0]['id']}'"
            await db.execute(query)
        else:
            console.log("Adding information to database...")
            query = f"""INSERT INTO Information
              (id         , remoteId, text           , imageUri, href                                 , date                             , importedAt, importedFrom) VALUES
              ('{uuid4()}', NULL    , '{information}', NULL    , 'https://www.pietsmiet.de/uploadplan', '{uploadplan['data'][0]['date']}', now()     , 'PietSmietDE')"""
            await db.execute(query)

    await db.disconnect()
    console.log("Done!", style="bold green")


asyncio.run(stuff())
