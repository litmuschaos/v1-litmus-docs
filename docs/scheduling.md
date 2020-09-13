---
id: scheduling
title: Scheduler Usage
sidebar_label: Scheduling
---
------

The ChaosSchedule is the user-facing chaos custom resource with a namespace scope and is 
built on top of ChaosEngine. It schedules a number of instances of chaosengine according to the given schedule specifications.

It basically helps for the scheduled execution of chaos immediately, at a specific time or helps to execute chaos repeatedly with a specific time interval in between two instances. It brings more resiliency to the cluster because of the repeated executions of chaos and not just a single time as is the case of chaos engine.


## Prepare ChaosSchedule 

There are 3 scheduling strategies by which we can trigger the formation of chaosengine -

- now
- once
- repeat

They can only be followed one at a time.

### Sample ChaosSchedule Manifest for Now

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    now: true
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

### Sample ChaosSchedule Manifest for Once

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    once:
      executionTime: "2020-05-12T05:47:00Z"   #should be modified according to current UTC Time
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

### Sample ChaosSchedule Manifest for Repeat

There are various ways we can trigger this type of schedule by varying the the fields inside <code>spec.repeat</code>. <br><br>
**Note** - We have just one field i.e. <code>minChaosInterval</code> to be specified as mandatory one. All other fields are optional and totally depend on how we want to change the behavious of schedules.

#### Basic schema to execute repeat strategy

This will keep on executing the schedule and creating engines for an indefinite amount of time.

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    repeat:
      properties:
        minChaosInterval: "2m"   #format should be like "10m" or "2h" accordingly for minutes and hours
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

#### Specifying time boundations for the schedule

This will manipulate the schedule to be started and ended according to our will.

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    repeat:
      timeRange:
        startTime: "2020-05-12T05:47:00Z"   #should be modified according to current UTC Time
        endTime: "2020-09-13T02:58:00Z"   #should be modified according to current UTC Time
      properties:
        minChaosInterval: "2m"   #format should be like "10m" or "2h" accordingly for minutes and hours
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

##### Opting just for end time

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    repeat:
      timeRange:
        endTime: "2020-09-13T02:58:00Z"   #should be modified according to current UTC Time
      properties:
        minChaosInterval: "2m"   #format should be like "10m" or "2h" accordingly for minutes and hours
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

##### Opting just for the start time

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    repeat:
      timeRange:
        startTime: "2020-05-12T05:47:00Z"   #should be modified according to current UTC Time
      properties:
        minChaosInterval: "2m"   #format should be like "10m" or "2h" accordingly for minutes and hours
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

#### Specifying  work hours

This will ensure our schedule to create engines in only a specified hours of the day and not beyond that. No matter if any time boundations are specified or not.

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    repeat:
      properties:
        minChaosInterval: "2m"   #format should be like "10m" or "2h" accordingly for minutes and hours
      workHours:
        includedHours: 0-12
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

#### Specifying work days

This will ensure our schedule to create engines in only a specified days of the week and not beyond that. No matter if any time boundations are specified or not.

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    repeat:
      properties:
        minChaosInterval: "2m"   #format should be like "10m" or "2h" accordingly for minutes and hours
      workDays:
        includedDays: "Mon,Tue,Wed,Sat,Sun"
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

#### Specifying all the conditons together

We can choose any condition to specify or not except <code>minChaosInterval</code>.

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: schedule-nginx
spec:
  schedule:
    repeat:
      timeRange:
        startTime: "2020-05-12T05:47:00Z"   #should be modified according to current UTC Time
        endTime: "2020-09-13T02:58:00Z"   #should be modified according to current UTC Time
      properties:
        minChaosInterval: "2m"   #format should be like "10m" or "2h" accordingly for minutes and hours
      workHours:
        includedHours: 0-12
      workDays:
        includedDays: "Mon,Tue,Wed,Sat,Sun"
  engineTemplateSpec:
    appinfo:
      appns: 'default'
      applabel: 'app=nginx'
      appkind: 'deployment'
    # It can be true/false
    annotationCheck: 'true'
    #ex. values: ns1:name=percona,ns2:run=nginx
    auxiliaryAppInfo: ''
    chaosServiceAccount: pod-delete-sa
    monitoring: false
    # It can be delete/retain
    jobCleanUpPolicy: 'delete'
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              # set chaos duration (in sec) as desired
              - name: TOTAL_CHAOS_DURATION
                value: '30'

              # set chaos interval (in sec) as desired
              - name: CHAOS_INTERVAL
                value: '10'

              # pod failures without '--force' & default terminationGracePeriodSeconds
              - name: FORCE
                value: 'false'
```

## Halt/Resume ChaosSchedule


Schdeules can be <code>halted</code> or <code>resumed</code> as per the need. But it only works for <code>once</code> or <code>repeat</code> strategy as <code>now</code> immediately creates the engine.

For halting an active schedule we can simply follow these steps -

### Edit the applied chaosschedule

```
kubectl edit chaosschedule schedule-nginx
```

### Halt the schedule

Change the <code>spec.scheduleState</code> to <code>halt</code>

```yaml
spec:
  scheduleState: halt
  ...
```

For resuming a halted schedule we can simply follow these steps -

### Edit the applied chaosschedule

```
kubectl edit chaosschedule schedule-nginx
```

### Resume the schedule

Change the <code>spec.scheduleState</code> to <code>active</code>

```yaml
spec:
  scheduleState: active
  ...
```