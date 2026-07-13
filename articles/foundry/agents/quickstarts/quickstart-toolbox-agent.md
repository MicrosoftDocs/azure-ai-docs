---
title: "Quickstart: Build a toolbox and use it with a hosted agent"
description: "Build a Foundry toolbox that combines web search and the Microsoft Learn MCP server, then consume it from a Python hosted agent that connects over the Model Context Protocol."
author: mattwojo
ms.author: mattwoj
ms.reviewer: lindazqli
ms.date: 07/09/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-toolbox-quickstart
# customer intent: As a developer, I want to build a toolbox that combines several tools behind one endpoint so that my hosted agent can discover and call them all through a single connection.
---

# Quickstart: Build a toolbox and use it with a hosted agent

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this quickstart, you build a [toolbox](../how-to/tools/toolbox.md) that combines two tools behind one managed endpoint:

- **Web search**, which grounds responses in real-time public web results.
- The **Microsoft Learn MCP server**, which grounds responses in official Microsoft documentation. It's a public endpoint that requires no authentication.

You then consume the toolbox from a [hosted agent](../concepts/hosted-agents.md) written in Python. The toolbox exposes one MCP endpoint, so the agent connects to a single URL and discovers every tool at runtime. You can change the tools later without changing agent code.

## Prerequisites

This quickstart builds on the hosted-agent toolchain. Complete the [Prerequisites](quickstart-hosted-agent.md#prerequisites) in the hosted agent quickstart first, which cover the Azure subscription, project roles, Python, the Azure Developer CLI (`azd`), and the `microsoft.foundry` extension.

:::zone pivot="python"

For the Python SDK path, use the Python section later in this article instead
of the Azure Developer CLI or VS Code workflow. That path creates the
toolbox with `project_client.toolboxes.create_version(...)`, then uploads the
hosted-agent code as a new version and points it at that toolbox by name.

Install the Python packages used in this path:

```bash
pip install "azure-ai-projects>=2.3.0" azure-identity python-dotenv
```

You need an existing Foundry project with a deployed chat-capable model. The
Python SDK path in this quickstart creates the toolbox and the hosted-agent
version, but it doesn't scaffold a new Foundry project or create a model
deployment for you.

:::zone-end

:::zone pivot="vscode"

You also need [Visual Studio Code](https://code.visualstudio.com/) with the
[Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
extension, signed in to Azure.

:::zone-end

## Step 1: Initialize the hosted agent

Initialize a hosted agent from the Foundry toolbox sample, which connects to a toolbox over MCP and exposes its tools to the model. You create the toolbox (`my-toolbox`) in the next step and point the agent at its endpoint. Run these commands in an empty directory.

```bash
mkdir my-toolbox-agent && cd my-toolbox-agent
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox/azure.yaml" --src src/toolbox-agent
```

Follow the prompts to select your project and an existing model deployment. When you're prompted to **Select container resource allocation**, choose **1 core, 2Gi memory**. The agent's container image needs more than the default tier. The `--src` flag scaffolds the agent into `src/toolbox-agent`.

> [!NOTE]
> Agent manifests (`agent.manifest.yaml`) and standalone agent definitions (`agent.yaml`) are deprecated. As of the Foundry `azd` extensions (`azure.ai.agents` 1.0.0-beta.1), all hosted agent configuration lives in a single `azure.yaml`. See [Author azure.yaml for hosted agents](../how-to/author-azure-yaml.md).

## Step 2: Create the toolbox

Create the toolbox, and then copy the MCP endpoint it returns. Set that endpoint as an environment variable in later steps.

The sample's `azure.yaml` defines the toolbox as an `azure.ai.toolbox` service and wires it to the hosted agent service with `uses:`. If you change the toolbox configuration, edit the toolbox service in `azure.yaml`, not `src/toolbox-agent/agent.yaml`.

First, point the toolbox commands at the Foundry project you selected during initialization. Reuse the endpoint that initialization already stored in your `azd` environment:

```bash
azd env set FOUNDRY_PROJECT_ENDPOINT "$(azd env get-value FOUNDRY_PROJECT_ENDPOINT)"
```

:::zone pivot="azd"

The sample includes a [`toolbox.yaml`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox/toolbox.yaml) in `src/toolbox-agent` that defines both tools behind one endpoint. Create the toolbox from that file:

```bash
azd ai toolbox create my-toolbox --from-file ./src/toolbox-agent/toolbox.yaml
```

The first version becomes the default version automatically. The command prints the toolbox's versioned MCP endpoint. Copy the `Endpoint` value from the output. Set it as the `TOOLBOX_ENDPOINT` environment variable in the next steps. It looks like this:

```text
https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/my-toolbox/versions/1/mcp?api-version=v1
```

:::zone-end

:::zone pivot="vscode"

1. Open Visual Studio Code and select **Foundry Toolkit** in the Activity Bar.
1. Sign in to your Azure account if you're prompted.
1. Under **My Resources**, expand your project, and then expand **Tools**.
1. In the **Tools** view, select the **+ Add Toolbox** icon.
1. Enter the toolbox name (`my-toolbox`) and a description.
1. Select **Web search**.
1. Select **+ Add tool**, choose to add a remote MCP server, and enter the server URL `https://learn.microsoft.com/api/mcp`. The server is public, so no authentication is required.
1. Select **Publish**. Publishing creates the first version of the toolbox.
1. Copy the toolbox's MCP endpoint. Run the following command and copy the `endpoint` value from the output. Set it as the `TOOLBOX_ENDPOINT` environment variable in the next steps:

    ```bash
    azd ai toolbox show my-toolbox --output json
    ```

:::zone-end

## Step 3: Provision Azure resources

The agent reads the toolbox's MCP endpoint from the `TOOLBOX_ENDPOINT` environment variable, which `azure.yaml` resolves from your `azd` environment. You set that value in the next steps. Provision the agent's Azure resources:

```bash
azd provision
```

## Step 4: Run the agent locally

1. Point the local agent at your toolbox by setting these values in the `.env` file in `src/toolbox-agent`. Paste the endpoint you copied in [Step 2](#step-2-create-the-toolbox):

    ```text
    FOUNDRY_MODEL_NAME=<your-model-deployment-name>
    TOOLBOX_ENDPOINT=<versioned-endpoint-from-step-2>
    ```

    `azd ai agent run` injects `FOUNDRY_PROJECT_ENDPOINT` and reads the `.env` file for local runs. The sample handles the toolbox connection, headers, and authentication for you.

1. Start the agent:

    ```bash
    azd ai agent run
    ```

    This command creates a virtual environment, installs dependencies, and serves the agent on `http://localhost:8088`. Preview packages can produce pip warnings during setup. These warnings are nonblocking.

1. In a separate terminal, send prompts that exercise the tools:

    ```bash
    azd ai agent invoke --local "Find the latest release notes for the Azure CLI on the web."
    azd ai agent invoke --local "How do I create a hosted agent in Microsoft Foundry? Use the Microsoft Learn documentation."
    ```

## Step 5: Deploy to Foundry Agent Service

Store the endpoint you copied in [Step 2](#step-2-create-the-toolbox) in your `azd` environment, which `azure.yaml` resolves at deploy time. Then build and deploy the agent container:

```bash
azd env set TOOLBOX_ENDPOINT "<versioned-endpoint-from-step-2>"
azd deploy
```

When the command finishes, the output shows links to the agent playground and the agent endpoint. Invoke the deployed agent:

```bash
azd ai agent invoke "What's new in Microsoft Foundry? Use the Microsoft Learn documentation."
```

:::zone pivot="python"

## Python SDK path

Use the following steps if you want to create the toolbox and deploy the
hosted-agent version by using the Python SDK instead of the Azure Developer CLI or
VS Code flow.

### 1. Create or choose a Foundry project

1. Open [Foundry portal](https://ai.azure.com) and create a Foundry project, or
   select an existing one.
1. In the project, deploy a chat-capable model such as `gpt-5.4-mini`.
1. Copy the project endpoint from **Overview** and the deployment name from
   **Build** > **Deployments**.

### 2. Download the toolbox hosted-agent sample

Clone the Foundry samples repo:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
```

Create a working folder for the deployment scripts. In that folder, create a
`.env` file with these values:

```text
FOUNDRY_PROJECT_ENDPOINT=<your-project-endpoint>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
FOUNDRY_HOSTED_AGENT_NAME=toolbox-agent
TOOLBOX_NAME=my-toolbox
FOUNDRY_SAMPLE_PATH=<full-path-to-foundry-samples/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox/src/agent-framework-agent-with-foundry-toolbox-responses>
```

## Step 3: Create the toolbox with Python

Create a file named `create_toolbox.py` in the same working folder as `.env`:

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPToolboxTool, WebSearchToolboxTool
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
toolbox_name = os.environ["TOOLBOX_NAME"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
):
    created = project_client.toolboxes.create_version(
        name=toolbox_name,
        description="Toolbox with web search and Microsoft Learn MCP.",
        tools=[
            WebSearchToolboxTool(
                name="web_search",
                search_context_size="medium",
            ),
            MCPToolboxTool(
                server_label="mslearn",
                server_url="https://learn.microsoft.com/api/mcp",
                require_approval="never",
            ),
        ],
    )
    print(f"Created toolbox version {created.version} for {created.name}")

    toolbox = project_client.toolboxes.get(name=toolbox_name)
    mcp_endpoint = (
        f"{endpoint}/toolboxes/{toolbox.name}/versions/"
        f"{toolbox.default_version}/mcp?api-version=v1"
    )
    print(f"Default toolbox version: {toolbox.default_version}")
    print(f"Toolbox MCP endpoint: {mcp_endpoint}")
```

Run the script:

```bash
python create_toolbox.py
```

The sample hosted agent can resolve the toolbox either from `TOOLBOX_ENDPOINT`
or from `FOUNDRY_PROJECT_ENDPOINT` plus `TOOLBOX_NAME`. This path uses
`TOOLBOX_NAME`, so you don't need to store the versioned endpoint in `.env`.

### 4. Deploy the hosted agent with Python

Create a file named `deploy_toolbox_agent.py` in the same working folder as
`.env`:

```python
import os
import tempfile
import time
import zipfile
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpointConfig,
    CodeConfiguration,
    CodeDependencyResolution,
    FixedRatioVersionSelectionRule,
    HostedAgentDefinition,
    ProtocolConfiguration,
    ProtocolVersionRecord,
    ResponsesProtocolConfiguration,
    VersionSelector,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_name = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]
agent_name = os.environ.get("FOUNDRY_HOSTED_AGENT_NAME", "toolbox-agent")
toolbox_name = os.environ["TOOLBOX_NAME"]
sample_path = Path(os.environ["FOUNDRY_SAMPLE_PATH"]).resolve()


def create_code_zip(source_dir: Path) -> Path:
    zip_path = Path(tempfile.gettempdir()) / f"{agent_name}.zip"
    excluded = {".git", ".venv", "__pycache__", ".env"}

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for path in source_dir.rglob("*"):
            if not path.is_file():
                continue
            if any(part in excluded for part in path.parts):
                continue
            zip_file.write(path, path.relative_to(source_dir))

    return zip_path


def wait_for_active_version(project_client: AIProjectClient, version: str) -> None:
    for attempt in range(60):
        time.sleep(10)
        details = project_client.agents.get_version(
            agent_name=agent_name,
            agent_version=version,
        )
        status = details["status"]
        print(f"Provisioning status: {status} (attempt {attempt + 1}/60)")

        if status == "active":
            return

        if status == "failed":
            raise RuntimeError(f"Hosted agent provisioning failed: {dict(details)}")

    raise RuntimeError("Timed out waiting for the hosted agent version to become active.")


code_zip_path = create_code_zip(sample_path)

with (
    code_zip_path.open("rb") as code_stream,
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
):
    original_agent_endpoint = None
    created = None

    try:
        created = project_client.agents.create_version_from_code(
            agent_name=agent_name,
            description="Hosted agent with Foundry Toolbox integration.",
            definition=HostedAgentDefinition(
                cpu="1",
                memory="2Gi",
                code_configuration=CodeConfiguration(
                    runtime="python_3_13",
                    entry_point=["python", "main.py"],
                    dependency_resolution=CodeDependencyResolution.REMOTE_BUILD,
                ),
                environment_variables={
                    "FOUNDRY_PROJECT_ENDPOINT": endpoint,
                    "AZURE_AI_MODEL_DEPLOYMENT_NAME": model_name,
                    "TOOLBOX_NAME": toolbox_name,
                },
                protocol_versions=[
                    ProtocolVersionRecord(protocol="responses", version="2.0.0")
                ],
            ),
            code=code_stream,
        )

        print(f"Created hosted agent version {created.version}")
        wait_for_active_version(project_client, created.version)

        original_agent_endpoint = project_client.agents.get(
            agent_name=agent_name
        ).agent_endpoint
        project_client.agents.update_details(
            agent_name=agent_name,
            agent_endpoint=AgentEndpointConfig(
                version_selector=VersionSelector(
                    version_selection_rules=[
                        FixedRatioVersionSelectionRule(
                            agent_version=created.version,
                            traffic_percentage=100,
                        ),
                    ]
                ),
                protocol_configuration=ProtocolConfiguration(
                    responses=ResponsesProtocolConfiguration()
                ),
            ),
        )

        with project_client.get_openai_client(agent_name=agent_name) as openai_client:
            response = openai_client.responses.create(
                input=(
                    "How do I create a hosted agent in Microsoft Foundry? "
                    "Use the Microsoft Learn documentation."
                ),
            )
            print(response.output_text)
    finally:
        if original_agent_endpoint is not None:
            project_client.agents.update_details(
                agent_name=agent_name,
                agent_endpoint=original_agent_endpoint,
            )

        if created is not None:
            project_client.agents.delete_version(
                agent_name=agent_name,
                agent_version=created.version,
                force=True,
            )
```

Run the script:

```bash
python deploy_toolbox_agent.py
```

This script uploads the toolbox sample as a new hosted-agent version, points
the hosted agent at that version temporarily, invokes it with a Microsoft Learn
question, and restores the previous endpoint configuration when it finishes.

### 5. Verify the toolbox-backed response

If you configure the toolbox correctly, the response shows that the
hosted agent discovered the toolbox tools and answered by using Microsoft Learn
documentation.

:::zone-end

## Clean up resources

Delete the resources when you're finished so you stop incurring charges.

:::zone pivot="azd"

Delete the toolbox:

```bash
azd ai toolbox delete my-toolbox --force
```

After you delete the toolbox, its endpoint stops working. Remove it from `src/toolbox-agent/.env` and clear it from your `azd` environment:

```bash
azd env set TOOLBOX_ENDPOINT ""
```

Delete the agent and its Azure resources:

> [!WARNING]
> `azd down` permanently deletes every resource in the resource group, including the Foundry project, model deployments, Container Registry, and the hosted agent. If you provisioned into a resource group that contains other resources, those resources are deleted too.

```bash
azd down
```

:::zone-end

:::zone pivot="python"

Delete the toolbox by name:

```python
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=credential,
    ) as project_client,
):
    project_client.toolboxes.delete(name=os.environ["TOOLBOX_NAME"])
```

If you created a dedicated resource group or project for this quickstart,
delete it from the Azure portal after you no longer need the toolbox, chat
deployment, or hosted agent.

:::zone-end

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `tools/list` returns no Microsoft Learn tools | Confirm the `mslearn` tool in `toolbox.yaml` points at `https://learn.microsoft.com/api/mcp`. |
| The agent starts but reports `TOOLBOX_ENDPOINT is set but empty` or has no tools | Set `TOOLBOX_ENDPOINT` to the versioned endpoint from Step 2 in `.env` for local runs, and run `azd env set TOOLBOX_ENDPOINT "<endpoint>"` before you deploy. |
| Calls to the toolbox endpoint fail with an authorization error | Confirm every request includes an Entra token scoped to `https://ai.azure.com/.default`. The sample handles this for you. |
| `Connection refused` on local run | Ensure no other process is using port `8088`. |

## What you learned

In this quickstart, you:

- Built a toolbox that combines web search and the Microsoft Learn MCP server behind one endpoint.
- Consumed the toolbox from a Python hosted agent that connects over the Model Context Protocol by using Azure Developer CLI or the Python SDK.
- Ran the agent locally or validated it remotely and deployed it to Foundry Agent Service.

## Next step

> [!div class="nextstepaction"]
> [Add a Foundry IQ knowledge base to a hosted agent](quickstart-foundry-iq-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Curate an intent-based toolbox in Foundry](../how-to/tools/toolbox.md)
- [Web search tool](../how-to/tools/web-search.md)
- [Connect agents to Model Context Protocol servers](../how-to/tools/model-context-protocol.md)
- [Quickstart: Deploy your first hosted agent](quickstart-hosted-agent.md)
