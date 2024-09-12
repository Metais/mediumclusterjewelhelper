

class Report:
    def __init__(self, pair, prices, total, divine_price):
        self.pair = pair

        # Convert chaos and divine sales
        chaos_prices = [self.get_price_in_chaos(price, divine_price) for price in prices]
        # Remove sales with unknown currencies
        self.prices = [x for x in chaos_prices if x != 0]

        self.total_items = total
        if self.total_items > 0:
            self.cheapest_price = self.prices[0]
            self.average_price = round(sum(self.prices) / len(self.prices), 1)
        else:
            self.cheapest_price = 0
            self.average_price = 0

    @staticmethod
    def get_price_in_chaos(price, divine_price):
        if price["currency"] == "chaos":
            return price["amount"]
        elif price["currency"] == "divine":
            return divine_price * price["amount"]
        else:
            return 0

    def __str__(self):
        return f"({self.pair[0]}, {self.pair[1]})"
