---
id: pod-network-loss
title: Pod Network Loss Experiment Detail
sidebar_label: Pod Network Loss  
---
------

## Experiment Metadata

| Type      | Description              | Tested K8s Platform                                               |
| ----------| ------------------------ | ------------------------------------------------------------------|
| Generic   | Inject Packet Loss Into Application Pod | GKE, Konvoy(AWS), Packet(Kubeadm), Minikube, OpenShift(Baremetal) |

## Prerequisites

- Ensure that the Litmus Chaos Operator is running
- Application subjected to chaos must have tc network traffic shaping tool installed
- Ensure that the `pod-network-loss` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/pod-network-loss)
- <div class="danger">
    <strong>NOTE</strong>: 
        Experimenting Cluster should be non-minikube cluster . Minikube is not seen to inject  
                the desired chaos.
        Experiment is supported only on Docker Runtime. We do not support containerd/CRIO runtimes yet for network tests.There is a way to directly invoke tc, but these utils aren't added yet.
</div>

## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- Pod-network-loss injects chaos to disrupt network connectivity to kubernetes pods.
- The application pod should be healthy once chaos is stopped. Service-requests should be         served despite chaos.
- Pumba is run as a daemonset on all nodes in dry-run mode to begin with; the network-loss        command is issued during experiment execution via kubectl exec
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
| TOTAL_CHAOS_DURATION  | The time duration for chaos insertion (seconds)              | Optional  | 60000                                            |
| NETWORK_PACKET_LOSS_PERCENTAGE  | The packet loss in percentage	| Mandatory  | |
 LIB                   | The chaos lib used to inject the chaos eg. Pumba             | Optional  |  |
| NETWORK_INTERFACE     | Name of ethernet interface considered for shaping traffic                                | Instance-Specific (Optional)  |   |
| TARGET_CONTAINER     | Name of container which is subjected to network latency      | Instance-Specific (Optional)  |   |
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
    applabel: "app=nginx-app"
    appkind: deployment
  chaosServiceAccount: nginx 
  experiments:
    - name: pod-network-loss
      spec:
        components:
        - name: ANSIBLE_STDOUT_CALLBACK
          value: default
        - name: TARGET_CONTAINER
          value: "nginx-deploy-container"
        - name: LIB_IMAGE
          value: gaiaadm/pumba:0.4.8
        - name: NETWORK_INTERFACE
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

  `ping http_address`

### Check Chaos Experiment Result

- Check whether the application is resilient to the Pod Network Loss, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult <ChaosEngine-Name>-<ChaosExperiment-Name> -n <application-namespace>`


## Application Pod Network Loss Demo  [TODO]

- A sample recording of this experiment execution is provided here.