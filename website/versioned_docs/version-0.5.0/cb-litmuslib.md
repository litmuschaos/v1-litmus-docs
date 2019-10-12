---
id: version-0.5.0-cb-litmuslib
title: Using the Litmus Utils
sidebar_label: Leveraging LitmusLib
original_id: cb-litmuslib
---
------

Litmus provides multiple ansible utils (task files) to perform 
Kubernetes, Storage (OpenEBS provider) & Chaos operations. The 
LitmusLib lends modularity to the litmusbook & achieves code 
reuse in the project. 

Once the experiment flow is identified, it is recommended to explore 
the existing list of utils to map to the test steps/blocks. In the 
event where an existing util (or a set of utils) cannot satisfy the 
experiment’s requirements, new utils can be created in conformance 
with the following characteristics: 

## <font size="6">Interface (Arguments)</font>

Each util is invoked with explicit arguments from the playbook 
(or a parent taskfile), passed as “include_vars”. For example, 
deployment details such as manifest paths, namespaces, service 
endpoints & labels (refer the individual utils readme for exact info). 
Typically, these don’t “return” any data to the main playbook (the 
scope of ansible register variables is valid/global across the 
lifetime of a playbook).

## <font size="6">Function</font>

Each util adheres to a definite purpose/function. Typically, utils 
consist of the logic to either manipulate cluster resources (create,
scale, patch, upgrade, fail, remove etc., therefore changing cluster 
state), run status checks on specific cluster components (namespaces, 
pods, nodes) or execute some stateful application-specific tasks 
(data writes, reads, integrity-checks). 

Some of the utils (esp. in chaoslib) use other supporting tools to 
perform its function. These are deployed, used & cleaned up as part 
of the util’s run. 

## <font size="6">Category</font>

Based on the function it performs, a util is categorized as belonging 
to a particular library (chaoslib, funclib or common) & placed accordingly 
in the Litmus repository directory structure. 

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
