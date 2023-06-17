from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class connection:
    def __init__(self, *args, **kwargs) -> None:
        self.Engine = create_engine(*args, **kwargs)
        self._sessionmaker = sessionmaker(bind=self.Engine)
        self.Session = self._sessionmaker()
