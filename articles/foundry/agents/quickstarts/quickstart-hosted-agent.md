---
title: "Quickstart: Deploy your first hosted agent"
description: "Learn how to deploy a containerized AI agent to Foundry Agent Service using the Azure Developer CLI, the Python SDK, Microsoft Foundry Toolkit for Visual Studio Code extension, or Microsoft Foundry Skill."
author: aahill
ms.author: aahi
ms.date: 07/09/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: hosted-agent-quickstart-method
---

# Quickstart: Deploy your first hosted agent

## Prerequisites

Before you begin, you need:

* An Azure subscription--[Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* If you have an existing Foundry project, you need `Foundry Project Manager` at project scope. If you need to create a new Foundry project, you need the `Owner` role at resource group scope. For the full role matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).
* [Python 3.13 or later](https://www.python.org/downloads/).

:::zone pivot="azd"

* [Azure Developer CLI (AZD) 1.25.3 or later](/azure/developer/azure-developer-cli/install-azd).
* The `azd microsoft.foundry` extension. Install and verify the extension after AZD is installed:

    ```
    azd ext install microsoft.foundry
    ```

:::zone-end

:::zone pivot="python"

* [Azure CLI](/cli/azure/install-azure-cli) installed and authenticated:

  ```bash
  az login
  ```

* The Python SDK packages used in this quickstart:

  ```bash
  pip install "azure-ai-projects>=2.3.0" python-dotenv
  ```

* An existing Foundry project with a deployed model. The Python SDK path in this quickstart creates and routes a hosted agent version, but it doesn't scaffold a new Foundry project or create a model deployment for you. If you need the full provisioning workflow, use the Azure Developer CLI tab in this article.

:::zone-end

:::zone pivot="vscode"

* [Visual Studio Code](https://code.visualstudio.com/).
* [Microsoft Foundry Toolkit for Visual Studio Code](https://aka.ms/foundrytk).

:::zone-end

:::zone pivot="foundry-skills"

* A coding agent host with the
  [Microsoft Foundry Skill](../../how-to/develop/use-microsoft-foundry-skill.md)
  installed.
* [Azure CLI](/cli/azure/install-azure-cli) and
  [Azure Developer CLI (AZD)](/azure/developer/azure-developer-cli/install-azd)
  installed and authenticated:

    ```bash
    az login
    azd auth login
    ```

:::zone-end

:::zone pivot="azd"

## Step 1: Initialize sample agent

Initialize a new hosted agent using the basic [Agent Framework sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/01-basic) in an empty directory:

```
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/01-basic/azure.yaml" --deploy-mode code
```

The interactive flow prompts for:

* **Agent name**: Customize the name or accept the *default*, **agent-framework-agent-basic-responses**
* **Foundry Project**: Select **Create a new Foundry project** or **Use an existing Foundry project**
* **Tenant**: Select your Azure tenant
* **Subscription**: Select your Azure subscription
* **Location**: Select an Azure region
* **Model**: Select the *default*, **gpt-5.4-mini**, or another model you can access.
* **Model Version**: Select the *default* option.
* **Model SKU**: Select an option with available quota that isn't Batch, usually **Standard** or **GlobalStandard**
* **Deployment capacity**: Select the *default*, **10**
* **Deployment name**: Select the *default*, **gpt-5.4-mini**

When complete, you should see **AI agent definition added to your azd project successfully!**. Change directory into newly created agent folder.

```
cd agent-framework-agent-basic-responses
```

## Step 2: Provision Azure resources

Provision the resources defined in `azure.yaml`:

```
azd provision
```

## Step 3: Test the agent locally

```
azd ai agent run
```

This command creates a virtual environment, installs dependencies, launches the agent using the `startupCommand` defined in `azure.yaml` and opens the agent inspector in your browser so you can chat with the agent.

## Step 4: Deploy to Foundry Agent Service

Build and deploy the agent container:

```
azd deploy
```

When the command finishes, the output shows links to the agent playground and the agent endpoint:

```output
Deploying services (azd deploy)

  Done: Deploying service basic-agent
  - Agent playground (portal): https://ai.azure.com/.../build/agents/basic-agent/build?version=1
  - Agent endpoint: https://ai-account-<name>.services.ai.azure.com/api/projects/<project>/agents/basic-agent/versions/1
```

## Step 5: Invoke your agent

1. Send the same prompt to the deployed agent:

    ```
    azd ai agent invoke "Write a haiku about deploying cloud applications."
    ```

    You should see a haiku response within a few seconds.

1. (Optional) Stream container logs while you interact with the agent:

    ```
    azd ai agent monitor --follow
    ```

:::zone-end

:::zone pivot="python"

## Step 1: Create or choose a Foundry project

1. Open [Azure AI Foundry](https://ai.azure.com) and create a Foundry project, or select an existing one.
1. In the project, deploy a chat-capable model such as `gpt-5.4-mini`.
1. Copy these values from the portal:
  * **Project endpoint** from **Overview**.
  * **Deployment name** from **Build** > **Deployments**.

## Step 2: Download the Basic sample agent code

Clone the Foundry samples repo.

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
```

For Windows (PowerShell):

```powershell
git clone https://github.com/microsoft-foundry/foundry-samples.git
```

## Step 3: Create a Python environment and configure settings

Create a virtual environment and install the Python packages required for this quickstart.

For macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "azure-ai-projects>=2.3.0" python-dotenv
```

For Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "azure-ai-projects>=2.3.0" python-dotenv
```

Create a working folder for the deployment script, then create a `.env` file in that folder:

```text
FOUNDRY_PROJECT_ENDPOINT=<your-project-endpoint>
FOUNDRY_MODEL_NAME=<your-model-deployment-name>
FOUNDRY_HOSTED_AGENT_NAME=basic-agent
FOUNDRY_SAMPLE_PATH=<full-path-to-foundry-samples/samples/python/hosted-agents/agent-framework/responses/01-basic>
```

## Step 4: Deploy the hosted agent with Python

Create a file named `deploy_hosted_agent.py` in the same working folder as `.env` with the following contents:

```python
import os
import tempfile
import time
import zipfile
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
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

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_name = os.environ["FOUNDRY_MODEL_NAME"]
agent_name = os.environ.get("FOUNDRY_HOSTED_AGENT_NAME", "basic-agent")
sample_path = Path(os.environ["FOUNDRY_SAMPLE_PATH"]).resolve()


def create_code_zip(source_dir: Path) -> Path:
  zip_path = Path(tempfile.gettempdir()) / f"{agent_name}.zip"
  excluded = {".git", ".venv", "__pycache__", ".env", "deploy_hosted_agent.py"}

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
    details = project_client.agents.get_version(agent_name=agent_name, agent_version=version)
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
      description="Basic hosted agent deployed from local Python source.",
      definition=HostedAgentDefinition(
        cpu="0.5",
        memory="1Gi",
        code_configuration=CodeConfiguration(
          runtime="python_3_14",
          entry_point=["python", "main.py"],
          dependency_resolution=CodeDependencyResolution.REMOTE_BUILD,
        ),
        environment_variables={
          "FOUNDRY_PROJECT_ENDPOINT": endpoint,
          "FOUNDRY_MODEL_NAME": model_name,
        },
        protocol_versions=[ProtocolVersionRecord(protocol="responses", version="2.0.0")],
      ),
      code=code_stream,
    )

    print(f"Created hosted agent version {created.version}")

    wait_for_active_version(project_client, created.version)

    original_agent_endpoint = project_client.agents.get(agent_name=agent_name).agent_endpoint
    project_client.agents.update_details(
      agent_name=agent_name,
      agent_endpoint=AgentEndpointConfig(
        version_selector=VersionSelector(
          version_selection_rules=[
            FixedRatioVersionSelectionRule(agent_version=created.version, traffic_percentage=100),
          ]
        ),
        protocol_configuration=ProtocolConfiguration(responses=ResponsesProtocolConfiguration()),
      ),
    )

    print(f"Agent endpoint configured for version {created.version}")

    with project_client.get_openai_client(agent_name=agent_name) as openai_client:
      response = openai_client.responses.create(
        input="Write a haiku about deploying cloud applications.",
      )

    print(f"Agent response: {response.output_text}")
  finally:
    if original_agent_endpoint is not None:
      project_client.agents.update_details(agent_name=agent_name, agent_endpoint=original_agent_endpoint)
      print("Agent endpoint restored")

    if created is not None:
      project_client.agents.delete_version(agent_name=agent_name, agent_version=created.version, force=True)
      print(f"Deleted hosted agent version {created.version}")
```

Run the script:

```bash
python deploy_hosted_agent.py
```

The script zips the sample source, uploads it as a new hosted-agent version, waits for provisioning to complete, temporarily routes the hosted agent endpoint to that version, invokes the deployed agent, and then restores the previous endpoint configuration and deletes the temporary version.

## Step 5: Invoke your agent

After the script completes, use the hosted agent in either of these ways:

1. Edit `deploy_hosted_agent.py` and change the `input` value passed to `openai_client.responses.create(...)`, then run the script again.
1. If you want a persistent routed version instead of a temporary validation deployment, adapt the script to skip the restore and `delete_version(...)` steps after you review the traffic-routing implications.

:::zone-end

:::zone pivot="vscode"

## Step 1: Create a Foundry project

1. Open the Command Palette (**Ctrl+Shift+P**) and select **Foundry Toolkit: Create Project**.
1. Select your Azure subscription.
1. Create a new resource group or select an existing one.
1. Enter a name for the Foundry project.

## Step 2: Deploy a model

1. Open the Command Palette and select **Foundry Toolkit: Open Model Catalog**.
1. Search for `gpt-4.1` and select **Deploy**.
1. On the model deployment page, select **Deploy to Microsoft Foundry**.

## Step 3: Create a hosted agent project

1. Open the Command Palette and select **Foundry Toolkit: Create new Hosted Agent**.
1. Select the **Python** as the language.
1. For "Framework", select **Agent Framework**.
1. Select **Responses API** as the protocol type.
1. Select **Basic** as the sample code.
1. Select the "Next" button.
1. Choose a folder for the project files and enter a name for the agent.
1. For "Environment Setup", choose **Set up with Microsoft Foundry**, the content should auto-populate with the project and model you created in step 1 and 2.
1. Select the "Create" button.

A new VS Code window opens with the project as the active workspace.

## Step 4: Install dependencies

Create a virtual environment and install the requirements.

For macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Step 5: Test the agent locally

Press **F5** to start the local HTTP server with debugging enabled. The Foundry Toolkit Agent Inspector opens for interactive testing, and you can set breakpoints in your code.

To run the server without debugging:

```bash
python main.py
```

The agent listens on `http://localhost:8088/`. Send a test prompt with curl (or any HTTP client):

```bash
curl -sS -H "Content-Type: application/json" -X POST http://localhost:8088/responses \
    -d '{"input": "Write a haiku about deploying cloud applications.", "stream": false}'
```

## Step 6: Deploy to Foundry Agent Service

1. Open the Command Palette and select **Foundry Toolkit: Deploy Hosted Agent**. A deployment webview will open.
1. For "Deployment Method", select **Code**.
1. Select **Remote** as the package mode.
1. The "Agent Name" should auto-populate.
1. Select the "Next" button.
1. This "Review and Deploy" page should all auto-populate.
1. Select the "Deploy" button.

When deployment completes, the agent appears under **Hosted Agents (Preview)** in the Foundry Toolkit explorer.

## Step 7: Invoke your agent

1. In the Foundry Toolkit explorer, expand **Hosted Agents (Preview)** and select your agent. The detail page shows the status under **Deployment Details**.
1. Select the **Playground** tab and send a test prompt such as `Write a haiku about deploying cloud applications.`.

:::zone-end

:::zone pivot="python"

1. If you used the sample script as written, it already restores the endpoint configuration and deletes the temporary hosted agent version after validation.
1. If you created a dedicated resource group for this quickstart, you can delete the resource group from the Azure portal after you no longer need the project or model deployment.

> [!WARNING]
> Deleting the resource group permanently removes everything in it, including the Foundry project, model deployments, Container Registry, Application Insights, and the hosted agent.

:::zone-end

:::zone pivot="foundry-skills"

## Step 1: Open a workspace with the Foundry Skill

Open an empty folder in your coding agent host, such as GitHub Copilot in Visual
Studio Code, Copilot CLI, or Claude Code. Confirm that the `microsoft-foundry`
skill is available before you ask the coding agent to create Azure resources.

If the skill isn't available, follow
[Use the Microsoft Foundry Skill in coding agents](../../how-to/develop/use-microsoft-foundry-skill.md).

## Step 2: Ask the skill to create the hosted agent

Ask your coding agent to use the skill for the complete hosted-agent workflow:

```text
Use the Microsoft Foundry Skill hosted-agent quick-start workflow to create my
first hosted agent end to end. Verify my environment first, and stop if I need
to sign in myself. Use Python 3.13, Agent Framework, the Responses API, the
Basic sample, and code deployment. Create a new Foundry project unless I provide
an existing project. Use the model deployment from the Basic sample unless I
provide an existing deployment. Test the agent locally, deploy it to Foundry
Agent Service, and invoke it with: "Write a haiku about deploying cloud
applications."
```

The coding agent should inspect the available Foundry tools when MCP tools are
available, load the hosted agent quick-start workflow, and ask for or default
missing values such as the subscription, region, project name, and whether to use
an existing Foundry project.

## Step 3: Review and approve the plan

1. Review the plan, files, commands, Azure resources, and role assignments the
   coding agent proposes.
1. To match this quickstart, choose **Python 3.13**, **Agent Framework**,
   **Responses API**, **Basic** sample code, and **Code** deployment.
1. Approve cost-bearing resource creation only after you verify the subscription,
   region, resource group, model deployment, and quota.
1. If the coding agent asks you to authenticate, run `az login` and
   `azd auth login` yourself, and then ask the coding agent to continue.

## Step 4: Let the skill scaffold and test the agent

Let the coding agent create the hosted agent project, provision resources when
you choose a new Foundry project, write local environment values, prepare the
local environment, and run a local smoke test. For Python agents, the skill
workflow uses `azd ai agent run` to install dependencies during the first local
run.

The workflow should also add the project guidance file required by the coding
agent host and sanity-check the generated project configuration before the local
test.

If your coding agent host can't keep a local server running for the smoke test,
use the Azure Developer CLI tab in this article for the local test commands. You
can continue to deployment only after you decide to validate the agent remotely
instead.

## Step 5: Deploy and invoke the hosted agent

After the local smoke test succeeds, ask your coding agent to finish the
deployment and remote validation:

```text
Continue with the Microsoft Foundry Skill workflow. Deploy the hosted agent to
Foundry Agent Service, show the deployment status and playground link, and invoke
it remotely with: "Write a haiku about deploying cloud applications." If the
skill workflow requires evaluation suite generation before the final summary,
submit the generation job and show me the follow-up eval command.
```

When the workflow completes, the coding agent should show the hosted agent name,
version, deployment status, endpoint, playground link, resources created, the
response to the test prompt, and any evaluation follow-up command.

:::zone-end

## Clean up resources

Delete the resources when you're finished so you stop incurring charges.

:::zone pivot="azd"

> [!WARNING]
> `azd down` permanently deletes every resource in the resource group, including the Foundry project, model deployments, Container Registry, Application Insights, and the hosted agent. If you provisioned into a resource group that contains other resources, those resources are deleted too.

```
azd down
```

`azd` lists the resources it deletes and prompts for confirmation. Cleanup takes about 2-5 minutes.

:::zone-end

:::zone pivot="vscode"

1. Open the [Azure portal](https://portal.azure.com) and navigate to the resource group that contains your agent.
1. Select **Delete resource group**, type the resource group name to confirm, and select **Delete**.

> [!WARNING]
> Deleting the resource group permanently removes everything in it, including the Foundry project, Container Registry, Application Insights, and the hosted agent.

:::zone-end

:::zone pivot="foundry-skills"

The Microsoft Foundry Skill doesn't delete resources by itself. It can help your
coding agent identify the resources that this quickstart created and choose the
right cleanup method. You or your coding agent still run the cleanup command
after you review and approve it.

1. In the hosted agent project folder, ask your coding agent to review cleanup:

    ```text
    Use the Microsoft Foundry Skill to identify the Azure resources created for
    this quickstart. Confirm whether azd down is the right cleanup method for
    this project, and show me the resources before any deletion command runs.
    ```

1. If the hosted agent project was created with `azd` and the resource group
   contains only quickstart resources, run:

    ```
    azd down
    ```

1. Approve deletion only after you verify the resource group and resources that
   the command lists.

If your coding agent can't run cleanup commands, use the Azure Developer CLI tab
in this article or delete the resource group from the Azure portal.

:::zone-end

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `SubscriptionNotRegistered` | Register the provider: `az provider register --namespace Microsoft.CognitiveServices`. |
| `AuthorizationFailed` during provisioning | Request the **Contributor** role on the subscription or resource group. |
| `AuthenticationError` or `DefaultAzureCredential` failure | To refresh credentials, run `azd auth logout` and then `azd auth login`. |
| `ResourceNotFound` or `DeploymentNotFound` | Verify the endpoint URL and model deployment name in the Foundry portal under **Build** > **Deployments**. |
| `create_version_from_code` fails with `Hosted agent provisioning failed` | Check that `main.py` and `requirements.txt` are at the root of the zip you uploaded, and verify that the model deployment name in `.env` exists in the target Foundry project. |
| `Connection refused` on local run | Ensure no other process is using port 8088. |
| `azd ai agent init` fails | Run `azd version` to verify 1.25.0 or later. Update with `winget upgrade Microsoft.Azd` (Windows) or `brew upgrade azd` (macOS). Run `azd ext list` and upgrade the agent extension with `azd ext upgrade azure.ai.agents` to get 0.1.34-preview or later. |
| Microsoft Foundry Toolkit extension not found | Install the [Microsoft Foundry Toolkit for Visual Studio Code](https://aka.ms/foundrytk) from the Marketplace and switch to the prerelease channel. |
| Coding agent doesn't load the Microsoft Foundry Skill | Install or reload the skill by following [Use the Microsoft Foundry Skill in coding agents](../../how-to/develop/use-microsoft-foundry-skill.md). |
| Coding agent can't run the local smoke test | Use the Azure Developer CLI or VS Code tab in this article for local testing. Continue to remote validation only after you review why local validation isn't available. |
| Local run fails on Windows ARM64 with build errors for `aiohttp`, `grpcio`, `cryptography`, or `httptools` | Prebuilt arm64 wheels aren't published for these packages, and source builds require Microsoft C++ Build Tools. As a workaround, skip Step 3 and validate the agent remotely with `azd deploy` followed by `azd ai agent invoke`. |

For the full permission and role-assignment matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

## What you learned

In this quickstart, you:

* Scaffolded a hosted agent project from the Basic agent sample.
* Uploaded and routed a hosted agent version with the Python SDK or scaffolded the sample with Azure Developer CLI.
* Tested the agent locally.
* Deployed the agent to Foundry Agent Service.
* Sent test prompts from the Python SDK, Azure Developer CLI, VS Code, or a coding agent that
  uses the Microsoft Foundry Skill.

## Next step

> [!div class="nextstepaction"]
> [Build a toolbox and use it with a hosted agent](quickstart-toolbox-agent.md)

## Related content

* [What are hosted agents?](../concepts/hosted-agents.md)
* [Trace your hosted agent](../../observability/quickstarts/quickstart-tracing-hosted-agent.md)
* [Deploy a hosted agent](../how-to/deploy-hosted-agent.md)
* [Author azure.yaml for hosted agents](../how-to/author-azure-yaml.md)
* [Agent development lifecycle](../concepts/development-lifecycle.md)
* [Python hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
