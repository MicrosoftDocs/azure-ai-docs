---
title: "Bring your own registry for hosted agents"
description: "Deploy a Microsoft Foundry hosted agent from an authenticated container registry outside Azure by using a project connection."
author: aahill
ms.author: aahi
ms.date: 08/27/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Bring your own registry for hosted agents

This article explains how to configure a Microsoft Foundry hosted agent to pull container images from an authenticated registry outside Azure or from a self-hosted Docker Distribution registry. You create a Foundry project connection that exchanges the project's managed identity token for short-lived image pull credentials, so you don't need to store registry credentials in the agent configuration.

In this article, *private registry* refers to any container registry that requires authentication. If you're using Azure Container Registry (ACR), including an ACR with public network access disabled, see [Deploy a hosted agent with a private Azure Container Registry](deploy-hosted-agent-private-azure-container-registry.md).

## Prerequisites

- An Azure subscription.
- An existing Foundry project. You need the `Foundry Project Manager` role to create a project connection. See [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

- [Azure CLI](/cli/azure/install-azure-cli), installed and authenticated.
- A Bash-compatible shell.
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd), version 1.32.0 or later, installed and authenticated.
- The Azure Developer CLI Foundry extensions, including `azure.ai.agents` 1.0.0-beta.13 or later. See [Install the Azure Developer CLI Foundry extensions](install-cli-foundry-extensions.md).
- A fully qualified prebuilt image in an authenticated container registry outside Azure or in a self-hosted Docker Distribution registry.
- Permission to configure identity trust and read-only repository access in the registry or its authentication service.
- The registry target, token audience, and token-exchange endpoint from your registry administrator.

A registry that supports OpenID Connect (OIDC) isn't automatically compatible with this workflow. The registry's authentication service must be able to exchange a Microsoft Foundry project managed identity token for short-lived credentials that the registry accepts for image pulls. JFrog Artifactory is one validated example of a compatible implementation. Docker Distribution requires an authentication adapter because its native bearer token authentication flow doesn't provide an OAuth 2.0 token exchange endpoint.

## Configure registry authentication

To configure the registry authentication service to trust the Foundry project managed identity and grant it pull access only to the repository that contains the agent image:

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

1. Choose the setup that matches your registry.

### JFrog Artifactory example

In JFrog Artifactory, create an OIDC integration and identity mapping that bind the project managed identity to a group with read-only repository access. Use `/access/api/v1/oidc/token` as the token endpoint. Record the JFrog OIDC provider name because the connection sends it to the token endpoint as`body.provider_name`.

Ask your JFrog administrator for the Microsoft Entra application ID configured as the OIDC audience. The audience in the Foundry connection must match the audience in the JFrog OIDC integration.

### Docker Distribution example

Docker Distribution uses a registry bearer-token challenge. A registry client first receives a `WWW-Authenticate` challenge and then requests a token with `service` and repository `scope` values. This flow differs from [OAuth 2.0 token exchange](https://www.rfc-editor.org/rfc/rfc8693).

Deploy an authentication adapter in front of the Distribution registry token service. Configure the adapter to:

- Trust the Foundry project managed identity.
- Accept the token exchange from the Foundry registry connection.
- Map the project identity to pull access for the required repository.
- Obtain or issue a short-lived credential that the Distribution registry
  accepts for that repository.

Configure the Distribution registry to trust the registry token service. For the challenge and token-service requirements, see [Docker Registry v2 authentication](https://distribution.github.io/distribution/spec/auth/token/).

The adapter implementation depends on your identity provider and registry token service. Use the adapter's HTTPS exchange endpoint as `tokenEndpoint` in the Foundry connection. Foundry doesn't define a universal Docker Distribution
adapter request and response contract. Before deployment, obtain the supported contract from your registry or adapter provider and test that the endpoint returns pull credentials that your Distribution registry accepts.

Record these values from your registry or adapter administrator:

| Value | Description |
| --- | --- |
| Registry target | HTTPS origin for the registry, such as `https://registry.contoso.com`. |
| Audience | Resource identifier configured as the token audience. |
| Token endpoint | HTTPS endpoint, or path relative to the registry target, that exchanges the project identity token. |
| Provider-specific fields | Extra form fields required by the token endpoint. JFrog Artifactory requires the OIDC provider name. |

## Create the registry connection

Create a `CustomKeys` connection in the same Foundry project that hosts the agent. The connection metadata identifies it as an image registry connection that uses OAuth token exchange.

1. Set the project endpoint. Include the project name in the `/api/projects/<project-name>` path:

   ```bash
   PROJECT_ENDPOINT="https://<account-name>.services.ai.azure.com/api/projects/<project-name>"
   ```

1. Create the connection. Choose the command for your registry authentication service.

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
  
     Add a `body.<field-name>` custom key for each extra form field that your
     adapter requires.

1. Verify the connection without displaying its credentials:

   ```azurecli
   azd ai connection show private-registry \
     --project-endpoint "$PROJECT_ENDPOINT"
   ```

The output identifies a `CustomKeys` connection with the registry target and the `registry_connection` metadata.

## Initialize the agent project

Initialize a hosted agent project with the fully qualified image and the connection name. The connection must already exist in the selected project.

1. Initialize the project:

   ```bash
   azd ai agent init --no-prompt \
     --agent-name private-registry-agent \
     --image <registry-host>/<repository>/agent:<tag> \
     --project-id "$PROJECT_ID" \
     --registry-connection private-registry
   ```

1. Review the generated `azure.yaml`. Keep the `azure.ai.project` service and the agent's `uses` relationship. The agent service must include the prebuilt image, `docker.imagePassthrough: true`, and the registry connection name:

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

1. If the agent requires runtime configuration, store nonsecret values in the active `azd` environment and reference them from the agent service's `env` map. Don't store secrets directly in `azure.yaml`. See [Configure environment variables for a hosted agent](configure-hosted-agent-env-variables.md).

## Configure private network access

Skip this section when the registry target and token endpoint are available through public HTTPS endpoints.

The Foundry account must also include hosted-agent virtual network injection when you create the account. You can't add network injection to an existing Foundry account for hosted agents. For the current constraints, see
[Set up private networking for Foundry Agent Service](virtual-networks.md).

1. Confirm that the registry provider exposes an Azure Private Link resource or that the self-hosted registry is available through a customer-managed Private Link Service. An Azure private endpoint can't target an arbitrary registry
   hostname.
1. Create a private endpoint in the Foundry virtual network that targets the provider's Private Link resource or the self-hosted registry's Private Link Service.
1. Configure private DNS so the registry hostname and token endpoint resolve to private endpoint addresses from the Foundry virtual network.
1. Allow outbound TCP 443 from the Foundry network to both endpoints.

## Deploy and verify the agent

Deploy the prebuilt image, wait for the hosted agent to become active, and send a test request.

1. Deploy the agent:

   ```azurecli
   azd deploy --no-prompt
   ```

1. Check its status:

   ```azurecli
   azd ai agent show
   ```

   Wait for the status to change to **Active**. A successful deployment confirms that Foundry exchanged the identity token and pulled the image.

1. Invoke the agent:

   ```azurecli
   azd ai agent invoke "Respond with a short deployment confirmation."
   ```

    A successful invocation returns a response from the agent. The **Active** deployment status confirms that Foundry retrieved and started the image. A successful invocation also confirms that the container implements the protocol declared in `azure.yaml`.

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
