import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

BOT_TOKEN = config["Bot"]["bot_token"]
DB_HOST = config["Bot"]["DB_HOST"]
DB_NAME = config["Bot"]["DB_NAME"]
DB_USER = config["Bot"]["DB_USER"]
DB_PASS = config["Bot"]["DB_PASS"]
