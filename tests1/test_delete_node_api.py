from utils.api_client import APIClient
from config.environment import config


def test_delete_note_api():

    api = APIClient(config["api_base_url"])

    # 🔐 Login
    api.login(
        config["credentials"]["username"],
        config["credentials"]["password"]
    )

    # 📥 Get existing notes
    notes = api.get_notes().json()["data"]

    if not notes:
        print("No notes available to delete")
        return

    note_id = notes[0]["id"]

    # 🗑️ Delete note
    response = api.delete_note(note_id)

    print("Delete Response:", response.status_code)

    # ✅ Validate deletion
    updated_notes = api.get_notes().json()["data"]

    assert note_id not in [note["id"] for note in updated_notes]