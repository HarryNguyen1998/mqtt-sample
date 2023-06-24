def test_ping(test_app):
    resp = test_app.get("/ping")
    assert resp.status_code == 200
    assert resp.json() == {"ping": "pong"}
