from allure import step


class Assertions:

    @staticmethod
    def status_code(r, status_code):
        with step(f'Получен ответ с кодом {status_code}'):
            assert r.status_code == status_code

    @staticmethod
    def config(r, locale):
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            assert r.json()['data']['app']['currency'] == 'USD'
            assert r.json()['data']['auth']['password_min_length'] == 6
            assert r.json()['data']['categories']['alias_max_length'] == 15
            assert r.json()['data']['products']['decorations'] == ['black_default', 'white_default']
            assert r.json()['data']['promocodes']['name_max_length'] == 10
            assert r.json()['data']['orders']['states'] == ['active', 'processed', 'accepted', 'sended', 'suspended']
            assert r.json()['data']['languages']['names'] == ['en', 'ru', 'uk']
            assert r.json()['data']['currencies']['names'] == ['USD', 'EUR', 'RUB', 'UAH']
            assert r.json()['data']['deliveries']['price_precision'] == 2
        with step('Параметр locale в теле ответа JSON соответствует значению, переданному в заголовке accept-language'):
            assert r.json()['data']['app']['locale'] == locale

    @staticmethod
    def load(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            for data in r.json()['data']:
                assert int(data['id'])
                assert data['name'] in ['ground', 'air']
                assert type(data['created_at']) == int
                assert type(data['updated_at']) == int

    @staticmethod
    def carts(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            assert len(r.json()['data']['uuid']) == 36
            assert type(r.json()['data']['uuid']) == str
            assert type(r.json()['data']['expired_at']) == int

    @staticmethod
    def uuid(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            assert r.json()['data']['products'] == []

    @staticmethod
    def add(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            assert r.json()['notification']['type'] == 'success'
            assert r.json()['notification']['message'] == 'The product was added to the shopping cart.'

    @staticmethod
    def change(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            assert r.json()['notification']['type'] == 'success'
            assert r.json()['notification']['message'] == 'The item in the shopping cart has been changed.'

    @staticmethod
    def remove(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            assert r.json()['notification']['type'] == 'success'
            assert r.json()['notification']['message'] == 'The product is removed from the basket.'

    @staticmethod
    def orders_with_empty_cart(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result'] is False
            assert r.json()['notification']['type'] == 'error'
            assert r.json()['notification']['message'] == 'There are no products in this cart.'

    @staticmethod
    def orders_valid_values(r):
        with step('Заголовки ответа соответствуют ожидаемому результату'):
            assert r.headers['content-type'] == 'application/json; charset=utf-8'
        with step('Тело ответа JSON соответствует ожидаемому результату'):
            assert r.json()['result']
            assert len(r.json()['data']['uuid']) == 36
            assert type(r.json()['data']['uuid']) == str

    @staticmethod
    def cart_is_empty(r):
        with step('В корзине отсутствуют товары'):
            assert r.json()['data']['products'] == []

    @staticmethod
    def product_in_cart(r, product):
        with step('Ранее добавленный товар находится в корзине'):
            assert r.json()['data']['products'][0]['id'] == str(product['product_id'])
            assert r.json()['data']['products'][0]['pivot']['total_count'] == int(product['count'])
            if 'size_id' in product:
                assert r.json()['data']['products'][0]['pivot']['size']['id'] == str(product['size_id'])
            else:
                assert r.json()['data']['products'][0]['pivot']['size'] is None

    @staticmethod
    def upd_product_count_in_cart(r, product_upd):
        with step('Внесенные изменения применились к ранее добавленному товару'):
            assert r.json()['data']['products'][0]['id'] == str(product_upd['product_id'])
            assert r.json()['data']['products'][0]['pivot']['total_count'] == int(product_upd['total_count'])
            if 'current_size_id' in product_upd:
                assert r.json()['data']['products'][0]['pivot']['size']['id'] == str(product_upd['current_size_id'])
            else:
                assert r.json()['data']['products'][0]['pivot']['size'] is None

    @staticmethod
    def upd_product_size_in_cart(r, product_upd):
        with step('Внесенные изменения применились к ранее добавленному товару'):
            assert r.json()['data']['products'][0]['id'] == str(product_upd['product_id'])
            assert r.json()['data']['products'][0]['pivot']['size']['id'] == str(product_upd['updated_size_id'])
