import copy

from core.hasher import PasswordHasher
from tests import client, session_maker

import json
import pytz
import uuid as uuid_gen

from sqlalchemy import select

import datetime as dt

from core.models import Client, Host

from tests.models.landing.test_landing import min_required_fields as landing_data
from tests.models.stream.test_stream import min_create_fields as stream_data
from tests.models.offer.offer_tests import min_correct_create_data as offer_data


dict_foreign_elements = {
    "partners": {"email": "sad@sda.sa", "password": "2222qwer"},
    "landings": landing_data,
    "streams": stream_data,
}


class TestClient:

    date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
    min_create_fields_without_uuid_email_phone = {
        "password": "qwerty123",
        "offer_id": 1,
        "card_first_six": "123456",
        "card_last_four": "1234",
    }

    async def test_get_list_clients(self):
        response = client.get("/api/v4/clients/")
        data = json.loads(response.content)

        assert response.status_code == 200
        assert isinstance(data, list) is True
        assert len(data) == 0

    async def test_get_client_not_exist(self):
        response = client.get("/api/v4/clients/1/")

        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "client с id 1 не найден"

    async def test_update_client_not_exist(self):
        response = client.patch("/api/v4/clients/1/", json={"password": "123456qwerty"})

        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "client с id 1 не найден"

    async def test_bad_create_client_without_offer_id(self):
        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        data.pop("offer_id")
        data.update({"email": "mail@ma.ru"})
        response = client.post("/api/v4/clients/", json=data)

        assert response.status_code == 422

    async def test_bad_create_client_without_email_phone(self):
        offer_create = copy.copy(offer_data)
        await self.create_objects_test(
            path_object="offers",
            create_data=offer_create,
        )

        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        response = client.post("/api/v4/clients/", json=data)

        assert (
            json.loads(response.content).get("detail")
            == "Одно из полей email / phone должно быть заполнено"
        )
        assert response.status_code == 422

    async def test_success_create_with_phone_without_uuid(self):
        for key, val in dict_foreign_elements.items():
            await self.create_objects_test(
                path_object=key,
                create_data=val,
            )

        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        data.update({"phone": "89991112233"})
        await self.actions_on_the_client(
            client_data=data, status_code=201, date_now=self.date
        )

    async def test_create_with_invalid_email_without_uuid(self):
        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        data.update({"email": "awd2233"})
        response = client.post("/api/v4/clients/", json=data)
        assert response.status_code == 422

    async def test_success_create_with_email_without_uuid(self):
        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        data.update({"email": "awd@ee.ru"})
        await self.actions_on_the_client(
            client_data=data, status_code=201, date_now=self.date
        )

    async def test_bad_create_with_not_unique_email_and_uuid(self):
        new_uuid = str(uuid_gen.uuid4())
        await self.create_objects_test(
            path_object="hosts",
            create_data={
                "uuid": new_uuid,
                "partner_id": 1,
                "stream_id": 1,
                "landing_id": 1,
            },
        )

        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        data.update({"email": "awd@ee.ru", "uuid": new_uuid})
        response = client.post("/api/v4/clients/", json=data)

        assert (
            json.loads(response.content).get("detail")
            == "Ошибка уникальности: awd@ee.ru offer: srting"
        )
        assert response.status_code == 422

    async def test_success_create_with_email_and_uuid(self):
        new_uuid = str(uuid_gen.uuid4())
        await self.create_objects_test(
            path_object="hosts",
            create_data={
                "uuid": new_uuid,
                "partner_id": 1,
                "stream_id": 1,
                "landing_id": 1,
            },
        )

        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        data.update({"email": "saqwer@ee.ru", "uuid": new_uuid})
        await self.actions_on_the_client(
            client_data=data, status_code=201, date_now=self.date
        )

    async def test_success_create_with_phone_and_uuid(self):
        new_uuid = str(uuid_gen.uuid4())
        await self.create_objects_test(
            path_object="hosts",
            create_data={
                "uuid": new_uuid,
                "partner_id": 1,
                "stream_id": 1,
                "landing_id": 1,
            },
        )

        data = copy.copy(self.min_create_fields_without_uuid_email_phone)
        data.update({"phone": "89993337766", "uuid": new_uuid})
        await self.actions_on_the_client(
            client_data=data, status_code=201, date_now=self.date
        )

    async def test_bad_auth_with_phone_not_exists(self):
        response = client.post(
            "/api/v4/clients/auth/",
            json={
                "phone": "89993337760",
                "password": "ssssss",
                "offer_id": 1,
            },
        )

        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail")
            == "Пользователь не зарегистрирован"
        )

    async def test_bad_auth_with_email_not_exists(self):
        response = client.post(
            "/api/v4/clients/auth/",
            json={
                "email": "masdfe@sss.ru",
                "password": "ssssss",
                "offer_id": 1,
            },
        )

        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail")
            == "Пользователь не зарегистрирован"
        )

    async def test_bad_auth_with_phone_other_offer(self):

        await self.create_objects_test(
            path_object="offers",
            create_data=offer_data,
        )

        response = client.post(
            "/api/v4/clients/auth/",
            json={
                "phone": "89993337766",
                "password": "asdfgg",
                "offer_id": 3,
            },
        )

        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail")
            == "Пользователь не зарегистрирован"
        )

    async def test_bad_auth_with_phone_wrong_password(self):

        response = client.post(
            "/api/v4/clients/auth/",
            json={
                "phone": "89993337766",
                "password": "asdfgg",
                "offer_id": 1,
            },
        )
        assert response.status_code == 400
        assert json.loads(response.content).get("detail") == "Неверный пароль"

    async def test_bad_auth_with_email_wrong_password(self):

        response = client.post(
            "/api/v4/clients/auth/",
            json={
                "email": "saqwer@ee.ru",
                "password": "asdfgg",
                "offer_id": 1,
            },
        )
        assert response.status_code == 400
        assert json.loads(response.content).get("detail") == "Неверный пароль"

    async def test_bad_auth_with_none_email_and_phone(self):

        response = client.post(
            "/api/v4/clients/auth/",
            json={
                "password": "asdfgg",
                "offer_id": 1,
            },
        )

        assert response.status_code == 400
        assert json.loads(response.content).get("detail") == "Введите email или телефон"

    async def test_bad_auth_with_none_password(self):

        response = client.post(
            "/api/v4/clients/auth/",
            json={
                "email": "saqwer@ee.ru",
                "offer_id": 1,
            },
        )

        assert response.status_code == 400
        assert json.loads(response.content).get("detail") == "Введите пароль"

    async def test_success_auth_with_email(self):
        await self.actions_on_the_client(
            auth=True,
            client_data={
                "email": "saqwer@ee.ru",
                "password": "qwerty123",
                "offer_id": 1,
            },
        )

    async def test_success_auth_with_phone(self):
        await self.actions_on_the_client(
            auth=True,
            client_data={
                "phone": "89993337766",
                "password": "qwerty123",
                "offer_id": 1,
            },
        )

    async def test_get_list_four_clients(self):
        response = client.get("/api/v4/clients/")
        data = json.loads(response.content)

        assert response.status_code == 200
        assert isinstance(data, list) is True
        assert len(data) == 4

    async def test_update_password(self):
        await self.actions_on_the_client(
            patch=4,
            client_data={"password": "1234567890"},
        )

    async def test_success_auth_with_changed_password(self):
        await self.actions_on_the_client(
            auth=True,
            client_data={
                "phone": "89993337766",
                "password": "1234567890",
                "offer_id": 1,
            },
        )

    @staticmethod
    async def create_objects_test(
        path_object: str,
        create_data: dict,
    ):
        response = client.post(f"/api/v4/{path_object}/", json=create_data)
        assert response.status_code == 201

    @staticmethod
    async def actions_on_the_client(
        client_data: dict,
        path: str = "/api/v4/clients/",
        auth: bool = False,
        patch: int | None = None,
        status_code: int = 200,
        date_now: dt = None,
        detail: str | None = None,
    ):
        if patch:
            request = client.patch(f"{path}{patch}", json=client_data)
        else:
            if auth:
                request = client.post(f"{path}auth/", json=client_data)
            else:
                request = client.post(path, json=client_data)

        assert request.status_code == status_code

        client_auth: dict = json.loads(request.content)
        hasher = PasswordHasher()

        async with session_maker() as session:
            query = select(Client).filter(Client.id == client_auth.get("id"))
            client_object: Client = await session.scalar(query)

            query = select(Host).filter(Host.id == client_auth.get("host_id"))
            host_object: Host = await session.scalar(query)

            if status_code == 201:
                assert client_auth.get("create_date").split(".")[0][
                    :-3
                ] == date_now.strftime("%Y-%m-%dT%H:%M")
                assert client_auth.get("create_date_day") == date_now.date().strftime(
                    "%Y-%m-%d"
                )
                assert client_auth.get("create_date_hour") == date_now.hour

            for key, value in client_data.items():
                if key == "password":
                    continue

                assert client_auth.get(key) == value

            if client_data.get("password"):
                assert hasher.verify(
                    password=client_data.get("password"), encoded=client_object.password
                )

            assert str(client_object.uuid) == client_auth.get("uuid")
            assert str(host_object.uuid) == client_auth.get("uuid")

            assert host_object.partner_id == client_object.n_partner_id
            assert host_object.n_partner_id == client_object.n_partner_id
            assert host_object.n_offer_id == client_object.offer_id
            assert host_object.stream_id == client_object.n_stream_id
            assert host_object.landing_id == client_object.n_landing_id
