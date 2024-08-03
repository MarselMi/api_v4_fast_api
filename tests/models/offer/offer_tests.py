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

from core.models import Offer


TYPES_OBJECT = {
    "int": 1,
    "int_negative": -1,
    "float": 123.11,
    "float_negative": -299.22,
    "str": "srting",
    "str_none": "",
    "email": "example@mail.ru",
    "domain": "https://www.example.ru",
    "bool_true": True,
    "bool_false": False,
    "dict": {"dict": "dict"},
    "list_positive_int": [1],
    "list_negative_int": [-4],
    "list_str_int": ["sa"],
    "list_None": [None],
    "list_dict": [{"a": 2}],
    "None": None,
    "datetime": dt.datetime.now(tz=pytz.timezone("Europe/Moscow")),
}

full_correct_offer_create_data = {
    "name": TYPES_OBJECT.get("str"),
    "rebill": TYPES_OBJECT.get("float"),
    "trial": TYPES_OBJECT.get("int"),
    "payments_periodicity": TYPES_OBJECT.get("int"),
    "main_domain": TYPES_OBJECT.get("domain"),
    "logo": TYPES_OBJECT.get("str"),
    "geo": "ru",
    "deduction": TYPES_OBJECT.get("float"),
    "unexepted_traffic": TYPES_OBJECT.get("str"),
    "description": TYPES_OBJECT.get("str"),
    "screenshot": TYPES_OBJECT.get("str"),
    "status": "ACTIVE",
    "type": "PUBLIC",
    "author_pay": TYPES_OBJECT.get("float"),
    "subs_pay": TYPES_OBJECT.get("int"),
    "author_percent": TYPES_OBJECT.get("float"),
    "first_pay": TYPES_OBJECT.get("float"),
    "cash_register_number": TYPES_OBJECT.get("str"),
    "inn": TYPES_OBJECT.get("str"),
    "rebill_low": TYPES_OBJECT.get("float"),
    "rebill_low_period": TYPES_OBJECT.get("float"),
    "conf_data": TYPES_OBJECT.get("str"),
    "user_stats_reports": TYPES_OBJECT.get("str"),
    "payment_place": TYPES_OBJECT.get("str"),
    "payment_description": TYPES_OBJECT.get("str"),
    "currency": "RUR",
    "private_partners": TYPES_OBJECT.get("list_positive_int"),
    "manager_id": TYPES_OBJECT.get("int"),
}
min_correct_create_data = {
    "name": full_correct_offer_create_data.get("name"),
    "rebill": full_correct_offer_create_data.get("rebill"),
    "trial": full_correct_offer_create_data.get("trial"),
    "payments_periodicity": full_correct_offer_create_data.get("payments_periodicity"),
    "main_domain": full_correct_offer_create_data.get("main_domain"),
}
none_default_fields = [
    "manager_id",
    "logo",
    "geo",
    "unexepted_traffic",
    "description",
    "screenshot",
    "cash_register_number",
    "inn",
    "conf_data",
    "user_stats_reports",
    "payment_place",
    "payment_description",
    "change_date",
    "change_date_day",
    "change_date_hour",
]
false_default = [
    "author_pay",
    "subs_pay",
    "author_percent",
    "deduction",
    "rebill_low",
    "rebill_low_period",
]


class TestOffer:

    async def test_get_offers_list(self):
        response = client.get("/api/v4/offers/")
        data = json.loads(response.content)
        assert response.status_code == 200
        assert isinstance(data, list) is True
        assert len(data) == 0

    async def test_update_none_exist_offer(self):
        response = client.patch("/api/v4/offers/1/", json={"name": "example"})
        data = json.loads(response.content)
        assert response.status_code == 404
        assert data.get("detail") == "offer с id 1 не найден"

    async def test_create_offer_without_required_fields(self):
        response = client.post("/api/v4/offers/", json={})
        assert response.status_code == 422

        dict_required_fields = copy.copy(min_correct_create_data)
        without_required_fields = dict()

        for _ in range(len(min_correct_create_data) - 1):
            items = dict_required_fields.popitem()
            without_required_fields.update({items[0]: items[1]})
            response = client.post("/api/v4/offers/", json=without_required_fields)
            assert response.status_code == 422

        response = client.post("/api/v4/offers/", json=dict_required_fields)
        assert response.status_code == 422

    async def test_invalid_simple_offer_create(self):
        min_invalid_create_data = copy.copy(min_correct_create_data)
        min_invalid_create_data["rebill"] = TYPES_OBJECT.get("str")
        response = client.post("/api/v4/offers/", json=min_invalid_create_data)

        assert response.status_code == 422

    async def test_valid_simple_offer_create(self):
        response = client.post("/api/v4/offers/", json=min_correct_create_data)
        datetime = TYPES_OBJECT.get("datetime")
        await self.assert_created_offer(
            response=response,
            datetime=datetime,
            data=min_correct_create_data,
            none_default_fields=none_default_fields,
            false_default=false_default,
        )

    async def test_create_offer_with_bad_relationship(self):
        dict_with_rel = copy.copy(min_correct_create_data)
        dict_with_rel.update({"private_partners": [1, 2]})

        response = client.post("/api/v4/offers/", json=dict_with_rel)

        assert response.status_code == 424
        assert json.loads(response.content).get("detail") == "partner с id 1 не найден"

    async def test_create_offer_with_good_relationship(self):
        for i in range(2):
            partner_create = client.post(
                "/api/v4/partners/",
                json={"email": f"{i}example@vv.ru", "password": "123456qwe"},
            )
            assert partner_create.status_code == 201
        dict_with_rel = copy.copy(min_correct_create_data)
        dict_with_rel.update({"private_partners": [1, 2]})
        datetime = TYPES_OBJECT.get("datetime")

        response = client.post("/api/v4/offers/", json=dict_with_rel)
        await self.assert_created_offer(
            response=response,
            datetime=datetime,
            data=dict_with_rel,
            none_default_fields=none_default_fields,
            false_default=false_default,
        )

    async def test_create_offer_with_bad_foreign_key(self):
        dict_with_foreign = copy.copy(min_correct_create_data)
        dict_with_foreign.update({"manager_id": 1})

        response = client.post("/api/v4/offers/", json=dict_with_foreign)

        assert response.status_code == 424
        assert json.loads(response.content).get("detail") == "manager с id 1 не найден"

    async def test_create_offer_with_good_foreign_key(self):
        email = f"{secrets.token_hex(3)}@manager.ru"
        manager_create = client.post(
            "/api/v4/managers/",
            json={"email": email, "password": "123456qwe"},
        )
        assert manager_create.status_code == 201

        dict_with_foreign = copy.copy(min_correct_create_data)
        dict_with_foreign.update({"manager_id": 1})
        datetime = TYPES_OBJECT.get("datetime")

        response = client.post("/api/v4/offers/", json=dict_with_foreign)
        await self.assert_created_offer(
            response=response,
            datetime=datetime,
            data=dict_with_foreign,
            none_default_fields=none_default_fields[1:],
            false_default=false_default,
        )

    async def test_create_offer_with_good_relationship_and_foreign_key(self):
        dict_with_rel = copy.copy(min_correct_create_data)
        dict_with_rel.update({"private_partners": [1, 2], "manager_id": 1})
        datetime = TYPES_OBJECT.get("datetime")

        response = client.post("/api/v4/offers/", json=dict_with_rel)
        await self.assert_created_offer(
            response=response,
            datetime=datetime,
            data=dict_with_rel,
            none_default_fields=none_default_fields[1:],
            false_default=false_default,
        )

    async def test_crete_offer_by_invalid_inn(self):
        min_data_with_inn = copy.copy(min_correct_create_data)
        too_long_inn = "1234567890123"
        too_short_inn = "123456789"

        min_data_with_inn["inn"] = too_long_inn
        response = client.post("/api/v4/offers/", json=min_data_with_inn)
        assert response.status_code == 422

        min_data_with_inn["inn"] = too_short_inn
        response = client.post("/api/v4/offers/", json=min_data_with_inn)
        assert response.status_code == 422

    async def test_update_offer_by_valid_inn(self):

        response = client.patch("/api/v4/offers/1/", json={"inn": "1234567890"})
        # datetime = TYPES_OBJECT.get("datetime")
        assert response.status_code == 200
        # assert json.loads(response.content).get("change_date").split(".")[0][
        #     :-3
        # ] == datetime.strftime("%Y-%m-%dT%H:%M")
        # assert json.loads(response.content).get(
        #     "change_date_day"
        # ) == datetime.date().strftime("%Y-%m-%d")
        # assert json.loads(response.content).get("change_date_hour") == datetime.hour

        response = client.patch("/api/v4/offers/1/", json={"inn": "123456789012"})
        # datetime = TYPES_OBJECT.get("datetime")
        assert response.status_code == 200
        # assert json.loads(response.content).get("change_date").split(".")[0][
        #     :-3
        # ] == datetime.strftime("%Y-%m-%dT%H:%M")
        # assert json.loads(response.content).get(
        #     "change_date_day"
        # ) == datetime.date().strftime("%Y-%m-%d")
        # assert json.loads(response.content).get("change_date_hour") == datetime.hour

    async def test_good_get_offer_by_id(self):
        response = client.get("/api/v4/offers/1/")
        datetime = TYPES_OBJECT.get("datetime")
        status_code = response.status_code
        await self.assert_created_offer(
            response=response,
            datetime=datetime,
            none_default_fields=none_default_fields[1:],
            false_default=false_default,
            status_code=status_code,
        )

    async def test_good_get_list_offers(self):
        response = client.get("/api/v4/offers/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    async def test_invalid_update_offer_private_partners(self):
        invalid_params = copy.copy(TYPES_OBJECT)
        del invalid_params["list_positive_int"]
        del invalid_params["None"]
        del invalid_params["datetime"]
        for key in invalid_params:
            response = client.patch(
                "/api/v4/offers/1/", json={"private_partners": invalid_params[key]}
            )

            assert response.status_code == 422

    async def test_invalid_update_offer_float_fields(self):
        invalid_params = copy.copy(TYPES_OBJECT)
        del (
            invalid_params["float"],
            invalid_params["None"],
            invalid_params["datetime"],
            invalid_params["int"],
            invalid_params["bool_true"],
            invalid_params["bool_false"],
        )
        for key in invalid_params:
            response = client.patch(
                "/api/v4/offers/1/",
                json={
                    "deduction": invalid_params[key],
                    "rebill": invalid_params[key],
                    "author_percent": invalid_params[key],
                    "first_pay": invalid_params[key],
                    "rebill_low": invalid_params[key],
                    "rebill_low_period": invalid_params[key],
                },
            )

            assert response.status_code == 422

    async def test_invalid_update_int_fields(self):
        invalid_params = copy.copy(TYPES_OBJECT)
        del (
            invalid_params["None"],
            invalid_params["datetime"],
            invalid_params["int"],
            invalid_params["bool_true"],
            invalid_params["bool_false"],
        )
        for key in invalid_params:
            response = client.patch(
                "/api/v4/offers/1/",
                json={
                    "trial": invalid_params[key],
                    "payments_periodicity": invalid_params[key],
                    "author_pay": invalid_params[key],
                    "subs_pay": invalid_params[key],
                    "change_date_hour": invalid_params[key],
                    "manager_id": invalid_params[key],
                },
            )

            assert response.status_code == 422

    @staticmethod
    async def assert_created_offer(
        response: Response,
        datetime: dt,
        data: dict = None,
        none_default_fields: list = None,
        false_default: list = None,
        status_code: int = 201,
    ):
        assert response.status_code == status_code
        new_offer = json.loads(response.content)

        if data:
            for key in data:
                if key == "private_partners":
                    for i in range(2):
                        assert new_offer.get(key)[i] == {
                            "email": f"{i}example@vv.ru",
                            "id": i + 1,
                        }
                else:
                    async with session_maker() as session:
                        query = (
                            select(Offer)
                            .options(selectinload(Offer.private_partners))
                            .filter(Offer.id == new_offer.get("id"))
                        )
                        db_result = await session.scalar(query)

                        assert db_result.__dict__.get(key) == data.get(key)

        if none_default_fields:
            for field in none_default_fields:
                assert new_offer.get(field) is None

        if false_default:
            for field in false_default:
                assert new_offer.get(field) == False

        assert new_offer.get("create_date").split(".")[0][:-3] == datetime.strftime(
            "%Y-%m-%dT%H:%M"
        )
        assert new_offer.get("create_date_day") == datetime.date().strftime("%Y-%m-%d")
        assert new_offer.get("create_date_hour") == datetime.hour

        assert new_offer.get("currency") == "RUR"
        assert new_offer.get("type") == "Публичный"
        assert new_offer.get("status") == "Активный"
