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

Publishing promotes an agent from a development asset into a managed Azure resource with a dedicated endpoint, independent identity, and governance capabilities. This article shows you how to publish an agent, configure its authentication and permissions, update published versions, and consume the agent through its stable endpoint. 

When you publish an agent, Microsoft Foundry creates an Agent Application resource with a dedicated invocation URL and its own Microsoft Entra agent identity blueprint and agent identity. A deployment is created under the application that references your agent version and registers it in the [Entra Agent Registry](/entra/agent-id/identity-platform/what-is-agent-registry) for discovery and governance.

Publishing enables you to share agents with teammates, your organization, or customers without granting access to your Foundry project or source code. The stable endpoint remains consistent as you iterate and deploy new agent versions. 

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md) with at least one agent version created
- [Azure AI Project Manager role](../../../concepts/rbac-foundry.md) on the Foundry project scope to publish agents
- [Azure AI User role](../../../concepts/rbac-foundry.md) on the Agent Application scope to chat with a published agent
- Familiarity with [Azure role-based access control (RBAC)](/azure/role-based-access-control/overview) for permission configuration
- Familiarity with [Agent identity concepts in Foundry](../concepts/agent-identity.md)
- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../../../how-to/develop/install-cli-sdk.md)

[!INCLUDE [code-preview](../../includes/code-preview.md)]

## When to use agent applications
Anyone with the AI User role on a Foundry project can interact with all the agents it contains with conversations and state shared between all users. This is appropriate for development tasks like authoring, debugging, and testing agents, but it’s not typically suitable for distribution of an agent to non-developers. 

Applications address the needs of broader agent distribution by providing a stable endpoint, unique Agent Identity with audit trails, cross-team sharing capabilities, integration with Entra Agent Registry, user data isolation, and the ability to preview the agent as a web application. 

Creating an application for an agent enables: 
- **External sharing**: You can provide access to teammates or customers who shouldn't have access to your Foundry project 
- **SaaS-like behavior**: The application has a stable endpoint so that you can update the application with new versions within Foundry without requiring downstream consumers to make changes 
- **Distinct identity**: The agent has its own identity, RBAC rules, and audit trail separate from the project-level default identity 
- **User data isolation**: The inputs and interactions one user has with the agent aren’t available to any other users by default 
- **Azure Policy integration**: As an ARM resource the application can be governed by Azure Policy 
<!--
It’s also a prerequisite for: 
- **M365 publishing**: Distributing your agent through Teams and Microsoft 365 Copilot 
- **Agent365 digital workers**: Distributing your agent as a digital worker that can interact through Teams, email, and M365 applications. 
-->
## Understand agent applications and deployments

Before publishing, it's important to understand the relationship between projects, agent versions, applications, and deployments.

:::image type="content" source="../../media/publish-agent/azure-agent-identity-overview.png" alt-text="Diagram illustrating how Foundry projects organize agent versions, applications, and deployments, highlighting governance and RBAC roles.":::

A Foundry **project** is a work organization concept that groups related resources such as agents, files, and indexes. An **agent** represents a composable unit — defined by its instructions, model, and tools. An **agent version** captures a specific immutable snapshot of an agent. Every time you make changes to your agent, such as updating the prompt or adding tools, a new agent version is created. When you create an agent version, it's exposed under the project where developers with project access can create, run, and test it.

An **Agent Application** projects one or more agents as a service — independently addressable, governable, and equipped with lifecycle and content management capabilities. It provides a durable interface that establishes authentication, identity, and a stable entry point for consumers. A **deployment** is a running instance of an agent version inside an application that can be started, stopped, and updated to reference new agent versions.

During development, all unpublished agents in a project share a default Agent Identity. Once published, an agent receives its own Agent Identity and becomes a nested Azure resource visible in the Azure portal, enabling independent governance and RBAC configuration.

### Routing and version management

Each Agent Application acts as a routing table to specific agent deployments. Currently, an Agent Application supports one active deployment, directing 100% of the traffic received by the application’s endpoint to that deployment. When you publish a new agent version to an existing application, 100% of the traffic received by the application’s endpoint will be directed to the deployment referencing the new agent version.  

:::image type="content" source="../../media/publish-agent/agent-application-routing-diagram.png" alt-text="Diagram of an Agent Application routing traffic to a deployment running a specific agent version, showing a stable entry point and traffic flow.":::

### Anatomy of an Agent Application and deployment

#### Agent Application properties

| Name | Description | Value | Can be specified in request body? |
| --- | --- | --- | --- |
| `displayName` | The display name of the agent application | string | ✅ |
| `baseUrl` | The agent application’s dedicated endpoint | string | ❌ (read only) |
| `agents` | The agents exposed by the application. | array of objects | ✅ |
| `agentIdentityBlueprint` | The agent identity blueprint associated with the agent application. | object | ❌ (read only) |
| `defaultInstanceIdentity` | The agent identity associated with the agent application | object | ❌ (read only) |
| `authorizationPolicy` | Defines how users are allowed to auth to the app. If not specified, this is set by default | object | ✅ |
| `trafficRoutingPolicy` | Defines what deployment the agent sends traffic to. Currently, all traffic can only be routed to one deployment. | object | ✅ |
| `provisioningState` | Gets the status of the agent application at the time the operation was called. | string | ❌ (read only) |
| `isEnabled` | Specifies whether an agent application is enabled or disabled. | boolean | ✅ |

#### Deployment properties

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

## Invoke agent applications

An Agent Application resource exposes a stable endpoint with multiple protocol and authentication options. 

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
<!--
- Channels (Azure Bot Service): Requests from a linked Azure Bot Service instance are permitted. This is used for M365 and Agent365 integration, and for scenarios where an upstream service interacts with the application through Activity Protocol. 
-->
API key authentication is not supported for agents through projects or through applications. 

## Publish an agent  

When you publish an agent, it receives its own Agent Identity separate from the project's shared identity. Tools that use agentic identity authentication run under the project identity before publishing and under the application identity after publishing. Because permissions don't transfer automatically, you must reassign the necessary RBAC roles to the new application identity.

### Foundry portal

This section shows you how to publish an agent using the Foundry portal interface.

1. In the Agent Builder, create or select an agent version you want to publish.

2. Select **Publish Agent** to create an Agent Application and deployment.

3. Configure authentication for your Agent Application:

   - By default, the authentication type is set to RBAC (Role-Based Access Control)
   - End users calling the agent must have Azure RBAC permissions on the application resource
   <!--
   - For Azure Bot Service integration (to support Microsoft 365/Microsoft 365 Copilot), requests from a linked Azure Bot Service instance are automatically permitted
    -->

4. Assign permissions for tool authentication:

   - If your agent includes tools that use Agent Identity for authentication, the newly created Agent Identity must have appropriate permissions
   - Navigate to each Azure resource your agent accesses and assign the required RBAC role to the new Agent Identity
   - The shared development identity permissions don't carry over—you must reconfigure permissions for the published agent's identity

5. After publishing, you can:
   
   - Open app to chat with your published agent application and easily share it with others in the UI (Note: sharing the application automatically grants them the Azure AI User role on the Agent Application resource) 
   <!-- - Publish it to Teams and Microsoft 365 Copilot -->
   - Share the published endpoint with external consumers

### REST API
To publish an agent version you must create an application and deployment that reference your agent version.

> [!IMPORTANT]
> Agent Applications are Azure resources. Use the latest API version available for your subscription and account when calling the management endpoint.

1. Create agent application. Update agentName field to the name of the agent you want to publish. 
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

2. Create a deployment. Replace agentName and agentVersion with the agent version you want to publish.

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

## Update a published agent application

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

## Consume your published Agent Application

After publishing, you invoke your agent through its endpoint using the responses protocol. Using the OpenAI-compatible API with Agent Applications provides a familiar interface while leveraging Microsoft Foundry's enterprise capabilities including authentication, governance, and user data isolation.

### Prerequisites for consuming Agent Applications

Before running the code sample, ensure you have:

- Python 3.8 or later installed
- [Azure CLI](/cli/azure/install-azure-cli) installed and configured
- Required Python packages installed:
  ```bash
  pip install openai azure-identity
  ```
- Authenticated to Azure CLI:
  ```bash
  az login
  ```
- Azure AI User role on the Agent Application resource you want to invoke

For more details on setting up your development environment, see [Prepare your development environment](../../../how-to/develop/install-cli-sdk.md).

### Use OpenAI client with Agent Applications endpoint

```python
# filepath: Direct OpenAI compatible approach
from openai import OpenAI 
from azure.identity import DefaultAzureCredential, get_bearer_token_provider 

# edit base_url with your <foundry-resource-name>, <project-name>, and <app-name>
openai = OpenAI(
    api_key=get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default"),
    base_url="https://<foundry-resource-name>.services.ai.azure.com/api/projects/<project-name>/applications/<app-name>/protocols/openai",
    default_query = {"api-version": "2025-11-15-preview"}
)

response = openai.responses.create( 
  input="Write a haiku", 
) 
print(f"Response output: {response.output_text}")
```
This approach authenticates using Azure credentials and requires the caller to have the Azure AI User role on the Agent Application resource.

## Security and privacy considerations

- Use least privilege. Grant users the minimum role they need (for example, separate publish permissions from invoke permissions).
- Avoid sharing project access when you only need to share an agent. Use the Agent Application endpoint and RBAC on the application resource.
- Don’t embed access tokens in source code, scripts, or client applications. Use Microsoft Entra authentication flows appropriate for your app.
- Plan for identity changes when you publish. Tool calls authenticated by agent identity use the application identity after publishing, not the project identity.
- Store conversation history in your client if you need multi-turn experiences. Agent Applications currently restrict APIs and don’t store responses.

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

