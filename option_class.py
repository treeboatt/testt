import math
import os
import sys

# Les classes existantes sont dans le dossier "testt" : on l'ajoute au chemin d'import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "testt"))

from financial_assets import FinancialAsset
from equity_asset import EquityAsset


def _norm_cdf(x):
    """Fonction de répartition de la loi normale centrée réduite."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


class Option(FinancialAsset):
    """Option européenne (call ou put) sur une action (EquityAsset)."""

    def __init__(self, name, price, underlying, strike, maturity, option_type="call"):
        super().__init__(name, price)          # prime de marché de l'option
        if not isinstance(underlying, EquityAsset):
            raise TypeError("Le sous-jacent doit être une EquityAsset")
        option_type = option_type.lower()
        if option_type not in ("call", "put"):
            raise ValueError("option_type doit être 'call' ou 'put'")
        self.underlying = underlying           # l'action sous-jacente
        self.strike = strike                   # prix d'exercice K
        self.maturity = maturity               # maturité en années, ex : 0.5
        self.option_type = option_type

    def payoff(self, spot=None):
        """Gain à l'échéance pour un prix du sous-jacent donné (par défaut le prix actuel)."""
        s = self.underlying.price if spot is None else spot
        if self.option_type == "call":
            return max(s - self.strike, 0.0)
        return max(self.strike - s, 0.0)

    def intrinsic_value(self):
        """Valeur intrinsèque = payoff si on exerçait maintenant."""
        return self.payoff()

    def time_value(self):
        """Valeur temps = prime - valeur intrinsèque."""
        return self.price - self.intrinsic_value()

    def is_in_the_money(self):
        return self.intrinsic_value() > 0

    def _d1_d2(self, rate, volatility):
        s, k, t = self.underlying.price, self.strike, self.maturity
        q = self.underlying.dividend_yield()   # rendement du dividende de l'action
        d1 = (math.log(s / k) + (rate - q + 0.5 * volatility ** 2) * t) / (volatility * math.sqrt(t))
        d2 = d1 - volatility * math.sqrt(t)
        return d1, d2, q

    def black_scholes_price(self, rate, volatility):
        """Prix théorique Black-Scholes (avec rendement de dividende continu)."""
        s, k, t = self.underlying.price, self.strike, self.maturity
        d1, d2, q = self._d1_d2(rate, volatility)
        if self.option_type == "call":
            return s * math.exp(-q * t) * _norm_cdf(d1) - k * math.exp(-rate * t) * _norm_cdf(d2)
        return k * math.exp(-rate * t) * _norm_cdf(-d2) - s * math.exp(-q * t) * _norm_cdf(-d1)

    def delta(self, rate, volatility):
        """Sensibilité du prix de l'option au prix du sous-jacent."""
        d1, _, q = self._d1_d2(rate, volatility)
        if self.option_type == "call":
            return math.exp(-q * self.maturity) * _norm_cdf(d1)
        return math.exp(-q * self.maturity) * (_norm_cdf(d1) - 1)

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name}, {self.price}, "
                f"{self.underlying.ticker}, K={self.strike}, T={self.maturity}, "
                f"{self.option_type})")


if __name__ == "__main__":
    apple = EquityAsset("Apple", 190.0, "AAPL", dividend=0.96)
    call = Option("Call Apple 200", 8.5, apple, strike=200, maturity=0.5, option_type="call")
    put = Option("Put Apple 200", 15.0, apple, strike=200, maturity=0.5, option_type="put")

    for opt in (call, put):
        print(opt)
        print(f"  Valeur intrinsèque : {opt.intrinsic_value():.2f}")
        print(f"  Valeur temps       : {opt.time_value():.2f}")
        print(f"  Dans la monnaie ?  : {opt.is_in_the_money()}")
        print(f"  Prix Black-Scholes : {opt.black_scholes_price(rate=0.04, volatility=0.25):.2f}")
        print(f"  Delta              : {opt.delta(rate=0.04, volatility=0.25):.3f}")
