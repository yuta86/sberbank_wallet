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

    def create_wallet(self, uuid, created, user_id, is_active=True, balance=current_config.START_BALANCE):
        """
       Регистрация (создание) нового кошелька
       :param uuid: UUID кошелька
       :param created: Дата создания
       :param user_id: Идентификатор пользователя
       :param is_active: Активность
       :param balance: Баланс (при регистрации равен START_BALANCE)
       :return: Результат выполнения функции (Строка)
       """
        try:
            wallet = Wallet(uuid=uuid, created=created, is_active=is_active, balance=balance)

            self.session.add(wallet)
            self.session.flush()
            self.session.commit()

            user = self.session.query(Users).filter(Users.id == user_id).first()
            user.wallet_id = wallet.id

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

    def input_money_by_id(self, wallet_id, amount):
        """
        Пополнение кошелька по id
        :param wallet_id: Идентификатор кошелька
        :param amount: Сумма пополнения
        :return: Результат выполнения функции (Строка)
        """

        try:
            wallet = self.session.query(Wallet).get(wallet_id)
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
