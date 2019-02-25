import datetime
from pprint import pprint

import aiohttp
import asyncio

USER_TYPES = {'individual': 'Физическое лицо', 'organization': 'Юридическое лицо'}


async def fetch(session, url, params=None):
    """

    :param session:
    :param url:
    :param params:
    :return:
    """
    print('------------------------------')

    async with session.get(url, params=params) as response:
        return await response.text()


async def post(session, url, data):
    """

    :param session:
    :param url:
    :param data:
    :return:
    """
    print('===================================')
    # session.post('http://httpbin.org/post', data=b'data')
    async with session.post(url, data=data) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://0.0.0.0:8080')
        print(html)
        #
        # html = await fetch(session, 'http://0.0.0.0:8080/vasya')
        # print(html)
        # params = {'key1': 'value1', 'key2': 'value2'}
        # html = await fetch(session, 'http://0.0.0.0:8080/vasya', params)
        # print(html)
        #
        #
        html = await fetch(session, 'http://0.0.0.0:8080/user/info/1')
        pprint(html)
        # delete_user = {'id': '3'}
        # html = await post(session, 'http://0.0.0.0:8080/user/delete', delete_user)
        # print(html)

        # start = '2019 - 02 - 24 11:46:55.143689'
        # end = '2019 - 02 - 24 11:50:55.143689'
        # params = {'start': start, 'end': end}

        # html = await fetch(session, 'http://0.0.0.0:8080/logs/apilogs', params)
        # pprint(html)

        # start = '2019-02-24 11:05:03.918103'
        # end = '2019-02-24 11:09:06.095966'
        # params = {'start': start, 'end': end}
        #
        # html = await fetch(session, 'http://0.0.0.0:8080/logs/errorlogs', params)
        # pprint(html)

        start = '2019-02-24 11:05:03.918103'
        end = '2019-02-24 11:09:06.095966'
        params = {'start': start, 'end': end, 'id': 1}


        html = await fetch(session, 'http://0.0.0.0:8080/report/history', params)
        pprint(html)





        # registration_user = {'name': 'name_user', 'last_name': 'last_name', 'fathers_name': 'fathers_name',
        #                      'birthday': 'birthday', 'email': 'email', 'phone': 'phone', 'type_account': USER_TYPES['individual']}
        #
        #
        # html = await post(session, 'http://0.0.0.0:8080/user/registration', registration_user)
        #
        # print(html)

        #
        # web.get('/user/info', api_user.info),  # получение информации о пользователе
        # web.post('/user/delete', api_user.delete),  # удаления пользователя
        # web.post('/user/registration', api_user.registration),  # регистрация пользователя

        # asyncio.sleep(0.1)
        # html = await post(session, 'http://0.0.0.0:8080', {'usd':'12345'})
        # print(html)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
