import pytest
import allure
from tests.utils.api import Api
from tests.utils.assertions import Assertions


def format_data(**kwargs):
    return kwargs


class TestPageLoad:

    @allure.feature(f'Запрос конфигурации {Api.url}/config')
    @allure.title(f'GET запрос {Api.url}/config Отображение локализации; Структура ответа')
    def test_config_lang(self):
        locales = ['en', 'ru', 'uk']
        headers = {'content-Type': 'application/json', 'accept-language': ''}
        for locale in locales:
            headers['accept-language'] = locale
            r = Api.config_request(headers)
            Assertions.status_code(r, 200)
            Assertions.config(r, locale)

    @allure.feature(f'{Api.url}/load')
    @allure.title(f'GET запрос {Api.url}/load Структура ответа')
    def test_load(self):
        r = Api.load_request()
        Assertions.status_code(r, 200)
        Assertions.load(r)

    @allure.feature(f'Создание корзины. {Api.url}/carts')
    @allure.title(f'{Api.url}/carts Структура ответа')
    def test_carts(self, wiremock):
        r = Api.carts_request()
        Assertions.status_code(r, 200)
        Assertions.carts(r)

    @allure.feature('Запрос содержимого корзины')
    @allure.title(f'GET запрос {Api.url}/[Номер корзины] Структура ответа')
    def test_uuid(self):
        r = Api.uuid_request(Api.get_uuid())
        Assertions.status_code(r, 200)
        Assertions.uuid(r)


class TestAdd:

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину переданы параметры типа int')
    @pytest.mark.add
    def test_add_int_values(self, uuid):
        product = format_data(uuid=uuid, product_id=12, size_id=4, count=1)
        r = Api.add_request(product)
        Assertions.status_code(r, 200)
        Assertions.add(r)
        r = Api.uuid_request(uuid)
        Assertions.product_in_cart(r, product)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину переданы параметры типа str')
    @pytest.mark.add
    def test_add_str_values(self, uuid):
        product = format_data(uuid=uuid, product_id='12', size_id='4', count='1')
        r = Api.add_request(product)
        Assertions.status_code(r, 200)
        Assertions.add(r)
        r = Api.uuid_request(uuid)
        Assertions.product_in_cart(r, product)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('Добавление товара, который не имеет размера')
    @pytest.mark.add
    def test_add_not_clothes(self, uuid):
        product = format_data(uuid=uuid, product_id='90', count=5)
        r = Api.add_request(product)
        Assertions.status_code(r, 200)
        Assertions.add(r)
        r = Api.uuid_request(uuid)
        Assertions.product_in_cart(r, product)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара, который не имеет размера передан параметр размера')
    @pytest.mark.add
    def test_add_not_clothes_with_size(self, uuid):
        product = format_data(uuid=uuid, product_id='90', size_id='1', count=1)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину передан несуществующий номер корзины')
    @pytest.mark.add
    def test_add_invalid_uuid(self, uuid):
        product = format_data(uuid='65305a9a-def7-4c14-a6d1-3ee1507c4d6c', product_id='12', size_id='4', count=5)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину передан неверный тип номера корзины')
    @pytest.mark.add
    def test_add_wrong_type_uuid(self, uuid):
        product = format_data(uuid=123456789012345678901234567890658375, product_id='12', size_id='4', count=1)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину передан несуществующий номер товара')
    @pytest.mark.add
    def test_add_invalid_product_id(self, uuid):
        product = format_data(uuid=uuid, product_id='300', size_id='4', count=3)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину передан несудествующий размер товара')
    @pytest.mark.add
    def test_add_invalid_size_id(self, uuid):
        product = format_data(uuid=uuid, product_id='12', size_id='65', count=1)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину передано отрицательное количество товаров')
    @pytest.mark.add
    def test_add_negative_count(self, uuid):
        product = format_data(uuid=uuid, product_id='5', size_id='3', count=-1)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину передано нулевое количество товаров')
    @pytest.mark.add
    def test_add_count_zero(self, uuid):
        product = format_data(uuid=uuid, product_id='5', size_id='3', count=0)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)

    @allure.feature(f'Добавление товара в корзину. {Api.url}/carts/add')
    @allure.title('При добавлении товара в корзину передано колчиичество товаров большее, чем допустимо')
    @pytest.mark.add
    def test_add_count_big_number(self, uuid):
        product = format_data(uuid=uuid, product_id='20', size_id='3', count=70000)
        r = Api.add_request(product)
        Assertions.status_code(r, 403)


class TestChange:

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение количества добавленного товара в корзину с параметрами типа int')
    @pytest.mark.change
    def test_change_count_int_values(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=int(add_product['product_id']), current_size_id=int(add_product['size_id']), total_count=5)
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 200)
        Assertions.change(r)
        r = Api.uuid_request(uuid)
        Assertions.upd_product_count_in_cart(r, product_upd)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение количества добавленного товара в корзину с параметрами типа str')
    @pytest.mark.change
    def test_change_count_str_values(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], total_count='5')
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 200)
        Assertions.change(r)
        r = Api.uuid_request(uuid)
        Assertions.upd_product_count_in_cart(r, product_upd)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение количества добавленного товара в корзину на такое же значение')
    @pytest.mark.change
    def test_change_count_self(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], total_count=add_product['count'])
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 200)
        Assertions.change(r)
        r = Api.uuid_request(uuid)
        Assertions.upd_product_count_in_cart(r, product_upd)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('При изменении количества добавленного товара в корзину передан некорректный id товара')
    @pytest.mark.change
    def test_change_count_different_product_id(self, uuid, add_product):
        product_upd = format_data(uuid=uuid, product_id='21', current_size_id=add_product['size_id'], total_count=1)
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('При изменении количества добавленного товара в корзину передан некорректный id размера')
    @pytest.mark.change
    def test_change_count_different_size_id(self, uuid, add_product):
        product_upd = format_data(uuid=uuid, product_id=add_product['product_id'], current_size_id=6, total_count=1)
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение количества добавленного товара в корзину на 0')
    @pytest.mark.change
    def test_change_count_zero(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], total_count=0)
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение количества добавленного товара в корзину на значение большее, чем допустимо')
    @pytest.mark.change
    def test_change_count_big_number(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], total_count=70000)
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение количества добавленного товара в корзину на отрицательное значение')
    @pytest.mark.change
    def test_change_count_negative_num(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], total_count=-2)
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение размера добавленного товара в корзину с параметрами типа int')
    @pytest.mark.change
    def test_change_size_int_values(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], updated_size_id=6)
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 200)
        Assertions.change(r)
        r = Api.uuid_request(uuid)
        Assertions.upd_product_size_in_cart(r, product_upd)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение размера добавленного товара в корзину с параметрами типа str')
    @pytest.mark.change
    def test_change_size_str_values(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], updated_size_id='6')
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 200)
        Assertions.change(r)
        r = Api.uuid_request(uuid)
        Assertions.upd_product_size_in_cart(r, product_upd)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение размера добавленного товара в корзину на тот же размер')
    @pytest.mark.change
    def test_change_size_self(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], updated_size_id=add_product['size_id'])
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('Изменение размера добавленного товара в корзину на несуществующий')
    @pytest.mark.change
    def test_change_size_invalid_size_id(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id=add_product['size_id'], updated_size_id='20')
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('При изменении размера добавленного товара в корзину передан некорректный id товара')
    @pytest.mark.change
    def test_change_size_different_product_id(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id='15', current_size_id=add_product['size_id'], updated_size_id='3')
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)

    @allure.feature(f'Изменение товара в корзине. {Api.url}/carts/change')
    @allure.title('При изменении размера добавленного товара в корзину передан некорректный текущий id размера')
    @pytest.mark.change
    def test_change_size_different_size_id(self, uuid, add_product):
        product_upd = format_data(
            uuid=uuid, product_id=add_product['product_id'], current_size_id='5', updated_size_id='3')
        r = Api.change_request(product_upd)
        Assertions.status_code(r, 403)


class TestRemove:

    @allure.feature(f'Удаление товара из корзины. {Api.url}/carts/remove')
    @allure.title('Удаление добавленного товара из корзины с параметрами типа int')
    @pytest.mark.remove
    def test_remove_int_values(self, uuid, add_product):
        r = Api.remove_request(format_data(
            uuid=uuid, product_id=int(add_product['product_id']), size_id=int(add_product['size_id'])))
        Assertions.status_code(r, 200)
        Assertions.remove(r)
        r = Api.uuid_request(uuid)
        Assertions.cart_is_empty(r)

    @allure.feature(f'Удаление товара из корзины. {Api.url}/carts/remove')
    @allure.title('Удаление добавленного товара из корзины с параметрами типа str')
    @pytest.mark.remove
    def test_remove_str_values(self, uuid, add_product):
        r = Api.remove_request(
            format_data(uuid=uuid, product_id=add_product['product_id'], size_id=add_product['size_id']))
        Assertions.status_code(r, 200)
        Assertions.remove(r)
        r = Api.uuid_request(uuid)
        Assertions.cart_is_empty(r)

    @allure.feature(f'Удаление товара из корзины. {Api.url}/carts/remove')
    @allure.title('При удалении добавленного товара из корзины передан некорректный id товара')
    @pytest.mark.remove
    def test_remove_different_product_id(self, uuid, add_product):
        r = Api.remove_request(format_data(uuid=uuid, product_id='20', size_id=add_product['size_id']))
        Assertions.status_code(r, 403)

    @allure.feature(f'Удаление товара из корзины. {Api.url}/carts/remove')
    @allure.title('При удалении добавленного товара из корзины передан некорректный id размера')
    @pytest.mark.remove
    def test_remove_different_size_id(self, uuid, add_product):
        r = Api.remove_request(format_data(uuid=uuid, product_id=add_product['product_id'], size_id='5'))
        Assertions.status_code(r, 403)


class TestOrders:

    @allure.feature(f'Создание заказа. {Api.url}/orders')
    @allure.title('Создание заказа с пустой корзиной')
    @pytest.mark.orders
    def test_orders_with_empty_cart(self, uuid):
        r = Api.orders_request(uuid)
        Assertions.status_code(r, 200)
        Assertions.orders_with_empty_cart(r)

    @allure.feature(f'Создание заказа. {Api.url}/orders')
    @allure.title('Создание заказа из корзины с одним товаром')
    @pytest.mark.orders
    def test_orders_valid_values(self, uuid, add_product):
        r = Api.orders_request(uuid)
        Assertions.status_code(r, 200)
        Assertions.orders_valid_values(r)

    @allure.feature(f'Создание заказа. {Api.url}/orders')
    @allure.title('Проверка доступности корзины после создания заказа')
    @pytest.mark.orders
    def test_orders_used_cart_is_not_available(self, uuid, add_product):
        Api.orders_request(uuid)
        r = Api.add_request(format_data(uuid=uuid, product_id='12', size_id='4', count=1))
        Assertions.status_code(r, 422)

    @allure.feature(f'Создание заказа. {Api.url}/orders')
    @allure.title('При создании заказа передан несуществующий номер корзины')
    @pytest.mark.orders
    def test_orders_invalid_uuid(self):
        uuid = '65305a9a-def7-4c14-a6d1-3ee1507c4d6c'
        r = Api.orders_request(uuid)
        Assertions.status_code(r, 422)
