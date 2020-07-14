---
id: docker-service-kill
title: Docker Service Kill Experiment Details
sidebar_label: Docker Service Kill
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
    <td> Kills the docker service on the application node to check the resiliency. </td>
    <td> GKE </td>
  </tr>
</table>

## Prerequisites

- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `docker-service-kill` experiment resource is available in the cluster  by executing                         `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/1.6.0?file=charts/generic/docker-service-kill/experiment.yaml)

## Entry Criteria

- Application pods should be healthy before chaos injection.

## Exit Criteria

- Application pods and the node should be healthy post chaos injection.

## Details

- This experiment Causes the application to become unreachable on account of node turning unschedulable (NotReady) due to docker service kill.
- The docker service has been stopped/killed on a node to make it unschedulable for a certain duration i.e `TOTAL_CHAOS_DURATION`. The application node should be healthy after the chaos injection and the services should be reaccessable.
- The application implies services. Can be reframed as:
Test application resiliency upon replica getting unreachable caused due to docker service down.

## Integrations

- Docker Service Kill can be effected using the chaos library: `litmus` 
- The desired chaos library can be selected by setting `litmus` as value for the env variable `LIB` 

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/docker-service-kill/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: docker-service-kill-sa
  namespace: default
  labels:
    name: docker-service-kill-sa
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: docker-service-kill-sa
  labels:
    name: docker-service-kill-sa
rules:
- apiGroups: ["","litmuschaos.io","batch","apps"]
  resources: ["pods","jobs","pods/log","events","chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update","delete"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get","list"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: docker-service-kill-sa
  labels:
    name: docker-service-kill-sa
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: docker-service-kill-sa
subjects:
- kind: ServiceAccount
  name: docker-service-kill-sa
  namespace: default
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- Setting up a watch over the nodes getting not schedulable in the Kubernetes Cluster
  `watch kubectl nodes`

### Check Chaos Experiment Result

- Check whether the application is resilient after the docker service kill, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-docker-service-kill -n <application-namespace>`

## Docker Service Kill Demo [TODO]

- A sample recording of this experiment execution is provided here.
