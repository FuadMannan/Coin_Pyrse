from quickchart import QuickChart
from pycoingecko import CoinGeckoAPI
import configparser
import redis


class App:
    __instance = None

    def setup(self):
        config = configparser.ConfigParser()
        config.read("config.cfg")
        self.dbconn = redis.Redis(
            username="test",
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["password"],
            decode_responses=True)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(App, cls).__new__(cls)
            cls.__instance.setup()
        return cls.__instance
