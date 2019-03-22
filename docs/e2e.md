---
id: e2e 
title: e2e Pipelines - Leveraging Litmus  
sidebar_label: Litmus Powered E2E
---
------

OpenEBS CI makes use of Litmus to drive its e2e pipelines, right from test bed 
creation (cluster creation playbooks) through the e2e tests (litmus experiments). 
The e2e pipeline involves several stages, with one or more gitlab jobs scheduled to 
run in a given stage. The sequence of stages, grouping of jobs within a given stage, 
intra (same stage) & inter (across stages) job dependencies, high-level test tunables 
are all specified within the .gitlab-ci.yml file in the respective e2e repositories. 

Each gitlab job is associated with a “runner script” or an “e2e test”, which in turn 
invokes/executes a litmus experiment (or litmus ansible playbook, as in the case of 
cluster creation/destroy jobs). 

The various stages in the e2e pipeline are discussed in the sections below.

## <font size="6">Cluster Creation</font>

Brings up the Kubernetes cluster by executing the platform-specific playbooks. 
Several cluster parameters such as the number of nodes, kubernetes versions, compute 
instance types (that control resources), regions, availability zones, CIDR ranges etc., 
can be controlled via runtime arguments (extra_vars). The artifacts generated upon 
this job’s execution (cluster config, i.e., kubeconfig, cluster resource names) 
are passed over to subsequent stages as dependencies. 

The Litmus pre-requisites (RBAC, kubeconfig configmap, Litmus result CRD setup) are 
also installed once the cluster is created, as part of this stage. 

## <font size="6">Cluster Provision</font>

Equips the cluster with additional disk resources, native to the specific platform 
(GPD, EBS, Packet Block Storage, Azure Block Device) that are used by the storage-engines 
as physical storage resources.

## <font size="6">Provider Setup</font>

Deploys the customized/preconditioned OpenEBS Operator manifest (based on the baseline commit) 
on the cluster, thereby setting up the control plane and preparing default storage 
pool resources.The logging infrastructure (fluentd) is also setup on the cluster created. 

## <font size="6">Stateful Application Deployment</font>

The OpenEBS e2e verifies interoperability with several standard stateful applications 
such as Percona-MySQL, MongoDB, Cassandra, PostGreSQL, Jupyter, Prometheus, Jenkins, 
Redis etc.,. These applications are deployed with OpenEBS storageClasses (tuned for each 
app’s storage requirement). Typically, two-versions of most apps are deployed, i.e., with 
Jiva & cStor storage engines. Each application is accompanied by respective load-generator 
jobs that simulate client operations/real-world workloads.

## <font size="6">App Functionality Tests</font>

Each deployed application is subjected to specific behavioural tests, such as replica 
scale, upgrade, storage resize, app replica re-deployment, storage affinity etc., most 
of which are common day1-day2 operations. 

## <font size="6">Storage/Persistent Volume Chaos Tests</font>

The PV components such as controller/replica pods are subjected to chaos (pod crash/kill, 
lossy networks, disconnects) using tools such as chaoskube, pumba, and also kubernetes APIs 
(via kubectl) to verify data availability & application liveness.

## <font size="6">Infrastructure Chaos Tests</font>

The cluster components such as storage pools, nodes and disks are subjected to failures 
using kubernetes APIs (forces evicts, cordon, drain) as well as platform/provider specific 
APIs (gcloud, awscli, packet) to verify data persistence and application liveness.

## <font size="6">Stateful Application Cleanup</font>

The deployed apps are deleted in this stage thereby verifying de-provisioning & cleanup 
functionalities in OpenEBS control plane.

## <font size="6">Cluster Cleanup</font>

The cluster resources (nodes, disks, VPCs) are deleted. With this step, the e2e pipeline 
ends. 


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
