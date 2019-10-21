class Deserializer:

    @classmethod
    def number_id(cls, identifier):
        return int(identifier)

    @classmethod
    def price(cls, price):
        return float(price)

    @classmethod
    def unix_time_int(cls, time):
        return int(float(time))
