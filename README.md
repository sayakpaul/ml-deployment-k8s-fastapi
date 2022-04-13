# Deploying ML models with FastAPI, Docker, and Kubernetes

*By: Sayak Paul and [Chansung Park](https://github.com/deep-diver)*

This project shows how to serve an ONNX-optimized image classification model as a
RESTful web service with FastAPI, Docker, and Kubernetes (k8s). The idea is to first
Dockerize the API and then deploy it on a k8s cluster running on [Google Kubernetes
Engine (GKE)](https://cloud.google.com/kubernetes-engine). We do this integration
using [GitHub Actions](https://github.com/features/actions). 

👋 **Note**: Even though this project uses an image classification its structure and techniques can
be used to serve other models as well.

## Deploying the model as a service with k8s

* We decouple the model optimization part from our API code. The optimization part is
available within the `notebooks/TF_to_ONNX.ipynb` notebook.
* Then we locally test the API. You can find the instructions within the `api`
directory.
* To deploy the API, we define our `deployment.yaml` workflow file inside `.github/workflows`.
It does the following tasks:

    * Looks for any changes in the specified directory. If there are any changes:
    * Builds and pushes the latest Docker image to Google Container Register (GCR).
    * Deploys the Docker container on the k8s cluster running on GKE. 

## Configurations needed beforehand

* Create a k8s cluster on GKE. [Here's](https://www.youtube.com/watch?v=hxpGC19PzwI) a
relevant resource. 
* [Create](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) a
service account key (JSON) file. It's a good practice to only grant it the roles
required for the project. For example, for this project, we created a fresh service 
account and granted it permissions for the following: Storage Admin, GKE Developer, and
GCR Developer. 
* Crete a secret named `GCP_CREDENTIALS` on your GitHub repository and copy paste the
contents of the service account key file into the secret. 
* Configure bucket storage related permissions for the service account:

    ```shell
    $ export PROJECT_ID=<PROJECT_ID>
    $ export ACCOUNT=<ACCOUNT>
    
    $ gcloud -q projects add-iam-policy-binding ${PROJECT_ID} \
        --member=serviceAccount:${ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
        --role roles/storage.admin
    
    $ gcloud -q projects add-iam-policy-binding ${PROJECT_ID} \
        --member=serviceAccount:${ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
        --role roles/storage.objectAdmin
    
    gcloud -q projects add-iam-policy-binding ${PROJECT_ID} \
        --member=serviceAccount:${ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
        --role roles/storage.objectCreator
    ```
* If you're on the `main` branch already then upon a new push, the worflow defined
in `.github/workflows/deployment.yaml` should automatically run. Here's how the
final outputs should look like so ([run link](https://github.com/sayakpaul/ml-deployment-k8s-fastapi/runs/5343002731)):

![](https://i.ibb.co/fDGFbpr/Screenshot-2022-03-01-at-12-25-42-PM.png)

## Notes

* Since we use CPU-based pods within the k8s cluster, we use ONNX optimizations
  since they are known to provide performance speed-ups for CPU-based environments.
  If you are using GPU-based pods then look into [TensorRT](https://developer.nvidia.com/tensorrt). 
* We use [Kustomize](https://kustomize.io) to manage the deployment on k8s.

## Querying the API endpoint

From workflow outputs, you should see something like so:

```shell
NAME             TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
fastapi-server   LoadBalancer   xxxxxxxxxx   xxxxxxxxxx        80:30768/TCP   23m
kubernetes       ClusterIP      xxxxxxxxxx     <none>          443/TCP        160m
```

Note the `EXTERNAL-IP` corresponding to `fastapi-server` (iff you have named
your service like so). Then cURL it:

```shell
curl -X POST -F image_file=@cat.jpg -F with_resizing=True http://{EXTERNAL-IP}:80/predict/image
```

You should get the following output (if you're using the `cat.jpg` image present
in the `api` directory):

```shell
"{\"Label\": \"tabby\", \"Score\": \"0.538\"}"
```

The request assumes that you have a file called `cat.jpg` present in your
working directory.

## TODO (s)

* Set up logging for the k8s pods.
* Find a better way to report the latest API endpoint.

## Acknowledgements

[ML-GDE program](https://developers.google.com/programs/experts/) for providing GCP credit support.

