---
id: version-0.5.0-cb-experiment
title: Understanding the test
sidebar_label: Know Your Experiment
original_id: cb-experiment
---
------

The first step in the creation of a new litmusbook is to clearly 
define the experiment, or in other words, identify the test intent, 
flow & its execution environment. This can be translated as 
understanding the following requirements: 

## <font size="6">Entry criteria of the test</font>

For example, it may be necessary for the application under test (AUT) 
to be in “Running” state prior to executing the experiment steps and 
the storage health checks to be successful. In case of chaos experiments, 
this corresponds to identification of steady state & means to ascertain 
it. 

![entry-criteria](/docs/assets/cookbook/entry-criteria.png)

## <font size="6">Experiment/Test business logic</font>

This consists of the main test procedure that corresponds to the user 
action- typically provisioning/other administrative/functional workflows 
OR failure injection/chaos of specific cluster components.

![business-logic](/docs/assets/cookbook/business-logic.png)

## <font size="6">Exit Criteria of the test</font>

Evaluation against success conditions based on the hypothesis around 
impact on service/system.Most of the times, this is successful 
(re)configuration in case of functional workflows or uninterrupted 
service availability in case of chaos. Data integrity verification 
could be an important post-test check.

![exit-criteria](/docs/assets/cookbook/exit-criteria.png)

## <font size="6">Tooling</font>

A majority of the Litmus tests are written with “kubectl” as the main tool 
through which the experiment’s steps are executed. In some cases, the test 
business logic might need to make use of additional tools, for example 
injecting packet loss in the pod network necessitates use of pumba or at 
least, tc & netem. 

![tooling](/docs/assets/cookbook/tooling.png)

## <font size="6">Target environments</font>

Most of the Litmus experiments are designed to be purely platform agnostic. 
They can run on any Kubernetes cluster regardless of the underlying 
infrastructure, i.e.., cloud-providers or on-premise. However, there are 
some experiments which use provider-specific APIs (gcloud, awscli) to execute 
some steps. For example, disk failure tests, where the nature of underlying 
disk/block volume depends on the platform. 

In such cases, different “utils” to achieve the requirement are created for 
different platforms, with these being selectively called based on user inputs 
for platform type. 

![packet](/docs/assets/cookbook/packet.png)

![aws](/docs/assets/cookbook/aws.png)


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
