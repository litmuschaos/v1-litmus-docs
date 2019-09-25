# Installation
Installation is made of three steps
* Install required RBAC (Role-based access control).
* Install required CRDS (Custom Resource Definitions).
* Install chaos operator for monitoring and execution.

### Linux/ macOS / Windows

We supported in all the OS environments.

```console
kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-operator/master/deploy/rbac.yaml

kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-operator/master/deploy/chaos_crds.yaml

kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-operator/master/deploy/operator.yaml

```

You are now ready to create chaos experiment.

# Demo
* Let's make an nginx deployment and try to inject chaos

```console
kubectl run myserver --image=nginx
```

* Here, we have made one nginx deployment. So, Let's inject some chaos say **"pod-delete"**

Go to [hub.litmuschaos.io](https://hub.litmuschaos.io) , search for the required experiment. For this demo we need **pod-delete**

```console
kubectl create -f https://raw.githubusercontent.com/litmuschaos/community-charts/master/charts/kubernetes/state/experiments/k8s_state_all_exp_crd.yaml
```
* Annotate your application to enable chaos. For eg:
```console
kubectl annotate deploy/myserver litmuschaos.io/chaos="true"
```

* For chaos to be injected, we have to mention the ```"app label"``` and ```"app namespace"```.

So, create a file **"chaosengine.yaml"** and paste the below yaml script.

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

* Refer to the ChaosEngine Status (or alternately, the corresponding ChaosResult resource) to know the status of each experiment. The ```spec.verdict``` is set to Running when the experiment is in progress, eventually changing to pass or fail.
```console
kubectl describe chaosresult engine-nginx-pod-delete
```
> Output

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
You can delete the chaos experiments and uninstall Litmuschaos:

```console
kubectl delete ns litmus
```

## Example
Click here to see more [experiments](https://github.com/litmuschaos/litmus/tree/master/experiments) example.

Also, check out the [LitmusChaos](https://github.com/litmuschaos/litmus/) repository to learn the concept of chaos engineering. we encourage contributions from the community- your PR is welcome!:) 

