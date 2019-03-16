---
id: chaos 
title: Chaos Engineering in Litmus
sidebar_label: Chaos Engineering 
---
------

## <font size="6">Litmus: Chaos Framework & More</font>

There are various possible failures that could occur in a Kubernetes cluster running 
stateful workloads. Chaos Engineering is used as an important means to gauge system 
behaviour, blast radius & recovery times. While there are tools which can induce specific 
types of failures on cluster resources, there is a need to tie the act of chaos itself 
with automated orchestration (steady state condition checks) & analysis 
(data availability & integrity, application & storage deployments’ health etc.,). 

Litmus facilitates a Kubernetes-native & persistent storage, i.e., stateful workload-focused 
approach to chaos, with ability to self-determine the success of a controlled chaos 
experiment based on predefined exit criteria. In order to achieve this, Litmus internally 
makes use of multiple opensource chaos tools, combined with the power of kubectl. 

This flowchart,  details the steps in the execution of a chaos test. 

<chaos-flowchart>

Subsequent sections discuss the tools and approaches behind some of the most used Litmus 
chaos experiments. 

## <font size="6">Container Crash</font>

Litmus makes use of a Pumba daemonset to setup the chaos infrastructure as it is necessary 
for the target & pumba containers to co-exist on a node in order for latter to execute the 
Kill operation on the target. Pumba “kills” a container by terminating the main process on 
the target container, with multiple termination signals (SIGKILL, SIGTERM, SIGSTOP) being 
supported. The object to be killed are either the app or PV target/replica/pool containers 
or their sidecars. 

## <font size="6">Forced Pod Reschedule</font>

A delete of a pod, which is managed by higher level kubernetes controllers such as deployments 
and statefulsets, causes it be to be rescheduled on a suitable node (same or different) in 
the cluster. Continuity of end application I/O and time taken for reschedule/bring-up are the 
crucial post checks performed in these tests. 

Litmus uses a chaoskube deployment to run custom pod failure chaos commands by providing 
appropriate label & namespace filters to point to the desired target pods.

## <font size="6">Network Delay & Packet loss</font>

Litmus uses the Pumba daemonset (which internally makes use of tc & netem tools on the target 
containers) & tc directly in some cases, to generate egress delays and percentage packet loss 
on the specified targets for desired duration. Pumba also has the capability to induce network 
delays using random distribution models (uniform, normal, pareto, paretonormal) & loss models 
(bernoulli, markov, gilbert-elliott).

These capabilities are used to simulate flaky iSCSI storage targets, lossy data replication 
channels and test data reconstruction post temporary component loss (such as storage replicas 
and pools).

## <font size="6">Forced Reschedule via Taint-Based Evictions</font>

Under certain specific node conditions/state, Kubernetes automatically taints the node with 
what are commonly referred to as “eviction taints”, which have a “NoExecute” taint effect. 
Which means, the pods scheduled and running on these nodes are immediately evicted and 
rescheduled onto other suitable nodes on the cluster. Amongst these taints, Kubernetes 
automatically adds a default toleration period (tolerationSeconds) of 300s for a couple of 
them - `node.kubernetes.io/unreachable` & `node.kubernetes.io/not-ready` to account for 
transient conditions. For other taints, such as `node.kubernetes.io/memory-pressure`, 
`node.kubernetes.io/disk-pressure` etc.., the pods are evicted immediately (unless specifically 
tolerated in the deployment spec. Visit [kubernetes docs](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#taint-based-evictions) for more details). 

This scenario holds relevance in case of stateful workloads, where an *en-masse* movement of 
application as well as storage resources (which may include control plane components) can 
have potential data availability considerations. In other words, it is an effective HA test, 
not dissimilar to a graceful node loss.

Litmus uses kubectl to simulate such node conditions by manually applying the taint on desired 
nodes (typically, the one which hosts the application and storage target pods) while monitoring 
end-application I/O. 

Litmus simulates graceful node loss via another mechanism: Cordon and Drain (also triggers 
reschedule of all the node’s pods) , which is typically used in cluster maintenance workflows. 

## <font size="6">Simulated Daemon Service Crashes</font>

Loss of node services (kubelet, docker) is one of the common reasons for failed/non-starting 
pods and inaccessible application/storage services on the cluster. Litmus uses a privileged 
daemonset in order to execute systemctl commands on the desired node

In case of managed (GKE) or cloud-hosted (KOPS based AWS, for ex.) kubernetes clusters, often 
times these crucial daemon services have corresponding health check/monitoring services which 
detect anomalies and attempt restart to restore node health. The litmus chaos utils disable 
these monitoring services temporarily for the duration of the chaos to ensure consistent chaos, 
instead of flaky state changes (this, it can be argued is a case for a separate test!). After 
the chaos duration is elapsed, all affected services are restored, with post checks confirming 
cluster health. 

These scenarios cause the ungraceful/forced reschedule workflows in Kubernetes to kick-in. 
They have significant implications on stateful workloads, with disk/volume unmount-detach and 
reattach-remount times in focus. As with the eviction by taint & drain scenarios, Litmus monitors 
end-application I/O & data integrity as part of the chaos experiment.

## <font size="6">Resource Exhaustion on Kubernetes Nodes</font>

While node conditions are simulated via eviction taints, it is also necessary to actually induce 
resource exhaustion such as CPU burn & Memory Hog to gauge real-time behaviour. Litmus uses simple 
docker containers that run (a) program causing unterminated string growth in a file leading to 
full memory allocation & (b) forkbomb to cause process multiplication & eventual CPU burn.

A node-action daemonset used to execute docker commands that in turn run the above containers 
with Litmus monitoring node status & end-application I/O.

## <font size="6">Kubernetes Node (instance) Failures</font>

Litmus supports instance termination on AWS (KOPS based Kubernetes clusters) & Packet 
(Bare-metal cluster) with work in progress to extend the similar capabilities to other platforms. 
Different impact is noticed when node failures are performed across platforms — for ex. in case of 
AWS, the another instance with the same root disk is automatically brought up as the nodes are by 
default a part of the KOPS auto-scaling instance group, while with Packet, the node remains shutdown 
and can be subsequently powered-on.

For AWS, Litmus uses chaostoolkit templates executed by a dedicated job to cause termination 
of a specific instance, or a random instance within an Availability zone.

The AWS access keys & instance details are passed as test inputs from the Litmus test job. 

For Packet, Litmus uses the Ansible Packet module to power-off & power-on the node instance, with 
the packet API keys, project id, node name & chaos duration passed as test inputs. 

## <font size="6">Disk Failures</font>

Litmus currently supports disk failure chaos utils for Kubernetes clusters built on AWS cloud. 
Work is in progress to extend this to other platforms. The AWSCLI & Boto Python SDK are used to 
force detach & reattach the EBS volumes used as the disk sources for the storage pools. As with 
other chaos tests, Litmus monitors the end-application I/O and data integrity over the course 
of the experiment.


<!-- Hotjar Tracking Code for https://docs.openebs.io -->

<script>
   (function(h,o,t,j,a,r){
       h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
       h._hjSettings={hjid:785693,hjsv:6};
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
