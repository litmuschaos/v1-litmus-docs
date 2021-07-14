---
id: ebs-loss-by-id
title: EBS Loss By ID Experiment Details
sidebar_label: EBS Loss By ID
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
    <td> Kube AWS </td>
    <td> EBS volume loss by ID against specified application </td>
    <td> EKS </td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `ebs-loss-by-id` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/kube-aws/ebs-loss-by-id/experiment.yaml)
- Ensure that you have sufficient AWS access to attach or detach an ebs volume for the instance.
- Ensure the target volume to detach should not be the root volume for the instance.
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

- Application pods are healthy before chaos injection
- EBS volume is attached to the instance.

## Exit-Criteria

-  Application pods are healthy post chaos injection 
-  EBS volume is attached to the instance.

## Details

-  Causes chaos to disrupt state of ebs volume by detaching it from the node/ec2 instance for a certain chaos duration using volume id.
-  In case of EBS persistent volumes, the volumes can get self-attached and experiment skips the re-attachment step.
-  Tests deployment sanity (replica availability & uninterrupted service) and recovery workflows of the application pod.

## Integrations

-   EBS Loss by id can be effected using the chaos library: `litmus`, which makes use of aws sdk to attach/detach an ebs volume from the target instance. 
    specified capacity on the node.
-   The desired chaoslib can be selected by setting the above options as value for the env variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/kube-aws/ebs-loss-by-id/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ebs-loss-by-id-sa
  namespace: default
  labels:
    name: ebs-loss-by-id-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ebs-loss-by-id-sa
  labels:
    name: ebs-loss-by-id-sa
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
  name: ebs-loss-by-id-sa
  labels:
    name: ebs-loss-by-id-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ebs-loss-by-id-sa
subjects:
- kind: ServiceAccount
  name: ebs-loss-by-id-sa
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
     <td> EBS_VOLUME_ID </td>
    <td> Comma separated list of volume IDs subjected to ebs detach chaos</td>
    <td> Mandatory </td>
    <td>  </td>
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
    <td> REGION </td>
    <td> The region name for the target volumes</td>
    <td> Optional </td>
    <td> </td>
  </tr>
  <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple volumes</td>
    <td> Optional </td>
    <td> Default value: parallel. Supported: serial, parallel </td>
  </tr>  
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before and after injection of chaos in sec </td>
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

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/kube-aws/ebs-loss-by-id/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  engineState: 'active'
  chaosServiceAccount: ebs-loss-by-id-sa
  experiments:
    - name: ebs-loss-by-id
      spec:
        components:
          env: 
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '30'

            # set chaos duration (in sec) as desired
            - name: CHAOS_INTERVAL
              value: '30'              

            # set target ebs volume ID  
            - name: EBS_VOLUME_ID
              value: ''

            # provide the region name of the instance
            - name: REGION
              value: ''
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- View the status of the pods as they are subjected to ebs loss. 

  `watch -n 1 kubectl get pods -n <application-namespace>`
  
- Monitor the attachment status for ebs volume from AWS CLI.

  `aws ec2 describe-volumes --volume-ids <vol-id>`

-  You can also use aws console to keep a watch over ebs attachment status.   

### Abort/Restart the Chaos Experiment

- To stop the ebs-loss-by-id experiment immediately, either delete the ChaosEngine resource or execute the following command: 

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"stop"}}'` 

- To restart the experiment, either re-apply the ChaosEngine YAML or execute the following command: 

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"active"}}'`

### Check Chaos Experiment Result

- Check whether the application is resilient to the ebs loss, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-ebs-loss-by-id -n <application-namespace>`

### EBS Loss Experiment Demo

- A sample recording of this experiment execution will be added soon.
