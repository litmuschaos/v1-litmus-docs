---
id: cb-bestpractices
title: Litmusbook Best Practices 
sidebar_label: Best Practices
---
------

Here are some guidelines while constructing litmusbooks, which should 
be followed to the extent possible: 

- All steps of an experiment should be executable from within the test 
container, i.e.,  localhost without the need to delegate action to remote 
nodes (ex: installation of packages). In exceptional cases, privileged 
daemonsets can be used to achieve the purpose. 

- The immutability of the test container should be maintained, i.e., 
artifacts should be generated from templates with values derived from the 
litmusbook job ENV

- Kubernetes resource details should be derived from the spec using kubectl 
functions such as -o {jsonpath, custom-columns, go-template, field-selector}

- It would be good to define resource requests/limits on the litmus 
kubernetes jobs 

- Avoid system operations such as directory/file creation removal etc., 
using ansible shell modules as they are not idempotent. 

- Generously add ‘debug messages’ that can be logged to aid troubleshooting 
(ansible: use “debug” module with “msg” flags)

- Include proper error/exception handling procedures (ansible: block_rescue, 
failed_when, var.defined, file.exists etc..,)

- Lint the test code, while explaining decisions on exceptions

- Document the litmus experiment to aid users in employing the litmus book 
directly or in CI/e2e pipelines.







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
