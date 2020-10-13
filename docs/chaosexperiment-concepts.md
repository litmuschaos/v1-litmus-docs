---
id: chaosexperiment
title: Constructing the ChaosExperiment
sidebar_label: ChaosExperiment
---
------

ChaosExperiment is the heart of litmus that contains the actual chaos details. The experiments are installed on your cluster as Kubernetes custom resource with a namespace scope and are designed to hold information of the actual ChaosExperiment that is to be executed which is specified via image, library, necessary permissions, low-level chaos parameters (default values). It allows us to provide the custom experiment image to run a ChaosExperiment and the image can also be patched from ChaosEngine.

This section describes the fields in the ChaosExperiment spec and the possible values that can be set against the same.

## Scope Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.scope</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the scope of the ChaosExperiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><code>Namespaced</code>, <code>Cluster</code></td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i> (depends on experiment type)</td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.spec.definition.scope</code> specifies the scope of the experiment. It can be Namespaced scope for pod level experiments and Cluster for the experiments having a cluster wide impact.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.permissions</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the minimum permission to run the ChaosExperiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type: list)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.spec.definition.permissions</code> specify the minimum permission that is required to run the ChaosExperiment. It also helps to estimate the blast radius for the ChaosExperiment.</td>
</tr>
</table>

## Component Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.image</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the image to run the ChaosExperiment </td>
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
  <td><i>n/a</i> (refer Notes)</td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.spec.definition.image</code> allows the developers to specify their experiment images which can be used for debugging purposes or creating a new experiment out of it.You can also override this image from ChaosEngine by providing the image name in <code>.spec.experiments[].spec.components.experimentImage</code></td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.imagePullPolicy</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag that helps the developers to specify imagePullPolicy for the ChaosExperiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><code>IfNotPresent</code>, <code>Always</code> (type: string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><code>Always</code></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.spec.definition.imagePullPolicy</code> allows developers to specify the pull policy for ChaosExperiment image. Set to <code>Always</code> during debug/test</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.args</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the entrypoint for the ChaosExperiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type:list of string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.spec.definition.args</code> specify the entrypoint for the ChaosExperiment. It depends on the language used in the experiment. For litmus-go the <code>.spec.definition.args</code> contains a single binary of all experiments and managed via <code>-name</code> flag which contains the name of the experiment to run(<code>-name (exp-name)</code>).</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.command</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the shell on which the ChaosExperiment will execute</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined</i> (type: list of string).</td>
</tr>
<tr>
  <th>Default</th>
  <td><code>/bin/bash</code></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.spec.definition.command</code> specifies the shell used to run the experiment <code>/bin/bash</code> is the most common shell to be used.</td>
</tr>
</table>

## Experiment Tunables Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.env</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify env used for ChaosExperiment</td>
</tr>
<tr>
  <th>Type</th>
  <td>Mandatory</td>
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
  <td> The <code>.spec.definition.env</code> specifies the array of tunable passed to the experiment pods. It is used to manage the experiment execution. We can set the default values for all the variables (tunable) here which can be overridden by ChaosEngine from <code>.spec.experiments[].spec.components.env</code> if required. To know about the variables that need to be overridden check the  list of "mandatory" & "optional" env for an experiment, refer to the respective experiment documentation.</td>
</tr>
</table>

## Configuration Specification

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.securityContext.containerSecurityContext.privileged</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the security context for the ChaosExperiment pod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>true, false</i> (type:bool)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td>The <code>.spec.definition.securityContext.containerSecurityContext.privileged</code> specify the privileged mode to the chaos pod.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.labels</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the label for the ChaosPod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined<i> (type:map[string]string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td> The <code>.spec.definition.labels</code> allow developers to specify the ChaosPod label for an experiment. </td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.securityContext.podSecurityContext</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify security context for ChaosPod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined<i> (type:corev1.PodSecurityContext)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td> The <code>.spec.definition.securityContext.podSecurityContext</code> allows the developers to specify the security context for the ChaosPod which applies to all containers inside the Pod.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.configmaps</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the configmap for ChaosPod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined<i></td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td> The <code>.spec.definition.configmaps</code> allows the developers to configure the container(s) in that ChaosPod based on the data in the ConfigMap.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.secrets</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the secrets for ChaosPod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined<i></td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td> The <code>.spec.definition.secrets</code> specify the secret data to be passed for the ChaosPod. The secrets should contain confidential information like credentials.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.experimentannotations</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the custom annotation to the ChaosPod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined<i> (type:map[string]string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td> The <code>.spec.definition.experimentannotations</code> allows the developer to specify the Custom annotation for the chaos pod.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.hostFileVolumes</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the host file volumes to the ChaosPod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>user-defined<i> (type:map[string]string)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td> The <code>.spec.definition.hostFileVolumes</code> allows the developer to specify the host file volumes to the ChaosPod.</td>
</tr>
</table>

<table>
<tr>
  <th>Field</th>
  <td><code>.spec.definition.hostPID</code></td>
</tr>
<tr>
  <th>Description</th>
  <td>Flag to specify the host PID for the ChaosPod</td>
</tr>
<tr>
  <th>Type</th>
  <td>Optional</td>
</tr>
<tr>
  <th>Range</th>
  <td><i>true, false</i> (type:bool)</td>
</tr>
<tr>
  <th>Default</th>
  <td><i>n/a</i></td>
</tr>
<tr>
  <th>Notes</th>
  <td> The <code>.spec.definition.hostPID</code> allows the developer to specify the host PID  for the ChaosPod. </td>
</tr>
</table>
