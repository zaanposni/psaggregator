import asyncio
import os
from datetime import datetime, timedelta

from databases import Database
from rich.console import Console


console = Console()

# create cdn directory if not exists
CDN_DIRECTORY = "/app/cdn/instagram/"
RELATIVE_CDN_DIRECTORY = "/app"
if not os.path.exists(CDN_DIRECTORY):
    console.log(f"{CDN_DIRECTORY} does not exist, exiting", style="bold red")
    exit()

DELETE_QUERY_INFORMATION = "DELETE FROM Information WHERE id = :id"
one_day_ago = datetime.now() - timedelta(days=1)
SELECT_QUERY_INFORMATION = "SELECT Information.id, Information.imageUri, InformationResource.videoUri FROM Information LEFT JOIN InformationResource ON Information.id = InformationResource.informationId WHERE Information.importedFrom = 'InstagramStory' AND Information.date < :one_day_ago"


async def instagram():
    console.log("Connecting to database...", style="bold green")
    db = Database(os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Fetching stories for deletion")
    stories = await db.fetch_all(SELECT_QUERY_INFORMATION, {"one_day_ago": one_day_ago})
    console.log(f"Found {len(stories)} stories to delete")

    for story in stories:
        console.log(f"Try deleting local files for story {story.id}")
        try:
            os.remove(f"{RELATIVE_CDN_DIRECTORY}{story.imageUri}")
            os.remove(f"{RELATIVE_CDN_DIRECTORY}{story.videoUri}")
            console.log(f"Deleted local files for story {story.id}")
        except FileNotFoundError:
            console.log(f"Local files for story {story.id} not found", style="yellow")
            console.log(f"{RELATIVE_CDN_DIRECTORY}{story.imageUri}")
            console.log(f"{RELATIVE_CDN_DIRECTORY}{story.videoUri}")
            continue
        except Exception as e:
            console.log(f"Error deleting local files for story {story.id}", style="red")
            console.log(e)
            continue

        console.log(f"Deleting story {story.id} from database", style="red")
        await db.execute(DELETE_QUERY_INFORMATION, {"id": story.id})
        console.log(f"Deleted story {story.id} from database")

    console.log("Done")


asyncio.run(instagram())
