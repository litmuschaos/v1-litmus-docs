---
id: version-0.9.0-container-kill
title: Container Kill Experiment Details
sidebar_label: Container Kill
original_id: container-kill
---
------

## Experiment Metadata

| Type      | Description              | Tested K8s Platform                                               |
| ----------| ------------------------ | ------------------------------------------------------------------|
| Generic   | Kill one container in the application pod | GKE, Konvoy(AWS), Packet(Kubeadm), Minikube, OpenShift(Baremetal)  |

## Prerequisites

- Ensure that the Litmus Chaos Operator is running
- Ensure that the `container-kill` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/container-kill)
- Cluster must run docker container runtime

## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- Kills one container in the specified application pod by sending SIGKILL termination signal to its docker socket (hence docker runtime is required)
- Containers are killed using the `kill` command provided by [pumba](https://github.com/alexei-led/pumba)
- Pumba is run as a daemonset on all nodes in dry-run mode to begin with; the `kill` command is issued during experiment execution via `kubectl exec`
- Tests deployment sanity (replica availability & uninterrupted service) and recovery workflow of the application
- Good for testing recovery of pods having side-car containers

## Integrations

- Container kill is achieved using the `pumba` chaos library
- The desired pumba image can be configured in the env variable `LIB_IMAGE`. 
<!--- For the furute, other chaoslibs might be added which do not depend on docker runtime. The LIB env varable must be added then.-->

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired

#### Supported Experiment Tunables

| Variables             | Description                                                  | Type      | Notes                                                      |
| ----------------------| ------------------------------------------------------------ |-----------|------------------------------------------------------------|
| TARGET_CONTAINER      | The container to be killed inside the pod                    | Mandatory |                                                            |
| LIB_IMAGE             | The pumba image used to run the kill command with            | Optional  | Default to `gaiaadm/pumba:0.4.8`; **note**: execution logic changed in version 0.6 ([here](https://github.com/alexei-led/pumba#running-inside-docker-container)). images >=0.6 do not work with litmuschaos.                           |

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  appinfo:
    appns: default
    applabel: 'app=nginx'
    appkind: deployment
  chaosServiceAccount: nginx-sa
  monitoring: false
  jobCleanUpPolicy: delete
  experiments:
    - name: container-kill
      spec:
        components:
           # specify the name of the container to be killed
          - name: TARGET_CONTAINER
            value: 'nginx'
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress

- View pod restart count by setting up a watch on the pods in the application namespace

  `watch -n 1 kubectl get pods -n <application-namespace>`

### Check Chaos Experiment Result

- Check whether the application is resilient to the container kill, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-container-kill -n <application-namespace>`

## Application Container Kill Demo [TODO]

- A sample recording of this experiment execution is provided here.

