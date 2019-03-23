---
id: components
title: Litmus Architecture
sidebar_label: Litmus Architecture
---
------



<br><img src="/docs/assets/archi.svg" alt="Litmus Overview" width="800"/>

<br>

<br>

The main components or building blocks of the Litmus framework are described in 
the following sections, in the order of execution: 

[Litmus experiment](/docs/next/components.html#font-size-6-litmus-experiment-font)

[Ansible-Runner](/docs/next/components.html#font-size-6-ansible-runner-font)

[Test Playbook](/docs/next/components.html#font-size-6-test-playbook-font)

[Test Libraries](/docs/next/components.html#font-size-6-test-libraries-font)

[Test Facilitator Containers](/docs/next/components.html#font-size-6-test-facilitator-containers-font)

[Result Custom Resource](/docs/next/components.html#font-size-6-result-custom-resource-font)

<br>

<br>



## <font size="6">Litmus Experiment</font>

This is the end user deployable/executable unit that corresponds to an independent “test”
(such as deploying a stateful application, running a chaos scenario), which may be part of a
larger scenario OR a complete e2e test case in itself. It is essentially a Kubernetes Job
YAML file with mandatory pod spec for the ansible-runner and optional pod spec for the logger.

Chaos experiment is the artifact into which the following type of test inputs can be fed
and  controlled as ENV variables:

- Application info (application namespace, labels, PVC names, access keys, liveness endpoints)
- Storage info (storage class, snapshot details)
- Test-specific info (chaos type, duration, data checks)

## <font size="6">Ansible Runner</font>

The Litmus job controls the Ansible-Runner, which is the “Test Container” that runs the 
test business logic. The runner image is built with ansible libraries, test code & other 
necessary dependencies. It executes the test playbook as the entrypoint function. 

## <font size="6">Test Playbook</font>

The test playbook consists of the actual test business logic. The inputs specified as 
litmusbook ENV variables are processed and used as part of the execution process. Typically, 
the playbook is built up of one or more auxiliary ansible task files which contains the 
code corresponding to the standard phases of the test, i.e., pre-requisites, main test steps, 
cleanup etc., 

## <font size="6">Test Libraries</font>

The test playbooks invoke different utils (ansible task files) that perform specificialized 
functions such as inducing different kinds of chaos on the cluster using various tools 
(aggregated into chaoslib), or perform some provisioning action such as replica scale, volume 
resize, upgrade (funclib) or other frequently used tasks, such as deployment status checks, 
for example.(common/utils). These library utils have clearly defined interfaces and are kept 
as modular as possible. 

## <font size="6">Test Facilitator Containers</font>

The Litmus framework provides application load generators as well as liveness monitors 
(app client simulation) in order to better test stateful applications during the course of 
chaos & other real-world e2e scenarios. Also available are other helper tools such as log 
collectors & compliance checkers. These tools are packaged as “Test Facilitator” container 
images, with dedicated deployment artifacts (jobs/pods), that are launched as part of 
litmusbook execution (by the chaoslib/funclib utils described above). In some cases, they 
are also used as sidecars to the ansible-runner.

## <font size="6">Result Custom Resource</font>

The test results in Litmus are stored in a Kubernetes Custom Resource, along with test metadata. 
This CR undergoes static updates at different points in the test to reflect current test status 
and the verdict (result) at the end of execution. The result CRs provide an  effective means 
for external execution monitoring, as is the case in CI pipelines.


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
