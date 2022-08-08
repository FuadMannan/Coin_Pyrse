from abc import ABC, abstractmethod
from app import *


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
        results = []
        for x in self.options['ids']:
            result = self.manager.get_coin_by_id(id=x,
                                                 community_data=self.options['community_data'],
                                                 developer_data=self.options['developer_data'],
                                                 localization_data=self.options['localization_data'])
            results.append(result)
        return results


class ExchangeRateFilter(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        self.manager.exchange()


class MarketFilter(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        self.manager.market()


class HistoricalFilter(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        self.manager.range()


class RunQuery(SearchCommand):
    def __init__(self, manager, options):
        super().__init__(manager, options)

    def execute(self):
        self.manager.run()


