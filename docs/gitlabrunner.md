---
id: gitlabrunner 
title: Gitlab Jobs for Litmus Experiments
sidebar_label: Gitlab Job Runner Template
---
------

Each Gitlab job goes through the following phases: Prepare (job executor deployed), 
Pre-build (clone source repo, download artifacts, restore cache), Build (run build steps), 
Post-build (upload artifacts, create cache). The build steps are typically placed in 
“runner scripts” that are invoked (with desired arguments) as part of the .gitlab-ci.yml’s 
execution. In case of the e2e jobs, these build steps are executed inside a custom container, 
packaged with required tools & running on the docker-machine executor. The steps involve 
running & monitoring a litmus experiment (litmusbook). 

The standard template maintained in these (bash) runner scripts & tasks performed therein 
is described below:

## <font size="6">Generate Unique Test Name</font>

Each gitlab job is associated with a litmus experiment, which has a test/experiment name. 
The result of this litmus experiment is stored in a Litmus Custom Resource (CR) of the same name. 
The success of a test & thereby the gitlab job is derived from this CR. Sometimes, it is possible 
that the same litmus experiment is run against different applications or storage engines in a 
pipeline, thereby necessitating a unique element or ID in the CR name. In this step a user-defined 
input (run_id ) is accepted to generate a unique test/CR name. 

## <font size="6">Setup Dependencies</font>

Depending on the nature of the gitlab job (cluster create/delete playbooks OR litmus experiments) 
the executor machine is updated with the appropriate directory structure & target cluster 
metadata (such as cluster configuration file, cluster names, disk details, VPC information etc..,) 
to ensure successful execution.

## <font size="6">Precondition Litmusbook</font>

Each litmusbook (the Kubernetes job specification YAML) consists of  a default set of test inputs 
(placeholders for application, storage, chaos info etc..,). These are overridden/replaced by desired 
values in this step. Also, the default name of the test is replaced with the unique name generated 
by the runner at the start of execution.

## <font size="6">Run Litmus Experiment</font>

The litmusbook is deployed & monitored for completion, with a polling interval of 10s. Both the 
litmus Kubernetes job & the ansible-runner container statuses are checked as necessary & sufficient 
conditions to determine completion of the litmus experiment.

## <font size="6">Dump Experiment Logs</font>

The logs of the Litmus ansible-runner pod (ansible-playbook run output) is dumped on the gitlab job 
runner console to aid a quick view of test behaviour & debug in case of failures.

## <font size="6">Get Litmus Experiment Result</font>

The result CR with the unique name generated is queried to determine the Litmus experiment result. 
The runner script completes execution with zero/non-zero exit code upon pass/failure result respectively, 
thereby setting the gitlab job status. 

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
