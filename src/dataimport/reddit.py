import os
import asyncio
from datetime import datetime

from rich.console import Console
from databases import Database
import praw
from prawcore.exceptions import NotFound


console = Console()


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

    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Deleting old data...", style="bold green")
    delete_query = "DELETE FROM RedditPost WHERE 1=1;"
    await db.execute(delete_query)

    INSERT_STATEMENT = """INSERT INTO RedditPost (id  , title, description, username, upvotes, comments, sticky, publishedAt, imageUri, href, importedAt) VALUES
                                                 ('{}', '{}' , NULL       , '{}'    , {}     , {}      , {}    , '{}'       , {}      , '{}', now());"""

    for submission in submissions:
        console.log(f"Adding {submission.id} to database...", style="bold yellow")
        created_at = datetime.fromtimestamp(int(submission.created_utc)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        thumbnail = "NULL"
        if submission.thumbnail.startswith("http"):
            thumbnail = f"'{submission.thumbnail}'"

        query = INSERT_STATEMENT.format(
            submission.id,
            submission.title.replace("'", "\\'"),
            submission.author.name,
            submission.score,
            submission.num_comments,
            1 if submission.stickied else 0,
            created_at,
            thumbnail,
            f"https://reddit.com{submission.permalink}",
        )

        await db.execute(query)

    await db.disconnect()
    console.log("Done!", style="bold green")


asyncio.run(stuff())
