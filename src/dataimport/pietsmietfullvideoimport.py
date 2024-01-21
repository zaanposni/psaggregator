# This file is not actively used in psaggregator.
# It is a script that was used to import all videos from PietSmiet once.
# Other imports only import recent videos.
# This script generates a sql file that can be used to import all videos.

import requests
from uuid import uuid4

import dateutil.parser


# Get these tokens by logging in to pietsmiet.de and inspecting the network requests
psde_auth3 = ""
xsrf_token = ""
authorization = ""
x_origin_integrity = ""

batch_size = 500
page = 0
endpoint = "https://www.pietsmiet.de/api/v1/videos?limit={}&page={}&order=latest"

INSERT_STATEMENT = """
    INSERT INTO ContentPiece (id  , remoteId, title, description, additionalInfo, startDate, imageUri, href, duration, importedAt, importedFrom , type) VALUES
                             ('{}', '{}'    , '{}' , NULL       , NULL          , {}       , {}      , '{}', {}      , now()     , 'PietSmietDE', 'PSVideo');"""

# remove all unnecessary newlines and whitespace
INSERT_STATEMENT = " ".join(INSERT_STATEMENT.split())

videos = []
# In January 2024 this took 71 iterations
while True:
    page += 1
    url = endpoint.format(batch_size, page)
    print("Fetching page {}".format(page))
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "XSRF-TOKEN": xsrf_token,
            "x-origin-integrity": x_origin_integrity,
        },
        cookies={"psde_auth3": psde_auth3, "XSRF-TOKEN": xsrf_token},
    )
    if response.status_code != 200:
        print("Error fetching page {}: {}".format(page, response.status_code))
        break
    data = response.json()

    videos.extend(data["data"])

    if len(data["data"]) < batch_size:
        print("No more videos found")
        break

print("Found {} videos".format(len(videos)))
print("Generating queries")

queries = []
for video in videos:
    publish_date = "NULL"
    imageUri = "NULL"
    if video.get("publish_date"):
        publish_date = f"'{dateutil.parser.parse(video['publish_date']).strftime('%Y-%m-%d %H:%M:%S')}'"
    if video.get("thumbnail"):
        try:
            imageUri = f"'{video['thumbnail']['variations'][0]['url']}'"
        except KeyError:
            pass
        except IndexError:
            pass
    queries.append(
        INSERT_STATEMENT.format(
            uuid4(),
            video["id"],
            video["title"].replace("'", "\\'"),
            publish_date,
            imageUri,
            video["short_url"],
            video["duration"],
        )
    )


print("Writing queries to videos.sql")
with open("videos.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(queries))

print("Done")
