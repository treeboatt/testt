from financial_assets import FinancialAsset


class EquityAsset(FinancialAsset):
    """Une action : actif financier avec un ticker et un dividende par action."""

    def __init__(self, name, price, ticker, dividend=0.0):
        super().__init__(name, price)
        self.ticker = ticker
        self.dividend = dividend

    def dividend_yield(self):
        """Rendement du dividende = dividende / prix."""
        if self.price == 0:
            return 0.0
        return self.dividend / self.price

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name}, {self.price}, "
                f"{self.ticker}, {self.dividend})")


if __name__ == "__main__":
    action = EquityAsset("Apple", 190.0, "AAPL", dividend=0.96)
    print(action)
    print(f"Rendement du dividende : {action.dividend_yield():.2%}")
