---
title: Hosted agents in Foundry Agent Service (preview)
description: Deploy and manage containerized agents on Foundry Agent Service (preview) with managed hosting, scaling, and observability.
titleSuffix: Microsoft Foundry
author: aahill
ms.author: aahi
ms.date: 02/03/2026
ms.manager: nitinme
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: references_regions, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# What are hosted agents?

When you build agentic applications by using open-source frameworks, you typically manage containerization, web server setup, security integration, memory persistence, infrastructure scaling, data transmission, instrumentation, and version rollbacks. These tasks become even more challenging in heterogeneous cloud environments.

> [!IMPORTANT]
> Hosted agents are currently in **public preview**. See [Limits, pricing, and availability (preview)](#limits-pricing-and-availability-preview) for current constraints.

Hosted agents in Foundry Agent Service solve these challenges for Microsoft Foundry users. By using this managed platform, you can deploy and operate AI agents securely and at scale. You can use your custom agent code or a preferred agent framework with streamlined deployment and management.

## Prerequisites

- A [Microsoft Foundry project](../../../how-to/create-projects.md)
- Basic understanding of [containerization and Docker](/azure/container-instances/container-instances-overview)
- Familiarity with [Azure Container Registry](/azure/container-registry/container-registry-intro)
- Knowledge of your preferred agent framework (LangGraph, Microsoft Agent Framework, or custom code)

## At a glance

Hosted agents let you bring your own agent code and run it as a managed containerized service.

Use this article to:

- Understand what hosted agents are and when to use them.
- Package and test your agent locally before deployment.
- Create, manage, publish, and monitor hosted agents.

If you want to jump to a task, see:

- [Package code and test locally](#package-code-and-test-locally)
- [Create a hosted agent](#create-a-hosted-agent)
- [Manage hosted agents](#manage-hosted-agents)
- [Publish hosted agents to channels](#publish-hosted-agents-to-channels)
- [Troubleshoot hosted agent endpoints](#troubleshoot-hosted-agent-endpoints)

## Limits, pricing, and availability (preview)

Hosted agents are currently in preview.

- **Private networking support**: You can't create hosted agents by using the standard setup for network isolation within network-isolated Foundry resources. For details, see [Configure virtual networks](../../../agents/how-to/virtual-networks.md).
- **Preview limits**: For the full list of preview limits, see [Limitations during preview](#limitations-during-preview).
- **Pricing**: For updates on pricing, see the Foundry [pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

### Region availability

Hosted Agents are supported in the following regions: 

- Brazil South	
- Canada East	
- East US	
- France Central	
- Germany West Central	
- Italy North	
- North Central US	
- South Africa North	
- South Central US	
- South India	
- Spain Central	
- Sweden Central	
- Canada Central	
- Korea Central	
- Southeast Asia	
- Australia East	
- East US 2	
- Japan East	
- UAE North	
- UK South	
- West US	
- West US 3	
- Norway East	
- Poland Central	
- Switzerland North

## Security and data handling

Treat a hosted agent like production application code.

- **Don't put secrets in container images or environment variables**. Use managed identities and connections, and store secrets in a managed secret store. For guidance, see [Set up a Key Vault connection](../../../how-to/set-up-key-vault-connection.md).
- **Be careful with non-Microsoft tools and servers**. If your agent calls tools backed by non-Microsoft services, some data might flow to those services. Review data sharing, retention, and location policies for any non-Microsoft service you connect.

## Understand key concepts

### Hosted agents

Hosted agents are containerized agentic AI applications that run on Agent Service. Unlike prompt-based agents, developers build hosted agents through code and deploy them as container images on Microsoft-managed pay-as-you-go infrastructure.

Hosted agents follow a standard lifecycle: create, start, update, stop, and delete. Each phase provides specific capabilities and status transitions to help you manage your agent deployments effectively.

> [!NOTE]
> Hosted agents are currently in preview. For current constraints and availability, see [Limits, pricing, and availability (preview)](#limits-pricing-and-availability-preview).

### Hosting adapter

The hosting adapter is a framework abstraction layer that helps expose supported agent frameworks (or your custom code) as an HTTP service for local testing and hosted deployments.

The hosting adapter provides several key benefits for developers:

**Simplified local testing**: Run your agent locally and validate the HTTP surface area before you containerize and deploy.

**Automatic protocol translation**: The adapter handles all complex conversions between the Foundry request and response formats and your agent framework's native data structures. These activities include:

- Conversation management
- Message serialization
- Streaming event generation

**Observability integration**: Export traces, metrics, and logs by using OpenTelemetry.

**Seamless Foundry integration**: Your locally developed agents work with the Foundry Responses API, conversation management, and authentication flows.

### Managed service capabilities

Agent Service handles:

- Provisioning and autoscaling of agents
- Conversation orchestration and state management
- Identity management
- Integration with Foundry tools and models
- Built-in observability and evaluation capabilities
- Enterprise-grade security, compliance, and governance

> [!IMPORTANT]
> If you use Agent Service to host agents that interact with non-Microsoft servers or agents, you take on the risk. Review all data that you share with non-Microsoft servers or agents. Be aware of non-Microsoft practices for retention and location of data. You're responsible for managing whether your data flows outside your organization's Azure compliance and geographic boundaries, along with any related implications.

### Framework and language support

| Framework | Python | C# |
| --------- | ------ | -- |
| Microsoft Agent Framework | ✅ | ✅ |
| LangGraph | ✅ | ❌ |
| Custom code | ✅ | ✅ |

### Public adapter packages

- Python: `azure-ai-agentserver-core`, `azure-ai-agentserver-agentframework`, `azure-ai-agentserver-langgraph`
- .NET: `Azure.AI.AgentServer.Core`, `Azure.AI.AgentServer.AgentFramework`

## Package code and test locally

Before you deploy to Microsoft Foundry, build and test your agent locally:

1. **Run your agent locally**: Use the hosting adapter to `azure-ai-agentserver-*` package to wrap your agent code and start a local web server that automatically exposes your agent as a REST API.
2. **Test by using REST calls**: The local server runs on `localhost:8088` and accepts standard HTTP requests.
3. **Build the container image**: Create a container image from your source code. 
4. **Use the Azure Developer CLI**: Use `azd` to streamline the packaging and deployment process.

### Wrap your agent code with the hosting adapter and test locally

**Sample agent authored using Microsoft Agent Framework**

```python

import os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv(override=True)

from agent_framework import ai_function, ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.identity import DefaultAzureCredential

# Configure these for your Azure AI Foundry project
PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")  # e.g., "https://<resource>.services.ai.azure.com/api/projects/<project>"
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1")  # Your model deployment name


@ai_function
def get_local_date_time(iana_timezone: str) -> str:
    """
    Get the current date and time for a given timezone.
    
    This is a LOCAL Python function that runs on the server - demonstrating how code-based agents
    can execute custom logic that prompt agents cannot access.
    
    Args:
        iana_timezone: The IANA timezone string (e.g., "America/Los_Angeles", "America/New_York", "Europe/London")
    
    Returns:
        The current date and time in the specified timezone.
    """
    try:
        tz = ZoneInfo(iana_timezone)
        current_time = datetime.now(tz)
        return f"The current date and time in {iana_timezone} is {current_time.strftime('%A, %B %d, %Y at %I:%M %p %Z')}"
    except Exception as e:
        return f"Error: Unable to get time for timezone '{iana_timezone}'. {str(e)}"


# Create the agent with a local Python tool
agent = ChatAgent(
    chat_client=AzureAIAgentClient(
        project_endpoint=PROJECT_ENDPOINT,
        model_deployment_name=MODEL_DEPLOYMENT_NAME,
        credential=DefaultAzureCredential(),
    ),
    instructions="You are a helpful assistant that can tell users the current date and time in any location. When a user asks about the time in a city or location, use the get_local_date_time tool with the appropriate IANA timezone string for that location.",
    tools=[get_local_date_time],
)

if __name__ == "__main__":
    from_agent_framework(agent).run()
```

Refer to the [samples repo](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agent) for code samples in LangGraph and custom code. 

When you run your agent locally by using the hosting adapter, it automatically starts a web server on `localhost:8088`. You can test your agent by using any REST client.

```http
@baseUrl = http://localhost:8088

POST {{baseUrl}}/responses
Content-Type: application/json
 
{
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "Where is Seattle?"
            }
        ]
    }
}
```

This local testing approach lets you:

- Validate agent behavior before containerization.
- Debug issues in your development environment.
- Test different input scenarios quickly.
- Verify API compatibility with the Foundry Responses API.

## Create a hosted agent

### Create a hosted agent using VS Code Foundry extension

You can use the [Foundry extension for Visual Studio Code](../../agents/how-to/vs-code-agents-workflow-pro-code.md?view=foundry&preserve-view=true) to create hosted agents.

### Create a hosted agent by using the Azure Developer CLI

Developers can use the Azure Developer CLI `ai agent` extension for seamless and rapid provisioning and deployment of their agentic applications on Microsoft Foundry.

This extension simplifies the setup of Foundry resources, models, tools, and knowledge resources. For example, it simplifies the setup of Azure Container Registry for bringing your own container, Application Insights for logging and monitoring, a managed identity, and role-based access control (RBAC). In other words, it provides everything you need to get started with hosted agents in Foundry Agent Service.

This extension is currently in preview. Don't use it for production.

To get started:

1. Install the Azure Developer CLI on your device.

   If you already have the Azure Developer CLI installed, check if you have the latest version of `azd` installed:

    ```bash
    azd version
    ```

    To upgrade to the latest version, see [Install or update the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd).

2. If you're starting with no existing Foundry resources and you want to simplify all the required infrastructure provisioning and RBAC, download the Foundry starter template. The template automatically installs the `ai agent` extension. When prompted, you can provide an environment name which creates a resource group named `rg-<name-you-provide>`.

    ```bash
    azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
    ```

    To check all installed extensions:

    ```bash
    azd ext list
    ```

    Make sure you have the latest version of the Foundry `azd` agent extension installed.

    If you have an existing Foundry project where you want to deploy your agent, and you want to provision only the additional resources that you might need for deploying your agent, run this command afterward:

    ```bash
    azd ai agent init --project-id /subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/projects/[PROJECTNAME]
    ```

3. Initialize the template by configuring the parameters in the agent definition:

    ```bash
    azd ai agent init -m <repo-path-to-agent.yaml>
    ```

    The GitHub repo for an agent that you want to host on Foundry contains the application code, referenced dependencies, Dockerfile for containerization, and the `agent.yaml` file that contains your agent's definition. To configure your agent, set values for the parameters that you're prompted for. This action registers your agent under `Services` in `azure.yaml` for the downloaded template. You can get started with samples on [GitHub](https://github.com/azure-ai-foundry/foundry-samples).

4. To open and view all Bicep and configuration files associated with your `azd`-based deployments, use this command:

    ```bash
    code .
    ```

5. Package, provision, and deploy your agent code as a managed application on Foundry:

    ```bash
    azd up
    ```

    This command abstracts the underlying execution of the commands `azd infra generate`, `azd provision`, and `azd deploy`. It also creates a hosted agent version and deployment on Foundry Agent Service. If you already have a version of a hosted agent, `azd` creates a new version of the same agent. For more information, see the [Azure CLI documentation](/azure/developer/azure-developer-cli/extensions/azure-ai-foundry-extension).
    
To learn more about how you can do non-versioned updates, along with starting, stopping, and deleting your hosted agent deployments and versions, see the [management section](#manage-hosted-agents) of this article. 

Make sure you have RBAC enabled so that `azd` can provision the services and models for you. For Foundry role guidance, see [Role-based access control in Foundry portal](../../../concepts/rbac-foundry.md). For Azure built-in roles, see [Azure built-in roles](/azure/role-based-access-control/built-in-roles).

### Roles and permissions

* If you have an existing Foundry resource and need to create a new Foundry project to deploy a hosted agent, you need **Azure AI Owner** roles.

* If you have an existing project and want to create the model deployment and container registry in the project, you need **Azure AI Owner**  role on Foundry in addition to the **Contributor** role on the Azure subscription.

* If you have everything configured in the project to deploy a hosted agent, you need **Reader** on the Foundry account and **Azure AI User** on the project. 

Refer to [this article](../../../concepts/authentication-authorization-foundry.md#built-in-roles-overview) to learn more about built-in roles in Foundry.

### Resource cleanup

To prevent unnecessary charges, clean up your Azure resources after you complete your work with the application.

When to clean up:

- After you finish testing or demonstrating the application.
- When the application is no longer needed or you transition to a different project or environment.
- When you complete development and are ready to decommission the application.

To delete all associated resources and shut down the application, run the following command:

```bash
azd down
```

This process might take up to 20 minutes to complete.

## Create a hosted agent by using the Foundry SDK

When you create a hosted agent, the system registers the agent definition in Microsoft Foundry and tries to create a deployment for that agent version.

### Prerequisites for deployment

Before you deploy a hosted agent, make sure that you have:

- A container image hosted in [Azure Container Registry](https://azure.microsoft.com/services/container-registry/).
- For more information, see [Create a private container registry](/azure/container-registry/container-registry-get-started-portal).
- Access to assign roles in Azure Container Registry. You need at least User Access Administrator or Owner permissions on the container registry.
- The Azure AI Projects SDK installed.

  ```bash
  pip install azure-ai-projects
  ```

### Build and push your Docker image to Azure Container Registry

To build your agent as a Docker container and upload it to Azure Container Registry:

1. Build your Docker image locally:

    ```bash
    docker build -t myagent:v1 .
    ```
    Refer to sample Dockerfile for [Python](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/agents-in-workflow/Dockerfile) and [C#](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/csharp/hosted-agents/AgentsInWorkflows/Dockerfile).
   
1. Sign in to Azure Container Registry:

   ```bash
   az acr login --name myregistry
   ```

1. Tag your image for the registry:

   ```bash
   docker tag myagent:v1 myregistry.azurecr.io/myagent:v1
   ```

1. Push the image to Azure Container Registry:

   ```bash
   docker push myregistry.azurecr.io/myagent:v1
   ```

For detailed guidance on working with Docker images in Azure Container Registry, see [Push and pull Docker images](/azure/container-registry/container-registry-get-started-docker-cli).

### Configure Azure Container Registry permissions

Before you create the agent, give your project's managed identity access to pull from the container registry that houses your image. This step ensures that all dependencies are available within the container.

1. In the [Azure portal](https://portal.azure.com), go to your Foundry project resource.

2. On the left pane, select **Identity**.

3. Under **System assigned**, copy the **Object (principal) ID** value. This value is the managed identity that you'll assign the Azure Container Instances role to.

4. Grant pull permissions by assigning the Container Registry Repository Reader role to your project's managed identity on the container registry. For detailed steps, see [Azure Container Registry roles and permissions](/azure/container-registry/container-registry-roles).

### Create an account-level capability host

Hosted agents require an account-level capability host with public hosting enabled.

Updating capability hosts isn't supported. If you already have a capability host for your Microsoft Foundry account, delete it and recreate it with `enablePublicHostingEnvironment` set to `true`.

Use `az rest` so you don't have to manage tokens manually.

#### Azure CLI (bash)

```bash
az rest --method put \
    --url "https://management.azure.com/subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/capabilityHosts/accountcaphost?api-version=2025-10-01-preview" \
    --headers "content-type=application/json" \
    --body '{
        "properties": {
            "capabilityHostKind": "Agents",
            "enablePublicHostingEnvironment": true
        }
    }'
```

#### Azure CLI (PowerShell)

```powershell
az rest --method put `
    --url "https://management.azure.com/subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/capabilityHosts/accountcaphost?api-version=2025-10-01-preview" `
    --headers "content-type=application/json" `
    --body '{
        "properties": {
            "capabilityHostKind": "Agents",
            "enablePublicHostingEnvironment": true
        }
    }'
```

### Create the hosted agent version

Install version>=2.0.0b3 of the Azure AI Projects SDK. Python 3.10 or later is required.

```bash
pip install --pre "azure-ai-projects>=2.0.0b3"
```

Use the Azure AI Projects SDK to create and register your agent:

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition, ProtocolVersionRecord, AgentProtocol
from azure.identity import DefaultAzureCredential

# Initialize the client
client = AIProjectClient(
    endpoint="https://your-project.services.ai.azure.com/api/projects/project-name",
    credential=DefaultAzureCredential()
)

# Create the agent from a container image
agent = client.agents.create_version(
    agent_name="my-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="your-registry.azurecr.io/your-image:tag",
        environment_variables={
            "AZURE_AI_PROJECT_ENDPOINT": "https://your-project.services.ai.azure.com/api/projects/project-name",
            "MODEL_NAME": "gpt-4",
            "CUSTOM_SETTING": "value"
        }
    )
)

# Print confirmation
print(f"Agent created: {agent.name} (id: {agent.id}, version: {agent.version})")
```

Expected output:

```output
Agent created: my-agent (id: agent_abc123, version: 1)
```

Here are the key parameters:

- `PROJECT_ENDPOINT`: Endpoint URL for your Foundry project.
- `AGENT_NAME`: Unique name for your agent.
- `CONTAINER_IMAGE`: Full Azure Container Registry image URL with tag.
- `CPU/Memory`: Resource allocation (for example, `1` for CPU, `2Gi` for memory).

> [!NOTE]
>
> - Ensure that your container image is accessible from the Foundry project.
> - `DefaultAzureCredential` handles authentication automatically.

---

The agent appears in the Foundry portal after you create it.

## Manage hosted agents

### Update an agent

You can update an agent in two ways: versioned updates and non-versioned updates.

#### Versioned update

Use a versioned update to modify the runtime configuration for your agent. This process creates a new version of the agent.

Changes that trigger a new version include:

- **Container image**: Updating to a new image or tag.
- **Resource allocation**: Changing CPU or memory settings.
- **Environment variables**: Adding, removing, or modifying environment variables.
- **Protocol versions**: Updating supported protocol versions.

To create a new version, use the same `client.agents.create_version()` method shown in the creation example with your updated configuration.

#### Non-versioned update

Use a non-versioned update to modify horizontal scale configuration (minimum and maximum replicas) or agent metadata such as description and tags. This process doesn't create a new version.

```bash
az cognitiveservices agent update
```

The arguments for this command include:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--account-name -a` | ✅ | Foundry Tools account name. |
| `--agent-version` | ✅ | Foundry Tools hosted agent version. |
| `--name -n` | ✅ | Foundry Tools hosted agent name. |
| `--project-name` | ✅ | AI project name. |
| `--description` | ❌ | Description of the agent. |
| `--max-replicas` | ❌ | Maximum number of replicas for horizontal scaling. |
| `--min-replicas` | ❌ | Minimum number of replicas for horizontal scaling. |
| `--tags` | ❌ | Space-separated tags: `key[=value] [key[=value] ...]`. Use two single quotation marks (`''`) to clear existing tags. |

Here's an example:

```bash
az cognitiveservices agent update --account-name myAccount --project-name myProject --name myAgent --agent-version 1 --min-replicas 1 --max-replicas 2
```

### Start an agent deployment

After you create your hosted agent version, start the deployment by using the `az` CLI extension to make it available for requests. You can also start a hosted agent that you previously stopped.

```bash
az cognitiveservices agent start
```

The arguments for this command include:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--agent-version` | ✅ | Foundry Tools hosted agent version |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |
| `--min-replicas` | ❌ | Minimum number of replicas for horizontal scaling |
| `--max-replicas` | ❌ | Maximum number of replicas for horizontal scaling |

If you don't specify max and min replicas during agent start operation, the default value is 1 for both the arguments. 

Here's an example:

```bash
az cognitiveservices agent start --account-name myAccount --project-name myProject --name myAgent --agent-version 1
```

When you start an agent:

- Current status: **Stopped**
- Allowed operation: **Start**
- Transitory status: **Starting**
- Final status: **Started** (if successful) or **Failed** (if unsuccessful)

### View container Log Stream

The container Logstream API for hosted agents gives you access to the system and console logs of the container deployed on your behalf in Microsoft's Azure environment to enable self-serve debugging for agent startup and runtime errors during deployment. 

#### REST API Details

| Item | Value |
| --- | --- |
| **Method** | `GET` |
| **Route** | `https://{endpoint}/api/projects/{projectName}/agents/{agentName}/versions/{agentVersion}/containers/default:logstream` |
| **Description** | Streams console or system logs for a specific hosted agent replica. |
| **Content-Type** | `text/plain` (chunked streaming) |

#### Path parameters

| Name | Description | Example |
| --- | --- | --- |
|  `api-version` | Required | API version, for example: `2025-11-15-preview` |
| `kind` | `console` | `console` returns container `stdout`/`stderr`, `system` returns container system event stream. |
| `endpoint` | Your Foundry service endpoint | `myservice.services.ai.azure.com` |
| `projectName` | The Foundry project name | `myproject` |
| `agentName` | The agent deployment name | `sample1` |
| `agentVersion` | The agent version number | `1` |

#### Query parameters

| Name | Default | Notes |
| --- | --- | --- |
| `kind` | `console` | `console` returns container stdout/stderr, `system` returns container app event stream. |
| `replica_name` | empty | When omitted, the server chooses the first replica for console logs. Required to target a specific replica. |
| `tail` | `20` | Number of trailing lines returned. Enforced to `1-300`. |

#### Timeout Settings

- Max Connection Duration: The maximum duration for a log stream connection is `10 minutes`. After this period, the server will automatically close the client connection.
- Idle Timeout: This timeout is set to `1 minute`. It applies when there is no response from the client, or if there is no activity after the previous response during the log stream. If the connection remains idle for 1 minute, it will be closed by the server.

#### Response status codes

- `200 OK`: Plain-text stream of log lines, one per line.
- `404 Not Found`: Agent version, replica, or container log endpoint was not found.
- `401/403`: Caller lacks authorization.
- `5xx`: Propagated from downstream container calls when details or tokens cannot be fetched.

#### Example: Fetch logs using curl

```bash
curl -N "https://{endpoint}/api/projects/{projectName}/agents/{agentName}/versions/{agentVersion}/containers/default:logstream?kind=console&tail=500&api-version=2025-11-15-preview" \
  -H "Authorization: Bearer $(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)"
```

**Flags:**
- `-N` disables output buffering (important for streaming logs in real-time)

#### Response samples

#### 200 OK (console logs)

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Transfer-Encoding: chunked

2025-12-15T08:43:48.72656  Connecting to the container 'agent-container'...
2025-12-15T08:43:48.75451  Successfully Connected to container: 'agent-container' [Revision: 'je90fe655aa742ef9a188b9fd14d6764--7tca06b', Replica: 'je90fe655aa742ef9a188b9fd14d6764--7tca06b-6898b9c89f-mpkjc']
2025-12-15T08:33:59.0671054Z stdout F INFO:     127.0.0.1:42588 - "GET /readiness HTTP/1.1" 200 OK
2025-12-15T08:34:29.0649033Z stdout F INFO:     127.0.0.1:60246 - "GET /readiness HTTP/1.1" 200 OK
2025-12-15T08:34:59.0644467Z stdout F INFO:     127.0.0.1:43994 - "GET /readiness HTTP/1.1" 200 OK
2025-12-15T08:35:29.0651892Z stdout F INFO:     127.0.0.1:59368 - "GET /readiness HTTP/1.1" 200 OK
2025-12-15T08:35:59.0644637Z stdout F INFO:     127.0.0.1:57488 - "GET /readiness HTTP/1.1" 200 OK
```

#### 200 OK (system logs)

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Transfer-Encoding: chunked

{"TimeStamp":"2025-12-15T16:51:33Z","Type":"Normal","ContainerAppName":null,"RevisionName":null,"ReplicaName":null,"Msg":"Connecting to the events collector...","Reason":"StartingGettingEvents","EventSource":"ContainerAppController","Count":1}
{"TimeStamp":"2025-12-15T16:51:34Z","Type":"Normal","ContainerAppName":null,"RevisionName":null,"ReplicaName":null,"Msg":"Successfully connected to events server","Reason":"ConnectedToEventsServer","EventSource":"ContainerAppController","Count":1}
```

### Stop an agent deployment

To stop the hosted agent, set the maximum replica for your agent deployment to zero and use the following command:

```bash
az cognitiveservices agent stop
```

The arguments for this command include:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--agent-version` | ✅ | Foundry Tools hosted agent version |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |

Here's an example:

```bash
az cognitiveservices agent stop --account-name myAccount --project-name myProject --name myAgent --agent-version 1
```

When you stop an agent:

- Current status: **Running**
- Allowed operation: **Stop**
- Transitory status: **Stopping**
- Final status: **Stopped** (if successful) or **Running** (if unsuccessful)

### Delete an agent

You can delete agents at various levels, depending on what you want to remove.

#### Delete a deployment only

The following command stops the running agent but keeps the agent version for future use. Use it when you want to stop the agent temporarily or switch to a different version.

```bash
az cognitiveservices agent delete-deployment
```

The arguments for this command include:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--agent-version` | ✅ | Foundry Tools hosted agent version |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |

#### Delete the agent

The following command removes all versions and deployments for the agent. Use it when you no longer need the agent and want to clean up all associated resources.

If you provide `agent_version` and you delete the agent deployment, the operation deletes the agent definition associated with that version. If the agent deployment is running, the operation doesn't succeed.

If you don't provide `agent_version`, the operation deletes all agent versions associated with the agent name.

```bash
az cognitiveservices agent delete
```

The arguments for this command include:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--account-name -a` | ✅ | Foundry Tools account name. |
| `--name -n` | ✅ | Foundry Tools hosted agent name. |
| `--project-name` | ✅ | AI project name. |
| `--agent-version` | ❌ | Foundry Tools hosted agent version. If you don't provide it, the command deletes all versions. |

### List hosted agents

#### List all versions of a hosted agent

```bash
az cognitiveservices agent list-versions
```

The arguments for this command include:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |

#### Show details of a hosted agent

```bash
az cognitiveservices agent show
```

The arguments for this command include:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |

---

### Invoke hosted agents

You can view and test hosted agents in the agent playground UI. Hosted agents expose an API that's compatible with OpenAI responses. Use the Azure AI Projects SDK to invoke this API.

```python
#!/usr/bin/env python3
"""
Call a deployed Microsoft Foundry agent
"""

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentReference

# Configuration
PROJECT_ENDPOINT = "https://your-project.services.ai.azure.com/api/projects/your-project"
AGENT_NAME = "your-agent-name"
AGENT_VERSION = "1"  # Optional: specify version, or use latest

# Initialize the client and retrieve the agent
client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
agent = client.agents.get(agent_name=AGENT_NAME)
print(f"Agent retrieved: {agent.name} (version: {agent.versions.latest.version})")

# Get the OpenAI client and send a message
openai_client = client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Hello! What can you help me with?"}],
    extra_body={"agent": AgentReference(name=agent.name, version=AGENT_VERSION).as_dict()}
)

print(f"Agent response: {response.output_text}")
```

Expected output:

```output
Agent retrieved: your-agent-name (version: 1)
Agent response: Hello! I'm your hosted agent. I can help you with...
```

For more information, see [Azure AI Projects SDK for Python](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&preserve-view=true).

### Use tools with hosted agents

Before your hosted agent can run with Foundry tools, create a connection to your remote Model Context Protocol (MCP) server on Foundry.

The `RemoteMCPTool` connection supports these authentication mechanisms:

- **Stored credentials**: Use predefined credentials stored in the system.
- **Project managed identity**: Use the managed identity for the Foundry project.

Choose your authentication method:

- **For shared identity**: Use key-based or Foundry project managed identity authentication when every user of your agent should use the same identity. Individual user identity or context doesn't persist with these methods.

- **For individual user context**: Use OAuth identity passthrough when every user of your agent should use their own account to authenticate with the MCP server. This approach preserves personal user context.

For more information, see [Connect to Model Context Protocol servers](../how-to/tools/model-context-protocol.md).

Reference the Foundry tool connection ID for Remote MCP servers within your agent code by using an environment variable. Wrap it by using the Hosting adapter for testing locally. Build and push your Docker image to Azure Container Registry (ACR). Configure image pull permissions on the ACR. Create a capability host by following the instructions mentioned [above](#create-a-hosted-agent) and proceed to registering your agent on Foundry.

Create a hosted agents version with tools definition by using the Foundry SDK.

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition, ProtocolVersionRecord, AgentProtocol
from azure.identity import DefaultAzureCredential

# Initialize the client
client = AIProjectClient(
    endpoint="https://your-project.services.ai.azure.com/api/projects/project-name",
    credential=DefaultAzureCredential()
)

# Create the agent from a container image
agent = client.agents.create_version(
    agent_name="my-agent",
    description="Coding agent expert in assisting with github issues",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="your-registry.azurecr.io/your-image:tag",
        tools=[
            {
                "type": "code_interpreter"
            },
            {
                "type": "mcp",
                "project_connection_id": "github_connection_id"
            }
        ],
        environment_variables={
            "AZURE_AI_PROJECT_ENDPOINT": "https://your-project.services.ai.azure.com/api/projects/project-name",
            "MODEL_NAME": "gpt-4",
            "CUSTOM_SETTING": "value"
        }
    )
)
```
Start the agent by using Azure Cognitive Services CLI or from within Agent Builder in the new Foundry UI. 

Currently supported built-in Foundry tools include:

- Code Interpreter
- Image Generation
- Web Search

## Manage observability with hosted agents

Hosted agents support exposing OpenTelemetry traces, metrics, and logs from underlying frameworks to Microsoft Foundry with Application Insights or any user-specified OpenTelemetry Collector endpoint.

If you use the `azd ai agent` CLI extension, Application Insights is automatically provisioned and connected to your Foundry project for you. Your project's managed identity is granted the Azure AI User role on the Foundry resource so that traces are exported to Application Insights.

If you use the Foundry SDK, you need to perform these steps independently. For more information, see [Enable tracing in your project](../../../how-to/develop/trace-application.md#enable-tracing-in-your-project).

The hosting adapter provides:

- **Complete OpenTelemetry setup**: `TracerProvider`, `MeterProvider`, `LoggerProvider`.
- **Auto-instrumentation**: HTTP requests, database calls, AI model calls.
- **Azure Monitor integration**: Exporters, formatting, authentication.
- **Performance optimization**: Sampling, batching, resource detection.
- **Live metrics**: Real-time dashboard in Application Insights.

### Local tracing

1. Install and set up AI Toolkit for Visual Studio Code (VS Code) by following [Trace in AI Toolkit](https://code.visualstudio.com/docs/intelligentapps/tracing).

1. Set up and export the environment variable `OTEL_EXPORTER_ENDPOINT`. You can find the endpoint from AI Toolkit for VS Code after you select the **Start Collector** button.

1. Invoke the agent and find traces in AI Toolkit.

### Tracing in the Foundry portal

You can also review traces for your hosted agent on the **Traces** tab in the playground.

### Export traces to your OpenTelemetry-compatible server

To send traces to your own OpenTelemetry collector or compatible observability platform, use the environment variable `OTEL_EXPORTER_ENDPOINT`.

## Manage conversations by using hosted agents

Hosted agents integrate seamlessly with the conversation management system in Microsoft Foundry. This integration enables stateful, multiple-turn interactions without manual state management.

### How conversations work with hosted agents

**Conversation objects**: Foundry automatically creates durable conversation objects with unique identifiers that persist across multiple agent interactions. When a user starts a conversation with your hosted agent, the platform maintains this conversation context automatically.

**State management**: Unlike traditional APIs where you manually pass conversation history, hosted agents receive conversation context automatically. The Foundry runtime manages:

- Previous messages and responses.
- Tool calls and their outputs.
- Agent instructions and configuration.
- Conversation metadata and time stamps.

**Conversation items**: Each conversation contains structured items that the system automatically maintains:

- **Messages**: User inputs and agent responses with time stamps.
- **Tool calls**: Function invocations with parameters and results.
- **Tool outputs**: Structured responses from external services.
- **System messages**: Internal state and context information.

### Conversation persistence and reuse

**Cross-session continuity**: Conversations persist beyond individual requests. Users can return to previous discussions with full context maintained.

**Conversation reuse**: Users can access the same conversation from multiple channels and applications. Conversations maintain consistent state and history.

**Automatic cleanup**: Foundry manages conversation lifecycle and cleanup based on your project's retention policies.

## Evaluate and test hosted agents

Microsoft Foundry provides comprehensive evaluation and testing capabilities that are designed for hosted agents. Use these capabilities to validate performance, compare versions, and help ensure quality before deployment.

### Built-in evaluation capabilities

**Agent performance evaluation**: Foundry includes built-in evaluation metrics to assess your hosted agent's effectiveness:

- Response quality and relevance
- Task completion accuracy
- Tool usage effectiveness
- Conversation coherence and context retention
- Response time and efficiency metrics

**Agent-specific evaluation**: Evaluate hosted agents by using the Foundry SDK with built-in evaluators that are designed for agentic workflows. The SDK provides specialized evaluators for measuring agent performance across key dimensions like intent resolution, task adherence, and tool usage accuracy.

### Testing workflows for hosted agents

**Development testing**: Test your hosted agent locally during development by using the agent playground and local testing tools before deployment.

**Staging validation**: Deploy to a staging environment to validate behavior by using real Foundry infrastructure while maintaining isolation from production.

**Production monitoring**: Continuously monitor deployed hosted agents by using automated evaluation runs to detect performance degradation or problems.

### Structured evaluation approaches

**Test dataset creation**: Create comprehensive test datasets that cover:

- Common user interaction patterns.
- Edge cases and error scenarios.
- Multiple-turn conversation flows.
- Tool usage scenarios.
- Performance stress tests.

**Supported evaluation metrics**: The Foundry SDK provides the following evaluators for agent workflows:

- **Intent Resolution**: Measures how well the agent identifies and understands user requests.
- **Task Adherence**: Evaluates whether the agent's responses adhere to assigned tasks and system instructions.
- **Tool Call Accuracy**: Assesses whether the agent makes correct function tool calls for user requests.
- **Additional Quality Metrics**: Enables the use of relevance, coherence, and fluency with agent messages.

### Evaluation best practices

**Test with representative data**: Create evaluation datasets that represent your actual user interactions and use cases.

**Monitor agent performance**: Use the Foundry portal to track agent performance and review conversation traces.

**Use iterative evaluation**: Regularly evaluate agent versions during development to catch problems early and measure improvements.

For more information about evaluating agents, see [Evaluate your AI agents](../../../how-to/develop/agent-evaluate-sdk.md) and [Agent evaluators](../../../concepts/evaluation-evaluators/agent-evaluators.md).

## Publish hosted agents to channels

Publishing transforms your hosted agent from a development asset into a managed Azure resource with a dedicated endpoint, independent identity, and governance capabilities. After you publish your hosted agent, you can share it across multiple channels and platforms.

### Publishing process for hosted agents

When you publish a hosted agent, Microsoft Foundry automatically:

1. Creates an agent application resource with a dedicated invocation URL.
1. Provisions a distinct agent identity that's separate from your project's shared identity.
1. Registers the agent in the Microsoft Entra agent registry for discovery and governance.
1. Enables stable endpoint access that remains consistent as you deploy new agent versions.

Unlike prompt-based agents that you can edit in the portal, hosted agents keep their code-based implementation while gaining the same publishing and sharing capabilities.

### Available publishing channels

**Web application preview**: Use a web interface to demonstrate and test your hosted agent with stakeholders. It's instant and shareable.

**Microsoft 365 Copilot and Teams**: Integrate your hosted agent directly into Microsoft 365 Copilot and Microsoft Teams through a streamlined, no-code publishing flow. Your agent appears in the agent store for organizational or shared scope distribution.

**Stable API endpoint**: Access your hosted agent programmatically through a consistent REST API that remains unchanged as you update agent versions.

**Custom applications**: Embed your hosted agent into existing applications by using the stable endpoint and SDK integration.

### Publishing considerations for hosted agents

**Identity management**: Published hosted agents use their own agent identity. You need to reconfigure permissions for any Azure resources that your agent accesses. Permissions for the shared development identity don't automatically transfer.

**Version control**: Publishing creates a deployment that references your current agent version. You can update the published agent by deploying new versions without changing the public endpoint.

**Authentication**: Published agents support RBAC-based authentication by default. This authentication includes automatic permission handling for Azure Bot Service integration when you're publishing to Microsoft 365 channels.

For detailed publishing instructions, see [Publish and share agents](../how-to/publish-agent.md).

## Troubleshoot hosted agent endpoints

If your agent deployment fails, view error logs by selecting **View deployment logs**. If you get 4xx errors, use the following table to determine next steps. If the agent endpoint returns 5xx status codes, contact Microsoft support.

| Error classification | HTTP status code | Solution |
| -------------------- | ---------------- | -------- |
| `SubscriptionIsNotRegistered` | 400 | Register the feature or subscription provider. |
| `InvalidAcrPullCredentials` (`AcrPullWithMSIFailed`) | 401 | Fix the managed identity or registry RBAC. |
| `UnauthorizedAcrPull` (`AcrPullUnauthorized`) | 403 | Provide the correct credentials or identity. |
| `AcrImageNotFound` | 404 | Correct the image name or tag, or publish the image. |
| `RegistryNotFound` | 400/404 | Fix registry DNS or server spelling, or network reachability. |
| `ValidationError` | 400 | Correct invalid request fields. |
| `UserError` (generic) | 400 | Inspect the message and fix the configuration. |

### Troubleshoot runtime issues

If your hosted agent deploys successfully but doesn't respond as expected, check these common issues:

| Symptom | Possible cause | Solution |
| ------- | -------------- | -------- |
| Agent doesn't respond | Container is still starting | Wait for the agent status to show **Started**. Check the log stream for startup progress. |
| Slow response times | Insufficient resource allocation | Increase CPU or memory allocation in the agent definition. |
| Timeout errors | Long-running operations | Increase timeout settings in your agent code. Consider breaking operations into smaller steps. |
| Intermittent failures | Replica scaling issues | Check that `min_replicas` is set appropriately for your workload. |
| Tool calls failing | Missing connection configuration | Verify that tool connections are properly configured and the managed identity has access. |
| Model errors | Invalid model deployment name | Verify that `MODEL_NAME` environment variable matches an available model deployment. |

To debug runtime issues:

1. Use the [log stream API](#view-container-log-stream) to view container logs in real time.
2. Check the **Traces** tab in the Foundry portal playground for detailed request and response information.
3. Verify environment variables are set correctly in your agent definition.

## Understand preview details

### Limitations during preview

| Dimension | Limit |
| --------- | ----- |
| Microsoft Foundry resources with hosted agents per Azure subscription | 100 |
| Maximum number of hosted agents per Foundry resource | 200 |
| Maximum `min_replica` count for an agent deployment | 2 |
| Maximum `max_replica` count for an agent deployment | 5 |

### Hosting pricing

Billing for managed hosting runtime is enabled no earlier than February 1, 2026, during the preview. For updates on pricing, check the Foundry [pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

### Private networking support

Currently, you can't create hosted agents by using the standard setup within network-isolated Foundry resources. For more information, see [Configure virtual networks](../../../agents/how-to/virtual-networks.md).

## Related content

- [Python code samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
- [C# code samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents)
- [Agent runtime components](./runtime-components.md)
- [Agent development lifecycle](./development-lifecycle.md)
- [Agent identity concepts in Microsoft Foundry](./agent-identity.md)
- [Discover tools in Foundry Tools](./tool-catalog.md)
- [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md)
- [Azure Container Registry documentation](/azure/container-registry/)