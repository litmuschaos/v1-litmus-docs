---
id: node-taint
title: Node Taint Experiment Details
sidebar_label: Node Taint
---
------

## Experiment Metadata

<table>
  <tr>
    <th> Type </th>
    <th> Description  </th>
    <th> Tested K8s Platform </th>
  </tr>
  <tr>
    <td> Generic </td>
    <td> Taint the node where application pod is scheduled. </td>
    <td> GKE, AWS, Packet(Kubeadm), Konvoy(AWS), EKS, AKS </td>
  </tr>
</table>

## Prerequisites

- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `node-taint` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/1.9.1?file=charts/generic/node-taint/experiment.yaml)
- Ensure that the node specified in the experiment ENV variable `TARGET_NODE` (the node which will be tainted) should be cordoned before execution of the chaos experiment (before applying the chaosengine manifest) to ensure that the litmus experiment runner pods are not scheduled on it / subjected to eviction. This can be achieved with the following steps: 

  - Get node names against the applications pods: `kubectl get pods -o wide`
  - Cordon the node `kubectl cordon <nodename>` 

## Entry Criteria

- Application pods are healthy on the respective Nodes before chaos injection

## Exit Criteria

- Target nodes are in Ready state post chaos injection
- Application pods are healthy on the respective Nodes after chaos injection

## Details

- This experiment taint the node where application pod is running and verifies if it is scheduled on another available node.
- In the end of experiment it remove the taints from the specified node so that it can be utilised in future.
- After experiment ends, you may manually uncordon the specified node so that it can be utilised in future.

## Integrations

- Taint node can be effected using the chaos library: `litmus`
- The desired chaos library can be selected by setting `litmus` as value for the env variable `LIB` 

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/node-taint/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: node-taint-sa
  namespace: default
  labels:
    name: node-taint-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-taint-sa
  labels:
    name: node-taint-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: ["","litmuschaos.io","batch","extensions"]
  resources: ["pods","jobs","events","chaosengines","pods/log","daemonsets","pods/eviction","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update","delete"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["patch","get","list","update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-taint-sa
  labels:
    name: node-taint-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: node-taint-sa
subjects:
- kind: ServiceAccount
  name: node-taint-sa
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
    <th> Specify In ChaosEngine </th>
    <th> Notes </th>
  </tr>
  <tr>
    <td> TARGET_NODE </td>
    <td> Name of the node to be tainted  </td>
    <td> Mandatory  </td>
    <td> </td>
  </tr>
  <tr>
    <td> TAINT_LABEL </td>
    <td> Label and effect to be tainted on application node </td>
    <td> Mandatory </td>
    <td> </td>
  </tr>
  <tr>
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (seconds)  </td>
    <td> Optional </td>
    <td> Defaults to 60s </td>
  </tr>
   <tr>
    <td> LIB  </td>
    <td> The chaos lib used to inject the chaos </td>
    <td> Optional </td>
    <td> Defaults to `litmus` </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before injection of chaos in sec </td>
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

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/node-taint/engine.yaml yaml)
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
  #ex. values: ns1:name=percona,ns2:run=nginx 
  auxiliaryAppInfo: ''
  appinfo:
    appns: 'default'
    applabel: 'app=nginx'
    appkind: 'deployment'
  chaosServiceAccount: node-taint-sa
  monitoring: false
  # It can be delete/retain
  jobCleanUpPolicy: 'delete'
  experiments:
    - name: node-taint
      spec:
        components:
          nodeSelector: 
            # provide the node labels
            kubernetes.io/hostname: 'node02'        
          env:
            # set node name
            - name: TARGET_NODE
              value: 'node-01'
              
             # set taint label & effect
             # key=value:effect or key:effect
            - name: TAINTS
              value: 'node.kubernetes.io/unreachable:NoExecute'
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- Set up a watch on the applications originally scheduled on the affected node and verify whether they are rescheduled on the other nodes in the Kubernetes Cluster.

  `watch kubectl get pods,nodes --all-namespaces `

### Check Chaos Experiment Result

- Check whether the application is resilient to the node taint, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-node-taint -n <application-namespace>`

## Post Chaos Steps

- In the beginning of experiment, we cordon the node so that chaos-pod won't schedule on the same node (to which we are going to taint) because for some taint with `NoExecute` effect the pods may get scheduled to other nodes(restarted). 
After experiment ends you can manually uncordon the application node so that it can be utilised in future.

  `kubectl uncordon <node-name>`

## Node Taint Experiment Demo [TODO]

- A sample recording of this experiment execution is provided here.   
