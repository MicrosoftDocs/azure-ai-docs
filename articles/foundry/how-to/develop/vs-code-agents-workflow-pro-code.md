---
title: "Create hosted agents with Microsoft Foundry Toolkit for Visual Studio Code"
description: "Create a Python or C# agent workflow from a sample, debug it with Agent Inspector, and deploy it with Microsoft Foundry Toolkit for Visual Studio Code."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 09/10/2026
ms.reviewer: erichen
ms.author: rotabor
author: bobtabor-msft
zone_pivot_groups: ai-foundry-vsc-extension-languages
#CustomerIntent: As a developer, I want to create and deploy hosted agent workflows in VS Code so that I can build multi-agent solutions without leaving my IDE.
ms.custom: doc-kit-assisted
---

# Create hosted agents with Microsoft Foundry Toolkit for Visual Studio Code

Use Microsoft Foundry Toolkit for Visual Studio Code to create a code-based
workflow from a Microsoft Agent Framework sample. Run it locally with
Agent Inspector, then deploy its source code to Foundry Agent Service as a
hosted agent. You maintain the code and its dependencies. Foundry manages the
hosting infrastructure and scaling.

Hosted workflows coordinate agents in code. They differ from the retiring
Foundry declarative workflow service. For other creation routes, see
[Create an agent](create-agent-visual-studio-code.md).

## Prerequisites

- [Install Microsoft Foundry Toolkit for Visual Studio Code](install-foundry-toolkit-visual-studio-code.md).
- [Select a Foundry project](set-up-foundry-project-visual-studio-code.md) with
  a deployed model. Use a
  [supported hosted-agent region](../../agents/concepts/hosted-agents.md#region-availability).
- Permission to use the model and deploy hosted agents. For source-code
  deployment, the **Foundry Project Manager** role at project scope includes
  agent operations and role assignment permissions. See
  [Hosted agent permissions](../../agents/concepts/hosted-agent-permissions.md).

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

- [Azure CLI](/cli/azure/install-azure-cli) for the local authentication steps
  in this article.
- For container deployment, the registry and image access required by
  [Azure Container Registry setup](../../agents/concepts/hosted-agent-permissions.md#azure-container-registry-setup).
  These registry requirements don't apply to a source-code deployment.

::: zone pivot="python"

- Python 3.13 for the sample's configured hosted runtime.
- The [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  for Visual Studio Code.

::: zone-end

::: zone pivot="csharp"

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0).
- [C# Dev Kit](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit)
  for Visual Studio Code.

::: zone-end

The main deployment path uses **Code** with **Remote** package mode and doesn't
require a local Docker build. Local execution still sends model requests to
Foundry and can incur charges. Review the
[service limits and availability](../../agents/concepts/hosted-agents.md#limits-pricing-and-availability)
and [Toolkit release notes](https://github.com/microsoft/foundry-dev-tools/blob/main/WHATS_NEW.md)
for the features you use.

## Create a hosted agent workflow

Choose an Agent Framework sample that uses the Responses protocol. You don't
need to create a separate prompt agent first. To compare samples, Agent Builder,
and Copilot-assisted coding, see
[Choose a creation route](create-agent-visual-studio-code.md#choose-a-creation-route).

::: zone pivot="python"

Use **Multi-Agent Workflow (Agent Framework)**, which chains a writer, a
reviewer, and a formatter. The final response comes from the formatter. Review
the [Python workflow sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/05-workflows)
for the complete implementation and its model guidance.

::: zone-end

::: zone pivot="csharp"

Use **Translation Workflow**, which chains three translation agents: English
to French, French to Spanish, and Spanish to English. Review the
[C# workflow sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/agent-framework/workflows)
for the complete implementation.

::: zone-end

1. In the **Foundry Toolkit** view, select **Developer Tools** > **Build** >
   **Create Agent**.
1. Under **Code an agent from samples**, select **Browse all samples**.
1. In **Create Hosted Agent from Sample**, filter by your **Language**,
   **Framework** = **Agent Framework**, and **Protocol Type** = **Responses**.
   Search for `workflow`.

   The following screenshot shows the gallery with **Basic Hosted Agent** selected as an
   example. For this guide, select the workflow sample for your language instead.

   :::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/hosted-agent-sample-gallery.png" alt-text="Screenshot of the hosted-agent sample gallery with Basic Hosted Agent selected, workflow samples, and language, framework, and protocol filters." lightbox="../../media/how-to/create-hosted-agents-vs-code/hosted-agent-sample-gallery.png":::

1. Select the workflow sample for your language.
1. Select **Next**.
1. On **Create**, choose the **Workspace Folder**. If the folder already
   contains files, enter a **Folder Name** for a new child folder.
1. If **Environment Setup** appears, select **Setup with Microsoft Foundry**,
   and then select your subscription and project. When a default project is
   already selected, the form uses that project.
1. Select an existing compatible **Model Deployment**.

   The following screenshot shows example project settings with local paths hidden.
   Use your own destination and the model deployment required by your sample.

   :::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/create-hosted-agent-project.png" alt-text="Screenshot of the Create tab showing workspace folder, folder name, model deployment, and Create controls, with local paths hidden." lightbox="../../media/how-to/create-hosted-agents-vs-code/create-hosted-agent-project.png":::

1. Review the destination, and then select **Create**.
1. Open the generated project in Visual Studio Code and read its `README.md`.

The **Agent Framework**, **Copilot SDK**, and **LangGraph** tiles on **Create
Agent** open the **Create** tab with a hello-world starter selected. Use
**Browse all samples** to choose a workflow rather than one of those starters.
You can also open the gallery from **My Resources** > **Agents** >
**Hosted Agent** > **Add Hosted Agent**.

Sample names and contents can change with the catalog. Some versions label
these samples **Workflows**. Use the sample's **GitHub** link to confirm that
you selected the intended workflow.

**Skip for now** generates the code without completing model setup. If you
choose it, configure the required project and model values before running the
sample. **Deploy & use new model**, when offered, provisions a model deployment,
not the hosted agent. Creating the local project files doesn't deploy the agent.

## Configure the local project

Keep the folder that contains `azure.yaml` open as the workspace root. Check
the hosted-agent service's `project` path in that file to find its source
directory.

| Artifact | Purpose |
| --- | --- |
| `azure.yaml` | Declares the hosted-agent service, source directory, runtime, protocols, and deployment settings. |
| `main.py` or `Program.cs` in the source directory | Implements the workflow and starts its Responses server. |
| `requirements.txt` or the `.csproj` file | Declares dependencies for the selected language. |
| `.env` in the source directory | Holds local project and model values. The Toolkit creates it from `.env.example` when the sample supplies that file. |
| `.vscode/launch.json` and `.vscode/tasks.json` | Configure the local server, debugger attachment, and Agent Inspector. |

Sample layouts can change. Use the generated `README.md` and `azure.yaml`
instead of assuming that the code and environment file are at the workspace root.

### Install dependencies

Use the generated sample's dependency files. Keep the selected interpreter or
SDK consistent with its runtime configuration.

::: zone pivot="python"

1. Run **Python: Create Environment...** from the Command Palette to create a
   virtual environment, or **Python: Select Interpreter** to select an existing
   Python 3.13 environment. For environment setup and selection, see
   [Python environments in Visual Studio Code](https://code.visualstudio.com/docs/python/environments).
1. Open a terminal with that environment active. Change to the source directory
   that contains `main.py` and `requirements.txt`.
1. Install the sample's packages:

   ```console
   python -m pip install -r requirements.txt
   ```

   The requirements include `debugpy`, which the generated F5 configuration
   uses. Reference: [Python workflow dependencies](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/05-workflows/src/agent-framework-workflows-responses/requirements.txt).

::: zone-end

::: zone pivot="csharp"

1. Run **C#: Check Workspace Requirements** from the Command Palette.
1. In a terminal, change to the source directory that contains the `.csproj`
   file and restore its packages:

   ```console
   dotnet restore
   ```

   Reference: [dotnet restore](/dotnet/core/tools/dotnet-restore).

For debugger controls and configuration, see
[C# debugging in Visual Studio Code](https://code.visualstudio.com/docs/csharp/debugging).

::: zone-end

### Set the project and model

Review the `.env` file in the source directory. If it doesn't exist, create it
with the values required by the sample.

| Variable | Value |
| --- | --- |
| `FOUNDRY_PROJECT_ENDPOINT` | Your project endpoint, in the form `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`. |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | The name of the model deployment in that project, not just the model's catalog name. |

Both workflow samples load `.env` during startup. The project endpoint is not
an Azure OpenAI account endpoint. Keep the file out of source control, and
don't put credentials in your application code.

### Authenticate locally

The samples use `DefaultAzureCredential`. For the Azure CLI credential path,
sign in with an account that can access the project's model:

```azurecli
az login
```

Reference: [Sign in with Azure CLI](/cli/azure/authenticate-azure-cli-interactively).

Toolkit sign-in selects the project for extension operations. The local agent
process also needs a supported credential. For other options, see
[DefaultAzureCredential for Python](/python/api/azure-identity/azure.identity.defaultazurecredential)
or [credential chains for .NET](/dotnet/azure/sdk/authentication/credential-chains).

## Run your hosted workflow locally

Use the generated debug configuration to start the HTTP server and open
**Agent Inspector**. Opening Agent Inspector alone doesn't start the server.

::: zone pivot="python"

Use this test request:
`Create a slogan for a new electric SUV that is affordable and fun to drive.`
The workflow returns a formatted slogan after the writer, reviewer, and
formatter complete.

::: zone-end

::: zone pivot="csharp"

Use this test request: `The quick brown fox jumps over the lazy dog.`
The workflow runs its translation chain and returns a response.

::: zone-end

1. Return to the generated project workspace.
1. Set a breakpoint in the workflow code if you want to inspect execution.
1. Press **F5**. If prompted, select **Debug Local Agent HTTP Server**.
1. Wait for the server to start and **Agent Inspector** to open.
1. Send the test request for your sample.
1. Inspect the response and repeat with another request. If you set a
   breakpoint, inspect the values and continue execution.

After the sample works, modify the workflow and repeat the local test. If you
add tools, send a request that requires a real tool result and inspect the call.
A model-only answer or a mock response doesn't prove that the live tool works.

The screenshot shows a tool-enabled local agent, not either workflow sample.
Agent Inspector displays its response and tool calls with a latency waterfall
and run timeline. Available inspection details depend on the running agent
and its instrumentation.

:::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/local-agent-inspector.png" alt-text="Screenshot of Agent Inspector connected to localhost on port 8088 with the Responses protocol, tool calls, a latency waterfall, and a run timeline." lightbox="../../media/how-to/create-hosted-agents-vs-code/local-agent-inspector.png":::

If you use GitHub Copilot, you can run
`/validate-microsoft-foundry-hosted-agent` in Copilot Chat to review the project
against Foundry best practices. This Chat command opens a report; it isn't a
terminal command or a substitute for running the workflow.

The generated tasks use port `8088` for the agent server. Python debugging
also uses port `5679`. If startup reports a port conflict, stop the conflicting
process that you own or adjust the generated task configuration consistently.

### Run without the debugger

To run manually, open a terminal in the sample's source directory with its
dependencies, environment values, and Azure credential available.

::: zone pivot="python"

```console
python main.py
```

Reference: [Python workflow entry point](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/05-workflows/src/agent-framework-workflows-responses/main.py).

::: zone-end

::: zone pivot="csharp"

Set the HTTP address for the local server, then run it:

#### [Windows (PowerShell)](#tab/windows-powershell)

```powershell
$env:ASPNETCORE_URLS = "http://localhost:8088"
dotnet run
```

#### [Windows (command prompt)](#tab/windows-command-prompt)

```dos
set ASPNETCORE_URLS=http://localhost:8088
dotnet run
```

#### [macOS/Linux (Bash)](#tab/macos-linux-bash)

```bash
export ASPNETCORE_URLS="http://localhost:8088"
dotnet run
```

---

Reference: [ASP.NET Core server URLs](/aspnet/core/fundamentals/servers/kestrel/endpoints#specify-endpoints-with-urls)
and [dotnet run](/dotnet/core/tools/dotnet-run).

::: zone-end

Then run **Foundry Toolkit: Open Agent Inspector** from the Command Palette
and connect to the local server on port `8088`. Running a sample with `python`
or `dotnet run` starts a local process, not a container.

## Visualize hosted agent workflow execution

Use Agent Inspector to inspect the events, responses, and tool calls that your running agent emits. When the runtime emits workflow events, use the workflow visualization to inspect the sequence of steps.

The available details depend on the sample's instrumentation. Follow the sample's telemetry setup instructions for runtime-specific requirements.

These steps use the Responses protocol. Other samples need clients that match
their protocol: the HTTP Invocations view isn't a WebSocket client, and Python
Activity samples use Microsoft 365 Agents Playground. Follow the selected
sample's local-testing instructions. Changing a protocol name in configuration
doesn't add that protocol to your server. See
[Choose a hosted-agent protocol](../../agents/concepts/hosted-agents.md#which-protocol-should-i-use).

## Deploy the hosted agent

After the local workflow behaves as expected, deploy it from the project
workspace. Python and C# share the deployment procedure. Start with **Code**
and **Remote** package mode to upload source and let Foundry restore dependencies.

### Prepare deployment configuration

Review and save the hosted-agent service in `azure.yaml`. Preserve the sample's
protocol configuration and declare the model deployment and other required
runtime settings there.

Deployment resolves declared environment values from the source directory's
`.env` or the process environment. It doesn't forward every local `.env` entry.
The platform supplies reserved runtime values such as `FOUNDRY_PROJECT_ENDPOINT`;
don't redeclare them as deployment settings. See
[Platform-injected environment variables](../../agents/how-to/deploy-hosted-agent.md#platform-injected-environment-variables).

Review the source directory's ignore rules before packaging. Keep `.env`,
credentials, virtual environments, and caches out of the package. For ZIP
deployment, a source-root `.agentignore` replaces the rules in `.gitignore`
and `.dockerignore`, so retain the necessary exclusions if you add that file.

> [!IMPORTANT]
> Don't commit or package secrets. Local sign-in doesn't transfer your user's
> permissions to the deployed agent. Configure access for the agent's runtime
> identity and supported connections. See
> [Hosted agent permissions](../../agents/concepts/hosted-agent-permissions.md).

### Deploy source with Remote package mode

Use the generated workspace root so the Toolkit can read the service
configuration and locate its source directory.

1. Stop the local debugging session.
1. Select **Developer Tools** > **Build** > **Deploy to Microsoft Foundry**.
   You can also run **Foundry Toolkit: Deploy Hosted Agent** from the Command Palette.

   :::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/open-hosted-agent-deployment.png" alt-text="Screenshot of Deploy to Microsoft Foundry under Build in the Foundry Toolkit Developer Tools section." lightbox="../../media/how-to/create-hosted-agents-vs-code/open-hosted-agent-deployment.png":::

1. If **Foundry Project Setup** appears, select the subscription and project,
   and then select **Next**. Otherwise, confirm that the default project is the
   intended destination.
1. On **Basics**, select **Code** as **Deployment Method** and **Remote** as
   **Package Mode**.
1. Select **New agent** and enter the **Hosted Agent Name**. To update a
   deployed agent, select **Existing agent** and choose that agent instead.

   :::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/code-remote-deployment.png" alt-text="Screenshot of Basics with Code deployment, Remote package mode, and New agent selected, with the agent name hidden." lightbox="../../media/how-to/create-hosted-agents-vs-code/code-remote-deployment.png":::

1. Select **Next**.
1. On **Review + Deploy**, check **Language**, **Runtime Version**, **Entry Point**,
   and **CPU and Memory** against the sample. Confirm that the source directory
   matches the service's `project` path.

   The following screenshot shows an example with **Python 3.14** and its entry point
   hidden, not the settings for these workflow samples. For Python, use
   **Python 3.13** with `python3 main.py`. For C#, use **.NET 10** and the
   detected entry point for your generated project.

   :::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/review-hosted-agent-deployment.png" alt-text="Screenshot of Review + Deploy showing Python 3.14 as an example, a hidden entry point, CPU and memory, and Deploy controls." lightbox="../../media/how-to/create-hosted-agents-vs-code/review-hosted-agent-deployment.png":::

1. Select **Deploy**. Follow progress in notifications and **Output**.
1. Continue to [Test the deployed workflow](#test-the-deployed-workflow).

Match the runtime to your sample configuration and local environment. Don't
accept a different runtime just because it's the wizard default.

The Toolkit saves deployment choices when you submit the form. Those local
settings don't prove that the cloud deployment succeeded. Updating an existing
agent creates a new version rather than changing a previous version in place.

### Choose another ZIP package mode

The Toolkit offers these source-code packaging options:

| Package mode | What happens | What to prepare |
| --- | --- | --- |
| **Remote** | The Toolkit packages source. Foundry restores Python requirements or the .NET project during provisioning. | Source, dependency declarations, and a compatible entry point. |
| **Bundled** | The Toolkit stages source and runs the **Package Command** locally before creating the ZIP. Foundry runs the prepared package. | Compatible Linux dependencies and the local tools required by the command. The default Python command installs compatible dependencies in `packages/`; the .NET command creates publish output. |

The selectable ZIP runtimes are Python 3.13, Python 3.14, and .NET 10. Match the
runtime to your code and dependencies. For layouts, limits, and service
requirements, see [Deploy from source code](../../agents/how-to/deploy-hosted-agent-code.md).
For the runtime support policy, see
[Supported hosted-agent runtimes](../../agents/how-to/deploy-hosted-agent-code.md#supported-runtimes).

### Deploy a container image

Choose **Container** on **Basics** when you need a custom runtime image or
already have a compatible image.

| Registry choice | Toolkit behavior |
| --- | --- |
| **Default ACR** | Creates or reuses a registry for the selected project, then builds and pushes the image through Azure Container Registry (ACR). |
| **Custom ACR** | Uses an existing registry you select, then builds and pushes the image through ACR. |
| **Custom ACR image** | Uses a prebuilt ACR image reference without building or pushing source. |

For the build options, review the Dockerfile and build context before deploying.
If you generate a Dockerfile in the wizard, review the file and select
**Continue and deploy**. These options use remote ACR builds, not local Docker builds.

Custom registry options use a registry in the selected subscription. The
custom-registry build path requires public network access; the prebuilt-image
path has separate private-network requirements. Choosing an image doesn't
configure network connectivity.

Review [container requirements](../../agents/how-to/deploy-hosted-agent.md#container-requirements)
and [private networking guidance](../../agents/how-to/virtual-networks.md)
before using a custom registry. These deployments target Foundry Agent Service,
not the retired Azure Container Apps hosted-agent path. To move an older agent,
follow [Migrate from the hosted-agent preview](../../agents/how-to/migrate-hosted-agent-preview.md).

## Test the deployed workflow

A successful create request doesn't prove that the runtime is ready or that
its model and tools are reachable. Test the exact deployed version.

1. Under **My Resources** > **Agents** > **Hosted Agent**, select the agent name.
1. Select the numbered version you just deployed.
1. On **Details**, wait for the deployment status to indicate that the agent
   is running. If it fails, inspect the deployment output before retrying.
1. Open **Playground** and send the same request you tested locally.
1. Review the response. If you added tools, send a request that requires those
   tools and inspect the calls.

Local and cloud runs use different credentials, dependency environments, and
network paths. A successful local response doesn't guarantee a successful
remote response.

## Inspect and update the deployed agent

Use the remote playground to test and inspect your deployed agent. Unlike
[local testing with Agent Inspector](#run-your-hosted-workflow-locally), requests
in this playground run against the agent hosted in Foundry.

1. In **Foundry Toolkit**, select **Developer Tools** > **Build** >
   **Hosted Agent Playground**.

   :::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/open-hosted-agent-playground.png" alt-text="Screenshot of Hosted Agent Playground under Build in the Foundry Toolkit Developer Tools section." lightbox="../../media/how-to/create-hosted-agents-vs-code/open-hosted-agent-playground.png":::

1. In the **Hosted Agent** dropdown, select your deployed agent and the version
   to inspect. Open **Playground** to send a request and view the response and
   session details.

   The following screenshot shows an illustrative deployed agent's response, not the
   expected output of either workflow sample. Agent and session identifiers
   are hidden.

   :::image type="content" source="../../media/how-to/create-hosted-agents-vs-code/hosted-agent-playground.png" alt-text="Screenshot of the remote hosted-agent playground with a response, session details, and inspection tabs, with agent and session identifiers hidden." lightbox="../../media/how-to/create-hosted-agents-vs-code/hosted-agent-playground.png":::

Use these controls to inspect and update the agent. The available tabs depend
on its protocol and connected services.

| Task | Action |
| --- | --- |
| Review deployment details | Open **Details** for status, configuration, and the copyable endpoint. |
| Test a version | Select a numbered version for playground requests. **Automatic** follows the service endpoint's version selection, which isn't necessarily the latest version. The picker doesn't change routing for other clients. |
| Review runtime logs | Open **Sessions**, select a session, and view its logs. Runtime logs require a session; build output is separate. Stopping a log stream or canceling a request doesn't stop the hosted agent. |
| Retrieve deployed code | Use **Download code asset** for a ZIP deployment. An image deployment exposes the image reference instead of a downloadable source project. |
| Update behavior | Edit and test the local code, then repeat the [deployment procedure](#deploy-the-hosted-agent) with **Existing agent** to create a new version. |

Use **Traces** and **Evaluation**, when available, for investigation and quality
measurement beyond one successful response. Follow the prerequisites for
[hosted-agent tracing](../../observability/quickstarts/quickstart-tracing-hosted-agent.md)
and [hosted-agent evaluation](../../observability/quickstarts/quickstart-evaluate-hosted-agent.md).

Deployment gives the agent an endpoint for programmatic use. A separate
publication step isn't required for API access. Publishing to Teams or
Microsoft 365 is a separate task. See the
[current agent endpoint and publishing model](../../agents/how-to/migrate-agent-applications.md).

## Troubleshooting

Use the reported error and the sample configuration to identify the failing step.

| Symptom | Action |
| --- | --- |
| Local startup fails because a package is missing. | Confirm the selected interpreter or SDK, then install dependencies from the sample's source directory. |
| The project endpoint or model can't be found. | Check `FOUNDRY_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME`. Don't substitute an account endpoint or a model catalog name. |
| Authentication or authorization fails. | Check the local credential and project access. Review [hosted agent permissions](../../agents/concepts/hosted-agent-permissions.md) for deployment and runtime identity requirements. |
| Agent Inspector can't connect. | Confirm that the server started and port `8088` is available. Opening Inspector alone doesn't start the server. |
| A deployment fails. | Review the deployment error and build output. For code, check the runtime, entry point, package mode, and ignore rules. For a container, check the image and registry permissions. |
| The local response works, but the deployed version fails. | Compare the deployed environment and identity permissions with the local configuration. Retest the exact deployed version. |

## Clean up resources

Stop the local debugging session when you're done. If you no longer need the deployed test agent, follow
[Manage hosted agents](../../agents/how-to/manage-hosted-agent.md)
to remove it.

Deleting the agent removes its versions and terminates active sessions. It
doesn't remove every associated Azure resource.

Delete only cloud resources created for this exercise that no other applications use. Don't delete a shared Foundry project, model deployment, or container registry.

## Related content

Use these guides to extend your workflow:

- [Microsoft Agent Framework workflows](/agent-framework/workflows/)
- [Hosted agent concepts](../../agents/concepts/hosted-agents.md)
- [Create a prompt agent](create-prompt-agent-visual-studio-code.md)
