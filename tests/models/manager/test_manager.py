import secrets
import json
import copy
import datetime as dt
import pytz
from sqlalchemy.orm import selectinload

from tests import client, session_maker
from typing import Dict
from httpx import Response

from sqlalchemy import select
from sqlalchemy.engine import Result

from core.hasher import PasswordHasher
from core.models import Manager, Partner


class TestManager:
    date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
    hasher = PasswordHasher()
    data_types = [1, 0, -1, "", "1", "x", None, True, False]
    user_data = {
        "password": "qwerty",
        "phone": "+7-918-123-45-67",
        "name": "TestUser",
        "avatar": "./home/admin/images/TestImage.jpeg",
        "telegram": "@test_telegram_user",
        "telegram_id": 123345567,
        "percent": 60,
        "email_verified": 1,
        "user_is_active": 0,
        "role": "AFFILIATE_MAJOR",
        "can_edit_offers": 1,
        "can_pay": 1,
        "partners_id": [1],
    }
    bad_user_data_fields = [
        "phone",
        "name",
        "avatar",
        "telegram",
        "telegram_id",
        "percent",
        "email_verified",
        "user_is_active",
        "role",
        "can_edit_offers",
        "can_pay",
        "partners_id",
    ]
    number_fields = [
        "telegram_id",
        "percent",
        "telegram_id",
        "create_date_hour",
        "email_verified",
        "user_is_active",
        "change_date_hour",
        "can_edit_offers",
        "can_pay",
    ]

    async def test_get_empty_manager_set(self):
        response = client.get("/api/v4/managers/")
        data = json.loads(response.content)
        assert response.status_code == 200
        assert isinstance(data, list) is True
        assert len(data) == 0

    async def test_get_a_none_existent_manager(self):
        response = client.get("/api/v4/managers/1/")
        data = json.loads(response.content)
        assert response.status_code == 404
        assert data.get("detail") == "manager с id 1 не найден"

    async def test_update_a_none_existent_manager(self):
        response = client.patch("/api/v4/managers/1/", json={"percent": 25})
        data = json.loads(response.content)
        assert response.status_code == 404
        assert data.get("detail") == "manager с id 1 не найден"

    async def test_create_manager_without_required_fields(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/managers/", json={})
        assert response.status_code == 422
        response = client.post("/api/v4/managers/", json={"email": email})
        assert response.status_code == 422
        response = client.post("/api/v4/managers/", json={"password": "qwerty"})
        assert response.status_code == 422

    async def test_simple_manager_create(self):
        email, response, data = self.generate_response_post()
        date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        await self.assert_default_manager_fields(data, response, email, date)

    async def test_full_manager_create(self):
        email_partner, response_partner, partner_data = (
            self.generate_response_post_partner()
        )
        email = f"{secrets.token_hex(8)}@gmail.com"
        user_data = copy.copy(self.user_data)
        user_data["email"] = email
        response = client.post("/api/v4/managers/", json=user_data)
        data = json.loads(response.content)
        user_data["partners_id"] = [
            {"email": email_partner, "id": partner_data.get("id")}
        ]
        self.process_user_data(response_data=data, user_data=user_data)

    async def test_get_one_manager(self):

        user_data = copy.copy(self.user_data)

        async with session_maker() as session:
            query = select(Partner).where(Partner.id == 1)
            result: Result = await session.execute(query)
            partner: Partner = result.scalars().all()[0]

        user_data["partners_id"] = [{"email": partner.email, "id": partner.id}]

        response = client.get("/api/v4/managers/2/")
        data = json.loads(response.content)
        assert response.status_code == 200
        self.process_user_data(data, user_data)

    async def test_unique_manager_email(self):
        email, response, _ = self.generate_response_post()
        assert response.status_code == 201
        response = client.post(
            "/api/v4/managers/", json={"email": email, "password": "qwerty"}
        )
        data = json.loads(response.content)
        assert response.status_code == 422
        assert data.get("detail") == "manager с таким email уже зарегистрирован"

    async def test_check_manager_relation_partners_field(self):
        email_partner, response, data_partner = self.generate_response_post_partner()
        partner_id = data_partner.get("id")

        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post(
            "/api/v4/managers/",
            json={
                "email": email,
                "password": "qwerty",
                "partners_id": [partner_id],
            },
        )
        manager_data = json.loads(response.content)
        manager_id = manager_data.get("id")
        async with session_maker() as session:
            query = (
                select(Manager)
                .options(selectinload(Manager.partners_id))
                .filter(Manager.id == manager_id)
            )
            parent = await session.scalar(query)
            assert parent.id == manager_id

            query = select(Partner).where(Partner.id == parent.partners_id[0].id)
            result: Result = await session.execute(query)
            child: Partner = result.scalars().all()[0]
            assert child.email == email_partner

    async def test_update_manager(self):
        email, response, data = self.generate_response_post()
        new_user_data = copy.deepcopy(self.user_data)
        response = client.patch(
            f"/api/v4/managers/{data.get('id')}/", json=new_user_data
        )
        async with session_maker() as session:
            query = select(Partner).where(Partner.id == 1)
            result: Result = await session.execute(query)
            partner: Partner = result.scalars().all()[0]

        new_user_data["partners_id"] = [{"email": partner.email, "id": partner.id}]
        data = json.loads(response.content)
        for key, value in new_user_data.items():
            if key == "password":
                continue
            assert data[key] == value

    async def test_update_manager_with_empty_data(self):
        email, response, data = self.generate_response_post()
        response = client.patch(f"/api/v4/managers/{data.get('id')}/", json={})
        data = json.loads(response.content)
        date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        await self.assert_default_manager_fields(data, response, email, date, 200)

    async def test_update_manager_email(self):
        email, response, data = self.generate_response_post()
        new_email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.patch(
            f"/api/v4/managers/{data.get('id')}/", json={"email": new_email}
        )
        data = json.loads(response.content)
        assert email != new_email
        assert data.get("email") == new_email

    async def test_update_manager_password(self):
        email, response, data = self.generate_response_post()
        client.patch(f"/api/v4/managers/{data.get('id')}/", json={"password": "ytrewq"})
        async with session_maker() as session:
            query = select(Manager).where(Manager.id == data.get("id"))
            result: Result = await session.execute(query)
            manager: Manager = result.scalars().all()[0]
            assert self.hasher.verify("ytrewq", manager.password) is True

    async def test_set_zero_to_manager_relation_field_via_create(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post(
            "/api/v4/managers/",
            json={"email": email, "password": "qwerty", "partners_id": [0]},
        )
        assert response.status_code == 422

    async def test_set_zero_to_manager_relation_field_via_update(self):
        _, _, data = self.generate_response_post()
        response = client.patch(
            f"/api/v4/managers/{data.get('id')}/", json={"partners_id": [0]}
        )
        assert response.status_code == 422

    async def test_set_not_existed_partner_id_to_manager_via_create(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post(
            "/api/v4/managers/",
            json={"email": email, "password": "qwerty", "partners_id": [9999]},
        )
        assert response.status_code == 424
        assert (
            json.loads(response.content).get("detail") == "partner с id 9999 не найден"
        )

    async def test_set_not_existed_partner_id_to_manager_via_update(self):
        _, _, data = self.generate_response_post()
        response = client.patch(
            f"/api/v4/managers/{data.get('id')}/", json={"partners_id": [9999]}
        )
        assert response.status_code == 424
        assert (
            json.loads(response.content).get("detail") == "partner с id 9999 не найден"
        )

    async def test_set_wrong_types_into_fields_via_manager_create(self):
        for key in self.data_types:
            for field in self.bad_user_data_fields:
                email = f"{secrets.token_hex(8)}@gmail.com"
                response = client.post(
                    "/api/v4/managers/",
                    json={"email": email, "password": "qwerty", key: field},
                )
                assert response.status_code in (201, 422)

    async def test_set_wrong_types_into_fields_via_manager_update(self):
        _, _, data = self.generate_response_post()
        for key in self.data_types:
            for field in self.bad_user_data_fields:
                response = client.patch(
                    f"/api/v4/managers/{data.get('id')}/", json={key: field}
                )
                assert response.status_code in (200, 422)

    async def test_update_manager_with_the_same_email(self):
        email, _, data = self.generate_response_post()
        response = client.patch(
            f"/api/v4/managers/{data.get('id')}/", json={"email": email}
        )
        assert response.status_code == 200

    async def test_manager_password_wrong_length(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post(
            "/api/v4/managers/",
            json={"email": email, "password": "".join(["x" for _ in range(5)])},
        )
        assert response.status_code == 422
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post(
            "/api/v4/managers/",
            json={"email": email, "password": "".join(["x" for _ in range(201)])},
        )
        assert response.status_code == 422

    async def test_verify_manager_password(self):
        email, response, data = self.generate_response_post()
        async with session_maker() as session:
            manager = await session.get(Manager, data.get("id"))
        assert self.hasher.verify(password="qwerty", encoded=manager.password) is True

    async def test_set_negative_numbers_into_manager_numeric_fields_via_create(self):
        for key in self.number_fields:
            email = f"{secrets.token_hex(8)}@gmail.com"
            response = client.post(
                "/api/v4/managers/",
                json={"email": email, "password": "qwerty", key: -1},
            )
            assert response.status_code == 422

    async def test_set_negative_numbers_into_manager_numeric_fields_via_update(self):
        _, _, data = self.generate_response_post()
        for key in self.number_fields:
            response = client.patch(
                f"/api/v4/managers/{data.get('id')}/", json={key: -1}
            )
            assert response.status_code == 422

    @staticmethod
    def generate_response_post():
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post(
            "/api/v4/managers/", json={"email": email, "password": "qwerty"}
        )
        data = json.loads(response.content)
        return email, response, data

    @staticmethod
    def generate_response_post_partner():
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post(
            "/api/v4/partners/", json={"email": email, "password": "qwerty"}
        )
        data = json.loads(response.content)
        return email, response, data

    @staticmethod
    def process_user_data(response_data: dict, user_data: dict):
        for key, value in user_data.items():
            if key == "password":
                assert response_data.get(key) is None
                continue
            assert response_data.get(key) == value

    @staticmethod
    async def assert_default_manager_fields(
        data: Dict, response: Response, email: str, date: dt, status: int = 201
    ):
        none_fields = [
            "phone",
            "name",
            "avatar",
            "telegram",
            "telegram_id",
            "change_date",
            "change_date_day",
            "change_date_hour",
        ]
        null_fields = ["email_verified"]
        true_fields = ["user_is_active"]
        false_fields = ["email_verified", "can_pay", "can_edit_offers"]
        assert response.status_code == status
        assert data.get("email") == email
        assert data.get("create_date").split(".")[0][:-3] == date.strftime(
            "%Y-%m-%dT%H:%M"
        )
        assert data.get("create_date_day") == date.date().strftime("%Y-%m-%d")
        assert data.get("create_date_hour") == date.hour
        assert data.get("role") == "AFFILIATE_REGULAR"
        assert data.get("percent") == 50
        assert len(data.get("partners_id")) == 0
        for field in true_fields:
            assert data.get(field) is True
        for field in false_fields:
            assert data.get(field) == False or 0
        for field in null_fields:
            assert data.get(field) == 0
        for field in none_fields:
            assert data.get(field) is None
