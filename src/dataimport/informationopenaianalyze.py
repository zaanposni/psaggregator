import json
import os
import asyncio
import base64
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from rich import print
from rich.console import Console
from databases import Database
from openai import OpenAI
from dateutil.parser import parse


if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set")
    exit(1)

console = Console()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INSERT_STATEMENT = """
    INSERT INTO ScheduledContentPiece (id, remoteId, title, description, additionalInfo, startDate, imageUri, href, secondaryHref, duration, importedAt, importedFrom, type)
    VALUES (:id, NULL, :title, :description, :additionalInfo, :startDate, NULL, 'https://twitch.tv/pietsmiet', NULL, NULL, now(), 'OpenAI', 'TwitchStream')"""


def openai_request(file_data) -> dict:
    console.log("Sending request to OpenAI...", style="bold green")
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": " ".join(
                            """
                        You are an assistant that generates JSON. You always return just the JSON with no additional description or context.
                        The following image might be a streaming plan of a content creator.
                        The JSON contains a list of streams. Each stream MUST have a start, title, game, additional_information. Use ISO 8601 format.
                        If the image is not a streaming plan, return an empty list of streams.
                        Keep in mind that all names, texts and times are in German. There can be multiple streams per day.
                    """.split()
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{file_data}",
                            "detail": "high",
                        },
                    },
                ],
            },
        ],
        max_tokens=2000,
    )

    console.log("Response:", style="bold green")
    console.log(response, style="bold green")

    sanitized_string = (
        response.choices[0]
        .message.content.replace("\n", "")
        .replace("```json", "")
        .replace("```", "")
    )
    data = json.loads(sanitized_string)
    console.log("Data:", style="bold green")
    console.log(data, style="bold green")
    return data


async def openai():
    console.log("Connecting to database...", style="bold green")
    db = Database(url=os.getenv("DATABASE_URL"))
    await db.connect()

    last_day = datetime.now() - timedelta(days=1)
    query = f"""
    SELECT * FROM Information
    WHERE analyzedAt IS NULL AND
          importedAt > '{last_day.strftime('%Y-%m-%d %H:%M:%S')}' AND
          imageUri IS NOT NULL AND
          importedFrom = 'YouTube'"""
    console.log("Fetching data...", style="bold green")

    rows = await db.fetch_all(query)
    console.log(f"Fetched {len(rows)} rows", style="bold green")

    for row in rows:
        try:
            console.log(f"Analyzing {row.id}", style="bold green")
            file_path = f"/app{row.imageUri}"
            with open(file_path, "rb") as image_file:
                file_data = base64.b64encode(image_file.read()).decode("utf-8")

            open_ai_res = openai_request(file_data)

            console.log(
                f"Analyzed {row.id} with {len(open_ai_res['streams'])} streams",
                style="bold green",
            )

            for stream in open_ai_res["streams"]:
                if any(x not in stream for x in ["start", "title", "game"]):
                    console.log(
                        f"Missing required fields in stream {stream}",
                        style="bold red",
                    )
                    continue

                start_date = parse(stream["start"])
                start_date = start_date.astimezone(timezone.utc)
                if start_date.year < datetime.now().year:
                    start_date = start_date.replace(year=datetime.now().year)

                query = "SELECT * FROM ScheduledContentPiece WHERE type = :type AND startDate = :startDate"
                values = {
                    "type": "TwitchStream",
                    "startDate": start_date.strftime("%Y-%m-%d %H:%M:%S"),
                }
                existing_stream = await db.fetch_one(query=query, values=values)
                if existing_stream:
                    console.log(
                        f"Stream {stream['title']} already exists, skipping",
                        style="bold red",
                    )
                    continue

                console.log(f"Inserting stream {stream['title']}", style="bold green")
                values = {
                    "id": str(uuid4()),
                    "title": stream["title"],
                    "description": stream["game"],
                    "additionalInfo": stream.get("additional_information"),
                    "startDate": start_date.strftime("%Y-%m-%d %H:%M:%S"),
                }
                await db.execute(query=INSERT_STATEMENT, values=values)
        finally:
            console.log(f"Setting analyzedAt for {row.id}", style="bold green")
            query = "UPDATE Information SET analyzedAt = NOW() WHERE id = :id"
            await db.execute(query=query, values={"id": row.id})

    await db.disconnect()
    console.log("Done")


asyncio.run(openai())
