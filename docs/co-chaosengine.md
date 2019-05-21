---
id: co-chaosengine
title: ChaosEngine: Define Chaos Workflow for an Application
sidebar_label: ChaosEngine CR
---
------

The ChaosEngine is the core schema that defines the chaos workflow for a given application. 
Currently, it defines the following:

- Application Data (namespace, labels, kind)
- List of Chaos Experiments to be executed
- Attributes of the experiments, such as, rank/priority
- Execution Schedule for the batch run of the experiments
- The ChaosEngine is the referenced as the owner of the secondary (reconcile) resource with 
  Kubernetes deletePropagation ensuring these also are removed upon deletion of the ChaosEngine CR.

Here is a sample ChaosEngineSpec for reference:

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: engine-nginx
spec:
  appinfo: 
    appns: default
    applabel: "app=nginx"
  experiments:
    - name: pod-delete 
      spec:
        rank: 1
    - name: container-kill
      spec:
        rank: 2 
  schedule:
    interval: "half-hourly"
    excludedTimes: ""
    excludedDays: ""
    concurrencyPolicy: "" 
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
