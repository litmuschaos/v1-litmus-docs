---
id: version-0.9.0-disk-fill
title: Disk Fill Experiment Details
sidebar_label: Disk Fill
original_id: disk-fill
---
------

## Experiment Metadata

<table>
<tr>
<th> Type </th>
<th>  Description  </th>
<th> Tested K8s Platform </th>
</tr>
<tr>
<td> Chaos </td>
<td> Fill up Ephemeral Storage of a Pod </td>
<td> GKE </td>
</tr>
</table>

## Prerequisites

- Ensure that Kubernetes Version > 1.13
- Ensure that the Litmus Chaos Operator is running
- Ensure that the `disk-fill` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/generic/experiments/disk-fill)
- Cluster must run docker container runtime
- Appropriate Ephemeral Storage Requests and Limits should be set before running the experiment. 
  An example specification is shown below:
  
```
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: db
    image: mysql
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: "password"
    resources:
      requests:
        ephemeral-storage: "2Gi"
      limits:
        ephemeral-storage: "4Gi"
  - name: wp
    image: wordpress
    resources:
      requests:
        ephemeral-storage: "2Gi"
      limits:
        ephemeral-storage: "4Gi"
  ```

## Entry-Criteria

-   Application pods are healthy before chaos injection.

## Exit-Criteria

-   Application pods are healthy post chaos injection.

## Details

-   Causes Disk Stress by filling up the ephemeral storage of the pod (in the /var/lib/docker/container/{{container_id}}) via a daemonset pod on the same node.
-   Causes the application pod to get evicted if the capacity filled exceeds the pod's ephemeral storage limit.
-   Tests the Ephemeral Storage Limits, to ensure those parameters are sufficient.
-   Tests the application's resiliency to disk stress/replica evictions.

## Integrations

-   Disk Fill can be effected using the chaos library: `litmus`, which makes use of `dd` to create a file of 
    specified capacity on the node.
-   The desired chaoslib can be selected by setting the above options as value for the env variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster. To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine)

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Override the experiment tunables if desired

#### Supported Experiment Tunables

<table>
<tr>
<th> Variables </th>
<th> Description </th>
<th> Type </th>
<th> Notes </th>
</tr>
<tr> 
<td> TOTAL_CHAOS_DURATION </td>
<td> The time duration for chaos insertion (sec) </td>
<td> Mandatory </td>
<td>  </td>
</tr>
<tr> 
<td> CHAOSENGINE </td>
<td> ChaosEngine CR name associated with the experiment instance </td>
<td> Optional </td>
<td>  </td>
</tr>
<tr> 
<td> CHAOS_SERVICE_ACCOUNT </td>
<td> Service account used by the deployment </td>
<td> Optional </td>
<td>  </td>
</tr>
<tr> 
<td> FILL_PERCENTAGE </td>
<td> Percentage to fill the Ephemeral storage limit </td>
<td> Mandatory </td>
<td> Can be set to more that 100 also, to force evict the pod </td>
</tr>
</table>

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  appinfo:
    appns: default
    applabel: 'app=nginx'
    appkind: deployment
  chaosServiceAccount: nginx-sa
  monitoring: false
  jobCleanUpPolicy: delete
  experiments:
    - name: disk-fill
      spec:
        components:
           # specify the fill percentage according to the disk pressure required
          - name: FILL_PERCENTAGE
            value: "80"
```

### Create the ChaosEngine Resource

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos.

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress

- View the status of the pods as they are subjected to disk stress. 

  `watch -n 1 kubectl get pods -n <application-namespace>`
  
- Monitor the capacity filled up on the host filesystem 

  `watch -n 1 du -kh /var/lib/docker/containers/<container-id>`

### Check Chaos Experiment Result

- Check whether the application is resilient to the container kill, once the experiment (job) is completed. The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult nginx-chaos-disk-fill -n <application-namespace>`

## Application Container Kill Demo [TODO]

- A sample recording of this experiment execution is provided here.
