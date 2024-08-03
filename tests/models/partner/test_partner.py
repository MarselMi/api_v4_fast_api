import secrets
import json
import copy
import datetime as dt
import pytz

from api_v4.models.partner.utils import generate_partner_uid
from tests import client, session_maker
from typing import Dict
from httpx import Response

from sqlalchemy import select
from sqlalchemy.engine import Result

from core.hasher import PasswordHasher
from core.models import Partner


class TestPartner:
    date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
    hasher = PasswordHasher()
    data_types = [1, 0, -1, '', '1', 'x', None, True, False]
    user_data = {
        "password": "qwerty",
        "phone": "+7-918-123-45-67",
        "name": "TestUser",
        "avatar": "./home/admin/images/TestImage.jpeg",
        "telegram": "@test_telegram_user",
        "telegram_id": 123345567,
        "percent": 60,
        "referal_fees": 10,
        "last_activity": date.strftime('%Y-%m-%d %H:%M:%S').replace(' ', 'T'),
        "ip_reg": "127.0.0.1",
        "ip_auth": "127.0.0.2",
        "email_verified": 1,
        "user_is_active": 0,
        "referal": 1,
        "theme": "Темная",
        "role": "AFFILIATE_MAJOR",
        "is_staff": 1,
        "is_superuser": 1,
        "want_to_get_notifications": 0,
        "contest_nick": "TestUserContest",
        "contest_check": 1,
        "two_factor_auth": 1,
        "traffic_is_stopped": 1,
        "comment": "TestComment",
        "permanent": 0,
        "temporary_percent": 40,
        "temporary_start": date.strftime('%Y-%m-%d %H:%M:%S').replace(' ', 'T'),
        "temporary_end": date.strftime('%Y-%m-%d %H:%M:%S').replace(' ', 'T'),
        "old_percent": 22,
        "auto_pay": 1,
        "auto_pay_limit": 1,
        "past_auto_pay_limit": 1,
        "last_auto_pay": date.strftime('%Y-%m-%d %H:%M:%S').replace(' ', 'T'),
    }
    bad_user_data_fields = ["phone", "name", "avatar", "telegram", "telegram_id", "percent",
                            "referal_fees", "last_activity", "ip_reg", "ip_auth", "email_verified", "user_is_active",
                            "referal", "theme", "role", "is_staff", "is_superuser", "want_to_get_notifications",
                            "contest_nick", "contest_check", "two_factor_auth", "traffic_is_stopped", "comment",
                            "permanent", "temporary_percent", "temporary_start", "temporary_end", "old_percent",
                            "auto_pay", "auto_pay_limit", "past_auto_pay_limit", "last_auto_pay"]
    number_fields = ["telegram_id", "percent", "referal_fees", "referal", "traffic_is_stopped", "permanent",
                     "temporary_percent", "old_percent", "auto_pay", "auto_pay_limit", "past_auto_pay_limit"]

    async def test_get_empty_partner_set(self):
        response = client.get("/api/v4/partners/")
        data = json.loads(response.content)
        assert response.status_code == 200
        assert isinstance(data, list) is True
        assert len(data) == 0

    async def test_get_a_none_existent_partner(self):
        response = client.get("/api/v4/partners/1/")
        data = json.loads(response.content)
        assert response.status_code == 404
        assert data.get('detail') == 'Партнер с id 1 не найден'

    async def test_update_a_none_existent_partner(self):
        response = client.patch("/api/v4/partners/1/", json={
            "percent": 25
        })
        data = json.loads(response.content)
        assert response.status_code == 404
        assert data.get('detail') == 'Партнер с id 1 не найден'

    async def test_create_partner_without_required_fields(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={})
        assert response.status_code == 422
        response = client.post("/api/v4/partners/", json={
            "email": email
        })
        assert response.status_code == 422
        response = client.post("/api/v4/partners/", json={
            "password": "qwerty"
        })
        assert response.status_code == 422

    async def test_simple_partner_create(self):
        email, response, data = self.generate_response_post()
        date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        await self.assert_default_partner_fields(data, response, email, date)

    async def test_full_partner_create(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        user_data = copy.deepcopy(self.user_data)
        user_data["email"] = email
        response = client.post("/api/v4/partners/", json=user_data)
        data = json.loads(response.content)
        self.process_user_data(data, user_data)

    async def test_get_one_partner(self):
        user_data = copy.deepcopy(self.user_data)
        response = client.get("/api/v4/partners/2/")
        data = json.loads(response.content)
        assert response.status_code == 200
        self.process_user_data(data, user_data)

    async def test_unique_partner_email(self):
        email, response, _ = self.generate_response_post()
        assert response.status_code == 201
        response = client.post("/api/v4/partners/", json={
            "email": email,
            "password": "qwerty"
        })
        data = json.loads(response.content)
        assert response.status_code == 422
        assert data.get('detail') == 'Партнер с таким email уже зарегистрирован'

    async def test_check_partner_referal_field(self):
        email_parent, response, data = self.generate_response_post()
        parent_id = data.get("id")
        email_child = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={
            "email": email_child,
            "password": "qwerty",
            "referal": parent_id
        })
        data = json.loads(response.content)
        child_id = data.get("id")
        async with session_maker() as session:
            query = select(Partner).where(Partner.referal == parent_id)
            result: Result = await session.execute(query)
            child: Partner = result.scalars().all()[0]
            assert child.id == child_id
            query = select(Partner).where(Partner.id == child.referal)
            result: Result = await session.execute(query)
            parent: Partner = result.scalars().all()[0]
            assert parent.email == email_parent

    async def test_update_partner(self):
        email, response, data = self.generate_response_post()
        new_user_data = copy.deepcopy(self.user_data)
        response = client.patch(f"/api/v4/partners/{data.get('id')}/", json=new_user_data)
        data = json.loads(response.content)
        for key, value in new_user_data.items():
            if key == 'password':
                continue
            assert data[key] == value

    async def test_update_partner_with_empty_data(self):
        email, response, data = self.generate_response_post()
        response = client.patch(f"/api/v4/partners/{data.get('id')}/", json={})
        data = json.loads(response.content)
        date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        await self.assert_default_partner_fields(data, response, email, date, 200)

    async def test_update_partner_email(self):
        email, response, data = self.generate_response_post()
        new_email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.patch(f"/api/v4/partners/{data.get('id')}/", json={
            "email": new_email
        })
        data = json.loads(response.content)
        assert email != new_email
        assert data.get("email") == new_email

    async def test_update_partner_password(self):
        email, response, data = self.generate_response_post()
        client.patch(f"/api/v4/partners/{data.get('id')}/", json={
            "password": "ytrewq"
        })
        async with session_maker() as session:
            query = select(Partner).where(Partner.id == data.get('id'))
            result: Result = await session.execute(query)
            partner: Partner = result.scalars().all()[0]
            assert self.hasher.verify("ytrewq", partner.password) is True

    async def test_set_zero_to_partner_referal_field_via_create(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={
            "email": email,
            "password": "qwerty",
            "referal": 0
        })
        assert response.status_code == 422

    async def test_set_zero_to_partner_referal_field_via_update(self):
        _, _, data = self.generate_response_post()
        response = client.patch(f"/api/v4/partners/{data.get('id')}/", json={
            "referal": 0
        })
        assert response.status_code == 422

    async def test_set_not_existed_referal_id_to_partner_via_create(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={
            "email": email,
            "password": "qwerty",
            "referal": 9999
        })
        assert response.status_code == 422

    async def test_set_not_existed_referal_id_to_partner_via_update(self):
        _, _, data = self.generate_response_post()
        response = client.patch(f"/api/v4/partners/{data.get('id')}/", json={
            "referal": 9999
        })
        assert response.status_code == 422

    async def test_set_wrong_types_into_fields_via_partner_create(self):
        for key in self.data_types:
            for field in self.bad_user_data_fields:
                email = f"{secrets.token_hex(8)}@gmail.com"
                response = client.post("/api/v4/partners/", json={
                    "email": email,
                    "password": "qwerty",
                    key: field
                })
                assert response.status_code in (201, 422)

    async def test_set_wrong_types_into_fields_via_partner_update(self):
        _, _, data = self.generate_response_post()
        for key in self.data_types:
            for field in self.bad_user_data_fields:
                response = client.patch(f"/api/v4/partners/{data.get('id')}/", json={
                    key: field
                })
                assert response.status_code in (200, 422)

    async def test_update_partner_with_the_same_email(self):
        email, _, data = self.generate_response_post()
        response = client.patch(f"/api/v4/partners/{data.get('id')}/", json={
            "email": email
        })
        assert response.status_code == 200

    async def test_partner_password_wrong_length(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={
            "email": email,
            "password": ''.join(['x' for _ in range(5)])
        })
        assert response.status_code == 422
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={
            "email": email,
            "password": ''.join(['x' for _ in range(201)])
        })
        assert response.status_code == 422

    async def test_verify_partner_password(self):
        email, response, data = self.generate_response_post()
        async with session_maker() as session:
            partner = await session.get(Partner, data.get('id'))
        assert self.hasher.verify(password='qwerty', encoded=partner.password) is True

    async def test_set_negative_numbers_into_partner_numeric_fields_via_create(self):
        for key in self.number_fields:
            email = f"{secrets.token_hex(8)}@gmail.com"
            response = client.post("/api/v4/partners/", json={
                "email": email,
                "password": "qwerty",
                key: -1
            })
            assert response.status_code == 422

    async def test_set_negative_numbers_into_partner_numeric_fields_via_update(self):
        _, _, data = self.generate_response_post()
        for key in self.number_fields:
            response = client.patch(f"/api/v4/partners/{data.get('id')}/", json={
                key: -1
            })
            assert response.status_code == 422

    @staticmethod
    def generate_response_post():
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={
            "email": email,
            "password": "qwerty"
        })
        data = json.loads(response.content)
        return email, response, data

    @staticmethod
    def process_user_data(response_data: Dict, user_data: Dict):
        for key, value in user_data.items():
            if key == 'password':
                assert response_data.get(key) is None
                continue
            assert response_data.get(key) == value

    @staticmethod
    async def assert_default_partner_fields(
            data: Dict,
            response: Response,
            email: str,
            date: dt,
            status: int = 201):
        none_fields = ['phone', 'name', 'avatar', 'telegram', 'telegram_id', 'last_activity', 'ip_reg', 'ip_auth',
                       'contest_nick', 'comment', 'temporary_start', 'temporary_end', 'last_auto_pay', 'referal_fees',
                       'referal', 'password']
        null_fields = ['email_verified', 'two_factor_auth', 'traffic_is_stopped', 'auto_pay', 'auto_pay_limit']
        true_fields = ['user_is_active', 'want_to_get_notifications']
        false_fields = ['is_staff', 'is_superuser', 'contest_check']
        assert response.status_code == status
        assert data.get('email') == email
        assert data.get('create_date').split('.')[0][:-3] == date.strftime('%Y-%m-%dT%H:%M')
        assert data.get('create_date_day') == date.date().strftime('%Y-%m-%d')
        assert data.get('create_date_hour') == date.hour
        assert data.get('theme') == 'Светлая'
        assert data.get('role') == 'AFFILIATE_REGULAR'
        assert data.get('permanent') == 1
        assert data.get('percent') == 50
        assert data.get('old_percent') == 50
        for field in true_fields:
            assert data.get(field) is True
        for field in false_fields:
            assert data.get(field) is False
        for field in null_fields:
            assert data.get(field) == 0
        for field in none_fields:
            assert data.get(field) is None
        async with session_maker() as session:
            uid = await generate_partner_uid(data.get('id'), session)
            query = select(Partner).where(Partner.id == data.get('id'))
            result: Result = await session.execute(query)
            partner: Partner = result.scalars().all()[0]
            assert partner.uid == uid.uid


'''
1. Если, во время создания партнера, происходит 500 ошибка, партнер не создается, но id считается использованым
    (прим.: если партнер должен был создасться с id 1, после ощибки, он создастся с id 2)
'''
