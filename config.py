class Config(object):
    """Базовые конфигурации приложения"""
    ALEMBIC_DB_URL = 'postgresql+psycopg2://postgres:olzeMyparol90@127.0.0.1:7433/wallet'
    DB_URL = 'postgresql+psycopg2://postgres:olzeMyparol90@127.0.0.1:7433/wallet'

    USER_TYPES = {'individual': 'Физическое лицо', 'organization': 'Юридическое лицо'}

    START_BALANCE = 10.00  # начальный баланс
    LIMIT = 100.00  # огаанччение в средствах

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    pass


class ProductionConfig(Config):
    """Конфигурация для production"""
    pass


# Рабочая конфигурация
current_config = DevelopmentConfig
