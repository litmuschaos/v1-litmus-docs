---
id: node-memory-hog
title: Node Memory Hog Experiment Details
sidebar_label: Node Memory Hog
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
    <td> Exhaust Memory resources on the Kubernetes Node </td>
    <td> GKE, EKS, AKS </td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `node-memory-hog` experiment resource is available in the cluster  by executing                         `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/generic/node-memory-hog/experiment.yaml)
- There should be administrative access to the platform on which the Kubernetes cluster is hosted, as the recovery of the affected node could be manual. For example, gcloud access to the GKE project

## Entry Criteria

- Application pods are healthy on the respective Nodes before chaos injection

## Exit Criteria

- Application pods may or may not be healthy post chaos injection

## Details

- This experiment causes Memory resource exhaustion on the Kubernetes node. The experiment aims to verify resiliency of applications whose replicas may be evicted on account on nodes turning unschedulable (Not Ready) due to lack of Memory resources.
- The Memory chaos is injected using a job running the linux stress-ng tool (a workload generator). The chaos is effected for a period equalling the TOTAL_CHAOS_DURATION and upto MEMORY_CONSUMPTION_PERCENTAGE(out of 100) or MEMORY_CONSUMPTION_MEBIBYTES(in Mebibytes out of total available memory).
- Application implies services. Can be reframed as:
Tests application resiliency upon replica evictions caused due to lack of Memory resources

## Integrations

- Node Memory Hog can be effected using the chaos library: `litmus`
- The desired chaos library can be selected by setting `litmus` as value for the env variable `LIB` 

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/node-memory-hog/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: node-memory-hog-sa
  namespace: default
  labels:
    name: node-memory-hog-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-memory-hog-sa
  labels:
    name: node-memory-hog-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: [""]
  resources: ["pods","events"]
  verbs: ["create","list","get","patch","update","delete","deletecollection"]
- apiGroups: [""]
  resources: ["pods/exec","pods/log"]
  verbs: ["create","list","get"]
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["create","list","get","delete","deletecollection"]
- apiGroups: ["litmuschaos.io"]
  resources: ["chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get","list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-memory-hog-sa
  labels:
    name: node-memory-hog-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: node-memory-hog-sa
subjects:
- kind: ServiceAccount
  name: node-memory-hog-sa
  namespace: default
```

***Note:*** In case of restricted systems/setup, create a PodSecurityPolicy(psp) with the required permissions. The `chaosServiceAccount` can subscribe to work around the respective limitations. An example of a standard psp that can be used for litmus chaos experiments can be found [here](https://docs.litmuschaos.io/docs/next/litmus-psp/).

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`. It is an optional parameter for infra level experiment.
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo`
- Override the experiment tunables if desired in `experiments.spec.components.env`
- To understand the values to provided in a ChaosEngine specification, refer [ChaosEngine Concepts](chaosengine-concepts.md)

#### Supported Experiment Tunables

<table>
  <tr>
    <th> Variables </th>
    <th> Description  </th>
    <th> Specify In ChaosEngine </th>
    <th> Notes </th>
  </tr>
   <tr>
    <td> TARGET_NODES </td>
    <td> Comma separated list of nodes, subjected to node memory hog</td>
    <td> Mandatory  </td>
    <td> </td>
  </tr>
  <tr>
    <td> NODE_LABEL </td>
    <td> It contains node label, which will be used to filter the target nodes if TARGET_NODES ENV is not set </td>
    <td> Optional </td>
    <td> </td>
  </tr>
  <tr>
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (in seconds) </td>
    <td> Optional </td>
    <td> Defaults to 120 </td>
  </tr>
   <tr>
    <td> LIB  </td>
    <td> The chaos lib used to inject the chaos </td>
    <td> Optional </td>
    <td> Defaults to `litmus` </td>
  </tr>
   <tr>
    <td> LIB_IMAGE  </td>
    <td> Image used to run the stress command </td>
    <td> Optional  </td>
    <td> Defaults to <code>litmuschaos/go-runner:latest</code> </td>
  </tr>
    <tr>
    <td> MEMORY_CONSUMPTION_PERCENTAGE </td>
    <td> Percent of the total node memory capacity </td>
    <td> Optional </td>
    <td> Defaults to 30 </td>
  </tr>
  </tr>
    <tr>
    <td> MEMORY_CONSUMPTION_MEBIBYTES </td>
    <td> The size in Mebibytes of total available memory. When using this we need to keep MEMORY_CONSUMPTION_PERCENTAGE empty as the percentage have more precedence</td>
    <td> Optional </td>
    <td>  </td>
  </tr>  
  <tr>
    <td> NUMBER_OF_WORKERS </td>
    <td> It is the number of VM workers involved in IO disk stress </td>
    <td> Optional  </td>
    <td> Default to 1 </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before and after injection of chaos in sec </td>
    <td> Optional  </td>
    <td> </td>
  </tr>
   <tr>
    <td> NODES_AFFECTED_PERC </td>
    <td> The Percentage of total nodes to target  </td>
    <td> Optional </td>
    <td> Defaults to 0 (corresponds to 1 node), provide numeric value only </td>
  </tr> 
   <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple target nodes </td>
    <td> Optional </td>
    <td> Default value: parallel. Supported: serial, parallel </td>
  </tr>
  <tr>
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name.</td>
    <td> Optional </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>

</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/node-memory-hog/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  # It can be active/stop
  engineState: 'active'
  #ex. values: ns1:name=percona,ns2:run=nginx 
  auxiliaryAppInfo: ''
  chaosServiceAccount: node-memory-hog-sa
  experiments:
    - name: node-memory-hog
      spec:
        components:
          env:
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '120'

            ## Specify the size as percent of total node capacity Ex: '30'
            ## Note: For consuming memory in mebibytes change the variable to MEMORY_CONSUMPTION_MEBIBYTES
            - name: MEMORY_CONSUMPTION_PERCENTAGE
              value: '30'
            
            ## percentage of total nodes to target
            - name: NODES_AFFECTED_PERC
              value: ''

            # provide the comma separated target node names
            - name: TARGET_NODES
              value: ''
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- Setting up a watch of the Memory consumed by nodes in the Kubernetes Cluster

  `watch kubectl top nodes`

OR
- Setting up a monitoring pod on the target node.

_myhtop.yml_
```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: myhtop
spec:
  containers:
  - name: myhtop
    image: litmuschaos/go-runner:latest
    imagePullPolicy: Always
    command: ['sh', '-c', 'sleep 3600']
  nodeName: kube-01 ## Replace this with the target node name...
```
Create the htop monitoring pod on Target node:

```bash
kubectl apply -f myhtop.yml
```

Now Exec into the pod and run htop command

```bash
kubectl exec -it myhtop -- /bin/sh
/litmus $ htop
```
The output will be similar to:

![Screenshot from 2021-01-22 16-01-30](https://user-images.githubusercontent.com/35391335/105480001-30b1b080-5ccb-11eb-91d1-09c49b81ea0a.png)

It is showing:
- The node size is `3.79G` out of which `517M` is in use. Now run the experiment and keep checking the available memory.

### Abort/Restart the Chaos Experiment

- To stop the pod-delete experiment immediately, either delete the ChaosEngine resource or execute the following command:

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"stop"}}'`

- To restart the experiment, either re-apply the ChaosEngine YAML or execute the following command:

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"active"}}'`

### Check Chaos Experiment Result

- Check whether the application is resilient to the memory hog, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-node-memory-hog -n <application-namespace>`

## Node Memory Hog Experiment Demo

- A sample recording of this experiment execution is provided [here](https://www.youtube.com/watch?v=ECxlWgQ8F5w).
