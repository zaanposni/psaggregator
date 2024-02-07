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

    browser.get("https://www.pietsmiet.de/uploadplan")
    browser.implicitly_wait(10)

    assert "Uploadplan" in browser.title

    console.log("Loading data...")

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

    console.log("Closing browser...")

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
            information = information_text
            console.log(f"Found information: {information}")

    with open("uploadplan.json", "w", encoding="utf-8") as f:
        json.dump(uploadplan, f, ensure_ascii=False, indent=4)

    if upcoming_events:
        with open("upcoming.json", "w", encoding="utf-8") as f:
            json.dump(upcoming_events, f, ensure_ascii=False, indent=4)

    console.log("Dumped data to uploadplan.json and upcoming.json")
    console.log("Parsing data...")

    if not uploadplan["success"]:
        raise Exception("Uploadplan not successful")

    data: List[ContentPiece] = []
    for content in uploadplan["data"][0]["items"]:
        uri = None
        remoteId = None
        secondaryUri = None
        duration = None
        if content["video"]:
            uri = content["video"]["short_url"]
            remoteId = content["video"]["id"]
            duration = content["video"]["duration"]
        if content["external_url"]:
            secondaryUri = content["external_url"]

        if uri == None and secondaryUri != None:
            uri = secondaryUri
            secondaryUri = None

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
                uri = None
                if content["video"]:
                    uri = content['video']['short_url']
                    duration = content["video"]["duration"]
                if content["external_url"]:
                    uri = content['external_url']

                time = content["publish_date"]
                time = dateutil.parser.parse(time)

                data.append(
                    ContentPiece(
                        remoteId=None,
                        duration=None,
                        title=content["title"].replace("Stream: ", ""),
                        time=time,
                        uri=uri,
                        secondaryUri=None,
                        type="TwitchStream",
                    )
                )

    console.log("Connecting to database...")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    INSERT_STATEMENT = """
    INSERT INTO ScheduledContentPiece ( id, remoteId, title, description, additionalInfo, startDate, imageUri, href, secondaryHref, duration, importedAt, importedFrom , type) VALUES
                                      (:id,:remoteId,:title, NULL       , NULL          ,:startDate, NULL    ,:href,:secondaryHref,:duration, now()     , 'PietSmietDE',:type);"""
    UPDATE_STATEMENT = """
    UPDATE ScheduledContentPiece SET startDate=:startDate, href=:href, secondaryHref=:secondaryHref, remoteId=:remoteId, duration=:duration WHERE id=:id;"""

    existing_imports_for_today = await db.fetch_all(
        "SELECT * FROM ScheduledContentPiece WHERE DATE(startDate) = :startDate AND importedFrom = 'PietSmietDE' AND type = 'Video'",
        values={"startDate": uploadplan["data"][0]["date"]},
    )

    console.log("Checking for existing entries...")
    for content in data:
        result = await db.fetch_one(
            "SELECT * FROM ScheduledContentPiece WHERE title = :title AND DATE(startDate) = :startDate AND type = :type",
            values={
                "title": content.title,
                "startDate": content.time.strftime("%Y-%m-%d"),
                "type": content.type,
            },
        )

        if result:
            console.log(
                f"Found existing entry for {content.title} on {content.time}. Updating...",
                style="bright_magenta",
            )

            await db.execute(
                UPDATE_STATEMENT,
                values={
                    "startDate": content.time.strftime("%Y-%m-%d %H:%M:%S"),
                    "href": content.uri,
                    "secondaryHref": content.secUri,
                    "remoteId": content.remoteId,
                    "duration": content.duration,
                    "id": result.id,
                },
            )
            console.log(f"Updated entry for {content.title} on {content.time}.")
        elif content.type == "TwitchStream" or not existing_imports_for_today:
            if content.type == "TwitchStream":
                result = await db.fetch_all(
                    "SELECT * FROM ScheduledContentPiece WHERE startDate = :startDate AND type = 'TwitchStream'",
                    values={"startDate": content.time.strftime("%Y-%m-%d %H:%M:%S")},
                )
                if len(result) > 0:
                    console.log(
                        f"Found existing entry for stream {content.title} on {content.time}. Skipping..."
                    )
                    continue

            console.log(
                f"Adding {content.title} on {content.time} to database...",
                style="bold green",
            )

            await db.execute(
                INSERT_STATEMENT,
                values={
                    "id": content.id,
                    "remoteId": content.remoteId,
                    "title": content.title,
                    "startDate": content.time.strftime("%Y-%m-%d %H:%M:%S"),
                    "href": content.uri,
                    "secondaryHref": content.secUri,
                    "duration": content.duration,
                    "type": content.type,
                },
            )
        else:
            console.log(
                f"Skipping {content.title} on {content.time} as there is already an import for today."
            )

    if information:
        console.log("Checking for existing information")
        result = await db.fetch_one(
            "SELECT * FROM Information WHERE importedFrom = 'PietSmietDE' AND DATE(date) = :date",
            values={"date": uploadplan["data"][0]["date"]},
        )
        if result:
            console.log(
                "Found existing information. Updating...", style="bright_magenta"
            )
            await db.execute(
                "UPDATE Information SET text = :text WHERE id = :id",
                values={"text": information, "id": result.id},
            )
        else:
            console.log("Adding information to database...", style="bold green")
            query = f"""INSERT INTO Information
              ( id, remoteId, text, imageUri, href                                 , date, importedAt, importedFrom) VALUES
              (:id, NULL    ,:text, NULL    , 'https://www.pietsmiet.de/uploadplan',:date, now()     , 'PietSmietDE')"""
            await db.execute(
                query,
                values={
                    "id": uuid4(),
                    "text": information,
                    "date": uploadplan["data"][0]["date"],
                },
            )

    await db.disconnect()
    console.log("Done!")


asyncio.run(stuff())
