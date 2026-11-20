from fastapi.testclient import TestClient

from dashboard.app import create_app


def test_index_renders(tmp_path, monkeypatch):
    """The index page renders (Starlette 1.x rejects the old TemplateResponse signature)."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
