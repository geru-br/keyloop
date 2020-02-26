from locust import between, HttpLocust, TaskSequence, seq_task


class AuthSession(TaskSequence):

    @property
    def headers(self):
        return {'content-type': 'application/vnd.api+json'}

    @seq_task(1)
    def on_start(self):
        """Login."""
        self.login()

    # @seq_task(2)
    # def on_stop(self):
    #     """Logout."""
    #     self.logout()

    def login(self):
        input_payload = {
            "data": {
                "type": "auth-session",
                "attributes": {
                    "username": "test@test.com.br",
                    "password": "1234567a"
                }
            }
        }
        import json
        self.client.post("/api/v1/realms/PLAYGROUND/auth-session", json.dumps(input_payload), headers=self.headers)

    def logout(self):
        self.client.delete("/api/v1/realms/PLAYGROUND/auth-session", headers=self.headers)


class WebsiteUser(HttpLocust):
    task_set = AuthSession
    wait_time = between(5, 9)
