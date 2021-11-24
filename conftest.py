import pytest
import allure
from wiremock.server import WireMockServer
from tests.utils.api import Api
from tests.utils.assertions import Assertions


@allure.title('Создание новой корзины; Проверка отсутствия товаров в корзине')
@pytest.fixture(name='uuid')
def setup_create_cart():
    uuid = Api.get_uuid()
    r = Api.uuid_request(uuid)
    Assertions.cart_is_empty(r)
    return uuid


@allure.title('Добавление товара в корзину; Проверка наличия добавленного товара в корзине')
@pytest.fixture()
def add_product(uuid):
    product = {'uuid': uuid, 'product_id': '12', 'size_id': '4', 'count': 1}
    r = Api.add_request(product)
    Assertions.status_code(r, 200)
    Assertions.add(r)
    r = Api.uuid_request(uuid)
    Assertions.product_in_cart(r, product)
    return product


@allure.title('Запуск и остановка wiremock')
@pytest.fixture()
def wiremock():
    port = 8080
    wm = WireMockServer(port=port, root_dir='../mock')
    wm.start()
    with allure.step(f'wiremock запущен на порту {port}'):
        pass
    yield
    wm.stop()
    with allure.step('wiremock остановлен'):
        pass

