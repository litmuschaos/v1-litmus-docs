---
id: pod-dns-spoof
title: Pod DNS Spoof Experiment Details
sidebar_label: Pod DNS Spoof 
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
    <td> Generic </td>
    <td> Spoofs particular dns requests in target pods to desired hostnames </td>
    <td> EKS, Minikube > v1.6.0</td>
  </tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.15
- Ensure that the Litmus Chaos Operator is running by executing `kubectl get pods` in operator namespace (typically, `litmus`). If not, install from [here](https://docs.litmuschaos.io/docs/getstarted/#install-litmus)
- Ensure that the `pod-dns-spoof` experiment resource is available in the cluster by executing                         `kubectl get chaosexperiments` in the desired namespace. If not, install from [here](https://hub.litmuschaos.io/api/chaos/master?file=charts/generic/pod-dns-spoof/experiment.yaml)
 
## Entry Criteria

- Application pods are healthy before chaos injection

## Exit Criteria

- Application pods are healthy post chaos injection

## Details

- Pod-dns-spoof injects chaos to spoof dns resolution in kubernetes pods.
- The application pod should be healthy once chaos is stopped.
- Causes dns resolution of target hostnames/domains to wrong IPs as specified by `SPOOF_MAP` in the engine config.

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to create the chaosServiceAccount, prepare the ChaosEngine & execute the experiment.

### Prepare chaosServiceAccount

- Use this sample RBAC manifest to create a chaosServiceAccount in the desired (app) namespace. This example consists of the minimum necessary role permissions to execute the experiment.

#### Sample Rbac Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/pod-dns-spoof/rbac.yaml yaml)
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-dns-spoof-sa
  namespace: default
  labels:
    name: pod-dns-spoof-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-dns-spoof-sa
  namespace: default
  labels:
    name: pod-dns-spoof-sa
    app.kubernetes.io/part-of: litmus
rules:
  - apiGroups: [""]
    resources: ["pods", "events"]
    verbs:
      ["create", "list", "get", "patch", "update", "delete", "deletecollection"]
  - apiGroups: [""]
    resources: ["pods/exec", "pods/log", "replicationcontrollers"]
    verbs: ["create", "list", "get"]
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["create", "list", "get", "delete", "deletecollection"]
  - apiGroups: ["apps"]
    resources: ["deployments", "statefulsets", "daemonsets", "replicasets"]
    verbs: ["list", "get"]
  - apiGroups: ["apps.openshift.io"]
    resources: ["deploymentconfigs"]
    verbs: ["list", "get"]
  - apiGroups: ["argoproj.io"]
    resources: ["rollouts"]
    verbs: ["list", "get"]
  - apiGroups: ["litmuschaos.io"]
    resources: ["chaosengines", "chaosexperiments", "chaosresults"]
    verbs: ["create", "list", "get", "patch", "update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-dns-spoof-sa
  namespace: default
  labels:
    name: pod-dns-spoof-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-dns-spoof-sa
subjects:
  - kind: ServiceAccount
    name: pod-dns-spoof-sa
    namespace: default
```

***Note:*** In case of restricted systems/setup, create a PodSecurityPolicy(psp) with the required permissions. The `chaosServiceAccount` can subscribe to work around the respective limitations. An example of a standard psp that can be used for litmus chaos experiments can be found [here](https://docs.litmuschaos.io/docs/next/litmus-psp/).

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
    <td> Name of container which is subjected to dns spoof </td>
    <td> Optional </td>
    <td> None </td>
  </tr>
  <tr>
    <td> TOTAL_CHAOS_DURATION </td>
    <td> The time duration for chaos insertion (seconds) </td>
    <td> Optional </td>
    <td> Default (60s) </td>
  </tr>
  <tr>
    <td> SPOOF_MAP </td>
    <td> Map of the target hostnames eg. '{"abc.com":"spoofabc.com"}' where key is the hostname that needs to be spoofed and value is the hostname where it will be spoofed/redirected to.</td>
    <td> Optional </td>
    <td> If not provided, no hostnames/domains will be spoofed</td>
  </tr>    
  <tr>
    <td> PODS_AFFECTED_PERC </td>
    <td> The Percentage of total pods to target  </td>
    <td> Optional </td>
    <td> Defaults to 0 (corresponds to 1 replica), provide numeric value only </td>
  </tr> 
  <tr>
    <td> CONTAINER_RUNTIME  </td>
    <td> container runtime interface for the cluster</td>
    <td> Optional </td>
    <td> Defaults to docker, supported values: docker, containerd and crio </td>
  </tr>
  <tr>
    <td> SOCKET_PATH </td>
    <td> Path of the containerd/crio/docker socket file </td>
    <td> Optional  </td>
    <td> Defaults to `/var/run/docker.sock` </td>
  </tr>
  <tr>
    <td> LIB </td>
    <td> The chaos lib used to inject the chaos </td>
    <td> Optional  </td>
    <td> Default value: litmus, supported values: litmus </td>
  </tr>
  <tr>
    <td> LIB_IMAGE  </td>
    <td> Image used to run the netem command </td>
    <td> Optional  </td>
    <td> Defaults to `litmuschaos/go-runner:latest` </td>
  </tr>
  <tr>
    <td> RAMP_TIME </td>
    <td> Period to wait before and after injection of chaos in sec </td>
    <td> Optional  </td>
    <td> </td>
  </tr>
  <tr>
    <td> SEQUENCE </td>
    <td> It defines sequence of chaos execution for multiple target pods </td>
    <td> Optional </td>
    <td> Default value: parallel. Supported: serial, parallel </td>
  </tr>
  <tr>
    <td> INSTANCE_ID </td>
    <td> A user-defined string that holds metadata/info about current run/instance of chaos. Ex: 04-05-2020-9-00. This string is appended as suffix in the chaosresult CR name.</td>
    <td> Optional  </td>
    <td> Ensure that the overall length of the chaosresult CR is still < 64 characters </td>
  </tr>

</table>

#### Sample ChaosEngine Manifest

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/pod-dns-spoof/engine.yaml yaml)
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
spec:
  appinfo:
    appns: "default"
    applabel: "app=nginx"
    appkind: "deployment"
  # It can be active/stop
  engineState: "active"
  #ex. values: ns1:name=percona,ns2:run=nginx
  auxiliaryAppInfo: ""
  chaosServiceAccount: pod-dns-spoof-sa
  experiments:
    - name: pod-dns-spoof
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60" # in seconds

            # map of the target hostnames eg. '{"abc.com":"spoofabc.com"}' . If empty no queries will be spoofed
            - name: SPOOF_MAP
              value: '{"google.com":"fakegoogle.com"}'

            # provide the name of container runtime, it supports docker, containerd, crio
            - name: CONTAINER_RUNTIME
              value: "docker"

            # provide the socket file path
            - name: SOCKET_PATH
              value: "/var/run/docker.sock"

             ## percentage of total pods to target
            - name: PODS_AFFECTED_PERC
              value: ""
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

- If the chaos experiment is not executed, refer to the [troubleshooting](https://docs.litmuschaos.io/docs/faq-troubleshooting/) 
  section to identify the root cause and fix the issues.

### Watch Chaos progress

- Ping the target hostname/domain before chaos execution and note down the ip

  `ping <target_domain>`

- Ping the target hostname/domain again from the affected pod, during chaos and you should notice the ip points to the spoofed destination

  `ping <target_domain>`

### Abort/Restart the Chaos Experiment

- To stop the pod-dns-spoof experiment immediately, either delete the ChaosEngine resource or execute the following command: 

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"stop"}}'` 

- To restart the experiment, either re-apply the ChaosEngine YAML or execute the following command: 

  `kubectl patch chaosengine <chaosengine-name> -n <namespace> --type merge --patch '{"spec":{"engineState":"active"}}'`  

### Check Chaos Experiment Result

- Check whether the application is resilient to the Pod Dns Spoof, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult <ChaosEngine-Name>-<ChaosExperiment-Name> -n <application-namespace>`
