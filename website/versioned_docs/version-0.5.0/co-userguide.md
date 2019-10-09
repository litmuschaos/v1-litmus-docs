---
id: version-0.5.0-co-userguide
title: Inject Chaos using the Chaos Operator
sidebar_label: User Guide
original_id: co-userguide
---
------

- Install Litmus infrastructure (RBAC, CRD) components

```
helm repo add https://litmuschaos.github.io/chaos-charts
helm repo update
helm install litmuschaos/litmusInfra --namespace=litmus
```

- Deploy the Chaos Operator

```
helm install litmuschaos/chaosOperator
```

- Download the desired Chaos Experiment bundles, say, general Kubernetes chaos

```
helm install litmuschaos/k8sChaos
```

- Annotate your application to enable chaos. For ex:

```
kubectl annotate deploy nginx-deployment `litmuschaos.io/chaos:"true"`
```

- Create a ChaosEngine CR with application information & chaos experiment list with 
their respective attributes

```
# engine-nginx.yaml is a chaosengine manifest file
kubectl apply -f engine-nginx.yaml
```

- Refer the ChaosEngine Status (or alternately, the corresponding ChaosResult resource) 
to know the status of each experiment. The spec.verdict is set to Running when the experiment 
is in progress, eventually changing to pass or fail.

```
kubectl describe chaosresult pod-delete
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
