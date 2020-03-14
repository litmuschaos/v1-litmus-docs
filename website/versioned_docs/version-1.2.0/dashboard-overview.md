---
id: version-1.2.0-dashboard-overview
title: CI/E2E Result Visualization Portal
sidebar_label: Overview
original_id: dashboard-overview
---
------

While Gitlab does provide a clear representation of build stages via individual pipeline graphs, 
the OpenEBS CI workflow consists of multiple distinct pipelines making it a difficult exercise to 
correlate results & derive desired info. 

[Openebs.ci](https://openebs.ci/) is an online portal that simplifies visualization of this data 
via a CI dashboard, which caters to both the developer and user communities to obtain “build” & 
“e2e” results against commits to the core OpenEBS component repositories across different branches. 

It also provides access to multiple workload dashboards that provide a real-time view of production 
workloads using OpenEBS PVs. 



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
