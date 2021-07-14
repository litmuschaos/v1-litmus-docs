---
id: aws-ssm-chaos-by-tag
title: AWS SSM Chaos By Tag Experiment Details
sidebar_label: AWS SSM Chaos By Tag
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
    <td> AWS SSM </td>
    <td> Perform chaos on AWS EC2 instance using SSM docs and instance ID</td>
    <td> EKS </td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `aws-ssm-chaos-by-tag` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/aws-ssm/aws-ssm-chaos-by-tag/experiment.yaml)
- Ensure that you have the required AWS access and your target EC2 instances have attached an IAM instance profile. To know more checkout [Systems Manager Docs](https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-launch-managed-instance.html).
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

- AWS SSM Chaos By Tag contains chaos to disrupt the state of infra resources. The experiment can induce chaos on AWS EC2 instance using Amazon SSM Run Command This is carried out by using SSM Docs that defines the actions performed by Systems Manager on your managed instances (having SSM agent installed) which let you perform chaos experiments on the instances.

- Causes chaos (like stress, network, disk or IO) on AWS EC2 instances with given instance Tag using SSM docs for a certain chaos duration.
- For the default execution the experiment uses SSM docs for stress-chaos while you can add your own SSM docs using configMap (`.spec.definition.configMaps`) in ChaosExperiment CR. 
- Tests deployment sanity (replica availability & uninterrupted service) and recovery workflows of the target application pod(if provided).

## Integrations

-   AWS SSM Chaos can be effected using the chaos library: `litmus`, which makes use of aws sdk to run ssm command on an EC2 instance using instance Tag. 
-   The desired chaoslib can be selected by setting the above options as value for the env variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/aws-ssm/aws-ssm-chaos-by-tag/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-ssm-chaos-by-tag-sa
  namespace: default
  labels:
    name: aws-ssm-chaos-by-tag-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: aws-ssm-chaos-by-tag-sa
  labels:
    name: aws-ssm-chaos-by-tag-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: [""]
  resources: ["pods","events","secrets","configmaps"]
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
  name: aws-ssm-chaos-by-tag-sa
  labels:
    name: aws-ssm-chaos-by-tag-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: aws-ssm-chaos-by-tag-sa
subjects:
- kind: ServiceAccount
  name: aws-ssm-chaos-by-tag-sa
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
    <td> Optional </td>
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
    <td> AWS_SHARED_CREDENTIALS_FILE </td>
    <td> Provide the path for aws secret credentials</td>
    <td> Optional </td>
    <td> Defaults to <code>/tmp/cloud_config.yml</code> </td>
  </tr>
  <tr> 
    <td> DOCUMENT_NAME </td>
    <td> Provide the name of addded ssm docs (if not using the default docs)</td>
    <td> Optional </td>
    <td> Default to LitmusChaos-AWS-SSM-Doc</td>
  </tr>
  <tr> 
    <td> DOCUMENT_FORMAT </td>
    <td> Provide the format of the ssm docs. It can be YAML or JSON</td>>
    <td> Optional </td>
    <td> Defaults to <code>YAML</code> </td>
  </tr>
  <tr> 
    <td> DOCUMENT_TYPE </td>
    <td> Provide the document type of added ssm docs (if not using the default docs)</td>
    <td> Optional </td>
    <td> Defaults to <code>Command</code> </td>
  </tr>
  <tr> 
    <td> DOCUMENT_PATH </td>
    <td> Provide the document path if added using configmaps</td>
    <td> Optional </td>
    <td> Defaults to the litmus ssm docs path </td>
  </tr>
  <tr> 
    <td> INSTALL_DEPENDENCIES </td>
    <td> Select to install dependencies used to run stress-ng with default docs. It can be either True or False</td>
    <td> Optional </td>
    <td> Defaults to True </td>
  </tr>
  <tr> 
    <td> NUMBER_OF_WORKERS </td>
    <td> Provide the number of workers to run stress-chaos with default ssm docs</td>
    <td> Optional </td>
    <td> Defaults to 1 </td>
  </tr>
  <tr> 
    <td> MEMORY_PERCENTAGE </td>
    <td> Provide the memory consumption in percentage on the instance for default ssm docs</td>
    <td> Optional </td>
    <td> Defaults to 80 </td>
  </tr>
  <tr> 
    <td> CPU_CORE </td>
    <td> Provide the number of cpu cores to run stress-chaos on EC2 with default ssm docs</td>
    <td> Optional </td>
    <td> Defaults to 0. It means it'll consume all the available cpu cores on the instance </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before and after injection of chaos in sec </td>
    <td> Optional  </td>
    <td> </td>
  </tr>
  <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple instance</td>
    <td> Optional </td>
    <td> Default value: parallel. Supported: serial, parallel </td>
  </tr>
  <tr>
    <td> INSTANCE_AFFECTED_PERC </td>
    <td> The Percentage of total ec2 instance to target  </td>
    <td> Optional </td>
    <td> Defaults to 0 (corresponds to 1 instance), provide numeric value only </td>
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

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/aws-ssm/aws-ssm-chaos-by-tag/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  engineState: 'active'
  chaosServiceAccount: aws-ssm-chaos-by-tag-sa
  experiments:
    - name: aws-ssm-chaos-by-tag
      spec:
        components:
          env: 
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '60'

            # set chaos duration (in sec) as desired
            - name: CHAOS_INTERVAL
              value: '60'              

             # provide tag of the target ec2 instances
             # ex: team:devops (key:value)
            - name: EC2_INSTANCE_TAG
              value: ''

            # provide the region name of the target instances
            - name: REGION
              value: ''

             # provide the percentage of available memory to stress
            - name: MEMORY_PERCENTAGE
              value: '80'

            # provide the CPU chores to comsumed
            # 0 will consume all the available cpu cores
            - name: CPU_CORE
              value: '0'

             # Provide the name of ssm doc 
            # if not using the default stress docs  
            - name: DOCUMENT_NAME
              value: ''

            # Provide the type of ssm doc 
            # if not using the default stress docs  
            - name: DOCUMENT_TYPE
              value: ''

            # Provide the format of ssm doc
            # if not using the default stress docs  
            - name: DOCUMENT_FORMAT
              value: ''

            # Provide the path of ssm doc 
            # if not using the default stress docs  
            - name: DOCUMENT_PATH
              value: ''

             # if you want to install dependencies to run default ssm docs
            - name: INSTALL_DEPENDENCIES
              value: 'True'     
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- Monitor the command status

`aws ssm list-commands --command-id "command-ID"`

**Note:** To list down the ssm docs and command to get the command id check out the [AWS SSM userguide](https://docs.aws.amazon.com/systems-manager/latest/userguide/walkthrough-cli.html) 
  
- Monitor the ec2 state from AWS CLI.

  `aws ec2 describe-instance-status --instance-ids <instance-id>`

-  You can also use aws console to keep a watch over the instance state and the ssm command state.   

### Abort/Restart the Chaos Experiment

- To stop the aws-ssm-chaos-by-tag experiment immediately, either delete the ChaosEngine resource or execute the following command: 

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"stop"}}'` 

- To restart the experiment, either re-apply the ChaosEngine YAML or execute the following command: 

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"active"}}'`  

### Check Chaos Experiment Result

- Check whether the application is resilient to the aws-ssm-chaos-by-tag, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-aws-ssm-chaos-by-tag -n <application-namespace>`

### AWS SSM Chaos Experiment Demo

- A sample recording of this experiment execution will be added soon.
