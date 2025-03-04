from app.config import get_db_url, get_auth_data
from app.users.core import get_password_hash, verify_password, create_access_token

from app.users.req_schemas import ProfileAddRequest, ProfileUpdateRequest
from jose import jwt as jose_jwt

import re
import pytest
from datetime import datetime, timedelta, timezone

def test_get_db_url_returns_correct_format():
    """Проверяем, что функция формирования URL для БД возвращает строку с нужным префиксом"""
    db_url = get_db_url()

    assert isinstance(db_url, str)
    assert db_url.startswith("postgresql+asyncpg://")

    for key in ['@', ':', '/']:
        assert key in db_url

def test_get_auth_data_contains_required_keys():
    """Проверяем, что конфигурация аутентификации содержит необходимые ключи"""
    auth_data = get_auth_data()

    assert isinstance(auth_data, dict)
    assert "secret_key" in auth_data
    assert "algorithm" in auth_data

def test_password_hashing():
    """Проверяем, что хэширование изменяет исходный пароль"""
    password = "TestPassword123"
    hashed = get_password_hash(password)

    assert isinstance(hashed, str)
    assert hashed != password

def test_verify_password_success():
    """Проверяем, что verify_password возвращает True для корректного пароля"""
    password = "TestPassword123"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed)

def test_verify_password_failure():
    """Проверяем, что verify_password возвращает False для неверного пароля"""
    password = "TestPassword123"
    wrong_password = "WrongPassword456"
    hashed = get_password_hash(password)

    assert not verify_password(wrong_password, hashed)

def test_create_and_decode_access_token():
    """Проверяем создание access-токена и его декодирование без зависимости от внешних сервисов"""
    data = {"sub": "100"}
    token = create_access_token(data)
    auth_data = get_auth_data()

    decoded = jose_jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])

    assert decoded["sub"] == "100"

    exp = decoded.get("exp")
    assert exp is not None
    if isinstance(exp, (int, float)):
        expire_time = datetime.fromtimestamp(exp, tz=timezone.utc)
        assert expire_time > datetime.now(timezone.utc)
    else:
        expire_time = datetime.fromisoformat(exp)
        assert expire_time > datetime.now(timezone.utc)

def test_profile_add_request_valid_phone_number():
    """Проверяем, что валидатор для phone_number принимает корректное значение"""
    valid_data = {
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "status": "active",
        "phone_number": "+71234567890",
        "birth_date": datetime.now().isoformat()
    }
    profile = ProfileAddRequest(**valid_data)

    assert profile.phone_number == "+71234567890"

def test_profile_add_request_invalid_phone_number():
    """Проверяем, что валидатор для phone_number выбрасывает ошибку для некорректного формата"""
    invalid_data = {
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "status": "active",
        "phone_number": "71234567890",  # отсутствует +
        "birth_date": datetime.now().isoformat()
    }
    with pytest.raises(ValueError) as excinfo:
        ProfileAddRequest(**invalid_data)

    assert re.search(r'Номер телефона должен начинаться с "\+"', str(excinfo.value))

def test_profile_update_request_phone_number_validator_valid():
    """Проверяем, что валидатор в схеме обновления профиля принимает корректное значение"""
    valid_update = {"phone_number": "+79876543210"}
    update_request = ProfileUpdateRequest(**valid_update)

    assert update_request.phone_number == "+79876543210"

def test_profile_update_request_phone_number_validator_invalid():
    """Проверяем, что валидатор в схеме обновления профиля отклоняет некорректное значение"""
    invalid_update = {"phone_number": "9876543210"}
    with pytest.raises(ValueError) as excinfo:
        ProfileUpdateRequest(**invalid_update)

    assert "Номер телефона должен начинаться с" in str(excinfo.value)