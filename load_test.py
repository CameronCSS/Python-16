from locust import HttpUser, task, between
import google.oauth2.service_account
import google.auth.transport.requests

# Your Cloud Run URL
IAP_CLIENT_ID = "Custom_oauth_token_from_GCP"
KEY_FILE = "load-test-key.json"

def get_iap_token():
    credentials = google.oauth2.service_account.IDTokenCredentials.from_service_account_file(
        KEY_FILE,
        target_audience=IAP_CLIENT_ID
    )
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    return credentials.token

class DriveInvestigationUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        self.token = get_iap_token()

    @task(1)
    def load_page(self):
        self.client.get(
            "/",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(2)
    def whoami(self):
        self.client.get(
            "/whoami",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(3)
    def investigate(self):
        self.client.get(
            "/investigate",
            headers={"Authorization": f"Bearer {self.token}"}
        )