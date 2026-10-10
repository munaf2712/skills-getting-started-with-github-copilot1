from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    original_participants = app_module.activities[activity_name]["participants"][:]

    try:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

        delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
        assert delete_response.status_code == 200

        activity = client.get("/activities").json()[activity_name]
        assert email not in activity["participants"]
    finally:
        app_module.activities[activity_name]["participants"] = original_participants
