from datetime import datetime

from sqlalchemy import DateTime, Column, Integer, String
from models import _base

__all__ = ["ErrorLog"]


class ErrorLog(_base.Base):
    """ Таблица : Логи ошибок """

    __tablename__ = 'errorlog'

    id = Column(Integer, primary_key=True)
    request_url = Column(String(512), nullable=False, info={'verbose_name': 'URL'})
    request_method = Column(String(512), nullable=False, info={'verbose_name': 'Метод'})
    request_data = Column(String(512), nullable=False, info={'verbose_name': 'Данные'})
    error = Column(String(512), nullable=False, info={'verbose_name': 'Ошибка'})
    traceback = Column(String(10000), nullable=False, info={'verbose_name': 'Подробности'})
    created = Column(DateTime, nullable=False, default=datetime.now(), info={'verbose_name': 'Время создания'})

    def __str__(self):
        return f'{self.created} - {self.request_url} - {self.request_method} - {self.request_data} - {self.error}'

    def __repr__(self):
        return f'{self.created} - {self.request_url} - {self.request_method} - {self.request_data} - {self.error}'

#  traceback.format_exc() модуль traceback