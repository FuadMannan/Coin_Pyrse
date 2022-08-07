from abc import ABC, abstractmethod
from portfolio import *
import time
import datetime
from command import *
from app import *


class Manager(ABC):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def update(self):
        pass


class PortfolioManager(Manager):
    def __init__(self, db_conn):
        super().__init__(db_conn)
        portfolios = self.db_conn.json().get('portfolios', '.portfolio_list')
        if portfolios is None:
            self.__portfolio_list = []
            self.db_conn.json.set('portfolios', {'portfolio_list': []})
        else:
            self.__portfolio_list = portfolios

    def __list(self):
        print('Portfolios:')
        for i, x in enumerate(self.__portfolio_list):
            print(f'{i+1}) Name: {x.name}')
            print(f'{" " * len(str(i+1))}  Assets: {x.coin_list}\n')

    def create(self):
        print('Create Portfolio selected.\n')
        portfolio_name = input('Enter Portfolio name: ')
        add = input('\nAdd cryptocurrencies to portfolio? Y/N: ')
        coins = []
        if add == 'Y':
            print('Example Coin IDs: bitcoin, ethereum, dogecoin')
            coins = input('Enter comma separated list of Coin IDs: ')
            coins = [x.strip() for x in coins.split(',')]
        portfolio = Portfolio(portfolio_name, coins)
        result = self.db_conn.json().arrappend('portfolios', '.portfolio_list', vars(portfolio))
        if result is True:
            self.__portfolio_list.append(portfolio)
            self.db_conn.incr('portfolio:count')

    def list(self):
        print('List Portfolios selected.\n')
        self.__list()

    def update(self):
        print('Update Portfolio selected.\n')
        self.__list()
        portfolio_choice = input('Enter Selection: ')
        selected_portfolio = self.__portfolio_list[int(portfolio_choice)]
        print(f'\n  Name: {selected_portfolio.name}')
        print(f'Assets: {selected_portfolio.coin_list}\n')
        print('What would you like to do?')
        update_choice = None
        while update_choice != '3':
            print('\n1) Add coin')
            print('2) Remove coin')
            print('3) Exit\n')
            update_choice = input('Selection: ')
            if update_choice == '3':
                break
            coin_id = input('Enter Coin ID: ')
            if update_choice == '1':
                selected_portfolio.coin_list.append(coin_id)
            elif update_choice == '2':
                selected_portfolio.coin_list.remove(coin_id)
            self.db_conn.json.set('portfolios', f'$.portfolio_list[{int(portfolio_choice) - 1}]', selected_portfolio)


class QueryManager(Manager):

    def __init__(self, db_conn, coin_gecko):
        super().__init__(db_conn)
        self.coin_gecko = coin_gecko
        query_list = self.db_conn.json().get('search-queries', '.query_list')
        if query_list is None:
            self.__query_list = []
            self.db_conn.json.set('search-queries', {'query_list': []})
        else:
            self.__query_list = query_list

    def __get_vs_currency(self, options):
        currencies = input('Enter comma separated list of currencies: ')
        currencies = currencies.replace(' ', '')
        options['vs_currency'] = currencies

    def __get_unix_time(self, key):
        timestamp = input(f'Enter {key} Date (YYYY-MM-DD): ')
        time_values = [int(x) for x in timestamp.split('-')]
        date = datetime.datetime(time_values[0], time_values[1], time_values[2])
        unix = time.mktime(date.timetuple())
        return unix

    def __select_filter(self, filter_list=[]):
        choice = None
        while choice != '5':
            print('\nAdd a filter:')
            print('1) Coin Info')
            print('2) Exchange Rate')
            print('3) Market')
            print('4) Historical\n')
            print('5) Exit\n')
            choice = input('Selection: ')
            search_filter = ''
            options = {}
            if choice == '1':
                community_flag = input('Do you want community data? y/n: ')
                community_data = True if community_flag == 'y' else False
                developer_flag = input('Do you want developer data? y/n: ')
                developer_data = True if developer_flag == 'y' else False
                localization_flag = input('Do you want community data? y/n: ')
                localization_data = True if localization_flag == 'y' else False
                options['community_data'] = community_data
                options['developer_data'] = developer_data
                options['localization_data'] = localization_data
                search_filter = CoinFilter(self, options)
            elif choice == '2':
                self.__get_vs_currency(options)
                market_cap = input('Do you want market cap? y/n: ')
                include_market_cap = True if market_cap == 'y' else False
                daily_vol = input('Do you want 24-hour volume? y/n: ')
                include_24hr_vol = True if daily_vol == 'y' else False
                daily_change = input('Do you want community data? y/n: ')
                include_24hr_change = True if daily_change == 'y' else False
                options['include_market_cap'] = include_market_cap
                options['include_24hr_vol'] = include_24hr_vol
                options['include_24hr_change'] = include_24hr_change
                search_filter = ExchangeRateFilter(self, options)
            elif choice == '3':
                self.__get_vs_currency(options)
                search_filter = MarketFilter(self, options)
            elif choice == '4':
                self.__get_vs_currency(options)
                start = self.__get_unix_time('Start')
                end = self.__get_unix_time('End')
                options['from'] = start
                options['to'] = end
                search_filter = HistoricalFilter(self, options)
            elif choice == 5 and len(filter_list) == 0:
                print('Add at least one filter.')
            if len(search_filter) > 0:
                filter_list.append(search_filter)
        return filter_list

    def create(self):
        print('Create Search Query selected.\n')
        query_name = input('Enter Search Query name: ')
        filter_list = self.__select_filter()
        filter_list_string = ", ".join(filter_list)
        count = self.db_conn.get('query:count')
        if count is None:
            count = 1
        else:
            count = int(count) + 1
        self.db_conn.set('query:count', count)
        query_id = 'query:' + str(count)
        self.db_conn.hset(query_id, 'quuery_name', query_name)
        self.db_conn.hset(query_id, 'filter_list', filter_list_string)

    def list(self):
        print('List Search Queries selected.\n')
        print('Search Queries:')
        count = int(self.db_conn.get('query:count'))
        for i in range(1, (count+1)):
            query_name = self.db_conn.hget(f'query:{i}', 'query_name')
            filter_list = self.db_conn.hget(f'query:{i}', 'filter_list')
            print(f'Name: {query_name}')
            print(f'Filters: {filter_list}\n')

    def update(self):
        print('Update Search Query selected.\n')
        name = input('Enter Search Query name: ')
        count = int(self.db_conn.get('query:count'))
        for i in range(1, (count + 1)):
            query_name = self.db_conn.hget(f'query:{i}', 'query_name')
            if query_name == name:
                filter_list = self.db_conn.hget(f'query:{i}', 'filter_list')
                filter_list_split = filter_list.split(', ')
                print(f'\nName: {query_name}')
                print(f'Filters: {filter_list}\n')
                print('What would you like to do?')
                choice = None
                while choice != '3':
                    print('\n1) Add filter')
                    print('2) Remove filter')
                    print('3) Exit\n')
                    choice = input('Selection: ')
                    if choice == '1':
                        filter_list_split = self.__select_filter(filter_list_split)
                        filter_list = ", ".join(filter_list_split)
                        self.db_conn.hset(f'query:{i}', 'filter_list', filter_list)
                    elif choice == '2':
                        index = input('Enter Index of command to remove: ')
                        del filter_list_split[index]
                        filter_list = ", ".join(filter_list_split)
                        self.db_conn.hset(f'query:{i}', 'filter_list', filter_list)
                break

    def run(self):
        print('Run Search Query Selected.\n')
        query_name = input('Enter Search Query Name: ')
        print()
        portfolio_name = input('Enter Portfolio Name: ')
        print(f'\nExecuting {query_name} on {portfolio_name}...\n')
        count = int(self.db_conn.get('query:count'))
        for i in range(1, (count + 1)):
            name = self.db_conn.hget(f'query:{i}', 'query_name')
            if name == query_name:
                filter_list = self.db_conn.hget(f'query:{i}', 'filter_list')
                print(f'\nName: {query_name}')
                print(f'\nFilter List: {filter_list}\n')


