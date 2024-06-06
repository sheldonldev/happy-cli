from fastapi.testclient import TestClient
from temp_project.server import app

client = TestClient(app)


def test_echo():
    res = client.get('echo/1')
    assert res.status_code == 200
