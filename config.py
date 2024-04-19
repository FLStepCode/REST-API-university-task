from dotenv.main import dotenv_values

STEAM_TOKEN = dotenv_values(".env").get('STEAM_TOKEN')
STEAM_ID = dotenv_values(".env").get('STEAM_ID')
ZULIP_EMAIL = dotenv_values(".env").get('ZULIP_EMAIL')
ZULIP_KEY = dotenv_values(".env").get('ZULIP_KEY')
ZULIP_SITE = dotenv_values(".env").get('ZULIP_SITE')
