---
id: co-components
title: Chaos Operator Components 
sidebar_label: Operator Internals    
---
------

The Chaos Operator is a Kubernetes Operator, which are nothing but custom-controllers with 
direct access to Kubernetes API that can manage the lifecycle of certain resources or applications, 
while always trying to ensure the resource is in the "desired state". The logic that ensures 
this is commonly called "reconcile" function.

The Chaos Operator is built using the popular Operator-SDK framework, which provides bootstrap 
support for new operator projects, allowing teams to focus on business/operational logic.

The Litmus Chaos Operator helps reconcile the state of the ChaosEngine, a custom resource that 
holds the chaos intent specified by a developer/devops engineer against a particular stateless/stateful 
Kubernetes deployment. The operator performs specific actions upon CRUD of the ChaosEngine, its 
primary resource. The operator also defines secondary resources (the engine runner pod and engine 
monitor service), which are created & managed by it in order to implement the reconcile functions.



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
