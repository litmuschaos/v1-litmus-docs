---
id: example 
title: Chaos Example
sidebar_label: Chaos Example 
---
------

## Example of running a chaos experiment

In this example we will create an `nginx` deployment and try to inject `pod-delete` chaos. We will deploy nginx under `litmus` namespace itself to simplify the process of access control. Please refer to [Get Started page](https://docs.litmuschaos.io/docs/next/getstarted.html) if you want to run the experiment on a deployment under a different namespace.


If you have not already installed Litmus, install it by using the following command.

```
kubectl apply -f https://litmuschaos.github.io/pages/litmus-operator-latest.yaml
```

Similarly, if you have not already installed generic chaos experiments, install the generic chaos chart by using the following command.

```
kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/experiments.yaml -n litmus
```


- Start  nginx application

```console
kubectl run myserver --image=nginx -n litmus
```

- Annotate your application to permit Litmus chaos operator to run chaos experiments on the application.

```console
kubectl annotate deploy/myserver litmuschaos.io/chaos="true" -n litmus
```

- Create the ChaosEngine CR using the application and chaos experiment details.

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
    appns: litmus # App namespace
    # FYI, To see app label, apply kubectl get pods --show-labels
    applabel: "run=myserver" # App Label
  chaosServiceAccount: litmus
  experiments:
    - name: pod-delete
      spec:
        rank: 1
```

- Apply the chaosengine.yaml using `kubectl` command.

```console
kubectl create -f chaosengine.yaml
```

It takes upto a couple of minutes for the experiments to be run and the result CR to be created. 

- Observe the ChaosResult CR Status to know the status of the experiment. If the experiment is still in progress, the ```spec.verdict``` is set to `running`. If the experiment is completed, the `spec.verdict` is set to either `pass` or `fail`

```console
kubectl describe chaosresult engine-nginx-pod-delete -n litmus
```

> Observed Output:

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

> Note: You may observe the pod status by the following command. And observe that nginx pod getting deleted couple of times and recreated.
>
> `watch -n 1 kubectl get pods -n litmus`

<br>

<br>

<hr>

<br>

<br>

<!-- Global site tag (gtag.js) - Google Analytics -->

<script async src="https://www.googletagmanager.com/gtag/js?id=UA-92076314-12"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-92076314-12');
</script>
