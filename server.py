import datetime
import traceback
from pprint import pprint

from aiohttp import web

import logging

# from api_logs import

import api_user
import api_logs
import api_report
import api_wallet

from db_helper import dbh

# from db_helper import DBHelper
# from config import current_config

# ------------------ИНИЦИАЛИЗАЦИЯ ЛОГЕРА----------------------
logger = logging.Logger('server')
logger.setLevel('DEBUG')
logger_fh = logging.FileHandler('server.log')
formatter = logging.Formatter('%(filename)s[LINE:%(lineno)d]#%(levelname)-6s [%(asctime)s] %(message)s')
logger_fh.setFormatter(formatter)
logger.addHandler(logger_fh)


# ------------------ИНИЦИАЛИЗАЦИЯ ЛОГЕРА----------------------

# dbh = DBHelper (db_url= current_config.DB_URL)


# async def handle(request):
#     """
#
#     :param request:
#     :return:
#     """
#     logger.info(f'BEGIN handle + {request}')
#     name = request.match_info.get('name', "Anonymous")
#     text = "Hello, " + name
#     logger.info(f'END handle + {request}')
#     return web.Response(text=text)

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
        trace = traceback.format_exc(chain= True)
        dbh.add_error(request_url, request_method, request_data, str(error),  str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)


async def post_handle(request):
    """

    :param request:
    :return:
    """
    data = await request.post()
    logger.info(f'BEGIN post_handle + {request} + {data}')
    text = "Data: " + str(data)
    logger.info(f'END post_handle + {request} + {data}')



    return web.Response(text=text)






if __name__ == '__main__':

    app = web.Application()
    app.add_routes([web.get('/', main),  # стартовая страница
                    web.get('/{name}', main),  # стартовая страница
                    web.get('/user/info/{id}', api_user.info),  # получение информации о пользователе
                    web.post('/user/delete', api_user.delete),  # удаления пользователя
                    web.post('/user/registration', api_user.registration),  # регистрация пользователя

                    web.get('/logs/apilogs', api_logs.apilogs),  # просмотр логов
                    web.get('/logs/errorlogs',  api_logs.errorlogs),  # просмотр ошибочных логов


                    web.get('/report/history', api_report.history),  # история операций

                    web.get('/wallet/balance/{uuid}', api_wallet.balance),  # проверка баланса кошелька
                    web.post('/wallet/create', api_wallet.create),  # создание кошелька
                    web.post('/wallet/delete', api_wallet.delete),  # удаление кошелька
                    web.post('/wallet/input', api_wallet.input),  # ввод средств
                    web.post('/wallet/output', api_wallet.output),  # вывод средств
                    web.post('/wallet/transfer', api_wallet.transfer)  # перевод средств

                    ])

    web.run_app(app)

# Основные функции и возможности е-кошельков
# Пополнение и вывод средств.
# Перевод электронных денег между пользователями
# Платежи
# история операция
# проверка баланса
# создание кошелька(регистрация)
# удаление кошелька
# https://aiohttp.readthedocs.io/en/stable/
# клиент кстати может быть использован для тестов  https://aiohttp.readthedocs.io/en/stable/testing.html
#   web.get('info/{name}', handle),
# схема БД
# описать тестирование в postman