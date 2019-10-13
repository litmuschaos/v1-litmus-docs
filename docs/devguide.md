---
id: devguide 
title: Developer Guide for Chaos Charts
sidebar_label: Developer Guide 
---
------

This page serves as a guide to develop either a new Chaos Chart or a new experiment in a Chaos Chart which are published at <a href="https://hub.litmuschaos.io" target="_blank">ChaosHub</a>.

Below are some key points to remember before understanding how to write a new chart or an experiment.

> Chaos Charts repository : https://github.com/litmuschaos/chaos-charts
>
> Litmusbooks repository : https://github.com/litmuschaos/litmus/tree/master/experiments
>
> Website rendering code repository: https://github.com/litmuschaos/charthub.litmuschaos.io



Chaos Libraries are written in Ansible programming language. To write new a Chaos Experiment, you need to know Ansible.

<hr>

## Glossary

### Chaos Chart

A group of Choas Experiments put together in a YAML file. This group or chart has metadata such as `ChartVersion`, `Provided By`. 

### Chaos Experiment

ChaosExperiment is a CRD that specifies the nature of a Chaos Experiment. The YAML file that constitutes a Chaos Experiment CR is stored under a Chaos Chart of ChaosHub. An important parameter of a ChaosExperiment CR is the `LitmusBook`.

### Litmus Book

Litmus book is an `ansible` playbook that encompasses the logic of pre-checks, injecting actual chaos, post-checks and updating the result. 

### Chaos functions

The `ansible` programs inside Litmus books can make use of readily avaialble chaos functions. The chaos functions are available as `ansible` functions which are wrapped in one of the chaos libraries. See [plugins](/docs/next/plugins.html) for more details.

<hr>

## Developing a Chaos Experiment

1. [Write a new Chaos Chart](#write-a-new-chaos-chart)
2. [Write a new ChaosExperiment CR YAML](#write-a-new-chaosexperiment-cr-yaml)
3. [Write a new Litmus Book](#write-a-new-litmus-book)
4. Test the Chaos Experiment
5. [Update the documentation](#update-the-documentation) 

See an [example](#example) of developing chaos chart for `newApp` with a new chaos experiment called `replica-kill`

### Write a new Chaos Chart

1. Clone `chaos-charts` repository

   ```
   https://github.com/litmuschaos/chaos-charts.git
   ```

   

2. Untar new-chart.tar.gz  available in the root folder of the repository.

3. If you are naming your chart as `newApp`, replace all instances of `exampleChart` with `newApp`

4. If you are naming your experiment as `replica-kill`, replace all instances of `exampleExp` with `replica-kill`

Now, your `newApp` chaos chart is ready. Next step is to update and verify CR YAML for `replica-kill`.  

### Write a new ChaosExperiment CR YAML

If you have extracted or untarred `new-chart.tar.gz`, you will have the required templace YAMLs for Chaos Experiment as well. Follow the below steps to prepare your chaos experiment `newExp` 

1. Update the reference to Limus

### Write a new Litmus Book



### Update the documentation

Documentation for your new chart and experiment have to be updated at <a href="/docs/next/chaoshub.html" target="_blank"> chaoshub</a>

## Example

The below video shows the example creation of `newChart` and `newExp` for an application called `busybox`. 

<ascii cinema video of the above example>

<br>

<hr>

<br>

<br>

<!-- Global site tag (gtag.js) - Google Analytics -->

<script async src="https://www.googletagmanager.com/gtag/js?id=UA-92076314-12"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-92076314-12');
</script>
