"""Working tests for the implemented plans endpoints. Copy this style for your own."""


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"


def test_create_and_join_plan(client):
    created = client.post("/api/plans", json={"title": "Lake weekend", "organizer_name": "Asha"}).json()
    invite = created["plan"]["invite_code"]
    assert created["member"]["role"] == "organizer"

    joined = client.post(f"/api/invites/{invite}/join", json={"display_name": "Ben"})
    assert joined.status_code == 201

    plan = client.get(f"/api/plans/{created['plan']['id']}", headers=auth(created["member_token"])).json()
    assert {m["display_name"] for m in plan["members"]} == {"Asha", "Ben"}


def test_plan_response_never_contains_secrets(client):
    created = client.post("/api/plans", json={"title": "Dinner", "organizer_name": "Asha"}).json()
    body = client.get(f"/api/plans/{created['plan']['id']}", headers=auth(created["member_token"])).text
    assert "token_hash" not in body
    assert created["member_token"] not in body


def test_outsider_cannot_read_plan(client):
    a = client.post("/api/plans", json={"title": "A", "organizer_name": "Asha"}).json()
    b = client.post("/api/plans", json={"title": "B", "organizer_name": "Ben"}).json()
    r = client.get(f"/api/plans/{a['plan']['id']}", headers=auth(b["member_token"]))
    assert r.status_code == 403
