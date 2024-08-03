import copy

from core.hasher import PasswordHasher
from tests import client, session_maker

import json
import pytz

from sqlalchemy import select

import datetime as dt

from core.models import Client, Subscription

from tests.models.landing.test_landing import min_required_fields as landing_data
from tests.models.stream.test_stream import min_create_fields as stream_data
from tests.models.offer.offer_tests import min_correct_create_data as offer_data


class TestSubscriptions:
    date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))
    min_create_required_fields = {
        "tarif_name": "qwerty123",
        "tarif_sum": 1.0,
        "period": 1,
    }

    async def test_get_list_subscriptions(self):
        response = client.get("/api/v4/subscriptions/")
        data = json.loads(response.content)

        assert response.status_code == 200
        assert isinstance(data, list) is True
        assert len(data) == 0

    async def test_get_subscription_not_exist(self):
        response = client.get("/api/v4/subscriptions/1/")

        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail")
            == "subscription с id 1 не найден"
        )

    async def test_update_subscription_not_exist(self):
        response = client.patch(
            "/api/v4/subscriptions/1/", json={"tarif_name": "123456qwerty"}
        )

        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail")
            == "subscription с id 1 не найден"
        )

    async def test_bad_create_subscription_without_required_field(self):
        data = copy.copy(self.min_create_required_fields)
        data.pop("period")
        response = client.post("/api/v4/subscriptions/", json=data)

        assert response.status_code == 422

    async def test_success_create(self):

        await self.actions_on_the_subscription(
            client_data=self.min_create_required_fields,
            status_code=201,
            date_now=self.date,
        )

    @staticmethod
    async def actions_on_the_subscription(
        client_data: dict,
        path: str = "/api/v4/subscriptions/",
        patch: int | None = None,
        status_code: int = 200,
        date_now: dt = None,
        detail: str | None = None,
    ):
        if patch:
            request = client.patch(f"{path}{patch}", json=client_data)
        else:
            request = client.post(path, json=client_data)

        assert request.status_code == status_code

        response: dict = json.loads(request.content)

        if status_code == 201:
            assert response.get("create_date").split(".")[0][:-3] == date_now.strftime(
                "%Y-%m-%dT%H:%M"
            )
            assert response.get("create_date_day") == date_now.date().strftime(
                "%Y-%m-%d"
            )
            assert response.get("create_date_hour") == date_now.hour

            async with session_maker() as session:
                query = select(Subscription).filter(
                    Subscription.id == response.get("id")
                )
                db_object: Subscription = await session.scalar(query)

                assert db_object

        for key, value in client_data.items():
            assert response.get(key) == value
