---
id: getstarted 
title: Getting Started with Litmus
sidebar_label: Getting Started 
---

------

## Pre-requisites:

Kubernetes 1.11 or later.

## Installation

Litmus toolset installation consists of the following:

- Install required RBAC (Role-based access control).
- Install Litmus CRDs (Custom Resource Definitions).
- Install Chaos Operator

Run the following commands on your Kubernetes shell.

```console
kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-operator/master/deploy/rbac.yaml

kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-operator/master/deploy/chaos_crds.yaml

kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-operator/master/deploy/operator.yaml

```

You are now ready to create and execuste chaos experiments on your cluster.

## Steps for running a chaos experiment

- Select the application (note down `applabel` and `namespace`) and annotate it with `litmus chaos/chaos="true"`
- Select one or more chaos experiments from <a href=" https://hub.litmuschaos.io" target="_blank">Chaos Hub</a>
- Create a ChaosEngine CR with `applabel`, `namespace` and `ChasoExperiment`s. ChaosOperator picks the ChaosEngine CR and runs the experiments on the application
- Observe the results on ChaosResult CR

## Example of running a chaos experiment
In this example we will create an nginx deployment and try to inject "pod-delete" chaos.



- Run `nginx`

```console
kubectl run myserver --image=nginx
```

* Download `pod-delete` chaos experiment from  <a href=" https://hub.litmuschaos.io" target="_blank">Chaos Hub</a> 

> Note: the below command downloads and installs more than one experiment. We will choose only `pod-delete` experiment in `ChaosEngine` CR.

```console
kubectl create -f https://raw.githubusercontent.com/litmuschaos/community-charts/master/charts/kubernetes/state/experiments/k8s_state_all_exp_crd.yaml
```
* Annotate your application to enable chaos. For eg:
```console
kubectl annotate deploy/myserver litmuschaos.io/chaos="true"
```

* Create the ChaosEngine CR using the application and chaos experiment details.

Create a file **"chaosengine.yaml"** and paste the below yaml script.

```yaml
# chaosengine.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: engine-nginx
  namespace: litmus
spec:
  appinfo: 
    appns: default # App namespace
    # FYI, To see app label, apply kubectl get pods --show-labels
    applabel: "run=myserver" # App Label
  chaosServiceAccount: litmus
  
  experiments:
    - name: pod-delete
      spec:
        rank: 1
```

and apply

```console
kubectl create -f chaosengine.yaml
```

* Observe the ChaosResult CR Status to know the status of each experiment. The ```spec.verdict``` is set to Running when the experiment is in progress, eventually changing to pass or fail.
```console
kubectl describe chaosresult engine-nginx-pod-delete
```
*Observed Output:*

```yaml

Name:         engine-nginx-pod-delete
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
              {"apiVersion":"litmuschaos.io/v1alpha1","kind":"ChaosResult","metadata":{"annotations":{},"name":"engine-nginx-pod-delete","namespace":"de...
API Version:  litmuschaos.io/v1alpha1
Kind:         ChaosResult
Metadata:
  Creation Timestamp:  2019-05-22T12:10:19Z
  Generation:          9
  Resource Version:    8898730
  Self Link:           /apis/litmuschaos.io/v1alpha1/namespaces/default/chaosresults/engine-nginx-pod-delete
  UID:                 911ada69-7c8a-11e9-b37f-42010a80019f
Spec:
  Experimentstatus:
    Phase:    <nil>
    Verdict:  pass
Events:       <none>
```


## Clean up

You can delete the chaos experiments and uninstall Litmus by deleting the namespace.

```console
kubectl delete ns litmus
```



<br>

<hr>

<br>	

## See Also:

### [Tutorials]()

### [Chaos Hub]()



