class Coin:
    def __init__(self, name, coin_id, symbol):
        self.name = name
        self.coin_id = coin_id
        self.symbol = symbol


class Portfolio:
    def __init__(self, name, coin_list=[]):
        self.name = name
        self.coin_list = coin_list

    def add_coin(self, coin):
        self.coin_list.append(coin)

    def remove_coin(self, coin_name):
        for x in self.coin_list:
            if x.name == coin_name:
                self.coin_list.remove(x)
