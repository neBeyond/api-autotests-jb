import allure
import pytest
from tests.utils.api import Api
from tests.utils.assertions import Assertions


class TestCartMethods:

    @allure.feature('Тестирование методов корзнины используя параметризацию @pytest.mark.parametrize()')
    @pytest.mark.skip(reason="требуется доработка для корректной работы тестов")
    @pytest.mark.parametrize('test_data, expected_values', [
        (
                {'uuid': Api.get_uuid(), 'product_id': 12, 'size_id': 4, 'count': 5},
                {'message': 'The product was added to the shopping cart.'}
        ),
        (
                {'uuid': Api.get_uuid(), 'product_id': '12', 'size_id': '4', 'count': '3'},
                {'message': 'The product was added to the shopping cart.'}
        ),
        (
                {'uuid': Api.get_uuid(), 'product_id': '90', 'count': '5'},
                {'message': 'The product was added to the shopping cart.'}
        ),
    ])
    def test_add_parametrized(self, test_data, expected_values):
        r = Api.add_request(test_data)
        Assertions.add(r)
        assert r.json()['notification']['message'] == expected_values['message']

    @allure.feature('Тестирование методов корзнины используя параметризацию @pytest.mark.parametrize()')
    @pytest.mark.skip(reason="требуется доработка для корректной работы тестов")
    @pytest.mark.parametrize('test_data, expected_values', [
        (
                {'uuid': Api.get_uuid(), 'product_id': 12, 'current_size_id': 4, 'total_count': 5},
                {'message': 'The item in the shopping cart has been changed.'}
        ),
        (
                {'uuid': Api.get_uuid(), 'product_id': '12', 'current_size_id': '4', 'total_count': '5'},
                {'message': 'The item in the shopping cart has been changed.'}
        ),
        (
                {'uuid': Api.get_uuid(), 'product_id': '12', 'current_size_id': '4', 'total_count': 1},
                {'message': 'The item in the shopping cart has been changed.'}
        ),
        (
                {'uuid': Api.get_uuid(), 'product_id': '12', 'current_size_id': '4', 'updated_size_id': '3'},
                {'message': 'The item in the shopping cart has been changed.'}
        ),
        (
                {'uuid': Api.get_uuid(), 'product_id': 12, 'current_size_id': 4, 'updated_size_id': 3},
                {'message': 'The item in the shopping cart has been changed.'}
        ),
    ])
    def test_change_parametrized(self, test_data, expected_values):
        Api.add_request({
            'uuid': test_data['uuid'],
            'product_id': test_data['product_id'],
            'size_id': test_data['current_size_id'],
            'count': 1})
        r = Api.change_request(test_data)
        Assertions.change(r)
        assert r.json()['notification']['message'] == expected_values['message']

    @allure.feature('Тестирование методов корзнины используя параметризацию @pytest.mark.parametrize()')
    @pytest.mark.skip(reason="требуется доработка для корректной работы тестов")
    @pytest.mark.parametrize('test_data, expected_values', [
        (
                {'uuid': Api.get_uuid(), 'product_id': 12, 'size_id': 4},
                {'message': 'The product is removed from the basket.'}
        ),
        (
                {'uuid': Api.get_uuid(), 'product_id': '12', 'size_id': '4'},
                {'message': 'The product is removed from the basket.'}
        ),
    ])
    def test_remove_parametrized(self, test_data, expected_values):
        Api.add_request({
            'uuid': test_data['uuid'],
            'product_id': test_data['product_id'],
            'size_id': test_data['size_id'],
            'count': 1})
        r = Api.remove_request(test_data)
        Assertions.remove(r)
        assert r.json()['notification']['message'] == expected_values['message']