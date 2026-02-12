---
title: Publish agents in Microsoft Foundry
description: Learn how to publish agents in Microsoft Foundry, configure authentication and permissions, and use a stable endpoint to invoke your agent.
#customer intent: As a developer, I want to publish an agent in Microsoft Foundry so that I can provide a stable endpoint for external consumption.
author: sdgilley
ms.author: sgilley
ms.reviewer: amandafoster
ms.date: 01/20/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
ms.custom: pilot-ai-workflow-jan-2026
---

# Publish and share agents in Microsoft Foundry

Publishing promotes an agent from a development asset inside your Foundry project into a managed Azure resource that external consumers can call through a stable endpoint. Think of it as the step that moves your agent from "works in my project" to "ready for others to use."

This article shows you how to publish an agent, configure its authentication and permissions, and update your Agent Application as you roll out new agent versions. After publishing, see the following articles to consume your Agent Application:
- [Invoke your Agent Application using the Responses API protocol](./publish-responses.md)
- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md) 

## What is publishing?

During development, you build and test your agent inside a Foundry project. The project gives you and your teammates a shared workspace, but it isn't designed for broad distribution — everyone with project access can interact with all agents and shares the same conversation context and permissions. Publishing is the step that moves an agent out of that shared development space and into a production-ready Azure resource.

When you publish an agent version, Foundry creates an **Agent Application** resource that wraps your agent version with its own invocation URL, authentication policy, unique Entra agent identity and Entra agent blueprint, and registers it in the [Entra Agent Registry](/entra/agent-id/identity-platform/what-is-agent-registry) for discoverability and governance. A **Deployment** is also created as a child resource of the application, referencing the specific agent version being published and supporting start/stop lifecycle management.

### Why publish?

Publishing gives you capabilities that project-level development doesn't provide:

- **External sharing** — Grant access to teammates or customers without giving them access to your Foundry project.
- **Stable endpoint** — The application URL stays the same even as you roll out new agent versions. Existing integrations continue to work without code changes, and you don't need to republish to Microsoft 365 or Teams, just update the Agent Application deployment and the changes take effect automatically.
- **Distinct agent identity** — The published agent gets its own Entra agent identity and Entra agent blueprint, separate from the project's shared identity and blueprint.
- **Independent RBAC and authorization** — The Agent Application is a separate Azure resource with its own RBAC scope. You can assign roles like Azure AI User directly on the Agent Application resource to control who can invoke it.
- **Azure Policy integration** — As an Azure Resource Manager (ARM) resource, the application can be governed by Azure Policy.
- **Integration with Microsoft 365 Copilot and Teams** — Distribute your Agent Application to channels like Microsoft 365 Copilot and Teams.
- **[Coming soon] User data isolation** — Each caller's interactions are private by default, unlike the shared conversation state in a project.
- **[Coming soon] Govern in Agent 365** — Published agents automatically surface in Agent 365 and the Entra Agent Registry.

### What changes when you publish?

The most important change is identity. Before publishing, your agent uses the project's shared agent identity. After publishing, the agent receives its own dedicated agent identity. Any tools that rely on agent identity authentication switch from the project's shared agent identity to the unique agent identity that's associated with the agent application.

### What to watch for

Because the identity changes, **permissions don't transfer automatically**. When you publish an agent, you must reassign RBAC permissions to the new agent identity for any resources that the agent needs to access. If you skip this step, tool calls that worked during development will fail with authorization errors once the agent is published.

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md) with at least one agent version created
- [Azure AI Project Manager role](../../../concepts/rbac-foundry.md) on the Foundry project scope to publish agents
- [Azure AI User role](../../../concepts/rbac-foundry.md) on the Agent Application scope to chat with a published agent using the Responses API protocol
- Familiarity with [Azure role-based access control (RBAC)](/azure/role-based-access-control/overview) for permission configuration
- Familiarity with [Agent identity concepts in Foundry](../concepts/agent-identity.md)
- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../../../how-to/develop/install-cli-sdk.md)

[!INCLUDE [code-preview](../../includes/code-preview.md)]


## Understand Agent Applications and deployments

Before publishing, it's important to understand the relationship between projects, agent versions, applications, and deployments.

:::image type="content" source="../../media/publish-agent/azure-agent-identity-overview.png" alt-text="Diagram illustrating how Foundry projects organize agent versions, applications, and deployments, highlighting governance and RBAC roles.":::

A Foundry **project** is a work organization concept that groups related resources such as agents, files, and indexes. An **agent** represents a composable unit — defined by its instructions, model, and tools. An **agent version** captures a specific immutable snapshot of an agent. Every time you make changes to your agent, such as updating the prompt or adding tools, a new agent version is created. When you create an agent version, it's exposed under the project where developers with project access can create, run, and test it.

An **Agent Application** projects one or more agents as a service — independently addressable, governable, and equipped with lifecycle and content management capabilities. It provides a durable interface that establishes authentication, identity, and a stable entry point for consumers. A **deployment** is a running instance of an agent version inside an application that can be started, stopped, and updated to reference new agent versions.

### Routing and version management

Each Agent Application acts as a routing table to specific agent deployments. Currently, an Agent Application supports one active deployment, directing 100% of the traffic received by the application’s endpoint to that deployment. When you publish a new agent version to an existing application, 100% of the traffic received by the application’s endpoint will be directed to the deployment referencing the new agent version.  

:::image type="content" source="../../media/publish-agent/agent-application-routing-diagram.png" alt-text="Diagram of an Agent Application routing traffic to a deployment running a specific agent version, showing a stable entry point and traffic flow.":::

## Invoke Agent Applications

An Agent Application resource exposes a stable endpoint with multiple protocol and authentication options. 

> [!NOTE]
> Currently, only one protocol — either Responses or Activity Protocol — can be enabled for an Agent Application at a time. This is a temporary limitation.

### Protocols

#### Responses protocol

Foundry agents by default expose an OpenAI-compatible protocol based around Responses for interacting with agents. 

For applications this is exposed at:

`https://{accountName}.services.ai.azure.com/api/projects/{projectName}/applications/{applicationName}/protocols/openai`

The behavior of the OpenAI API exposed through applications has been modified to allow user data isolation. It is more limited than the OpenAI API served by the project endpoint – applications currently remove any ability to provide inputs except through the create response call. Specifically: 
- Only the POST /responses API is currently available; all other APIs including /conversations, /files, /vector_stores, and /containers are inaccessible 
- The POST /responses call overrides store to false to prevent storing the response 

This means that for multi-turn conversations the conversation history must be stored by the client. 

#### Activity Protocol 
Foundry agents can also expose the [Activity Protocol](https://github.com/microsoft/Agents/blob/main/specs/activity/protocol-activity.md) used by Azure Bot Service. 

For applications this is exposed at:

`https://{accountName}.services.ai.azure.com/api/projects/{projectName}/applications/{applicationName}/protocols/activityprotocol`

### Authentication

You can configure inbound end-user authentication on the application. The following option is available:

- **Default (RBAC)**: The caller must have the Azure RBAC permission `/applications/invoke/action` on the application resource. 
- **Channels (Azure Bot Service)**: When you publish to M365/Teams or to A365 as a digital worker, channels is the authentication that is used. This is selected automatically in the UI through the M365/Teams publish flow.
<!--
- Channels (Azure Bot Service): Requests from a linked Azure Bot Service instance are permitted. This is used for M365 and Agent365 integration, and for scenarios where an upstream service interacts with the application through Activity Protocol. 
-->
API key authentication is not supported for agents through projects or through applications. 

## Publish an agent  

### Foundry portal

This section shows you how to publish an agent using the Foundry portal interface.

1. In the Agent Builder, create or select an agent version you want to publish.

2. Select **Publish Agent** to create an Agent Application and deployment.

3. Configure authentication for your Agent Application:

   - By default, the authentication type is set to RBAC (Role-Based Access Control)
   - Users calling the agent application using responses protocol must be granted the Azure AI User built-in Azure RBAC role or the permission `/applications/invoke/action`
   <!--
   - For Azure Bot Service integration (to support Microsoft 365/Microsoft 365 Copilot), requests from a linked Azure Bot Service instance are automatically permitted
    -->

4. Assign permissions for tool authentication:

   - If your agent includes tools that use agent identity for authentication, the newly created agent identity must have appropriate permissions
   - Navigate to each Azure resource your agent accesses and assign the required RBAC role to the new agent identity

5. After publishing, you can:
   
   - [Coming soon] Open app to chat with your published agent application and easily share it with others in the UI (Note: sharing the application automatically grants them the Azure AI User role on the Agent Application resource) 
   - Share the published endpoint with external consumers or integrate it into your existing application
   - Share and chat with your application in channels like Teams/M365 Copilot

### REST API
To publish an agent version you must create an application and deployment that reference your agent version.

> [!IMPORTANT]
> Agent Applications are Azure resources. Use the latest API version available for your subscription and account when calling the management endpoint.

#### 1. Create agent application. 

**Required**: Set the `agentName` field to the name of the agent you want to publish. 

The following example shows only the minimum required fields. By default `authorizationPolicy` is set to **Default (Azure RBAC)** and `trafficRoutingPolicy` routes all traffic to the first deployment.

```
PUT https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group}}/providers/Microsoft.CognitiveServices/accounts/{{account_name}}/projects/{{project_name}}/applications/{{application_name}}?api-version={{api_version}}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "properties":{
    "displayName": "niceapp",
    "agents": [{"agentName": "Publishing Agent"}]
  }
}
```

#### 2. Create an agent deployment. 

**Required**: Replace `agentName` and `agentVersion` with the agent version you want to publish.

For prompt and workflow agents:
```
PUT https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group}}/providers/Microsoft.CognitiveServices/accounts/{{account_name}}/projects/{{project_name}}/applications/{{application_name}}/agentdeployments/{{deployment_name}}?api-version={{api_version}}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "properties":{
    "displayName": "Test Managed Deployment",
    "deploymentType": "Managed",
    "protocols": [
        {
          "protocol": "responses",
          "version": "1.0"
        }
    ],
    "agents": [
        {
            "agentName": "Publishing Agent",
            "agentVersion": "1"
        }
    ]
  }
}    
```

For hosted agents:
```
PUT https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group}}/providers/Microsoft.CognitiveServices/accounts/{{account_name}}/projects/{{project_name}}/applications/default/agentdeployments/{{deployment_name2}}?api-version={{api_version}}
Authorization: Bearer {{token}}
Content-Type: application/json
{
  "properties": {
    "displayName": "Test Hosted Deployment",
    "deploymentType": "Hosted",
    "minReplicas": 1,
    "maxReplicas": 1,
    "protocols": [
        {
            "protocol": "responses",
            "version": "1.0"
        }
    ],
    "agents": [
        {
            "agentName": "ContainerAgent",
            "agentVersion": "1"
        }
    ]
  }
}
```

#### 3. Verify deployment is running

Prompt and workflow agent deployments start running automatically. Hosted agent deployments inherit the state of the published agent version — if the version is stopped, the deployment is also stopped. Use the following call to start a stopped deployment:
```
POST https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group}}/providers/Microsoft.CognitiveServices/accounts/{{account_name}}/projects/{{project_name}}/applications/{{application_name}}/agentDeployments/{{deployment_name}}/start?api-version={{api_version}}
Authorization: Bearer {{token}}
Content-Type: application/json

```


## Verify publishing succeeded

Confirm that your agent published successfully before sharing the endpoint with consumers. After you publish, verify that:

- The Agent Application resource exists.
- The deployment is running.
- You can invoke the application endpoint.

### Quick verification by calling the endpoint

1. Get an access token for the calling user.

  ```azurecli
  az account get-access-token --resource https://ai.azure.com
  ```

1. Call the Agent Application endpoint (Responses protocol).

  ```bash
  curl -X POST \
    "https://<foundry-resource-name>.services.ai.azure.com/api/projects/<project-name>/applications/<app-name>/protocols/openai/responses?api-version=2025-11-15-preview" \
    -H "Authorization: Bearer <access-token>" \
    -H "Content-Type: application/json" \
    -d '{"input":"Say hello"}'
  ```

If you receive `403 Forbidden`, confirm the caller has the Azure AI User role on the Agent Application resource.

## Update a published Agent Application

When you need to roll out a new version of your agent, update the existing application and deployment to reference the new agent version.

### Foundry portal
1. In the Agent Builder, navigate to the specific agent version you want to publish.

2. Select **Publish Updates**.

3. Confirm the update. The Agent Application automatically directs 100% of traffic to the new agent version.

The stable endpoint URL remains unchanged, ensuring downstream consumers aren't disrupted by the update.

### REST API
If your agent name remains the same and you only want to roll out a new agent version, update the deployment to reference a new agent version. 
```
PUT https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group}}/providers/Microsoft.CognitiveServices/accounts/{{account_name}}/projects/{{project_name}}/applications/{{application_name}}/agentdeployments/{{deployment_name}}?api-version={{api_version}}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "properties":{
    "description": "This is a managed deployment",
     "displayName": "Test Managed Deployment",
    "deploymentType": "Managed",
    "protocols": [
        {
          "protocol": "responses",
          "version": "1.0"
        }
    ],
    "agents": [
        {
            "agentName": "Publishing Agent",
            "agentVersion": "<updated-agent-version>"
        }
    ]
  }
}

```
To roll out an agent with a different name, you must:

1. Update the Agent Application to allow the new agent name.
1. Create or update a deployment to reference the new agent version.
1. If you created a new deployment, update the Agent Application's traffic routing policy so 100% of traffic goes to the new deployment.

> [!NOTE]
> Currently, all traffic must be routed to a single deployment.

## Consume your Agent Application

> [!NOTE]
> Agent applications currently support one protocol at a time, but this can be changed. When you create an Agent Application in the Foundry UI, it defaults to the Responses API protocol. If you later publish to Microsoft 365 or Teams, the protocol is automatically updated to the Activity Protocol.

After publishing, you invoke your agent through its endpoint using either the Responses API protocol or the Activity Protocol. The activity protocol applies when your agent is published to Microsoft 365 and Teams.

For step-by-step instructions for consuming your Agent Application using the Responses API protocol, see [Invoke your Agent Application using the Responses API protocol](./publish-responses.md)

For step-by-step instructions for distributing your agent to Microsoft 365 and Teams or as a digital worker in Agent 365, see [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md).

## Security and privacy considerations

- Use least privilege. Grant users the minimum role they need (for example, separate publish permissions from invoke permissions).
- Avoid sharing project access when you only need to share an agent. Use the Agent Application endpoint and RBAC on the application resource.
- Don’t embed access tokens in source code, scripts, or client applications. Use Microsoft Entra authentication flows appropriate for your app.
- Plan for identity changes when you publish. Tool calls authenticated by agent identity use the application identity after publishing, not the project identity.
- Store conversation history in your client if you need multi-turn experiences. Agent Applications currently restrict APIs and don’t store responses.

## Limitations

**Note**: All of these limitations are temporary and fixes are already in progress.

Agents published as Agent Applications have the following limitations:

| Limitation | Description |
| --- | --- |
| Entra Agent Registry visibility | There is a bug where published agents don't appear in the Entra Agent Registry (EAR). Fix in progress and we will backfill existing published agents as well. |
| No UI or CLI management | There's no user interface or command-line interface for managing published agents. Use the REST API for management operations. |


## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| **Publish Agent** is disabled | Missing Azure AI Project Manager role on the project scope | Confirm you have the required role assignment on the Foundry project. |
| `403 Forbidden` when invoking the endpoint | Caller lacks invoke permissions on the Agent Application resource | Assign the Azure AI User role on the Agent Application resource to the caller. |
| `401 Unauthorized` when invoking the endpoint | The access token is missing, expired, or for the wrong resource | Re-authenticate and request a token for `https://ai.azure.com`. |
| Tool calls fail after publishing | The Agent Application identity doesn’t have the same access as the project identity | Reassign the required RBAC roles to the published agent identity for any downstream Azure resources it must access. |
| Multi-turn conversations don’t work as expected | Agent Applications don’t store conversation state for you | Store conversation history in your client and send the context as part of your request. |

## Clean up resources

If you no longer need a published endpoint, delete the Agent Application Azure resource (and its deployments). Deleting the application doesn’t delete your agent versions in the Foundry project.

## Reference: Agent Application and deployment properties

Use the following tables when you construct REST API requests or need to understand the fields returned in responses.

<br>

<details>

<summary>Agent Application properties</summary>

| Name | Description | Value | Can be specified in request body? |
| --- | --- | --- | --- |
| `displayName` | The display name of the agent application | string | ✅ |
| `baseUrl` | The agent application's dedicated endpoint | string | ❌ (read only) |
| `agents` | The agents exposed by the application. | array of objects | ✅ |
| `agentIdentityBlueprint` | The agent identity blueprint associated with the agent application. | object | ❌ (read only) |
| `defaultInstanceIdentity` | The agent identity associated with the agent application | object | ❌ (read only) |
| `authorizationPolicy` | Defines how users are allowed to auth to the app. If not specified, this is set by default | object | ✅ |
| `trafficRoutingPolicy` | Defines what deployment the agent sends traffic to. Currently, all traffic can only be routed to one deployment. | object | ✅ |
| `provisioningState` | Gets the status of the agent application at the time the operation was called. | string | ❌ (read only) |
| `isEnabled` | Specifies whether an agent application is enabled or disabled. | boolean | ✅ |

</details>

<details>
<summary>Deployment properties</summary>

| Name | Description | Value | Can be specified in request body? |
| --- | --- | --- | --- |
| `displayName` | The display name of the deployment. | string | ✅ |
| `deploymentId` | This is a system-generated unique identifier for each distinct lifetime of a deployment with a given resource identifier. | string | ❌ (read only) |
| `state` | The state of the deployment. | enum (`Starting`, `Running`, `Stopping`, `Failed`, `Deleting`, `Deleted`, `Updating`) | ❌ (read only) there are explicit APIs like start/stop to control state |
| `protocols` | The protocols supported by the deployment | array of objects | ✅ |
| `agents` | The agent version attached to a specific deployment. | array of objects | ✅ |
| `provisioningState` | Gets the status of the deployment at the time the operation was called. | enum (`Succeeded`, `Failed`, `Canceled`, `Creating`, `Updating`, `Deleting`) | ❌ (read only) |
| `deploymentType` | The type of agent attached to the deployment | Enum (`Hosted` or `Managed`) | ✅ |
| `minReplicas` | The minimum number of replicas that are always running. | integer | ✅ (only when deploymentType: `Hosted`) |
| `maxReplicas` | The maximum number of replicas that can be running. | integer | ✅ (only when deploymentType: `Hosted`) |

</details>

## Related content

- Learn about [Agent identity concepts in Foundry](../concepts/agent-identity.md)
- Learn about [Hosted agents](../concepts/hosted-agents.md)
- Learn how to [publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md)

## Next steps

> [!div class="nextstepaction"]
> [Manage agents at scale](../../control-plane/how-to-manage-agents.md)

> [!div class="nextstepaction"]
> [Prepare your development environment](../../../how-to/develop/install-cli-sdk.md)

> [!div class="nextstepaction"]
> [Get started with the SDK](../../../quickstarts/get-started-code.md)

