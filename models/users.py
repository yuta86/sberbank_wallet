from sqlalchemy import Integer, Column, String, ForeignKey

from .enums import USER_TYPES
from models import _base
from sqlalchemy.orm import relationship

__all__ = ["Users"]


class Users(_base.Base):
    """ Таблица пользователь """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(512), nullable=False, info={'verbose_name': 'Имя'})
    last_name = Column(String(512), nullable=False, info={'verbose_name': 'Фамилия'})
    fathers_name = Column(String(512), nullable=False, info={'verbose_name': 'Отчество'})

    birthday = Column(String(512), nullable=False, info={'verbose_name': 'Дата рождения'})

    email = Column(String(512), nullable=False, info={'verbose_name': 'Эл. почта'})
    phone = Column(String(512), nullable=True, info={'verbose_name': 'Телефон'})
    type_account = Column(USER_TYPES, default='Физическое лицо', info={'verbose_name': 'Тип пользователя'})

    wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=True, info={'verbose_name': 'Идентификатор кошелька '})

    wallet = relationship("Wallet", backref="users")

    def __str__(self):
        return f'{self.id} - {self.name} - {self.fathers_name}'

    def __repr__(self):
        return f'{self.id} - {self.name} - {self.fathers_name}'
