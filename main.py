"""
HW by Talibov Serhan from group BIV221
"""
import json
import time
from jinja2 import Template
import responses


def get_from_key(dictionary, key):
    """
    This function safely extracts data by the key\n
    dictionary: dictionary you want to parse\n
    key: key you want to extract data with
    """
    try:
        data = dictionary[key]
    except KeyError:
        data = "N/A"
    return data


def get_steam_image(link_hash, game_id):
    """
    This function returns steam game image by game ID and by image's link hash:
    """
    link = f"http://media.steampowered.com/steamcommunity/" \
           f"public/images/apps/{game_id}/{link_hash}.jpg"
    return link


if __name__ == "__main__":
    responses.steam_response()
    responses.zulip_response()

    CURRENT_TIME = f"This site was generated at: {time.ctime()}"

    with open("steam_summary.json", "r", encoding="utf-8") as f:
        STEAM_SUMMARY = json.loads(f.readline())

    with open("steam_games.json", "r", encoding="utf-8") as f:
        STEAM_GAMES = json.loads(f.readline())

    with open("zulip.json", "r", encoding="utf-8") as f:
        ZULIP_JSON = json.loads(f.readline())

    with open("template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    STEAM_SUMMARY = STEAM_SUMMARY['response']['players'][0]
    STEAM_GAMES = STEAM_GAMES['response']['games']

    # steam summary
    STEAM_AVATAR = get_from_key(STEAM_SUMMARY, 'avatarfull')
    STEAM_NAME = get_from_key(STEAM_SUMMARY, 'personaname')
    STEAM_ARRAY = ["Offline",
                   "Online",
                   "Busy",
                   "Away",
                   "Snooze",
                   "Looking to trade",
                   "Looking to play"]
    STEAM_STATUS = STEAM_ARRAY[get_from_key(STEAM_SUMMARY, 'personastate')]
    VISIBILITY_ARRAY = ["", "Not public", "", "Public"]
    VISIBILITY = VISIBILITY_ARRAY[get_from_key(STEAM_SUMMARY,
                                               'communityvisibilitystate')]

    # steam games
    GAMES_ARRAY = []
    for k in STEAM_GAMES:
        GAMES_ARRAY.append([k['name'], get_steam_image(k['img_icon_url'],
                                                       k['appid'])])

    # zulip
    ZULIP_AVATAR = f"https://chat.miem.hse.ru" \
                   f"{get_from_key(ZULIP_JSON, 'avatar_url')}"
    ZULIP_ID = get_from_key(ZULIP_JSON, 'user_id')
    ZULIP_NAME = get_from_key(ZULIP_JSON, 'full_name')
    ZULIP_EMAIL = get_from_key(ZULIP_JSON, 'email')
    ZULIP_ROLES = [
        "Organization owner",
        "Organization administrator",
        "Organization moderator",
        "Member",
        "Member",
        "Guest",
        "Guest"
    ]
    ZULIP_STATUS = [
        f"Is active? {get_from_key(ZULIP_JSON, 'is_active')}",
        f"Is an admin? {get_from_key(ZULIP_JSON, 'is_admin')}",
        f"Is an owner? {get_from_key(ZULIP_JSON, 'is_owner')}",
        f"Is a guest? {get_from_key(ZULIP_JSON, 'is_guest')}",
        f"Is a billing admin? "
        f"{get_from_key(ZULIP_JSON, 'is_billing_admin')}",
        f"Is a bot? {get_from_key(ZULIP_JSON, 'is_bot')}"
    ]
    ZULIP_INFO = [ZULIP_JSON['profile_data'][k]['value']
                  for k in ZULIP_JSON['profile_data'].keys()]

    rendered_page = template.render(
        steam_avatar=STEAM_AVATAR,
        steam_name=STEAM_NAME,
        steam_status=STEAM_STATUS,
        steam_profile_status=VISIBILITY,
        steam_games=GAMES_ARRAY,

        zul_avatar=ZULIP_AVATAR,
        zul_id=ZULIP_ID,
        zul_name=ZULIP_NAME,
        zul_email=ZULIP_EMAIL,
        zul_role=ZULIP_ROLES[ZULIP_JSON['role'] // 100 - 1],
        zul_status=ZULIP_STATUS,
        zul_info=ZULIP_INFO,

        time=CURRENT_TIME
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_page)
