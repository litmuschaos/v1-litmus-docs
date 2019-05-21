---
id: gitlabinfra 
title: Gitlab Framework Components 
sidebar_label: Gitlab Infrastructure
---
------

This page briefly explains the Gitlab based infrastructure of the OpenEBS CI framework.

![gitlabinfra](/docs/assets/ci-workflows/gitlab_infrastructure.svg)

## <font size="6">Gitlab CI Server</font>

The Cloud-Native Gitlab (EE) Server (represented by the black box in the schematic diagram) 
is hosted on a multi-node baremetal OpenShift Cluster with all its components 
(Unicorn, Shell, Workhorse, Registry, Sidekiq, Gitaly, PostgreSQL, Redis, Minio) running 
as deployments.

## <font size="6">Source Repositories</font>

The Gitlab CI server is integrated & setup to monitor the OpenEBS Github source repositories 
(maya, jiva, zfs/cStor & e2e) via pull-based repository mirroring, i.e., creation of Gitlab 
repositories corresponding to its respective source on Github, that are automatically updated 
via a webhook mechanism whenever there are commits to the source repos. These repositories 
are configured with the `.gitlab-ci.yml` files that specify the build/CI steps to be performed 
upon commits.


## <font size="6">Gitlab Runners</font>

As part of Gitlab’s CI orchestration, each of the aforementioned OpenEBS components is 
configured with dedicated Gitlab Runners, which are responsible for running the Gitlab Jobs 
carrying out the build steps. The Gitlab runner implements different kinds of “executors”, 
i.e., entity (machine) that runs these steps. The Maya & Jiva repositories are mapped to 
“Shell Executors” that run the build steps in pre-configured VMs (installed with all build 
dependencies), while the zfs/cStor & e2e repositories are mapped to “Docker-Machine” 
executors which are lightweight VMs with Docker installed. In case of the latter, the build 
steps are carried out inside the docker containers running on the executor (the docker image 
contains the necessary build tools and packages). The “docker-machine” executors are inherently 
auto-scaling, which is a necessary feature for e2e builds, as multiple parallel jobs are 
spawned during the course of e2e pipeline stages. 



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
