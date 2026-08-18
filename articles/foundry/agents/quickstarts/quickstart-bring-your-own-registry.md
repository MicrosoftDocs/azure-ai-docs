---
title: "Quickstart: Deploy a hosted agent from a private registry"
description: "Deploy a Microsoft Foundry hosted agent from your private container registry using OIDC-based authentication."
author: aahill
ms.author: aahi
ms.date: 08/18/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Quickstart: Deploy a hosted agent from a private registry

Deploy a Microsoft Foundry hosted agent from your private container registry using OIDC-based authentication. This approach uses short-lived tokens instead of storing long-lived credentials in your Foundry configuration.

This quickstart uses JFrog Artifactory as an example. The same steps work for any registry that supports OIDC token exchange.

## Prerequisites

- An Azure subscription.
- A Foundry project with `Foundry Project Manager` role. See [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).
- [Azure CLI](/cli/azure/install-azure-cli) installed and authenticated.
- A private container registry with OIDC support (for example, JFrog Artifactory).
- A container image in your registry.
- Permissions to configure OIDC in your registry.

## Set up OIDC authentication

### Step 1: Create a Microsoft Entra workload identity

```azurecli
# Create an app registration
az ad app create --display-name "Foundry-Registry-Agent"
```

Copy the `appId` output.

```azurecli
# Create a service principal
az ad sp create --id <appId>

# Create a federated credential for OIDC token exchange
az ad app federated-credential create \
  --id <appId> \
  --parameters '{
    "name": "foundry-registry",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:foundry-project-<projectId>:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

### Step 2: Configure your registry for OIDC

#### JFrog Artifactory

1. In JFrog, go to **Administration** > **Integrations** > **OIDC**.
2. Create an OIDC provider:
   - **Issuer URL**: The Foundry issuer (provided by your Foundry project)
   - **Audience**: `api://AzureADTokenExchange`
   - **Service Account**: Create a service account with read access to your image repository
3. Note the token endpoint: `https://<your-jfrog-instance>/artifactory/api/oauth/token`

#### Other registries

Configure your registry to:
- Trust the Foundry OIDC issuer
- Map OIDC subjects to a registry identity with image pull permissions
- Expose a token endpoint that exchanges OIDC tokens for registry tokens

### Step 3: Test token exchange

```bash
# Get an OIDC token
OIDC_TOKEN=$(az account get-access-token \
  --resource "api://AzureADTokenExchange" \
  --output json | jq -r '.accessToken')

# Exchange for a registry token
curl -X POST https://<your-jfrog-instance>/artifactory/api/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=$OIDC_TOKEN" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token"
```

A successful response includes an `access_token`.

## Deploy your agent

### Step 1: Create a registry connection

```azurecli
az foundry registry create \
  --name "my-registry" \
  --registry-type "oidc" \
  --registry-url "https://<your-jfrog-instance>/artifactory/docker" \
  --token-endpoint "https://<your-jfrog-instance>/artifactory/api/oauth/token" \
  --project "<foundry-project-name>" \
  --resource-group "<resource-group>"
```

Copy the registry ID from the output.

### Step 2: Update your agent configuration

In your `azure.yaml`, reference the private registry image and connection:

```yaml
agent:
  image:
    name: "docker.artifactory.jfrog.io/your-repo/your-agent:latest"
    registry: "<registry-connection-id>"
```

## Scenario A: Foundry without VNet isolation

For Foundry projects with public network access (no VNet injection):

### Deploy the agent

```azurecli
azd deploy
```

### Verify the agent is active

```azurecli
az foundry hosted-agent show \
  --agent-name "<agent-name>" \
  --project "<foundry-project-name>" \
  --resource-group "<resource-group>"
```

Wait for the status to change to **Active**.

### Invoke the agent

```azurecli
az foundry hosted-agent invoke \
  --agent-name "<agent-name>" \
  --project "<foundry-project-name>" \
  --resource-group "<resource-group>"
```

## Scenario B: Foundry with VNet isolation

For Foundry projects deployed within a VNet with private endpoints:

### Network requirements

Before deployment, ensure:
- Your JFrog token endpoint is accessible from within the Foundry VNet.
- Set up a private link or private endpoint to your JFrog instance (if needed).
- Configure firewall rules to allow outbound traffic from your Foundry VNet to the JFrog token endpoint.

### JFrog connectivity options

**Option 1: Private Link (recommended)**

If your JFrog instance supports Azure Private Link:

1. Create a private endpoint in your Foundry VNet targeting the JFrog service.
2. Configure DNS resolution in your Foundry VNet to route requests to your JFrog instance via the private endpoint.

**Option 2: Firewall rules**

If Private Link isn't available:

1. Identify the JFrog token endpoint URL (for example, `https://<your-jfrog-instance>/artifactory/api/oauth/token`).
2. Add a firewall rule to allow outbound HTTPS (port 443) from your Foundry VNet to the JFrog instance.
3. Ensure DNS resolution works from within your Foundry VNet.

### Deploy the agent

```azurecli
azd deploy
```

Foundry automatically uses the registry connection to pull images over the VNet's private network path.

### Verify the agent is active

```azurecli
az foundry hosted-agent show \
  --agent-name "<agent-name>" \
  --project "<foundry-project-name>" \
  --resource-group "<resource-group>"
```

Wait for the status to change to **Active**.

### Invoke the agent

```azurecli
az foundry hosted-agent invoke \
  --agent-name "<agent-name>" \
  --project "<foundry-project-name>" \
  --resource-group "<resource-group>"
```

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Token exchange fails with "Public access is disabled" | Registry OIDC provider isn't accessible publicly | Verify your registry OIDC integration allows public token requests |
| Token exchange fails with "invalid_subject" or "invalid_audience" | OIDC claim mappings don't match | Confirm issuer, subject, and audience values match in Entra ID and your registry |
| Image pull fails after successful token exchange | Service account lacks permissions | Ensure the registry service account has read access to your image repository |
| Agent deployment fails with connection timeout | VNet isolation blocks registry access | Set up a private link or firewall rule to allow outbound traffic to the registry token endpoint |

## Next steps

- Learn more about [hosted agent concepts](../concepts/hosted-agents.md).
- Explore [Foundry permissions](../concepts/hosted-agent-permissions.md).
- Set up [CI/CD for agents](set-up-cicd-hosted-agent.md).

