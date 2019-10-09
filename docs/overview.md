---
id: overview
title: Welcome to Litmus Documentation 
sidebar_label: Overview 
---
------

## Litmus Overview

Modern cloud native systems are expected to have a high degree of resiliency and sustain failures. 
To achieve this most of the enterprises are either already practicing or advised to practice 
chaos engineering both during the implementation of systems and in production. By using Litmus powered chaos engineering practices, 
failures are converted to resiliency. 

Litmus is a framework for e2e testing and chaos engineering for Kubernetes, focusing on stateful workloads.
The primary objective of Litmus is to ensure a consistent and reliable behavior of Kubernetes for various 
persistent workloads and to catch hard-to-find or unacceptable issues. It provides the pieces to construct 
and also hosts a ready set of “deployable tests” called “Litmusbooks”, or “Litmus experiments” 
or “Chaos experiments” which are essentially Kubernetes jobs running test containers. 

<br><img src="/docs/assets/litmus.svg" alt="Litmus Overview" width="800"/>

<br>

## Who uses Litmus ?

Kubernetes developers writing stateful applications use Litmus books to easily perform chaos experiments or litmus experiments. DevOps administrators use Litmus to build CI/E2E pipelines where most of the pipeline jobs are already available as Litmus books and can tune the remaining jobs quickly. 



## How to use Litmus ?

Litmus books are defined as Kubernetes jobs. All Litmus experiments are conducted using the standard kubectl command.

```
kubectl create -f <litmus-experiment.yaml>
```



## Why Litmus ?

Kubernetes is the de-facto standard for container orchestration today with an ever-growing increase 
in the adoption of stateful applications. DevOps teams managing stateful workloads have an increasing need 
to validate real world performance of their environments, especially for day-1/day-2 operations around 
application/storage maintenance and resiliency to various component failures, something which is typically 
not covered by unit or integration tests. DevOps teams need an easy to use framework mainly for the following reasons :

- Building various jobs in CI pipelines that are part of the core infrastructure, so that they can just 
  concentrate on their own business logic. Chaos experiments are performed at various layers such as application and storage
- Build pipelines for CI/E2E pipelines for validating and certifying new Kubernetes versions before moving to production
- Introduce chaos experiments in production to validate the resiliency of the systems. Through these experiments the failures are detected in a planned manner rather than finding them accidentally.

Litmus provides a means by which these scenarios are executed as (e2e) tests with easy provision to integrate 
them into the CI/CD pipeline. It achieves this in a Kubernetes-native way, using end-user tools such as kubectl 
and employing chaos engineering practices, while maintaining simple interfaces for user inputs & results.



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
