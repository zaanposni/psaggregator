[![PietSmiet Aggregator][repo_logo_img]][repo_url]

# PietSmiet Aggregator

[![Website][repo_website_img]][website_url]
[![License][repo_license_img]][repo_license_url]

PietSmiet Aggregator is a selfhostable web application that aggregates all the videos, streams and additional content from PietSmiet and displays them in a nice overview.

⭐ **Dashboard** - Display all PietSmiet videos and streams in a nice overview.\
⭐ **API** - Free and Public JSON HTTP API.\
⭐ **PietSmietDE Import** - Import all videos and news from the PietSmiet website.\
⭐ **YouTube Import** - Import all community posts from the PietSmiet YouTube channel.\
⭐ **Reddit Import** - Import trending posts from r/pietsmiet.\
⭐ **Instagram Import** - Import all posts.\
⭐ **Streamingplan** - Analyze the Streamingplan with OpenAI Vision and import scheduled streams.\
⭐ **Full Control** - Selfhostable, Open Source and Dockerized.

## ⚡️ Quick Start Self Deployment

First, [download][docker_download_url] and install **Docker**.

Create a `.env` file in the root directory of the project. You can use the `.env.example` file as a template.
If you do not want to use certain features (for example the OpenAI Streamingplan Analysis), you can skip the corresponding API keys.

A `docker-compose.yml` file is provided to run the application. It will start the application and a MySQL database.

```bash
docker-compose up -d
```

👀 You can view the application at `http://localhost:5650`.

You can view the docker logs with `docker-compose logs -f`.

Keep in mind that some data imports might take a while. You can view the progress of the data imports in the docker logs.\
Most data imports are executed periodically. Wait at least an hour before you start to worry about missing data.

That's all you need to know to start! 🎉

## 📝 Development

Feel free to contribute to this project. Please read the [contribution guidelines](CONTRIBUTING.md) before submitting a pull request.

### 💡 Overview

This project has four main components:

- **Frontend**: The frontend is a [SvelteKit][svelte_kit_url] application. It is located in the `src/psaggregator` directory.
- **Dataimporter**: The dataimporter is a small project containing multiple python scripts. These scripts are used to import data from the PietSmiet website and various other APIs. The scripts are located in the `src/dataimporter` directory.
- **NGINX**: NGINX is used as a reverse proxy for the frontend. The configuration is located in the `src/nginx` directory.
- **Database**: The database is a MySQL database. The schema and data are located in the frontend project
- **YouTubeOperationalAPI**: The YouTubeOperationalAPI is a Open Source Solution by [Benjamin Loison][benjamin_loison_url]. It supports more features than the official public YouTube API.

### 📦 Requirements

Depending on the component you want to work on, you will need the following tools:

- **Docker**: Docker `>= 24.0.0` and docker-compose `>= 2.23.0`.
- **Frontend**: Node.js `>= 20.0.0` and npm `>= 9.6.0`.
- **Dataimporter**: Python `>= 3.10.0`.

### 🚀 Getting Started

First, clone the repository:

```bash
git clone https://github.com/zaanposni/psaggregator.git
```

Then, create a `.env` file in the root directory of the project. You can use the `.env.example` file as a template.
If you do not want to use certain features (for example the OpenAI Streamingplan Analysis), you can skip the corresponding API keys.

Start the MySQL database and YouTubeOperationalAPI:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

Setup the frontend

```bash
cd src/psaggregator
npm install
npm run prismagenerate
npm run prismamigrate  # might be needed if the database is not initialized yet
npm run dev
```

Setup the dataimporter by setting up the environment variables like in the `.env.example` file.\
The dataimporter uses numerous APIs to import data.\
You might want to create API keys for the APIs you want to use and skip the ones you don't want to use.

Start the dataimport scripts (the process is the same for all kind of imports)

```bash
cd src/dataimporter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 pietsmietdeuploadplan.py  # uploadplan does not need any API key. However - for example - reddit.py does
```

## ⭐️ Project assistance

If you want to say **thank you** or/and support active development of `psaggregator`:

- Add a [GitHub Star][repo_url] to the project.
- Support me on [Ko-fi][kofi_url].

## 🏆 A win-win cooperation

And now, I invite you to participate in this project! Let's work **together** to
create the **most useful** tool for all PietSmiet Enjoyers.

- [Issues][repo_issues_url]: ask questions and submit your features.
- [Pull requests][repo_pull_request_url]: send your improvements to the current.
- [Mail][mail_url]: send your ideas for the project.
- [Discord][discord_url]: add me as a friend on Discord: @zaanposni

Together, we can make this project **better** every day!

## 🔥 Other projects of the authors

- [discord-masz][discord_masz_url] - MASZ is a selfhostable highly sophisticated moderation bot for Discord. Includes a web dashboard and a discord bot.

## ⚠️ License

[`psaggregator`][repo_url] is free and open-source software licensed under
the [GPL-3.0 License][repo_license_url].

<!-- Website -->

[website_url]: https://pietsmiet.zaanposni.com
[repo_website_img]: https://img.shields.io/badge/Website-Online-blue?style=for-the-badge&logo=none

<!-- Repository -->

[repo_url]: https://github.com/zaanposni/psaggregator
[repo_issues_url]: https://github.com/zaanposni/psaggregaor/issues
[repo_pull_request_url]: https://github.com/zaanposni/psaggregaor/pulls
[repo_logo_img]: https://raw.githubusercontent.com/zaanposni/psaggregator/master/logo.png
[repo_license_url]: https://github.com/zaanposni/psaggregator/blob/master/LICENSE
[repo_license_img]: https://img.shields.io/badge/license-GPL%203.0-red?style=for-the-badge&logo=none

[docker_download_url]: https://docs.docker.com/get-docker/
[svelte_kit_url]: https://kit.svelte.dev/
[benjamin_loison_url]: https://github.com/Benjamin-Loison

<!-- Author -->

[kofi_url]: https://ko-fi.com/zaanposni
[discord_masz_url]: https://github.com/zaanposni/discord-masz
[mail_url]: mailto:psaggregator@zaanposni.com
[discord_url]: https://discord.com
