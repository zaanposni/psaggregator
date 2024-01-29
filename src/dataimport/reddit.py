import requests
import os
import asyncio
from datetime import datetime
from uuid import uuid4

from rich.console import Console
from databases import Database
import praw
from prawcore.exceptions import NotFound


console = Console()

# create cdn directory if not exists
if not os.path.exists("/app/cdn/reddit"):
    console.log("Creating /app/cdn/reddit directory...", style="bold green")
    os.makedirs("/app/cdn/reddit")


async def stuff() -> asyncio.coroutine:
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    console.log("Connecting to Reddit...")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="android:com.example.myredditapp:v1.2.3 (by u/kemitche)",
    )

    console.log("Fetching subreddit...")

    subreddit = reddit.subreddit("pietsmiet")

    console.log("Fetching submissions...")

    submissions = [x for x in subreddit.hot(limit=20)]

    try:
        sticky1 = subreddit.sticky(number=1)
        if sticky1.id not in [submission.id for submission in submissions]:
            submissions.append(sticky1)
        sticky2 = subreddit.sticky(number=2)
        if sticky2.id not in [submission.id for submission in submissions]:
            submissions.append(sticky2)
    except NotFound:
        console.log("No sticky found")

    if not submissions:
        raise Exception("No submissions found")

    console.log("Connecting to database...")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Deleting old data...", style="bold yellow")
    delete_query = "DELETE FROM RedditPost WHERE 1=1;"
    await db.execute(delete_query)

    console.log("Deleting old thumbnails...", style="bold yellow")
    try:
        for file in os.listdir("/app/cdn/reddit"):
            os.remove(f"/app/cdn/reddit/{file}")
    except Exception as e:
        console.log(f"Error deleting old thumbnails: {e}", style="bold red")

    INSERT_STATEMENT = """INSERT INTO RedditPost (id  , title, description, username , upvotes , comments , sticky , publishedAt , imageUri , href , importedAt) VALUES
                                                 (:id, :title, NULL       , :username, :upvotes, :comments, :sticky, :publishedAt, :imageUri, :href, now());"""

    for submission in submissions:
        console.log(f"Adding {submission.id} to database...", style="bold green")
        created_at = datetime.fromtimestamp(int(submission.created_utc)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        thumbnail = None
        if submission.thumbnail.startswith("http"):
            try:
                thubmnail_content = requests.get(submission.thumbnail).content
                thumbnail = f"{uuid4()}.jpg"
                with open(f"/app/cdn/reddit/{thumbnail}", "wb") as f:
                    f.write(thubmnail_content)
                thumbnail = f"/cdn/reddit/{thumbnail}"
            except Exception as e:
                console.log(f"Error downloading thumbnail: {e}", style="bold red")
                thumbnail = submission.thumbnail

        await db.execute(
            query=INSERT_STATEMENT,
            values={
                "id": submission.id,
                "title": submission.title,
                "username": submission.author.name,
                "upvotes": submission.score,
                "comments": submission.num_comments,
                "sticky": 1 if submission.stickied else 0,
                "publishedAt": created_at,
                "imageUri": thumbnail,
                "href": f"https://reddit.com{submission.permalink}",
            },
        )

    await db.disconnect()
    console.log("Done!")


asyncio.run(stuff())
