from locust import HttpUser, task, constant

class ImgClssificationUser(HttpUser):
    wait_time = constant(1)

    @task
    def predict(self):
        attach = open('cat_224x224.jpg', 'rb')
        payload = {'with_resize': False, 'with_post_process': False}
        r = self.client.post("/predict/image", files={"image_file": attach}, data=payload)

        # uncomment to check the response of the prediction 
        # print(r.text)