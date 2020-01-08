---
id: pod-network-corruption
title: Pod Network Corruption Experiment Details
sidebar_label: Pod Network Corruption
---
------

## Experiment Metadata

| Type      | Description              | Tested K8s Platform                                               |
| ----------| ------------------------ | ------------------------------------------------------------------|
| Generic   | Inject Network Packet Corruption Into Application Pod | GKE, Konvoy(AWS), Packet(Kubeadm), Minikube > v1.6.0 |

## Prerequisites
- Ensure that the Litmus Chaos Operator is running. If not, install from [here](https://github.com/litmuschaos/chaos-operator/blob/master/deploy/operator.yaml)
- Ensure that the `pod-network-corruption` experiment resource is available in the cluster by `kubectl get chaosexperiments` command. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/pod-network-corruption)

<div class="danger">
    <strong>NOTE</strong>: 
        Experiment is supported only on Docker Runtime. Support for containerd/CRIO runtimes will be added in subsequent releases.
</div>

## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- The application pod should be healthy once chaos is stopped. Service-requests should be         served despite chaos.
- Injects packet corruption on the specified container by starting a traffic control (tc) process with netem rules to add egress packet corruption
- Corruption is injected via pumba library with command pumba netem corruption by passing the relevant network interface, packet-corruption-percentage, chaos duration and regex filter for container name
- Can test the application's resilience to lossy/flaky network

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
| TARGET_CONTAINER     | Name of container which is subjected to network latency       | Mandatory  |   |
| NETWORK_PACKET_CORRUPTION_PERCENTAGE       | Packet corruption in percentage                           | Mandatory | Default (100)
| LIB                   | The chaos lib used to inject the chaos eg. Pumba             | Optional  |  |
| CHAOSENGINE     | ChaosEngine CR name associated with the experiment instance      | Optional  |   |
| CHAOS_SERVICE_ACCOUNT     | Service account used by the pumba daemonset Optional      | Optional  |   |
| TOTAL_CHAOS_DURATION  | The time duration for chaos insertion in milliseconds  | Optional| Default (60000ms)|
| LIB_IMAGE     | The pumba image used to run the kill command                                | Optional  | Default to gaiaadm/pumba:0.6.5 |

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name:  nginx-network-chaos
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
    - name: pod-network-corruption
      spec:
        components:
        - name: ANSIBLE_STDOUT_CALLBACK
          value: default
        - name: TARGET_CONTAINER
          #Container name where chaos has to be injected
          value: "nginx" 
        - name: NETWORK_INTERFACE
          #Network interface inside target container
          value: eth0                   
        - name: LIB_IMAGE
          value: gaiaadm/pumba:0.6.5
        - name: NETWORK_PACKET_CORRUPTION_PERCENTAGE
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

- View impact of network packet corruption on the affected pod from the cluster nodes (alternate is to setup ping to a remote IP from inside the target pod) 

  `ping <pod_ip_address>`

### Check Chaos Experiment Result

- Check whether the application is resilient to the Pod Network Packet Corruption, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult <ChaosEngine-Name>-<ChaosExperiment-Name> -n <application-namespace>`


## Application Pod Network Packet Corruption Demo  [TODO]

- A sample recording of this experiment execution is provided here.
