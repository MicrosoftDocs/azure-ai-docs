---
title: "Bring your own registry for hosted agents"
description: "Deploy a Microsoft Foundry hosted agent from your private container registry using OIDC-based authentication."
author: aahill
ms.author: aahi
ms.date: 08/18/2026
ms.manager: mcleans
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Bring your own registry for hosted agents

**Overview**

This article shows how to let a Microsoft Foundry hosted agent pull its image
from a private container registry. You create a Foundry project connection that
uses OIDC token exchange and short-lived tokens instead of stored registry
credentials.

The pattern works with any registry that supports OIDC token exchange. For a
walkthrough, see the setup examples for JFrog Artifactory and Docker
Distribution.

The Entra application provides the audience value used during token exchange.
The Foundry project managed identity (MI) authenticates with the registry's
OIDC provider, which exchanges its token for short-lived image-pull
credentials.

## Prerequisites

- An Azure subscription.
- A Foundry project with `Foundry Project Manager` role. See [Hosted agent permissions reference](hosted-agent-permissions.md).
- [Azure CLI](/cli/azure/install-azure-cli) installed and authenticated.
- A private container registry with OIDC support.
- A container image in your registry.
- Permissions to configure OIDC in your registry.
- For Docker Distribution, an RFC 8693 token-exchange service and a registry
  token service.

## Set up OIDC authentication

### Step 1: Create an Entra application

```azurecli
az ad app create --display-name "Foundry-Registry-Agent"
```

Copy the application (client) ID. Use it as the audience when you configure
your registry.

## Configure the registry connection

Choose the registry that hosts your image. In either tab:

1. Configure the registry to trust the Foundry project managed identity.
2. Map the identity to a repository with image-pull permission.
3. Create the Foundry project connection with `type` set to
   `registry_connection` and `mode` set to `oauth_token_exchange`.

### [JFrog Artifactory](#tab/jfrog)

1. In JFrog, create an OIDC provider for the Foundry project managed identity.
2. Give the provider read access to the image repository.
3. Use `/access/api/v1/oidc/token` as the token endpoint.
4. Record the JFrog OIDC provider name.

Create the connection with these values:

| Field | Value |
| --- | --- |
| `target` | `https://<jfrog-host>` |
| `credentials.keys.audience` | Entra application client ID |
| `credentials.keys.tokenEndpoint` | `/access/api/v1/oidc/token` |
| `credentials.keys.body.provider_name` | JFrog OIDC provider name |

When you create the connection, also provide
`body.provider_name=<oidc-provider-name>` as a custom key.

### [Docker Distribution](#tab/docker-distribution)

Docker Distribution doesn't provide OIDC by itself. Deploy an RFC 8693
token-exchange service and a registry token service in front of the registry.

1. Configure the token-exchange service to validate the Foundry project
   managed identity token.
2. Configure the registry token service to authorize the exchanged credential
   for the image repository.
3. Return a short-lived `access_token` and `username` from the
   token-exchange service.
4. Record the token-exchange endpoint.

Create the connection with these values:

| Field | Value |
| --- | --- |
| `target` | `https://<registry-host>` |
| `credentials.keys.audience` | Entra application client ID |
| `credentials.keys.tokenEndpoint` | `<token-exchange-path>` |
| `metadata.type` | `registry_connection` |
| `metadata.mode` | `oauth_token_exchange` |

## Create the registry connection

If your Foundry project already exists, create the registry connection with
Azure Developer CLI or the Azure REST API. If the project doesn't exist, use
the Azure REST API to create the project and registry connection before you
create the agent. Use the values from the registry tab you selected.

### [Azure Developer CLI](#tab/azd)

Use this option when you already have a Foundry project.

```bash
azd extension install azure.ai.connections

PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"

azd ai connection create private-registry \
  --project-endpoint "$PROJECT_ENDPOINT" \
  --kind custom-keys \
  --target "https://<registry-host>" \
  --auth-type custom-keys \
  --custom-key "audience=<entra-application-client-id>" \
  --custom-key "tokenEndpoint=<token-exchange-path>" \
  --metadata "type=registry_connection" \
  --metadata "mode=oauth_token_exchange"
```

### [Azure REST API](#tab/rest)

Use this option for an existing project, or to create the project and registry
connection before you create the agent.

Check whether the connection exists before creating it. Reuse an existing
connection with the expected configuration.

```powershell
$connectionId = "/subscriptions/$env:AZURE_SUBSCRIPTION_ID/resourceGroups/$env:AZURE_RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/$env:FOUNDRY_ACCOUNT_NAME/projects/$env:FOUNDRY_PROJECT_NAME/connections/$env:FOUNDRY_CONNECTION_NAME"

az rest `
  --method get `
  --url "https://management.azure.com${connectionId}?api-version=2025-10-01-preview"
```

If the connection doesn't exist, create it with the registry-specific values:

```powershell
$connection = @{
  properties = @{
    category = "CustomKeys"
    authType = "CustomKeys"
    target = "https://<registry-host>"
    isSharedToAll = $true
    useWorkspaceManagedIdentity = $false
    metadata = @{
      type = "registry_connection"
      mode = "oauth_token_exchange"
    }
    credentials = @{
      keys = @{
        audience = "<entra-application-client-id>"
        tokenEndpoint = "<token-exchange-path>"
      }
    }
  }
} | ConvertTo-Json -Depth 10

az rest `
  --method put `
  --url "https://management.azure.com${connectionId}?api-version=2025-10-01-preview" `
  --body $connection
```

## Create the agent

After the registry connection exists, initialize the agent with the existing
project and connection:

```bash
azd ai agent init --no-prompt \
  --agent-name private-registry-agent \
  --image <registry-host>/<repository>/agent:<tag> \
  --project-id <foundry-project-resource-id> \
  --registry-connection private-registry
```

In the generated `azure.yaml`, reference the private registry image and
connection:

```yaml
services:
  private-registry-agent:
    host: azure.ai.agent
    image: "<registry-host>/<repository>/agent:<tag>"
    docker:
      imagePassthrough: true
    registryConnectionId: "private-registry"
    kind: hosted
    name: private-registry-agent
```

## Network options

Choose the option that matches your Foundry project network configuration:

### [Without VNet isolation](#tab/without-vnet)

For Foundry projects with public network access:

#### Deploy the agent

```azurecli
azd deploy
```

#### Verify the agent is active

```azurecli
azd ai agent show
```

Wait for the status to change to **Active**.

#### Invoke the agent

```azurecli
azd ai agent invoke "<prompt>"
```

### [With VNet isolation](#tab/with-vnet)

For Foundry projects deployed within a VNet with private endpoints:

#### Network requirements

Before deployment, ensure that your registry token endpoint is accessible from
within the Foundry VNet.

#### Registry connectivity via Private Link

If your registry supports Azure Private Link:

1. Create a private endpoint in your Foundry VNet targeting your registry.
2. Configure DNS resolution in your Foundry VNet to route requests to your
   registry through the private endpoint.

#### Deploy the agent

```azurecli
azd deploy
```

Foundry automatically uses the registry connection to pull images over the
VNet's private network path.

#### Verify the agent is active

```azurecli
azd ai agent show
```

Wait for the status to change to **Active**.

#### Invoke the agent

```azurecli
azd ai agent invoke "<prompt>"
```

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Token exchange fails with "Public access is disabled" | Registry OIDC provider isn't accessible publicly | Verify your registry OIDC integration allows public token requests |
| Token exchange fails with "invalid_subject" or "invalid_audience" | OIDC claim mappings don't match | Confirm issuer, subject, and audience values match in Entra ID and your registry |
| Image pull fails after successful token exchange | Registry identity lacks permissions | Ensure the registry identity has read access to your image repository |
| Agent deployment fails with connection timeout | VNet isolation blocks registry access | Set up a private link to allow access to the registry token endpoint |

## Next steps

- Learn more about [hosted agent concepts](hosted-agents.md).
- Explore [Foundry permissions](hosted-agent-permissions.md).
- Set up [CI/CD for agents](../quickstarts/set-up-cicd-hosted-agent.md).
