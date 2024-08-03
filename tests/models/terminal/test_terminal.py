import random

from sqlalchemy import select

from core.models import Terminal, Organisation, Offer, Kassa, Paysystem, AcquBank

from tests import client, session_maker

import json
import copy
from tests.models.offer.offer_tests import TYPES_OBJECT
from tests.models.offer.offer_tests import min_correct_create_data as offer_create_data

kassa_create_data = {
    "login": TYPES_OBJECT.get("str"),
    "password": TYPES_OBJECT.get("str"),
    "organisation_id": TYPES_OBJECT.get("int"),
    "kass_type": TYPES_OBJECT.get("str"),
}
organisation_create_data = {"title": TYPES_OBJECT.get("str"), "inn": "1234567890"}
paysystem_create_data = {
    "code": TYPES_OBJECT.get("str"),
    "title": TYPES_OBJECT.get("str"),
}
acqu_create_data = {
    "code": TYPES_OBJECT.get("str"),
    "name": TYPES_OBJECT.get("str"),
    "title": TYPES_OBJECT.get("str"),
}

full_create_data = {
    "offer_id": TYPES_OBJECT.get("int"),
    "paysystem_id": TYPES_OBJECT.get("int"),
    "organisation_id": TYPES_OBJECT.get("int"),
    "kassa_id": TYPES_OBJECT.get("int"),
    "acqu_bank": TYPES_OBJECT.get("int"),
    "title": TYPES_OBJECT.get("str"),
    "paysystem_service_id": TYPES_OBJECT.get("str"),
    "paysystem_public_id": TYPES_OBJECT.get("str"),
    "paysystem_secret_key": TYPES_OBJECT.get("str"),
    "one_time_pay": TYPES_OBJECT.get("int"),
    "contains_rebills": TYPES_OBJECT.get("int"),
    "rebills": TYPES_OBJECT.get("int"),
    "paysystem_service_name": TYPES_OBJECT.get("str"),
    "status": TYPES_OBJECT.get("str"),
    "percent": TYPES_OBJECT.get("int"),
    "selected": TYPES_OBJECT.get("int"),
    "rebill_terminal_id": TYPES_OBJECT.get("int"),
    "currency": "RUR",
}
min_create_data = {
    "title": full_create_data.get("title"),
    "paysystem_service_id": full_create_data.get("paysystem_service_id"),
    "paysystem_public_id": full_create_data.get("paysystem_public_id"),
    "paysystem_secret_key": full_create_data.get("paysystem_secret_key"),
}
foreign_fields = [
    "offer_id",
    "paysystem_id",
    "organisation_id",
    "kassa_id",
    "acqu_bank",
]
int_fields = [
    "one_time_pay",
    "contains_rebills",
    "rebills",
    "percent",
    "selected",
    "rebill_terminal_id",
]
str_fields = [
    "title",
    "paysystem_service_id",
    "paysystem_public_id",
    "paysystem_secret_key",
    "paysystem_service_name",
    "status",
    "currency",
]


class TestTerminal:

    async def test_get_terminals_not_exist(self):
        response = client.get("/api/v4/terminals/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    async def test_update_terminal_not_exist(self):
        response = client.patch("/api/v4/terminals/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "terminal с id 1 не найден"

    async def test_get_terminal_not_exist(self):
        response = client.get("/api/v4/terminals/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "terminal с id 1 не найден"

    async def test_get_terminal_path_not_int(self):
        response = client.get("/api/v4/terminals/ssss/")
        assert response.status_code == 422

    async def test_create_without_required_fields(self):
        for field, value in min_create_data.items():
            response = client.post("/api/v4/terminals/", json={field: value})
            assert response.status_code == 422

    async def test_create_with_zero_foreign_fields(self):
        copy_data = copy.copy(full_create_data)

        await self.create_with_change_fields(
            create_data=copy_data,
            list_change_fields=foreign_fields,
            status_code=422,
            invalid_field=0,
            valid_field=1,
        )

    async def test_create_with_negative_foreign_fields(self):
        copy_data = copy.copy(full_create_data)

        await self.create_with_change_fields(
            create_data=copy_data,
            list_change_fields=foreign_fields,
            status_code=422,
            invalid_field=-1,
            valid_field=1,
        )

    async def test_create_with_negative_int_fields(self):
        copy_data = copy.copy(full_create_data)

        await self.create_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=-1,
            valid_field=1,
        )

    async def test_create_with_not_exist_organisation_foreign_key(self):

        await self.create_organisation(data_create=organisation_create_data)
        await self.create_acqu(data_create=acqu_create_data)
        await self.create_kassa(data_create=kassa_create_data)
        await self.create_paysystem(data_create=paysystem_create_data)
        await self.create_offer(data_create=offer_create_data)

        copy_data = copy.copy(full_create_data)
        copy_data["organisation_id"] = 9999

        await self.create_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="organisation с id 9999 не найден",
        )

    async def test_create_with_not_exist_offer_foreign_key(self):
        copy_data = copy.copy(full_create_data)
        copy_data["offer_id"] = 9999

        await self.create_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="offer с id 9999 не найден",
        )

    async def test_create_with_not_exist_kassa_foreign_key(self):
        copy_data = copy.copy(full_create_data)
        copy_data["kassa_id"] = 9999

        await self.create_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="kassa с id 9999 не найден",
        )

    async def test_create_with_not_exist_paysystem_foreign_key(self):
        copy_data = copy.copy(full_create_data)
        copy_data["paysystem_id"] = 9999

        await self.create_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="paysystem с id 9999 не найден",
        )

    async def test_create_with_not_exist_acqu_foreign_key(self):
        copy_data = copy.copy(full_create_data)
        copy_data["acqu_bank"] = 9999

        await self.create_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="acqu_bank с id 9999 не найден",
        )

    async def test_success_full_create(self):
        copy_data = copy.copy(full_create_data)

        await self.create_with_change_fields(
            create_data=copy_data,
            status_code=201,
            success_create=True,
        )

    async def test_success_min_create(self):

        copy_data = copy.copy(min_create_data)

        await self.create_with_change_fields(
            create_data=copy_data,
            status_code=201,
            success_create=True,
        )

    async def test_int_fields_invalid_update(self):
        update_data = copy.copy(full_create_data)

        await self.update_obj(
            update_data=update_data,
            status_code=422,
            fields_list=int_fields,
            invalid_fields=["example", 2.3, {"s": 2}, [1, 3]],
            valid_field=1,
        )

    async def test_str_fields_invalid_update(self):
        update_data = copy.copy(full_create_data)

        await self.update_obj(
            update_data=update_data,
            status_code=422,
            fields_list=str_fields,
            invalid_fields=[1, 2.3, {"s": 2}, [1, 3]],
            valid_field="example",
        )

    async def test_success_upgrade(self):
        for i in range(3):
            await self.create_organisation(
                data_create={
                    "title": f"{random.randint(0, 9)}_name",
                    "inn": "1234567890",
                }
            )

        full_create = copy.copy(full_create_data)
        full_create["organisation_id"] = 3
        full_create["title"] = "new_title"

        await self.update_obj(
            update_data=full_create,
        )

    @staticmethod
    async def create_with_change_fields(
        create_data: dict = None,
        list_change_fields: list = None,
        status_code: int = 201,
        invalid_field: int | float | dict | list | str | bool = None,
        valid_field: int | float | dict | list | str | bool = None,
        detail: str = None,
        success_create=False,
    ):
        copy_create_data_dict = create_data

        if list_change_fields:
            for field in list_change_fields:
                if invalid_field is not None:
                    copy_create_data_dict[field] = invalid_field
                    response = client.post(
                        "/api/v4/terminals/", json=copy_create_data_dict
                    )
                    copy_create_data_dict[field] = valid_field
                else:
                    response = client.post(
                        "/api/v4/terminals/", json=copy_create_data_dict
                    )
                assert response.status_code == status_code

                if detail:
                    assert json.loads(response.content).get("detail") == detail
        else:
            response = client.post("/api/v4/terminals/", json=copy_create_data_dict)
            assert response.status_code == status_code
            if detail:
                assert json.loads(response.content).get("detail") == detail

        if success_create:
            obj_response = json.loads(response.content)
            obj_id = obj_response.get("id")
            async with session_maker() as session:
                query = select(Terminal).filter(Terminal.id == obj_id)
                db_result = await session.scalar(query)
                for key, val in create_data.items():
                    assert db_result.__dict__.get(key) == obj_response.get(key)

    @staticmethod
    async def update_obj(
        update_data: dict = None,
        status_code: int = 200,
        detail: str = None,
        fields_list: list = None,
        invalid_fields: list = None,
        valid_field: int | dict | list | str | bool = None,
    ):

        if invalid_fields:
            for field in fields_list:
                for invalid_values in invalid_fields:
                    update_data[field] = invalid_values
                    response = client.patch("/api/v4/terminals/1/", json=update_data)
                    update_data[field] = valid_field

                    assert response.status_code == status_code
                    if detail:
                        assert json.loads(response.content).get("detail") == detail
        else:
            response = client.patch("/api/v4/terminals/1/", json=update_data)

            assert response.status_code == status_code

            obj_response = json.loads(response.content)
            obj_id = obj_response.get("id")
            async with session_maker() as session:
                db_result = await session.get(Terminal, obj_id)

                for key, val in update_data.items():
                    assert db_result.__dict__.get(key) == val

    @staticmethod
    async def create_kassa(data_create: dict):
        data_create["login"] = f"{random.randint(1, 8)}_{data_create.get('login')}"
        response = client.post("/api/v4/kasses/", json=data_create)
        assert response.status_code == 201

    @staticmethod
    async def create_organisation(data_create: dict):
        response = client.post("/api/v4/organisations/", json=data_create)
        assert response.status_code == 201

    @staticmethod
    async def create_paysystem(data_create: dict):
        data_create["title"] = f"{random.randint(1, 8)}_{data_create.get('title')}"
        response = client.post("/api/v4/paysystems/", json=data_create)
        assert response.status_code == 201

    @staticmethod
    async def create_offer(data_create: dict):
        data_create["name"] = f"{random.randint(1, 8)}_{data_create.get('title')}"
        response = client.post("/api/v4/offers/", json=data_create)
        assert response.status_code == 201

    @staticmethod
    async def create_acqu(data_create: dict):
        data_create["name"] = f"{random.randint(1, 8)}_{data_create.get('name')}"
        response = client.post("/api/v4/acqubanks/", json=data_create)
        assert response.status_code == 201
