---
id: pod-network-latency
title: Pod Network Latency Experiment Detail
sidebar_label: Pod Network Latency
---
------

## Experiment Metadata

| Type      | Description              | Tested K8s Platform                                               |
| ----------| ------------------------ | ------------------------------------------------------------------|
| Generic   | Inject Network Latency Into Application Pod | Packet Cluster(Kubeadm)|

## Prerequisites

- Ensure that the Litmus Chaos Operator is running
- Experimenting Cluster should be non-minikube cluster
- Application subjected to chaos must have tc network traffic shaping tool installed
- Ensure that the `pod-network-latency` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/pod-network-latency)

## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- Pod-network-latency contains chaos to disrupt network connectivity of kubernetes pods.
- The test involved setting up a ping to general/public IPs from inside the pod & also setting up a ping to the pod IP itself from a cluster node.
- The application pod should be healthy once chaos is stopped. Service-requests should be served despite chaos.
- Causes flaky access to application replica by injecting network delay using pumba.


## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired

#### Supported Experiment Tunables

| Variables             | Description                                                  | Type      | Notes                                                      |
| ----------------------| ------------------------------------------------------------ |-----------|------------------------------------------------------------|
| TOTAL_CHAOS_DURATION  | The time duration for chaos insertion (seconds)              | Mandatory  | 60000                                            |
| NETWORK_LATENCY        | The latency/delay in milliseconds                           | Mandatory  | 60000
| LIB                   | The chaos lib used to inject the chaos eg. Pumba             | Optional  |  |
| NETWORK_INTERFACE     | Name of ethernet interface considered for shaping traffic                                | Mandatory  |   |
| TARGET_CONTAINER     | Name of container which is subjected to network latency      | Mandatory  |   |
| CHAOSENGINE     | ChaosEngine CR name associated with the experiment instance      | Optional  |   |
| CHAOS_SERVICE_ACCOUNT     | Service account used by the pumba daemonset Optional      | Optional  |   |

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: engine-nginx
  namespace: default
spec:
  jobCleanUpPolicy: retain
  monitoring: false
  appinfo: 
    appns: default
    # FYI, To see app label, apply kubectl get pods --show-labels
    applabel: "app=nginx-app"
    appkind: deployment
  chaosServiceAccount: nginx 
  experiments:
    - name: pod-network-latency
      spec:
        components:
        - name: ANSIBLE_STDOUT_CALLBACK
          value: default
        - name: TARGET_CONTAINER
          value: nginx-deploy-container
        - name: NETWORK_INTERFACE
          value: eth0
        - name: LIB_IMAGE
          value: gaiaadm/pumba:0.4.8
        - name: NETWORK_LATENCY
          value: "60000"
        - name: TOTAL_CHAOS_DURATION
          value: "60000"
        - name: LIB
          value: pumba
```
### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Check Chaos Experiment Result

- Check whether the application is resilient to the Pod Network Latency, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult <ChaosEngine-Name>-<ChaosExperiment-Name> -n <application-namespace>`

### Test Chaos progress

- During Chaos progress interval View Pod Network Latency inside targeted container , By setting Up Traffic control (tc) tool in targeted container .Check Ping Simulate Internet connections.

  `ping http_address`




	 	
	
	