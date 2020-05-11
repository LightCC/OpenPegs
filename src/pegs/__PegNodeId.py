class PegNodeId:

    def __init__(self, node_id: int, id_str: str = None):
        self.value = node_id
        if id_str is None:
            self._id_str = str(node_id)
        else:
            if not isinstance(id_str, str):
                raise ValueError('id_str must be a string, it was {}'.format(type(id_str)))
            self._id_str = id_str

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, PegNodeId):
            return self.value == other.value
        else:
            return NotImplemented

    def __str__(self):
        return self._id_str
