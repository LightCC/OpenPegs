class PegNodeException(Exception):
    pass


class PegAlreadyPresent(PegNodeException, ValueError):
    pass


class PegNotAvailable(PegNodeException, ValueError):
    pass
