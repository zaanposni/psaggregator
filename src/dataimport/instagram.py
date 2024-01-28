import asyncio
import os
import requests
import time
import random
from databases import Database
from uuid import uuid4

from rich.console import Console
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import pyotp


console = Console()

# create cdn directory if not exists
if not os.path.exists("/app/cdn/instagram"):
    console.log("Creating /app/cdn/instagram directory...", style="bold green")
    os.makedirs("/app/cdn/instagram")

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
KEY_2FA = os.getenv("INSTAGRAM_2FA_SECRET")
CONFIG_PATH = os.getenv("INSTAGRAM_CONFIG_PATH")
if not CONFIG_PATH:
    CONFIG_PATH = "session.json"
console.log(f"Using config path {CONFIG_PATH}")

if not USERNAME or not PASSWORD:
    raise Exception("No Instagram username or password provided")


def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    console.log("Attempting to login user...")
    if not os.path.exists(CONFIG_PATH):
        console.log("No session file found, creating empty session file")
        with open(CONFIG_PATH, "w") as f:
            f.write("{}")

    cl = Client()
    session = cl.load_settings(CONFIG_PATH)

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)

            code_2fa = ""
            if KEY_2FA:
                code_2fa = pyotp.TOTP(KEY_2FA.replace(" ", "")).now()
            cl.login(USERNAME, PASSWORD, verification_code=code_2fa)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                console.log(
                    "Session is invalid, need to login via username and password"
                )

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                code_2fa = ""
                if KEY_2FA:
                    code_2fa = pyotp.TOTP(KEY_2FA.replace(" ", "")).now()
                cl.login(USERNAME, PASSWORD, verification_code=code_2fa)
            login_via_session = True
        except Exception as e:
            console.log("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            console.log(
                "Attempting to login via username and password. username: %s" % USERNAME
            )

            code_2fa = ""
            if KEY_2FA:
                code_2fa = pyotp.TOTP(KEY_2FA.replace(" ", "")).now()

            if cl.login(USERNAME, PASSWORD, verification_code=code_2fa):
                login_via_pw = True
        except Exception as e:
            console.log("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    cl.dump_settings(CONFIG_PATH)
    return cl


cl = login_user()
console.log("Successfully logged in user")

time.sleep(random.randint(10, 30))

user_dict = {
    "peter": 344058897,
    "brammen": 1588473759,
    "jay": 2030403724,
    "sep": 1609561808,
    "chris": 1057433625,
}

console.log("Fetching last 50 media items for each user")

INSERT_QUERY_INFORMATION = """
    INSERT INTO Information (id, remoteId, text, additionalInfo, imageUri, href, date, analyzedAt, importedAt, importedFrom)
    VALUES (:id, :remoteId, :text, :additionalInfo, :imageUri, :href, :date, NULL, now(), 'Instagram')"""
INSERT_QUERY_RESOURCE = """
    INSERT INTO InformationResource (id, remoteId, informationId, imageUri, videoUri, importedAt, importedFrom)
    VALUES (:id, :remoteId, :informationId, :imageUri, :videoUri, now(), 'Instagram')"""
SELECT_QUERY_INFORMATION = """
    SELECT id FROM Information WHERE remoteId = :remoteId AND importedFrom = 'Instagram'"""


async def instagram():
    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()
    for user, user_id in user_dict.items():
        console.log(f"Fetching last 3 media items for {user}")
        last_media = cl.user_medias(user_id, amount=3)
        time.sleep(random.randint(10, 30))
        console.log(f"Found {len(last_media)} media items for {user}")
        for media in last_media:
            remote_id = f"{user}_{str(media.id)}"
            media_db_id = uuid4()
            console.log(f"Processing media item {remote_id}")
            if await db.fetch_one(
                SELECT_QUERY_INFORMATION, {"remoteId": str(remote_id)}
            ):
                console.log(
                    f"Media item {remote_id} already in database", style="bold red"
                )
                continue
            console.log(f"Media item {remote_id} not in database, inserting")

            thumbnail_url = media.thumbnail_url
            if not thumbnail_url:
                for resource in media.resources:
                    if resource.thumbnail_url:
                        thumbnail_url = resource.thumbnail_url
                        break

            if not thumbnail_url:
                console.log(
                    f"Media item {remote_id} has no thumbnail, skipping",
                    style="bold red",
                )
                continue

            console.log(f"Downloading thumbnail for {remote_id}")
            try:
                thumbnail = requests.get(thumbnail_url).content
                filename = f"{uuid4()}.jpg"
                with open(f"/app/cdn/instagram/{filename}", "wb") as f:
                    f.write(thumbnail)
                thumbnail_url = f"/cdn/instagram/{filename}"
            except Exception as e:
                console.log(f"Error downloading thumbnail: {e}", style="bold red")
                continue

            await db.execute(
                INSERT_QUERY_INFORMATION,
                {
                    "id": media_db_id,
                    "remoteId": remote_id,
                    "text": media.caption_text,
                    "additionalInfo": user,
                    "imageUri": thumbnail_url,
                    "href": f"https://www.instagram.com/p/{media.code}",
                    "date": media.taken_at.strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            for resource in media.resources:
                time.sleep(random.randint(10, 30))
                thumbnail_url = resource.thumbnail_url
                if thumbnail_url:
                    console.log(f"Downloading thumbnail for resource {resource.pk}")
                    try:
                        thumbnail = requests.get(thumbnail_url).content
                        filename = f"r_{uuid4()}.jpg"
                        with open(f"/app/cdn/instagram/{filename}", "wb") as f:
                            f.write(thumbnail)
                        thumbnail_url = f"/cdn/instagram/{filename}"
                    except Exception as e:
                        console.log(
                            f"Error downloading thumbnail: {e}", style="bold red"
                        )
                        continue

                await db.execute(
                    INSERT_QUERY_RESOURCE,
                    {
                        "id": uuid4(),
                        "remoteId": str(resource.pk),
                        "informationId": media_db_id,
                        "imageUri": thumbnail_url,
                        "videoUri": resource.video_url,
                    },
                )


asyncio.run(instagram())
