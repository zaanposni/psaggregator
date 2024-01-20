import os
import asyncio
from uuid import uuid4

from rich.console import Console
from databases import Database
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first


console = Console()


async def twitch_example():
    console.log("Logging into Twitch...")
    twitch = await Twitch(
        os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET")
    )

    console.log("Fetching stream info...")

    stream = await first(twitch.get_streams(user_id="21991090"))

    console.log("Connecting to database...", style="bold green")
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
            query = "DELETE FROM TwitchStatus WHERE id = '{}'".format(result["id"])
            await db.execute(query)
    else:
        console.log("Stream is online")
        if result is None:
            console.log("No entry in database. Adding...")
            query = """INSERT INTO TwitchStatus (id  , title, gameName, viewers, startedAt, live, thumbnail)
                        VALUES                  ('{}', '{}' , '{}'    , '{}'   , '{}'     , '{}', '{}')""".format(
                uuid4(),
                stream.title,
                stream.game_name,
                stream.viewer_count,
                stream.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                1 if stream.type == "live" else 0,
                stream.thumbnail_url.replace(r"{width}", "1280").replace(
                    r"{height}", "720"
                ),
            )
            await db.execute(query)
        else:
            console.log("Entry in database. Updating...")
            query = """UPDATE TwitchStatus SET title = '{}', gameName = '{}', viewers = '{}', startedAt = '{}', live = '{}', thumbnail = '{}'
                        WHERE id = '{}'""".format(
                stream.title,
                stream.game_name,
                stream.viewer_count,
                stream.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                1 if stream.type == "live" else 0,
                stream.thumbnail_url.replace(r"{width}", "1280").replace(
                    r"{height}", "720"
                ),
                result["id"],
            )
            await db.execute(query)

    console.log("Done")

    await twitch.close()
    await db.disconnect()


# run this example
asyncio.run(twitch_example())
