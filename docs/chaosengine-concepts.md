---
id: chaosengine 
title: Constructing the ChaosEngine 
sidebar_label: ChaosEngine
---
------

The ChaosEngine is the main user-facing chaos custom resource with a namespace scope and is designed to hold information 
around how the chaos experiments are executed. It connects an application instance with one or more chaos experiments, 
while allowing the users to specify run level details (override experiment defaults, provide new environment variables and 
volumes, options to delete or retain experiment pods, etc.,). This CR is also updated/patched with status of the chaos 
experiments, making it the single source of truth with respect to the chaos. 

This section describes the fields in the ChaosEngine spec and the possible values that can be set against the same.

## State Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.engineState</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to control the state of the chaosengine</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><code>active</code>, <code>stop</code></td>
</tr>
<tr>
  <th>Default</th>
  <td><code>active</code></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>engineState</code> in the spec is a user defined flag to trigger chaos. Setting it to <code>active</code> ensures successful execution of chaos. Patching it with <code>stop</code> aborts ongoing experiments. It has a corresponding flag in the chaosengine status field, called <code>engineStatus</code> which is updated by the controller based on actual state of the ChaosEngine.</td>
</tr>
</table>

## Application Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.appinfo.appns</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify namespace of application under test</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type: string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>appns</code> in the spec specifies the namespace of the AUT. Usually provided as a quoted string.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.appinfo.applabel</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify unique label of application under test</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type: string)(pattern: "label_key=label_value")</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>applabel</code> in the spec specifies a unique label of the AUT. Usually provided as a quoted string of pattern key=value. Note that if multiple applications share the same label within a given namespace, the AUT is filtered based on the presence of the chaos annotation <code>litmuschaos.io/chaos: "true"</code>. If, however, the <code>annotationCheck</code> is disabled, then a random application (pod) sharing the specified label is selected for chaos.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.appinfo.appkind</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify resource kind of application under test</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><code>deployment</code>, <code>statefulset</code>, <code>daemonset</code></td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i> (depends on app type)</td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>appkind</code> in the spec specifies the Kubernetes resource type of the app deployment. The Litmus ChaosOperator supports chaos on deployments, statefulsets and daemonsets. Application health check routines are dependent on the resource types, in case of some experiments.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.auxiliaryAppInfo</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify one or more app namespace-label pairs whose health is also monitored as part of the chaos experiment, in addition to a primary application specified in the <code>.spec.appInfo</code>. <b>NOTE</b>: If the auxiliary applications are deployed in namespaces other than the AUT, ensure that the chaosServiceAccount is bound to a cluster role and has adequate permissions to list pods on other namespaces. </td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type: string)(pattern: "namespace:label_key=label_value").</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>auxiliaryAppInfo</code> in the spec specifies a (comma-separated) list of namespace-label pairs for downstream (dependent) apps of the primary app specified in <code>.spec.appInfo</code> in case of pod-level chaos experiments. In case of infra-level chaos experiments, this flag specifies those apps that may be directly impacted by chaos and upon which health checks are necessary.</td>
</tr>
</table>

**Note**: Irrespective of the nature of the chaos experiment, i.e., pod-level (single-app impact/lesser blast radius) or infra-level(multi-app impact/higher blast radius), the `.spec.appinfo` is a must-fill where the experiment is pointed to at least one primary app whose health is measured as an indicator of the resiliency / success of the chaos experiment. 

## RBAC Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.chaosServiceAccount</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify serviceaccount used for chaos experiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type: string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>chaosServiceAccount</code> in the spec specifies the name of the serviceaccount mapped to a role/clusterRole with enough permissions to execute the desired chaos experiment. The minimum permissions needed for any given experiment is provided in the <code>.spec.definition.permissions</code> field of the respective <b>chaosexperiment</b> CR.</td>
</tr>
</table>

## Runtime Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.annotationCheck</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to control annotationChecks on applications as prerequisites for chaos</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><code>true</code>, <code>false</code></td>
</tr>
<tr>
  <th>Default</th>
  <td><code>true</code></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>annotationCheck</code> in the spec controls whether or not the operator checks for the annotation "litmuschaos.io/chaos" to be set against the application under test (AUT). Setting it to <code>true</code> ensures the check is performed, with chaos being skipped if the app is not annotated, while setting it to <code>false</code> suppresses this check and proceeds with chaos injection.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.monitoring</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to enable collection of simple chaos metrics</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><code>true</code>, <code>false</code></td>
</tr>
<tr>
  <th>Default</th>
  <td><code>false</code></td>
</tr>
<tr>
  <th>Notes</th>
  <td><code>monitoring</code> in the spec enables or disables collection of chaos metrics with an exporter pod. Metrics include count of experiments in a chaosengine & individual experiment status. It is recommended to keep this disabled.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.jobCleanupPolicy</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to control cleanup of chaos experiment job post execution of chaos</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><code>delete</code>, <code>retain</code></td>
</tr>
<tr>
  <th>Default</th>
  <td><code>delete</code></td>
</tr>
<tr>
  <th>Notes</th>
  <td><The <code>jobCleanupPolicy</code> controls whether or not the experiment pods are removed once execution completes. Set to <code>retain</code> for debug purposes (in the absence of standard logging mechanisms).</td>
</tr>
</table>

## Component Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.components.runner.image</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify image of ChaosRunner pod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type: string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i> (refer <i>Notes</i>)</td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.components.runner.image</code> allows developers to specify their own debug runner images. Defaults for the runner image can be enforced via the operator env <b>CHAOS_RUNNER_IMAGE</b></td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.components.runner.imagePullPolicy</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify imagePullPolicy for the ChaosRunner</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td><code>Always</code>, <code>IfNotPresent</code></td>
</tr>
<tr>
  <th>Default</th>
  <td><code>IfNotPresent</code></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.components.runner.imagePullPolicy</code> allows developers to specify the pull policy for chaos-runner. Set to <code>Always</code> during debug/test.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.components.runner.runnerannotation</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Annotations that needs to be provided in the pod which will be created (runner-pod)</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td> <i>user-defined</i> (type: map[string]string) </td>
</tr>
<tr>
  <th>Default</th>
  <td> n/a </td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.components.runner.runnerannotation</code> allows developers to specify the custom annotations for the runner pod.</td>
</tr>
</table>

## Experiment Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].name</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Name of the chaos experiment CR</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
<td><i>user-defined</i> (type: string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>experiment[].name</code> specifies the chaos experiment to be executed by the ChaosOperator.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.components.env</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Environment variables passed to the chaos experiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td><i>user-defined</i> (type: {name: string, value: string})</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>experiment[].spec.components.env</code> specifies the array of tunables passed to the experiment pods. Though the field is optional from a chaosengine definition viewpoint, it is almost always necessary to provide experiment tunables via this definition. While some of the env variables override the defaults in the experiment CR and some of the env are mandatory additions filling in for placeholders/empty values in the experimet CR. For a list of "mandatory" & "optional" env for an experiment, refer to the respective experiment documentation.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.components.configMaps</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Configmaps passed to the chaos experiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td><i>user-defined</i> (type: {name: string, mountPath: string})</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>experiment[].spec.components.configMaps</code> provides for a means to insert config information into the experiment. The configmaps definition is validated for correctness and those specified are checked for availability (in the cluster/namespace) before being mounted into the experiment pods.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.components.secrets</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Kubernetes secrets passed to the chaos experiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td><i>user-defined</i> (type: {name: string, mountPath: string})</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>experiment[].spec.components.secrets</code> provides for a means to push secrets (typically project ids, access credentials etc.,) into the experiment pods. These are especially useful in case of platform-level/infra-level chaos experiments. The secrets definition is validated for correctness and those specified are checked for availability (in the cluster/namespace) before being mounted into the experiment pods.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.components.experimentImage</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Override the image of the chaos experiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td><i> string </i></td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>experiment[].spec.components.experimentImage</code> overrides the experiment image for the chaoexperiment.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.components.nodeSelector</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Provide the node selector for the experiment pod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td><i> Labels in the from of label key=value</i></td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>experiment[].spec.components.nodeSelector</code> The nodeselector contains labels of the node on which experiment pod should be scheduled. Typically used in case of infra/node level chaos.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.components.statusCheckTimeouts</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Provides the timeout and retry values for the status checks. Defaults to 180s & 90 retries (2s per retry)</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td><i> It contains values in the form {delay: int, timeout: int} </i></td>
</tr>
<tr>
  <th>Default</th>
  <td><i>delay: 2s and timeout: 180s</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>experiment[].spec.components.statusCheckTimeouts</code> The statusCheckTimeouts override the status timeouts inside chaosexperiments. It contains timeout & delay in seconds.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.components.runner.experimentannotation</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Annotations that needs to be provided in the pod which will be created (experiment-pod)</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td> <i>user-defined</i> (type: label key=value) </td>
</tr>
<tr>
  <th>Default</th>
  <td> n/a </td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.components.runner.experimentannotation</code> allows developers to specify the custom annotations for the experiment pod.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.httpProbe</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>An experiment probe that accesses a service endpoint </td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td> <i>user-defined</i> </td>
</tr>
<tr>
  <th>Default</th>
  <td> n/a </td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.httpProbe</code> allows developers to specify a URL which the experiment uses to gauge health/service availability (or other custom conditions) as part of the entry/exit criteria. The received status code is mapped against an expectedStatus</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.k8sProbe</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>An experiment probe that accesses a Kubernetes resource on the cluster.</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td> <i>user-defined</i> </td>
</tr>
<tr>
  <th>Default</th>
  <td> n/a </td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.k8sProbe</code> allows developers to list K8s resources (native or custom) as as part of the entry/exit criteria. It accepts the gvr (group, version, resource), namespace and fieldselector as inputs filter the desired resources.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.experiments[].spec.cmdProbe</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>An experiment probe that executes a shell command</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
<td> <i>user-defined</i> </td>
</tr>
<tr>
  <th>Default</th>
  <td> n/a </td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.cmdProbe</code> allows developers to run shell commands and match the resulting output as part of the entry/exit criteria. The probe supports an <code>inline</code> mode in which the command is run from within the experiment image as well as <code>source</code> mode, where the command execution is carried out from with a new pod whose image can be specified.</td>
</tr>
</table>
