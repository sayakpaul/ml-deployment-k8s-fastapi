# Load Test with Locust

This directory contains a Locust script for load testing. 

## How to setup

1. Installation

```python
pip3 install locust
```

2. Run 

```bash
# with UI 
$ locust 

OR

$ locust --users NUM_OF_USERS \
         --spawn-rate SPAWN_RATE \ 
         --host HOST_ADDRESS

# without UI & manual config
# the report will be generated to report.html
$ locust --headless \ 
         --users NUM_OF_USERS \
         --spawn-rate SPAWN_RATE \ 
         --host HOST_ADDRESS \ 
         --html report.html

# without UI & auto config
$ locust --config=load_test.conf
```

## Notes

* We used an `n1-standard` VM (4vCPU + 16GB RAM) on GCP in `us-central1` region 
since the nodes on GKE are also located there. 
* Before running the load-test, don't forget to replace `<<GKE Service IP>>` with the endpoint of 
your API in the `load_test.conf`.
* We prepare a resized image beforehand whose size is 224x224 (`cat_224x224.jpg`).
This is because we only focus on load testing on the server side thereby minimizing
the time for pre and post processing as much as possible.
