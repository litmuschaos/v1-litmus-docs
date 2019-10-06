---
id: getstarted 
title: Getting Started with Litmus
sidebar_label: Getting Started 
---

------

## Pre-requisites

Kubernetes 1.11 or later.

## Getting Started

Running chaos on your application involves the following steps:

[Install Litmus](#install-litmus)

[Install  Chaos Experiments](#install-chaos-experiments)

[Prepare ChaosEngine](#prepare-chaosengine)

[Annotate your application](#annotate-your-application)

[Run Chaos](#run-chaos)

[Observe chaos results](#observe-chaos-results)

<hr>



###  Install Litmus

```
kubectl apply -f https://litmuschaos.github.io/pages/litmus-operator-latest.yaml
```

The above command installs all the chaos operator, required service account configuration, and chaos CRDs. Before you start running a chaos experiment, verify if your Litmus is installed correctly.

**Verify your installation**

- Verify if the chaos operator is running 

```
kubectl get pods -n litmus
```

> Expected output:
>
> *kubectl get pods -n litmus*
>
> NAME                                  READY   STATUS    RESTARTS   AGE
>
> litmus-operator-ce-554d6c8f9f-slc8k   1/1     Running   0          6m41s



- Verify if chaos CRDs are installed

```
kubectl get crds | grep chaos
```

> Expected output:
>
> *kubectl get crds | grep chaos*
>
> chaosengines.litmuschaos.io             2019-10-02T08:45:25Z
>
> chaosexperiments.litmuschaos.io         2019-10-02T08:45:26Z
>
> chaosresults.litmuschaos.io             2019-10-02T08:45:26Z



### Install Chaos Experiments

Chaos experiments contain the actual chaos details. These experiments are installed on to your cluster as Kubernetes CRs (or Custom Resources). The Chaos Experiments are grouped as Chaos Charts and are published on <a href=" https://hub.litmuschaos.io" target="_blank">Chaos Hub</a>. 

The generic chaos experiments such as `pod-kill`, `container-kill`,` network-delay` are avaialbe under Generic Chaos Chart. This is the first chart you install. You can later install application specific chaos charts for running application specific chaos.

```
kubectl create -f https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/experiment.yaml
```



Verify if the chaos experiments are installed.

```
kubectl get chaosexperiments
```



### Prepare ChaosEngine 

ChaosEngine connects the application to the Chaos Experiment. Copy the following YAML snippet into a file called chaosengine.yaml and update `applabel` and `experiments` as per your choice.

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



### Annotate your application

Your application has to be annotated with `litmuschaos.io/chaos="true"`. As a security measure, Chaos Operator checks for this annotation on the application before invoking chaos experiment(s) on the application.

```console
kubectl annotate deploy/myserver litmuschaos.io/chaos="true"
```



### Run Chaos



```console
kubectl create -f chaosengine.yaml
```



### Observe Chaos results

Observe the ChaosResult CR Status to know the status of each experiment. The ```spec.verdict``` is set to Running when the experiment is in progress, eventually changing to pass or fail.

```console
kubectl describe chaosresult engine-nginx-pod-delete
```



## Uninstallation

You can delete the chaos experiments and uninstall Litmus by deleting the namespace.

```console
kubectl delete ns litmus
```



## Example

See [the tutorial](example.html) on running a `pod-delete` chaos experiment on `nginx` application.



## Join our community

If you have not joined our community, do join us [here](community.html).



<br>

<hr>

<br>	



