---
id: ec2-terminate-by-id
title: EC2 Terminate By ID Experiment Details
sidebar_label: EC2 Terminate By ID
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
    <td> Kube AWS </td>
    <td> Termination of an EC2 instance by id for a certain chaos duration</td>
    <td> EKS </td>
  </tr>
</table>

### WARNING
```
If the target EC2 instance is a part of a self-managed nodegroup:
Make sure to drain the target node if any application is running on it and also ensure to cordon the target node before running the experiment so that the experiment pods do not schedule on it. 
```
## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `ec2-terminate-by-id` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/kube-aws/ec2-terminate-by-id/experiment.yaml)
- Ensure that you have sufficient AWS access to stop and start an ec2 instance. 
- Ensure to create a Kubernetes secret having the AWS access configuration(key) in the `CHAOS_NAMESPACE`. A sample secret file looks like:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloud-secret
type: Opaque
stringData:
  cloud_config.yml: |-
    # Add the cloud AWS credentials respectively
    [default]
    aws_access_key_id = XXXXXXXXXXXXXXXXXXX
    aws_secret_access_key = XXXXXXXXXXXXXXX
```

- If you change the secret key name (from `cloud_config.yml`) please also update the `AWS_SHARED_CREDENTIALS_FILE` 
ENV value on `experiment.yaml`with the same name.


## Entry-Criteria

-   EC2 instance is healthy before chaos injection.

## Exit-Criteria

-   EC2 instance is healthy post chaos injection.

## Details

-   Causes termination of an EC2 instance by instance ID or list of instance IDs before bringing it back to running state after the specified chaos duration. 
-   It helps to check the performance of the application/process running on the ec2 instance.
-   When the `MANAGED_NODEGROUP` is enable then the experiment will not try to start the instance post chaos instead it will check of the addition of the new node instance to the cluster.

## Integrations

-   EC2 Terminate can be effected using the chaos library: `litmus`, which makes use of aws sdk to start/stop an EC2 instance. 
-   The desired chaoslib can be selected by setting the above options as value for the env variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/kube-aws/ec2-terminate-by-id/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ec2-terminate-by-id-sa
  namespace: default
  labels:
    name: ec2-terminate-by-id-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ec2-terminate-by-id-sa
  labels:
    name: ec2-terminate-by-id-sa
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
  verbs: ["patch","get","list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ec2-terminate-by-id-sa
  labels:
    name: ec2-terminate-by-id-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ec2-terminate-by-id-sa
subjects:
- kind: ServiceAccount
  name: ec2-terminate-by-id-sa
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
    <td> EC2_INSTANCE_ID </td>
    <td> Instance ID of the target ec2 instance. Multiple IDs can also be provided as a comma(,) separated values</td>
    <td> Mandatory </td>
    <td> Multiple IDs can be provided as `id1,id2` </td>
  </tr>
  <tr> 
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The total time duration for chaos insertion (sec) </td>
    <td> Optional </td>
    <td> Defaults to 30s </td>
  </tr>
  <tr> 
    <td> CHAOS_INTERVAL </td>
    <td> The interval (in sec) between successive instance termination.</td>
    <td> Optional </td>
    <td> Defaults to 30s </td>
  </tr>  
  <tr> 
    <td> MANAGED_NODEGROUP </td>
    <td> Set to <code>enable</code> if the target instance is the part of self-managed nodegroups </td>
    <td> Optional </td>
    <td> Defaults to <code>disable</code> </td>
  </tr>  
  <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple instance</td>
    <td> Optional </td>
    <td> Default value: parallel. Supported: serial, parallel </td>
  </tr>  
  <tr>
    <td> REGION </td>
    <td> The region name of the target instace</td>
    <td> Optional </td>
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

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/kube-aws/ec2-terminate-by-id/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  engineState: 'active'
  chaosServiceAccount: ec2-terminate-by-id-sa
  experiments:
    - name: ec2-terminate-by-id
      spec:
        components:
          env: 
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '30'

            # set interval duration (in sec) as desired
            - name: CHAOS_INTERVAL
              value: '30'

             # Instance ID of the target ec2 instance
             # Multiple IDs can also be provided as comma separated values ex: id1,id2
            - name: EC2_INSTANCE_ID
              value: ''
              
            # provide the region name of the instance
            - name: REGION
              value: ''

            # enable it if the target instance is a part of self-managed nodegroup.
            - name: MANAGED_NODEGROUP
              value: 'disable'              
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress
  
- Monitor the ec2 state from AWS CLI.

  `aws ec2 describe-instance-status --instance-ids <instance-id>`

-  You can also use aws console to keep a watch over the instance state.   

### Check Chaos Experiment Result

- Check whether the application is resilient to the ec2-terminate-by-id, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-ec2-terminate-by-id -n <application-namespace>`

### EC2 Terminate Experiment Demo

- A sample recording of this experiment execution will be added soon.
