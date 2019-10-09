---
id: version-0.5.0-workloads-dashboard
title: Reference Stateful Applications
sidebar_label: Workloads Dashboard
original_id: workloads-dashboard
---
------

OpenEBS hosts several production stateful applications on GKE as reference workloads 
that use OpenEBS PVs (cStor storage engine) as the underlying storage. These PVs are 
periodically upgraded based on successful builds from the master. 


The openebs.ci portal consists of a “Workload Dashboard” that provides a summary view 
of all stateful applications (with details such as status, type, PV versions, replica count) 
while also maintaining a detailed real-time view of each application in dedicated dashboards. 

## <font size="6">Application Dashboards</font>

The application dashboards carry detailed information of the stateful application and 
importantly, also provides users with interfaces for live interaction with the application 
on the cluster. These are highlighted in the screenshots below: 

- Real-time status of the stateful application replicas

  ![app-status](/docs/assets/openebs.ci-screens/real-time-app-status.jpg)

- Deployment details (link to YAML manifests, namespace, labels, PV versions)

  ![app-deploy-info](/docs/assets/openebs.ci-screens/app-deployment-details.jpg)

- Interface to list OpenEBS volumes associated with the application

  ![app-storage-info](/docs/assets/openebs.ci-screens/app-storage-info.jpg)

- Interface to perform simple I/O (writes, reads) on the application to verify stability/ 
  operational storage

  ![app-storage-IO](/docs/assets/openebs.ci-screens/app-IO.jpg)

- Interface to induce chaos on the application/storage components using Litmus APIs with 
  visibility into progress / logs of the chaos operation

  ![app-chaos-1](/docs/assets/openebs.ci-screens/app-chaos-1.jpg)

  The application replica status can be observed for changes during the course of the chaos
  test.

  ![app-chaos-2](/docs/assets/openebs.ci-screens/app-chaos-2.jpg)

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
