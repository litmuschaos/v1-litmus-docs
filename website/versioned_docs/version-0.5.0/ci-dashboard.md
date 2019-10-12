---
id: version-0.5.0-ci-dashboard
title: CI/E2E Results
sidebar_label: CI Dashboard
original_id: ci-dashboard
---
------

The benefits provided by the CI dashboard include: 

- An integrated view of the “build” & “e2e” pipelines, across source branches & platforms 
  for a given commit 

  ![ci-summary](/docs/assets/openebs.ci-screens/ci-summary.jpg)

- Details of the baseline commit (with links to the relevant commit/pull request details on github) 
  against which the pipelines were triggered, along with relative versions of other OpenEBS components 
  used in the e2e tests

  ![commit-info](/docs/assets/openebs.ci-screens/commit-info.jpg)

- Job summary in a given e2e pipeline with ability to navigate to desired stages (graph nodes) 
  across pipelines

  ![job-summary](/docs/assets/openebs.ci-screens/job-summary.jpg)

- Access to the pipeline’s execution logs on Kibana 

  ![log-link](/docs/assets/openebs.ci-screens/log-link.jpg)

  Sample kibana dashboard with default filters: 

  ![kibana-ds](/docs/assets/openebs.ci-screens/kibana-dashboard.jpg)

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
