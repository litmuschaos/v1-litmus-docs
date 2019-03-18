---
id: prerequisites
title: Litmus Pre-Requisites
sidebar_label: Pre-Requisites 
---
------

- Healthy Kubernetes Cluster (size depends on test scenario)

- Test harness instance with access to the cluster & installed with kubectl. 

- Set Kubernetes admin context

- Obtain Access Key details in case of certain managed clusters (ex: EKS). These need to 
be passed as ENV in the litmusbooks before execution

- Ensure that the package dependencies for the storage provider which will be used in the 
tests are installed. For ex. OpenEBS storage classes require iSCSI initiators to be installed 
on all nodes 

- In the case of on-premise solutions such as Openshift, ensure that the project and user 
under which the Litmus e2e is executed has sufficient permissions. 

- Verify that the security policies are updated with necessary changes to create & consume 
the given storage provider’s persistent volume.


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
