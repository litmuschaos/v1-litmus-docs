---
id: drain-node
title: Drain Node Experiment Details
sidebar_label: Drain Node
---
------

## Experiment Metadata

| Type      | Description                                  | Tested K8s Platform                                               |
| ----------| -------------------------------------------- | ------------------------------------------------------------------|
| Generic   | Drain the node where application pod is scheduled. |  GKE, Konvoy(AWS), Packet(Kubeadm), Minikube|

## Prerequisites

- Ensure that the Litmus Chaos Operator is running. If not, install from [here](https://github.com/litmuschaos/chaos-operator/blob/master/deploy/operator.yaml)
- Ensure that the `drain-node` experiment resource is available in the cluster by `kubectl get chaosexperiments` command. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/drain-node)

## Entry Criteria

- Application pods are healthy on the respective Nodes before chaos injection

## Exit Criteria

- Target nodes are in Ready state post chaos injection

## Details

- This experiment drains the node where application pod is running and verifies if it is scheduled on another available node.
- In the end of experiment it uncordons the specified node so that it can be utilised in future.


## Integrations

- Drain node can be effected using the chaos library: `litmus`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo`
- Override the experiment tunables if desired 

#### Supported Experiment Tunables

<table>
<tr>
<th>  Variables </th>
<th>  Description </th>
<th> Type  </th>
<th> Notes </th>
</tr>
<tr>
<td> APP_NODE </td>
<td> Name of the node to drain  </td>
<td> Mandatory  </td>
<td> </td>
</tr>
<tr>
<td> TOTAL_CHAOS_DURATION </td>
<td> The time duration for chaos insertion (seconds)  </td>
<td> Optional </td>
<td> Defaults to 60s </td>
</tr>
</table>

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  chaosType: 'infra'  # It can be app/infra
  auxiliaryAppInfo: "ns1:name=percona,ns2:run=nginx"
  appinfo:
    appns: default
    applabel: 'app=nginx'
    appkind: deployment
  chaosServiceAccount: nginx-sa
  monitoring: false
  jobCleanUpPolicy: delete
  experiments:
    - name: drain-node
      spec:
        components:
           # set node name
          - name: APP_NODE
            value: 'node-1'
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress

- Set up a watch on the applications originally scheduled on the affected node and verify whether they are rescheduled on the other nodes in the Kubernetes Cluster.

  `watch kubectl get pods,nodes --all-namespaces `

### Check Chaos Experiment Result

- Check whether the application is resilient to the node drain, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-drain-node -n <application-namespace>`

## Drain Node Experiment Demo [TODO]

- A sample recording of this experiment execution is provided here.   