---
id: version-0.8.0-kafka-broker-pod-failure
title: Kafka Broker Pod Failure Experiment Details
sidebar_label: Kafka Broker Pod Failure
original_id: kafka-broker-pod-failure
---

## Experiment Metadata

| Type  | Description                    | Kafka Distribution   | Tested K8s Platform
| ----- | -------------------------------|----------------------|---------------------
| Kafka | Fail kafka leader-broker pods  | Confluent, Kudo-Kafka| AWS Konvoy, GKE

## Prerequisites

- Ensure that the Litmus Chaos Operator is running
- Ensure that the `kafka-broker-pod-failure` experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/kafka/experiments/kafka-broker-pod-failure) 
- Ensure that Kafka & Zookeeper are deployed as Statefulsets
- If Confluent/Kudo Operators have been used to deploy Kafka, note the instance name, which will be 
  used as the value of `KAFKA_INSTANCE_NAME` experiment environment variable 

  - In case of Confluent, specified by the `--name` flag
  - In case of Kudo, specified by the `--instance` flag
 
  Zookeeper uses this to construct a path in which kafka cluster data is stored. 

- Ensure that the kafka-broker-disk failure experiment resource is available in the cluster. If not, install from [here](https://hub.litmuschaos.io/charts/kafka/experiments/kafka-broker-pod-failure) 


## Entry Criteria

- Kafka Cluster (comprising the Kafka-broker & Zookeeper Statefulsets) is healthy

## Exit Criteria

- Kafka Cluster (comprising the Kafka-broker & Zookeeper Statefulsets) is healthy
- Kafka Message stream (if enabled) is unbroken

## Details

- Causes (forced/graceful) pod failure of specific/random Kafka broker pods
- Tests deployment sanity (replica availability & uninterrupted service) and recovery workflows of the Kafka cluster
- Tests unbroken message stream when `KAFKA_LIVENESS_STREAM` experiment environment variable is set to `enabled`

## Integrations

- Pod failures can be effected using one of these chaos libraries: `litmus`, `powerfulseal`
- The desired chaos library can be selected by setting one of the above options as value for the environment variable `LIB`

## Steps to Execute the Chaos Experiment

- This Chaos Experiment can be triggered by creating a ChaosEngine resource on the cluster.
  To understand the values to provide in a ChaosEngine specification, refer [Getting Started](getstarted.md/#prepare-chaosengine) 

- Follow the steps in the sections below to prepare the ChaosEngine & execute the experiment.

### Prepare ChaosEngine

- Provide the application info in `spec.appinfo`
- Provide the experiment tunables. While many tunables have default values specified in the ChaosExperiment CR, some need to be 
  explicitly supplied.

#### Supported Experiment Tunables

| Variables             | Description                                                  |Type       | Notes                                                   |
| ----------------------| ------------------------------------------------------------ |-----------|---------------------------------------------------------|
| KAFKA_NAMESPACE       | Namespace of Kafka Brokers                                   | Mandatory | May be same as value for `spec.appinfo.appns`           |
| KAFKA_LABEL           | Unique label of Kafka Brokers                                | Mandatory | May be same as value for `spec.appinfo.applabel`        |
| KAFKA_SERVICE         | Headless service of the Kafka Statefulset                    | Mandatory |                                                         |
| KAFKA_PORT            | Port of the Kafka ClusterIP service                          | Mandatory |                                                         |
| ZOOKEEPER_NAMESPACE   | Namespace of Zookeeper Cluster                               | Mandatory | May be same as value for KAFKA_NAMESPACE or other       |
| ZOOKEEPER_LABEL       | Unique label of Zokeeper statefulset                         | Mandatory |                                                         |
| ZOOKEEPER_SERVICE     | Headless service of the Zookeeper Statefulset                | Mandatory |                                                         |
| ZOOKEEPER_PORT        | Port of the Zookeeper ClusterIP service                      | Mandatory |                                                         |
| KAFKA_KIND            | Kafka deployment type                                        | Optional  | Same as `spec.appinfo.appkind`. Supported: `statefulset`| 
| KAFKA_LIVENESS_STREAM | Kafka liveness message stream                                | Optional  | Supported: `enabled`, `disabled`                        |
| KAFKA_LIVENESS_IMAGE	| Image used for liveness message stream                       | Optional  | Image as `<registry_url>/<repository>/<image>:<tag>`    |
| KAFKA_REPLICATION_FACTOR| Number of partition replicas for liveness topic partition  | Optional  | Necessary if KAFKA_LIVENESS_STREAM is `enabled`         |
| KAFKA_INSTANCE_NAME   | Name of the Kafka chroot path on zookeeper                   | Optional  | Necessary if installation involves use of such path     |
| KAFKA_CONSUMER_TIMEOUT| Kafka consumer message timeout, post which it terminates     | Optional  | Defaults to 30000ms                                     |
| KAFKA_BROKER          | Kafka broker pod (name) to be deleted                        | Optional  | A target selection mode (random/liveness-based/specific)|
| TOTAL_CHAOS_DURATION  | The time duration for chaos insertion (seconds)              | Optional  | Defaults to 15s                                         |
| CHAOS_INTERVAL        | Time interval b/w two successive broker failures (sec)       | Optional  | Defaults to 5s                                          |
| LIB                   | The chaos lib used to inject the chaos                       | Optional  | Defaults to `litmus`. Supported: `litmus`, `powerfulseal| 
| CHAOS_SERVICE_ACCOUNT	| Service account used by the powerfulseal deployment          | Optional  | Defaults to `default` on namespace `spec.appinfo.appns` |

#### Sample ChaosEngine Manifest

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: kafka-chaos
  namespace: default
spec:
  appinfo: 
    appns: default
    applabel: 'app=cp-kafka'
    appkind: statefulset
  chaosServiceAccount: kafka-sa
  monitoring: false
  jobCleanUpPolicy: delete
  experiments:
    - name: kafka-broker-pod-failure
      spec:
        components:  
          # choose based on available kafka broker replicas           
          - name: KAFKA_REPLICATION_FACTOR
            value: '3'

          # get via "kubectl get pods --show-labels -n <kafka-namespace>"
          - name: KAFKA_LABEL
            value: 'app=cp-kafka'

          - name: KAFKA_NAMESPACE
            value: 'default'
     
          # get via "kubectl get svc -n <kafka-namespace>" 
          - name: KAFKA_SERVICE
            value: 'kafka-cp-kafka-headless'

          # get via "kubectl get svc -n <kafka-namespace>  
          - name: KAFKA_PORT
            value: '9092'

          # in milliseconds  
          - name: KAFKA_CONSUMER_TIMEOUT
            value: '70000'

          # ensure to set the instance name if using KUDO operator
          - name: KAFKA_INSTANCE_NAME
            value: ''

          - name: ZOOKEEPER_NAMESPACE
            value: 'default'

          # get via "kubectl get pods --show-labels -n <zk-namespace>"
          - name: ZOOKEEPER_LABEL
            value: 'app=cp-zookeeper'

          # get via "kubectl get svc -n <zk-namespace>  
          - name: ZOOKEEPER_SERVICE
            value: 'kafka-cp-zookeeper-headless'

          # get via "kubectl get svc -n <zk-namespace>  
          - name: ZOOKEEPER_PORT
            value: '2181'

          # set chaos duration (in sec) as desired
          - name: TOTAL_CHAOS_DURATION
            value: '60'
            
          # set chaos interval (in sec) as desired
          - name: CHAOS_INTERVAL
            value: '20'

          # pod failures without '--force' & default terminationGracePeriodSeconds
          - name: FORCE
            value: "false"
```

### Create the ChaosEngine Resource 

- Create the ChaosEngine manifest prepared in the previous step to trigger the Chaos. 

  `kubectl apply -f chaosengine.yml`

### Watch Chaos progress  

- View pod terminations & recovery by setting up a watch on the pods in the Kafka namespace

  `watch -n 1 kubectl get pods -n <kafka-namespace>` 

### Check Chaos Experiment Result 

- Check whether the kafka deployment is resilient to the broker pod failure, once the experiment (job) is completed.
  The ChaosResult resource name is derived like this: `<ChaosEngine-Name>-<ChaosExperiment-Name>`.

  `kubectl describe chaosresult kafka-chaos-kafka-broker-pod-failure -n <kafka-namespace>` 

## Kafka Broker Pod Failure Demo 

- TODO: A sample recording of this experiment execution is provided here.

------
