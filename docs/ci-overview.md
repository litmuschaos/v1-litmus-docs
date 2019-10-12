---
id: ci-overview
title: Reference Implementation - OpenEBS CI 
sidebar_label: Overview 
---
------

One of the design goals of the Litmus framework is the ability to seamlessly integrate with 
Continuous Integration frameworks to implement the e2e pipelines post build & unit/integration 
tests. The OpenEBS CI framework, which is based on GitLab (enterprise edition), uses Litmus 
to power its E2E pipelines. 

Gitlab EE (enterprise-edition) is the core execution engine of the OpenEBS CI infra, which 
is focused on continuous evaluation of the OpenEBS cloud-native persistent storage solution 
as a whole with all its components, while tracking commits to the core subsystems, namely: 

- Storage Engines (jiva, cStor) 
- Storage orchestrator (control plane) (Maya)

In addition, the CI/CD pipelines are also triggered on updates to the e2e repositories, 
thereby ensuring quick turnaround times for establishing the sanity of both feature/product 
code as well as the test cases.

Some of the compelling features, among other standard ones (such as two factor auth, webhook 
support etc.,) which aided in making this choice are listed below: 

- Availability of an intuitive and well-defined user-interface that provides pipeline views, 
artifact storage (explorable/downloadable), and dependency definitions. 

- Ability to run as a Kubernetes deployment, with easy setup (helm) & capacity to infinitely 
scale “gitlab-runners” as new jobs are added.

- The possibility of dogfooding i.e., using OpenEBS storage as the backend store (Postgres) 
for Gitlab server.

The subsequent sections will explain the general framework & workflow of the Gitlab-based 
OpenEBS CI followed by details of how Litmus is used to drive the e2e pipelines.



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
