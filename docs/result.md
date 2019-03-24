---
id: result 
title: Viewing Result of a Litmus Experiment
sidebar_label: Result Mechanism
---
------

Litmus test results are captured in the Litmus custom resource along with test 
metadata. The custom resource name is the same as the litmusbook job name 
(in some cases followed by a user-specific tag if the RUN_ID ENV is specified in 
the container spec of ansible-runner). Upon job completion, the results can be 
viewed using kubectl commands

```Kubectl get litmusresult <custom resource name> -o custom-columns=:spec.testStatus.result```

An example spec (pruned) of a litmus result custom resource:

```
apiVersion: litmus.io/v1alpha1
kind: LitmusResult
metadata:
  name: storage-volume-replica-failure
  namespace: litmus
spec:
  testMetadata:
    app: percona
    chaostype: openebs/jiva_replica_pod_failure
  testStatus:
    phase: completed
    result: Pass
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
