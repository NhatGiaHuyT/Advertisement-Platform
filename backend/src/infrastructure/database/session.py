from .interfaces import IUnitOfWork

class Session(ISession):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow
        self._identity_map