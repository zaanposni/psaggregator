import asyncio
import os
import time
import random
from databases import Database
from uuid import uuid4

import requests
from rich.console import Console
from tweety import Twitter
from tweety.types import Tweet, SelfThread, ConversationThread


INSERT_QUERY_INFORMATION = """
    INSERT INTO Information (id, remoteId, text, additionalInfo, imageUri, href, date, analyzedAt, importedAt, importedFrom)
    VALUES (:id, :remoteId, :text, :additionalInfo, NULL, :href, :date, NULL, now(), 'Twitter')"""
INSERT_QUERY_RESOURCE = """
    INSERT INTO InformationResource (id, remoteId, informationId, imageUri, videoUri, importedAt, importedFrom)
    VALUES (:id, :remoteId, :informationId, :imageUri, :videoUri, now(), 'Twitter')"""
SELECT_QUERY_INFORMATION = """
    SELECT id FROM Information WHERE remoteId = :remoteId AND importedFrom = 'Twitter'"""

USER_DICT = {
    120150508: "jay",
    394250799: "brammen",
    832560607: "sep",
    400567148: "chris",
    109850283: "peter",
}

console = Console()
app = Twitter("session")

# create cdn directory if not exists
if not os.path.exists("/app/cdn/twitter"):
    console.log("Creating /app/cdn/twitter directory...", style="bold green")
    os.makedirs("/app/cdn/twitter")

USERNAME = os.getenv("TWITTER_USERNAME")
PASSWORD = os.getenv("TWITTER_PASSWORD")
LIST_ID = os.getenv("TWITTER_LIST_ID")

if not USERNAME or not PASSWORD:
    raise Exception("No Twitter username or password provided")

if not LIST_ID:
    raise Exception("No Twitter list ID provided")

app.start(USERNAME, PASSWORD)


async def handle_tweet(tweet: Tweet, db):
    if tweet.author.id not in USER_DICT:
        console.log(
            f"Tweet author {tweet.author.id} not in user dict. skipping",
            style="bold red",
        )
        return

    if tweet.is_retweet:
        console.log(f"Tweet {tweet.id} is a retweet, skipping", style="bold red")
        return

    remote_id = f"{tweet.author.id}_{tweet.id}"
    media_db_id = uuid4()
    console.log(f"Processing tweet {remote_id}")

    if await db.fetch_one(SELECT_QUERY_INFORMATION, {"remoteId": str(remote_id)}):
        console.log(f"Tweet {remote_id} already in database", style="bold red")
        return

    console.log(f"Tweet {remote_id} not in database, inserting")

    await db.execute(
        INSERT_QUERY_INFORMATION,
        {
            "id": media_db_id,
            "remoteId": remote_id,
            "text": tweet.text,
            "additionalInfo": USER_DICT[tweet.author.id],
            "href": tweet.url,
            "date": tweet.created_on.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )

    if random.randint(0, 100) < 50:
        try:
            console.log(f"Liking tweet {remote_id}")
            app.like_tweet(tweet.id)
        except Exception as e:
            console.log(f"Error liking tweet: {e}", style="bold red")

    if tweet.media:
        for media in tweet.media:
            console.log(f"Downloading media {media.id} for tweet {remote_id}")
            time.sleep(random.randint(10, 30))

            thumbnail_url = media.media_url_https
            if thumbnail_url:
                console.log(f"Donwloading thumbnail for media {media.id}")
                try:
                    thumbnail = requests.get(thumbnail_url).content
                    filename = f"r_{uuid4()}.jpg"
                    with open(f"/app/cdn/twitter/{filename}", "wb") as f:
                        f.write(thumbnail)
                    thumbnail_url = f"/cdn/twitter/{filename}"
                except Exception as e:
                    console.log(f"Error downloading thumbnail: {e}", style="bold red")
                    continue

            video_url = None
            if media.type == "video":
                console.log(f"Media {media.id} is a video. Downloading...")
                try:
                    filename = f"r_{uuid4()}.mp4"
                    media.best_stream().download(f"/app/cdn/twitter/{filename}")
                    video_url = f"/cdn/twitter/{filename}"
                except Exception as e:
                    console.log(f"Error downloading video: {e}", style="bold red")
                    continue

            await db.execute(
                INSERT_QUERY_RESOURCE,
                {
                    "id": media.id,
                    "remoteId": f"{remote_id}_{media.id}",
                    "informationId": media_db_id,
                    "imageUri": thumbnail_url,
                    "videoUri": video_url,
                },
            )


async def twitter():
    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    console.log("Fetching last tweets of list...")

    contents = app.get_list_tweets(LIST_ID)
    for content in contents:
        if isinstance(content, Tweet):
            await handle_tweet(content, db)
        if isinstance(content, SelfThread):
            print("=== Detected a self thread")
            for t in content.tweets:
                if isinstance(t, Tweet):
                    await handle_tweet(t, db)
            print("=== End of self thread")
        if isinstance(content, ConversationThread):
            print("=== Detected a conversation thread")
            for t in content.threads:
                if isinstance(t, Tweet):
                    await handle_tweet(t, db)
            print("=== End of conversation thread")

    console.log("Done")


asyncio.run(twitter())
