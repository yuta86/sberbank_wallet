import datetime
import traceback
from pprint import pprint
from aiohttp import web
import logging

import api_user
import api_logs
import api_report
import api_wallet

from db_helper import dbh

# ------------------ИНИЦИАЛИЗАЦИЯ ЛОГЕРА----------------------
logger = logging.Logger('server')
logger.setLevel('DEBUG')
logger_fh = logging.FileHandler('server.log')
formatter = logging.Formatter('%(filename)s[LINE:%(lineno)d]#%(levelname)-6s [%(asctime)s] %(message)s')
logger_fh.setFormatter(formatter)
logger.addHandler(logger_fh)
# логирование в текстовый файл при необходимости (в текущей версии используется логирование в БД)
# ------------------ИНИЦИАЛИЗАЦИЯ ЛОГЕРА----------------------


async def main(request):
    """
    Главная страница
    :param request:
    :return:
    """
    created = datetime.datetime.now()

    try:
        name = request.match_info.get('name', "Анонимный пользователь")
        pprint(request)
        request_url = str(request.url)
        request_method = str(request.method)
        request_data = str(request.query_string)
        remote = str(request.remote)

        finished = datetime.datetime.now()
        result = "Добро пожаловать, " + name
        dbh.add_log(request_url, request_method, request_data, remote, result, created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', main),  # стартовая страница
                    web.get('/{name}', main),  # стартовая страница
                    web.get('/user/info/{id}', api_user.info),  # получение информации о пользователе
                    web.post('/user/delete', api_user.delete),  # удаления пользователя
                    web.post('/user/registration', api_user.registration),  # регистрация пользователя

                    web.get('/logs/apilogs', api_logs.apilogs),  # просмотр логов
                    web.get('/logs/errorlogs', api_logs.errorlogs),  # просмотр ошибочных логов

                    web.get('/report/history', api_report.history),  # история операций

                    web.get('/wallet/balance/{uuid}', api_wallet.balance),  # проверка баланса кошелька
                    web.post('/wallet/create', api_wallet.create),  # создание кошелька
                    web.post('/wallet/delete', api_wallet.delete),  # удаление кошелька
                    web.post('/wallet/input', api_wallet.input),  # ввод средств
                    web.post('/wallet/output', api_wallet.output),  # вывод средств
                    web.post('/wallet/transfer', api_wallet.transfer)  # перевод средств

                    ])

    web.run_app(app)

# клиент кстати может быть использован для тестов  https://aiohttp.readthedocs.io/en/stable/testing.html
