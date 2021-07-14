---
id: azure-disk-loss
title: Azure Disk Loss Experiment Details
sidebar_label: Azure Disk Loss
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
    <td> Azure </td>
    <td> Disk loss for a certain chaos duration</td>
    <td>  </td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in the operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `azure-disk-loss` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/kube-aws/azure-disk-loss/experiment.yaml)
- Ensure that you have sufficient Azure access to update the VM properties. 
- We will use azure [ file-based authentication ](https://docs.microsoft.com/en-us/azure/developer/go/azure-sdk-authorization#use-file-based-authentication) to connect with the instance using azure GO SDK in the experiment. For generating auth file, run `az ad sp create-for-rbac --sdk-auth > azure.auth` Azure CLI command.
- Ensure to create a Kubernetes secret having the auth file created in the step in `CHAOS_NAMESPACE`. A sample secret file looks like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloud-secret
type: Opaque
stringData:
  azure.auth: |-
    {
      "clientId": "XXXXXXXXX",
      "clientSecret": "XXXXXXXXX",
      "subscriptionId": "XXXXXXXXX",
      "tenantId": "XXXXXXXXX",
      "activeDirectoryEndpointUrl": "XXXXXXXXX",
      "resourceManagerEndpointUrl": "XXXXXXXXX",
      "activeDirectoryGraphResourceId": "XXXXXXXXX",
      "sqlManagementEndpointUrl": "XXXXXXXXX",
      "galleryEndpointUrl": "XXXXXXXXX",
      "managementEndpointUrl": "XXXXXXXXX"
    }
```

- If you change the secret key name (from `azure.auth`), please also update the `AZURE_AUTH_LOCATION` 
ENV value on `experiment.yaml` with the same name.


## Entry-Criteria

-   Application pods are healthy before chaos injection
-   Virtual disks are attached to the instance before chaos injection.

## Exit-Criteria

-   Application pods are healthy post chaos injection
-   Virtual disks are attached to the instance after chaos injection.

## Details

-   Causes chaos to disrupt the state of the virtual disk by detaching it from the VM instance for a certain chaos duration using disk name and VM instance name.
-   It helps to check the performance of the application/process running on the instance.

## Integrations

-   Azure Disk Loss can be effected using the chaos library: `litmus`, which makes use of azure sdk to attach/detach a disk. 
-   The desired chaoslib can be selected by setting the above option as a value for the env variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer to [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/azure/azure-disk-loss/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: azure-disk-loss-sa
  namespace: default
  labels:
    name: azure-disk-loss-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: azure-disk-loss-sa
  labels:
    name: azure-disk-loss-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: ["","litmuschaos.io","batch"]
  resources: ["pods","jobs","secrets","events","pods/log","pods/exec","chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update","delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: azure-disk-loss-sa
  labels:
    name: azure-disk-loss-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: azure-disk-loss-sa
subjects:
- kind: ServiceAccount
  name: azure-disk-loss-sa
  namespace: default
```

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`. It is an optional parameter for an infra level experiment.
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo`
- Override the experiment tunables if desired in `experiments.spec.components.env`
- To understand the values provided in a ChaosEngine specification, refer to [ChaosEngine Concepts](chaosengine-concepts.md)

#### Supported Experiment Tunables

<table>
  <tr>
    <th> Variables </th>
    <th> Description </th>
    <th> Specify In ChaosEngine </th>
    <th> Notes </th>
  </tr>
  <tr> 
    <td> VIRTUAL_DISK_NAMES </td>
    <td> Name of virtual disks to target.</td>
    <td> Mandatory </td>
    <td> Provide comma separated names for multiple disks</td>
  </tr>
  <tr> 
    <td> AZURE_INSTANCE_NAME </td>
    <td> Instance name of the target azure instance.</td>
    <td> Mandatory </td>
    <td>  </td>
  </tr>
  <tr>
    <td> RESOURCE_GROUP </td>
    <td> The resource group of the target instance</td>
    <td> Mandatory </td>
    <td> </td>
  </tr> 
  <tr> 
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (sec) </td>
    <td> Optional </td>
    <td> Defaults to 30s </td>
  </tr>
  <tr>
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name.</td>
    <td> Optional </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>

</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/azure/azure-disk-loss/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
spec:
  # It can be active/stop
  engineState: 'active'
  chaosServiceAccount: azure-disk-loss-sa
  # It can be delete/retain
  jobCleanUpPolicy: 'delete'
  experiments:
    - name: azure-disk-loss
      spec:
        components:
          env:
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '30'

            # set chaos interval (in sec) as desired
            - name: CHAOS_INTERVAL
              value: '30'

            # provide the resource group of the instance
            - name: RESOURCE_GROUP
              value: ''

            # provide the target instance name
            - name: AZURE_INSTANCE_NAME
              value: ''

            # provide the virtual disk names (comma separated if multiple)
            - name: VIRTUAL_DISK_NAMES
              value: ''

            # provide the sequence type for the run. Options: serial/parallel
            - name: SEQUENCE
              value: 'parallel'

```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress
  
- Monitor the disk state from Azure CLI.

  `az disk list -o table --query "[?name=='<disk-name>']"` (vm name without <>)

-  You can also use the Azure console to keep a watch over the disk status.   

### Check Chaos Experiment Result

- Check whether the application is resilient to the azure-disk-loss, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-azure-disk-loss -n <chaos-namespace>`

### Azure Disk Loss Experiment Demo

- A sample recording of this experiment execution will be added soon.
{"mode":"full","isActive":false}