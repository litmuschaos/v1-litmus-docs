---
id: openebs-target-container-failure
title: OpenEBS Target Container Failure Experiment Details
sidebar_label: Target Container Failure
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
    <td> Kill the cStor target/Jiva controller container </td>
    <td> GKE, Konvoy(AWS), Packet(Kubeadm), Minikube, OpenShift(Baremetal) </td>
  </tr>
</table>

<b>Note:</b> In this example, we are using nginx as stateful application that stores static pages on a Kubernetes volume.  

## Prerequisites

- Ensure that the Litmus Chaos Operator is running in the cluster. If not, install from [here](https://github.com/litmuschaos/chaos-operator/blob/master/deploy/operator.yaml)
- Ensure that the `openebs-target-container-failure` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/openebs/experiments/openebs-target-container-failure)
- The DATA_PERSISTENCE can be enabled by provide the application's info in a configmap volume so that the experiment can perform necessary checks. Currently, LitmusChaos supports data consistency checks only for MySQL and Busybox. 
    - For MYSQL data persistence check create a configmap as shown below in the application namespace (replace with actual credentials):

    ```
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: openebs-target-container-failure
    data:
      parameters.yml: | 
        dbuser: root
        dbpassword: k8sDem0
        dbname: test
    ```
    - For Busybox data persistence check create a configmap as shown below in the application namespace (replace with actual credentials):

    ```
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: openebs-target-container-failure
    data:
      parameters.yml: | 
        blocksize: 4k
        blockcount: 1024
        testfile: exampleFile
    ```
- Ensure that the chaosServiceAccount used for the experiment has cluster-scope permissions as the experiment may involve carrying out the chaos in the `openebs` namespace
  while performing application health checks in its respective namespace. 

## Entry Criteria

- Application pods are healthy before chaos injection
- Application writes are successful on OpenEBS PVs

## Exit Criteria

- Stateful application pods are healthy post chaos injection
- OpenEBS Storage target pods are healthy

If the experiment tunable DATA_PERSISTENCE is set to 'enabled':

- Application data written prior to chaos is successfully retrieved/read 
- Database consistency is maintained as per db integrity check utils 

## Details

- This scenario validates the behaviour of stateful applications and OpenEBS data plane upon forced termination of the controller container
- Kills the specified container in the controller pod by sending SIGKILL termination signal to its docker socket (hence docker runtime is required)
- Containers are killed using the `kill` command provided by [pumba](https://github.com/alexei-led/pumba)
- Pumba is run as a daemonset on all nodes in dry-run mode to begin with; the `kill` command is issued during experiment execution via `kubectl exec`
- Can test the stateful application's resilience to momentary iSCSI connection loss

## Integrations

- Container kill is achieved using the `pumba` chaos library in case of docker runtime, & `litmuslib` using `crictl` tool in case of containerd runtime. 
- The desired lib image can be configured in the env variable `LIB_IMAGE`. 

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to be provided in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-sa
  namespace: default
  labels:
    name: nginx-sa
---
# Source: openebs/templates/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: nginx-sa
  labels:
    name: nginx-sa
rules:
- apiGroups: ["","litmuschaos.io","batch","apps","storage.k8s.io"]
  resources: ["pods","jobs","pods/exec","configmaps","secrets","persistentvolumeclaims","storageclasses","persistentvolumes","chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update","delete"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: nginx-sa
  labels:
    name: nginx-sa
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: nginx-sa
subjects:
- kind: ServiceAccount
  name: nginx-sa
  namespace: default

```

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo`

#### Supported Experiment Tunables

<table>
  <tr>
    <th> Variables </th>
    <th> Description  </th>
    <th> Type </th>
    <th> Notes </th>
  </tr>
  <tr>
    <td> APP_PVC </td>
    <td> The PersistentVolumeClaim used by the stateful application </td>
    <td> Mandatory </td>
    <td> PVC may use either OpenEBS Jiva/cStor storage class </td>
  </tr>
  <tr>
    <td> LIB_IMAGE </td>
    <td> The chaos library image used to run the kill command </td>
    <td> Optional  </td>
    <td> Defaults to `gaiaadm/pumba:0.4.8`. Supported: `{docker : gaiaadm/pumba:0.4.8, containerd: gprasath/crictl:ci}` </td>
  </tr>
  <tr>
    <td> CONTAINER_RUNTIME </td>
    <td> The container runtime used in the Kubernetes Cluster </td>
    <td> Optional  </td>
    <td> Defaults to `docker`. Supported: `docker`, `containerd` </td>
  </tr>
  <tr>
    <td> TARGET_CONTAINER </td>
    <td> The container to be killed in the storage controller pod  </td>
    <td> Optional  </td>
    <td> Defaults to `cstor-volume-mgmt` </td>
  </tr>
  <tr>
    <td> TOTAL_CHAOS_DURATION </td>
    <td> Amount of soak time for I/O post container kill </td>
    <td> Optional </td>
    <td> Defaults to 60 seconds </td>
  </tr>
  <tr>
    <td> DEPLOY_TYPE </td>
    <td> Type of Kubernetes resource used by the stateful application </td>
    <td> Optional  </td>
    <td> Defaults to `deployment`. Supported: `deployment`, `statefulset` </td>
  </tr>
  <tr>
    <td> DATA_PERSISTENCE </td>
    <td> Flag to perform data consistency checks on the application </td>
    <td> Optional  </td>
    <td> Default value is disabled (empty/unset). It supports only `mysql` and `busybox`. Ensure configmap with app details are created </td>
  </tr>
</table>

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: target-chaos
  namespace: default
spec:
  # It can be true/false
  annotationCheck: 'false' 
  #ex. values: ns1:name=percona,ns2:run=nginx 
  auxiliaryAppInfo: ''
  appinfo:
    appns: 'default'
    applabel: 'app=percona'
    appkind: 'deployment'
  chaosServiceAccount: nginx-sa
  monitoring: false
  components:
    runner:
      image: 'litmuschaos/chaos-executor:1.0.0'
      type: 'go'
  # It can be delete/retain
  jobCleanUpPolicy: 'delete'
  experiments:
    - name: openebs-target-container-failure
      spec:
        components:
          env:
            - name: TARGET_CONTAINER
              value: 'cstor-istgt'
            - name: APP_PVC
              value: 'pvc-c466262a-a5f2-4f0f-b594-5daddfc2e29d'    
            - name: DEPLOY_TYPE
              value: deployment        
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress

- View pod restart count by setting up a watch on the pods in the OpenEBS namespace

  `watch -n 1 kubectl get pods -n <openebs-namespace>`

### Check Chaos Experiment Result

- Check whether the application is resilient to the target container kill, once the experiment (job) is completed. The ChaosResult resource naming convention 
  is: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult target-chaos-openebs-target-container-failure -n <application-namespace>`

## OpenEBS Target Container Failure Demo [TODO]

- A sample recording of this experiment execution is provided here.