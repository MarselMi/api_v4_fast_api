import copy

from tests import client, session_maker
import json

from core.models import LandingElement

from tests.models.offer.offer_tests import TYPES_OBJECT


class TestLandingElement:
    async def test_get_land_elements_not_exist(self):
        response = client.get("/api/v4/landingelements/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    async def test_update_land_element_not_exist(self):
        response = client.patch(
            "/api/v4/landingelements/1/", json={"elements": "some text"}
        )
        assert response.status_code == 404
        assert (
            json.loads(response.content).get("detail")
            == "land_element с id 1 не найден"
        )

    async def test_get_land_element_path_not_int(self):
        response = client.get("/api/v4/landingelements/ssss/")
        assert response.status_code == 422

    async def test_create_land_element_with_invalid_fields(self):
        dict_fields = copy.copy(TYPES_OBJECT)
        del dict_fields["datetime"]
        for field, value in dict_fields.items():
            if field not in ["str", "str_none", "email", "domain", "None"]:
                response = client.post(
                    "/api/v4/landingelements/", json={"elements": value}
                )
                assert response.status_code == 422

    async def test_create_land_element_with_valid_fields(self):
        dict_fields = copy.copy(TYPES_OBJECT)
        del dict_fields["datetime"]
        for field, value in dict_fields.items():
            if field in ["str", "str_none", "email", "domain", "None"]:
                response = client.post(
                    "/api/v4/landingelements/", json={"elements": value}
                )
                assert response.status_code == 201

                landing_element = json.loads(response.content)
                assert landing_element.get("elements") == value

                async with session_maker() as session:
                    res = await session.get(LandingElement, landing_element.get("id"))
                    assert res.elements == value

    async def test_get_land_element(self):
        response = client.get("/api/v4/landingelements/1/")
        assert response.status_code == 200
        assert json.loads(response.content).get("id") == 1

    async def test_get_land_elements(self):
        response = client.get("/api/v4/landingelements/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

    async def test_update_land_element_with_invalid_fields(self):
        dict_fields = copy.copy(TYPES_OBJECT)
        del dict_fields["datetime"]
        for field, value in dict_fields.items():
            if field not in ["str", "str_none", "email", "domain", "None"]:
                response = client.patch(
                    "/api/v4/landingelements/1/", json={"elements": value}
                )
                assert response.status_code == 422

    async def test_update_land_element_with_valid_fields(self):
        new_value = "new value example {'sss': 33}"
        landing_elements = json.loads(client.get("/api/v4/landingelements/").content)
        for i in range(len(landing_elements)):
            response = client.patch(
                f"/api/v4/landingelements/{i + 1}/", json={"elements": new_value}
            )
            assert response.status_code == 200
            assert json.loads(response.content).get("elements") == new_value

            async with session_maker() as session:
                res = await session.get(LandingElement, i + 1)
                assert res.elements == new_value
