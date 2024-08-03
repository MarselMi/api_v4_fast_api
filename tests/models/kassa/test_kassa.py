import random

from sqlalchemy import select

from core.models import Kassa

from tests import client, session_maker

import json
import copy
from tests.models.offer.offer_tests import TYPES_OBJECT


data_kassa_type_create = {
    "title": TYPES_OBJECT.get("str"),
    "link": TYPES_OBJECT.get("domain"),
}
data_organisation_create = {"title": TYPES_OBJECT.get("str"), "inn": "1234567890"}

data_full_create_kassa = {
    "number": TYPES_OBJECT.get("str"),
    "used_in_pay": TYPES_OBJECT.get("int"),
    "login": TYPES_OBJECT.get("str"),
    "password": TYPES_OBJECT.get("str"),
    "organisation_id": TYPES_OBJECT.get("int"),
    "kass_type": TYPES_OBJECT.get("str"),
}
data_min_create_kassa = {
    "login": data_full_create_kassa.get("login"),
    "password": data_full_create_kassa.get("password"),
    "organisation_id": data_full_create_kassa.get("organisation_id"),
    "kass_type": data_full_create_kassa.get("kass_type"),
}

int_fields = ["organisation_id"]
str_fields = ["number", "login", "password", "kass_type"]


class TestKassa:

    async def test_get_kassas_not_exist(self):
        response = client.get("/api/v4/kasses/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    async def test_update_kassa_not_exist(self):
        response = client.patch("/api/v4/kasses/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "kassa с id 1 не найден"

    async def test_get_kassa_not_exist(self):
        response = client.get("/api/v4/kasses/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "kassa с id 1 не найден"

    async def test_get_kassa_path_not_int(self):
        response = client.get("/api/v4/kasses/ssss/")
        assert response.status_code == 422

    async def test_create_without_required_fields(self):
        for field, value in data_min_create_kassa.items():
            response = client.post("/api/v4/kasses/", json={field: value})
            assert response.status_code == 422

    async def test_create_with_zero_int_fields(self):
        copy_data = copy.copy(data_full_create_kassa)
        await self.create_kassa_type(data_create=data_kassa_type_create)
        await self.create_organisation(data_create=data_organisation_create)

        await self.create_kassa_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=0,
            valid_field=1,
        )

    async def test_create_with_negative_int_fields(self):
        copy_data = copy.copy(data_full_create_kassa)

        await self.create_kassa_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=-1,
            valid_field=1,
        )

    async def test_create_with_not_exist_organisation_foreign_key(self):
        copy_data = copy.copy(data_full_create_kassa)
        copy_data["organisation_id"] = 9999

        await self.create_kassa_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="organisation с id 9999 не найден",
        )

    async def test_success_create(self):

        copy_data = copy.copy(data_full_create_kassa)

        await self.create_kassa_with_change_fields(
            create_data=copy_data,
            status_code=201,
            success_create=True,
        )

    async def test_int_fields_invalid_update(self):
        update_data = copy.copy(data_full_create_kassa)

        await self.update_kassa(
            update_data=update_data,
            status_code=422,
            fields_list=int_fields,
            invalid_fields=["example", 2.3, {"s": 2}, [1, 3]],
            valid_field=1,
        )

    async def test_str_fields_invalid_update(self):
        update_data = copy.copy(data_full_create_kassa)

        await self.update_kassa(
            update_data=update_data,
            status_code=422,
            fields_list=str_fields,
            invalid_fields=[1, 2.3, {"s": 2}, [1, 3]],
            valid_field="example",
        )

    async def test_success_upgrade_landing(self):
        for i in range(3):
            await self.create_organisation(data_create=data_organisation_create)

        full_create = copy.copy(data_full_create_kassa)
        full_create["organisation_id"] = 3
        full_create["number"] = "new_number"

        await self.update_kassa(
            update_data=full_create,
            status_code=200,
        )

    @staticmethod
    async def create_kassa_type(data_create: dict):
        data_create["title"] = f"{random.randint(1, 8)}_{data_create.get('title')}"
        response = client.post("/api/v4/kasstypes/", json=data_create)
        assert response.status_code == 201

    @staticmethod
    async def create_organisation(data_create: dict):
        data_create["title"] = f"{random.randint(1, 8)}_{data_create.get('title')}"
        response = client.post("/api/v4/organisations/", json=data_create)
        assert response.status_code == 201

    @staticmethod
    async def create_kassa_with_change_fields(
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
                        "/api/v4/kasses/", json=copy_create_data_dict
                    )
                    copy_create_data_dict[field] = valid_field
                else:
                    response = client.post(
                        "/api/v4/kasses/", json=copy_create_data_dict
                    )
                assert response.status_code == status_code

                if detail:
                    assert json.loads(response.content).get("detail") == detail
        else:
            response = client.post("/api/v4/kasses/", json=copy_create_data_dict)
            assert response.status_code == status_code
            if detail:
                assert json.loads(response.content).get("detail") == detail

        if success_create:
            postback_response = json.loads(response.content)
            postback_id = postback_response.get("id")
            async with session_maker() as session:
                query = select(Kassa).filter(Kassa.id == postback_id)
                db_result = await session.scalar(query)
                for key, val in create_data.items():
                    assert db_result.__dict__.get(key) == postback_response.get(key)

    @staticmethod
    async def update_kassa(
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
                    response = client.patch("/api/v4/kasses/1/", json=update_data)
                    update_data[field] = valid_field

                    assert response.status_code == status_code
                    if detail:
                        assert json.loads(response.content).get("detail") == detail
        else:
            response = client.patch("/api/v4/kasses/1/", json=update_data)
            assert response.status_code == status_code

            kassa_response = json.loads(response.content)
            kassa_id = kassa_response.get("id")

            async with session_maker() as session:
                query = select(Kassa).filter(Kassa.id == kassa_id)
                db_result = await session.scalar(query)

                for key, val in update_data.items():
                    assert db_result.__dict__.get(key) == val
