import json
import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    data_file = tmp_path / "submissions.json"

    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "DATA_FILE": data_file
    })

    with app.test_client() as test_client:
        yield test_client


def test_valid_submission_is_saved_and_displayed(client):
    response = client.post("/", data={
        "name": "Ali Ahmed",
        "registration_number": "FA23-BAI-001",
        "assignment_title": "DevOps Lab Assignment",
        "submission_url": "https://github.com/example/assignment"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data
    assert b"Ali Ahmed" in response.data
    assert b"FA23-BAI-001" in response.data

    submissions = json.loads(
        (client.application.config["DATA_FILE"]).read_text(
            encoding="utf-8"
        )
    )

    assert len(submissions) == 1
    assert submissions[0]["name"] == "Ali Ahmed"


def test_missing_registration_number_is_rejected(client):
    response = client.post("/", data={
        "name": "Ali Ahmed",
        "registration_number": "",
        "assignment_title": "DevOps Assignment",
        "submission_url": "https://github.com/example/assignment"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"All fields are required." in response.data

    data_file = client.application.config["DATA_FILE"]
    assert not data_file.exists()


def test_invalid_submission_url_is_rejected(client):
    response = client.post("/", data={
        "name": "Ali Ahmed",
        "registration_number": "FA23-BAI-001",
        "assignment_title": "DevOps Assignment",
        "submission_url": "not-a-valid-url"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid submission URL" in response.data

    data_file = client.application.config["DATA_FILE"]
    assert not data_file.exists()


