import requests
import logging
import inspect
from allure import step


class Api:
    log = logging.getLogger(__name__)
    headers = {'Accept': 'application/json',
               'content-type': 'application/json',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    url = 'https://api.jolybell.com'
    mock_url = 'http://localhost:8080'

    @staticmethod
    def get_uuid():
        path = '/carts'
        with step('Создать новую корзину'):
            r = requests.post(Api.url + path, headers=Api.headers)
            uuid = r.json()['data']['uuid']
            with step(f"Номер корзины: [{uuid}]"):
                pass
        Api.logging(r)
        return uuid

    @staticmethod
    def logging(r, test_data=None):
        Api.log.info(f'CALLED BY: {inspect.currentframe().f_back.f_back.f_code.co_name}\n'
                     f'Request URL: {r.request.url}\n'
                     f'Request Method: {r.request.method}\n'
                     f'Status code: {r.status_code}\n'
                     f'Response Headers: {r.headers}\n'
                     f'Request Headers: {r.request.headers}\n'
                     f'Request Payload: {test_data}\n'
                     f'Response JSON: {r.json()}\n'
                     f'Elapsed: {r.elapsed.total_seconds()}\n')

    @staticmethod
    def add_request(test_data):
        path = '/carts/add'
        with step('Добавить товар в корзину'):
            r = requests.post(Api.url + path, headers=Api.headers, json=test_data)
            with step(f'Товар: {test_data}'):
                pass
        Api.logging(r, test_data)
        return r

    @staticmethod
    def change_request(test_data):
        path = '/carts/change'
        with step('Изменить ранее добавленный товар в корзине'):
            r = requests.put(Api.url + path, headers=Api.headers, json=test_data)
            with step(f'Изменение товара: {test_data}'):
                pass
        Api.logging(r, test_data)
        return r

    @staticmethod
    def remove_request(test_data):
        path = '/carts/remove'
        with step('Удалить ранее добавленный товар из корзины'):
            r = requests.delete(Api.url + path, headers=Api.headers, json=test_data)
            with step(f'Товар: {test_data}'):
                pass
        Api.logging(r, test_data)
        return r

    @staticmethod
    def config_request(headers):
        path = '/config'
        with step(f'Отправить GET запрос config с заголовком accept-language = {headers["accept-language"]}'):
            r = requests.get(Api.url + path, headers=headers)
        Api.logging(r)
        return r

    @staticmethod
    def load_request():
        path = '/deliveries/load'
        with step('Отправить GET запрос load'):
            r = requests.get(Api.url + path, headers=Api.headers)
        Api.logging(r)
        return r

    @staticmethod
    def uuid_request(uuid):
        path = f'/carts/{uuid}'
        with step(f'Запросить содержимое корзины [{uuid}]'):
            r = requests.get(Api.url + path, headers=Api.headers)
        Api.logging(r)
        return r

    @staticmethod
    def orders_request(uuid):
        path = '/orders'
        with step('Оформить заказ'):
            r = requests.post(Api.url + path, headers=Api.headers, json={'cart_uuid': uuid})
        Api.logging(r)
        return r

    @staticmethod
    def carts_request():
        path = '/carts'
        with step('Создать новую корзину'):
            r = requests.post(Api.mock_url + path, headers=Api.headers)
            with step(f"Номер корзины: [{r.json()['data']['uuid']}]"):
                pass
        Api.logging(r)
        return r
