from locust import HttpUser, constant, task


class ImgClssificationUser(HttpUser):
    wait_time = constant(1)

    @task
    def predict(self):
        attach = open("cat_224x224.jpg", "rb")
        payload = {"with_resize": False, "with_post_process": False}
        _ = self.client.post(
            "/predict/image", files={"image_file": attach}, data=payload
        )
