
taken_positions = set()


class EntityPlaceholder:
    def __init__(self, id, *args):
        self.id = id
        self.args = args