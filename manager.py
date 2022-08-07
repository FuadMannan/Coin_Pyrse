from abc import ABC, abstractmethod
from portfolio import *
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
            print(f'{" " * len(str(i))}  Assets: {x.coin_list}\n')

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
        name = input('Enter Portfolio name: ')
        count = int(self.db_conn.get('portfolio:count'))
        for i in range(1, (count + 1)):
            portfolio_name = self.db_conn.hget(f'portfolio:{i}', 'portfolio_name')
            if portfolio_name == name:
                asset_list = self.db_conn.hget(f'portfolio:{i}', 'coin_list')
                print(f'\nName: {portfolio_name}')
                print(f'Assets: {asset_list}\n')
                print('What would you like to do?')
                choice = None
                while choice != '3':
                    print('\n1) Add coin')
                    print('2) Remove coin')
                    print('3) Exit\n')
                    choice = input('Selection: ')
                    if choice == '1':
                        coin_id = input('Enter Coin ID: ')
                        asset_list += f', {coin_id}'
                        self.db_conn.hset(f'portfolio:{i}', 'coin_list', asset_list)
                    elif choice == '2':
                        coin_id = input('Enter Coin ID: ')
                        asset_list_split = asset_list.split(', ')
                        asset_list_split.remove(coin_id)
                        asset_list = ", ".join(asset_list_split)
                        self.db_conn.hset(f'portfolio:{i}', 'coin_list', asset_list)


class QueryManager(Manager):

    def __init__(self, db_conn, coin_gecko):
        super().__init__(db_conn)
        self.coin_gecko = coin_gecko

    def select_filter(self, filter_list=[]):
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
            if choice == '1':
                search_filter = 'coin'
            elif choice == '2':
                search_filter = 'exchange'
                currencies = input('Enter comma separated list of currencies: ')
                search_filter += f'[{currencies}]'
            elif choice == '3':
                search_filter = 'market'
                currencies = input('Enter comma separated list of currencies: ')
                search_filter += f'[{currencies}]'
            elif choice == '4':
                search_filter = 'historical'
                start = input('Enter Start Date (YYYY-MM-DD): ')
                end = input('Enter End Date (YYYY-MM-DD): ')
                search_filter += f'[{start}, {end}]'
            elif choice == 5 and len(filter_list) == 0:
                print('Add at least one filter.')
            if len(search_filter) > 0:
                filter_list.append(search_filter)
        return filter_list

    def create(self):
        print('Create Search Query selected.\n')
        query_name = input('Enter Search Query name: ')
        filter_list = self.select_filter()
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
                        filter_list_split = self.select_filter(filter_list_split)
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


