---
id: version-0.5.0-cb-quality
title: Desired features of a Litmusbook
sidebar_label: Quality Parameters
original_id: cb-quality
---
------

Some of the basic quality parameters associated with a litmusbook 
(common to any form of code) & their meaning (in litmus context) 
are listed below: 

- Reliability: The experiment gives the same result under unchanged 
conditions (which includes test environment and versions of the 
components under test). In other words, the test does not provide 
random false positives/negatives.

- Maintainability: The test playbook can be decomposed into well 
defined task files and utils that can be maintained & updated 
individually 

- Extensibility: An experiment with platform dependent tasks can be 
easily extended to run on other platforms with minimal implementation 
effort. 

- Usability: Often, the increasing test complexity can be gauged by 
a proliferation of user inputs (ENVs) in the litmus book. This is a 
judgement the user will have to make - to keep the test simple/focused, 
yet effective. 



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
