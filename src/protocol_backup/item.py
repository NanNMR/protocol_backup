_FIELDS = 'id', 'title'


class Item:

    def __init__(self, data: dict):
        self.id = data['id']  # redundant for PyCharm
        self.title = data['title']  # redundant for PyCharm
        for f in _FIELDS:
            setattr(self, f, data[f])

    def __str__(self):
        return self.title

    @staticmethod
    def fields() -> str:
        """Return expected fields comma separated"""
        return ','.join(_FIELDS)
