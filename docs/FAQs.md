# Litmus FAQs
---
### Q.1 Why Should I use Litmus?

<b>Ans:</b> Litmus is a toolset to do cloud-native chaos engineering. Litmus provides tools to orchestrate chaos on Kubernetes to help SREs find weaknesses in their deployments. SREs use Litmus to run chaos experiments initially in the staging environment and eventually in production to find bugs, vulnerabilities. Fixing the weaknesses leads to increased resilience of the system.

### Q.2 What are the Prerequisites to get started with Litmus?

<b>Ans:</b> For getting started with Litmus the only Prerequisites is to have Kubernetes 1.11 or later version installed in your system. 

### Q.3 Do I need to change the service account permission before running a Chaos Experiment?

<b>Ans:</b> Litmus provides all the permissions required for running a particular chaos experiment. These permissions are different for different experiments but you don't need to change it at any point of time. These permissions are present in the rbac manifest which you install at the time of installing Litmus. You can get the manifest for all experiments from <a href="https://docs.Litmuschaos.io/docs/chaoshub/">here</a>.

### Q.4 I don't know how to get started with Litmus.

<b>Ans:</b> It is very easy to get started with Litmus you only need to follow the steps mentioned in the <a href="https://docs.Litmuschaos.io/docs/getstarted/">Getstarted Docs</a> and if you still face problems you can visit our video demo of experiments from YouTube Channel <a href="https://www.youtube.com/channel/UCa57PMqmz_j0wnteRa9nCaw">Litmus Chaos</a>.

### Q.5 How to contribute in Litmus or I found some bug on how to report it?

<b>Ans:</b> We welcome you for your contribution in Litmus. If you are with a new feature or a bug report feel free to raise the issue for/against it some of our team members will surely address it. For raising issue first identify the issue is related to which repository of Litmus like if you want to contribute to Litmus docs go to Litmus-docs repository and raise the issue with the details of what type of feature you are proposing for or if you are with some bug report describe the type of bug.

### Q.6 How to get the logs of the runner and chaos experiment?

<b>Ans:</b> For getting the logs of runner or chaos experiment use the following command.
`kubectl logs -f <name-of-pod> -n <namespace>`
by running this command you will be able to get the logs of the engine or experiment.

### Q.7 What is Chaos Engine in Litmus and how to install it manually?

<b>Ans:</b> Chaos Engine connects application to the Chaos Experiment. To install it manually Copy the YAML snippet from the experiments in <a href="https://docs.Litmuschaos.io/docs/chaoshub/">ChaosHub </a> into a file (say) chaosengine.yaml and update the values of applabel , appns, appkind and experiments as per your choice. Toggle monitoring between true/false, to allow the chaos-exporter to fetch experiment related metrics. Change the chaosServiceAccount to the name of Service Account.

### Q.8 Even after creating the chaos experiment the experiment pod is not getting created.

<b>Ans:</b> There can be different reasons for this like:

- <b><u>Make sure you the chaos operator is running.</b></u> If chaos operator is not running then you need to install it first as it is custom-controllers with direct access to Kubernetes API that can manage the lifecycle of certain resources or applications, while always trying to ensure the resource is in the "desired state. You can create the operator from <a href="https://github.com/litmuschaos/chaos-operator/blob/master/deploy/operator.yaml">here</a>.

- <b></u>Make sure that you have annotated your application</b></u> before creating the Chaos Experiment.Your application has to be annotated with litmuschaos.io/chaos="true". As a security measure, Chaos Operator checks for this annotation on the application before invoking chaos experiment(s) on the application.
<b>NOTE:</b> The annotation has to be done in the same namespace where the application is running.


### Q.9 How to install Chaos Experiments manually?

<b>Ans:</b> Chaos experiments contain the actual chaos details. These experiments are installed on your cluster as Kubernetes CRs (Custom Resources). The Chaos Experiments are grouped as Chaos Charts and are published on <a href="https://hub.Litmuschaos.io/">Chaos Hub</a>.
Following are the steps to install the Chaos Experiment:
- Select the experiment from the <a href="https://hub.Litmuschaos.io/">Chaos Hub</a> which you want to install.
- Click on the Install Experiment button from the chart.
- Copy the command and run it the experiment will be installed successfully.

### Q.10 How to delete Chaos Engine and Chaos Experiment manually?

<b>Ans:</b> Follow these commands to delete the Chaos Engine and Chaos Experiment manually:
- To delete the Chaos Engine manually run the following command.
 `kubectl delete chaosengine <chaos-engine-name>-runner`.
 Where chaos-engine-name is the name of Chaos Engine or if you want to delete all chaosengine present use the following command 
 `kubectl delete chaosengine <chaos-engine-name>-runner --all`

- To delete the Chaos Experiment manually run the following command.
 `kubeclt delete chaosexperiment <experiment-name>`.
 If you want to delete all chaos experiments then use 
 `kubectl delete chaosexperiment <experiment-name> --all`

### Q.11 How to monitor the CPU or Memory uses for Infra Chaso Experiments? 

<b>Ans:</b> For monitoring the CPU or memory uses, you can use the `top` command.
    `kubectl top pods` or `kubectl top nodes`.

### Q.12 How will I know that the chaos has been injected successfully?

<b>Ans:</b> To check whether the chaos has been injected successfully or not check verdict in the chaosresult of the experiment. Use the following command to get the chaosresult.
`kubectl describe chaosresult <chaos-engine-name>-<chaos-experiment-name>`. Check the `spec.verdict` in the chaos result. The spec.verdict is set to `Running` when the experiment is in progress, eventually changing to either `pass` or `fail`.

### Q.13 I'm still not able to run the Chaos Experiment. What should I do?

<b>Ans:</b> Don't worry we have recently added the video demo of the generic experiments you can take a reference from there if you are still facing the problem. Visit our YouTube channel <a href="https://www.youtube.com/channel/UCa57PMqmz_j0wnteRa9nCaw">Litmus Chaos</a> now.

### Q.14 Is there any public channel where I can join?

<b>Ans:</b> You Can join us at <a href="https://app.slack.com/client/T09NY5SBT/CNXNB0ZTN">Litmus Slack Channel</a>.

### Q.15 Does Litmus organize any Community Sync Up?

<b>Ans:</b> The Litmus Community has now decided to sync up once every month, on the third Wednesday at 8.30 AM PST/10.00 PM IST to review the release gone by, discuss roadmap items, present/demonstrate features the contributors have been working on… and just to meet and greet! The notes from previous meetings are now maintained <a href="https://hackmd.io/a4Zu_sH4TZGeih-xCimi3Q">here</a>. Feel free to add your topic of interest in the agenda to have it discussed.

