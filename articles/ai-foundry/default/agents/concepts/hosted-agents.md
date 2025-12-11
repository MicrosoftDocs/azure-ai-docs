---
title: Hosted Agents in Microsoft Foundry Agent Service (Preview)
description: Learn how to deploy and manage containerized AI agents with zero infrastructure setup by using the feature of hosted agents in Microsoft Foundry.
titleSuffix: Microsoft Foundry
author: aahill
ms.author: aahi
ms.date: 12/05/2025
ms.manager: nitinme
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
---

# What are hosted agents? 

When you build agentic applications with open-source frameworks, you typically manage containerization, web server setup, security integration, memory persistence, infrastructure scaling, data transmission, instrumentation, and version rollbacks. These tasks become even more challenging in heterogeneous cloud environments.

Hosted agents in Microsoft Foundry Agent Service solve these challenges. With this fully managed platform, you can deploy and operationalize AI agents securely and at scale. You can use your custom agent code or a preferred agent framework with seamless deployment and management.

## Prerequisites

- A [Microsoft Foundry project](../../../how-to/create-projects.md)
- Basic understanding of [containerization and Docker](/azure/container-instances/container-instances-overview)
- Familiarity with [Azure Container Registry](/azure/container-registry/container-registry-intro)
- Knowledge of your preferred agent framework (LangGraph, Microsoft Agent Framework, or custom code)

## Understand key concepts

### Hosted agents

Hosted agents are containerized agentic AI applications that run on Foundry Agent Service. Unlike prompt-based agents, hosted agents are built via code and deployed as container images on Microsoft-managed pay-as-you-go infrastructure.

Hosted agents follow a standard lifecycle: create, start, update, stop, delete. Each phase provides specific capabilities and status transitions to manage your agent deployments effectively.

> [!NOTE]
> Hosted agents are currently in preview. For hosting pricing and limitations during the preview, see the [Microsoft Foundry](https://eastus2euap.ai.azure.com/nextgen/r/R_HJFOKZSVOpnT40ZEz-HA,container_agents_2509_preview,,hostedagents-testing-ws2,hostedagents-testing/home?flight=ignite_preview%3Dfalse%2Cnextgen_canary%2Cagent_ignite_group%2CshowAgentDetailsInInvokeAgent) home page.

### Hosting adapter

The hosting adapter is a framework abstraction layer that automatically converts popular agent frameworks into Microsoft Foundry-compatible HTTP services. This adapter eliminates the need to manually implement REST APIs and message handling.

The hosting adapter provides several key benefits for developers:

**One-line deployment**: Transform complex agent deployment into a single line of code (`from_langgraph(my_agent).run()`) that instantly hosts your agent on `localhost:8088` with all necessary HTTP endpoints, streaming support, and Foundry protocol compliance.

**Automatic protocol translation**: The adapter handles all complex conversions between the Foundry request/response formats and your agent framework's native data structures. These activities include:

- Conversation management
- Message serialization
- Streaming event generation

**Built-in production features**: Get the following enterprise-ready capabilities automatically without additional configuration:

- OpenTelemetry tracing
- Cross-origin resource sharing (CORS) support
- Server-sent events (SSE) streaming
- Structured logging

**Seamless Foundry integration**: Your locally developed agents work immediately with the Foundry Responses API, conversation management, and authentication flows. This integration bridges the gap between development frameworks and the Azure production AI platform.

### Managed service capabilities

Foundry Agent Service handles:

- Provisioning and autoscaling of agents.
- Conversation orchestration and state management.
- Identity management.
- Integration with Microsoft Foundry tools and models.
- Built-in observability and evaluation capabilities.
- Enterprise-grade security, compliance, and governance.

> [!IMPORTANT]
> If you use Foundry Agent Service to host agents that interact with non-Microsoft servers or agents, you do so at your own risk. We recommend that you review all data that you share with non-Microsoft servers or agents and be aware of non-Microsoft practices for retention and location of data. It's your responsibility to manage whether your data flows outside your organization's Azure compliance and geographic boundaries, along with any related implications.

### Framework and language support

| Framework | Python | C# |
|-----------|--------|-----|
| Microsoft Agent Framework | ✅ |  ✅ |
| LangGraph |  ✅ | ❌ |
| Custom code | ✅ | ✅ |

### Public adapter packages

- Python: `azure-ai-agentserver-core`, `azure-ai-agentserver-agentframework`, `azure-ai-agentserver-langgraph`
- .NET: `Azure.AI.AgentServer.Core`, `Azure.AI.AgentServer.AgentFramework`

## Package code and test locally

Before you deploy to Microsoft Foundry, you can build and test your agent locally:

1. **Run your agent locally**: Use the hosting adapter to start a local web server that automatically exposes your agent as a REST API.
2. **Test with REST calls**: The local server runs on `localhost:8088` and accepts standard HTTP requests.
3. **Build the container image**: Create a container image from your source files by using the `azure-ai-agents-server-*` package to wrap your agent code.
4. **Use the Azure Developer CLI**: Use `azd` to streamline the packaging and deployment process.

### Local testing with the REST API

When you run your agent locally by using the hosting adapter, it automatically starts a web server on `localhost:8088`. You can test your agent by using any REST client:

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

## Create a hosted agent by using the Azure Developer CLI

Developers can use the [Azure Developer CLI](/azure/developer/azure-developer-cli/overview) `ai agent` extension for seamless and rapid provisioning and deployment of their agentic applications on Microsoft Foundry.

This extension simplifies the setup of Foundry resources, models, tools, and knowledge resources. For example, it simplifies the setup of Azure Container Registry for bringing your own container, Application Insights for logging and monitoring, a managed identity, and role-based access control (RBAC). In other words, it provides everything you need to get started with hosted agents in Foundry Agent Service.

This extension is currently in preview. We don't recommend it for production use.

To get started:

1. Install the Azure Developer CLI on your device.

   If you already have the Azure Developer CLI installed, check if you have the latest version of `azd` installed:

    ```bash
    azd version
    ```

    To upgrade to the latest version, see [Install or update the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd).

1. If you're starting with no existing Foundry resources and you want to simplify all the required infrastructure provisioning and RBAC, download the Foundry starter template. The template automatically installs the `ai agent` extension.

    ```bash
    azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
    ```

    To check all installed extensions:

    ```bash
    azd ext list
    ```

    We recommend that you have the latest version of the Foundry `azd` agent extension installed.

    If you have an existing Foundry project where you want to deploy your agent, and you want to provision only the additional resources that you might need for deploying your agent, run this command afterward:

    ```bash
    azd ai agent init --project-id /subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/projects/[PROJECTNAME]
    ```

1. Initialize the template by configuring the parameters in the agent definition:

    ```bash
    azd ai agent init -m <repo-path-to-agent.yaml>
    ```

    The GitHub repo for an agent that you want to host on Foundry contains the application code, referenced dependencies, Dockerfile for containerization, and the `agent.yaml` file that contains your agent's definition. To configure your agent, set values for the parameters that you're prompted for. This action registers your agent under `Services` in `azure.yaml` for the downloaded template. You can get started with samples on [GitHub](https://github.com/azure-ai-foundry/foundry-samples).

1. To open and view all Bicep and configuration files associated with your `azd`-based deployments, use this command:

    ```bash
    code .
    ```

1. Package, provision, and deploy your agent code as a managed application on Foundry:

    ```bash
    azd up
    ```

    This command abstracts the underlying execution of the commands `azd infra generate`, `azd provision`, and `azd deploy`. It also creates a hosted agent version and deployment on Foundry Agent Service. If you already have a version of a hosted agent, `azd` creates a new version of the same agent. To learn more on how you can do non-versioned updates, along with starting, stopping, and deleting your hosted agent deployments and versions, see the [management section](#manage-hosted-agents) of this article.

Make sure you have [RBAC](/azure/role-based-access-control/built-in-roles) enabled so that `azd` can provision the services and models for you.

### Roles and permissions

If you have an existing Foundry resource and need to create a new Foundry project to deploy a hosted agent, you need Account Owner and Azure AI User roles.

If you have an existing project and want to create the model deployment and container registry in the project, you need Account Owner and Azure AI User roles on Foundry in addition to the Contributor role on the Azure subscription.

If you have everything configured in the project to deploy a hosted agent, you need Reader and Azure AI User roles.

### Resource cleanup

To prevent unnecessary charges, it's important to clean up your Azure resources after you complete your work with the application.

When to clean up:

- After you finish testing or demonstrating the application
- When the application is no longer needed or you transition to a different project or environment
- When you complete development and are ready to decommission the application

To delete all associated resources and shut down the application, run the following command:

```bash
azd down
```

This process might take up to 20 minutes to complete.

## Create a hosted agent by using the Foundry SDK

When you create a hosted agent, the system registers the agent definition in Microsoft Foundry and tries to create a deployment for that agent version.

### Prerequisites for deployment

Before you deploy a hosted agent, ensure that you have:

- A container image hosted in [Azure Container Registry](https://azure.microsoft.com/services/container-registry/). For more information, see [Create a private container registry](/azure/container-registry/container-registry-get-started-portal).
- Access to assign roles in Azure Container Registry. You need at least User Access Administrator or Owner permissions on the container registry.
- The Azure AI Projects SDK installed:

  ```bash
  pip install azure-ai-projects
  ```

### Build and push your Docker image to Azure Container Registry

To build your agent as a Docker container and upload it to Azure Container Registry:

1. Build your Docker image locally:

   ```bash
   docker build -t myagent:v1 .
   ```   
   Refer to sample DockerFile for [python](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agents_in_workflow/Dockerfile) and [C#](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/csharp/hosted-agents/AgentsInWorkflows/Dockerfile). 
   
2. Sign in to Azure Container Registry:

   ```bash
   az acr login --name myregistry
   ```

3. Tag your image for the registry:

   ```bash
   docker tag myagent:v1 myregistry.azurecr.io/myagent:v1
   ```

4. Push the image to Azure Container Registry:

   ```bash
   docker push myregistry.azurecr.io/myagent:v1
   ```

For detailed guidance on working with Docker images in Azure Container Registry, see [Push and pull Docker images](/azure/container-registry/container-registry-get-started-docker-cli).

### Configure Azure Container Registry permissions

Before you create the agent, give your project's managed identity access to pull from the container registry that houses your image. This step ensures that all dependencies are available within the container.

1. In the [Azure portal](https://portal.azure.com), go to your Foundry project resource.

1. On the left pane, select **Identity**.

1. Under **System assigned**, copy the **Object (principal) ID** value. This value is the managed identity that you'll assign the Azure Container Instances role to.

1. Grant pull permissions by assigning the Container Registry Repository Reader role to your project's managed identity on the container registry. For detailed steps, see [Azure Container Registry roles and permissions](/azure/container-registry/container-registry-roles).

### Create account-level Capability Host

Updating capability hosts is not supported. If you have an existing capability host for your Microsoft Foundry account, you must delete the existing one and recreate it with the property `enablePublicHostingEnvironment` set to `true`. 

#### Get access token

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)
```

#### Create capability host

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/capabilityHosts/accountcaphost?api-version=2025-10-01-preview' \
  --header 'content-type: application/json' \
  --header "authorization: Bearer $TOKEN"\
  --data '{
  "properties": {
    "capabilityHostKind": "Agents",
    "enablePublicHostingEnvironment": true
    }
 }
```


### Create the hosted agent version

Install version>=2.0.0b2 of the [Azure AI Projects SDK](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&preserve-view=true)

```bash
pip install --pre azure-ai-projects==2.0.0b2
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
            "API_KEY": "your-api-key",
            "MODEL_NAME": "gpt-4",
            "CUSTOM_SETTING": "value"
        }
    )
)
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

The arguments for this code include:

| Argument | Required | Description |
|----------|----------|-------------|
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

After you create your hosted agent version, you can start the deployment by using the `az` CLI extension to make it available for requests. You can also start a hosted agent that's stopped.

```bash
az cognitiveservices agent start
```

The arguments for this code include:

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--agent-version` | ✅ | Foundry Tools hosted agent version |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |
| `--min-replicas` | ❌ | Minimum number of replicas for horizontal scaling |
| `--max-replicas` | ❌ | Maximum number of replicas for horizontal scaling |

If no max and min replicas are specified during agent start operation, default value used is 1 for both the arguments. 

Here's an example:

```bash
az cognitiveservices agent start --account-name myAccount --project-name myProject --name myAgent --agent-version 1
```

When you start an agent:

- Current status: **Stopped**
- Allowed operation: **Start**
- Transitory status: **Starting**
- Final status: **Started** (if successful) or **Failed** (if unsuccessful)

### Stop an agent deployment

You can override the maximum replica configured for your agent deployment by setting it to zero and force stop the hosted agent by using this command:

```bash
az cognitiveservices agent stop
```

The arguments for this code include:

| Argument | Required | Description |
|----------|----------|-------------|
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

The arguments for this code include:

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--agent-version` | ✅ | Foundry Tools hosted agent version |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |

#### Delete the agent

The following command removes all versions and deployments for the agent. Use it when you no longer need the agent and want to clean up all associated resources.

If you provide `agent_version` and you delete the agent deployment, the agent definition associated with that version is deleted. If the agent deployment is running, this operation doesn't succeed.

If you don't provide `agent_version`, all agent versions associated with the agent name are deleted.

```bash
az cognitiveservices agent delete
```

The arguments for this code include:

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Foundry Tools account name. |
| `--name -n` | ✅ | Foundry Tools hosted agent name. |
| `--project-name` | ✅ | AI project name. |
| `--agent-version` | ❌ | Foundry Tools hosted agent version. If you don't provide it, the command deletes all versions. |

### List hosted agents

#### List all versions of a hosted agent

```bash
az cognitiveservices agent list-versions
```

The arguments for this code include:

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |

#### Show details of a hosted agent

```bash
az cognitiveservices agent show
```

The arguments for this code include:

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Foundry Tools account name |
| `--name -n` | ✅ | Foundry Tools hosted agent name |
| `--project-name` | ✅ | AI project name |

---

### Invoke hosted agents

You can view and test hosted agents in the agent playground UI. Hosted agents expose an OpenAI Responses-compatible API that you can invoke by using the Azure AI Projects SDK.

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
agent = client.agents.retrieve(agent_name=AGENT_NAME)

# Get the OpenAI client and send a message
openai_client = client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Hello! What can you help me with?"}],
    extra_body={"agent": AgentReference(name=agent.name, version=AGENT_VERSION).as_dict()}
)

print(f"Agent response: {response.output_text}")
```

### Use tools with hosted agents

Before your hosted agent can run with Foundry tools, you need to create a connection to your remote Model Context Protocol (MCP) server on Foundry.

The `RemoteMCPTool` connection supports these authentication mechanisms:

- **Stored credentials**: Use predefined credentials stored in the system.
- **Project managed identity**: Use the managed identity for the Foundry project.

Choose your authentication method:

- **For shared identity**: Use key-based or Foundry project managed identity authentication when every user of your agent should use the same identity. Individual user identity or context doesn't persist with these methods.

- **For individual user context**: Use OAuth identity passthrough when every user of your agent should use their own account to authenticate with the MCP server. This approach preserves personal user context.

To learn how to create the `RemoteMCPTool` connection, see [Connect to Model Context Protocol servers](../../../agents/how-to/tools/model-context-protocol.md).

Reference the Foundry tool connection ID for Remote MCP servers within your agent code using an environment variable and wrap it with the Hosting adapter for testing locally. Build and push your Docker image to Azure Container Registry (ACR), configure image pull permissions on the ACR, [create a capability host](#create-a-hosted-agent-by-using-the-foundry-sdk) and proceed to registering your agent on Foundry.

Create Hosted Agents Version with tools definition using the Foundry SDK:

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
            "API_KEY": "your-api-key",
            "MODEL_NAME": "gpt-4",
            "CUSTOM_SETTING": "value"
        }
    )
)
```
Start the agent using Azure CognitiveServices CLI or from within Agent Builder in the new Foundry UI. 

Currently supported built-in Foundry tools include:

- Code Interpreter
- Image Generation
- Web Search

## Manage observability with hosted agents

Hosted agents support exposing OpenTelemetry traces, metrics, and logs from underlying frameworks to Microsoft Foundry with Application Insights or any user-specified OpenTelemetry Collector endpoint.

If you use the `azd ai agent` CLI extension, Application Insights is automatically provisioned and connected to your Foundry project for you. Your project's managed identity is granted the Azure AI User role on the Foundry resource so that traces are exported to Application Insights.

If you use the Foundry SDK, you have to perform these steps independently. Learn more in [this article](/azure/ai-foundry/how-to/develop/trace-application#enable-tracing-in-your-project).

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

### Export of traces to your OpenTelemetry-compatible server

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

**Conversation items**: Each conversation contains structured items that are automatically maintained:

- **Messages**: User inputs and agent responses with time stamps.
- **Tool calls**: Function invocations with parameters and results.
- **Tool outputs**: Structured responses from external services.
- **System messages**: Internal state and context information.

### Conversation persistence and reuse

**Cross-session continuity**: Conversations persist beyond individual requests. Users can return to previous discussions with full context maintained.

**Conversation reuse**: Users can access the same conversation from multiple channels and applications. Conversations maintain consistent state and history.

**Automatic cleanup**: Foundry manages conversation lifecycle and cleanup based on your project's retention policies.

## Evaluate and test hosted agents

Microsoft Foundry provides comprehensive evaluation and testing capabilities that are designed for hosted agents. You can use these capabilities to validate performance, compare versions, and help ensure quality before deployment.

### Built-in evaluation capabilities

**Agent performance evaluation**: Foundry includes built-in evaluation metrics to assess your hosted agent's effectiveness:

- Response quality and relevance
- Task completion accuracy
- Tool usage effectiveness
- Conversation coherence and context retention
- Response time and efficiency metrics

**Agent-specific evaluation**: Evaluate hosted agents by using the Azure AI Evaluation SDK with built-in evaluators that are designed for agentic workflows. The SDK provides specialized evaluators for measuring agent performance across key dimensions like intent resolution, task adherence, and tool usage accuracy.

### Testing workflows for hosted agents

**Development testing**: Test your hosted agent locally during development by using the agent playground and local testing tools before deployment.

**Staging validation**: Deploy to a staging environment to validate behavior with real Foundry infrastructure while maintaining isolation from production.

**Production monitoring**: Continuously monitor deployed hosted agents with automated evaluation runs to detect performance degradation or problems.

### Structured evaluation approaches

**Test dataset creation**: Create comprehensive test datasets that cover:

- Common user interaction patterns.
- Edge cases and error scenarios.
- Multiple-turn conversation flows.
- Tool usage scenarios.
- Performance stress tests.

**Supported evaluation metrics**: The Azure AI Evaluation SDK provides the following evaluators for agent workflows:

- **Intent Resolution**: Measures how well the agent identifies and understands user requests.
- **Task Adherence**: Evaluates whether the agent's responses adhere to assigned tasks and system instructions.
- **Tool Call Accuracy**: Assesses whether the agent makes correct function tool calls for user requests.
- **Additional Quality Metrics**: Enables the use of relevance, coherence, and fluency with agent messages.

### Evaluation best practices

**Test with representative data**: Create evaluation datasets that represent your actual user interactions and use cases.

**Monitor agent performance**: Use the Foundry portal to track agent performance and review conversation traces.

**Use iterative evaluation**: Regularly evaluate agent versions during development to catch issues early and measure improvements.

For detailed information about evaluating agents, see [Evaluate your AI agents locally](../../../how-to/develop/agent-evaluate-sdk.md) and [Agent evaluators](../../../concepts/evaluation-evaluators/agent-evaluators.md).

## Publish hosted agents to channels

Publishing transforms your hosted agent from a development asset into a managed Azure resource with a dedicated endpoint, independent identity, and governance capabilities. After you publish your hosted agent, you can share it across multiple channels and platforms.

### Publishing process for hosted agents

When you publish a hosted agent, Microsoft Foundry automatically:

1. Creates an agent application resource with a dedicated invocation URL.
2. Provisions a distinct agent identity that's separate from your project's shared identity.
3. Registers the agent in the Microsoft Entra agent registry for discovery and governance.
4. Enables stable endpoint access that remains consistent as you deploy new agent versions.

Unlike prompt-based agents that can be edited in the portal, hosted agents maintain their code-based implementation while gaining the same publishing and sharing capabilities.

### Available publishing channels

**Web application preview**: Get an instant, shareable web interface to demonstrate and test your hosted agent with stakeholders.

**Microsoft 365 Copilot and Teams**: Integrate your hosted agent directly into Microsoft 365 Copilot and Microsoft Teams through a streamlined, no-code publishing flow. Your agent appears in the agent store for organizational or shared scope distribution.

**Stable API endpoint**: Access your hosted agent programmatically through a consistent REST API that remains unchanged as you update agent versions.

**Custom applications**: Embed your hosted agent into existing applications by using the stable endpoint and SDK integration.

### Publishing considerations for hosted agents

**Identity management**: Published hosted agents receive their own agent identity, which requires you to reconfigure permissions for any Azure resources that your agent accesses. Permissions for the shared development identity don't automatically transfer.

**Version control**: Publishing creates a deployment that references your current agent version. You can update the published agent by deploying new versions without changing the public endpoint.

**Authentication**: Published agents support RBAC-based authentication by default. This authentication includes automatic permission handling for Azure Bot Service integration when you're publishing to Microsoft 365 channels.

For detailed publishing instructions, see [Publish and share agents](../how-to/publish-agent.md).

## Troubleshoot hosted agent endpoints

If your agent deployment fails, view error logs by selecting **View deployment logs**. If you get 4xx errors, use the following table to determine next steps. If the agent endpoint returns 5xx status codes, contact Microsoft support.

| Error classification | HTTP status code | Solution |
|----------------------|------------------|------------|
| `SubscriptionIsNotRegistered` | 400 | Register the feature or subscription provider. |
| `InvalidAcrPullCredentials` (`AcrPullWithMSIFailed`) | 401 | Fix the managed identity or registry RBAC. |
| `UnauthorizedAcrPull` (`AcrPullUnauthorized`) | 403 | Provide the correct credentials or identity. |
| `AcrImageNotFound` | 404 | Correct the image name/tag or publish the image. |
| `RegistryNotFound` | 400/404 | Fix registry DNS/server spelling or network reachability. |
| `ValidationError` | 400 | Correct invalid request fields. |
| `UserError` (generic) | 400 | Inspect the message and fix the configuration. |

## Understand preview details

### Limitations during preview

| Dimension | Limit |
|-----------|-------|
| Microsoft Foundry resources with hosted agents per Azure subscription | 100 |
| Maximum number of hosted agents per Foundry resource | 200 |
| Maximum `min_replica` count for an agent deployment | 2 |
| Maximum `max_replica` count for an agent deployment | 5 |

### Hosting pricing

Billing for managed hosting runtime will be enabled no earlier than February 1, 2026, during the preview. For updates on pricing, check the Foundry [pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

### Region availability

Currently, hosted agents are supported in North Central US only.

### Private networking support

Currently, hosted agents can not be created with the [standard setup](/azure/ai-foundry/agents/how-to/virtual-networks) within network isolated Foundry resources. 

## Related content

- [Python code samples](https://github.com/azure-ai-foundry/foundry-samples/tree/hosted-agents/pyaf-samples/samples/microsoft/python/getting-started-agents/hosted-agents)
- [C# code samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents)
- [Agent runtime components](./runtime-components.md)
- [Agent development lifecycle](./development-lifecycle.md)
- [Agent identity concepts in Microsoft Foundry](./agent-identity.md)
- [Discover tools in Foundry Tools](./tool-catalog.md)
- [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md)
- [Azure Container Registry documentation](/azure/container-registry/)
