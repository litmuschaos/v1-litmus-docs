---
id: getstarted 
title: Getting Started with Litmus
sidebar_label: Getting Started 
---

------
<html>
<head>
<style>
div {
  margin-bottom: 15px;
  padding: 4px 12px;
}
.danger {
  background-color: #ffdddd;
  border-left: 6px solid #f44336;
}
</style>
</head>
<body>

## Pre-requisites

Kubernetes 1.11 or later.

## Getting Started

Running chaos on your application involves the following steps:

[Install Litmus](#install-litmus)

[Install Chaos Experiments](#install-chaos-experiments)

[Setup ServiceAccount](#setup-serviceaccount)

[Prepare ChaosEngine](#prepare-chaosengine)

[Annotate your application](#annotate-your-application)

[Run Chaos](#run-chaos)

[Observe chaos results](#observe-chaos-results)

<hr>



###  Install Litmus

```
kubectl apply -f https://litmuschaos.github.io/pages/litmus-operator-v0.7.0.yaml
```

The above command install all the CRDS, required service account configuration, and chaos-operator. Before you start running a chaos experiment, verify if your Litmus is installed correctly.

**Verify your installation**

- Verify if the chaos operator is running 

```
kubectl get pods -n litmus
```

 Expected output:




>chaos-operator-ce-554d6c8f9f-slc8k             1/1         Running     0            6m41s



- Verify if chaos CRDs are installed

```
kubectl get crds | grep chaos
```

Expected output:

> chaosengines.litmuschaos.io             2019-10-02T08:45:25Z
>
> chaosexperiments.litmuschaos.io         2019-10-02T08:45:26Z
>
> chaosresults.litmuschaos.io             2019-10-02T08:45:26Z

<div class="danger">
<strong>NOTE</strong>: 
In this guide, we shall describe the steps to inject chaos on an application
deployed in the default namespace.
</div>

### Install Chaos Experiments

Chaos experiments contain the actual chaos details. These experiments are installed on your cluster as Kubernetes CRs (Custom Resources). The Chaos Experiments are grouped as Chaos Charts and are published on <a href=" https://hub.litmuschaos.io" target="_blank">Chaos Hub</a>. 

The generic chaos experiments such as `pod-kill`, `container-kill`,` network-delay` are available under Generic Chaos Chart. This is the first chart you install. You can later install application specific chaos charts for running application specific chaos.

```
kubectl create -f https://hub.litmuschaos.io/api/chaos?file=charts/generic/experiments.yaml
```

Verify if the chaos experiments are installed.

```
kubectl get chaosexperiments 
```

### Setup ServiceAccount

A ServiceAccount should be created to allow chaosengine to run experiments in your application namespace. Copy the following into `rbac.yaml` and run `kubectl apply -f rbac.yaml` to create one such account on your default namespace. You can change the service account name and namespace as needed.

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx
  labels:
    app: nginx
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nginx
rules:
- apiGroups: ["", "extensions", "apps", "batch", "litmuschaos.io"]
  resources: ["daemonsets", "deployments", "replicasets", "jobs", "pods", "pods/exec", "events", "chaosengines", "chaosexperiments", "chaosresults"]
  verbs: ["*"] 
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nginx
subjects:
- kind: ServiceAccount
  name: nginx
  namespace: default # App namespace
roleRef:
  kind: ClusterRole
  name: nginx
  apiGroup: rbac.authorization.k8s.io
```

### Annotate your application

Your application has to be annotated with `litmuschaos.io/chaos="true"`. As a security measure, Chaos Operator checks for this annotation on the application before invoking chaos experiment(s) on the application. Replace `myserver` with an name of your deployment.

```console
kubectl annotate deploy/myserver litmuschaos.io/chaos="true"
```

### Prepare ChaosEngine 

ChaosEngine connects the application to the Chaos Experiment. Copy the following YAML snippet into a file called `chaosengine.yaml` and update `applabel` , `appns`, `appkind` and `experiments` as per your choice. Toggle `monitoring` between `true`/`false`, to allow the chaos-exporter to fetch experiment related metrics. Change the `chaosServiceAccount` to the name of ServiceAccount created in above step, if applicable.

```yaml
# chaosengine.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: engine-nginx
  namespace: default
spec:
  monitoring: true
  appinfo: 
    appns: default 
    # FYI, To see app label, apply kubectl get pods --show-labels
    applabel: "run=myserver" 
  chaosServiceAccount: nginx 
  experiments:
    - name: container-kill
      spec:
        components:
        - name: TARGET_CONTAINER
          value: hello
```

### Over-ride Default Chaos Experiments Variables

After LitmusChaos v0.7.0, to over-ride the default enviroment variables in the chaosExperiments, add the entry of those variable with the same name under `experiments.<experiment_name>.spec.components` with the over-riding value.

```console
...
experiments:
    - name: container-kill
      spec:
        components:
        - name: TARGET_CONTAINER
          value: hello
```


### Annotate your application

Your application has to be annotated with `litmuschaos.io/chaos="true"`. As a security measure, Chaos Operator checks for this annotation on the application before invoking chaos experiment(s) on the application. Replace `myserver` with the name of your deployment.

```console
kubectl annotate deploy/myserver litmuschaos.io/chaos="true"
```

### Run Chaos


```console
kubectl create -f chaosengine.yaml
```

<div class="danger">
<strong>NOTE</strong>: It is recommended to create Application, ChaosEngine, ChaosExperiment and ServiceAccount in the same namespace for smooth execution of experiments.
</div>

### Observe Chaos results

Observe the ChaosResult CR Status to know the status of each experiment. The ```spec.verdict``` is set to Running when the experiment is in progress, eventually changing to pass or fail.

<strong> NOTE:</strong>  ChaosResult name will be `<chaos-engine-name>-<chaos-experiment-name>`

```console
kubectl describe chaosresult engine-nginx-pod-delete
```

## Uninstallation

You can uninstall Litmus by deleting the namespace.

```console
kubectl delete ns litmus
```



## Example

See [the tutorial](example.md) on running a `pod-delete` chaos experiment on `nginx` application.



## Join our community

If you have not joined our community, do join us [here](https://app.slack.com/client/T09NY5SBT/CNXNB0ZTN).



<br>

<hr>

<br>	
</body>
</html>
