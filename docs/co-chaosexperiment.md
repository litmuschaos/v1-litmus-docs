---
id: co-chaosexperiment
title: ChaosExperiments: Define Chaos Experiment Details
sidebar_label: ChaosExperiment CR
---
------

ChaosExperiment CRs describe low-level information about a given chaos experiment. 
ChaosExperiments of similar nature are bundled together as chaos charts, giving 
developers the option to install & a execute specific set of experiments. 

The charts are currently categorized as:

- (a) Kubernetes general Chaos (Ex: random pod failures, container crashes, container egress delays, node loss)
- (b) Storage provider Chaos (Ex: OpenEBS target failures, OpenEBS pool failures, OpenEBS control plane failures)
- (c) Application specific Chaos (Ex: NuoDB storage manager failures, NuoDB transaction engine failures) 

While (b) & (c)  make use of similar techniques/tools as (a) to implement the 
failures, they have additional entry & exit criteria depending upon the usecases 
involved.

The spec.definition.fields and their corresponding values are used to construct 
the eventual execution artifact that runs the chaos experiment (typically, the 
litmusbook, which is a K8s job resource).

```yaml
apiVersion: litmuschaos.io/v1alpha1
description:
  message: |
    Deletes a pod belonging to a deployment/statefulset/daemonset
kind: ChaosExperiment
metadata:
  labels:
    helm.sh/chart: k8sChaos-0.1.0
    litmuschaos.io/instance: dealing-butterfly
    litmuschaos.io/name: k8sChaos
  name: pod-delete
spec:
  definition:
    image: openebs/ansible-runner:ci
    litmusbook: /experiments/chaos/kubernetes/pod_delete/run_litmus_test.yml
    labels:
      name: pod-delete
    args:
    - -c
    - ansible-playbook ./experiments/chaos/kubernetes/pod_delete/test.yml -i /etc/ansible/hosts
      -vv; exit 0
    command:
    - /bin/bash
    env:
    - name: ANSIBLE_STDOUT_CALLBACK
      value: null
    - name: TOTAL_CHAOS_DURATION
      value: 15
    - name: CHAOS_INTERVAL
      value: 5
    - name: LIB
      value: ""
```


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
