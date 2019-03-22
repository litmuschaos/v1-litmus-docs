---
id: platforms 
title: E2E Platforms Supported by Litmus 
sidebar_label: E2E Platforms
---
------

The OpenEBS e2e pipelines can be executed on several platforms, with Litmus providing cluster 
creation playbooks for a majority of them. They are categorized as: 

- Baremetal Cloud: Packet (ARM based physical servers)
- Managed Kubernetes Clusters: GKE, EKS, AKS 
- Cloud hosted Clusters: KOPS based clusters on AWS, GCP instances
- On-premise Solutions: OpenShift (vSphere VMs, AWS instances)

While most Litmus experiments are platform-agnostic, a minimal number are currently supported 
only on certain platforms, with efforts in progress to extend support across others. 

The CI for the OpenEBS project makes use of Packet Cloud as the platform of choice, running 
multiple e2e pipelines on it corresponding to different Kubernetes versions (1.11, 1.12 & 1.13 currently). 

## <font size="6">Packet</font>

The platform is a single-master, multi-node cluster built using kubeadm on ARM-based baremetal 
servers. The cluster creation playbook requires some mandatory user-inputs such as the Packet 
project_id & some optional arguments, such as k8s_version, clustername, node_count, operating_system, 
instance_type & taint_value (if a cluster node is required to be tainted with a specific key and action). 

Litmus also provides a disk creation playbook on Packet that creates the Datera-based Packet block 
storage devices & attaches to the nodes with size and performance_tier as extra vars. 

It requires the Packet API key to be configured as ENV on the job executor.


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
