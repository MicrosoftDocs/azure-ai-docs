---
title: Hosted agents in Microsoft Foundry Agent service (preview)
description: Learn how to deploy and manage containerized AI agents with zero infrastructure setup using Microsoft Foundry's hosted agents feature.
titleSuffix: Microsoft Foundry
author: aahill
ms.author: aahi
ms.date: 12/02/2025
ms.manager: nitinme
ms.topic: article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
---

# What are hosted agents? 

When you build agentic applications with open-source frameworks, you typically manage containerization, web server setup, security integration, memory persistence, infrastructure scaling, telemetry, instrumentation, and version rollbacks. These tasks become even more challenging in heterogeneous cloud environments.

Hosted agents in Microsoft Foundry Agent Service solve these challenges. This fully managed platform lets you deploy and operationalize AI agents securely and at scale. You can use your custom agent code or a preferred agent framework with seamless deployment and management.

## Prerequisites

* An [Microsoft Foundry project](../../../how-to/create-projects.md)
* Basic understanding of [containerization and Docker](/azure/container-instances/container-instances-overview)
* Familiarity with [Azure Container Registry](/azure/container-registry/container-registry-intro) 
* Knowledge of your preferred agent framework (LangGraph, Microsoft Agent Framework, or custom code)

## Key concepts

### Hosted agents
Hosted agents are containerized agentic AI applications that run on the Microsoft Foundry Agent Service. Unlike prompt-based agents, hosted agents are built using code and deployed as container images on Microsoft managed pay as you go infrastructure.

### Agents hosting adapter
A framework abstraction layer that automatically converts popular agent frameworks into Microsoft Foundry-compatible HTTP services. This adapter eliminates the need to manually implement REST APIs and message handling.

### Hosted agent lifecycle
Hosted agents follow a standard lifecycle: Create → Start → Update → Stop → Delete. Each phase provides specific capabilities and status transitions to manage your agent deployments effectively.

### Managed service capabilities
The Microsoft Foundry Agent Service handles:
- Provisioning and autoscaling of agents
- Conversation orchestration and state management  
- Identity management
- Integration with Microsoft Foundry tools and models
- Built-in observability and evaluation capabilities
- Enterprise-grade security, compliance, and governance

> [!IMPORTANT]
> If you use the Microsoft Foundry Agent Service to host agents that interact with non-Microsoft servers or agents, you do so at your own risk. We recommend reviewing all data being shared with non-Microsoft servers or agents and being cognizant of non-Microsoft practices for retention and location of data. It is your responsibility to manage whether your data will flow outside of your organization's Azure compliance and geographic boundaries and any related implications.

> [!Note]
> Hosted Agents are currently in public preview. See the [Microsoft Foundry](https://eastus2euap.ai.azure.com/nextgen/r/R_HJFOKZSVOpnT40ZEz-HA,container_agents_2509_preview,,hostedagents-testing-ws2,hostedagents-testing/home?flight=ignite_preview%3Dfalse%2Cnextgen_canary%2Cagent_ignite_group%2CshowAgentDetailsInInvokeAgent) for hosting pricing and limitations during public preview. 

## Agents hosting adapter benefits

The hosting adapter provides several key benefits for developers:

**One-line deployment**: Transform complex agent deployment into a single line of code (`from_langgraph(my_agent).run()`) that instantly hosts your agent on `localhost:8088` with all necessary HTTP endpoints, streaming support, and Microsoft Foundry protocol compliance.

**Automatic protocol translation**: The adapter handles all complex conversions between Microsoft Foundry's request/response formats and your agent framework's native data structures, including:
- Conversation management
- Message serialization  
- Streaming event generation

**Built-in production features**: Get enterprise-ready capabilities automatically without additional configuration:
- OpenTelemetry tracing
- CORS support
- Server-Sent Events (SSE) streaming
- Structured logging

**Seamless Microsoft Foundry integration**: Your locally developed agents work immediately with Microsoft Foundry's Responses API, conversation management, and authentication flows, bridging the gap between development frameworks and Azure's production AI platform.

## Framework and language support

| Framework | Python | C# |
|-----------|--------|-----|
| Microsoft Agent Framework | ✅ |  ✅ |
| LangGraph |  ✅ | ❌ |
| Custom code | ✅ | ✅ |

## Public adapter packages

* Python: `azure-ai-agentserver-core`, `azure-ai-agentserver-agentframework`, `azure-ai-agentserver-langgraph`
* .NET: `Azure.AI.AgentServer.Core`, `Azure.AI.AgentServer.AgentFramework`

## Package code and test locally

Before deploying to Microsoft Foundry, you can build and test your agent locally:

1. **Run your agent locally**: Use the hosting adapter to start a local web server that automatically exposes your agent as a REST API
2. **Test with REST calls**: The local server runs on `localhost:8088` and accepts standard HTTP requests
3. **Build container image**: Create a container image from your source files using the `azure-ai-agents-server-*` package to wrap your agent code
4. **Use Azure Developer CLI**: Use `azd` to streamline the packaging and deployment process

### Local testing with REST API

When you run your agent locally using the hosting adapter, it automatically starts a web server on `localhost:8088`. You can test your agent using any REST client:

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
- **Validate agent behavior** before containerization
- **Debug issues** in your development environment  
- **Test different input scenarios** quickly
- **Verify API compatibility** with Microsoft Foundry's Responses API

## Create a hosted agent

## Using Azure Developer CLI

Developers can use the [Azure Developer CLI](/azure/developer/azure-developer-cli/overview) `ai agent` extension for seamless and rapid provisioning and deployment of their agentic applications on Foundry. This extension simplifies the setup of foundry resources, models, tools and knowledge resources, Azure container registry for Bring-your-own (BYO) container, application insights for logging and monitoring, managed identity and Role Based Access Control - everything you need to get started with hosted agents with Foundry Agent Service. This extension is currently in preview. Microsoft does not recommend it for production use. 

**Get Started**

1. Install the [Azure Developer CLI](/azure/developer/azure-developer-cli/overview) on your device.

3. If you already have Azure Developer CLI installed, check if you have the latest version of `azd` CLI installed. 

    ```bash 
    azd version
    ``` 
To upgrade to the latest version, see the [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) documentation.
    
2. If you are starting with no existing Foundry resources and want to simplify all the required infrastructure provisioning and RBAC, download the Microsoft Foundry starter template, which automatically installs the  `ai agent` extension. 

    ```bash
    azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
    ```
    
    To check all installed extensions:
    
     ```bash
     azd ext list
     ```
     
   It is recommended to have the latest version of the Microsoft Foundry Agents extension installed.

   If you have an existing foundry project you want to deploy your agent in, and want to provision only the additional resources that may be needed for deploying your agent, run this command afterwards:

   ```bash
   azd ai agent init --project-id /subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/projects/[PROJECTNAME]
   ```  
   
3. Initialize the template by configuring the parameters in the agent definition:

     ```bash
     azd ai agent init -m <repo-path-to-agent.yaml>
     ```
   
The GitHub repo for an agent you want to host on foundry contains the application code, dependencies referenced, Dockerfile for containerization, and agent.yaml that contains your agent's definition. Set values for the parameters you are prompted for, to configure your agent. This registers your agent under 'Services' in `azure.yaml` of the downloaded template. You can get started with samples [on GitHub](https://github.com/azure-ai-foundry/foundry-samples).


4. To open and view all bicep and configuration files associated with your `azd` based deployments: 

     ```bash
     code .
     ```

5. Package, provision and deploy your agent code as a managed application on Foundry. 

    ```bash
    azd up
    ```
    
This command abstracts the underlying execution of commands `azd infra generate`, `azd provision` and `azd deploy`, and creates a hosted agent version and deployment on Foundry Agent Service. If you already have a version of a hosted agent, `azd` creates a new version of the same agent. See the [management section](#manage-hosted-agents) to learn more on how you can do non-versioned updates, start, stop, and delete your hosted agent deployments and versions. 

Make sure you have the [role based access](/azure/role-based-access-control/built-in-roles) enabled to provision the services and models `azd` is provisioning for you.

**Roles and permissions** 

If you have an existing foundry resource and will need to create a new foundry project to deploy a hosted agent, you require Account Owner and Azure AI user roles. 

If you have an existing project and want to create the model deployment and Azure container registry in the project, you will require Azure AI user and Account Owner roles on Foundry besides contributor on the Azure subscription.

If you have everything configured in the project to deploy a hosted agent, you will require Azure AI User and Reader roles.

**Resource clean-up** 

To prevent incurring unnecessary charges, it's important to clean up your Azure resources after completing your work with the application.

_When to clean up:_

  - After you have finished testing or demonstrating the application
  - If the application is no longer needed or you have transitioned to a different project or environment
  - When you have completed development and are ready to decommission the application
  
_Deleting Resources:_ To delete all associated resources and shut down the application, execute the following command:

```bash
azd down
```

That this process may take up to 20 minutes to complete. 

## Using the Microsoft Foundry SDK 

When you create a hosted agent, the system registers the agent definition in Microsoft Foundry and attempts to create a deployment for that agent version.

### Prerequisites for deployment

Before deploying a hosted agent, ensure you have:

* A container image hosted in [Azure Container Registry](https://azure.microsoft.com/services/container-registry/). For more information, see [Create a private container registry](/azure/container-registry/container-registry-get-started-portal)
* Access to assign roles in Azure Container Registry (you need at least `User Access Administrator` or `Owner` permissions on the container registry)
* The Azure AI Projects SDK installed: 

```bash
pip install azure-ai-projects
```

### Build and push your Docker image to Azure Container Registry

To build your agent as a Docker container and upload it to Azure Container Registry:

1. **Build your Docker image locally**:
   ```bash
   docker build -t myagent:v1 .
   ```

2. **Log in to your Azure Container Registry**:
   ```bash
   az acr login --name myregistry
   ```

3. **Tag your image for the registry**:
   ```bash
   docker tag myagent:v1 myregistry.azurecr.io/myagent:v1
   ```

4. **Push the image to ACR**:
   ```bash
   docker push myregistry.azurecr.io/myagent:v1
   ```

For detailed guidance on working with Docker images in Azure Container Registry, see [Push and pull Docker images](/azure/container-registry/container-registry-get-started-docker-cli).

### Configure Azure Container Registry permissions

Before creating the agent, give your project's managed identity access to pull from the container registry that houses your image. This step ensures all dependencies are available within the container.

1. **Find your Microsoft Foundry project's managed identity**:
   
   1. Go to the [Azure portal](https://portal.azure.com) and navigate to your Microsoft Foundry project resource.
   2. In the left pane, select **Identity**.
   3. Under **System assigned**, copy the **Object (principal) ID**. This is the managed identity you'll assign the ACR role to.

2. **Grant pull permissions**: Assign the `Container Registry Repository Reader` role to your project's managed identity on the container registry. For detailed steps, see [Azure Container Registry roles and permissions](/azure/container-registry/container-registry-roles).

### Create the hosted agent version 

Use the Azure AI Projects SDK to create and register your agent:

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition, ProtocolVersionRecord, AgentProtocol
from azure.identity import DefaultAzureCredential

# Initialize client
client = AIProjectClient(
    endpoint="https://your-project.services.ai.azure.com/api/projects/project-name",
    credential=DefaultAzureCredential()
)

# Create agent from container image
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

print(f"Agent created: {agent.id}")
```

#### Key parameters

- **PROJECT_ENDPOINT**: Your Microsoft Foundry project endpoint URL
- **AGENT_NAME**: Unique name for your agent
- **CONTAINER_IMAGE**: Full ACR image URL with tag
- **CPU/Memory**: Resource allocation (for example, "1" CPU, "2Gi" memory)

> [!NOTE]
> - Ensure your container image is accessible from the Microsoft Foundry project
> - DefaultAzureCredential handles authentication automatically
> - The agent appears in the Microsoft Foundry portal once created

## Manage hosted agents 

## Update an agent

You can update an agent in two ways: versioned updates that create a new agent version, or non-versioned updates that modify the min and max replica for your deployment. 

### Versioned update

Use a versioned update to modify the runtime configuration for your agent. This process creates a new version of the agent.

Changes that trigger a new version include:

- **Container image**: Updating to a new image or tag
- **Resource allocation**: Changing CPU or memory settings  
- **Environment variables**: Adding, removing, or modifying environment variables
- **Protocol versions**: Updating supported protocol versions

To create a new version, use the same `client.agents.create_version()` method shown in the creation example with your updated configuration.

### Non-versioned update

Use a non-versioned update to modify horizontal scale configuration (minimum and maximum replicas) or agent metadata such as description and tags. This process doesn't create a new version.

```bash
az cognitiveservices agent update
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Cognitive service account name |
| `--agent-version` | ✅ | Cognitive Services hosted agent version |
| `--name -n` | ✅ | Cognitive Services hosted agent name |
| `--project-name` | ✅ | AI Project name |
| `--description` | ❌ | Description of the agent |
| `--max-replicas` | ❌ | Maximum number of replicas for horizontal scaling |
| `--min-replicas` | ❌ | Minimum number of replicas for horizontal scaling |
| `--tags` | ❌ | Space-separated tags: key[=value] [key[=value] ...]. Use '' to clear existing tags |

**Example:**

```bash
az cognitiveservices agent update --account-name myAccount --project-name myProject --name myAgent --agent-version 1 --min-replicas 1 --max-replicas 2
```

## Start agent deployment

After creating your hosted agent version, you can start the deployment using `az` CLI to make it available for requests. You can also start a hosted agent that has been stopped.

```bash
az cognitiveservices agent start
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Cognitive service account name |
| `--agent-version` | ✅ | Cognitive Services hosted agent version |
| `--name -n` | ✅ | Cognitive Services hosted agent name |
| `--project-name` | ✅ | AI Project name |
| `--min-replicas` | ✅ | Minimum number of replicas for horizontal scaling |
| `--max-replicas` | ✅ | Maximum number of replicas for horizontal scaling |

**Example:**

```bash
az cognitiveservices agent start --account-name myAccount --project-name myProject --name myAgent --agent-version 1
```

When you start an agent:
- **Current status**: Stopped

- **Allowed operation**: Start

- **Transitory status**: Starting

- **Final status**: Started (if successful) or Failed (if unsuccessful)

### Stop an agent deployment

You can override the maximum replica configured for your agent deployment by setting it to zero and force stop the hosted agent using this command:

```bash
az cognitiveservices agent stop
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Cognitive service account name |
| `--agent-version` | ✅ | Cognitive Services hosted agent version |
| `--name -n` | ✅ | Cognitive Services hosted agent name |
| `--project-name` | ✅ | AI Project name |

**Example:**

```bash
az cognitiveservices agent stop --account-name myAccount --project-name myProject --name myAgent --agent-version 1
```

When you stop an agent:

- **Current status**: Running

- **Allowed operation**: Stop

- **Transitory status**: Stopping

- **Final status**: Stopped (if successful) or Running (if unsuccessful)

## Delete an agent

You can delete agents at different levels depending on what you want to remove:

### Delete a deployment only

Stops the running agent but keeps the agent version for future use:

```bash
az cognitiveservices agent delete-deployment
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Cognitive service account name |
| `--agent-version` | ✅ | Cognitive Services hosted agent version |
| `--name -n` | ✅ | Cognitive Services hosted agent name |
| `--project-name` | ✅ | AI Project name |

Use this when you want to stop the agent temporarily or switch to a different version.

### Delete the agent

Removes all versions and deployments for the agent:

If `agent_version` is provided, and the agent deployment has been deleted, the agent definition associated with that version is deleted. If the agent deployment is running, this operation will not succeed.

If `agent_version` is not provided, all agent versions associated with the agent name are deleted.

```bash
az cognitiveservices agent delete
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Cognitive service account name |
| `--name -n` | ✅ | Cognitive Services hosted agent name |
| `--project-name` | ✅ | AI Project name |
| `--agent-version` | ❌ | Cognitive Services hosted agent version. If not provided, deletes all versions |

Use this when you no longer need the agent and want to clean up all associated resources.

## List hosted agents

### List versions for an agent

List all versions of a hosted agent.

```bash
az cognitiveservices agent list-versions
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Cognitive service account name |
| `--name -n` | ✅ | Cognitive Services hosted agent name |
| `--project-name` | ✅ | AI Project name |

### Show details of a hosted agent

```bash
az cognitiveservices agent show
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | ✅ | Cognitive service account name |
| `--name -n` | ✅ | Cognitive Services hosted agent name |
| `--project-name` | ✅ | AI Project name |

---
## Invoke hosted agents

You can view and test hosted agents in the agent playground UI. Hosted agents expose an OpenAI Responses-compatible API that you can invoke using the OpenAI SDK.

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

# Initialize client and retrieve agent
client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
agent = client.agents.retrieve(agent_name=AGENT_NAME)

# Get OpenAI client and send message
openai_client = client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Hello! What can you help me with?"}],
    extra_body={"agent": AgentReference(name=agent.name, version=AGENT_VERSION).as_dict()}
)

print(f"Agent response: {response.output_text}")
```

## Use tools with hosted agents

Before your hosted agent can execute tools, create a connection to your remote MCP server on Foundry. 

The `RemoteMCPTool` connection supports these authentication mechanisms:
* **Stored credentials**: Use predefined credentials stored in the system
* **Project managed identity**: Use the Microsoft Foundry project's managed identity

### Choose your authentication method

- **For shared identity**: Use key-based or Microsoft Foundry Project Managed Identity authentication when every user of your agent should use the same identity. Individual user identity or context doesn't persist with these methods.

- **For individual user context**: Use OAuth Identity Passthrough when every user of your agent should use their own account to authenticate with the MCP server. This approach preserves personal user context.

To learn how to create the `RemoteMCPTool` connection, see [MCP server tool](../../../agents/how-to/tools/model-context-protocol.md).

Use the companion package with your local agent code to list and invoke tools from within your container.

```python
from azure.ai.agentshosting import tool_client, from_langgraph
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

async def agent_run(self, request_body: CreateResponse, context: AgentRunContext):
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
    model = AzureChatOpenAI(model=deployment_name)
    
    tools_client = await tool_client(context)

    try:
        tools = await tools_client.list_tools()
        agent = create_react_agent(model, tools)
        await from_langgraph(agent).run_async()
    except OAuthRequiresConsentException as oauthException:
        return ResponseOauthConsentRequestEvent(oauthException)
```
Hosted agents can also be used with Foundry built-in tools. Supported tools include:

- Code Interpreter
- Image Generation
- Web Search

Integrated support for additional Foundry tools coming soon.

## Observability with hosted agents

Hosted agents support exposing OpenTelemetry traces/metrics/logs from underlying frameworks to Microsoft Foundry with Application Insights or any user-specified OpenTelemetry Collector endpoint.

If you are using the `azd ai agent` CLI extension, app insights are automatically provisioned and connected to your Foundry project for you, and your project managed identity is granted **Azure AI User** role on the Foundry resource so traces are exported to Foundry Connected Application Insights.

If you are using the Foundry SDK, you  have to perform these steps independently. Learn more [in this article](/azure/ai-foundry/how-to/develop/trace-application#enable-tracing-in-your-project).

#### Azure Hosting Adapter provides the following:
- **Complete OpenTelemetry setup** - TracerProvider, MeterProvider, LoggerProvider
- **Auto-instrumentation** - HTTP requests, database calls, AI model calls
- **Azure Monitor integration** - Exporters, formatting, authentication
- **Performance optimization** - Sampling, batching, resource detection
- **Live metrics** - Real-time dashboard in Application Insights

### Local tracing

- Follow [Trace in AI Toolkit](https://code.visualstudio.com/docs/intelligentapps/tracing) to install and set up AI Toolkit for VS Code
- Setup/export environment variable **OTEL_EXPORTER_ENDPOINT**. You can find the endpoint from AI Toolkit in VS Code after clicking `Start Collector` button.
- Invoke the agent and find traces in AI Toolkit.

### Tracing in the Microsoft Foundry Portal

You can also review traces for your hosted agent in the **Traces** tab in the playground.

### Export traces to your OpenTelemetry compatible server

Use environment variable `OTEL_EXPORTER_ENDPOINT` to send traces to your own OpenTelemetry collector or compatible observability platform.

## Conversation management with hosted agents

Hosted agents integrate seamlessly with Microsoft Foundry's conversation management system, enabling stateful, multi-turn interactions without manual state management.

### How conversations work with hosted agents

**Conversation objects**: Microsoft Foundry automatically creates durable conversation objects with unique identifiers that persist across multiple agent interactions. When a user starts a conversation with your hosted agent, the platform maintains this conversation context automatically.

**State management**: Unlike traditional APIs where you manually pass conversation history, hosted agents receive conversation context automatically. The Microsoft Foundry runtime manages:
- Previous messages and responses
- Tool calls and their outputs  
- Agent instructions and configuration
- Conversation metadata and timestamps

**Conversation items**: Each conversation contains structured items that are automatically maintained:
- **Messages**: User inputs and agent responses with timestamps
- **Tool calls**: Function invocations with parameters and results
- **Tool outputs**: Structured responses from external services
- **System messages**: Internal state and context information

### Conversation persistence and reuse

**Cross-session continuity**: Conversations persist beyond individual requests, enabling users to return to previous discussions with full context maintained.

**Conversation reuse**: The same conversation can be accessed from multiple channels and applications while maintaining consistent state and history.

**Automatic cleanup**: Microsoft Foundry manages conversation lifecycle and cleanup based on your project's retention policies.

## Evaluation and testing for hosted agents

Microsoft Foundry provides comprehensive evaluation and testing capabilities specifically designed for hosted agents, enabling you to validate performance, compare versions, and ensure quality before deployment.

### Built-in evaluation capabilities

**Agent performance evaluation**: Microsoft Foundry includes built-in evaluation metrics to assess your hosted agent's effectiveness:
- Response quality and relevance
- Task completion accuracy
- Tool usage effectiveness
- Conversation coherence and context retention
- Response time and efficiency metrics

**Agent-specific evaluation**: Evaluate hosted agents using Azure AI Evaluation SDK with built-in evaluators designed specifically for agentic workflows. The SDK provides specialized evaluators for measuring agent performance across key dimensions like intent resolution, task adherence, and tool usage accuracy.

### Testing workflows for hosted agents

**Development testing**: Test your hosted agent locally during development using the agent playground and local testing tools before deployment.

**Staging validation**: Deploy to a staging environment to validate behavior with real Microsoft Foundry infrastructure while maintaining isolation from production.

**Production monitoring**: Continuously monitor deployed hosted agents with automated evaluation runs to detect performance degradation or issues.

### Structured evaluation approaches

**Test dataset creation**: Create comprehensive test datasets that cover:
- Common user interaction patterns
- Edge cases and error scenarios  
- Multi-turn conversation flows
- Tool usage scenarios
- Performance stress tests

**Supported evaluation metrics**: The Azure AI Evaluation SDK provides the following evaluators for agent workflows:

- **Intent Resolution**: Measures how well the agent identifies and understands user requests
- **Task Adherence**: Evaluates whether the agent's responses adhere to assigned tasks and system instructions  
- **Tool Call Accuracy**: Assesses whether the agent makes correct function tool calls for user requests
- **Additional Quality Metrics**: Relevance, Coherence, Fluency can also be used with agent messages

### Evaluation best practices

**Test with representative data**: Create evaluation datasets that represent your actual user interactions and use cases.

**Monitor agent performance**: Use the Microsoft Foundry portal to track agent performance and review conversation traces.

**Iterative evaluation**: Regularly evaluate agent versions during development to catch issues early and measure improvements.

For detailed information about evaluating agents, see [Evaluate AI agents](../../../how-to/develop/agent-evaluate-sdk.md) and [Agent evaluators](../../../concepts/evaluation-evaluators/agent-evaluators.md).

## Publish hosted agents to channels

Publishing transforms your hosted agent from a development asset into a managed Azure resource with a dedicated endpoint, independent identity, and governance capabilities. Once published, your hosted agent can be shared across multiple channels and platforms.

### Publishing process for hosted agents

When you publish a hosted agent, Microsoft Foundry automatically:

1. **Creates an Agent Application resource** with a dedicated invocation URL
2. **Provisions a distinct Agent Identity** separate from your project's shared identity  
3. **Registers the agent** in the Microsoft Entra Agent Registry for discovery and governance
4. **Enables stable endpoint access** that remains consistent as you deploy new agent versions

Unlike prompt-based agents that can be edited in the portal, hosted agents maintain their code-based implementation while gaining the same publishing and sharing capabilities.

### Available publishing channels

**Web application preview**: Get an instant shareable web interface to demonstrate and test your hosted agent with stakeholders.

**Microsoft 365 Copilot and Teams**: Integrate your hosted agent directly into Microsoft 365 Copilot and Microsoft Teams through a streamlined, no-code publishing flow. Your agent will appear in the Agent Store for organizational or shared scope distribution.

**Stable API endpoint**: Access your hosted agent programmatically through a consistent REST API that remains unchanged as you update agent versions.

**Custom applications**: Embed your hosted agent into existing applications using the stable endpoint and SDK integration.

### Publishing considerations for hosted agents

**Identity management**: Published hosted agents receive their own Agent Identity, requiring you to reconfigure permissions for any Azure resources your agent accesses. The shared development identity permissions don't automatically transfer.

**Version control**: Publishing creates a deployment that references your current agent version. You can update the published agent by deploying new versions without changing the public endpoint.

**Authentication**: Published agents support RBAC-based authentication by default, with automatic permission handling for Azure Bot Service integration when publishing to Microsoft 365 channels.

For detailed publishing instructions, see [Publish and share agents](../how-to/publish-agent.md). <!--For Microsoft 365 and Teams integration, see [Publish to Microsoft 365 Copilot and Teams](../how-to/publish-channels.md).-->

## Troubleshoot hosted agent endpoints
If your agent deployment fails, view error logs by clicking "view deployment logs". Refer to the table below for good next steps in case of 4xx errors. Reach out to Microsoft support in case of 5xx status codes returned from the agent endpoint.

| Error Classification | HTTP Status Code | Root Cause |
|----------------------|------------------|------------|
| SubscriptionIsNotRegistered | 400 | Register feature / subscription provider |
| InvalidAcrPullCredentials (AcrPullWithMSIFailed) | 401 | Fix managed identity / registry RBAC |
| UnauthorizedAcrPull (AcrPullUnauthorized) | 403 | Provide correct credentials / identity |
| AcrImageNotFound | 404 | Correct image name/tag or publish image |
| RegistryNotFound | 400/404 | Fix registry DNS/server spelling, network reachability |
| ValidationError | 400 | Correct invalid request fields |
| UserError (generic) | 400 | Inspect message, fix config |

## Limitations during public preview

| Dimension | Limit |
|-----------|-------|
| Microsoft Foundry resource per region per Azure subscription | 100 |
| Maximum number of agents per Foundry resource | 200 |
| Maximum min_replica count for an agent deployment | 2 |
| Maximum max_replica count for an agent deployment | 5 |

## Hosting pricing

Billing for managed hosting runtime will be enabled no earlier than February 1st 2026 during the preview. Please check our Foundry [pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/) for updates on pricing.

## Region availability

Hosted agents are supported in North Central US only (more region support coming soon).

## Next steps

* Learn about [agent development lifecycle](./development-lifecycle.md)
* Explore [agent identity concepts](./agent-identity.md) for authentication
* Understand [runtime components](./runtime-components.md) for response generation
* Discover available [tools in the catalog](./tool-catalog.md)
* See [how to publish your agent](../how-to/publish-agent.md) to share and deploy

## Related content

* [Azure Container Registry documentation](/azure/container-registry/)
* [Create projects in Microsoft Foundry](../../../how-to/create-projects.md)
* [Microsoft Foundry reference](../../../reference/region-support.md)
* [Agent samples and quickstarts](../../../quickstarts/get-started-code.md)