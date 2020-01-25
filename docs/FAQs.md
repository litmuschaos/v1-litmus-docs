# Litmus FAQs
---
### Q. Why Should I use Litmus?

<b>Ans:</b> Litmus is a toolset to do cloud-native chaos engineering. Litmus provides tools to orchestrate chaos on Kubernetes to help SREs find weaknesses in their deployments. SREs use Litmus to run chaos experiments initially in the staging environment and eventually in production to find bugs, vulnerabilities. Fixing the weaknesses leads to increased resilience of the system.

### Q. What are the Pre-requisites to get started with Litmus?

<b>Ans:</b> For getting started with Litmus the only Pre-requisites is to have Kubernetes 1.11 or later version installed in your system.

### Q. Do I need to change the service account permission before running a Chaos Experiment?

<b>Ans:</b> Litmus provides all the permissions required for running a particular chaos experiment. These permissions are different for different experiments but you don't need to change it at any point of time. These permissions are present in rbac manifest which you install at the time of installing Litmus. You can get the manifest for all experiments from <a href="https://docs.Litmuschaos.io/docs/chaoshub/">here</a>.

### Q. I don't know how to get started with Litmus.

<b>Ans:</b> It is versy easy to get started with Litmus you only need to follow the steps mention in the <a href="https://docs.Litmuschaos.io/docs/getstarted/">Getstarted Docs</a> and if you still face problem you can visit our video demo of experiments from <a href="https://www.youtube.com/channel/UCa57PMqmz_j0wnteRa9nCaw">YouTube</a> 

### Q. How to contribute in Litmus or I found some bug on how to report it?

<b>Ans:</b> We welcome you for your contribution in Litmus. If you are with a new feature or a bug report feel free to raise the issue for/against it some of our team members will surely address it. For raising issue first identify the issue is related to which repository of Litmus like if you want to contribute to Litmus docs go to Litmus-docs repository and raise the issue with the details of what type of feature you are proposing for or if you are with some bug report describe the type of bug.

### Q. How to get the logs of the runner and chaos experiment?

<b>Ans:</b> Forgetting the logs of runner or chaos experiment use the following command.
`kubectl logs -f <name of pod> -n <namespace>`
By running this command you will be able to get the logs of the engine or experiment.

### Q. What is Chaos Engine in Litmus and how to install it manually?

<b>Ans:</b> ChaosEngine connects application to the Chaos Experiment. To install it manually Copy the YAML snippet from the experiments in <a href="https://docs.Litmuschaos.io/docs/chaoshub/">ChaosHub </a> into a file (say) chaosengine.yaml and update the values of applabel , appns, appkind and experiments as per your choice. Toggle monitoring between true/false, to allow the chaos-exporter to fetch experiment related metrics. Change the chaosServiceAccount to the name of Service Account created in the above step, if applicable.

### Q. How to install Chaos Experiments manually?

<b>Ans:</b> Chaos experiments contain the actual chaos details. These experiments are installed on your cluster as Kubernetes CRs (Custom Resources). The Chaos Experiments are grouped as Chaos Charts and are published on <a href="https://hub.Litmuschaos.io/">Chaos Hub</a>.
Following are the steps to install the Chaos Experiment:
- Select the experiment from the <a href="https://hub.Litmuschaos.io/">Chaos Hub</a> which you want to install.
- Click on the Install Experiment button from the chart.
- Copy the command and run it the experiment will be installed successfully.

### Q. How to delete Chaos Engine and Chaos Experiment manually?

<b>Ans:</b> Follow these commands to delete the Chaos Engine and Chaos Experiment manually:
- To delete the Chaos Engine manually run the following command.
 `kubectl delete chaosengine <chaos-engine-name>-runner`.
 Where chaos-engine-name is the name of Chaos Engine or if you want to delete all chaosengine present use the following command 
 `kubectl delete chaosengine <chaos-engine-name>-runner --all`

- To delete the Chaos Experiment manually run the following command.
 `kubeclt delete chaosexperiment <experiment-name>`.
 If you want to delete all chaos experiments then use 
 `kubectl delete chaosexperiment <experiment-name> --all`

#### Q. How will I know that the chaos has injected successfully?

<b>Ans:</b> To check whether the chaos has injected successfully or nor check verdict in the chaosresult of the experiment. Use the following command to get the chaosresult.
`kubectl describe chaosresult <chaos-engine-name>-<chaos-experiment-name>`. Check the `spec.verdict` in the chaos result. The spec.verdict is set to `Running` when the experiment is in progress, eventually changing to either `pass` or `fail`.

### Q. I'm still not able to run the Chaos Experiment what should I do?

<b>Ans:</b> Don't worry we have recently added the video demo of the generic experiments you can take a reference from there if you are still facing the problem. Visit our YouTube channel <a href="https://www.youtube.com/channel/UCa57PMqmz_j0wnteRa9nCaw">Litmus Chaos</a>now.

### Q. Is there any public channel where I can join?

<b>Ans:</b> You Can join us at <a href="https://app.slack.com/client/T09NY5SBT/CNXNB0ZTN">Litmus Slack Channel</a>.

### Q. Does Litmus organize any Community Sync Up?

<b>Ans:</b> The Litmus Community has now decided to sync up once every month, on the third Wednesday at 8.30 AM PST/10.00 PM IST to review the release gone by, discuss roadmap items, present/demonstrate features the contributors have been working on… and just to meet and greet! The notes from previous meetings are now maintained <a href="https://hackmd.io/a4Zu_sH4TZGeih-xCimi3Q">here</a>. Feel free to add your topic of interest in the agenda to have it discussed.

