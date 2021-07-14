---
id: gcp-vm-instance-stop
title: GCP VM Instance Stop Experiment Details
sidebar_label: GCP VM Instance Stop
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
    <td> GCP </td>
    <td> Stops GCP VM instances and GKE nodes for a specified duration of time and later restarts them </td>
    <td> GKE, Minikube </td>
  </tr>
</table>

### WARNING
```
If the target GCP VM instance is a part of a self-managed nodegroup:
Make sure to drain the target node if any application is running on it and also ensure to cordon the target node before running the experiment so that the experiment pods do not schedule on it. 
```
## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `gcp-vm-instance-stop` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/gcp/gcp-vm-instance-stop/experiment.yaml)
- Ensure that you have sufficient GCP permissions to stop and start the GCP VM instances. 
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

-   VM instance is healthy before chaos injection.

## Exit-Criteria

-   VM instance is healthy post chaos injection.

## Details

-   Causes termination of a GCP VM instance by instance name or list of instance names before bringing it back to the running state after the specified chaos duration. 
-   It helps to check the performance of the application/process running on the VM instance.
-   When the `AUTO_SCALING_GROUP` is enable then the experiment will not try to start the instance post chaos, instead it will check the addition of the new node instances to the cluster.

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/gcp/gcp-vm-instance-stop/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gcp-vm-instance-stop-sa
  namespace: default
  labels:
    name: gcp-vm-instance-stop-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gcp-vm-instance-stop-sa
  labels:
    name: gcp-vm-instance-stop-sa
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
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get","list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: gcp-vm-instance-stop-sa
  labels:
    name: gcp-vm-instance-stop-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: gcp-vm-instance-stop-sa
subjects:
- kind: ServiceAccount
  name: gcp-vm-instance-stop-sa
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
    <td> The total time duration for chaos insertion (sec) </td>
    <td> Optional </td>
    <td> Defaults to 30s </td>
  </tr>
  <tr> 
    <td> CHAOS_INTERVAL </td>
    <td> The interval (in sec) between successive instance termination </td>
    <td> Optional </td>
    <td> Defaults to 30s </td>
  </tr>  
  <tr> 
    <td> AUTO_SCALING_GROUP </td>
    <td> Set to <code>enable</code> if the target instance is the part of a auto-scaling group </td>
    <td> Optional </td>
    <td> Defaults to <code>disable</code> </td>
  </tr>  
  <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple instance </td>
    <td> Optional </td>
    <td> Default value: parallel. Supported: serial, parallel </td>
  </tr>  
  <tr> 
    <td> GCP_PROJECT_ID </td>
    <td> GCP project ID to which the VM instances belong </td>
    <td> Required </td>
    <td> All the VM instances must belong to a single GCP project </td>
  </tr>
  <tr> 
    <td> VM_INSTANCE_NAMES </td>
    <td> Name of target VM instances </td>
    <td> Required </td>
    <td> Multiple instance names can be provided as instance1,instance2,... </td>
  </tr>
  <tr>
    <td> INSTANCE_ZONES </td>
    <td> The zones of the target VM instaces </td>
    <td> Required </td>
    <td> Zone for every instance name has to be provided as zone1,zone2,... in the same order of <code>VM_INSTANCE_NAMES</code> </td>
  </tr> 
  <tr>
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name </td>
    <td> Optional </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>

</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/gcp/gcp-vm-instance-stop/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: gcp-vm-chaos
spec:
  engineState: 'active'
  chaosServiceAccount: gcp-vm-instance-stop-sa
  experiments:
    - name: gcp-vm-instance-stop
      spec:
        components:
          env:
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '30'

            # set chaos interval (in sec) as desired
            - name: CHAOS_INTERVAL
              value: '30'
            
            # Instance name of the target vm instance(s)
            # Multiple instance names can be provided as comma separated values ex: instance1,instance2
            - name: VM_INSTANCE_NAMES
              value: ''
            
            # GCP project ID to which the vm instances belong
            - name: GCP_PROJECT_ID
              value: ''

            # Instance zone(s) of the target vm instance(s)
            # If more than one instance is targetted, provide zone for each in the order of their 
            # respective instance name in VM_INSTANCE_NAME as comma separated values ex: zone1,zone2
            - name: INSTANCE_ZONES
              value: ''

            # enable it if the target instance is a part of self-managed auto scaling group.
            - name: AUTO_SCALING_GROUP
              value: 'disable'              
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) section to identify the root cause and fix the issues.

### Watch Chaos progress
  
- Monitor the VM Instance status using GCP Cloud SDK:

  `gcloud compute instances describe INSTANCE_NAME --zone=INSTANCE_ZONE`

-  GCP console can also be used to monitor the instance status.

### Check Chaos Experiment Result

- Check whether the application is resilient to the gcp-vm-instance-stop, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult gcp-vm-chaos-gcp-vm-instance-stop`

### EC2 Terminate Experiment Demo

- A sample recording of this experiment execution will be added soon.
