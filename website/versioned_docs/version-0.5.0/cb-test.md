---
id: version-0.5.0-cb-test
title: Testing the Litmus test
sidebar_label: Testing Litmusbooks
original_id: cb-test
---
------

A “dev” image of the ansible-runner, with the newly created test 
playbooks needs to be built, pushed to the desired repo & updated in 
the litmus job spec (litmus book) before deploying/testing it. 
However, users who wish to refrain from pushing development images 
into public/private repositories can instead download this “dev” image 
on the cluster nodes with imagePullPolicy of the custom ansible-runner 
set to “Never”. 

Also, it is necessary to have the environment (platform, application 
configured with PVCs of desired storage classes) for which the test is 
built, in place, before trialing the litmus book. 

It is recommended to perform negative testing of the litmusbook too, in 
order to gauge how test failures at various points impacts the cluster. 
The test playbooks (and by extension, the utils) make use of ansible’s 
version of the try-catch construct, i.e., the block-rescue-always flow 
to define the error-handling logic.

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
