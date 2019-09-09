---
id: overview
title: Welcome to Litmus Documentation 
sidebar_label: Overview 
---
------

## Litmus Overview

Modern cloud native systems are expected to have a high degree of resiliency and sustain failures. 
To achieve this most of the enterprises are either already practicing or advised to practice 
chaos engineering both during the implementation of systems and in production. By using Litmus powered chaos engineering practices,failures are converted to resiliency. 

Litmus is a framework for e2e testing and chaos engineering for Kubernetes, focusing on stateful workloads.The primary objective of Litmus is to ensure a consistent and reliable behavior of Kubernetes for various persistent workloads and to catch hard-to-find or unacceptable issues. It provides the pieces to construct and also hosts a ready set of “deployable tests” called “Litmusbooks”, or “Litmus experiments” or “Chaos experiments” which are essentially Kubernetes jobs running test containers. 

While Litmus experiments were developed initially to test if a given stateful workload is suitable for running on OpenEBS(a Kubernetes dynamic storage provisioner), the use cases now are broader and overall system resilience can be characterized before and during operations.

<br><img src="/docs/assets/litmus.svg" alt="Litmus Overview" width="800"/>

<br>

## Core Components:

Litmus is an umbrella project that incorporates different pieces of a typical chaos engineering environment to deliver a complete solution to its users. Some of the core components include:
1. <b>Litmus:</b><br> The actual execution framework & repository of ready/configurable chaos experiments (mostly written as ansible playbooks & executed as Kubernetes jobs). The jobs are often executed in CI pipelines as part of e2e (refer https://openebs.ci)
2. <b>Chaos-Operator:</b><br> A Kubernetes Operator that watches & acts on custom resources defining litmus chaos experiment workflows. Typically used in deployment environments (dev/staging/pre-prod/prod) where chaos experiments can be scheduled & monitored against specific applications.
3. <b>Chaos-Exporter:</b><br> A Prometheus Exporter that exposes chaos metrics based on experiment results.


## Who uses Litmus ?

Kubernetes developers writing stateful applications use Litmus books to easily perform chaos experiments or litmus experiments. DevOps administrators use Litmus to build CI/E2E pipelines where most of the pipeline jobs are already available as Litmus books and can tune the remaining jobs quickly. 



## Quickstart:

Litmus experiment jobs(also called Litmusbooks) run using a dedicated ServiceAccount in the Litmus namespace. Setup RBAC & custom resource definitions (CRDs) via kubectl or helm, as shown below:
  <details>
  <summary>Using kubectl:<b>Click here to see the process.</b></summary>
  <ol>
  <li>git clone https://github.com/openebs/litmus.git</li>
  <li>cd litmus</li>
  <li>kubectl apply -f hack/rbac.yaml</li>
   <li>kubectl apply -f hack/crds.yaml  </li>
</ol>
  </details>
<details>
<summary>Using helm:<b>Click here to see the process.</b></summary>
<ol>
<li>helm repo add https://litmuschaos.github.io/chaos-charts</li>
<li>helm install litmuschaos/litmusInfra --namespace=litmus</li>
</ol>
</details>
<br><br>
 Litmus experiments can be run using the following command:

```
kubectl create -f <litmus-experiment.yaml>
```



## Why Litmus ?

Kubernetes is the de-facto standard for container orchestration today with an ever-growing increase 
in the adoption of stateful applications. DevOps teams managing stateful workloads have an increasing need to validate real world performance of their environments, especially for day-1/day-2 operations around application/storage maintenance and resiliency to various component failures, something which is typically not covered by unit or integration tests. DevOps teams need an easy to use framework mainly for the following reasons :

- Building various jobs in CI pipelines that are part of the core infrastructure, so that they can just 
  concentrate on their own business logic. Chaos experiments are performed at various layers such as application and storage
- Build pipelines for CI/E2E pipelines for validating and certifying new Kubernetes versions before moving to production
- Introduce chaos experiments in production to validate the resiliency of the systems. Through these experiments the failures are detected in a planned manner rather than finding them accidentally.

Litmus provides a means by which these scenarios are executed as (e2e) tests with easy provision to integrate them into the CI/CD pipeline. It achieves this in a Kubernetes-native way, using end-user tools such as kubectl and employing chaos engineering practices, while maintaining simple interfaces for user inputs & results.



<br>

<br>

<hr>

<br>

<br>



<!-- Hotjar Tracking Code for https://docs.openebs.io -->

<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:1239116,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>


<!-- Global site tag (gtag.js) - Google Analytics -->

<script async src="https://www.googletagmanager.com/gtag/js?id=UA-92076314-12"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-92076314-12');
</script>
