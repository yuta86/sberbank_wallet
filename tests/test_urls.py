import aiohttp

TEST_SERVER_URL = 'http://0.0.0.0:8080'

MAIN_URL_1 = f'{TEST_SERVER_URL}'  # стартовая страница
MAIN_URL_2 = f'{TEST_SERVER_URL}/Yurii'

USER_INFO_URL = f'{TEST_SERVER_URL}/user/info/1'  # получение информации о пользователе

LOGS_API_LOGS_URL = f'{TEST_SERVER_URL}/logs/apilogs'  # просмотр логов
LOGS_ERROR_LOGS_URL = f'{TEST_SERVER_URL}/logs/errorlogs'  # просмотр ошибочных логов

WALLET_BALANCE_URL = f'{TEST_SERVER_URL}/wallet/balance/12345'  # проверка баланса кошелька

start = '2019-02-24 11:05:03.918103'
end = '2019-02-24 11:09:06.095966'
id = 1
REPORT_HISTORY_URL = f'{TEST_SERVER_URL}/report/history?start={start}&end={end}&id={id}'  # история операций

name = 'test name'
last_name = 'test last_name'
fathers_name = 'test father_name'
birthday = '01.01.2000'
email = 'test email@mail.ru'
phone = '1234567890'
type_account = 'Физическое лицо'
USER_REGISTRATION_URL = f'{TEST_SERVER_URL}/user/registration'  # регистрация пользователя

new_user = {'name': name, 'last_name': last_name, 'fathers_name': fathers_name,
            'birthday': birthday, 'email': email, 'phone': phone, 'type_account': type_account}

delete_user = {'id': 1111}
DELETE_USER_URL = f'{TEST_SERVER_URL}/user/delete'  # удаления пользователя

new_user_wallet = {'id': 8}
WALLET_CREATE_URL = f'{TEST_SERVER_URL}/wallet/create'  # создание кошелька

delete_wallet = {'id': 8}
WALLET_DELETE_URL = f'{TEST_SERVER_URL}/wallet/delete'  # удаление кошелька

money_input = {'money': 123.45, 'id': 9}
WALLET_INPUT_URL = f'{TEST_SERVER_URL}/wallet/input'  # ввод средств

money_output = {'money': 100.45, 'id': 9}
WALLET_OUTPUT_URL = f'{TEST_SERVER_URL}/wallet/output'  # вывод средств

money_transfer = {'money': 10.00, 'from': '16bf189d-82c3-46be-a2ff-a4e39bb991b2',
                  'to': 'd64e3fec-c15e-490c-9f24-bd647de6156d'}
WALLET_TRANSFER_URL = f'{TEST_SERVER_URL}/wallet/transfer'  # перевод средств


async def test_main_url_1():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(MAIN_URL_1) as response:
            assert response.status == 200


async def test_main_url_2():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(MAIN_URL_2) as response:
            assert response.status == 200


async def test_user_info_url():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(USER_INFO_URL) as response:
            assert response.status == 200


async def test_logs_apilogs_url():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(LOGS_API_LOGS_URL) as response:
            assert response.status == 200


async def test_logs_errorlogs_url():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(LOGS_ERROR_LOGS_URL) as response:
            assert response.status == 200


async def test_wallet_balance_url():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(REPORT_HISTORY_URL) as response:
            assert response.status == 200


async def test_report_history_url():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(WALLET_BALANCE_URL) as response:
            assert response.status == 200


async def test_user_registration():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_REGISTRATION_URL, data=new_user) as response:
            assert response.status == 200


async def test_user_delete():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(DELETE_USER_URL, data=delete_user) as response:
            assert response.status == 200


async def test_wallet_create():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(WALLET_CREATE_URL, data=new_user_wallet) as response:
            assert response.status == 200


async def test_wallet_delete():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(WALLET_DELETE_URL, data=delete_wallet) as response:
            assert response.status == 200


async def test_wallet_input():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(WALLET_INPUT_URL, data=money_input) as response:
            assert response.status == 200


async def test_wallet_output():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(WALLET_OUTPUT_URL, data=money_output) as response:
            assert response.status == 200


async def test_wallet_transfer():
    """
    Проверка на статус ответа
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(WALLET_TRANSFER_URL, data=money_transfer) as response:
            assert response.status == 200


# кроме этого можно добавить несколько тестов на текст ответа, на проверку наличия функций в модулях, на наличие
# самих модулей, на проверку типа возвращаемого значения, проверку суммы и разности переводов, выводов, пополнений
# дополнительно по тестам можно изучить https://aiohttp.readthedocs.io/en/stable/testing.html
import api_wallet


def test_import_api_wallet():
    """
    Проверка наличия функции balance в модуле api_wallet
    """
    assert hasattr(api_wallet, 'balance')


async def test_user_info__return_map():
    """
    Проверка на тип возвращаемого значения
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(USER_INFO_URL) as response:
            assert isinstance(await response.text(), str)
