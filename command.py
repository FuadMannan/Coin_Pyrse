from abc import ABC, abstractmethod


class MenuCommand(ABC):
    def __init__(self, manager):
        self.manager = manager

    @abstractmethod
    def execute(self):
        pass


class CreateCommand(MenuCommand):
    def __init__(self, manager):
        super().__init__(manager)

    def execute(self):
        self.manager.create()


class ListCommand(MenuCommand):
    def __init__(self, manager):
        super().__init__(manager)

    def execute(self):
        self.manager.list()


class UpdateCommand(MenuCommand):
    def __init__(self, manager):
        super().__init__(manager)

    def execute(self):
        self.manager.update()


class SearchCommand(MenuCommand):
    def __init__(self, manager, options):
        super().__init__(manager)
        self.options = options

    @abstractmethod
    def execute(self):
        pass

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}({vars(self.options)})'


class CoinFilter(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        response = {'section': 'CoinFilter'}
        results = []
        for x in self.options['ids']:
            result = self.manager.get_coin_by_id(id=x,
                                                 community_data=self.options['community_data'],
                                                 developer_data=self.options['developer_data'],
                                                 localization_data=self.options['localization_data'])
            results.append(result)
        response['results'] = results
        return response


class ExchangeRateFilter(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        response = {'section': 'ExchangeRateFilter'}
        ids_string = ','.join(self.options['ids'])
        result = self.manager.get_price(ids=ids_string,
                                        vs_currencies=self.options['vs_currency'],
                                        include_market_cap=self.options['include_market_cap'],
                                        include_24hr_vol=self.options['include_24hr_vol'],
                                        include_24hr_change=self.options['include_24hr_change'])
        response['results'] = result
        return response


class MarketFilter(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        response = {'section': 'MarketFilter'}
        ids_string = ','.join(self.options['ids'])
        result = self.manager.get_coins_markets(ids=ids_string, vs_currency=self.options['vs_currency'])
        response['results'] = result
        return response


class HistoricalFilter(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        response = {'section': 'HistoricalFilter'}
        results = []
        for x in self.options['ids']:
            result = self.manager.get_coin_market_chart_range_by_id(id=x,
                                                                    vs_currency=self.options['vs_currency'],
                                                                    from_timestamp=self.options['from'],
                                                                    to_timestamp=self.options['to'])
            results.append(result)
        response['results'] = results
        return response


class RunQuery(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        self.manager.run()


