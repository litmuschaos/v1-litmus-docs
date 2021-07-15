---
id: node-poweroff
title: Node Poweroff Experiment Details
sidebar_label: Node Poweroff
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
    <td> Generic </td>
    <td> Powers off the target node </td>
    <td> Kubevirt VMs </td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `node-poweroff` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/generic/node-poweroff/experiment.yaml)
- Create a Kubernetes secret named `id-rsa` where the experiment will run, where its contents will be the private SSH key for `SSH_USER` used to connect to the node that hosts the target pod in the secret field `ssh-privatekey`. A sample secret is shown below:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: id-rsa
type: kubernetes.io/ssh-auth
stringData:
  ssh-privatekey: |-
    # SSH private key for ssh contained here
```

Creating the RSA key pair for remote SSH access should be a trivial exercise for those who are already familiar with an ssh client, which entails the following actions:
1. Create a new key pair and store the keys in a file named `my-id-rsa-key` and `my-id-rsa-key.pub` for the private and public keys respectively: 
```
ssh-keygen -f ~/my-id-rsa-key -t rsa -b 4096
```
2. For each node available, run this following command to copy the public key of `my-id-rsa-key`:
```
ssh-copy-id -i my-id-rsa-key user@node
```

 For further details, please check this [documentation](https://www.ssh.com/ssh/keygen/). Once you have copied the public key to all nodes and created the secret described earlier, you are ready to start your experiment.

## Entry-Criteria

-  Application pods should be healthy before chaos injection.
-  Target Nodes should be in Ready state before chaos injection.

## Exit-Criteria

- Application pods should be healthy after chaos injection.
- Target Nodes should be in Ready state after chaos injection.

## Details

-   Causes chaos to disrupt state of node by powering it off. 
-   Tests deployment sanity (replica availability & uninterrupted service) and recovery workflows of the application pod

## Integrations

-   Node Poweroff can be effected using the chaos library: `litmus`.

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/node-poweroff/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: node-poweroff-sa
  namespace: default
  labels:
    name: node-poweroff-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-poweroff-sa
  labels:
    name: node-poweroff-sa
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
  name: node-poweroff-sa
  labels:
    name: node-poweroff-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: node-poweroff-sa
subjects:
- kind: ServiceAccount
  name: node-poweroff-sa
  namespace: default
```

***Note:*** In case of restricted systems/setup, create a PodSecurityPolicy(psp) with the required permissions. The `chaosServiceAccount` can subscribe to work around the respective limitations. An example of a standard psp that can be used for litmus chaos experiments can be found [here](https://docs.litmuschaos.io/docs/next/litmus-psp/).

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`. It is an optional parameter for infra level experiment.
- Populate the `TARGET_NODE` and `TARGET_NODE_IP` in the `experiments.spec.components.env` section. Note that the environment values take precedence over the `spec.appinfo` fields.
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo` 
- Override the extra experiment tunables if desired in `experiments.spec.components.env`
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
    <td> LIB_IMAGE  </td>
    <td> The image used to poweroff the node </td>
    <td> Optional </td>
    <td> Defaults to `litmuschaos/go-runner:latest` </td>
  </tr>
  <tr>
    <td> SSH_USER  </td>
    <td> Name of ssh user </td>
    <td> Optional </td>
    <td> Defaults to `root` </td>
  </tr>
  <tr>
    <td> TARGET_NODE </td>
    <td> Name of target node, subjected to chaos. If not provided, the experiment will lookup the node that hosts the pod running based on the `appInfo` details section in the `ChaosEngine`. If provided, it also requires the `TARGET_NODE_IP` to be populated</td>
    <td> Optional </td>
    <td> Defaults to empty </td>
  </tr>
  <tr>
    <td> NODE_LABEL </td>
    <td> It contains node label, which will be used to filter the target nodes if TARGET_NODE ENV is not set </td>
    <td> Optional </td>
    <td> </td>
  </tr>
  <tr>
    <td> TARGET_NODE_IP </td>
    <td> Internal IP of the target node, subjected to chaos. If not provided, the experiment will lookup the node IP that hosts the pod running based on the `appInfo` details section in the `ChaosEngine`. If provided, it also requires `TARGET_NODE` to be populated.</td>
    <td> Optional </td>
    <td> Defaults to empty </td>
  </tr>
  <tr>
    <td> REBOOT_COMMAND  </td>
    <td> Command used for reboot </td>
    <td> Optional </td>
    <td> Defaults to `-o ServerAliveInterval=1 -o ServerAliveCountMax=1 "sudo systemctl poweroff --force --force" ; true` </td>
  </tr>
  <tr>
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (sec) </td>
    <td> Optional </td>
    <td> Defaults to 360s </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before and after injection of chaos in sec </td>
    <td> Optional  </td>
    <td> </td>
  </tr>
  <tr>
    <td> LIB  </td>
    <td> The chaos lib used to inject the chaos </td>
    <td> Optional </td>
    <td> Defaults to `litmus` supported litmus only </td>
  </tr>
  <tr>
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name.</td>
    <td> Optional </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>

</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/node-poweroff/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  # It can be active/stop
  engineState: 'active'
  #ex. values: ns1:name=percona,ns2:run=nginx 
  auxiliaryAppInfo: ''
  chaosServiceAccount: node-poweroff-sa
  experiments:
    - name: node-poweroff
      spec:
        components:
        # nodeSelector: 
        #   # provide the node labels
        #   kubernetes.io/hostname: 'node02'   
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'

             # ENTER THE TARGET NODE NAME
            - name: TARGET_NODE
              value: ''

            # ENTER THE TARGET NODE IP
            - name: TARGET_NODE_IP
              value: ''

             # ENTER THE USER TO BE USED FOR SSH AUTH
            - name: SSH_USER
              value: 'root'
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- View the status of the nodes as they are subjected to Node Poweroff. 

  `watch -n 1 kubectl get nodes`
  
### Check Chaos Experiment Result

- Check whether the application is resilient to the Node Poweroff, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-node-poweroff -n <application-namespace>`

### Node Poweroff Experiment Demo

- A sample recording of this experiment execution will be added soon.
