from utils.api_client import APIClient
from config.environment import config


def setup_api():
    api = APIClient(config["api_base_url"])
    api.login(
        config["credentials"]["username"],
        config["credentials"]["password"]
    )
    return api


# 🔹 TC-API-01 → GET Notes
def test_get_notes():

    api = setup_api()

    response = api.get_notes()
    data = response.json()

    print("GET Notes Response:", data)

    # ✅ Validations
    assert response.status_code == 200
    assert "data" in data
    assert isinstance(data["data"], list)


# 🔹 TC-API-03 → Delete Note
def test_delete_note():

    api = setup_api()

    notes = api.get_notes().json()["data"]

    if not notes:
        print("No notes to delete")
        return

    note_id = notes[0]["id"]

    response = api.delete_note(note_id)

    print("Delete Response:", response.status_code)

    # ✅ Validate deletion
    updated_notes = api.get_notes().json()["data"]

    assert note_id not in [note["id"] for note in updated_notes]