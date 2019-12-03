---
id: version-0.8.0-pod-delete
title: Pod Delete Experiment Details
sidebar_label: Pod Delete
original_id: pod-delete
---
------

## Experiment Metadata

| Type      | Description              | Tested K8s Platform                                               |
| ----------| ------------------------ | ------------------------------------------------------------------|
| Generic   | Fail the application pod | GKE, Konvoy(AWS), Packet(Kubeadm), Minikube, OpenShift(Baremetal)  |

## Prerequisites

- Ensure that the Litmus Chaos Operator is running
- Ensure that the `pod-delete` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/pod-delete)

## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- Causes (forced/graceful) pod failure of specific/random replicas of an application resources
- Tests deployment sanity (replica availability & uninterrupted service) and recovery workflow of the application

## Integrations

- Pod failures can be effected using one of these chaos libraries: `litmus`, `powerfulseal`
- The desired chaos library can be selected by setting one of the above options as value for the env variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired

#### Supported Experiment Tunables

| Variables             | Description                                                  | Type      | Notes                                                      |
| ----------------------| ------------------------------------------------------------ |-----------|------------------------------------------------------------|
| TOTAL_CHAOS_DURATION  | The time duration for chaos insertion (seconds)              | Optional  | Defaults to 15s                                            |
| CHAOS_INTERVAL        | Time interval b/w two successive pod failures (sec)          | Optional  | Defaults to 5s                                             |
| LIB                   | The chaos lib used to inject the chaos                       | Optional  | Defaults to `litmus`. Supported: `litmus`, `powerfulseal`  |
| FORCE                 | Application Pod failures type                                | Optional  | Default to `true`, With `terminationGracePeriodSeconds=0`  |

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
    - name: pod-delete
      spec:
        components:
           # set chaos duration (in sec) as desired
          - name: TOTAL_CHAOS_DURATION
            value: '30'
          # set chaos interval (in sec) as desired
          - name: CHAOS_INTERVAL
            value: '10'
          # pod failures without '--force' & default terminationGracePeriodSeconds
          - name: FORCE
            value: "false"
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress

- View pod terminations & recovery by setting up a watch on the pods in the application namespace

  `watch -n 1 kubectl get pods -n <application-namespace>`

### Check Chaos Experiment Result

- Check whether the application is resilient to the pod failure, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-pod-delete -n <application-namespace>`

## Application Pod Failure Demo

- A sample recording of this experiment execution is provided here.
