from sqlalchemy.orm import selectinload
from starlette.testclient import TestClient
from sqlalchemy import select
from core.models import Prelanding, Partner
from tests import client, session_maker

from sqlalchemy.engine import Result

from httpx import Response

import secrets
import json
import copy
import datetime as dt
import pytz
from tests.models.offer.offer_tests import TYPES_OBJECT


status_choice = ["Активный", "Отключен", "Удален"]
type_choice = ["Публичный", "Приватный"]
correct_full_fields = {
    "offer_id": TYPES_OBJECT.get("int"),
    "name": TYPES_OBJECT.get("str"),
    "description": TYPES_OBJECT.get("str"),
    "screenshot": TYPES_OBJECT.get("str"),
    "status": "Активный",
    "type": "Публичный",
    "private_partners": TYPES_OBJECT.get("list_positive_int"),
}
min_required_fields = {
    "name": correct_full_fields.get("name"),
    "screenshot": correct_full_fields.get("screenshot"),
    "offer_id": correct_full_fields.get("offer_id"),
}
str_fields = ["name", "screenshot", "description", "status", "type"]
int_fields = ["offer_id"]
list_int_fields = ["private_partners"]
offer_create_data = {
    "name": TYPES_OBJECT.get("str"),
    "rebill": TYPES_OBJECT.get("float"),
    "trial": TYPES_OBJECT.get("int"),
    "payments_periodicity": TYPES_OBJECT.get("int"),
    "main_domain": TYPES_OBJECT.get("domain"),
}
valid_update_data = {
    "offer_id": 2,
    "name": "new_value",
    "description": "new_value",
    "screenshot": "new_value",
    "status": "Активный",
    "type": "Приватный",
    "private_partners": [1, 2],
}


class TestPrelanding:
    async def test_get_prelandings_not_exist(self):
        response = client.get("/api/v4/prelandings/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    async def test_update_prelanding_not_exist(self):
        response = client.patch("/api/v4/prelandings/1/")
        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail") == "prelanding с id 1 не найден"
        )

    async def test_get_prelanding_not_exist(self):
        response = client.get("/api/v4/prelandings/1/")
        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail") == "prelanding с id 1 не найден"
        )

    async def test_get_prelanding_path_not_int(self):
        response = client.get("/api/v4/prelandings/ssss/")
        assert response.status_code == 422

    async def test_create_prelanding_without_required_fields(self):
        for field, value in correct_full_fields.items():
            response = client.post("/api/v4/prelandings/", json={field: value})
            assert response.status_code == 422

    async def test_create_prelanding_with_zero_and_negative_int_fields(self):
        await self.create_prelanding_with_change_fields(
            create_data=correct_full_fields,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=0,
            valid_field=1,
        )

        await self.create_prelanding_with_change_fields(
            create_data=correct_full_fields,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=-1,
            valid_field=1,
        )

    async def test_create_prelanding_with_zero_and_negative_int_list(self):
        await self.create_prelanding_with_change_fields(
            create_data=correct_full_fields,
            list_change_fields=list_int_fields,
            status_code=422,
            invalid_field=[0],
            valid_field=[1],
        )
        await self.create_prelanding_with_change_fields(
            create_data=correct_full_fields,
            list_change_fields=list_int_fields,
            status_code=422,
            invalid_field=[-1],
            valid_field=[1],
        )

    async def test_create_prelanding_with_not_exist_offer_foreign_key(self):
        await self.create_prelanding_with_change_fields(
            create_data=min_required_fields,
            status_code=424,
            detail="offer с id 1 не найден",
        )

    async def test_create_prelanding_with_not_exist_partners(self):
        create_data = copy.copy(min_required_fields)

        offer_create = client.post("/api/v4/offers/", json=offer_create_data)
        assert offer_create.status_code == 201

        create_data["private_partners"] = [1]
        await self.create_prelanding_with_change_fields(
            create_data=create_data,
            status_code=424,
            detail="partner с id 1 не найден",
        )

    async def test_success_create_prelanding(self):
        partner_create = client.post(
            "/api/v4/partners/",
            json={"email": "example@mail.ru", "password": "qwerty123"},
        )
        assert partner_create.status_code == 201

        create_data = copy.copy(correct_full_fields)

        await self.create_prelanding_with_change_fields(
            create_data=create_data,
            status_code=201,
            success_create=True,
        )

    async def test_int_fields_invalid_update(self):
        update_data = copy.copy(correct_full_fields)

        await self.update_prelanding(
            update_data=update_data,
            status_code=422,
            fields_list=int_fields,
            invalid_fields=["example", 2.3, {"s": 2}, [1, 3]],
            valid_field=1,
        )

    async def test_str_fields_invalid_update(self):
        update_data = copy.copy(correct_full_fields)

        await self.update_prelanding(
            update_data=update_data,
            status_code=422,
            fields_list=str_fields,
            invalid_fields=[1, 2.3, {"s": 2}, [1, 3]],
            valid_field="example",
        )

    async def test_list_int_fields_invalid_update(self):
        update_data = copy.copy(correct_full_fields)

        await self.update_prelanding(
            update_data=update_data,
            status_code=422,
            fields_list=list_int_fields,
            invalid_fields=[1, 2.3, {"s": 2}, ["1.4", 3], "example"],
            valid_field=[1],
        )

    async def test_success_upgrade_prelanding(self):
        offer_create_response = client.post("/api/v4/offers/", json=offer_create_data)
        assert offer_create_response.status_code == 201

        land_el_create_response = client.post(
            "/api/v4/landingelements/", json={"elements": "ssssss"}
        )
        assert land_el_create_response.status_code == 201

        partner_create_response = client.post(
            "/api/v4/partners/",
            json={"email": "2_partner@mail.ru", "password": "qwerqwe"},
        )
        assert partner_create_response.status_code == 201

        await self.update_prelanding(
            update_data=valid_update_data,
            status_code=200,
        )

    async def test_success_get_prelandings_list(self):
        response_create_land = client.post(
            "/api/v4/prelandings/", json=min_required_fields
        )
        assert response_create_land.status_code == 201

        response = client.get("/api/v4/prelandings/")
        assert response.status_code == 200
        async with session_maker() as session:
            query = (
                select(Prelanding)
                .options(selectinload(Prelanding.private_partners))
                .order_by(Prelanding.id)
            )
            result: Result = await session.execute(query)
            landings = result.scalars().all()
            assert len(landings) == len(json.loads(response.content))

    async def test_success_get_prelanding(self):
        response_list = client.get("/api/v4/prelandings/")
        assert response_list.status_code == 200

        list_prelandings = json.loads(response_list.content)
        for land in list_prelandings:

            response_prelanding = client.get(f"/api/v4/prelandings/{land.get('id')}/")
            assert response_prelanding.status_code == 200

            land_from_api = json.loads(response_prelanding.content)
            async with session_maker() as session:
                query = (
                    select(Prelanding)
                    .options(selectinload(Prelanding.private_partners))
                    .filter(Prelanding.id == land.get("id"))
                )
                db_result = await session.scalar(query)
                assert db_result.id == land_from_api.get("id")

    @staticmethod
    async def create_prelanding_with_change_fields(
        create_data: dict = None,
        list_change_fields: list = None,
        status_code: int = 201,
        invalid_field: int | float | dict | list | str | bool = None,
        valid_field: int | float | dict | list | str | bool = None,
        detail: str = None,
        success_create=False,
    ):
        copy_create_data_dict = copy.copy(create_data)

        if list_change_fields:
            for field in list_change_fields:
                if invalid_field is not None:
                    copy_create_data_dict[field] = invalid_field
                    response = client.post(
                        "/api/v4/prelandings/", json=copy_create_data_dict
                    )
                    copy_create_data_dict[field] = valid_field
                else:
                    response = client.post(
                        "/api/v4/prelandings/", json=copy_create_data_dict
                    )
                if response.status_code == 422:
                    print("response = ", json.loads(response.content).get("detail"))
                assert response.status_code == status_code

                if detail:
                    assert json.loads(response.content).get("detail") == detail
        else:
            response = client.post("/api/v4/prelandings/", json=copy_create_data_dict)
            assert response.status_code == status_code
            if detail:
                assert json.loads(response.content).get("detail") == detail

        if success_create:
            prelanding_response = json.loads(response.content)
            preland_id = prelanding_response.get("id")
            async with session_maker() as session:
                query = (
                    select(Prelanding)
                    .options(selectinload(Prelanding.private_partners))
                    .filter(Prelanding.id == preland_id)
                )
                db_result = await session.scalar(query)
                for key, val in create_data.items():
                    if key == "private_partners":
                        for i in range(
                            len(prelanding_response.get("private_partners"))
                        ):
                            assert db_result.__dict__.get("private_partners")[
                                i
                            ].id == prelanding_response.get("private_partners")[i].get(
                                "id"
                            )
                    else:
                        assert db_result.__dict__.get(key) == prelanding_response.get(
                            key
                        )

    @staticmethod
    async def update_prelanding(
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
                    response = client.patch("/api/v4/prelandings/1/", json=update_data)
                    update_data[field] = valid_field
                    if response.status_code == 424:
                        print("invalid_values = ", invalid_values)
                        print("detail", json.loads(response.content).get("detail"))

                    assert response.status_code == status_code
                    if detail:
                        assert json.loads(response.content).get("detail") == detail
        else:
            response = client.patch("/api/v4/prelandings/1/", json=update_data)
            assert response.status_code == status_code

            prelanding_response = json.loads(response.content)
            preland_id = prelanding_response.get("id")

            async with session_maker() as session:
                query = (
                    select(Prelanding)
                    .options(selectinload(Prelanding.private_partners))
                    .filter(Prelanding.id == preland_id)
                )
                db_result = await session.scalar(query)

                for key, val in update_data.items():
                    if key == "private_partners":
                        assert len(db_result.private_partners) == len(val)
                        for i in range(len(val)):
                            assert db_result.private_partners[
                                i
                            ].id == prelanding_response.get("private_partners")[i].get(
                                "id"
                            )
                    else:
                        assert db_result.__dict__.get(key) == val
