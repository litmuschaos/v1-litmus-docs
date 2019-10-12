---
id: cb-overview
title: How to write a Litmusbook 
sidebar_label: Overview 
---
------

The Litmus framework adopts a user-friendly structure in which addition 
of new experiments (tests) can be an easy exercise without too-much logic 
building. However, it does involve packaging the test in the standard 
litmusbook structure and reusing/creating simple ansible task files and 
playbooks. Here is a quick refresher on the moving parts & basic process 
flow in a Litmus experiment:

- The deployable/executable artifact associated with the Litmus experiment 
is called Litmusbook. This is a Kubernetes Job (run_litmus_test.yml) 

- The Litmusbook runs & manages the “ansible-runner” container

- The ansible-runner container executes the test playbook (test.yml) as 
the entrypoint function. 

- The test playbook executes several locally defined tasks as well as 
those in (statically imported) LitmusLib utils/taskfiles (viz. common, 
funclib, chaoslib) 

- The LitmusLib utils may utilize specific “third-party” tools (deployed 
as Kubernetes deployments or daemonsets) to perform specific functions

- Test result is updated in a dedicated Kubernetes custom resource called 
litmusresult

The subsequent sections will explain how an interested user/developer can 
approach the creation of a new Litmus Experiment. An intermediate-level 
knowledge of ansible (& of course, Kubernetes) is expected. 


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
