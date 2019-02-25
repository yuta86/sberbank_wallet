"""
    Помощник для работы с БД
"""
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from models import Journal, Users, Wallet, ErrorLog, ApiLog
from config import current_config
from decimal import Decimal


class DBHelper:

    def __init__(self, db_url):
        """
        Функция инициализации
        :param db_url: настройки
        """
        self.engine = create_engine(db_url, echo=False, pool_size=50, max_overflow=50)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_journal(self, created, from_wallet_id, to_wallet_id, type_operation):
        """
        Добавление записи в журнал
        :param created: Время записи
        :param from_wallet_id: От кого
        :param to_wallet_id: Кому
        :param type_operation: Тип события
        :return: Результат выполнения функции (Строка)
        """
        try:
            journal = Journal(created=created, from_wallet_id=from_wallet_id, to_wallet_id=to_wallet_id,
                              type_operation=type_operation)

            self.session.add(journal)
            self.session.flush()
            self.session.commit()
            return 'ОК.'
        except:
            return 'ERROR.'

    def user_registration(self, name, last_name, fathers_name, birthday, email, phone, type_account):
        """
        Добавление пользователя
        :param name: Имя
        :param last_name: Фамилия
        :param fathers_name: Отчество
        :param birthday: Дата рождения
        :param email: Почта
        :param phone: Телефон
        :param type_account: Тип аккаунта (Физ. лицо, Юр. лицо)
        :return: Результат выполнения функции (Строка)
        """
        try:
            user = Users(name=name, last_name=last_name, fathers_name=fathers_name,
                         birthday=birthday, email=email, phone=phone, type_account=type_account)

            self.session.add(user)
            self.session.flush()
            self.session.commit()
            return 'Поздравляем, регистрации прошла успешно.'
        except Exception as e:
            return f'Ошибка регистрации. {e}'

    def add_error(self, request_url, request_method, request_data, error, traceback, created):
        """
         Добавление ошибки в БД
        :param request_url: URL
        :param request_method: Метод
        :param request_data: Данные
        :param error: Ошибка
        :param traceback: Подробности
        :param created: Время создания
        :return: Результат выполнения функции (Строка)
        """
        try:

            error_instance = ErrorLog(request_url=request_url, request_method=request_method, request_data=request_data,
                                      error=error, traceback=traceback, created=created)
            self.session.add(error_instance)
            self.session.flush()
            self.session.commit()
            return 'OK.'
        except Exception as e:
            return f'ERROR: {e}'

    def add_log(self, request_url, request_method, request_data, remote, result, created, finished):
        """
         Добавление ошибки в БД
        :param request_url: URL
        :param request_method: Метод
        :param request_data: Данные
        :param remote: Адрес клиента
        :param result: Результат
        :param created: Время создания
        :param finished: Время окончания
        :return: Результат выполнения функции (Строка)
        """
        try:
            log = ApiLog(request_url=request_url, request_method=request_method, request_data=request_data,
                         remote=remote,
                         result=result, created=created, finished=finished)
            self.session.add(log)
            self.session.flush()
            self.session.commit()
            return 'OK.'
        except Exception as e:
            return f'ERROR: {e}'

    def get_user_by_id(self, id):
        """
        Получение информации о пользователе по id
        :param id:
        :return: Результат выполнения функции (Строка либо словарь)
        """
        user = self.session.query(Users).filter(Users.id == id).first()
        if user:
            res = {
                'id': user.id,
                'name': user.name,
                'last_name': user.last_name,
                'fathers_name': user.fathers_name,
                'birthday': str(user.birthday),
                'email': user.email,
                'phone': user.phone,
                'type_account': user.type_account,
                'wallet_id': user.wallet_id,
            }
            return res
        else:
            return 'Отсутствует пользователь с данным id.'

    def delete_user_by_id(self, id):
        """
        Удаление пользователя по id
        :param id: Идентификатор пользователя
        :return: Результат выполнения функции (Строка)
        """
        try:
            user = self.session.query(Users).get(id)
            self.session.delete(user)
            self.session.flush()
            self.session.commit()
            return 'OK.'
        except Exception as e:
            return f'ERROR DELETE: {e}'

    def get_apilogs(self, start, end):
        """
        Получение логов API за интервал времени

        :param start: Дата начала
        :param end: Дата окончания
        :return: Результат выполнения функции (Строка, список словарей)
        """

        api_logs = self.session.query(ApiLog).filter(and_(ApiLog.created >= start, ApiLog.created <= end)).all()
        if api_logs:
            res_api_logs = []
            result = []
            result.append({'count': len(api_logs)})

            for api_log in api_logs:
                one_record = {
                    'id': api_log.id,
                    'request_url': api_log.request_url,
                    'request_method': api_log.request_method,
                    'request_data': api_log.request_data,
                    'remote': api_log.remote,
                    'result': api_log.result,
                    'created': str(api_log.created),
                    'finished': str(api_log.finished),
                }
                res_api_logs.append(one_record)

            result.append({'data': res_api_logs})

            return result
        else:
            return 'Отсутствуют логи api за указанный период.'

    def get_errorlogs(self, start, end):
        """
        Получение логов ошибок за интервал времени

        :param start: Дата начала
        :param end: Дата окончания
        :return: Результат выполнения функции (Строка либо список словарей)
        """

        error_logs = self.session.query(ErrorLog).filter(and_(ErrorLog.created >= start, ErrorLog.created <= end)).all()
        if error_logs:
            res_error_logs = []
            result = []
            result.append({'count': len(error_logs)})

            for error_log in error_logs:
                one_record = {
                    'id': error_log.id,
                    'request_url': error_log.request_url,
                    'request_method': error_log.request_method,
                    'request_data': error_log.request_data,
                    'error': error_log.error,
                    'traceback': error_log.traceback,
                    'created': str(error_log.created),
                }
                res_error_logs.append(one_record)

            result.append({'data': res_error_logs})

            return result
        else:
            return 'Отсутствуют логи ошибок за указанный период.'

    def get_history(self, start, end, id):
        """
        Получение истории за интервал времени

        :param start: Дата начала
        :param end: Дата окончания
        :param id: Идентификатор кошелька
        :return: Результат выполнения функции (Строка либо список словарей)
        """
        histories = self.session.query(Journal).filter(and_(Journal.created >= start, Journal.created <= end)).filter(
            or_(Journal.from_wallet_id == id, Journal.to_wallet_id == id)).all()
        if histories:
            res_histori_logs = []
            result = []
            result.append({'count': len(histories)})

            for histori in histories:
                one_record = {
                    'id': histori.id,
                    'created': str(histori.created),
                    'from_wallet_id': histori.from_wallet_id,
                    'to_wallet_id': histori.to_wallet_id,
                    'type_operation': histori.type_operation,
                }
                res_histori_logs.append(one_record)

            result.append({'data': res_histori_logs})

            return result
        else:
            return 'Отсутствует история операций  за указанный период для данного id.'

    def get_balance_by_uuid(self, uuid):
        """
        Получение баланса по uuid
        :param uuid: uuid идентификатор
        :return: Результат выполнения функции (Строка либо число)
        """
        wallet = self.session.query(Wallet).filter(Wallet.uuid == uuid).first()
        if wallet:
            return wallet.balance
        else:
            return 'Отсутствует кошелёк с данным uuid'

    def create_wallet(self, uuid, created, id, is_active=True, balance=current_config.START_BALANCE):
        """
       Регистрация (создание) нового кошелька
       :param uuid: UUID кошелька
       :param created: Дата создания
       :param id: Идентификатор пользователя
       :param is_active: Активность
       :param balance: Баланс (при регистрации равен START_BALANCE)
       :return: Результат выполнения функции (Строка)
       """
        try:
            wallet = Wallet(uuid=uuid, created=created, is_active=is_active, balance=balance)

            self.session.add(wallet)
            self.session.flush()
            self.session.commit()

            user = self.session.query(Users).filter(Users.id == id).first()
            user.wallet_id = id

            self.session.flush()
            self.session.commit()

            return 'Поздравляем, регистрации кошелька прошла успешно.'
        except Exception as e:
            return f'Ошибка регистрации кошелька: {e}'

    def delete_wallet_by_id(self, id):
        """
        Удаление кошелька по id
        :param id: Идентификатор кошелька
        :return: Результат выполнения функции (Строка)
        """
        try:
            wallet = self.session.query(Wallet).get(id)
            self.session.delete(wallet)
            self.session.flush()
            self.session.commit()
            return 'OK.'
        except AttributeError as e:
            return f'Ошибка удаление кошелька: неправильный идентификатор кошелька'
        except Exception as e:
            return f'ERROR DELETE: {e}'

    def input_money_by_id(self, id, amount):
        """
        Пополнение кошелька по id
        :param id: Идентификатор кошелька
        :param amount: Сумма пополнения
        :return: Результат выполнения функции (Строка)
        """

        try:
            wallet = self.session.query(Wallet).get(id)
            # можно внести лишь ту часть которая до LIMIT
            # if  wallet.balance + amount >  Decimal(current_config.LIMIT):
            #     ostatok = abs(Decimal(current_config.LIMIT) - wallet.balance + amount)
            #     wallet.balance = Decimal(current_config.LIMIT)
            #
            if wallet.balance < Decimal(current_config.LIMIT):
                wallet.balance += amount
                self.session.flush()
                self.session.commit()
                return 'OK'
            else:
                return 'Ошибка пополнения средств: на счету больше, чем лимит.'
        except AttributeError as e:
            return f'Ошибка вывода средств: неправильный идентификатор кошелька'
        except Exception as e:
            return f'Ошибка пополнения средств: {e}'

    def output_money_by_id(self, id, amount):
        """
        Вывод средств с кошелька по id
        :param id: Идентификатор кошелька
        :param amount: Сумма вывода
        :return: Результат выполнения функции (Строка)
        """

        try:
            wallet = self.session.query(Wallet).get(id)

            if wallet.balance >= amount:
                wallet.balance -= amount
                self.session.flush()
                self.session.commit()
                return 'OK'
            else:
                return 'Ошибка вывода средств: недостаточно средств.'
        except AttributeError as e:
            return f'Ошибка вывода средств: неправильный идентификатор кошелька'

        except Exception as e:
            return f'Ошибка вывода средств: {e}'

    def transfer_money(self, from_wallet, to_wallet, amount):
        """
        Вывод средств с кошелька по id
        :param from_wallet: Идентификатор uuid кошелька (от кого)
        :param to_wallet: Идентификатор uuid кошелька (кому)
        :param amount: Сумма перевода
        :return: Результат выполнения функции (Строка)
        """

        try:
            instance_from = self.session.query(Wallet).filter(Wallet.uuid == from_wallet).first()
            if instance_from:
                instance_to = self.session.query(Wallet).filter(Wallet.uuid == to_wallet).first()
                if instance_to:
                    if instance_from.balance >= amount:
                        if instance_to.balance + amount < Decimal(current_config.LIMIT):
                            instance_to.balance += amount
                            instance_from.balance -= amount
                            self.session.flush()
                            self.session.commit()
                        else:
                            return f'Ошибка перевода средств: на счету получателя больше, чем лимит.'
                    else:
                        return f'Ошибка перевода средств: недостаточно средств.'
                else:
                    return f'Ошибка перевода средств: неправильный идентификатор кошелька (кому переводим).'

            else:
                return f'Ошибка перевода средств: неправильный идентификатор кошелька (от кого перевод).'


        except Exception as e:
            return f'Ошибка вывода средств: {e}'


dbh = DBHelper(db_url=current_config.DB_URL)

# def add_eyes(self, journal_id, ratio_left, left_top_x, left_top_y, left_bottom_x, left_bottom_y, ratio_right,
#              right_top_x, right_top_y, right_bottom_x, right_bottom_y):
#     """
#     Добавление глаз в БД
#     :param journal_id: Идентификатор в журнале
#     :param ratio_left: Соотношение левого глаза
#     :param left_top_x: Координаты верхнего X левого глаза
#     :param left_top_y: Координаты верхнего Y левого глаза
#     :param left_bottom_x: Координаты нижнего X  левого глаза
#     :param left_bottom_y: Координаты нижнего У левого глаза
#     :param ratio_right: Соотношение правого глаза
#     :param right_top_x: Координаты верхнего X правого глаза
#     :param right_top_y: Координаты верхнего Y правого глаза
#     :param right_bottom_x: Координаты нижнего X  правого глаза
#     :param right_bottom_y: Координаты нижнего У правого глаза
#     :return:
#     """
#     eyes = Eyes(journal_id=journal_id, ratio_left=ratio_left, left_top_x=left_top_x, left_top_y=left_top_y,
#                 left_bottom_x=left_bottom_x, left_bottom_y=left_bottom_y, ratio_right=ratio_right,
#                 right_top_x=right_top_x, right_top_y=right_top_y,
#                 right_bottom_x=right_bottom_x, right_bottom_y=right_bottom_y)
#     # # print(eyes)
#     self.session.add(eyes)
#     self.session.flush()
#     self.session.commit()
#     return eyes.id
#
# def add_journal(self, rec_date, user_id, camera_id, image, is_deviant, vector_json):
#     """
#     Функция добавления в журнал в БД
#     :param rec_date: Время записи
#     :param user_id: Идентификатор пользователя
#     :param camera_id: Номер камеры
#     :param image: Изображение с камеры
#     :param is_deviant: Отклонился от времени
#     :param vector_json: Вектор пришедшего
#     :return:
#     """
#     # print('add_journal')
#     journal = Journal(rec_date=rec_date, user_id=user_id, camera_id=camera_id, image=image,
#                       is_deviant=is_deviant, vector_json=vector_json)
#     self.session.add(journal)
#     self.session.flush()
#     self.session.commit()
#     # print('add_journal')
#     return journal.id
#
# def add_camera(self, ip, location, description, add_guest):
#     """
#     Функция добавления камеры в БД
#     :param ip: Ip адрес
#     :param location: Расположение
#     :param description: Описание камеры
#     :param add_guest: ДОбавлять гостей с этой камеры
#     :return:
#     """
#     camera = Camera(location=location, description=description, ip=ip, add_guest=add_guest)
#     # print(camera.id)
#     self.session.add(camera)
#     self.session.flush()
#     self.session.commit()
#     print(camera.id)  # получение вставленной записи
#     return camera
#
# def add_user(self, name, surname, fathers_name, login, org, post, birthday, passport, email,
#              type_account, photo, vector_json, is_active):
#     """
#     Функция добавления пользователя в БД сразу под ВСЕ камеры !!!
#     :param name: Имя
#     :param surname: Фамилия
#     :param fathers_name: Отчество
#     :param login: Логин
#     :param org: Организация
#     :param post: Должность
#     :param birthday: Дата рождения
#     :param passport: Паспорт
#     :param email: Эл. почта
#     :param type_account: Тип пользователя
#     :param photo: Фото в ByteArr
#     :param vector_json: JSON
#     :param is_active: Активность
#     :return:
#     """
#     camera_ids = self.get_all_camera()
#     max_id = self.get_max_id_from_users()
#     user_id = max_id + 1  # увеличение id пользователя
#
#     for camera_id in camera_ids:
#         user = Users(id=user_id, camera_id=camera_id, name=name, surname=surname, fathers_name=fathers_name,
#                      login=login,
#                      org=org, post=post, birthday=birthday, passport=passport, email=email,
#                      type_account=type_account,
#                      photo=photo, vector_json=vector_json, is_active=is_active
#                      )
#         self.session.add(user)
#     self.session.flush()
#     self.session.commit()
#     return user_id
#
# def add_base_vector(self, user_id, base_json):
#     """
#     Функция добавления базового вектора для пользователя
#     :param user_id: Id пользователя
#     :param base_json: JSON
#     :return:
#     """
#     vector = Vectors(user_id=user_id, vector_json=base_json)
#     self.session.add(vector)
#     self.session.flush()
#     self.session.commit()
#     return vector
#
# def add_all_base_vector(self, camera_id, type_account):
#     """
#     Функция добавления базового вектора для пользователя
#     :param camera_id: Id камеры
#     :param type_account: Тип аккаунта
#     :return:
#     """
#     print('---------------add_all_base_vector---------------')
#
#     users = self.session.query(Users).filter(
#         Users.type_account == type_account).all()  # получили все id пользователей
#     user_ids = [user.id for user in users]
#     # print(user_ids)
#
#     unic_users_id = list(set(user_ids))  # убрали повторы из-за id камер
#
#     print('ДОБАВЛЯЕМ БАЗОВЫЙ ВЕКТОР ДЛЯ {count} ПОЛЬЗОВАТЕЛЕЙ'.format(count=len(unic_users_id)))
#
#
#     for user_id in unic_users_id:
#         # print('-=-=-=-=-=-=-=--=-=-=-')
#         # print(user_id)
#         vector = self.get_vector_by_user_id(user_id)  # получили БАЗОВЫЙ вектор пользователя
#         # print(type(vector))
#         # user = self.session.query(Users).filter(Users.id == user_id).first()
#         # # print(type(user))
#         # # print ('user' + str(user))
#
#         user = self.session.query(Users).filter(Users.id == user_id).first()  # получили пользователя
#
#         new_user = Users(id=user_id, camera_id=camera_id, name=user.name, surname=user.surname,
#                          fathers_name=user.fathers_name,
#                          login=user.login,
#                          org=user.org, post=user.post, birthday=user.birthday, passport=user.passport,
#                          email=user.email,
#                          type_account=user.type_account,
#                          photo=user.photo, vector_json=str(vector.vector_json), is_active=user.is_active)
#         self.session.add(new_user)
#
#     # print('---------------END add_all_base_vector---------------')
#
#     self.session.flush()
#     self.session.commit()
#
#     return users
#
# def get_vector_by_user_id(self, user_id):
#     """
#     Функция получения базового вектора по id пользователя
#     :param user_id:
#     :return:
#     """
#
#     user_vector = self.session.query(Vectors).filter(Vectors.user_id == user_id).first()
#     return user_vector
#
# def update_user_type_account(self, user, type_account):
#     """
#     Функция обновления типа аккаунта пользователя
#     :param user: Пользователь
#     :param type_account: Тип аккаунта
#     :return:
#     """
#     user_ids = self.get_users_by_id(user.id)
#     # print(user_ids)
#     for user in user_ids:
#         user.type_account = type_account
#
#     self.session.flush()
#     self.session.commit()
#
# def update_user_vector(self, user, camera_id, vector):
#     """
#     Функция обновления типа аккаунта пользователя
#     :param user: Пользователь
#     :param camera_id: Камера
#     :param vector: Вектор пользователя
#     :return:
#     """
#     user_ids = self.get_users_by_id(user.id)  # получение пользователя на всех камерах
#     # print(user_ids)
#     for user in user_ids:
#         if user.camera_id == camera_id:  # меняем вектор пользователя под эту камеру
#             user.vector_json = vector
#             break
#
#     self.session.flush()
#     self.session.commit()
#
# def update_user_vector_by_id(self, user, camera_id, vector):
#     """
#     Функция обновления типа аккаунта пользователя
#     :param user: ID Пользователь
#     :param camera_id: Камера
#     :param vector: Вектор пользователя
#     :return:
#     """
#     user_ids = self.get_users_by_id(user)  # получение пользователя на всех камерах
#     # print(user_ids)
#     for user in user_ids:
#         if user.camera_id == camera_id:  # меняем вектор пользователя под эту камеру
#             user.vector_json = vector
#             break
#
#     self.session.flush()
#     self.session.commit()
#
# def get_users_by_id(self, ids):
#     """
#     Получение пользователей по id
#     :param ids: ID пользователя
#     :return: Список пользователей
#     """
#
#     if isinstance(ids, int):
#         users = self.session.query(Users).filter(Users.id == ids).all()
#     else:
#         users = self.session.query(Users).filter(Users.id.in_(ids)).all()
#     return users
#
# def get_users_by_type_account_camera_id(self, type_account, camera_id):
#     """
#     Функция получения пользователей по типу type_account и по номеру камеры
#     :param type_account: Тип аккаунта
#     :param camera_id: Номер камеры
#     :return: Пользователи
#     """
#     users = self.session.query(Users).filter(Users.type_account == type_account).filter(
#         Users.camera_id == camera_id).all()  # Фильтр по типу акаунта и номеру камеры
#     # print(users)
#     # for user in users:
#     #     print(user.id)
#     return users
#
# def get_camera_from_ip(self, ip):
#     """
#     Функция получения id камеры по ip
#     :param ip: IP камеры
#     :return:
#     """
#
#     camera = self.session.query(Camera).filter(Camera.ip == ip).first()  # .all()
#     if camera is None:
#         num = 0
#     else:
#         num = camera.id
#     return num
#
# def get_camera_from_add_user(self):
#     """
#     Функция получения id камер по полю add_user = True
#     :return:
#     """
#     cameras = self.session.query(Camera).filter(Camera.add_guest == 'True').all()
#     # print(camera)
#     num = [camera.ip for camera in cameras]
#     return num
#
# def get_all_camera(self):
#     """
#     Функция получения id камер
#     :return: Список id камер
#     """
#     cameras = self.session.query(Camera).all()
#     # print(cameras)
#     num = [camera.id for camera in cameras]
#     return num
#
# def get_max_id_from_users(self):
#     """
#     Функция получения максимального id в таблице Users
#     :return:
#     """
#     max_id = self.session.query(func.max(Users.id)).scalar()
#     if max_id is None:
#         max_id = 0
#     return max_id
#
# def get_rows_from_journal_by_date_less(self, date):
#     """
#     Функция получения id пользователей в таблице Journal по дате
#     :param date: Дата со сдвигом для поиска старых значений
#     :return: строки в таблице
#     """
#     rows = self.session.query(Journal).filter(Journal.rec_date < date).all()  # старше
#     return rows
#
# def get_journal_by_id(self, id):
#     """
#     Функция Получения строки в журнале по id
#     :param id: ID в Журнале
#     :return: Строку
#     """
#     journal = self.session.query(Journal).filter(Journal.id == id).first()
#     return journal
#
# def get_rows_from_journal_by_date_more(self, date_more):
#     """
#     Функция получения id пользователей в таблице Journal по дате
#     :param date_more: Дата больше чем
#     :return: строки в таблице
#     """
#
#     rows = self.session.query(Journal).filter(Journal.rec_date >= date_more).order_by(desc(Journal.rec_date))
#
#     # rows_ids = [row.id for row in rows]
#     # print('rows_ids=' + str(rows_ids))
#
#     return rows
#
# def get_users_by_type_account(self, type_account):
#     """
#     Функция получения id пользователей которые принадлежат к type_account
#     :param type_account: Тип аккаунта
#     :return: id пользователей
#     """
#
#     users = self.session.query(Users).filter(or_(Users.type_account == v for v in type_account))
#
#     # print('users=' + str(users))
#     user_ids = [user.id for user in users]
#     # print('user_ids=' + str(user_ids))
#     return user_ids
#
# def delete_from_journal(self, selection):
#     """
#      Функция удаления  выборки строк журнала из таблицы Journal
#     :param selection:
#     :return:
#     """
#     for item in selection:
#         self.session.delete(item)
#         # print(str(item.id) + '\n')
#
#     self.session.flush()
#     self.session.commit()
#
# def delete_from_eyes(self):
#     """
#     Функция удаления глаз из таблицы Eyes
#     :return:
#     """
#     self.session.query(Eyes).filter(Eyes.journal_id is None).delete()  # ==
#     # print('good delete_from_eyes')
#     self.session.flush()
#     self.session.commit()
#
# def delete_users(self, ids):
#     """
#     Функция удаления  выборки пользователей из таблицы User
#     :param ids:
#     :return:
#     """
#     # print('Пришло в get_users_by_id' + str(ids))
#
#     for id in ids:
#         self.session.query(Users).filter(Users.id == id).delete()
#         # print(str(id) + '\n')
#     # print('good delete_users')
#     self.session.flush()
#     self.session.commit()
#
# def get_count(self):
#     count_guest = (self.session.query(func.count('*')).select_from(Users)).filter(
#         Users.type_account == 'GUEST').scalar()
#     count_worker = (self.session.query(func.count('*')).select_from(Users)).filter(
#         Users.type_account == 'WORKER').scalar()
#     count_frequent = (self.session.query(func.count('*')).select_from(Users)).filter(
#         Users.type_account == 'FREQUENT_VISITOR').scalar()
#
#     # print(count_guest)
#     # print(count_worker)
#     # print(count_frequent)
#     return count_guest, count_worker, count_frequent
#
# # def join(self, type_account):
# #     query = self.session.query(Journal, Users)
# #     query = query.filter(Journal.user_id == Users.id).filter(Journal.camera_id == Users.camera_id).filter(
# #         Users.type_account == type_account)
# #     records = query.all()
# #     # print(type(records))
# #     for journal, user in records:
# #         str = f'journal.id ={journal.id} journal.camera_id = {journal.camera_id} ournal.user_id = {journal.user_id} ' \
# #               f'user.id = {users.id} user.camera_id = {user.camera_id} user.name ={users.name} user.type_account = {users.type_account}'
# #         print(str)
#
# def join_rec_date(self, type_account, date, date_old):
#     query = self.session.query(Journal, Users)
#     query = query.filter(Journal.user_id == Users.id).filter(Journal.camera_id == Users.camera_id).filter(
#         Users.type_account == type_account).filter(Journal.rec_date < date).filter(Journal.rec_date > date_old)
#
#     records = query.all()
#     # print(type(records))
#     for journal, user in records:
#         str = f'journal.id ={journal.id} journal.camera_id = {journal.camera_id} ournal.user_id = {journal.user_id} ' \
#               f'user.id = {users.id} user.camera_id = {user.camera_id} user.name ={users.name} user.type_account = {users.type_account}'
