---
id: overview
title: Welcome to Litmus Documentation 
sidebar_label: Overview 
---
------

## <font size="6">Overview - What is Litmus ?</font>

Modern cloud native systems are expected to have a high degree of resiliency and sustain failures. 
To achieve this most of the enterprises are either already practicing or advised to practice 
chaos engineering both during the implementation of systems and in productions. Through chaos engineering, 
failures are converted to resiliency. 

Litmus is a framework for e2e testing and chaos engineering for Kubernetes, focusing on stateful workloads.
The primary objective of Litmus is to ensure a consistent and reliable behavior of Kubernetes for various 
persistent workloads and to catch hard-to-find or unacceptable issues. It provides the pieces to construct 
and also hosts a ready set of “deployable tests” called “Litmusbooks”, or “Litmus experiments” 
or “Chaos experiments” which are essentially kubernetes jobs running test containers. 

## <font size="6">Why Litmus ?</font>

Kubernetes is the de-facto standard for container orchestration today with an ever-growing increase 
in the adoption of stateful applications. DevOps teams managing stateful workloads have an increasing need 
to validate real world performance of their environments, especially for day-1/day-2 operations around 
application/storage maintenance and resiliency to various component failures, something which is typically 
not covered by unit or integration tests. DevOps teams need an easy to use framework mainly for two reasons :

- Building various jobs in CI pipelines that are part of the core infrastructure, so that they can just 
concentrate on their own business logic
- Performing chaos experiments at various layers such as application and storage

Litmus provides a means by which these scenarios are executed as (e2e) tests with easy provision to integrate 
them into the CI/CD pipeline. It achieves this in a Kubernetes-native way, using end-user tools such as kubectl 
and employing chaos engineering practices, while maintaining simple interfaces for user inputs & results.

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
