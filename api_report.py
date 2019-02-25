"""
Модуль для работы с отчётами
"""
import datetime
import traceback
from db_helper import dbh
from aiohttp import web

async def history(request):  # GET /report/history
    """
    Получение информации о пользователе
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
        id = int(request_data.split('&')[2].split('=')[1])

        start_obj = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        end_obj = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')

        remote = str(request.remote)

        result = dbh.get_history(start_obj, end_obj, id)
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, request_data, remote, str(result), created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    # return web.Response(text=result)
    return web.json_response(result)