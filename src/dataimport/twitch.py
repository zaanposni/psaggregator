import os
import asyncio
from uuid import uuid4

from rich import print
from rich.console import Console
from databases import Database
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first


if not os.getenv("TWITCH_CLIENT_ID") or not os.getenv("TWITCH_CLIENT_SECRET"):
    print("TWITCH_CLIENT_ID or TWITCH_CLIENT_SECRET not set")
    exit(1)

console = Console()


async def twitch_example():
    console.log("Logging into Twitch...")
    twitch = await Twitch(
        os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET")
    )

    console.log("Fetching stream info...")

    stream = await first(twitch.get_streams(user_id="21991090"))

    console.log("Connecting to database...")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Fetching database data...")

    query = "SELECT * FROM TwitchStatus"
    result = await db.fetch_one(query)

    if stream is None:
        console.log("Stream is offline")
        if result is None:
            console.log("No entry in database. Skipping")
        else:
            console.log("Entry in database. Deleting...")
            query = "DELETE FROM TwitchStatus WHERE id = :id"
            await db.execute(query=query, values={"id": result.id})
    else:
        console.log("Stream is online")
        if result is None:
            console.log("No entry in database. Adding...")
            query = "INSERT INTO TwitchStatus (id  , title, gameName, viewers, startedAt, live, thumbnail) VALUES (:id, :title, :gameName, :viewers, :startedAt, :live, :thumbnail)"
            await db.execute(
                query=query,
                values={
                    "id": uuid4(),
                    "title": stream.title,
                    "gameName": stream.game_name,
                    "viewers": stream.viewer_count,
                    "startedAt": stream.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "live": 1 if stream.type == "live" else 0,
                    "thumbnail": stream.thumbnail_url.replace(
                        r"{width}", "1280"
                    ).replace(r"{height}", "720"),
                },
            )
        else:
            console.log("Entry in database. Updating...")
            query = "UPDATE TwitchStatus SET title = :title, gameName = :gameName, viewers = :viewers, startedAt = :startedAt, live = :live, thumbnail = :thumbnail WHERE id = :id"
            await db.execute(
                query=query,
                values={
                    "title": stream.title,
                    "gameName": stream.game_name,
                    "viewers": stream.viewer_count,
                    "startedAt": stream.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "live": 1 if stream.type == "live" else 0,
                    "thumbnail": stream.thumbnail_url.replace(
                        r"{width}", "1280"
                    ).replace(r"{height}", "720"),
                    "id": result.id,
                },
            )

    console.log("Done")

    await twitch.close()
    await db.disconnect()


# run this example
asyncio.run(twitch_example())
