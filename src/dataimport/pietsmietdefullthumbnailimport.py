# This file is not actively used in psaggregator.
# It is a script that was used to import all thumbnails from PietSmiet once.
# Other imports only import recent thumbnails.
# This script generates a sql file that can be used to sync all thumbnails in combination with the pietsmietfullvideoimport.py script.

import os
import asyncio
from uuid import uuid4
import requests

from rich.console import Console
from databases import Database


console = Console()


async def stuff() -> asyncio.coroutine:
    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    handled = dict()

    query = "SELECT * FROM ContentPiece WHERE importedFrom='PietSmietDE' AND type='PSVideo' AND remoteId IS NOT NULL AND imageUri IS NOT NULL"
    console.log("Fetching all videos...", style="bold green")
    videos = await db.fetch_all(query=query)

    for index, video in enumerate(videos):
        if video.remoteId in handled:
            continue
        handled[video.remoteId] = uuid4()

        console.log(
            f"Fetching thumbnail for {video.remoteId} ({index})...", style="bold green"
        )

        thumbnail = requests.get(video.imageUri).content
        filename = f"/app/cdn/psde/{handled[video.remoteId]}.jpg"
        with open(filename, "wb") as f:
            f.write(thumbnail)

    console.log("Write mapping to file...", style="bold green")

    update_statements = list()

    for handledId, uuid in handled.items():
        update_statements.append(
            f"UPDATE ContentPiece SET imageUri='/cdn/psde/{uuid}.jpg' WHERE remoteId='{handledId}'"
        )

    with open("psde.sql", "w", encoding="utf-8") as f:
        f.writelines(update_statements)

    console.log("Done!", style="bold green")


asyncio.run(stuff())
