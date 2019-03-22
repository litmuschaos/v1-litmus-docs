---
id: ci-workflow 
title: OpenEBS CI Workflow 
sidebar_label: CI Workflow 
---
------

This page briefly explains the OpenEBS CI workflow  

## <font size="6">Phases of OpenEBS CI</font>

The standard CI workflow, triggered by commits to the monitored source repositories, 
can be split into two logical phases, each running a distinct set of pipelines, namely 
“build” & “e2e”. The build pipeline cascades into the e2e pipelines via appropriate 
triggers in the .gitlab-ci.yml. 

The build phase typically involves executing the `make` process - each of the OpenEBS 
component source repos for which the build pipelines are setup includes a Makefile with 
well defined targets & dependencies that executes the following steps:

- Runs unit tests 
- Compiles the go code 
- Builds docker images 
- Runs integration tests 
- Pushes image tagged with commit IDs to the container repositories (docker hub/quay)
- Performs certain pre-e2e routines 
- Finally triggers the e2e pipelines  

This entire process is carried out in single pipeline. 

## <font size="6">Baseline Commit</font>

Before triggering the e2e pipelines as part of its final step, the build pipeline performs 
a pre-e2e routine to generate metadata about the impending e2e run. As is evident from the 
preceding sections, the e2e pipelines are triggered against commits to any of the OpenEBS 
component repos (maya, jiva, zfs/cstor, e2e). Images pushed (commit ID as image tags) as 
part of the build pipeline are deployed during the e2e. Therefore, it is necessary to baseline 
or identify an e2e run against the primary trigger (commit) while maintaining details of 
image versions of the other components relative to it. 

This is achieved by writing the details of the baseline commit 
(timestamp, component repo, branch & commit ID) into the file head of a “baseline artifact” 
maintained in a separate repository. Once the e2e pipeline is initiated, the baseline 
artifact is parsed for the “most current” image tags of each component (which will invariably 
include the current baseline commit & latest ones for other components) in the test-bed 
preparation stage & this information is then used to precondition the OpenEBS Operator manifest 
before its deployment on the clusters.

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
