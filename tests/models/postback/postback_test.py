from sqlalchemy.orm import selectinload
from sqlalchemy import select

from core.models import Postback

from tests import client, session_maker
from sqlalchemy.engine import Result
import datetime as dt
import pytz

import json
import copy
from tests.models.offer.offer_tests import TYPES_OBJECT


event_names = ["Активация", "Регистрация", "Ребилл", "Подписка", "Отписка"]
full_create = {
    "name": TYPES_OBJECT.get("str"),
    "postdata": TYPES_OBJECT.get("str"),
    "status": "Активный",
    "partner_id": TYPES_OBJECT.get("int"),
    "method": "GET",
    "event_id": TYPES_OBJECT.get("list_positive_int"),
    "link": TYPES_OBJECT.get("domain"),
    "manager_id": TYPES_OBJECT.get("int"),
}
min_create_fields = {
    "name": TYPES_OBJECT.get("str"),
    "link": TYPES_OBJECT.get("domain"),
    "partner_id": TYPES_OBJECT.get("int"),
    "method": "GET",
}

int_fields = ["partner_id", "manager_id"]
str_fields = ["name", "method", "link", "postdata", "status"]
list_int_fields = ["event_id"]
create_data_fields = ["created", "created_day", "created_hour"]
change_data_fields = ["change_date", "change_date_day", "change_date_hour"]


class TestPostback:

    async def test_get_postbacks_not_exist(self):
        response = client.get("/api/v4/postbacks/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    async def test_update_postback_not_exist(self):
        response = client.patch("/api/v4/postbacks/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "postback с id 1 не найден"

    async def test_get_postback_not_exist(self):
        response = client.get("/api/v4/postbacks/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "postback с id 1 не найден"

    async def test_get_postback_path_not_int(self):
        response = client.get("/api/v4/postbacks/ssss/")
        assert response.status_code == 422

    async def test_create_postback_without_required_fields(self):
        for field, value in min_create_fields.items():
            response = client.post("/api/v4/postbacks/", json={field: value})
            assert response.status_code == 422

    async def test_create_postback_with_zero_int_fields(self):
        copy_data = copy.copy(full_create)
        await self.create_partner(email="1_partner@mail.ru", password="qwertyu")
        await self.create_manager(email="1_manager@mail.ru", password="qwertyu")
        await self.create_events(event_list=event_names)

        await self.create_postback_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=0,
            valid_field=1,
        )

    async def test_create_postback_with_negative_int_fields(self):
        copy_data = copy.copy(full_create)

        await self.create_postback_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=-1,
            valid_field=1,
        )

    async def test_create_postback_with_invalid_list_int(self):
        copy_data = copy.copy(full_create)

        await self.create_postback_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=[-1],
            valid_field=1,
        )
        await self.create_postback_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=["aa"],
            valid_field=1,
        )
        await self.create_postback_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=[0],
            valid_field=1,
        )
        await self.create_postback_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=[2.3],
            valid_field=1,
        )

    async def test_create_postback_with_not_exist_manager_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["manager_id"] = 9999

        await self.create_postback_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="manager с id 9999 не найден",
        )

    async def test_create_postback_with_not_exist_partner_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["partner_id"] = 9999

        await self.create_postback_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="partner с id 9999 не найден",
        )

    async def test_create_postback_with_not_exist_event_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["event_id"] = [1, 2, 9999]

        await self.create_postback_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="event с id 9999 не найден",
        )

    async def test_success_create_postback(self):
        copy_data = copy.copy(full_create)

        await self.create_postback_with_change_fields(
            create_data=copy_data,
            status_code=201,
            success_create=True,
        )

    async def test_int_fields_invalid_update(self):
        update_data = copy.copy(full_create)

        await self.update_postback(
            update_data=update_data,
            status_code=422,
            fields_list=int_fields,
            invalid_fields=["example", 2.3, {"s": 2}, [1, 3]],
            valid_field=1,
        )

    async def test_str_fields_invalid_update(self):
        update_data = copy.copy(full_create)

        await self.update_postback(
            update_data=update_data,
            status_code=422,
            fields_list=str_fields,
            invalid_fields=[1, 2.3, {"s": 2}, [1, 3]],
            valid_field="example",
        )

    async def test_list_int_fields_invalid_update(self):
        update_data = copy.copy(full_create)

        await self.update_postback(
            update_data=update_data,
            status_code=422,
            fields_list=list_int_fields,
            invalid_fields=[1, 2.3, {"s": 2}, ["1.4", 3], "example"],
            valid_field=[1],
        )

    async def test_success_upgrade_landing(self):
        update_data = copy.copy(full_create)
        for i in range(3):
            await self.create_partner(
                email=f"{i+2}_partner@mail.ru", password="qwertyu"
            )
            await self.create_manager(
                email=f"{i+2}_manager@mail.ru", password="qwertyu"
            )

        update_data["manager_id"] = 3
        update_data["partner_id"] = 3
        update_data["event_id"] = [1, 2, 3, 4, 5]

        await self.update_postback(
            update_data=update_data,
            status_code=200,
        )

    @staticmethod
    async def create_events(event_list: list):
        for event in event_list:
            response = client.post("/api/v4/events/", json={"name": event})
            assert response.status_code == 201

    @staticmethod
    async def create_manager(email: str, password: str):
        response = client.post(
            "/api/v4/managers/",
            json={"email": email, "password": password},
        )
        assert response.status_code == 201

    @staticmethod
    async def create_partner(email: str, password: str):
        response = client.post(
            "/api/v4/partners/",
            json={"email": email, "password": password},
        )
        assert response.status_code == 201

    @staticmethod
    async def create_postback_with_change_fields(
        create_data: dict = None,
        list_change_fields: list = None,
        status_code: int = 201,
        invalid_field: int | float | dict | list | str | bool = None,
        valid_field: int | float | dict | list | str | bool = None,
        detail: str = None,
        success_create=False,
    ):

        date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        copy_create_data_dict = create_data

        if list_change_fields:
            for field in list_change_fields:
                if invalid_field is not None:
                    copy_create_data_dict[field] = invalid_field
                    response = client.post(
                        "/api/v4/postbacks/", json=copy_create_data_dict
                    )
                    copy_create_data_dict[field] = valid_field
                else:
                    response = client.post(
                        "/api/v4/postbacks/", json=copy_create_data_dict
                    )
                assert response.status_code == status_code

                if detail:
                    assert json.loads(response.content).get("detail") == detail
        else:
            response = client.post("/api/v4/postbacks/", json=copy_create_data_dict)
            assert response.status_code == status_code
            if detail:
                assert json.loads(response.content).get("detail") == detail

        if success_create:
            postback_response = json.loads(response.content)
            postback_id = postback_response.get("id")
            async with session_maker() as session:
                query = (
                    select(Postback)
                    .options(selectinload(Postback.event_id))
                    .filter(Postback.id == postback_id)
                )
                db_result = await session.scalar(query)
                for key, val in create_data.items():
                    if key == "event_id":
                        for i in range(len(postback_response.get("event_id"))):
                            assert db_result.__dict__.get("event_id")[
                                i
                            ].id == postback_response.get("event_id")[i].get("id")
                    else:
                        assert db_result.__dict__.get(key) == postback_response.get(key)

                assert db_result.__dict__.get("created").strftime(
                    "%Y-%m-%dT%H:%M"
                ) == date.strftime("%Y-%m-%dT%H:%M")
                assert db_result.__dict__.get("created_day").strftime(
                    "%Y-%m-%d"
                ) == date.date().strftime("%Y-%m-%d")
                assert int(db_result.__dict__.get("created_hour")) == int(date.hour)

    @staticmethod
    async def update_postback(
        update_data: dict = None,
        status_code: int = 200,
        detail: str = None,
        fields_list: list = None,
        invalid_fields: list = None,
        valid_field: int | dict | list | str | bool = None,
    ):
        date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        if invalid_fields:
            for field in fields_list:
                for invalid_values in invalid_fields:
                    update_data[field] = invalid_values
                    response = client.patch("/api/v4/postbacks/1/", json=update_data)
                    update_data[field] = valid_field

                    assert response.status_code == status_code
                    if detail:
                        assert json.loads(response.content).get("detail") == detail
        else:
            response = client.patch("/api/v4/postbacks/1/", json=update_data)
            assert response.status_code == status_code

            postback_response = json.loads(response.content)
            postback_id = postback_response.get("id")

            async with session_maker() as session:
                query = (
                    select(Postback)
                    .options(selectinload(Postback.event_id))
                    .filter(Postback.id == postback_id)
                )
                db_result = await session.scalar(query)

                for key, val in update_data.items():
                    if key == "event_id":
                        assert len(db_result.event_id) == len(val)
                        for i in range(len(val)):
                            assert db_result.event_id[i].id == postback_response.get(
                                "event_id"
                            )[i].get("id")
                    else:
                        assert db_result.__dict__.get(key) == val

                assert db_result.__dict__.get("change_date").strftime(
                    "%Y-%m-%dT%H:%M"
                ) == date.strftime("%Y-%m-%dT%H:%M")
                assert db_result.__dict__.get("change_date_day").strftime(
                    "%Y-%m-%d"
                ) == date.date().strftime("%Y-%m-%d")
                assert int(db_result.__dict__.get("change_date_hour")) == int(date.hour)
