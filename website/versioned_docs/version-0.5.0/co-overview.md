---
id: version-0.5.0-co-overview
title: Kubernetes Operator For Chaos
sidebar_label: Overview
original_id: co-overview
---
------

While the Litmus execution model with its experiments provides a simple way to 
integrate chaos engineering into the CI framework, there are a few additional 
requirements when it comes to using it in deployment environments (dev/staging/
pre-prod/production). These include: 

- Ability to schedule the execution of an experiment or batch of chaos experiments
 
- Ability to monitor chaos runs & visualize results over a period of time 
  (say, across builds/releases)

- A standard specifiction of the chaos experiment(s) along with its attributes
  (such as, rank/priority) 

- Availability of categorized experiment bundles 

- Ability to chaos run as a background service based on annotations/labels 

The Litmus Chaos Operator fills this gap & satisfies the above requirements by
making use of the Operator paradigm to watch & reconcile a Custom Resource (CR)
called ChaosEngine, which describes the chaos intent of the developer/devops engineer
mapped against a given application deployment. 

With the Chaos Operator, setting up chaos in your cluster involves the following 
simple steps: 

- Install the Litmus infrastructure components (RBAC, CRDs), the Operator & Experiment 
custom resource bundles via helm charts

- Annotate the application under test (AUT), enabling it for chaos

- Create a ChaosEngine custom resource tied to the AUT, which describes the experiment 
list to be executed


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
