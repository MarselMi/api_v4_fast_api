import secrets
import json
import copy
import datetime as dt
import pytz

from api_v4.models.partner.utils import generate_partner_uid
from tests import client, session_maker
from typing import Dict
from httpx import Response

from sqlalchemy import select
from sqlalchemy.engine import Result

from uuid import uuid4


class TestDailyStatistic:

    async def test_get_daily_statistic(self):
        email = f"{secrets.token_hex(8)}@gmail.com"
        response = client.post("/api/v4/partners/", json={
            "email": email,
            "password": "qwerty"
        })
        data = json.loads(response.content)
        for i in range(10):
            host_uuid = str(uuid4())
            client.post("/api/v4/hosts/", json={
                "uuid": host_uuid,
                "n_partner_id": data.get("id")
            })

        response = client.post("/api/v4/statistic/days/1/", json={})
        data = json.loads(response.content)
        print(data)