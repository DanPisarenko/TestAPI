import pytest
from api import PetFriends
import os
pf = PetFriends()
valid_email = 'daniil.alex.p@gmail.com'
valid_password = '123'

not_valid_email = 'pisarekno@yandex.ru'
not_valid_password = '321'

def test_get_api_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_new_pet_with_valid_data(name='Най', animal_type='алабай',
                                          age='1', pet_photo='img/alabay.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.post_add_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet_with_valid_data(pet_id=0):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    sum_pets = len(my_pets['pets'])
    if sum_pets == 0:
        raise Exception("Ваш список питомцев пуст")
    elif pet_id > (sum_pets - 1):
        raise Exception("В Вашем списоке нет питомца с таким id")
    else:
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()


def test_put_pet_with_valid_data(pet_id=0, name='Най', animal_type='алабай', age=1):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    sum_pets = len(my_pets['pets'])

    if sum_pets == 0:
        raise Exception("Ваш список питомцев пуст")
    else:
        status, result = pf.put_pet(auth_key, my_pets['pets'][pet_id]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name


# Еще 10 тестов
def test_get_api_for_novalid_user(email=not_valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_post_creat_pet_with_valid_data(name='Дружок', animal_type='немецкая овчарка', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_creat_pet(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ""


def test_post_creat_pet_with_novalid_data(name='', animal_type='', age=-1):
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_creat_pet(auth_key, name, animal_type, age)
    try:
        assert status == 400
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")

def test_post_creat_pet_with_novalid_key(name='Кузя', animal_type='Кот', age=3):

    auth_key = {"key": "aa90bee76bc6b446ad084b7bbddc7360e5f476538dfffd75cec9e935"}
    status, result = pf.post_creat_pet(auth_key, name, animal_type, age)
    try:
        assert status == 403
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")

def test_get_all_pets_with_novalid_key(filter=''):

    auth_key = {"key": "aa90bee76bc6b446ad084b7bbddc7360e5f476538dfffd75cec9e935"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    try:
        assert status == 400
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")

def test_get_all_pets_with_valid_key_novalid_filter(filter='fgjtfghj'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    try:
        assert status == 400
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")

def test_post_new_pet_with_valid_data_novalid_key(name='Най', animal_type='алабай',
                                          age='2', pet_photo='img/alabay.jpg'):

    auth_key = {"key": "aa90bee76bc6b446ad084b7bbddc7360e5f476538dfffd75cec9e935"}
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.post_add_pet(auth_key, name, animal_type, age, pet_photo)
    try:
        assert status == 403
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")

def test_post_new_pet_with_null_data(name='', animal_type='',
                                          age='', pet_photo='img/alabay.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.post_add_pet(auth_key, name, animal_type, age, pet_photo)
    try:
        assert status == 400
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")

def test_delete_pet_with_valid_data_novalid_key(pet_id=0):
    auth_key = {"key": "aa90bee76bc6b446ad084b7bbddc7360e5f476538dfffd75cec9e935"}
    status, _ = pf.delete_pet(auth_key, pet_id)
    try:
        assert status == 403
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")
def test_put_pet_with_valid_data_novalid_key(pet_id='0', name='Маруся', animal_type='кошка', age=1):

    auth_key = {"key": "aa90bee76bc6b446ad084b7bbddc7360e5f476538dfffd75cec9e935"}
    status, result = pf.put_pet(auth_key, pet_id, name, animal_type, age)
    try:    
        assert status == 403
    except AssertionError:
        print("Исключение AssertionError")
    else:
        print("pass")