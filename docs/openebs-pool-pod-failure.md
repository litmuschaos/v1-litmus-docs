---
id: openebs-pool-pod-failure
title: OpenEBS Pool Pod Failure Experiment Details
sidebar_label: Pool Pod Failure
---
------

## Experiment Metadata

| Type      | Description              | Tested K8s Platform                                               |
| ----------| ------------------------ | ------------------------------------------------------------------|
| OpenEBS   | Kill the cstor pool pod and check if gets created again | GKE, Konvoy(AWS), Packet(Kubeadm), Minikube, OpenShift(Baremetal)  |

<b>Note:</b> In this example, we are using nginx as stateful application that stores static pages on a Kubernetes volume.  

## Prerequisites

- Ensure that the Litmus Chaos Operator is running in the cluster. If not, install from [here](https://github.com/litmuschaos/chaos-operator/blob/master/deploy/operator.yaml)
- Ensure that the `openebs-pool-pod-failure` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/openebs/experiments/openebs-pool-pod-failure)
- If DATA_PERSISTENCE is 'enabled', provide the application info in a configmap volume so that the experiment can perform necessary checks. Currently, LitmusChaos supports
  data consistency checks only on MySQL databases. Create a configmap as shown below in the application namespace (replace with actual credentials):

  ```
  ---
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: openebs-pool-pod-failure
  data:
    parameters.yml: | 
      dbuser: root
      dbpassword: k8sDem0
      dbname: test
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

- This scenario validates the behaviour of stateful applications and OpenEBS data plane upon forced termination of the target pod
- Target pool pod are killed using the litmus chaoslib [random pod delete](https://github.com/litmuschaos/litmus/blob/master/chaoslib/litmus/kill_random_pod.yml)
- Can test the stateful application's resilience to momentary iSCSI connection loss

## Integrations

- Pod delete is achieved using the `litmus` chaos library

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to be provided in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app)namespace. This example consists of the minimum necessary cluster role permissions to execute the experiment.

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
- apiGroups: ["","apps","litmuschaos.io","batch","extensions","storage.k8s.io","openebs.io"]
  resources: ["pods","jobs","deployments","configmaps","secrets","replicasets","persistentvolumeclaims","storageclasses","cstorvolumereplicas","chaosexperiments","chaosresults","chaosengines"]
  verbs: ["create","list","get","patch","update","delete"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get","list"]
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
- Provide the auxiliary applications info (ns & labels) in `spec.auxiliaryAppInfo`
- Override the experiment tunables if desired

#### Supported Experiment Tunables

| Variables             | Description                                                  | Type      | Notes                                                      |
| ----------------------| ------------------------------------------------------------ |-----------|------------------------------------------------------------|
| APP_PVC               | The PersistentVolumeClaim used by the stateful application   | Mandatory | PVC must use OpenEBS cStor storage class        |
| DEPLOY_TYPE           | Type of Kubernetes resource used by the stateful application | Optional  | Defaults to `deployment`. Supported: `deployment`, `statefulset`|                           |
| TOTAL_CHAOS_DURATION  | Amount of soak time for I/O post pod kill              | Optional  | Defaults to 600 seconds					|
| DATA_PERSISTENCE      | Flag to perform data consistency checks on the application   | Optional  | Default value is disabled (empty/unset). Set to `enabled` to perform data checks. Ensure configmap with app details are created                                                                                                                   |             

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: target-chaos
  namespace: default
spec:
  # It can be app/infra
  chaosType: 'infra' 
  #ex. values: ns1:name=percona,ns2:run=nginx 
  auxiliaryAppInfo: ""
  appinfo:
    appns: default
    applabel: 'app=percona'
    appkind: deployment
  chaosServiceAccount: nginx-sa
  monitoring: false
  components:
    runner:
      image: "litmuschaos/chaos-executor:1.0.0"
      type: "go"
  # It can be delete/infra
  jobCleanUpPolicy: delete
  experiments:
    - name: openebs-pool-pod-failure
      spec:
        components:
          - name: FORCE
            value: 'true'
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

- Check whether the application is resilient to the pool pod failure, once the experiment (job) is completed. The ChaosResult resource naming convention 
  is: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult target-chaos-openebs-pool-pod-failure -n <application-namespace>`

## OpenEBS Pool Pod Failure Demo [TODO]

- A sample recording of this experiment execution is provided here.
