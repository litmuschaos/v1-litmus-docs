---
id: azure-instance-stop
title: Azure Instance Stop Experiment Details
sidebar_label: Azure Instance Stop
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
    <td> Termination of an azure instance for a certain chaos duration</td>
    <td> EKS </td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.13
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `azure-instance-stop` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/kube-aws/azure-instance-stop/experiment.yaml)
- Ensure that you have sufficient Azure access to stop and start the an instance. 
- We will use azure [ file-based authentication ](https://docs.microsoft.com/en-us/azure/developer/go/azure-sdk-authorization#use-file-based-authentication) to connect with the instance using azure GO SDK in the experiment. For generating auth file run `az ad sp create-for-rbac --sdk-auth > azure.auth` Azure CLI command.
- Ensure to create a Kubernetes secret having the auth file created in the step in `CHAOS_NAMESPACE`. A sample secret file looks like:

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

- If you change the secret key name (from `azure.auth`) please also update the `AZURE_AUTH_LOCATION` 
ENV value on `experiment.yaml`with the same name.


## Entry-Criteria

-   Azure instance is healthy before chaos injection.

## Exit-Criteria

-   Azure instance is healthy post chaos injection.

## Details

-   Causes PowerOff an Azure instance before bringing it back to running state after the specified chaos duration. 
-   It helps to check the performance of the application/process running on the instance.

## Integrations

-   Azure Instance Stop can be effected using the chaos library: `litmus`, which makes use of azure sdk to start/stop an instance. 
-   The desired chaoslib can be selected by setting the above options as value for the env variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/azure/azure-instance-stop/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: azure-instance-stop-sa
  namespace: default
  labels:
    name: azure-instance-stop-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: azure-instance-stop-sa
  labels:
    name: azure-instance-stop-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: ["","litmuschaos.io","batch"]
  resources: ["pods","jobs","secrets","events","pods/log","pods/exec","chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update","delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: azure-instance-stop-sa
  labels:
    name: azure-instance-stop-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: azure-instance-stop-sa
subjects:
- kind: ServiceAccount
  name: azure-instance-stop-sa
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
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name.</td>
    <td> Optional </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>

</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/azure/azure-instance-stop/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  annotationCheck: 'false'
  engineState: 'active'
  chaosServiceAccount: azure-instance-stop-sa
  monitoring: false
  # It can be retain/delete
  jobCleanUpPolicy: 'delete'
  experiments:
    - name: azure-instance-stop
      spec:
        components:
          env: 
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '30'

            # provide the target instance name
            - name: AZURE_INSTANCE_NAME
              value: ''

            # provide the resource group of the instance
            - name: RESOURCE_GROUP
              value: ''

```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress
  
- Monitor the azure state from Azure CLI.

  `az vm list -d -o table --query "[?name=='<vm-name>']"` (vm name without <>)

-  You can also use Azure console to keep a watch over the instance state.   

### Abort/Restart the Chaos Experiment

- To stop the azure-instance-terminate experiment immediately, either delete the ChaosEngine resource or execute the following command:

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"stop"}}'`

- To restart the experiment, either re-apply the ChaosEngine YAML or execute the following command:

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"active"}}'`

### Check Chaos Experiment Result

- Check whether the application is resilient to the azure-instance-stop, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-azure-instance-stop -n <chaos-namespace>`

### EC2 Stop Experiment Demo

- A sample recording of this experiment execution will be added soon.
