---
id: pod-network-loss
title: Pod Network Loss Experiment Details
sidebar_label: Pod Network Loss  
---
------

## Experiment Metadata

| Type      | Description              | Tested K8s Platform                                               |
| ----------| ------------------------ | ------------------------------------------------------------------|
| Generic   | Inject Packet Loss Into Application Pod | GKE, Konvoy(AWS), Packet(Kubeadm), OpenShift(Baremetal) |

## Prerequisites

- Ensure that the Litmus Chaos Operator is running
- Ensure that the `pod-network-loss` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/pod-network-loss)
- <div class="danger">
    <strong>NOTE</strong>: 
        Experimenting Cluster should be non-minikube cluster . 
        Experiment is supported only on Docker Runtime. Support for containerd/CRIO runtimes will be added in subsequent releases.
</div>

## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- Pod-network-loss injects chaos to disrupt network connectivity to kubernetes pods.
- The application pod should be healthy once chaos is stopped. Service-requests should be         served despite chaos.
- Causes loss of access to application replica by injecting packet loss using pumba


## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired

#### Supported Experiment Tunables

| Variables             | Description                                                  | Type      | Notes                                                      |
| ----------------------| ------------------------------------------------------------ |-----------|------------------------------------------------------------|
| NETWORK_INTERFACE     | Name of ethernet interface considered for shaping traffic                                | Mandatory  |   |
| TARGET_CONTAINER     | Name of container which is subjected to network latency      | Mandatory  |   |
| NETWORK_PACKET_LOSS_PERCENTAGE  | The packet loss in percentage	| Mandatory  | |
| TOTAL_CHAOS_DURATION  | The time duration for chaos insertion in milliseconds | Optional  | Default (60000ms)                                            |
 LIB                   | The chaos lib used to inject the chaos eg. Pumba             | Optional  |  |
| CHAOSENGINE     | ChaosEngine CR name associated with the experiment instance      | Optional  |   |
| CHAOS_SERVICE_ACCOUNT     | Service account used by the pumba daemonset Optional      | Optional  |   |

#### Sample ChaosEngine Manifest

```yaml
# chaosengine.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-network-chaos
  namespace: default
spec:
  jobCleanUpPolicy: retain
  monitoring: false
  appinfo: 
    appns: default
    # FYI, To see app label, apply kubectl get pods --show-labels
    applabel: "app=nginx"
    appkind: deployment
  chaosServiceAccount: nginx 
  experiments:
    - name: pod-network-loss
      spec:
        components:
        - name: ANSIBLE_STDOUT_CALLBACK
          value: default
        - name: TARGET_CONTAINER
          #Container name where chaos has to be injected
          value: "nginx" 
        - name: LIB_IMAGE
          value: gaiaadm/pumba:0.6.5
        - name: NETWORK_INTERFACE
          #Network interface inside target container
          value: eth0                    
        - name: NETWORK_PACKET_LOSS_PERCENTAGE
          value: "100"
        - name: TOTAL_CHAOS_DURATION
          value: "60000"
        - name: LIB
          value: pumba
```
### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress

- View network latency by setting up a ping on the affected pod from the cluster nodes 

  `ping <pod_ip_address>`

### Check Chaos Experiment Result

- Check whether the application is resilient to the Pod Network Loss, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult <ChaosEngine-Name>-<ChaosExperiment-Name> -n <application-namespace>`


## Application Pod Network Loss Demo  [TODO]

- A sample recording of this experiment execution is provided here.