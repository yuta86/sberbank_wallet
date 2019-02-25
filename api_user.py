"""
Модуль для работы с пользователями
"""
import datetime
import traceback
from aiohttp import web
from db_helper import dbh


# created = datetime.datetime.now()
#
# try:
#     name = request.match_info.get('name', "Анонимный пользователь")
#     pprint(request)
#     request_url = str(request.url)
#     request_method = str(request.method)
#     request_data = str(request.query_string)
#     remote = str(request.remote)
#
#     finished = datetime.datetime.now()
#     result = "Добро пожаловать, " + name
#     dbh.add_log(request_url, request_method, request_data, remote, result, created, finished)
# except Exception as error:
#     trace = traceback.format_exc(chain=True)
#     dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
#     return web.Response(text=str(error))
#
# return web.Response(text=result)


async def info(request):  # GET /user/info/{id}
    """
    Получение информации о пользователе
    :param request:
    :return:
    """

    try:
        id = request.match_info.get('id')
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        request_data = str(request.query_string)
        remote = str(request.remote)

        result = dbh.get_user_by_id(id)
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, request_data, remote, str(result), created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    # return web.Response(text=result)
    return web.json_response(result)


async def delete(request):  # POST  /user/delete
    """
    Удаление пользователя
    :param request:
    :return:
    """
    try:
        request_data = await request.post()

        id = int(request_data['id'])
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        remote = str(request.remote)

        result = dbh.delete_user_by_id(id)
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, str(request_data), remote, str(result), created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)


async def registration(request):  # POST /user/registration
    """
    Регистрация пользователя
    :param request:
    :return:
    """
    try:
        request_data = await request.post()

        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        remote = str(request.remote)

        result = dbh.user_registration(name=request_data['name'], last_name=request_data['last_name'],
                              fathers_name=request_data['fathers_name'],
                              birthday=request_data['birthday'], email=request_data['email'],
                              phone=request_data['phone'], type_account=request_data['type_account'])

        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, str(request_data), remote, result, created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)
