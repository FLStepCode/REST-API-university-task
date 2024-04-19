import os
import requests
import zulip
import config


def steam_response():

    steam_token = config.STEAM_TOKEN
    if steam_token is None:
        steam_token = os.getenv("STEAM_TOKEN")
    steam_id = config.STEAM_ID
    if steam_id is None:
        steam_id = os.getenv("STEAM_ID")

    summary_url = f"https://api.steampowered.com/ISteamUser/" \
                  f"GetPlayerSummaries/v0002/?key={steam_token}" \
                  f"&steamids={steam_id}"

    games_url = f"https://api.steampowered.com/IPlayerService/" \
                f"GetOwnedGames/v0001/?key={steam_token}" \
                f"&steamid={steam_id}&include_appinfo=true&format=json"

    with open("steam_summary.json", "w", encoding="utf-8") as f:
        f.write(requests.get(summary_url).text)

    with open("steam_games.json", "w", encoding="utf-8") as f:
        f.write(requests.get(games_url).text)


def zulip_response():

    zulip_email = config.ZULIP_EMAIL
    if zulip_email is None:
        zulip_email = os.getenv("ZULIP_EMAIL")

    zulip_key = config.ZULIP_KEY
    if zulip_key is None:
        zulip_key = os.getenv("ZULIP_KEY")

    zulip_site = config.ZULIP_SITE
    if zulip_site is None:
        zulip_site = os.getenv("ZULIP_SITE")

    client = zulip.Client(email=zulip_email,
                          api_key=zulip_key,
                          site=zulip_site)
    response = str(client.get_profile()).replace('\'', '\"'). \
        replace("True", "\"True\"").replace("False", "\"False\"")

    with open("zulip.json", "w", encoding="utf-8") as r:
        r.write(response)
