class Serializer:

    @classmethod
    def number_id(cls, identifier):
        return str(identifier)

    @classmethod
    def unit(cls, unit):
        return "{:.1f}".format(float(unit))
