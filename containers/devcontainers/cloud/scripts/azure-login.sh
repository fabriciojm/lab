#!/bin/bash
set -euo pipefail

az login \
  --service-principal \
  --username "$AZURE_CLIENT_ID" \
  --password "$AZURE_CLIENT_SECRET" \
  --tenant "$AZURE_TENANT_ID" \
  --output none

az account set --subscription "$AZURE_SUBSCRIPTION_ID"
