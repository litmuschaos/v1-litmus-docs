---
id: logging 
title: EFK-Based Logging Framework
sidebar_label: E2E Logging Framework
---
------

OpenEBS CI uses the popular EFK (Elasticsearch-Fluentd-Kibana) stack as the logging framework 
for the e2e pipelines. Each target cluster brought up as part of the e2e pipeline is configured 
with the fluentd-forwarder daemonset & fluentd-aggregator deployment, with the latter streaming 
the logs to the remote ElasticSearch instance running on the master (Gitlab-CI) cluster, which 
are then rendered by the Kibana visualization platform (also running on the master cluster). 

The master cluster is also configured with local instances of the fluentd forwarder & aggregators 
in order to collect its own logs.

The fluentd forwarders in both the master & remote (target) clusters are tuned to collect desired 
logs (for example, in the case of target clusters’,  kube-system logs are neglected) and appropriate 
filters based on gitlab pipeline IDs & baseline commit IDs are provided to aid quick data search 
and analysis on Kibana. 

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
