import datetime as dt
import json
import copy

from tests import client


class TestInvoice:
    date = dt.datetime.now()
    operation_types = ["SUBSCRIPTION", "REBILL"]
    integer_fields = ["operation_id", "n_subscription_id", "n_client_id", "n_host_id", "n_partner_id",
                      "n_stream_id", "n_offer_id", "n_landing_id"]
    data_types = [None, [], {}, ()]

    async def test_simple_invoice_create(self):
        for ind in range(2):
            response = client.post("/api/v4/invoices/", json={
                "operation_type": self.operation_types[ind],
                "operation_id": 1
            })
            assert response.status_code == 201

    async def test_full_invoice_create(self):
        for ind in range(2):
            response = client.post("/api/v4/invoices/", json={
                "operation_type": self.operation_types[ind],
                "operation_id": 1,
                "n_subscription_id": 1,
                "n_client_id": 1,
                "n_host_id": 1,
                "n_partner_id": 1,
                "n_stream_id": 1,
                "n_offer_id": 1,
                "n_landing_id": 1,
            })
            assert response.status_code == 201

    async def test_create_invoice_without_operation_type(self):
        response = client.post("/api/v4/invoices/", json={
            "operation_id": 1
        })
        assert response.status_code == 422

    async def test_create_invoice_without_operation_id(self):
        response = client.post("/api/v4/invoices/", json={
            "operation_type": "SUBSCRIPTION"
        })
        assert response.status_code == 422

    async def test_create_invoice_with_wrong_types_in_operation_type(self):
        for key in self.data_types:
            response = client.post("/api/v4/invoices/", json={
                "operation_type": key,
                "operation_id": 1
            })
            assert response.status_code == 422

    async def test_create_invoice_with_wrong_types_in_operation_id(self):
        for key in self.data_types:
            response = client.post("/api/v4/invoices/", json={
                "operation_type": "REBILL",
                "operation_id": key
            })
            assert response.status_code == 422

    async def test_create_invoice_with_wrong_string_in_operation_type_field(self):
        response = client.post("/api/v4/invoices/", json={
            "operation_type": "RANDOM",
            "operation_id": 1
        })
        assert response.status_code == 422

    async def test_invoice_operation_type_depends_on_register(self):
        response = client.post("/api/v4/invoices/", json={
            "operation_type": "subscription",
            "operation_id": 1
        })
        assert response.status_code == 422

    async def test_create_invoice_with_wrong_data_types(self):
        fields = copy.copy(self.integer_fields)
        fields.pop(0)
        for key in fields:
            for value in [[], {}, (), '', 'x']:
                response = client.post("/api/v4/invoices/", json={
                    "operation_type": "REBILL",
                    "operation_id": 1,
                    key: value
                })
                assert response.status_code == 422

    async def test_set_negative_number_or_null_into_invoice_operation_id_field(self):
        for value in [0, -1]:
            response = client.post("/api/v4/invoices/", json={
                "operation_type": "REBILL",
                "operation_id": value
            })
            assert response.status_code == 422

    async def test_set_negative_numbers_into_invoice_integer_fields(self):
        for key in self.integer_fields:
            response = client.post("/api/v4/invoices/", json={
                "operation_type": "REBILL",
                "operation_id": 1,
                key: -1
            })
            assert response.status_code == 422

    async def test_get_invoices(self):
        client.post("/api/v4/invoices/", json={
            "operation_type": "SUBSCRIPTION",
            "operation_id": 1
        })
        response = client.get("/api/v4/invoices/")
        data = json.loads(response.content)
        assert response.status_code == 200
        assert isinstance(data, list) is True
        assert len(data) > 0

    async def test_get_invoice_by_id(self):
        response = client.get("/api/v4/invoices/1/")
        assert response.status_code == 200

    async def test_get_nonexistent_invoice_by_id(self):
        response = client.get("/api/v4/invoices/9999/")
        assert response.status_code == 404

    async def test_invoice_create_date_writes_correctly(self):
        response = client.post("/api/v4/invoices/", json={
            "operation_type": "SUBSCRIPTION",
            "operation_id": 1
        })
        data = json.loads(response.content)
        date = data.get("create_date")
        date = dt.datetime.strptime(date.split('.')[0], "%Y-%m-%dT%H:%M:%S")
        assert date.date() == self.date.date()
        assert date.hour == self.date.hour
