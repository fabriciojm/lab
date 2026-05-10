# Example: Installing gethomepage.dev with Helm

Following https://github.com/gethomepage/homepage/blob/dev/kubernetes.md

We use the unofficial gethomepage.dev helm chart.

```bash
helm repo add jameswynn https://jameswynn.github.io/helm-charts
helm install my-release jameswynn/homepage
```

Default port on gethomepage.dev was 3000, but I was already using that for something else, so need to choose a new one.

Now I need to:
- Include the gateway IP in the `HOMEPAGE_ALLOWED_HOSTS` variable.
- Have the homepage be a service of type LoadBalancer with port `HOMEPAGE_PORT` and targetPort `HOMEPAGE_TARGETPORT`

```bash
helm show values jameswynn/homepage > homepage-values.yaml
```

Then edit

```yaml
# (...)
service:
  main:
    type: LoadBalancer
    ports:
      http:
        port: ${HOMEPAGE_PORT}
        targetPort: ${HOMEPAGE_TARGETPORT}

# (...)
env:
  - name: HOMEPAGE_ALLOWED_HOSTS
    # This value must be set
    # ref: https://gethomepage.dev/installation/#homepage_allowed_hosts
    value: "${HOMEPAGE_HOST}"
# (...)
```

Note that the variable `HOMEPAGE_HOST` is `<external_ip>:<target_port>`.

Add a little script `homepage-upgrade`

```bash
#!/bin/bash
# One liner to use envsubst to process secrets
# Usage: homepage-upgrade values.yaml
set -a
source ../../.env
set +a
envsubst < "$1" | helm upgrade my-release jameswynn/homepage -n monitoring -f -
```

Then

```bash
./homepage-upgrade homepage-values.yaml
```


