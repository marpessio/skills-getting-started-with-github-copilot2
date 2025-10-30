import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

def test_signup_for_activity_success():
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_duplicate():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # This email is already registered
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"