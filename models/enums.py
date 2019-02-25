from sqlalchemy.dialects.postgresql import ENUM

USER_TYPES = ENUM('Юридическое лицо', 'Физическое лицо', name='USER_TYPES', create_type=False)

EVENT_TYPES = ENUM('Пополнение', 'Вывод', 'Перевод', name='EVENT_TYPES', create_type=False)


