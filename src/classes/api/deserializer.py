from datetime import datetime

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

    @classmethod
    def formatted_time(cls, time):
        t = cls.unix_time_int(time)
        dt = datetime.fromtimestamp(t)
        return dt.strftime('%Y/%m/%d %H:%M:%S')

    @classmethod
    def unit_int(cls, unit):
        return int(float(unit))

    @classmethod
    def unit_float(cls, unit):
        return float(unit)
