from locust import HttpLocust, TaskSet, between
import json


def login(l):
    headers = {'content-type': 'application/vnd.api+json'}
    l.client.post(
        "/api/v1/realms/PLAYGROUND/auth-session",
        data=json.dumps({
            "data": {
                "type":"auth-session", 
                "attributes":{
                    "username":"test@test.com.br",
                    "password":"1234567a"
                }
            }
        }),
        headers=headers
    )


class UserBehavior(TaskSet):
    tasks = {login: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        pass


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
