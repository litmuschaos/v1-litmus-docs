---
id: litmus-psp
title: Using Pod Security Policies with Litmus 
sidebar_label: Chaos Pod Security Policies
---
------

While working in environments (clusters) that have restrictive security policies, the default litmuschaos experiment execution procedure may be inhibited. 
This is mainly due to the fact that the experiment pods running the chaos injection tasks run with a root user. This, in turn, is necessitated due to the mounting 
of container runtime-specific socket files from the Kubernetes nodes in order to invoke runtime APIs. While this is not needed for all experiments (a considerable 
number of them use purely the K8s API), those involving injection of chaos processes into the network/process namespaces of other containers have this requirement 
(ex: netem, stress).

The restrictive policies are often enforced via [pod security policies](https://kubernetes.io/docs/concepts/policy/pod-security-policy/) (PSP) today, with organizations
opting for the default ["restricted"](https://kubernetes.io/docs/concepts/policy/pod-security-policy/#example-policies) policy. 


## Applying Pod Security Policies to Litmus Chaos Pods


- To run the litmus pods with operating characteristics described above, first create a custom PodSecurityPolicy that allows the same: 

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/pod-security-policy/psp-litmus.yaml yaml)
```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: litmus
  annotations:
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: '*'
spec:
  privileged: true
  # Required to prevent escalations to root.
  allowPrivilegeEscalation: true
  # Allow core volume types.
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    # Assume that persistentVolumes set up by the cluster admin are safe to use.
    - 'persistentVolumeClaim'
  allowedHostPaths:
    # substitutes this path with an appropriate socket path
    # ex: '/var/run/docker.sock', '/run/containerd/containerd.sock', '/run/crio/crio.sock'
    - pathPrefix: "/var/run/docker.sock"
    # substitutes this path with an appropriate container path
    # ex: '/var/lib/docker/containers', '/var/lib/containerd/io.containerd.runtime.v1.linux/k8s.io', '/var/lib/containers/storage/overlay/'
    - pathPrefix: "/var/lib/docker/containers"
  allowedCapabilities:
    - "NET_ADMIN"
    - "SYS_ADMIN"
  hostNetwork: false
  hostIPC: false
  hostPID: true
  seLinux:
    # This policy assumes the nodes are using AppArmor rather than SELinux.
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      # Forbid adding the root group.
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      # Forbid adding the root group.
      - min: 1
        max: 65535
  readOnlyRootFilesystem: false
```

  **Note**: This PodSecurityPolicy is a sample configuration which works for a majority of the usecases. It is left to the user's discretion to modify it based 
  on the environment. For example, if the experiment doesn't need the socket file to be mounted, `allowedHostPaths` can be excluded from the psp spec. On the
  other hand, in case of CRI-O runtime, network-chaos tests need the chaos pods executed in privileged mode. It is also possible that different PSP configs are
  used in different namespaces based on ChaosExperiments installed/executed in them. 

- Subscribe to the created PSP in the experiment RBAC (or in the [admin-mode](https://docs.litmuschaos.io/docs/admin-mode/#prepare-rbac-manifest) rbac, as applicable).
  For example, the pod-delete experiment rbac instrumented with the PSP is shown below:

[embedmd]:# (https://raw.githubusercontent.com/litmuschaos/chaos-charts/master/charts/generic/pod-delete/rbac-psp.yaml yaml) 
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-delete-sa
  namespace: default
  labels:
    name: pod-delete-sa
    app.kubernetes.io/part-of: litmus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-delete-sa
  namespace: default
  labels:
    name: pod-delete-sa
    app.kubernetes.io/part-of: litmus
rules:
- apiGroups: [""]
  resources: ["pods","events"]
  verbs: ["create","list","get","patch","update","delete","deletecollection"]
- apiGroups: [""]
  resources: ["pods/exec","pods/log","replicationcontrollers"]
  verbs: ["create","list","get"]
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["create","list","get","delete","deletecollection"]
- apiGroups: ["apps"]
  resources: ["deployments","statefulsets","daemonsets","replicasets"]
  verbs: ["list","get"]
- apiGroups: ["apps.openshift.io"]
  resources: ["deploymentconfigs"]
  verbs: ["list","get"]
- apiGroups: ["argoproj.io"]
  resources: ["rollouts"]
  verbs: ["list","get"]
- apiGroups: ["litmuschaos.io"]
  resources: ["chaosengines","chaosexperiments","chaosresults"]
  verbs: ["create","list","get","patch","update"]
- apiGroups: ["policy"]
  resources: ["podsecuritypolicies"]
  verbs: ["use"]
  resourceNames: ["litmus"] 
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-delete-sa
  namespace: default
  labels:
    name: pod-delete-sa
    app.kubernetes.io/part-of: litmus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-delete-sa
subjects:
- kind: ServiceAccount
  name: pod-delete-sa
  namespace: default

```

- Execute the ChaosEngine and verify that the litmus experiment pods are created successfully.  



