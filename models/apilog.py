from datetime import datetime

from sqlalchemy import DateTime, Column, Integer, String
from models import _base

__all__ = ["ApiLog"]


class ApiLog(_base.Base):
    """ Таблица : Логи """

    __tablename__ = 'apilog'

    id = Column(Integer, primary_key=True)
    request_url = Column(String(512), nullable=False, info={'verbose_name': 'URL'})
    request_method = Column(String(512), nullable=False, info={'verbose_name': 'Метод'})
    request_data = Column(String(512), nullable=False, info={'verbose_name': 'Данные'})
    remote = Column(String(512), nullable=False, info={'verbose_name': 'Адрес клиента'})
    result = Column(String(10000), nullable=False, info={'verbose_name': 'Результат'})
    created = Column(DateTime, nullable=False, default=datetime.now(), info={'verbose_name': 'Время создания'})
    finished = Column(DateTime, nullable=False, default=datetime.now(), info={'verbose_name': 'Время окончания'})

    def __str__(self):
        return f'{self.created} - {self.request_url} - {self.request_method} - {self.request_data} - {self.result}'

    def __repr__(self):
        return f'{self.created} - {self.request_url} - {self.request_method} - {self.request_data} - {self.result}'
