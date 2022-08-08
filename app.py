from quickchart import QuickChart
from pycoingecko import CoinGeckoAPI
import configparser
import redis
from manager import *
from selectable import *


class App:
    __instance = None

    def setup(self):
        config = configparser.ConfigParser()
        config.read("config.cfg")
        self.dbconn = redis.Redis(
            username=config["Database"]["username"],
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["password"],
            decode_responses=True)
        self.coin_gecko = CoinGeckoAPI()

        # Creating the Portfolio and Query Manager classes
        portfolio_manager = PortfolioManager(self.dbconn)
        query_manager = QueryManager(self.dbconn, self.coin_gecko)

        # Creating Portfolio menu items
        create_portfolio = MenuItem('Create Portfolio', CreateCommand(portfolio_manager))
        list_portfolio = MenuItem('List Portfolio', ListCommand(portfolio_manager))
        update_portfolio = MenuItem('Update Portfolio', UpdateCommand(portfolio_manager))
        portfolio_menu_items = [create_portfolio, list_portfolio, update_portfolio]
        portfolio_menu = Menu('Portfolio Menu', portfolio_menu_items)

        # Creating Query menu items
        create_query = MenuItem('Create Search Query', CreateCommand(query_manager))
        list_query = MenuItem('List Search Query', ListCommand(query_manager))
        update_query = MenuItem('Update Search Query', UpdateCommand(query_manager))
        search_menu_items = [create_query, list_query, update_query]
        search_menu = Menu('Search Menu', search_menu_items)

        # Main menu items are Portfolio menu and Search menu
        main_menu_items = [portfolio_menu, search_menu]

        # Creating main menu
        main_menu = Menu('Main Menu', main_menu_items)

        self.main_menu = main_menu

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(App, cls).__new__(cls)
            cls.__instance.setup()
        return cls.__instance
