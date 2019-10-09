---
id: version-0.5.0-ci
title: Litmus Powered CI Pipelines
sidebar_label: CI Integration
original_id: ci
---
------

## <font size="6">Litmus e2e In CI Pipelines</font>

Litmus can be integrated into an application or storage provider’s CI pipeline post 
the build & unit/integration test phases to test real-world behaviour on Kubernetes 
clusters. Litmus provides useful utilities that can aid the deployment of the latest 
images with extremely quick turnaround times. These include: 

Cluster Creation Playbooks to aid quick and easy creation of Kubernetes clusters on 
different popular cloud platforms (GCP, AWS, GKE, AKS, EKS, Packet Cloud, On-premise 
vSphere VMs, OpenShift-on-AWS, OpenShift-on-vSphere) with minimal config inputs 

Litmusbooks to setup the storage provider pre-requisites (such as the OpenEBS control 
plane/operator) on a K8s cluster. 

The litmusbook execution can be overseen by CI-tool specific job wrappers with the 
Result CRs used to derive the success of the pipeline jobs/stages.

Openebs.ci is a reference implementation of the above, where a gitlab-based CI framework 
makes use of Litmus to power the e2e phase upon commits to the storage control plane 
and data plane code repositories.

<img src="/docs/assets/litmuse2e.svg" alt="Litmus powered CI/E2E pipelines" width="900"/>



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
