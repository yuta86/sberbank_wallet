from datetime import datetime

from sqlalchemy import Integer, Column, String, Boolean, text, DateTime
from models import _base
from sqlalchemy.dialects.postgresql import NUMERIC

__all__ = ["Wallet"]


class Wallet(_base.Base):
    """ Таблица электронный кошелёк """

    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(100), default='12345', info={'verbose_name': 'UUID'})
    created = Column(DateTime, nullable=False, default=datetime.now(), info={'verbose_name': 'Время записи'})
    is_active = Column(Boolean, nullable=False, server_default=text('true'), info={'verbose_name': 'Активность'})
    balance = Column(NUMERIC(precision=2), nullable=False, info={'verbose_name': 'Баланс'})

    def __str__(self):
        return f'{self.id} - {self.uuid} - {self.created} - {self.is_active}'

    def __repr__(self):
        return f'{self.id} - {self.uuid} - {self.created} - {self.is_active}'
