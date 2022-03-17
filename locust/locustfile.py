from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def predict(self):
        attach = open('cat.jpg', 'rb')
        r = self.client.post("/predict/image", files={"image_file": attach})

        # uncomment to check the response of the prediction 
        # print(r.text)