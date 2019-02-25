"""
Модуль для работы с электронным кошельком
"""
import datetime
import traceback
from server import dbh
from aiohttp import web
import uuid
from decimal import Decimal


async def balance(request):  # GET /wallet/balance/{uuid}
    """
    Проверка баланса кошелька (МОЖНО ПОДУМАТЬ ОБ УСЛОЖНЕНИИ ЛОГИКИ ПРОВЕРКИ)
    :param request:
    :return:
    """
    try:
        uuid = request.match_info.get('uuid')
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        request_data = str(request.query_string)
        remote = str(request.remote)

        result = dbh.get_balance_by_uuid(uuid)
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, request_data, remote, str(result), created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, request_data, str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=str(result))


async def create(request):  # POST /wallet/create
    """
    Создание кошелька
    :param request:
    :return:
    """

    try:
        request_data = await request.post()
        user_id = int(request_data['id'])
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        remote = str(request.remote)
        wallet_uuid = uuid.uuid4()

        result = dbh.create_wallet(uuid=wallet_uuid, created=created, user_id=user_id)

        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, str(request_data), remote, result, created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, str(request_data), str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)


async def delete(request):  # POST /wallet/delete
    """
    Удаление кошелька
    :param request:
    :return:
    """
    try:
        request_data = await request.post()

        id = request_data['id']
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        remote = str(request.remote)

        result = str(dbh.delete_wallet_by_id(id))
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, str(request_data), remote, result, created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, str(request_data), str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)


async def input(request):  # POST /wallet/input
    """
    Ввод средств
    :param request:
    :return:
    """
    try:
        request_data = await request.post()

        wallet_id = request_data['id']
        money = Decimal(request_data['money'])
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        remote = str(request.remote)

        result = str(dbh.input_money_by_id(wallet_id=wallet_id, amount=money))
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, str(request_data), remote, result, created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, str(request_data), str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)


async def output(request):  # POST /wallet/output
    """
    Вывод средств
    :param request:
    :return:
    """
    try:
        request_data = await request.post()

        id = request_data['id']
        money = Decimal(request_data['money'])
        print(f'money = {money}')
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        remote = str(request.remote)

        result = str(dbh.output_money_by_id(id, money))
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, str(request_data), remote, result, created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, str(request_data), str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)


async def transfer(request):  # POST /wallet/transfer
    """
    Перевод средств
    :param request:
    :return:
    """
    try:
        request_data = await request.post()

        from_wallet = request_data['from']
        to_wallet = request_data['to']

        money = Decimal(request_data['money'])
        print(f'money = {money}')
        created = datetime.datetime.now()
        request_url = str(request.url)
        request_method = str(request.method)
        remote = str(request.remote)

        result = str(dbh.transfer_money(from_wallet, to_wallet, money))
        finished = datetime.datetime.now()

        dbh.add_log(request_url, request_method, str(request_data), remote, result, created, finished)
    except Exception as error:
        trace = traceback.format_exc(chain=True)
        dbh.add_error(request_url, request_method, str(request_data), str(error), str(trace), created)
        return web.Response(text=str(error))

    return web.Response(text=result)
