from locust import HttpLocust, TaskSet, between


class AuthSession(TaskSet):

    @property
    def login_payload(self):
        return {
            "data": {
                "type": "identity",
                "attributes": {
                    "username": "test@test.com",
                    "password": "blablabla",
                    "name": "xablau",
                }
            }
        }

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post("/api/v1/realms/PLAYGROUND/identities", self.login_payload)

    def logout(self):
        self.client.delete("/api/v1/realms/PLAYGROUND/identities")


class WebsiteUser(HttpLocust):
    task_set = AuthSession
    wait_time = between(5, 9)
