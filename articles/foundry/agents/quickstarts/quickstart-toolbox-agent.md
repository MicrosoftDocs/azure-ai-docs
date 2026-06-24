---
title: "Quickstart: Build a toolbox and use it with a hosted agent"
description: "Build a Foundry toolbox that combines web search and the Microsoft Learn MCP server, then consume it from a Python hosted agent that connects over the Model Context Protocol."
author: aahill
ms.author: aahi
ms.date: 06/16/2026
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

For the **VS Code** path, you also need [Visual Studio Code](https://code.visualstudio.com/) with the [Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio) extension, signed in to Azure.

## Step 1: Initialize the hosted agent

Initialize a hosted agent from the Foundry toolbox sample, which connects to a toolbox over MCP and exposes its tools to the model. You create the toolbox (`my-toolbox`) in the next step and point the agent at its endpoint. Run these commands in an empty directory.

```bash
mkdir my-toolbox-agent && cd my-toolbox-agent
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox/agent.manifest.yaml" --src src/toolbox-agent
```

Follow the prompts to select your project and an existing model deployment. When you're prompted to **Select container resource allocation**, choose **1 core, 2Gi memory**. The agent's container image needs more than the default tier. The `--src` flag scaffolds the agent into `src/toolbox-agent`.

## Step 2: Create the toolbox

Create the toolbox, then copy the MCP endpoint it returns. You set that endpoint as an environment variable in later steps.

First, point the toolbox commands at the Foundry project you selected during initialization. Reuse the endpoint that initialization already stored in your `azd` environment:

```bash
azd env set FOUNDRY_PROJECT_ENDPOINT "$(azd env get-value AZURE_AI_PROJECT_ENDPOINT)"
```

:::zone pivot="azd"

The sample includes a [`toolbox.yaml`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox/toolbox.yaml) in `src/toolbox-agent` that defines both tools behind one endpoint. Create the toolbox from that file:

```bash
azd ai toolbox create my-toolbox --from-file ./src/toolbox-agent/toolbox.yaml
```

The first version becomes the default version automatically. The command prints the toolbox's versioned MCP endpoint. Copy the `Endpoint` value from the output. You set it as the `TOOLBOX_ENDPOINT` environment variable in the next steps. It looks like this:

```
https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/my-toolbox/versions/1/mcp?api-version=v1
```

:::zone-end

:::zone pivot="vscode"

1. Open Visual Studio Code and select **Foundry Toolkit** in the Activity Bar.
1. Sign in to your Azure account if you're prompted.
1. Under **My Resources**, expand your project, then expand **Tools**.
1. In the **Tools** view, select the **+ Add Toolbox** icon.
1. Enter the toolbox name (`my-toolbox`) and a description.
1. Select **Web search**.
1. Select **+ Add tool**, choose to add a remote MCP server, and enter the server URL `https://learn.microsoft.com/api/mcp`. The server is public, so no authentication is required.
1. Select **Publish**. Publishing creates the first version of the toolbox.
1. Copy the toolbox's MCP endpoint. Run the following command and copy the `endpoint` value from the output. You set it as the `TOOLBOX_ENDPOINT` environment variable in the next steps:

    ```bash
    azd ai toolbox show my-toolbox --output json
    ```

:::zone-end

## Step 3: Provision Azure resources

The agent reads the toolbox's MCP endpoint from the `TOOLBOX_ENDPOINT` environment variable, which `src/toolbox-agent/agent.yaml` resolves from your `azd` environment. You set that value in the next steps. Provision the agent's Azure resources:

```bash
azd provision
```

## Step 4: Run the agent locally

1. Point the local agent at your toolbox by setting these values in the `.env` file in `src/toolbox-agent`. Paste the endpoint you copied in [Step 2](#step-2-create-the-toolbox):

    ```
    AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
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

Store the endpoint you copied in [Step 2](#step-2-create-the-toolbox) in your `azd` environment, which `agent.yaml` resolves at deploy time. Then build and deploy the agent container:

```bash
azd env set TOOLBOX_ENDPOINT "<versioned-endpoint-from-step-2>"
azd deploy
```

When the command finishes, the output shows links to the agent playground and the agent endpoint. Invoke the deployed agent:

```bash
azd ai agent invoke "What's new in Azure AI Foundry? Use the Microsoft Learn documentation."
```

## Clean up resources

Delete the resources when you're finished so you stop incurring charges.

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

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `tools/list` returns no Microsoft Learn tools | Confirm the `mslearn` tool in `toolbox.yaml` points at `https://learn.microsoft.com/api/mcp`. |
| The agent starts but reports `TOOLBOX_ENDPOINT is set but empty` or has no tools | Set `TOOLBOX_ENDPOINT` to the versioned endpoint from Step 2 in `.env` for local runs, and run `azd env set TOOLBOX_ENDPOINT "<endpoint>"` before you deploy. |
| Calls to the toolbox endpoint fail with an authorization or header error | Confirm every request includes the `Foundry-Features: Toolboxes=V1Preview` header and an Entra token scoped to `https://ai.azure.com/.default`. The sample handles this for you. |
| `Connection refused` on local run | Ensure no other process is using port `8088`. |

## What you learned

In this quickstart, you:

- Built a toolbox that combines web search and the Microsoft Learn MCP server behind one endpoint.
- Consumed the toolbox from a Python hosted agent that connects over the Model Context Protocol.
- Ran the agent locally and deployed it to Foundry Agent Service.

## Next step

> [!div class="nextstepaction"]
> [Add a Foundry IQ knowledge base to a hosted agent](quickstart-foundry-iq-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Curate an intent-based toolbox in Foundry](../how-to/tools/toolbox.md)
- [Web search tool](../how-to/tools/web-search.md)
- [Connect agents to Model Context Protocol servers](../how-to/tools/model-context-protocol.md)
- [Quickstart: Deploy your first hosted agent](quickstart-hosted-agent.md)
