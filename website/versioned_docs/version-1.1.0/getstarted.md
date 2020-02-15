---
id: version-1.1.0-getstarted
title: Getting Started with Litmus
sidebar_label: Introduction
original_id: getstarted
---
------

## Pre-requisites

Kubernetes 1.11 or later.

## Getting Started

Running chaos on your application involves the following steps:

[Install Litmus](#install-litmus)

[Install Chaos Experiments](#install-chaos-experiments)

[Setup Service Account](#setup-service-account)

[Annotate your application](#annotate-your-application)

[Prepare ChaosEngine](#prepare-chaosengine)

[Run Chaos](#run-chaos)

[Observe chaos results](#observe-chaos-results)

<hr>



###  Install Litmus

```
kubectl apply -f https://litmuschaos.github.io/pages/litmus-operator-v1.1.0.yaml
```

The above command install all the CRDs, required service account configuration, and chaos-operator. Before you start running a chaos experiment, verify if your Litmus is installed correctly.

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

- Verify if the chaos api resources are successfully created in the desired (application) namespace.
 
  *Note*: Sometimes, it can take a few seconds for the resources to be available post the CRD installation

```
kubectl api-resources | grep chaos
```

Expected output: 

> chaosengines							    litmuschaos.io 			     true	  ChaosEngine
>
> chaosexperiments                                                  litmuschaos.io                           true         ChaosExperiment
>
> chaosresults                                                      litmuschaos.io                           true         ChaosResult

 

<div class="danger">
<strong>NOTE</strong>: 
In this guide, we shall describe the steps to inject chaos on an application
already deployed in the default namespace. It is a mandatory requirement to ensure that the 
chaosexperiment & chaosengine custom resoures are created in the same namespace (typically, 
the same as the namespace of the application under test (AUT).
</div>

### Install Chaos Experiments

Chaos experiments contain the actual chaos details. These experiments are installed on your cluster as Kubernetes CRs (Custom Resources). The Chaos Experiments are grouped as Chaos Charts and are published on <a href=" https://hub.litmuschaos.io" target="_blank">Chaos Hub</a>. 

The generic chaos experiments such as `pod-kill`,  `container-kill`,` network-delay` are available under Generic Chaos Chart. This is the first chart you install. You can later install application specific chaos charts for running application oriented chaos.

```
kubectl apply -f https://hub.litmuschaos.io/api/chaos?file=charts/generic/experiments.yaml
```

Verify if the chaos experiments are installed.

```
kubectl get chaosexperiments 
```

### Setup Service Account

A Service Account should be created to allow chaosengine to run experiments in your application namespace. Copy the following into `rbac.yaml` and run `kubectl apply -f rbac.yaml` to create one such account on your default namespace. You can change the service account name and namespace as needed.

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/container-kill/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: container-kill-sa
  namespace: default
  labels:
    name: container-kill-sa
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: Role
metadata:
  name: container-kill-sa
  namespace: default
  labels:
    name: container-kill-sa
rules:
- apiGroups: ["","litmuschaos.io","batch","apps"]
  resources: ["pods","jobs","daemonsets","pods/exec","chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update","delete"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: RoleBinding
metadata:
  name: container-kill-sa
  namespace: default
  labels:
    name: container-kill-sa
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: container-kill-sa
subjects:
- kind: ServiceAccount
  name: container-kill-sa
  namespace: default

```

### Annotate your application

Your application has to be annotated with `litmuschaos.io/chaos="true"`. As a security measure, Chaos Operator checks for this annotation on the application before invoking chaos experiment(s) on the application. Replace `nginx` with the name of your deployment.

```console
kubectl annotate deploy/nginx litmuschaos.io/chaos="true"
```

### Prepare ChaosEngine 

ChaosEngine connects application to the Chaos Experiment. Copy the following YAML snippet into a file called `chaosengine.yaml` and update the values of `applabel` , `appns`, `appkind` and `experiments` as per your choice. Toggle `monitoring` between `true`/`false`, to allow the chaos-exporter to fetch experiment related metrics. Change the `chaosServiceAccount` to the name of Service Account created in above step, if applicable.

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/container-kill/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  # It can be true/false
  annotationCheck: 'true'
  # It can be active/stop
  engineState: 'active'
  #ex. values: ns1:name=percona,ns2:run=nginx 
  auxiliaryAppInfo: ''
  appinfo:
    appns: 'default'
    applabel: 'app=nginx'
    appkind: 'deployment'
  chaosServiceAccount: container-kill-sa
  monitoring: false
  # It can be delete/retain
  jobCleanUpPolicy: 'delete' 
  experiments:
    - name: container-kill
      spec:
        components:
          env:
            # specify the name of the container to be killed
            - name: TARGET_CONTAINER
              value: 'nginx'
```

### Override Default Chaos Experiments Variables

After LitmusChaos v1.1.0, to override the default environment variables in chaosExperiments, add the entry of those variables with the same name under `experiments.<experiment_name>.spec.components.env` with the overriding value.

```console
...
experiments:
    - name: container-kill
      spec:
        components:
          env:
            - name: TARGET_CONTAINER
              value: nginx
```



### Run Chaos


```console
kubectl apply -f chaosengine.yaml
```

### Observe Chaos results

Describe the ChaosResult CR to know the status of each experiment. The ```spec.verdict``` is set to `Awaited` when the experiment is in progress, eventually changing to either `Pass` or `Fail`.

<strong> NOTE:</strong>  ChaosResult CR name will be `<chaos-engine-name>-<chaos-experiment-name>`

```console
kubectl describe chaosresult engine-nginx-container-kill
```

## Uninstallation

You can uninstall Litmus by deleting the namespace.

```console
kubectl delete -f https://litmuschaos.github.io/pages/litmus-operator-v1.1.0.yaml
```

## More Chaos Experiments

- For more details on supported chaos experiments and the steps to run them, refer the **Experiments** section.

## Join our community

If you have not joined our community, do join us [here](https://app.slack.com/client/T09NY5SBT/CNXNB0ZTN).
