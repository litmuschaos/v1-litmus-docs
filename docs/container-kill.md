---
id: container-kill
title: Container Kill Experiment Details
sidebar_label: Container Kill
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
    <td> Kill one container in the application pod </td>
    <td> GKE, Packet(Kubeadm), Minikube, EKS, AKS </td>
  </tr>
</table>

## Prerequisites

- Ensure that the Litmus ChaosOperator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `container-kill` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/generic/container-kill/experiment.yaml)

## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- litmus LIB Details:
    - It supports docker, containerd and crio container runtime.
    - It can kill the container of multiple pods in parallel (can be tuned by `PODS_AFFECTED_PERC` env).
    - Containers are killed using the `docker kill` in docker runtime and `crictl stop` command in containerd or crio runtime.
    - container-kill is run as a pod on the application node. It have ability to kill the application containers multiple times. Which can be varied by `TOTAL_CHAOS_DURATION` and `CHAOS_INTERVAL`.
- pumba LIB Details:
    - It support only docker container runtime.
    - It can kill the container of multiple pods in parallel (can be tuned by `PODS_AFFECTED_PERC` env). It kill the container by sending SIGKILL termination signal to its docker socket (hence docker runtime is required).
    - Containers are killed using the `kill` command provided by [pumba](https://github.com/alexei-led/pumba)
    - Pumba is run as a pod on the application node. It have ability to kill the application containers multiple times. Which can be varied by `TOTAL_CHAOS_DURATION` and `CHAOS_INTERVAL`.
- Tests deployment sanity (replica availability & uninterrupted service) and recovery workflow of the application
- Good for testing recovery of pods having side-car containers

## Integrations

- Container kill supports `litmus` and `pumba` LIB.
- The container runtime can be choose via setting `CONTAINER_RUNTIME` env. supported values: `docker`, `containerd`, `crio`
- The desired pumba and litmus image can be configured in the env variable `LIB_IMAGE`. 

## Steps to Execute the ChaosExperiment

- This ChaosExperiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample RBAC Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/container-kill/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: container-kill-sa
  namespace: default
  labels:
    name: container-kill-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: container-kill-sa
  namespace: default
  labels:
    name: container-kill-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: [""]
  resources: ["pods","events"]
  verbs: ["create","list","get","patch","update","delete","deletecollection"]
- apiGroups: [""]
  resources: ["pods/exec","pods/log","replicationcontrollers"]
  verbs: ["list","get","create"]
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["create","list","get","delete","deletecollection"]
- apiGroups: ["apps"]
  resources: ["deployments","statefulsets","daemonsets","replicasets"]
  verbs: ["list","get"]
- apiGroups: ["apps.openshift.io"]
  resources: ["deploymentconfigs"]
  verbs: ["list","get"]
- apiGroups: ["argoproj.io"]
  resources: ["rollouts"]
  verbs: ["list","get"]
- apiGroups: ["litmuschaos.io"]
  resources: ["chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: container-kill-sa
  namespace: default
  labels:
    name: container-kill-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: container-kill-sa
subjects:
- kind: ServiceAccount
  name: container-kill-sa
  namespace: default

```

***Note:*** In case of restricted systems/setup, create a PodSecurityPolicy(psp) with the required permissions. The `chaosServiceAccount` can subscribe to work around the respective limitations. An example of a standard psp that can be used for litmus chaos experiments can be found [here](https://docs.litmuschaos.io/docs/next/litmus-psp/). 

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired in `experiments.spec.components.env`
- To understand the values to provided in a ChaosEngine specification, refer [ChaosEngine Concepts](chaosengine-concepts.md)

***Note:*** *Ensure that the CHAOS_INTERVAL used in the experiment is fairly high (i.e., enough time is provided for app recovery). Else, it can cause an exponential increase in the backOff delay, causing the app to stay in CrashLoopBackOff state for much longer*

#### Supported Experiment Tunables

<table>
  <tr>
    <th> Variables </th>
    <th> Description  </th>
    <th> Specify In ChaosEngine </th>
    <th> Notes </th>
  </tr>
  <tr>
    <td> TARGET_CONTAINER  </td>
    <td> The name of container to be killed inside the pod </td>
    <td> Optional </td>
    <td> If the TARGET_CONTAINER is not provided it will delete the first container </td>
  </tr>
  <tr>
    <td> CHAOS_INTERVAL  </td>
    <td> Time interval b/w two successive container kill (in sec) </td>
    <td> Optional </td>
    <td> If the CHAOS_INTERVAL is not provided it will take the default value of 10s </td>
  </tr>
  <tr>
    <td> TOTAL_CHAOS_DURATION  </td>
    <td> The time duration for chaos injection (seconds) </td>
    <td> Optional </td>
    <td> Defaults to 20s </td>
  </tr>
    <tr>
    <td> PODS_AFFECTED_PERC </td>
    <td> The Percentage of total pods to target  </td>
    <td> Optional </td>
    <td> Defaults to 0 (corresponds to 1 replica), provide numeric value only </td>
  </tr>  
  <tr>
    <td> TARGET_PODS </td>
    <td> Comma separated list of application pod name subjected to container kill chaos</td>
    <td> Optional </td>
    <td> If not provided, it will select target pods randomly based on provided appLabels</td>
  </tr>  
  <tr>
    <td> LIB_IMAGE  </td>
    <td> LIB Image used to kill the container </td>
    <td> Optional </td>
    <td> Defaults to `litmuschaos/go-runner:latest`</td>
  </tr>
  <tr>
    <td> LIB  </td>
    <td> The category of lib use to inject chaos </td>
    <td> Optional  </td>
    <td> Default value: litmus, supported values: pumba and litmus </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before injection of chaos in sec </td>
    <td> Optional  </td>
    <td> </td>
  </tr>
  <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple target pods </td>
    <td> Optional </td>
    <td> Default value: parallel. Supported: serial, parallel </td>
  </tr>
  <tr>
    <td> SIGNAL </td>
    <td> It contains termination signal used for container kill </td>
    <td> Optional </td>
    <td> Default value: SIGKILL </td>
  </tr>
  <tr>
    <td> SOCKET_PATH </td>
    <td> Path of the containerd/crio/docker socket file </td>
    <td> Optional  </td>
    <td> Defaults to `/var/run/docker.sock` </td>
  </tr>
  <tr>
    <td> CONTAINER_RUNTIME  </td>
    <td> container runtime interface for the cluster</td>
    <td> Optional </td>
    <td>  Defaults to docker, supported values: docker, containerd and crio for litmus and only docker for pumba LIB </td>
  </tr>
  <tr>
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name.</td>
    <td> Optional  </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>
</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/container-kill/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  # It can be true/false
  annotationCheck: 'false'
  # It can be active/stop
  engineState: 'active'
  appinfo:
    appns: 'default'
    applabel: 'app=nginx'
    appkind: 'deployment'
  chaosServiceAccount: container-kill-sa
  # It can be delete/retain
  jobCleanUpPolicy: 'delete' 
  experiments:
    - name: container-kill
      spec:
        components:
          env:
            # provide the chaos interval
            - name: CHAOS_INTERVAL
              value: '10'

            # provide the total chaos duration
            - name: TOTAL_CHAOS_DURATION
              value: '20'

            # provide the name of container runtime
            # for litmus LIB, it supports docker, containerd, crio
            # for pumba LIB, it supports docker only
            - name: CONTAINER_RUNTIME
              value: 'docker'

            # provide the socket file path
            - name: SOCKET_PATH
              value: '/var/run/docker.sock'
              
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- View pod restart count by setting up a watch on the pods in the application namespace

  `watch -n 1 kubectl get pods -n <application-namespace>`

### Abort/Restart the ChaosExperiment

- To stop the pod-delete experiment immediately, either delete the ChaosEngine resource or execute the following command:

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"stop"}}'`

- To restart the experiment, either re-apply the ChaosEngine YAML or execute the following command:

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"active"}}'`

### Check ChaosExperiment Result

- Check whether the application is resilient to the container kill, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-container-kill -n <application-namespace>`

## Application Container Kill Demo 

- A sample recording of this experiment execution is provided [here](https://youtu.be/XKyMNdVsKMo).
