---
id: running 
title: Running a Litmus Experiment  
sidebar_label: Running a Litmus Experiment
---
------

A general set of instructions on the procedure to run a litmus test has been provided below:  

- Navigate to the appropriate test folder containing the litmusbook `(run_litmus_test.yml)`

- Update the placeholder values of the application, storage provider, infrastructure & use 
  case specific ENV to the ansible-runner container 

  - **Note**: Each litmusbook has a common set of test inputs that it shares with other 
    tests (mostly, app info) and another set of inputs specific to itself. The respective tests 
    contain details/instructions on their significance & example values that can be referred 
    before its execution

- [Optional] Update the log-location on the node (on which the litmus pod runs) in the logger 
  spec (MY_POD_HOSTPATH). If the cluster is already configured with standard logging frameworks 
  such as EFK, StackDriver, then this step is not necessary

- Execute the litmus test job using the kubectl create command. 

  ```
  kubectl create -f run_litmus_test.yml
  ```

- The litmus test job typically launch multiple other deployments as part of the test, with 
  the litmus test pod eventually entering ‘Completed’ state.


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
