---
id: gcp-vm-disk-loss
title: GCP VM Disk Loss Experiment Details
sidebar_label: GCP VM Disk Loss
---
------

## Experiment Metadata

<table>
  <tr>
    <th> Type </th>
    <th>  Description  </th>
    <th> Tested K8s Platform </th>
  </tr>
  <tr>
    <td> GCP </td>
    <td> Causes loss of a non-boot storage persistent disk from a GCP VM instance for a specified duration of time </td>
    <td> GKE, Minikube </td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `gcp-vm-disk-loss` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/gcp/gcp-vm-disk-loss/experiment.yaml)
- Ensure that your service account has an editor access or owner access for the GCP project.
- Ensure the target disk volume to be detached should not be the root volume its instance.
- Ensure to create a Kubernetes secret having the GCP service account credentials in the default namespace. A sample secret file looks like:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloud-secret
type: Opaque
stringData:
  type: 
  project_id: 
  private_key_id: 
  private_key: 
  client_email: 
  client_id: 
  auth_uri: 
  token_uri: 
  auth_provider_x509_cert_url: 
  client_x509_cert_url: 
```

## Entry-Criteria

- Disk volumes are attached to their respective instances

## Exit-Criteria

- Disk volumes are attached to their respective instances

## Details

-  Causes chaos to disrupt state of GCP persistent disk volume by detaching it from its VM instance for a certain chaos duration using the disk name.

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/gcp/gcp-vm-disk-loss/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gcp-vm-disk-loss-sa
  namespace: default
  labels:
    name: gcp-vm-disk-loss-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gcp-vm-disk-loss-sa
  labels:
    name: gcp-vm-disk-loss-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: [""]
  resources: ["pods","events","secrets"]
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
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: gcp-vm-disk-loss-sa
  labels:
    name: gcp-vm-disk-loss-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: gcp-vm-disk-loss-sa
subjects:
- kind: ServiceAccount
  name: gcp-vm-disk-loss-sa
  namespace: default
```

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`. It is an optional parameter for infra level experiment.
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo`
- Override the experiment tunables if desired in `experiments.spec.components.env`
- To understand the values to provided in a ChaosEngine specification, refer [ChaosEngine Concepts](chaosengine-concepts.md)

#### Supported Experiment Tunables

<table>
  <tr>
    <th> Variables </th>
    <th> Description </th>
    <th> Specify In ChaosEngine </th>
    <th> Notes </th>
  </tr>
  <tr> 
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (sec) </td>
    <td> Optional </td>
    <td> Defaults to 30s </td>
  </tr>
  <tr> 
    <td> CHAOS_INTERVAL </td>
    <td> The time duration between the attachment and detachment of the volumes (sec) </td>
    <td> Optional </td>
    <td> Defaults to 30s </td>
  </tr>
  <tr> 
    <td> GCP_PROJECT_ID </td>
    <td> The ID of the GCP Project of which the disk volumes are a part of </td>
    <td> Mandatory </td>
    <td> All the target disk volumes should belong to a single GCP Project </td>
  </tr>
  <tr> 
    <td> DISK_VOLUME_NAMES </td>
    <td> Target non-boot persistent disk volume names</td>
    <td> Mandatory </td>
    <td> Multiple disk volume names can be provided as disk1,disk2,... </td>
  </tr>  
  <tr>
    <td> DISK_ZONES </td>
    <td> The zones of respective target disk volumes </td>
    <td> Mandatory </td>
    <td> Provide the zone for every target disk name as zone1,zone2... in the respective order of <code>DISK_VOLUME_NAMES</code>  </td>
  </tr>
  <tr>
    <td> DEVICE_NAMES </td>
    <td> The device names of respective target disk volumes </td>
    <td> Mandatory </td>
    <td> Provide the device name for every target disk name as deviceName1,deviceName2... in the respective order of <code>DISK_VOLUME_NAMES</code>  </td>
  </tr> 
  <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple instance</td>
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

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/gcp/gcp-vm-disk-loss/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: gcp-disk-chaos
  namespace: default
spec:
  # It can be active/stop
  engineState: 'active'
  chaosServiceAccount: gcp-vm-disk-loss-sa
  experiments:
    - name: gcp-vm-disk-loss
      spec:
        components:
          env:
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '30'

            # set chaos interval (in sec) as desired
            - name: CHAOS_INTERVAL
              value: '30'

            # set the GCP project id
            - name: GCP_PROJECT_ID
              value: ''

            # set the disk volume name(s) as comma seperated values 
            # eg. volume1,volume2,...
            - name: DISK_VOLUME_NAMES
              value: ''
              
            # set the disk zone(s) as comma seperated values in the corresponding 
            # order of DISK_VOLUME_NAME  
            # eg. zone1,zone2,...
            - name: DISK_ZONES
              value: ''
            
            # set the device name(s) as comma seperated values in the corresponding 
            # order of DISK_VOLUME_NAME 
            # eg. device1,device2,...
            - name: DEVICE_NAMES
              value: ''
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) section to identify the root cause and fix the issues.

### Watch Chaos progress
  
- Monitor the attachment status for ebs volume from AWS CLI.

  `gcloud compute disks describe DISK_NAME --zone=DISK_ZONE`

- GCP console can also be used to monitor the disk volume attachment status.   

### Check Chaos Experiment Result

- Check whether the application is resilient to the GCP disk loss, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult gcp-disk-chaos-gcp-vm-disk-loss`

### EBS Loss Experiment Demo

- A sample recording of this experiment execution will be added soon.
