---
id: logs 
title: Capturing & Viewing Logs  
sidebar_label: Log Collection & Analysis
---
------

Litmus test pod logs (playbook execution logs) as well as that of the application and 
storage pods are automatically collected as part of any standard Kubernetes logging 
frameworks such as fluentd. 

However, in the absence of other mechanisms, Litmus provides a (stern-based) logger 
container, that can be run as a sidecar to the ansible-runner in the Litmus pod. 
The logger collects both the pod (stdout) logs as well as the cluster nodes’ kubelet logs 
& places them in a user-specified location on the host. This simple support bundle
can be used for debug purposes. 

It allows for selective pod capture (pod list specified by comma-separated list of 
starting literals) for a given duration.


<!-- Hotjar Tracking Code for https://docs.openebs.io -->

<script>
   (function(h,o,t,j,a,r){
       h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
       h._hjSettings={hjid:785693,hjsv:6};
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
