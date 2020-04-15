---
id: openebs-nfs-kill-chaos
title: OpenEBS NFS KILL Chaos Experiment Details
sidebar_label: OpenEBS NFS Kill Chaos
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
    <td> OpenEBS </td>
    <td> Kill the OpenEBS NFS provisioner container and check if pods mounted with RWM modes.  </td>
    <td> GKE </td>
  </tr>
</table>

## Prerequisites

- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)

- Ensure that the `openebs-nfs-kill-chaos` experiment resource is available in the cluster by executing `kubectl get chaosexperiments` in the `openebs` namespace. If not, install from [here](https://hub.litmuschaos.io/charts/openebs/experiments/openebs-nfs-kill-chaos)

- The DATA_PERSISTENCE is used when `EXTERNAL_APP_CHECK` sets to true and it is enabled by provide the application's info in a configmap volume so that the experiment can perform necessary checks. By Default it will using `Busybox` data persistency check.

Busybox data persistence check create a configmap as shown below in the application namespace (replace with actual credentials):

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: openebs-nfs-kill-cm
data:
  parameters.yml: | 
    blocksize: 4k
    blockcount: 1024
    testfile: exampleFile
```

## Entry Criteria

- OpenEBS NFS pods are healthy before chaos injection
- Pods using NFS RWM mode are healthy before chaos injection

## Exit Criteria

- OpenEBS NFS pods are healthy after chaos injection
- Pods using NFS RWM mode are healthy after chaos injection

## Details

- This scenario validates graceful & forced terminations of OpenEBS NFS container

## Integrations

- Container kill is achieved using the `pumba` or `containerd_chaos` chaos library
- The desired pumba and containerd image can be configured in the env variable `LIB_IMAGE`. 

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to be provided in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.


### Prepare chaosServiceAccount

Use this sample RBAC manifest to create a chaosServiceAccount in the desired namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/openebs/openebs-nfs-kill-chaos/rbac.yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nfs-kill-sa
  namespace: default
  labels:
    name: nfs-kill-sa
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: nfs-kill-sa
  namespace: default
  labels:
    name: nfs-kill-sa
rules:
- apiGroups: ["","apps","litmuschaos.io","batch","extensions","storage.k8s.io"]
  resources: ["pods","pods/exec","pods/log", "deployments","events","jobs","configmaps","services","persistentvolumeclaims","storageclasses","persistentvolumes","chaosexperiments","chaosresults","chaosengines"]
  verbs: ["create","list","get","patch","update","delete"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: nfs-kill-sa
  namespace: default
  labels:
    name: nfs-kill-sa
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: nfs-kill-sa
subjects:
- kind: ServiceAccount
  name: nfs-kill-sa
  namespace: default
```

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
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
    <td> TARGET_CONTAINER  </td>
    <td> The container to be killed inside the pod </td>
    <td> Mandatory </td>
    <td> If the TARGET_CONTAINER is not provided it will delete the first container </td>
  </tr>
  <tr>
    <td> LIB_IMAGE  </td>
    <td> The pumba/containerd image used to run the kill command </td>
    <td> Optional </td>
    <td> Defaults to `gaiaadm/pumba:0.6.5`, for containerd runtime use `gprasath/crictl:ci`</td>
  </tr>
  <tr>
    <td> LIB  </td>
    <td> The category of lib use to inject chaos </td>
    <td> Optional  </td>
    <td> It can be pumba or containerd </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before injection of chaos in sec </td>
    <td> Optional  </td>
    <td> </td>
  </tr>
</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/openebs/openebs-nfs-kill-chaos/engine.yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nfs-kill-chaos
  namespace: default
spec:
  # It can be true/false
  annotationCheck: 'false'
  # It can be active/stop
  engineState: 'active'
  appinfo:
    appns: 'minio'
    applabel: 'app=minio'
    appkind: 'deployment'
  chaosServiceAccount: nfs-kill-sa
  monitoring: false
  # It can be delete/retain
  jobCleanUpPolicy: 'delete'
  experiments:
    - name: openebs-nfs-kill-chaos
      spec:
        components:
          env:
            - name: NFS_PROVISIONER_NAMESPACE
              value: 'app-nfs-ns'
  
            ## Period to wait before injection of chaos  
            - name: RAMP_TIME
              value: '10'

            - name: NFS_PROVISIONER_LABEL
              value: 'app=nfs'

            - name: NFS_PVC
              value: 'nfs-pvc-claim'
            
            - name: NFS_SVC
              value: 'nfs-provisioner'

            - name: TARGET_CONTAINER
              value: 'nfs-provisioner'

            # EXTERNAL_APP_CHECK can be true/false
            - name: EXTERNAL_APP_CHECK
              value: 'true'
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml -n <application-namespace>`

### Watch Chaos progress

- View pod terminations by setting up a watch on the pods in the application namespace

  `watch -n 1 kubectl get pods -n -n <application-namespace>`

### Check Chaos Experiment Result

- Check whether the OpenEBS NFS pod is resilient to the container kill, once the experiment (job) is completed. The ChaosResult resource naming convention is: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nfs-kill-chaos-openebs-nfs-provisioner-kill -n <application-namespace>`

## Recovery 

- If the verdict of the ChaosResult is `Fail`, and/or the OpenEBS components do not return to healthy state post the chaos experiment, then please refer the [OpenEBS troubleshooting guide](https://docs.openebs.io/docs/next/troubleshooting.html#installation) for more info on how to recover the same.

## OpenEBS NFS KILL Chaos Demo [TODO]

- A sample recording of this experiment execution is provided here.
