from sqlalchemy.orm import selectinload
from sqlalchemy import select

from core.models import Stream

from tests import client, session_maker
from sqlalchemy.engine import Result
import datetime as dt
import pytz

import json
import copy
from tests.models.offer.offer_tests import TYPES_OBJECT

from tests.models.postback.postback_test import (
    min_create_fields as postback_create_data,
)
from tests.models.landing.test_landing import min_required_fields as landing_create
from tests.models.offer.offer_tests import min_correct_create_data as offer_create
from tests.models.prelanding.test_prelanding import (
    min_required_fields as prelanding_create,
)


full_create = {
    "name": TYPES_OBJECT.get("str"),
    "offer_id": TYPES_OBJECT.get("int"),
    "landing_id": TYPES_OBJECT.get("int"),
    "partner_id": TYPES_OBJECT.get("int"),
    "manager_id": TYPES_OBJECT.get("int"),
    "prelanding_id": TYPES_OBJECT.get("int"),
    "postback_id": TYPES_OBJECT.get("list_positive_int"),
    "yandex_id": TYPES_OBJECT.get("str"),
    "yandex_metric": TYPES_OBJECT.get("str"),
    "google_analytics": TYPES_OBJECT.get("str"),
    "top_mail_ru": TYPES_OBJECT.get("str"),
    "facebook_pixel": TYPES_OBJECT.get("str"),
    "vk_counter": TYPES_OBJECT.get("str"),
    "tiktok_pixel": TYPES_OBJECT.get("str"),
    "landingelement_data": TYPES_OBJECT.get("str"),
}
min_create_fields = {
    "name": TYPES_OBJECT.get("str"),
    "offer_id": TYPES_OBJECT.get("int"),
    "landing_id": TYPES_OBJECT.get("int"),
    "partner_id": TYPES_OBJECT.get("int"),
}

int_fields = ["offer_id", "landing_id", "partner_id", "manager_id", "prelanding_id"]
str_fields = [
    "name",
    "yandex_id",
    "google_analytics",
    "yandex_metric",
    "top_mail_ru",
    "facebook_pixel",
    "vk_counter",
    "tiktok_pixel",
    "link",
]
list_int_fields = ["postback_id"]
create_data_fields = ["created_date", "created_day", "created_hour"]
change_data_fields = ["change_date", "change_date_day", "change_date_hour"]


class TestStream:

    async def test_get_streams_not_exist(self):
        response = client.get("/api/v4/streams/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    async def test_update_stream_not_exist(self):
        response = client.patch("/api/v4/streams/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "stream с id 1 не найден"

    async def test_get_stream_not_exist(self):
        response = client.get("/api/v4/streams/1/")
        assert response.status_code == 404
        assert json.loads(response.content).get("detail") == "stream с id 1 не найден"

    async def test_get_stream_path_not_int(self):
        response = client.get("/api/v4/streams/ssss/")
        assert response.status_code == 422

    async def test_create_stream_without_required_fields(self):
        for field, value in min_create_fields.items():
            response = client.post("/api/v4/streams/", json={field: value})
            assert response.status_code == 422

    async def test_create_stream_with_zero_int_fields(self):
        copy_data = copy.copy(full_create)
        await self.create_partner(email="1_partner@mail.ru", password="qwertyu")
        await self.create_manager(email="1_manager@mail.ru", password="qwertyu")
        await self.create_offer(data=offer_create)
        await self.create_postback(data=postback_create_data)
        await self.create_landing(data=landing_create)
        await self.create_prelanding(data=prelanding_create)

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=0,
            valid_field=1,
        )

    async def test_create_stream_with_negative_int_fields(self):
        copy_data = copy.copy(full_create)

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=-1,
            valid_field=1,
        )

    async def test_create_stream_with_invalid_list_int(self):
        copy_data = copy.copy(full_create)

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=[-1],
            valid_field=1,
        )
        await self.create_stream_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=["aa"],
            valid_field=1,
        )
        await self.create_stream_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=[0],
            valid_field=1,
        )
        await self.create_stream_with_change_fields(
            create_data=copy_data,
            list_change_fields=int_fields,
            status_code=422,
            invalid_field=[2.3],
            valid_field=1,
        )

    async def test_create_stream_with_not_exist_manager_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["manager_id"] = 9999

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="manager с id 9999 не найден",
        )

    async def test_create_stream_with_not_exist_partner_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["partner_id"] = 9999

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="partner с id 9999 не найден",
        )

    async def test_create_stream_with_not_exist_landing_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["landing_id"] = 9999

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="landing с id 9999 не найден",
        )

    async def test_create_stream_with_not_exist_offer_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["offer_id"] = 9999

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="offer с id 9999 не найден",
        )

    async def test_create_stream_with_not_exist_prelanding_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["prelanding_id"] = 9999

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="prelanding с id 9999 не найден",
        )

    async def test_create_stream_with_not_exist_postback_foreign_key(self):
        copy_data = copy.copy(full_create)
        copy_data["postback_id"] = [1, 9999]

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            status_code=424,
            detail="postback с id 9999 не найден",
        )

    async def test_success_create_stream(self):

        copy_data = copy.copy(full_create)

        await self.create_stream_with_change_fields(
            create_data=copy_data,
            status_code=201,
            success_create=True,
        )

    async def test_int_fields_invalid_update(self):
        update_data = copy.copy(full_create)

        await self.update_stream(
            update_data=update_data,
            status_code=422,
            fields_list=int_fields,
            invalid_fields=["example", 2.3, {"s": 2}, [1, 3]],
            valid_field=1,
        )

    async def test_str_fields_invalid_update(self):
        update_data = copy.copy(full_create)

        await self.update_stream(
            update_data=update_data,
            status_code=422,
            fields_list=str_fields,
            invalid_fields=[1, 2.3, {"s": 2}, [1, 3]],
            valid_field="example",
        )

    async def test_list_int_fields_invalid_update(self):
        update_data = copy.copy(full_create)

        await self.update_stream(
            update_data=update_data,
            status_code=422,
            fields_list=list_int_fields,
            invalid_fields=[1, 2.3, {"s": 2}, ["1.4", 3], "example"],
            valid_field=[1],
        )

    async def test_success_upgrade_stream(self):
        for i in range(3):
            await self.create_partner(
                email=f"{i+2}_partner@mail.ru", password="qwertyu"
            )
            await self.create_manager(
                email=f"{i+2}_manager@mail.ru", password="qwertyu"
            )

        postback_create_data["name"] = "new_name"
        await self.create_postback(data=postback_create_data)

        full_create["manager_id"] = 3
        full_create["partner_id"] = 3
        full_create["postback_id"] = [1, 2]

        await self.update_stream(
            update_data=full_create,
            status_code=200,
        )

    @staticmethod
    async def create_postback(data: dict):
        response = client.post("/api/v4/postbacks/", json=data)
        assert response.status_code == 201

    @staticmethod
    async def create_landing(data: dict):
        response = client.post("/api/v4/landings/", json=data)
        assert response.status_code == 201

    @staticmethod
    async def create_prelanding(data: dict):
        response = client.post("/api/v4/prelandings/", json=data)
        assert response.status_code == 201

    @staticmethod
    async def create_offer(data: dict):
        response = client.post("/api/v4/offers/", json=data)
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
    async def create_stream_with_change_fields(
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
                        "/api/v4/streams/", json=copy_create_data_dict
                    )
                    copy_create_data_dict[field] = valid_field
                else:
                    response = client.post(
                        "/api/v4/streams/", json=copy_create_data_dict
                    )
                assert response.status_code == status_code

                if detail:
                    assert json.loads(response.content).get("detail") == detail
        else:
            response = client.post("/api/v4/streams/", json=copy_create_data_dict)
            assert response.status_code == status_code
            if detail:
                assert json.loads(response.content).get("detail") == detail

        if success_create:
            stream_response = json.loads(response.content)
            stream_id = stream_response.get("id")
            async with session_maker() as session:
                query = (
                    select(Stream)
                    .options(selectinload(Stream.postback_id))
                    .filter(Stream.id == stream_id)
                )
                db_result = await session.scalar(query)
                for key, val in create_data.items():
                    if key == "postback_id":
                        for i in range(len(stream_response.get("postback_id"))):
                            assert db_result.__dict__.get("postback_id")[
                                i
                            ].id == stream_response.get("postback_id")[i].get("id")
                    else:
                        assert db_result.__dict__.get(key) == stream_response.get(key)

                assert db_result.__dict__.get("created_date").strftime(
                    "%Y-%m-%dT%H:%M"
                ) == date.strftime("%Y-%m-%dT%H:%M")
                assert db_result.__dict__.get("created_day").strftime(
                    "%Y-%m-%d"
                ) == date.date().strftime("%Y-%m-%d")
                assert int(db_result.__dict__.get("created_hour")) == int(date.hour)

    @staticmethod
    async def update_stream(
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
                    response = client.patch("/api/v4/streams/1/", json=update_data)
                    update_data[field] = valid_field

                    assert response.status_code == status_code
                    if detail:
                        assert json.loads(response.content).get("detail") == detail
        else:
            response = client.patch("/api/v4/streams/1/", json=update_data)
            assert response.status_code == status_code

            stream_response = json.loads(response.content)
            stream_id = stream_response.get("id")

            async with session_maker() as session:
                query = (
                    select(Stream)
                    .options(selectinload(Stream.postback_id))
                    .filter(Stream.id == stream_id)
                )
                db_result = await session.scalar(query)

                for key, val in update_data.items():
                    if key == "postback_id":
                        assert len(db_result.postback_id) == len(val)
                        for i in range(len(val)):
                            assert db_result.postback_id[i].id == stream_response.get(
                                "postback_id"
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
