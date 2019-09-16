---
id: co-userguide
title: Inject Chaos using the Chaos Operator 
sidebar_label: User Guide
---
------

- Install Litmus infrastructure (RBAC, CRD) & chaos-operator components

```
helm repo add litmuschaos https://litmuschaos.github.io/chaos-charts
helm repo update
helm install litmuschaos/litmus --namespace=litmus
```

- Download the desired Chaos Experiment bundles, say, for base Kubernetes chaos (pod-delete, container-kills)
into your application's namespace

```
helm install litmuschaos/kubernetes
```

- Annotate your application to enable chaos. For ex:

```
kubectl annotate deploy nginx-deployment litmuschaos.io/chaos="true"`
```

- Create a chaos service account in the application's namespace. This is the service account that will be used by the chaos executor to perform chaos. Setup necessary permissions, while ensuring ability to list and update litmuschaos.io resources chaosengine, chaosexperiment & chaosresults 

- Create a ChaosEngine CR with application information & chaos experiment list with 
their respective attributes

```
# engine-nginx.yaml is a chaosengine manifest file
kubectl apply -f engine-nginx.yaml
```

- Refer the chaosresult status to know the status of each experiment. The spec.verdict is set to Running when the experiment 
is in progress, eventually changing to pass or fail.

```
kubectl describe chaosresult <chaosengine-name>-<experiment-name>
```
NOTE: For a more detailed guide, with examples/output snippets, please refer: https://github.com/litmuschaos/community/tree/master/feature-demos/chaos-operator-workflow


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
