from tests import client

import json
import pytz
from uuid import uuid4

import datetime as dt

from tests.models.landing.test_landing import min_required_fields as landing_data
from tests.models.stream.test_stream import min_create_fields as stream_data
from tests.models.offer.offer_tests import min_correct_create_data as offer_data

dict_for_create_foreign_elements = {
    "partners": {"password": "sqwert12", "email": "partners@sad.ww"},
    "managers": {"password": "sqwert12", "email": "managers@sad.ww"},
    "offers": offer_data,
    "landings": landing_data,
    "streams": stream_data,
}


class TestHost:
    date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow"))

    async def test_get_empty_hosts_set(self):
        response = client.get("/api/v4/hosts/")
        data = json.loads(response.content)

        assert response.status_code == 200

        assert isinstance(data, list) is True

        assert len(data) == 0

    async def test_host_simple_create(self):
        for key, val in dict_for_create_foreign_elements.items():
            await self.create_objects_test(
                path_object=key,
                create_data=val,
            )

        host_uuid = str(uuid4())
        response = client.post(
            "/api/v4/hosts/",
            json={
                "uuid": host_uuid,
                "partner_id": 1,
                "manager_id": 1,
                "stream_id": 1,
                "landing_id": 1,
            },
        )
        data = json.loads(response.content)
        assert response.status_code == 201
        assert data.get("uuid") == host_uuid
        assert (
            not all(
                [
                    data.get("partner_id"),
                    data.get("manager_id"),
                    data.get("stream_id"),
                    data.get("landing_id"),
                    data.get("country_id"),
                    data.get("os_id"),
                    data.get("browser_id"),
                    data.get("ref_domain_id"),
                    data.get("referrer_id"),
                    data.get("ipv4"),
                    data.get("utm_source"),
                    data.get("utm_medium"),
                    data.get("utm_campaign"),
                    data.get("utm_content"),
                    data.get("utm_term"),
                    data.get("sub_1"),
                    data.get("sub_2"),
                    data.get("sub_3"),
                    data.get("sub_4"),
                    data.get("sub_5"),
                    data.get("click_id"),
                ]
            )
            is True
        )

        assert (
            all(
                [
                    data.get("n_partner_id") == 1,
                    data.get("n_manager_id") == 1,
                    data.get("n_stream_id") == 1,
                    data.get("n_landing_id") == 1,
                    data.get("n_offer_id") == 1,
                    data.get("version") == 0,
                ]
            )
            is True
        )

        assert data.get("device_type") == "DESKTOP"

        assert data.get("create_date").split(".")[0][:-3] == self.date.strftime(
            "%Y-%m-%dT%H:%M"
        )
        assert data.get("create_date_day") == self.date.date().strftime("%Y-%m-%d")
        assert data.get("create_date_hour") == self.date.hour

    async def test_host_full_create(self):
        pass

    async def test_get_host(self):
        response = client.get("/api/v4/hosts/1/")
        data = json.loads(response.content)

        assert response.status_code == 200

        assert isinstance(data, dict)

        assert data.get("id") == 1

    async def test_get_hosts(self):
        for i in range(2):
            host_uuid = str(uuid4())
            client.post(
                "/api/v4/hosts/",
                json={
                    "uuid": host_uuid,
                    "partner_id": 1,
                    "manager_id": 1,
                    "stream_id": 1,
                    "landing_id": 1,
                },
            )
        response = client.get("/api/v4/hosts/")
        data = json.loads(response.content)

        assert response.status_code == 200

        assert isinstance(data, list)

        assert len(data) >= 2

    async def test_get_non_existent_host(self):
        response = client.get("/api/v4/hosts/999999/")
        data = json.loads(response.content)

        assert response.status_code == 404

        assert data.get("detail") == "Партнер с id 999999 не найден"

    async def test_update_get_non_existent_host(self):
        response = client.patch("/api/v4/hosts/999999/", json={"sub_5": "123"})
        data = json.loads(response.content)

        assert response.status_code == 404

        assert data.get("detail") == "Партнер с id 999999 не найден"

    async def test_host_simple_update(self):
        response = client.patch("/api/v4/hosts/1/", json={"sub_5": "123"})
        data = json.loads(response.content)

        assert response.status_code == 200

        assert isinstance(data, dict)

        assert data.get("sub_5") == "123"

    async def test_host_full_update(self):
        pass

    async def test_create_host_with_empty_body(self):
        response = client.post("/api/v4/hosts/")
        data = json.loads(response.content)
        msg = data.get("detail")
        print(data)

        assert response.status_code == 422

        assert isinstance(data, dict)

        assert isinstance(msg, list)

        assert msg[0].get("loc") == ["body"]

        assert msg[0].get("msg") == "Field required"

    async def test_create_host_with_wrong_data_types(self):
        pass

    async def test_update_host_with_wrong_data_types(self):
        pass

    @staticmethod
    async def create_objects_test(path_object: str, create_data: dict):
        response = client.post(f"/api/v4/{path_object}/", json=create_data)
        assert response.status_code == 201
