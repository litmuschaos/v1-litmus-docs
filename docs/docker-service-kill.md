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
- Ensure that the `docker-service-kill` experiment resource is available in the cluster  by executing                         `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/1.5.0?file=charts/generic/docker-service-kill/experiment.yaml)

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

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
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
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (seconds) </td>
    <td> Optional </td>
    <td> Defaults to 90 </td>
  </tr>
   <tr>
    <td> LIB  </td>
    <td> The chaos lib used to inject the chaos </td>
    <td> Optional </td>
    <td> Defaults to `litmus` </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before & after injection of chaos in sec </td>
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

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/docker-service-kill/engine.yaml yaml)
```yaml

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
