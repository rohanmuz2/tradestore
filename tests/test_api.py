def test_create_and_get_trade(client, valid_trade):
    response = client.post("/trades", json=valid_trade)
    assert response.status_code == 201
    assert response.json()["operation"] == "created"
    assert response.json()["trade"]["expired"] is False

    found = client.get("/trades/T1")
    assert found.status_code == 200
    assert found.json()["counterparty_id"] == "CP-1"


def test_same_version_replaces_trade(client, valid_trade):
    client.post("/trades", json=valid_trade)
    replacement = valid_trade | {"counterparty_id": "CP-NEW"}
    response = client.post("/trades", json=replacement)
    assert response.status_code == 200
    assert response.json()["operation"] == "replaced"
    assert client.get("/trades/T1").json()["counterparty_id"] == "CP-NEW"


def test_higher_version_replaces_trade(client, valid_trade):
    client.post("/trades", json=valid_trade)
    response = client.post("/trades", json=valid_trade | {"version": 2})
    assert response.status_code == 200
    assert response.json()["trade"]["version"] == 2


def test_lower_version_is_rejected(client, valid_trade):
    client.post("/trades", json=valid_trade | {"version": 2})
    response = client.post("/trades", json=valid_trade)
    assert response.status_code == 409
    assert response.json()["current_version"] == 2


def test_past_maturity_is_rejected(client, valid_trade):
    response = client.post("/trades", json=valid_trade | {"maturity_date": "2000-01-01"})
    assert response.status_code == 422
    assert "earlier than today" in response.json()["detail"]


def test_list_filter_delete_and_not_found(client, valid_trade):
    client.post("/trades", json=valid_trade)
    assert len(client.get("/trades?include_expired=false").json()) == 1
    assert client.delete("/trades/T1").status_code == 204
    assert client.get("/trades/T1").status_code == 404
    assert client.delete("/trades/T1").status_code == 404


def test_health_and_input_validation(client, valid_trade):
    assert client.get("/health").json() == {"status": "ok"}
    response = client.post("/trades", json=valid_trade | {"version": 0})
    assert response.status_code == 422

