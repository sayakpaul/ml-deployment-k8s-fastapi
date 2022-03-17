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
