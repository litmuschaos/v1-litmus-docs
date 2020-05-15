---
id: pod-memory-hog
title: Pod Memory Hog Details
sidebar_label: Pod Memory Hog
---
------

## Experiment Metadata

<table>
  <tr>
    <th> Type </th>
    <th> Description </th>
    <th> Tested K8s Platform </th>
  </tr>
  <tr>
     <td> Generic </td>
    <td> Consume memory resources on the application container</td>
    <td> GKE, Packet(Kubeadm), Minikube, EKS  </td>
  </tr>
</table>

## Prerequisites

- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `pod-memory-hog` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/1.3.0?file=charts/generic/pod-memory-hog/experiment.yaml)
- Cluster must run docker container runtime

## Entry Criteria

- Application pods are healthy on the respective nodes before chaos injection

## Exit Criteria

- Application pods are healthy on the respective nodes post chaos injection

## Details

- This experiment consumes the Memory resources on the application container on specified memory in megabytes.
- It simulates conditions where app pods experience Memory spikes either due to expected/undesired processes thereby testing how the overall application stack behaves when this occurs. 


## Integrations

- Pod Memory can be effected using the chaos library: `litmus`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/pod-memory-hog/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-memory-hog-sa
  namespace: default
  labels:
    name: pod-memory-hog-sa
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: Role
metadata:
  name: pod-memory-hog-sa
  namespace: default
  labels:
    name: pod-memory-hog-sa
rules:
- apiGroups: ["","litmuschaos.io","batch"]
  resources: ["pods","jobs","events","pods/log","chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update","delete"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: RoleBinding
metadata:
  name: pod-memory-hog-sa
  namespace: default
  labels:
    name: pod-memory-hog-sa
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-memory-hog-sa
subjects:
- kind: ServiceAccount
  name: pod-memory-hog-sa
  namespace: default
```

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo`
- Override the experiment tunables if desired in `experiments.spec.components.env`
- To understand the values to provided in a ChaosEngine specification, refer [ChaosEngine Concepts](chaosengine-concepts.md)

#### Supported Experiment Tunables

<table>
  <tr>
    <th>  Variables </th>
    <th>  Description </th>
    <th> Type  </th>
    <th> Notes </th>
  </tr>
  <tr>
    <td> TARGET_CONTAINER </td>
    <td> Name of the container subjected to Memory stress  </td>
    <td> Mandatory  </td>
    <td> </td>
  </tr>
  <tr>
    <td> MEMORY_CONSUMPTION </td>
    <td>  The amount of memory used of hogging a Kubernetes pod (megabytes)</td>
    <td> Optional  </td>
    <td> Defaults to 500MB </td>
    <td> </td>
  </tr>
  <tr>
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (seconds)  </td>
    <td> Optional </td>
    <td> Defaults to 60s </td>
  </tr>
  <tr>
    <td> LIB_IMAGE </td>
    <td> The image used by the litmus (only supported) lib </td>
    <td> Optional </td>
    <td> Defaults to `litmuschaos/app-memory-stress:latest`  </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before and after injection of chaos in sec </td>
    <td> Optional  </td>
    <td> </td>
  </tr>
  <tr>
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name.</td>
    <td> Optional </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>

</table>
                      
#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/pod-memory-hog/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  # It can be true/false
  annotationCheck: 'true'
  # It can be active/stop
  engineState: 'active'
  #ex. values: ns1:name=percona,ns2:run=nginx 
  auxiliaryAppInfo: ''
  appinfo:
    appns: 'default'
    applabel: 'app=nginx'
    appkind: 'deployment'
  chaosServiceAccount: pod-memory-hog-sa
  monitoring: false
  # It can be delete/retain
  jobCleanUpPolicy: 'delete'
  experiments:
    - name: pod-memory-hog
      spec:
        components:
          env:
            # Provide name of target container
            # where chaos has to be injected
            - name: TARGET_CONTAINER
              value: 'nginx'

            # Enter the amount of memory in megabytes to be consumed by the application pod
            # default: 500 (Megabytes) 
            - name: MEMORY_CONSUMPTION
              value: ''

            - name: TOTAL_CHAOS_DURATION
              value: '60' # in seconds
            
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress

- Set up a watch on the applications interacting/dependent on the affected pods and verify whether they are running

  `watch kubectl get pods -n <application-namespace>`

### Check Chaos Experiment Result

- Check whether the application stack is resilient to Memory spikes on the app replica, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-pod-memory-hog -n <application-namespace>`

## Pod Memory Hog Experiment Demo 

- A sample recording of this experiment will be added very soon.
