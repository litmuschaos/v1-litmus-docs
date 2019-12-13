---
id: disk-loss
title: Disk Loss Experiment Details
sidebar_label: Disk Loss
---
------
## Experiment Metadata

<table>
<tr>
<th> Type </th>
<th>  Description  </th>
<th> K8s Platform </th>
</tr>
<tr>
<td> Chaos </td>
<td> External Disk loss from the node </td>
<td> GKE/AWS </td>
</tr>
</table>

## Prerequisites
- Ensure that the Litmus Chaos Operator is running
- There should be administrative access to the platform on which the Kubernetes cluster is hosted, as the recovery of the affected could be manual. Example gcloud access to the project
- Ensure that the `disk-loss` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/api/chaos?file=charts/generic/disk-loss/experiment.yaml)
- Ensure to create a secret object having the gcloud/aws configuration in the namespace of 'CHAOS_NAMESPACE'.
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloud_secret
type: Opaque
stringData:
  cloud_config.yml: |-
  # Add the cloud configuration

```

## Entry-Criteria

-   The disk is healthy before chaos injection

## Exit-Criteria

-   The disk is healthy post chaos injection
-   If `APP_CHECK` is true, the application pod health is checked post chaos injection

## Details

-   In this experiment, the external disk is detached from the node and wait for the chaos duration.
- If there is any PV provisioner it will attach automatically, Else it will attach manually.
- This chaos experiment is support for GCP and AWS.

## Integrations

- Disk Loss can be effected using the chaos library: `litmus`
- The desired chaos library can be selected by setting `litmus` as value for the env variable LIB
- It uses imperative aws and gcloud command to attach and detach the disks

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)
- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired

### Supported Experiment Tunables for application

<table>
<tr>
<th> Parameter </th>
<th> Description  </th>
<th> Type </th>
</tr>
<tr>
<td> APP_CHECK </td>
<td> If it checks to true, the experiment will check the status of the application. </td>
<td> Optional </td>
</tr>
<tr>
<td> APP_NAMESPACE </td>
<td> Namespace in which application pods are deployed </td>
<td> Optional </td>
</tr>
<tr>
<td> APP_LABEL </td>
<td> Unique Labels in `key=value` format of application deployment </td>
<td> Optional </td>
</tr>
<tr>
<td> TOTAL_CHAOS_DURATION </td>
<td> The time duration for chaos insertion (sec) </td>
<td> Mandatory </td>
</tr>
<tr>
<td> CHAOS_NAMESPACE </td>
<td> This is a chaos namespace which will create all infra chaos resources in that namespace </td>
<td> Mandatory </td>
</tr>
<tr>
<td> CLOUD_PLATFORM </td>
<td> Cloud Platform name </td>
<td> Mandatory </td>
</tr>
<tr>
<td> PROJECT_ID </td>
<td> GCP project ID </td>
<td> Mandatory </td>
</tr>
<tr>
<td> NODE_NAME </td>
<td> Node name of the cluster </td>
<td> Mandatory </td>
</tr>
<tr>
<td> DISK_NAME </td>
<td> Disk Name of the node, it must be an external disk. </td>
<td> Mandatory </td>
</tr>
<tr>
<td> DEVICE_NAME </td>
<td> Enter the device name which you wanted to mount only for AWS. </td>
<td> Mandatory </td>
</tr>
<tr>
<td> ZONE_NAME </td>
<td> Zone Name of the node </td>
<td> Mandatory </td>
</tr>
<tr>
<td> CHAOSENGINE </td>
<td> ChaosEngine CR name associated with the experiment instance </td>
<td> Mandatory </td>
</tr>
<tr>
<td> CHAOS_SERVICE_ACCOUNT </td>
<td> Service account used by the litmus </td>
<td> Mandatory </td>
</tr>
</table>

## Sample ChaosEngine Manifest

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
    - name: disk-loss
      spec:
        components:
           # set chaos duration (in sec) as desired
          - name: TOTAL_CHAOS_DURATION
            value: '60'
          # set chaos platform as desired
          - name: PLATFORM
            value: 'GCP'
          # set app_check to check application state
          - name: APP_CHECK
            value: 'true'
          # Cloud Platform name
          - name: CHAOS_NAMESPACE
            value: 'default'
          # This is a chaos namespace which will create all infra chaos resources in that namespace
          - name: CLOUD_NAMESPACE
            value: 'default'
          # GCP project ID
          - name: PROJECT_ID
            value: 'litmus-demo-123'
          # Node name of the cluster
          - name: NODE_NAME
            value: 'demo-node-123'
          # Disk Name of the node, it must be an external disk.	
          - name: DISK_NAME
            value: 'demo-disk-123'
          # Enter the device name which you wanted to mount only for AWS.	
          - name: DEVICE_NAME
            value: ''
          # Zone Name of the node	
          - name: ZONE_NAME
            value: 'us-central1-a'
          # ChaosEngine CR name associated with the experiment instance	
          - name: CHAOSENGINE
            value: ''
          # Service account used by the litmus	
          - name: CHAOS_SERVICE_ACCOUNT
            value: ''
```
## Create the ChaosEngine Resource
- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

`kubectl apply -f chaosengine.yml`

## Watch Chaos progress
- Setting up a watch of the app which is using the disk in the Kubernetes Cluster

`watch kubectl get pods`

## Check Chaos Experiment Result
- Check whether the application is resilient to the disk loss, once the experiment (job) is completed. The ChaosResult resource name is derived like this: <ChaosEngine-Name>-<ChaosExperiment-Name>.

`kubectl describe chaosresult nginx-chaos-disk-loss -n <CHAOS_NAMESPACE>`
