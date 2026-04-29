# Kubernetes Services

A way to consistently access pods via the network.

The `expose` command directly creates a service from a resource:

```bash
kubectl apply -f frontend.yaml
kubectl expose frontend
kubectl get service -o wide
```
(Although in practice this is often done by code.)

Can edit a service to be of a specific type by editing

```bash
kubectl edit svc frontend # modify spec/type to LoadBalancer, for example, to get an external IP if it was created as ClusterIP (no extenal IP).
```

If a service was created from a deployment, one can export it via `kubectl get service [SVC_NAME] -o yaml > file.yaml`
