---
title: "Bring your own registry for hosted agents"
description: "Deploy a Microsoft Foundry hosted agent from an authenticated container registry outside Azure by using a project connection."
author: aahill
ms.author: aahi
ms.date: 09/01/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Bring your own registry for hosted agents

This article shows how to deploy a Microsoft Foundry hosted agent that uses a container image stored in an authenticated container registry outside Azure, such as JFrog Artifactory or a self-hosted Docker Distribution registry. The solution uses OpenID Connect (OIDC) token exchange so that the agent can authenticate with the registry by using short-lived credentials instead of stored secrets, such as registry usernames, passwords, or access tokens.

In this article, *private registry* refers to any container registry that requires authentication. It doesn't refer to an Azure Container Registry (ACR) secured with an Azure private endpoint. To use an existing ACR or an ACR with public network access disabled, see [Deploy a hosted agent with a private Azure Container Registry](deploy-hosted-agent-private-azure-container-registry.md).

This approach works with non-Azure registries that support OIDC token exchange. A Microsoft Entra application and the Foundry project managed identity participate in the authentication flow, allowing the registry to issue short-lived credentials for image pulls.

## Prerequisites

- An Azure subscription.
- An existing Foundry project. You need the `Foundry Project Manager` role to create a project connection. See [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

- [Azure CLI](/cli/azure/install-azure-cli), installed and authenticated.
- A Bash-compatible shell.
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd), version 1.32.0 or later, installed and authenticated.
- The Azure Developer CLI Foundry extensions, including `azure.ai.agents` 1.0.0-beta.13 or later. See [Install the Azure Developer CLI Foundry extensions](install-cli-foundry-extensions.md).
- For the Python SDK workflow, Python 3.9 or later and the Azure AI Projects and Azure Identity packages.

  ```bash
  pip install azure-ai-projects azure-identity
  ```

- A fully qualified prebuilt image in an authenticated container registry outside Azure or in a self-hosted Docker Distribution registry.
- Permission to configure identity trust and read-only repository access in the registry or its authentication service.
- The registry target, token audience, and token-exchange endpoint from your registry administrator.

A registry that supports OpenID Connect (OIDC) isn't automatically compatible with this workflow. The registry's authentication service must be able to exchange a Microsoft Foundry project managed identity token for short-lived credentials that the registry accepts for image pulls. JFrog Artifactory is one validated example of a compatible implementation. Docker Distribution requires an authentication adapter because its native bearer token authentication flow doesn't provide an OAuth 2.0 token exchange endpoint.

## Create an Entra application

Create an Entra application to provide the audience value used during token exchange:

```bash
ENTRA_APPLICATION_ID=$(az ad app create \
  --display-name "Foundry-Registry-Agent" \
  --query appId \
  --output tsv)

echo "$ENTRA_APPLICATION_ID"
```

Record the application (client) ID. The application doesn't need a client secret for this flow. Give the application ID to your registry administrator to configure as the expected audience in the registry's OIDC provider or token-exchange service.

## Configure OIDC for your registry

Configure the registry authentication service to trust the Foundry project managed identity and grant it pull access only to the repository that contains the agent image:

1. Set the Foundry project resource ID.

   ```bash
   PROJECT_ID="/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/projects/<project-name>"
   ```

1. Get the project managed identity object ID.

   ```azurecli
   PROJECT_PRINCIPAL_ID=$(az resource show \
     --ids "$PROJECT_ID" \
     --api-version 2025-06-01 \
     --query identity.principalId \
     --output tsv)

   echo "$PROJECT_PRINCIPAL_ID"
   ```

1. Give `PROJECT_PRINCIPAL_ID` to your registry administrator. Bind that identity
  to read-only access for the repository that contains the agent image.

Choose the setup that matches your registry.

### [JFrog Artifactory](#tab/jfrog)

In JFrog Artifactory, create an OIDC integration and identity mapping that bind the project managed identity to a group with read-only repository access. Use `/access/api/v1/oidc/token` as the token endpoint. Record the JFrog OIDC provider name because the connection sends it to the token endpoint as `body.provider_name`.

Configure the Entra application ID from Step 1 as the JFrog OIDC audience. The audience in the Foundry connection must match the audience in the JFrog OIDC integration.

Record these values from your JFrog administrator:

| Value | Description |
| --- | --- |
| Registry target | HTTPS origin for the registry, such as `https://registry.contoso.com`. |
| Audience | Microsoft Entra application ID configured as the JFrog OIDC audience. |
| Token endpoint | `/access/api/v1/oidc/token`. |
| OIDC provider name | Provider name sent as `body.provider_name`. |

### [Docker Distribution](#tab/docker-distribution)

Docker Distribution uses a registry bearer-token challenge. A registry client first receives a `WWW-Authenticate` challenge and then requests a token with `service` and repository `scope` values. This flow differs from [OAuth 2.0 token exchange](https://www.rfc-editor.org/rfc/rfc8693).

Deploy an authentication adapter in front of the Distribution registry token service. Configure the adapter to:

- Trust the Foundry project managed identity.
- Accept the token exchange from the Foundry registry connection.
- Map the project identity to pull access for the required repository.
- Obtain or issue a short-lived credential that the Distribution registry
  accepts for that repository.

Configure the Distribution registry to trust the registry token service. For the challenge and token-service requirements, see [Docker Registry v2 authentication](https://distribution.github.io/distribution/spec/auth/token/).

The adapter implementation depends on your identity provider and registry token service. Use the adapter's HTTPS exchange endpoint as `tokenEndpoint` in the Foundry connection. Foundry doesn't define a universal Docker Distribution adapter request and response contract. Before deployment, obtain the supported contract from your registry or adapter provider and test that the endpoint returns pull credentials that your Distribution registry accepts.

Record these values from your adapter administrator:

| Value | Description |
| --- | --- |
| Registry target | HTTPS origin for the registry, such as `https://registry.contoso.com`. |
| Audience | Resource identifier configured as the token audience. |
| Token endpoint | HTTPS endpoint, or path relative to the registry target, that exchanges the project identity token. |
| Provider-specific fields | Extra form fields required by the token endpoint. |

---

## Create the registry connection

Create a `CustomKeys` connection in the same Foundry project that hosts the agent. The connection metadata identifies it as an image registry connection that uses OAuth token exchange.

### [Azure Developer CLI](#tab/connection-azd)

Set the project endpoint. Include the project name in the `/api/projects/<project-name>` path:

```bash
PROJECT_ENDPOINT="https://<account-name>.services.ai.azure.com/api/projects/<project-name>"
```

Create the connection. Choose the command for your registry authentication service.

For JFrog Artifactory:

```bash
azd ai connection create private-registry \
  --project-endpoint "$PROJECT_ENDPOINT" \
  --kind custom-keys \
  --target "https://<registry-host>" \
  --auth-type custom-keys \
  --custom-key "audience=<token-audience>" \
  --custom-key "tokenEndpoint=<token-exchange-path>" \
  --custom-key "body.provider_name=<oidc-provider-name>" \
  --metadata "type=registry_connection" \
  --metadata "mode=oauth_token_exchange"
```

For a Docker Distribution authentication adapter:

```bash
azd ai connection create private-registry \
  --project-endpoint "$PROJECT_ENDPOINT" \
  --kind custom-keys \
  --target "https://<registry-host>" \
  --auth-type custom-keys \
  --custom-key "audience=<token-audience>" \
  --custom-key "tokenEndpoint=<adapter-token-exchange-path>" \
  --metadata "type=registry_connection" \
  --metadata "mode=oauth_token_exchange"
```

Add a `body.<field-name>` custom key for each extra form field that your adapter requires.

Verify the connection without displaying its credentials:

```azurecli
azd ai connection show private-registry \
  --project-endpoint "$PROJECT_ENDPOINT"
```

The output identifies a `CustomKeys` connection with the registry target and the `registry_connection` metadata.

### [Bicep](#tab/connection-bicep)

Create a file named `registry-connection.bicep`. The `providerName` parameter is optional. Supply it for JFrog Artifactory and omit it for a Docker Distribution authentication adapter.

```bicep
targetScope = 'resourceGroup'

param accountName string
param projectName string
param connectionName string = 'private-registry'
param registryTarget string
param audience string
param tokenEndpoint string
param providerName string = ''

var registryKeys = union(
  {
    audience: audience
    tokenEndpoint: tokenEndpoint
  },
  empty(providerName) ? {} : {
    'body.provider_name': providerName
  }
)

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  parent: account
  name: projectName
}

resource registryConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-04-01-preview' = {
  parent: project
  name: connectionName
  properties: {
    category: 'CustomKeys'
    target: registryTarget
    authType: 'CustomKeys'
    credentials: {
      keys: registryKeys
    }
    metadata: {
      type: 'registry_connection'
      mode: 'oauth_token_exchange'
    }
  }
}

output registryConnectionId string = registryConnection.id
```

Deploy the template at resource-group scope:

```azurecli
az deployment group create \
  --resource-group <resource-group> \
  --template-file registry-connection.bicep \
  --parameters \
      accountName=<foundry-account-name> \
      projectName=<foundry-project-name> \
      connectionName=private-registry \
      registryTarget=https://<registry-host> \
      audience=<token-audience> \
      tokenEndpoint=<token-exchange-path> \
      providerName=<jfrog-oidc-provider-name>
```

For a Docker Distribution authentication adapter, omit the `providerName` parameter. Add another key to `registryKeys` for each extra `body.<field-name>` value that your adapter requires.

---

## Configure private network access

Choose the option that matches your Foundry project network configuration.

### [Without VNet isolation](#tab/without-vnet)

When the registry target and token endpoint are available through public HTTPS endpoints, you don't need to configure extra registry networking.

### [With VNet isolation](#tab/with-vnet)

The Foundry account must also include hosted-agent virtual network injection when you create the account. You can't add network injection to an existing Foundry account for hosted agents. For the current constraints, see
[Set up private networking for Foundry Agent Service](virtual-networks.md).

1. Confirm that the registry provider exposes an Azure Private Link resource or that the self-hosted registry is available through a customer-managed Private Link Service. An Azure private endpoint can't target an arbitrary registry
   hostname.
1. Create a private endpoint in the Foundry virtual network that targets the provider's Private Link resource or the self-hosted registry's Private Link Service.
1. Configure private DNS so the registry hostname and token endpoint resolve to private endpoint addresses from the Foundry virtual network.
1. Allow outbound TCP 443 from the Foundry network to both endpoints.

---

## Create and deploy the agent

Create and deploy the hosted agent from the prebuilt private registry image.

### [Azure Developer CLI](#tab/deployment-azd)

Initialize a hosted agent project with the fully qualified image and the connection name. The connection must already exist in the selected project.

```bash
azd ai agent init --no-prompt \
  --agent-name private-registry-agent \
  --image <registry-host>/<repository>/agent:<tag> \
  --project-id "$PROJECT_ID" \
  --registry-connection private-registry
```

Review the generated `azure.yaml`. Keep the `azure.ai.project` service and the agent's `uses` relationship. The agent service must include the prebuilt image, `docker.imagePassthrough: true`, and the registry connection name:

```yaml
services:
  existing-project:
    host: azure.ai.project
    endpoint: ${FOUNDRY_PROJECT_ENDPOINT}

  private-registry-agent:
    host: azure.ai.agent
    uses:
      - existing-project
    kind: hosted
    name: private-registry-agent
    image: "<registry-host>/<repository>/agent:<tag>"
    docker:
      imagePassthrough: true
    registryConnectionId: private-registry
    protocols:
      - protocol: responses
        version: "2.0.0"
```

An existing connection doesn't belong in the `uses` list. The `registryConnectionId` value can be the connection's Foundry name or resource ID.

If the agent requires runtime configuration, store nonsecret values in the active `azd` environment and reference them from the agent service's `env` map. Don't store secrets directly in `azure.yaml`. See [Configure environment variables for a hosted agent](configure-hosted-agent-env-variables.md).

Deploy the agent:

```azurecli
azd deploy --no-prompt
```

### [Python SDK](#tab/deployment-python)

Create the hosted agent version with `registry_connection_id` set to the name or resource ID of the existing Foundry project connection. Creating the version also deploys the agent.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ContainerConfiguration,
    HostedAgentDefinition,
    ProtocolVersionRecord,
)
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

agent = project.agents.create_version(
    agent_name="private-registry-agent",
    definition=HostedAgentDefinition(
        cpu="0.5",
        memory="1Gi",
        container_configuration=ContainerConfiguration(
            image="<registry-host>/<repository>/agent:<tag>",
            registry_connection_id="private-registry",
        ),
        protocol_versions=[
            ProtocolVersionRecord(
                protocol="responses",
                version="2.0.0",
            )
        ],
        environment_variables={
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": os.environ[
                "AZURE_AI_MODEL_DEPLOYMENT_NAME"
            ],
        },
    ),
)

print(f"Created {agent.name}, version {agent.version}")
```

The SDK sends the connection name or resource ID as `registry_connection_id` in the agent definition. Registry credentials remain in the Foundry project connection and aren't included in your code.

---

## Verify and invoke the agent

Wait for the hosted agent to become active, and then send a test request.

### [Azure Developer CLI](#tab/deployment-azd)

Check the agent status:

```azurecli
azd ai agent show
```

Wait for the status to change to **Active**, and then invoke the agent:

```azurecli
azd ai agent invoke "Respond with a short deployment confirmation."
```

### [Python SDK](#tab/deployment-python)

Poll the deployed version until it becomes active:

```python
import time

while True:
    version = project.agents.get_version(
        agent_name="private-registry-agent",
        agent_version=agent.version,
    )
    status = version["status"]
    print(f"Status: {status}")

    if status == "active":
        break
    if status == "failed":
        raise RuntimeError(f"Agent deployment failed: {version['error']}")

    time.sleep(5)
```

Invoke the agent through its Responses endpoint:

```python
openai_client = project.get_openai_client(
    agent_name="private-registry-agent"
)

response = openai_client.responses.create(
    input="Respond with a short deployment confirmation.",
)

print(response.output_text)
```

---

A successful deployment confirms that Foundry exchanged the identity token, retrieved the image, and started the container. A successful invocation also confirms that the container implements the configured Responses protocol.

## Troubleshoot registry deployment

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Token exchange returns `invalid_subject` | The registry mapping doesn't identify the project managed identity. | Compare the identity claim used by the registry with the project's managed identity object ID. |
| Token exchange returns `invalid_audience` or `invalid_target` | The connection audience and registry identity-provider audience don't match. | Use the same resource identifier in the registry provider and the connection's `audience` key. |
| Token exchange rejects the issuer | The registry provider expects a different token issuer. | Inspect the presented token in the registry authentication logs, and configure the provider to match its `iss` claim exactly. |
| Token exchange succeeds, but the image pull returns `403` | The mapped identity lacks repository pull permission, or the issued token has the wrong scope. | Grant read-only pull permission for the image repository and verify the token's repository scope. |
| A Docker Distribution registry returns `401` after token exchange | The adapter-issued credential doesn't satisfy the registry's bearer-token requirements. | Verify the registry `service`, repository `scope`, token issuer, signing key, and trust configuration. |
| The registry connection can't be found | The connection exists in a different Foundry project, or the name doesn't match. | Create the connection in the selected project and set `registryConnectionId` to its exact name or resource ID. |
| The request times out | Foundry can't resolve or reach the registry or token endpoint. | Verify private DNS, private endpoint approval, routes, firewalls, and outbound TCP 443 for both endpoints. |

## Related content

- [Understand hosted agents](../concepts/hosted-agents.md).
- [Review hosted agent permissions](../concepts/hosted-agent-permissions.md).
- [Set up CI/CD for hosted agents](set-up-ci-cd-cli.md).
