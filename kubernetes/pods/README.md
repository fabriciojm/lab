# Kubernetes Cluster Pods

Pods are the atoms of a Kubernetes cluster, its smallest part.

Survival commands

```bash
kubectl get pods
kubectl run [IMAGE-NAME] --image=[IMAGE]
```

## Examples of Pods as Code

- `nginx.yml` was created from a dry run `kubectl run [POD-NAME] --image=[IMAGE-NAME] --dry-run=client -o yaml > [FILE]`.
- `nginx-docs.yml` from the docs: https://kubernetes.io/docs/concepts/workloads/pods/.
