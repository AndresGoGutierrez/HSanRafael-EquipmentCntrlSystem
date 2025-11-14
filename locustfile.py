from locust import HttpUser, task, between

# credenciales reales que tengas en tu BD
USERNAME = "admin"         # cambia por tu username
PASSWORD = "admin123"      # cambia por tu pass real

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # LOGIN con OAuth2PasswordRequestForm (form-data, no JSON)
        response = self.client.post(
            "/api/v1/auth/login",
            data={
                "username": USERNAME,
                "password": PASSWORD
            }
        )

        if response.status_code == 200:
            token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    @task(3)
    def home(self):
        self.client.get("/", headers=self.headers)

    @task(3)
    def health(self):
        self.client.get("/health", headers=self.headers)

    @task(1)
    def list_users(self):
        # ejemplo de endpoint protegido
        self.client.get("/api/v1/user", headers=self.headers)
