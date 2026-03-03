---
title: Create hosted agent workflows in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Create, test, and deploy hosted agent workflows in Foundry Agent Service by using the Microsoft Foundry for Visual Studio Code extension.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 02/18/2026
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: ai-foundry-vsc-extension-languages
#CustomerIntent: As a developer, I want to create and deploy hosted agent workflows in VS Code so that I can build multi-agent solutions without leaving my IDE.
---

# Create hosted agent workflows in Visual Studio Code (preview)

Create, test, and deploy [hosted Foundry Agent workflows](../concepts/hosted-agents.md) by using the [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry). Hosted workflows let multiple agents collaborate in sequence, each with its own model, tools, and instructions.

Before you start, [build an agent in Foundry Agent Service](/azure/ai-foundry/how-to/develop/vs-code-agents?view=foundry&preserve-view=true) by using the extension. You can then add hosted workflows to that agent.

This article covers creating a workflow project, running it locally, visualizing the execution, and deploying it to your Foundry workspace.

## Prerequisites

- A Foundry project with a deployed model, or an Azure OpenAI resource.
- The [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) installed.
- The project's managed identity with the [Azure AI User](https://aka.ms/foundry-ext-project-role) and [AcrPull](/azure/role-based-access-control/built-in-roles/containers#acrpull) roles assigned. Also assign the `acrPull` role to the managed identity of the Foundry project where you plan to deploy the hosted agent.
- A [supported region](../concepts/hosted-agents.md#region-availability) for hosted agents.

::: zone pivot="python"
- Python 3.10 or higher.
::: zone-end

::: zone pivot="csharp"
- [.NET 9 SDK](https://dotnet.microsoft.com/download) or later.
::: zone-end

## Create a hosted agent workflow  

You can use the Foundry for Visual Studio Code extension to create hosted agent workflows. A hosted agent workflow is a sequence of agents that work together to accomplish a task. Each agent in the workflow can have its own model, tools, and instructions.

1. Open the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>).

1. Run this command: `>Microsoft Foundry: Create a New Hosted Agent`.

1. Select a programming language.

1. Select a folder where you want to save your new workflow.

1. Enter a name for your workflow project.

A new folder is created with the necessary files for your hosted agent project, including a sample code file to get you started.

### Install dependencies

Install the required dependencies for your hosted agent project. The dependencies vary based on the programming language that you selected when you created the project.
::: zone pivot="python"

1. Create virtual environment.

   ```bash
    python -m venv .venv
   ```

1. Activate the virtual environment.

   ```bash
   # PowerShell
   ./.venv/Scripts/Activate.ps1

   # Windows cmd
   .venv\Scripts\activate.bat

   # Unix/MacOS
   source .venv/bin/activate
   ```

1. Install the following package:

    ```bash
    pip install azure-ai-agentserver-agentframework
    ```

::: zone-end

::: zone pivot="csharp"

1. Go to your project directory and run this command to get the necessary NuGet packages:

    ```bash
    dotnet restore
    ```
::: zone-end

## Run your hosted workflow locally

::: zone pivot="python"
The sample workflow project creates an .env file with the necessary environment variables. Create or update the .env file with your Foundry credentials:

```
AZURE_AI_PROJECT_ENDPOINT=https://<your-resource-name>.services.ai.azure.com/api/projects/<your-project-name>

AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

> [!IMPORTANT]
> Never commit the `.env` file to version control. Add it to your `.gitignore` file.

### Authenticate your hosted agent

The hosted agent sample authenticates using [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python&preserve-view=true). Configure your development environment to provide credentials via one of the supported sources, for example:

- Azure CLI (`az login`)
- Visual Studio Code account sign-in
- Visual Studio account sign-in
- Environment variables for a service principal (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

Confirm authentication locally by running either the Azure CLI `az account show` or `az account get-access-token` commands before running the sample.

You can run the hosted agent in interactive mode or container mode.

### Run your hosted agent in interactive mode

Press **F5** in VS Code to start debugging. Alternatively, you can use the VS Code debug menu:

1. Open the **Run and Debug** view (Ctrl+Shift+D / Cmd+Shift+D)
2. Select **"Debug Local Workflow HTTP Server"** from the dropdown
3. Select the green **Start Debugging** button (or press F5)

This will:

1. Start the HTTP server with debugging enabled
2. Open the AI Toolkit Agent Inspector for interactive testing
3. Allow you to set breakpoints and inspect the workflow execution in real time.

### Run your hosted agent in container mode

> [!TIP]
> Open the local playground before starting the container agent to ensure the visualization functions correctly.

To run the hosted agent in container mode:
1. Open the Visual Studio Code Command Palette and execute the `Microsoft Foundry: Open Container Agent Playground Locally` command.
1. Execute `main.py` to initialize the containerized hosted agent.
1. Submit a request to the agent through the playground interface. For example, enter a prompt such as: "Create a slogan for a new electric SUV that's affordable and fun to drive."
1. Review the agent's response in the playground interface.

::: zone-end

::: zone pivot="csharp"

The sample workflow project creates an .env file with the necessary environment variables. Create or update the .env file with your Foundry credentials:

1. Set up your environment variables based on your operating system:

   #### [Windows (PowerShell)](#tab/windows-powershell)

   ```powershell
   $env:AZURE_AI_PROJECT_ENDPOINT="https://<your-resource-name>.services.ai.azure.com/api/projects/<your-project-name>"
   $env:AZURE_AI_MODEL_DEPLOYMENT_NAME="your-deployment-name"
   ```

   #### [Windows (command prompt)](#tab/windows-command-prompt)

   ```dos
   set AZURE_AI_PROJECT_ENDPOINT=https://your-resource-name.openai.azure.com/
   set AZURE_AI_MODEL_DEPLOYMENT_NAME=your-deployment-name
   ```

   #### [macOS/Linux (Bash)](#tab/macos-linux-bash)

   ```bash
   export AZURE_AI_PROJECT_ENDPOINT="https://your-resource-name.openai.azure.com/"
   export AZURE_AI_MODEL_DEPLOYMENT_NAME="your-deployment-name"
   ```

    ---

### Authenticate your hosted agent

The hosted agent sample authenticates using [DefaultAzureCredential](/dotnet/azure/sdk/authentication/credential-chains?tabs=dac#defaultazurecredential-overview). Configure your development environment to provide credentials via one of the supported sources, for example:

- Azure CLI (`az login`)
- Visual Studio Code account sign-in
- Visual Studio account sign-in
- Environment variables for a service principal (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

Confirm authentication locally by running either the Azure CLI `az account show` or `az account get-access-token` commands before running the sample.

You can run the hosted agent in interactive mode or container mode.

### Run your hosted agent in interactive mode

Run the hosted agent directly for development and testing:

```bash
dotnet restore
dotnet build
dotnet run
```

### Run your hosted agent in container mode

> [!TIP]
> Open the local playground before starting the container agent to ensure the visualization functions correctly.

To run the agent in container mode:

1. Open the Visual Studio Code Command Palette and execute the `Microsoft Foundry: Open Container Agent Playground Locally` command.
2. Use the following command to initialize the containerized hosted agent.
   ```bash
   dotnet restore
   dotnet build
   dotnet run
   ```
3. Submit a request to the agent through the playground interface. For example, enter a prompt such as: "Create a slogan for a new electric SUV that's affordable and fun to drive."
4. Review the agent's response in the playground interface.

::: zone-end

## Visualize hosted agent workflow execution

The Foundry for Visual Studio Code extension provides a real-time execution graph that shows how agents in your workflow interact and collaborate. Enable observability in your project to use this visualization.

::: zone pivot="python"
Enable visualization in your workflows by adding the following code snippet:

```python
from agent_framework.observability import setup_observability
setup_observability(vs_code_extension_port=4319) # Default port is 4319
```
::: zone-end

::: zone pivot="csharp"
Add the following reference to your csproj file:

```xml
<ItemGroup>
    <PackageReference Include="OpenTelemetry" Version="1.12.0" />
    <PackageReference Include="OpenTelemetry.Exporter.Console" Version="1.12.0" />
    <PackageReference Include="OpenTelemetry.Exporter.OpenTelemetryProtocol" Version="1.12.0" />
    <PackageReference Include="System.Diagnostics.DiagnosticSource" Version="9.0.10" />
</ItemGroup>
```

Update your program to include the following code snippet:

```CSharp
using System.Diagnostics;
using OpenTelemetry;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var otlpEndpoint =
    Environment.GetEnvironmentVariable("OTLP_ENDPOINT") ?? "http://localhost:4319";

var resourceBuilder = OpenTelemetry
    .Resources.ResourceBuilder.CreateDefault()
    .AddService("WorkflowSample");

var s_tracerProvider = OpenTelemetry
    .Sdk.CreateTracerProviderBuilder()
    .SetResourceBuilder(resourceBuilder)
    .AddSource("Microsoft.Agents.AI.*") // All agent framework sources
    .SetSampler(new AlwaysOnSampler()) // Ensure all traces are sampled
    .AddOtlpExporter(options =>
    {
        options.Endpoint = new Uri(otlpEndpoint);
        options.Protocol = OpenTelemetry.Exporter.OtlpExportProtocol.Grpc;
    })
    .Build();
```
::: zone-end

### Monitor and visualize your hosted agent workflow

To monitor and visualize your hosted agent workflow execution in real time:

1. Open the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>).

1. Run this command: `>Microsoft Foundry: Open Visualizer for Hosted Agents`.

A new tab opens in VS Code to display the execution graph. The visualization updates itself automatically as your workflow progresses, to show the flow between agents and their interactions.

#### Port conflicts

For port conflicts, you can change the visualization port by setting it in the Foundry extension settings. To do that, follow these steps:

1. In the left sidebar of VS Code, select the gear icon to open the settings menu.
1. Select `Extensions` > `Microsoft Foundry Configuration`.
1. Locate the `Hosted Agent Visualization Port` setting and change it to an available port number.
1. Restart VS Code to apply the changes.

#### Change port in code 

::: zone pivot="python"
Change the visualization port by setting the `FOUNDRY_OTLP_PORT` environment variable. Update the observability port in the `workflow.py` file accordingly.

For example, to change the port to 4318, use this command:

```bash
  export FOUNDRY_OTLP_PORT=4318
```

In `workflow.py`, update the port number in the observability configuration:

```python
  setup_observability(vs_code_extension_port=4318)
```
> [!TIP]
> To enable more debugging information, add the `enable_sensitive_data=True` parameter to the `setup_observability` function.


::: zone-end

::: zone pivot="csharp"

For any port conflicts, change the visualization port by setting the `FOUNDRY_OTLP_PORT` environment variable. Update the OTLP endpoint in your program accordingly.

For example, to change the port to 4318, use this command:

```powershell
  $env:FOUNDRY_OTLP_PORT="4318"
```
In your program, update the OTLP endpoint to use the new port number:

```CSharp
var otlpEndpoint =
    Environment.GetEnvironmentVariable("OTLP_ENDPOINT") ?? "http://localhost:4318";
```
::: zone-end

## Deploy the hosted agent

After testing your hosted agent locally, deploy it to your Foundry workspace so other team members and applications can use it.

>[!IMPORTANT]
> Make sure you give the necessary permissions to deploy hosted agents in your Foundry workspace, as stated in the [Prerequisites](#prerequisites). You might need to work with your Azure administrator to get the required role assignments. 

::: zone pivot="python"
1. Open the Visual Studio Code Command Palette and run the `Microsoft Foundry: Deploy Hosted Agent` command.
1. Configure the deployment settings by selecting your target workspace, specifying the container agent file (`container.py`), and defining any other deployment parameters as needed.
1. Upon successful deployment, the hosted agent appears in the `Hosted Agents (Preview)` section of the Microsoft Foundry extension tree view.
1. Select the deployed agent to access detailed information and test functionality using the integrated playground interface.
::: zone-end

::: zone pivot="csharp"
1. Open the Visual Studio Code Command Palette and run the `Microsoft Foundry: Deploy Hosted Agent` command.
1. Configure the deployment settings by selecting your target workspace, specifying the container agent file (`<your-project-name>.csproj`), and defining any other deployment parameters as needed.
1. Upon successful deployment, the hosted agent appears in the `Hosted Agents (Preview)` section of the Microsoft Foundry extension tree view.
1. Select the deployed agent to access detailed information and test functionality using the integrated playground interface.
::: zone-end

## Related content

- [Hosted agent concepts](../concepts/hosted-agents.md)
- [Build an agent in Foundry Agent Service](/azure/ai-foundry/how-to/develop/vs-code-agents?view=foundry&preserve-view=true)
- [Publish and share agents in Microsoft Foundry](./publish-agent.md)
