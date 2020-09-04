---
id: litmus-probe
title: Declarative Hypothesis via Litmus Probe
sidebar_label: Litmus Probe
---
------

## Evolution of litmus probe

Litmus experiments contain pre/post chaos checks, to verify the health status of AUT(application under test), Auxiliary Application(dependent applications), some application-specific checks, for example, Cassandra check for the load re-distribution and Kafka check for the message stream. 
If there is a requirement for any additional custom checks then we have to re-write the experiment with additional check, build our own image and use inside chaos-experiment CR. This process needs lots of efforts and time consuming as well. This problem can be solved if we can define the pluggable checks and use directly inside chaos-experiment instead of re-write the experiment. Here litmus probe comes into play.

## Introduction of Litmus Probes

Litmus probes can define the declarative hypothesis inside chaos-engine. Which can be used by chaos-experiment to decide the resiliency of the experiment. Probes are used by chaos-experiment to generate the `Probe Success Percentage`, which is passed probes/ total probe (all probes have equal weightage). Probes support following four modes:

- <b>SOT:</b> SOT stands for start of test. Probes will run only at the start of the test (pre-chaos).
- <b>EOT:</b> EOT stands for end of test. Probes will run only at the end of the test (post-chaos).
- <b>Edge:</b> Edge contains both SOT and EOT. These probes run in both starts as well as at the end of the test.
- <b>Continuous:</b> Continuus probe run continuously for the entire chaos duration.

The probe contains `runProperties` attribute which provides an ability to retry with a timeout. It contains the following four fields.
- <b>probeTimeout:</b> It contains timeout, maximum duration after which probe is marked failed if it doesn't get the expected result.
- <b>interval:</b> It contains time interval, after which the probe makes a re-attempt to run the probe commands.
- <b>retry:</b> It contains retry count, for which probe make an attempt if it exceeds probeTimeout without getting the expected result.
- <b>probePollingInterval:</b> It contains time interval, after which a continuous probe makes a re-attempt to run the probe commands for each iteration. It is only applicable to the continuous probe.

Litmus probes can be defined in three different types. It consist `httpProbe`, `k8sProbe`, `cmdProbe`. The details explanation of all the three probes is provided below:

### httpProbe Probe

The httpProbe allows developers to specify a URL which the experiment uses to gauge health/service availability (or other custom conditions) as part of the entry/exit criteria. The received status code is mapped against an expected status. It can be defined at `.spec.experiments[].spec.httpProbe` the path inside chaosengine.

Sample snippet for the http probe

```
httpProbe:
- name: "http-probe"
  inputs:
    url: "<url>"
    expectedResponseCode: "200"
  mode: "Continuous"
  runProperties:
    probeTimeout: 5
    interval: 5
    retry: 1
    probePollingInterval: 2

```

### cmdProbe

The cmdProbe allows developers to run shell commands and match the resulting output as part of the entry/exit criteria. The probe supports an inline mode in which the command is run from within the experiment image as well as source mode, where the command execution is carried out from with a new pod whose image can be specified. We can set the `source` variable as `inline` for the inline mode otherwise we have to provide the source image inside the `source` variable if the httpProbe command needs an external pod to run. It can be defined at `.spec.experiments[].spec.cmdProbe` the path inside chaosengine.

Sample snippet for the cmd probe

```
cmdProbe:
- name: "cmd-probe"
  inputs:
    command: "<command>"
    expectedResult: "<expected-result>"
  source: "inline" # it can be inline or any image
  mode: "Continuous"
  runProperties:
    probeTimeout: 5
    interval: 5
    retry: 1
    probePollingInterval: 2

```

### k8sProbe

An experiment probe that accesses a Kubernetes resource on the cluster. The k8sProbe allows developers to list K8s resources (native or custom) as part of the entry/exit criteria. It accepts the gvr (group, version, resource), namespace, and fieldselector as inputs filter the desired resources. It can be defined at `.spec.experiments[].spec.k8sProbe` the path inside chaosengine.

Sample snippet for the k8s probe

```
k8sProbe:
- name: "k8s-probe"
  inputs:
  command:
  group: ""
  version: "v1"
  resource: "pods"
  namespace: "default"
  fieldSelector: "metadata.name=my-deployment-78ff9649f5-2nqhd,status.phase=Running"
  mode: "SOT"
  runProperties:
    probeTimeout: 5
    interval: 5
    retry: 1
```