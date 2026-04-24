# Kubernetes Services

A way to consistently access pods via the network.

The `expose` command directly creates a service from a resource:

```bash
kubectl apply -f frontend.yaml
kubectl expose frontend
kubectl get service -o wide
```

(Although in practice this is often done by code.)
