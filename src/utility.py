class Util:
    @staticmethod
    def interpolate(t, list_one, list_two):
        zipped = zip(list_one, list_two)

        for a, b in zipped:
            yield int(a + t * (b - a))