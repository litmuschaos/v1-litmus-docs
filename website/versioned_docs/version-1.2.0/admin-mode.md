---
id: version-1.2.0-admin-mode
title: Administrator Mode
sidebar_label: Administrator Mode
original_id: admin-mode
---
------

###  What is Adminstator Mode? 

Admin Mode is a priviledged mode that LitmusChaos support in order to make SRE's/ Cluster Admins/ Developers life easier.
This mode helps to induce chaos in different namespaces, by managing all the chaos resources in a single namespace.

### How to use Adminstator Mode?

In order to use Admin Mode, you just have to create a ServiceAccount in Chaos Resources Namespace, that has the permissions to perform operations on different kubernetes resources, in different namespaces.
Just use this ServiceAccount Name in ChaosEngine chaosServiceAccount, this will let you to have all chaos resources in a single namespace, with chaos being performed on various namespaces.

### Example

#### Prepare RBAC Manifest 

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: litmus
  namespace: litmus
  labels:
    name: litmus
---
# Source: openebs/templates/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: litmus
  labels:
    name: litmus
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: litmus
  labels:
    name: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: litmus
subjects:
- kind: ServiceAccount
  name: litmus
  namespace: litmus
```

#### Prepare ChaosEngine 

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: litmus #Chaos Resources Namespace
spec:
  appinfo:
    appns: 'default' #Application Namespace
    applabel: 'app=nginx'
    appkind: 'deployment'
  # It can be true/false
  annotationCheck: 'true'
  # It can be active/stop
  engineState: 'active'
  #ex. values: ns1:name=percona,ns2:run=nginx
  auxiliaryAppInfo: ''
  chaosServiceAccount: litmus
  monitoring: false
  # It can be delete/retain
  jobCleanUpPolicy: 'delete'
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            # set chaos duration (in sec) as desired
            - name: TOTAL_CHAOS_DURATION
              value: '30'

            # set chaos interval (in sec) as desired
            - name: CHAOS_INTERVAL
              value: '10'
              
            # pod failures without '--force' & default terminationGracePeriodSeconds
            - name: FORCE
              value: 'false'
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos Engine 

- Describe Chaos Engine for chaos steps.

  `kubectl describe chaosengine <chaos-engine> -n <chaos-resources-namespace>`

### Watch Chaos progress

- View pod terminations & recovery by setting up a watch on the pods in the application namespace

  `watch -n 1 kubectl get pods -n <application-namespace>`

### Check Chaos Experiment Result

- Check whether the application is resilient to the pod failure, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-pod-delete -n <application-namespace>`