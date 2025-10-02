###
# Test that classify routes return current items for the sample data
###

from fastapi.testclient import TestClient


def test_classify_message_not_found(test_client: TestClient):
    response = test_client.post("/classify/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


def test_classify_message_no_rules_matched(test_client: TestClient):
    # message 10153: Question about reimbursement and prior auth forms.
    response = test_client.post("/classify/10153")
    assert response.status_code == 200
    data = response.json()
    assert data["compliance_version"] == "v1"
    assert data["matched_rules"] == []


def test_classify_message_one_rule_matched(test_client: TestClient):
    # Message ID 10013: "Requesting patient samples for clinic use."
    response = test_client.post("/classify/10013")
    assert response.status_code == 200
    data = response.json()
    assert len(data["matched_rules"]) == 1
    rule = data["matched_rules"][0]
    assert rule["id"] == "R-004"
    assert "samples" in rule["matched_keywords"]
