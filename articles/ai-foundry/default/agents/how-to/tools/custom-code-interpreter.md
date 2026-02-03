---
title: Use custom code interpreter with agents
titleSuffix: Microsoft Foundry
description: Configure a custom code interpreter for Microsoft Foundry agents. Customize Python packages and compute by using Azure Container Apps Dynamic Sessions and MCP.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/19/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Custom code interpreter tool for agents (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

By using a custom code interpreter for your agent, you can customize the resources, available Python packages, and [Azure Container Apps environment](/azure/container-apps/environment) that the agent uses to run the Python code it writes. The code interpreter container exposes a Model Context Protocol (MCP) server.

Use a custom code interpreter when you need more control over the runtime than the built-in [Code Interpreter tool for agents](code-interpreter.md) provides.

For more information about MCP and how agents connect to MCP tools, see [Connect to Model Context Protocol servers (preview)](model-context-protocol.md).

## Usage support

This article uses the Azure CLI and a runnable sample project.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | - | - | - | ✔️ | - | ✔️ |

For the latest SDK and API support for agents tools, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Prerequisites

To use the preview feature, you need the following prerequisites:

- The [Azure CLI](/cli/azure/install-azure-cli).
- Optionally install `uv` as an alternative to `pip`. `uv` is a fast package and project manager for Python projects. You can install it by following the instructions at [Installing uv](https://docs.astral.sh/uv/getting-started/installation/) in the official documentation.
- An Azure subscription and resource group with the following permissions:
  - [Azure AI Owner](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-owner)
  - [Container Apps ManagedEnvironment Contributor](/azure/role-based-access-control/built-in-roles/containers#container-apps-managedenvironments-contributor)
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true) for details.

### Environment variables

Set these environment variables after provisioning the infrastructure:

| Variable | Description |
| --- | --- |
| `FOUNDRY_PROJECT_ENDPOINT` | Your Foundry project endpoint URL. |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Your model deployment name (for example, `gpt-4o`). |
| `MCP_SERVER_URL` | The MCP server endpoint from your Azure Container Apps deployment. |
| `MCP_PROJECT_CONNECTION_ID` | Your project connection ID for the custom code interpreter. |

## Before you begin

This procedure provisions Azure infrastructure, including Azure Container Apps resources. Review Azure cost and governance requirements for your organization before you deploy.

## Custom code interpreter example

The following console commands and code samples show how to create an agent that uses a custom code interpreter MCP server.

### Enable MCP server for dynamic sessions

To enable the preview feature, run the following commands.

```console
az feature register --namespace Microsoft.App --name SessionPoolsSupportMCP
az provider register -n Microsoft.App
```

### Get the sample code

Clone the [sample code in the GitHub repo](https://github.com/azure-ai-foundry/foundry-samples) and navigate to the `samples/python/hosted-agents/code-interpreter-custom` folder in your terminal.

### Provision the infrastructure

To provision the infrastructure, run the following command by using the Azure CLI (`az`):

```console
az deployment group create \
    --name custom-code-interpreter \
    --subscription <your_subscription> \
    --resource-group <your_resource_group> \
    --template-file ./infra.bicep
```

> [!NOTE]
> This process can take a while. Allocating the dynamic session pool can take up to one hour, depending on the number of standby instances you request.

### Use the custom code interpreter in an agent

Copy the `.env.sample` file from the repository to `.env` and fill in the values with the output from the preceding deployment. You can find this output in the Azure portal under the resource group.

Install the Python dependencies by using `uv sync` or `pip install`. Finally, run `./main.py`.

### Quick verification

Before running the full sample, verify your authentication and project connection:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=credential) as project_client,
):
    print("Connected to project.")
    # List connections to verify MCP connection exists
    connections = project_client.connections.list()
    for conn in connections:
        print(f"  Connection: {conn.name} (type: {conn.type})")
```

If this code runs without errors, your credentials and project endpoint are configured correctly.

### Code example

The following Python sample shows how to create an agent with a custom code interpreter MCP tool:

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

with project_client:
    openai_client = project_client.get_openai_client()

    # Configure the custom code interpreter MCP tool
    custom_code_interpreter = MCPTool(
        server_label="custom-code-interpreter",
        server_url=os.environ["MCP_SERVER_URL"],
        project_connection_id=os.environ.get("MCP_PROJECT_CONNECTION_ID"),
    )

    agent = project_client.agents.create_version(
        agent_name="CustomCodeInterpreterAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that can run Python code to analyze data and solve problems.",
            tools=[custom_code_interpreter],
        ),
        description="Agent with custom code interpreter for data analysis.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Test the agent with a simple calculation
    response = openai_client.responses.create(
        input="Calculate the factorial of 10 using Python.",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response: {response.output_text}")

    # Clean up
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```

### Expected output

When you run the sample, you see output similar to:

```console
Agent created (id: agent-xxxxxxxxxxxx, name: CustomCodeInterpreterAgent, version: 1)
Response: The factorial of 10 is 3,628,800. I calculated this using Python's math.factorial() function.
Agent deleted
```

## Verify your setup

After you provision the infrastructure and run the sample:

1. Confirm the Azure deployment completes successfully.
1. Confirm the sample can connect by using the values in your `.env` file.
1. In Microsoft Foundry, verify your agent calls the tool by using tracing. For more information, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| Feature registration is still pending | The `az feature register` command returns `Registering` state. | Wait for registration to complete (can take 15-30 minutes). Check status with `az feature show --namespace Microsoft.App --name SessionPoolsSupportMCP`. Then run `az provider register -n Microsoft.App` again. |
| Deployment fails with permission error | Missing required role assignments. | Confirm you have **Azure AI Owner** and **Container Apps ManagedEnvironment Contributor** roles on the subscription or resource group. |
| Deployment fails with region error | The selected region doesn't support Azure Container Apps Dynamic Sessions. | Try a different region. See [Azure Container Apps regions](/azure/container-apps/overview#regions) for supported regions. |
| Agent doesn't call the tool | The MCP connection isn't configured correctly, or the agent instructions don't prompt tool use. | Use tracing in Microsoft Foundry to confirm tool invocation. Verify the `MCP_SERVER_URL` matches your deployed Container Apps endpoint. See [Best practices](../../concepts/tool-best-practice.md). |
| MCP server connection timeout | The Container Apps session pool isn't running or has no standby instances. | Check the session pool status in the Azure portal. Increase `standbyInstanceCount` in your Bicep template if needed. |
| Code execution fails in container | Missing Python packages in the custom container. | Update your container image to include required packages. Rebuild and redeploy the container. |
| Authentication error connecting to MCP server | The project connection credentials are invalid or expired. | Regenerate the connection credentials and update the `.env` file. Verify the `MCP_PROJECT_CONNECTION_ID` format. |

## Limitations

The APIs don't directly support file input or output, or the use of file stores. To get data in and out, you must use URLs, such as data URLs for small files and Azure Blob Service shared access signature (SAS) URLs for large files.

## Security

If you use SAS URLs to pass data in or out of the runtime:

- Use short-lived SAS tokens.
- Don't log SAS URLs or store them in source control.
- Scope permissions to the minimum required (for example, read-only or write-only).

## Clean up

To stop billing for provisioned resources, delete the resources created by the sample deployment. If you used a dedicated resource group for this article, delete the resource group.

## Related content

- [Connect to Model Context Protocol servers (preview)](model-context-protocol.md)
- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Azure Container Apps Dynamic Sessions](/azure/container-apps/sessions)
- [Session pools with custom containers](/azure/container-apps/session-pool#custom-container-pool)
- [Azure Container Apps environment](/azure/container-apps/environment)
- [Install the Azure CLI](/cli/azure/install-azure-cli)
- [Code Interpreter tool for agents](code-interpreter.md)
