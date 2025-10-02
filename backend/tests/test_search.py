###
# Test that search routes return correct items for the sample data
###
from fastapi.testclient import TestClient


def test_get_physicians_no_filter(test_client: TestClient):
    response = test_client.get("/physicians")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "physician_id" in data[0]


def test_get_physicians_filter_by_state(test_client: TestClient):
    response = test_client.get("/physicians?state=CA")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for physician in data:
        assert physician["state"] == "CA"


def test_get_physicians_filter_by_specialty(test_client: TestClient):
    response = test_client.get("/physicians?specialty=Cardiology")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for physician in data:
        assert physician["specialty"] == "Cardiology"


def test_get_physicians_filter_by_state_and_specialty(test_client: TestClient):
    response = test_client.get("/physicians?state=NY&specialty=Oncology")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # there are no matching in sample data


def test_get_messages_no_filter(test_client: TestClient):
    response = test_client.get("/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "message_id" in data[0]


def test_get_messages_filter_by_physician(test_client: TestClient):
    response = test_client.get("/messages?physician_id=101")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for message in data:
        assert message["physician_id"] == 101


def test_get_messages_filter_by_start_date(test_client: TestClient):
    response = test_client.get("/messages?start_date=2024-01-15T00:00:00")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for message in data:
        assert message["timestamp"] >= "2025-01-15T00:00:00"


def test_get_messages_filter_by_end_date(test_client: TestClient):
    response = test_client.get("/messages?end_date=2025-09-15T00:00:00")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for message in data:
        assert message["timestamp"] <= "2025-09-15T23:59:59"


def test_get_messages_filter_by_date_range(test_client: TestClient):
    response = test_client.get(
        "/messages?start_date=2024-01-10T00:00:00&end_date=2025-09-12T23:59:59"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for message in data:
        assert "2024-01-10T00:00:00" <= message["timestamp"] <= "2025-09-12T23:59:59"
