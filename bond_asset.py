class FinancialAsset:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.price})"


class Bond(FinancialAsset):
    def __init__(self, name, price, face_value, coupon_rate, maturity):
        super().__init__(name, price)        # reprend name et price de FinancialAsset
        self.face_value = face_value         # nominal, ex : 1000
        self.coupon_rate = coupon_rate       # ex : 0.05 pour 5 %
        self.maturity = maturity             # années avant échéance

    def coupon(self):
        return self.face_value * self.coupon_rate

    def theoretical_price(self, rate):
        """Valeur actuelle des coupons + du nominal, actualisés au taux `rate`."""
        pv_coupons = sum(self.coupon() / (1 + rate) ** t
                         for t in range(1, self.maturity + 1))
        pv_face = self.face_value / (1 + rate) ** self.maturity
        return pv_coupons + pv_face