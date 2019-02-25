"""
Модуль для работы с логами
"""
import datetime
import traceback
from db_helper import dbh
from aiohttp import web


async def apilogs(request):  # GET /logs/apilogs
    """
    Получение информации о логах
    :param request:
    :return:
    """

    try:
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        request_data = str(request.query_string)

        start = request_data.split('&')[0].split('=')[1]
        end = request_data.split('&')[1].split('=')[1]

        start_obj = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        end_obj = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')

        remote = str(request.remote)

        result = dbh.get_apilogs(start_obj, end_obj)
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, request_data, remote, str(result), created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.json_response(result)


async def errorlogs(request):  # GET '/logs/errorlogs
    """
     Получение информации о логах ошибок
    :param request:
    :return:
    """
    try:
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        request_data = str(request.query_string)

        start = request_data.split('&')[0].split('=')[1]
        end = request_data.split('&')[1].split('=')[1]

        start_obj = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        end_obj = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')

        remote = str(request.remote)

        result = dbh.get_errorlogs(start_obj, end_obj)
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, request_data, remote, str(result), created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.json_response(result)
