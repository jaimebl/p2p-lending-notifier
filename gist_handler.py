import logging
import requests

GISTS_API_URL = "https://api.github.com/gists"

def get_gist_value(gist_id, file_name, github_token):
    """Fetches the stored value from the Gist. If missing, initializes it to 0."""
    headers = {"Authorization": f"token {github_token}"}
    gist_url = f"{GISTS_API_URL}/{gist_id}"

    try:
        response = requests.get(gist_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if file_name in data["files"]:
            count = int(data["files"][file_name]["content"].strip())
            logging.info(f"📂 Last stored opportunities: {count}")
            return count
        else:
            logging.warning(f"⚠️ File '{file_name}' not found in Gist. Initializing to 0.")
            update_gist_value(gist_id, file_name, github_token, 0)
            return 0
    except requests.exceptions.HTTPError as e:
        logging.error(f"⚠️ Could not fetch value from Gist: {e}")
        raise e

def update_gist_value(gist_id, file_name, github_token, value):
    headers = {"Authorization": f"token {github_token}"}
    gist_url = f"{GISTS_API_URL}/{gist_id}"
    payload = {"files": {file_name: {"content": str(value)}}}

    try:
        response = requests.patch(gist_url, json=payload, headers=headers)
        response.raise_for_status()
        logging.info("✅ Updated last opportunity count in Gist.")
    except Exception as e:
        logging.error(f"⚠️ Failed to update Gist: {e}")
        raise e
