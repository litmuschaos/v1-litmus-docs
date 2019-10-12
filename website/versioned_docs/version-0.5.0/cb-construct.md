---
id: version-0.5.0-cb-construct
title: Building the Litmus test artifact
sidebar_label: Constructing Litmusbooks
original_id: cb-construct
---
------
Once the test blocks are mapped with the respective LitmusLib 
utils, they need to be strung together with relevant test inputs 
in the test playbook, and run in a kubernetes job. This process 
can be carried out in the following phases: 

## <font size="6">User & Derived Inputs</font>

Each experiment, at a high-level will have its own control 
(for ex: chaos params — considering that different applications, 
storage engines, PV component versions, and deployment models are 
evaluated against a particular chaos sequence) & independent 
variables (PV, application and K8s deployment params) that are 
provided by the user upfront. These user inputs are used to derive 
certain parameters, which are then passed to other utils as 
arguments. For example, application label & namespace info can be 
used to derive the application pod name. The test variables are 
maintained in a separate yaml file (test_vars.yml) which is 
included into the playbooks. 

![user-input](/docs/assets/cookbook/user-input.png)

![derived-input-1](/docs/assets/cookbook/derived-input-1.png)

![derived-input-2](/docs/assets/cookbook/derived-input-2.png)

## <font size="6">Building the Playbook</font>

The execution of the experiment / test can be neatly divided into 
different phases. The standard segregation is like this:

- Pre-Requisites: Certain pre-test routines to determine the application 
and storage properties, such as the provisioner, storage class etc., 

- Test Main: Actual test steps which include steady-state checks, 
functional/chaos steps, post-test checks followed by updates to the 
result custom resource.

- Cleanup: Involves removal of any intermediate (created during test) 
resources on the cluster 

![playbook-components](/docs/assets/cookbook/playbook-components.png)

It is recommended to maintain the logic for these phases in separate 
files: one main playbook (test.yml) with one or more auxiliary task 
file YAMLs (test_prerequisites.yml & test_cleanup.yml) to ensure easier 
and uncluttered updates on each. However, this is not mandatory, and it 
is left to the discretion of the user to structure the artifacts as 
desired. 

## <font size="6">Litmus Job Specification</font>

The test playbook which has been constructed after putting in place 
the desired tasks & importing the right utils, is executed by a 
Kubernetes job. This job runs the “ansible-runner” docker container 
which has ansible installed & also the test playbooks packaged into it. 
Some of the considerations while framing the job specification is 
listed below: 

- The test inputs which are user-defined (application, storage, 
chaos info etc..,) is recommended to be passed as pod/container env 
variables. These can be referred by the ansible lookup function.

- In some cases, it is desired that the litmus pod is scheduled on a 
specific node in the kubernetes cluster as part of the test requirement. 
For example, litmus experiments that contain steps to fail a node 
meeting specific requirements (such as the one that hosts the 
application pod) require that the litmus pod itself is not scheduled 
on that node. 

There are several ways to implement this: nodeSelectors, affinity/anti-pod 
affinity & taint tolerations. This needs to be burnt into the job 
specification.

- It is recommended to define resource limits to the ansible-runner 
(and other application / facilitator pods) used as part of the litmus 
experiment in order to use resources efficiently. The values to be used 
can be frozen after benchmarking the test over the course of a few runs. 

![litmusjob-scheduling](/docs/assets/cookbook/litmusjob-scheduling.png)

- The litmus experiment can be configured with maximum run duration by 
specifying the spec.activeDeadlineSeconds. This is especially helpful in 
cases where unmonitored jobs are stuck (on a task) during execution.

![litmusjob-duration](/docs/assets/cookbook/litmusjob-duration.png)

- The stern-based logger sidecar is an optional configuration that can 
be used in the absence of any standard logging infrastructure on the test 
clusters. 

![logger-spec](/docs/assets/cookbook/logger-spec.png)

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
