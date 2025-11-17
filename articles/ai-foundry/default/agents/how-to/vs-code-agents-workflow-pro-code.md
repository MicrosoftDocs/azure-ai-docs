---
title: Work with Hosted (Pro-code) Agent workflows in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Use this article to learn how to use Hosted (Pro-code) workflows with Foundry Agent Service directly in VS Code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 11/17/2025
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: ai-foundry-vsc-extension-languages
---

# Work with Hosted (Pro-code) Agents in Visual Studio Code (preview)

In this article, you learn how to add and use hosted Foundry Agent workflows with Azure AI agents by using the [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).

After you [build an agent in Foundry Agent Service](
/azure/ai-foundry/how-to/develop/vs-code-agents?view=foundry&tabs=windows-powershell&pivots=python&preserve-view=true) by using this Visual Studio Code (VS Code) extension, you can add hosted agent workflows to your agent.

Foundry developers can stay productive by developing, testing, and deploying hosted agent workflows in the familiar environment of VS Code.

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

#### Prerequisites

To run the sample hosted agent Python project, ensure that you have Python 3.10 or higher installed. You also need a Foundry project with a deployed model, or an Azure OpenAI resource. 

Grant the project's managed identity the required permissions by assigning the built-in [Azure AI User](https://aka.ms/foundry-ext-project-role) role.

#### Setup and installation

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

#### Prerequisites

To run the sample hosted agent C# project, ensure that you have a Foundry project with a deployed model, or an Azure OpenAI resource. 

Grant the project's managed identity the required permissions by assigning the built-in [Azure AI User](https://aka.ms/foundry-ext-project-role) role.


#### Setup and installation

1. Download and install the .NET 9 SDK from the [official .NET website](https://dotnet.microsoft.com/download).

1. Go to your project directory and run this command to get the necessary NuGet packages:

    ```bash
    dotnet restore
    ```
::: zone-end

## Run your hosted workflow locally

::: zone pivot="python"
The sample workflow project creates an .env file with the necessary environment variables. Create or update the .env file with your Azure OpenAI credentials:

```
# Your Azure OpenAI endpoint
AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com/
    
# Your model deployment name in Azure OpenAI
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

> [!IMPORTANT]
> Never commit the `.env` file to version control. Add it to your `.gitignore` file.

### Authenticate your hosted agent

The hosted agent sample authenticates using DefaultAzureCredential (/azure/developer/python/sdk/authentication/credential-chains?tabs=dac#defaultazurecredential-overview). Configure your development environment to provide credentials via one of the supported sources, for example:

- Azure CLI (`az login`)
- Visual Studio Code account sign-in
- Visual Studio account sign-in
- Environment variables for a service principal (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

Confirm authentication locally by running either the Azure CLI `az account show` or `az account get-access-token` commands before running the sample.

You can run the hosted agent in interactive mode or container mode.

### Run your hosted agent in interactive mode

Run the hosted agent directly for development and testing:

```bash
python interactive.py
```

### Run your hosted agent in container mode

> [!TIP]
> Open the local playground before starting the container agent to ensure the visualization functions correctly.

To run the hosted agent in container mode:
1. Open the Visual Studio Code Command Palette and execute the `Microsoft Foundry: Open Container Agent Playground Locally` command.
1. Execute `container.py` to initialize the containerized hosted agent.
1. Submit a request to the agent through the playground interface. For example, enter a prompt such as: "Create a slogan for a new electric SUV that's affordable and fun to drive."
1. Review the agent's response in the playground interface.

::: zone-end

::: zone pivot="csharp"

The sample workflow project creates an .env file with the necessary environment variables. Create or update the .env file with your Azure OpenAI credentials:

1. Set up your environment variables based on your operating system:

   #### [Windows (PowerShell)](#tab/windows-powershell)

   ```powershell
   $env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
   $env:MODEL_DEPLOYMENT_NAME="your-deployment-name"
   ```

   #### [Windows (command prompt)](#tab/windows-command-prompt)

   ```dos
   set AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   set MODEL_DEPLOYMENT_NAME=your-deployment-name
   ```

   #### [macOS/Linux (Bash)](#tab/macos-linux-bash)

   ```bash
   export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
   export MODEL_DEPLOYMENT_NAME="your-deployment-name"
   ```

    ---

#### Authenticate your hosted agent

The hosted agent sample authenticates using DefaultAzureCredential (/dotnet/azure/sdk/authentication/credential-chains?tabs=dac#defaultazurecredential-overview). Configure your development environment to provide credentials via one of the supported sources, for example:

- Azure CLI (`az login`)
- Visual Studio Code account sign-in
- Visual Studio account sign-in
- Environment variables for a service principal (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

Confirm authentication locally by running either the Azure CLI `az account show` or `az account get-access-token` commands before running the sample.

You can run the hosted agent in interactive mode or container mode.

### Run your hosted agent in interactive mode

Run the hosted agent directly for development and testing:

```bash
dotnet build
dotnet run --interactive
```

### Run your hosted agent in container mode

> [!TIP]
> Open the local playground before starting the container agent to ensure the visualization functions correctly.

To run the agent in container mode:

1. Open the Visual Studio Code Command Palette and execute the `Microsoft Foundry: Open Container Agent Playground Locally` command.
2. Use the following command to initialize the containerized hosted agent.
   ```bash
   dotnet build
   dotnet run
   ```
3. Submit a request to the agent through the playground interface. For example, enter a prompt such as: "Create a slogan for a new electric SUV that's affordable and fun to drive."
4. Review the agent's response in the playground interface.

::: zone-end

## Visualize hosted agent workflow execution

By using the Foundry for Visual Studio Code extension, you can visualize the interactions between agents and how they collaborate to achieve your desired outcome.

::: zone pivot="python"
Enable visualization in your workflows by adding the following code snippet:

```python
from agent_framework.observability import setup_observability
setup_observability(vs_code_extension_port=4317) # Default port is 4317
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

1. Run this command: `>Foundry: Open Visualizer for Hosted Agents`.

A new tab opens in VS Code to display the execution graph. The visualization updates itself automatically as your workflow progresses, to show the flow between agents and their interactions.

#### Port conflicts
::: zone pivot="python"
For any port conflicts, change the visualization port by setting the `FOUNDRY_OTLP_PORT` environment variable. Update the observability port in the `workflow.py` file accordingly.

For example, to change the port to 4318, use this command:

```bash
  export FOUNDRY_OTLP_PORT=4318
```

In `workflow.py`, update the port number in the observability configuration:

```python
  setup_observability(vs_code_extension_port=4318)
```
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

To deploy the hosted agent:

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

## Next steps