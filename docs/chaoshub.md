---
id: chaoshub 
title: Using and contributing to ChaosHub
sidebar_label:ChaosHub 
---
------


**Important links**

Chaos Hub is maintained at https://hub.litmuschaos.io

To contribute new chaos charts visit: https://github.com/litmuschaos/chaos-charts

**Introduction**

Litmus chaos hub is a place where the chaos engineering community members publish their chaos experiments. A set of related chaos experiments are bundled into a `Chaos Chart`. Chaos Charts are classified into the following categories.

- [Generic Chaos](#generic-chaos)
- [Application Chaos](#application-chaos)
- [Platform Chaos](#platform-chaos)



### Generic Chaos 

Chaos actions that apply to generic Kubernetes resources are classified into this category. Following chaos experiments are supported under Generic Chaos Chart

<table>
<tr>
<th>Experiment name</th>
<th>Description</th>
<th> User guide link </th>
</tr>
<tr>
<td>Container Kill</td>
<td>Kill one container in the application pod</td>
<td></td>
</tr>
<tr>
<td>POD Delete</td>
<td>Fail the application pod</td>
<td><a href="https://docs.litmuschaos.io/docs/pod-delete">pod delete</a></td>
</tr>
<tr>
<td>Pod Network Latency</td>
<td>Experiment to inject network latency to the POD</td>
<td>-</td>
</tr>
<tr>
<td>Pod Network Loss</td>
<td>Experiment to inject network loss to the POD</td>
<td>-</td>
</tr>
<tr>
<td>CPU Hog</td>
<td>Exhaust CPU resources on the Kubernetes Node</td>
<td></td>
</tr>
<tr>
<td>Disk Fill</td>
<td></td>
<td></td>
</tr>
<td>Disk Loss</td>
<td>External disk loss from the node</td>
<td></td>
</tr>
</table>

### Application Chaos

While Chaos Experiments under the Generic category offer the ability to induce chaos into Kubernetes resources, it is difficult to analyze and conclude if the chaos induced found a weakness in a given application. The application specific chaos experiments are built with some checks on *pre-conditions* and some expected outcomes after the chaos injection. The result of the chaos experiment is determined by matching the outcome with the expected outcome. 

<div class="danger">
<strong>NOTE:</strong> If the result of the chaos experiment is `pass`, it means that the application is resilient to that chaos.
</div>


**Benefits of contributing an application chaos experiment**

Application developers write negative tests in their CI pipelines to test the resiliency of the applications. These negative can be converted into Litmus Chaos Experiments and contributed to ChaosHub, so that the users of the application can use them in staging/pre-production/production environments to check the resilience. Application environments vary considerably from where they are tested (CI pipelines) to where they are deployed (Production). Hence, running the same chaos tests in the user's environment will help determine the weaknesses of the deployment and fixing such weaknesses leads to increased resilience. 



Following Application Chaos experiments are available on ChaosHub



| Application | Description                               | Chaos Experiments                                         |
| ----------- | ----------------------------------------- | --------------------------------------------------------- |
| OpenEBS     | Container Attached Storage for Kubernetes | Replica Kill, Controller Kill, cStorPool instance failure |
| Kubernetes  | Orchestration platform for Containers     |                                                           |
|             |                                           |                                                           |

### Platform Chaos

Chaos experiments that inject chaos into the platform resources of Kubernetes are classified into this category. Management of platform resources vary significantly from each other, Chaos Charts may be maintained separately for each platform (For example, AWS, GCP, Azure, etc)

Following Platform Chaos experiments are available on ChaosHub



| Platform | Description                                 | Chaos Experiments |
| -------- | ------------------------------------------- | ----------------- |
| AWS      | Amazon Web Services platform. Includes EKS. | None              |
| GCP      | Google Cloud Platform. Includes GKE.        | None              |
| Azure    | Microsoft Azure platform. Includes AKS.     | None              |
|          |                                             |                   |


<!-- Global site tag (gtag.js) - Google Analytics -->

<script async src="https://www.googletagmanager.com/gtag/js?id=UA-92076314-12"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-92076314-12');
</script>
