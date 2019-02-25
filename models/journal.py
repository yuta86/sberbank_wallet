from datetime import datetime

from sqlalchemy import DateTime, Column, ForeignKey, Integer
from .enums import EVENT_TYPES
from models import _base

__all__ = ["Journal"]


class Journal(_base.Base):
    """ Таблица : Журнал """

    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.now(), info={'verbose_name': 'Время записи'})
    from_wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=True, info={'verbose_name': 'От кого'})
    to_wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=True, info={'verbose_name': 'Кому '})
    type_operation = Column(EVENT_TYPES, default='Перевод', info={'verbose_name': 'Тип события'})

    def __str__(self):
        return f'{self.created} - {self.type_operation} - {self.from_wallet_id} -  {self.from_wallet_id}'

    def __repr__(self):
        return f'{self.created} - {self.type_operation} - {self.from_wallet_id} -  {self.from_wallet_id}'
