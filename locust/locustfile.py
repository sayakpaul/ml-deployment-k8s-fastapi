from locust import HttpUser, task, constant

class ImgClssificationUser(HttpUser):
    wait_time = constant(1)

    @task
    def predict(self):
        attach = open('cat.jpg', 'rb')
        r = self.client.post("/predict/image", files={"image_file": attach})

        # uncomment to check the response of the prediction 
        # print(r.text)