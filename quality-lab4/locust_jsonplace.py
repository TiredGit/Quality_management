from locust import HttpUser, task, between


class JSONPlaceholderUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def get_posts(self):
        with self.client.get("/posts", name="GET /posts", catch_response=True) as response:

            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                try:
                    data = response.json()
                    if not isinstance(data, list):
                        response.failure("Expected a list of posts")
                except ValueError:
                    response.failure("Invalid JSON response")

    @task(1)
    def get_users(self):
        with self.client.get("/users", name="GET /users", catch_response=True) as response:

            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                try:
                    data = response.json()
                    if not isinstance(data, list):
                        response.failure("Expected a list of users")
                except ValueError:
                    response.failure("Invalid JSON response")
