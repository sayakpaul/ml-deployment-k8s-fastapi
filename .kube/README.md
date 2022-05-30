# Run Experimental Setup

## Build Docker image
```bash
# under /.kube directory

$ TARGET_EXPERIMENT=experiment_1/2vCPU+2GB/
$ TAG=gcr.io/GCP_PROJECT_ID/IMG_NAME:IMG_TAG

$ docker build -f $TARGET_EXPERIMENT -t $TAG .
```

## Deploy on k8s cluster
```bash
# under /.kube directory

$ ./kustomize build $TARGET_EXPERIMENT | kubectl apply -f -
```