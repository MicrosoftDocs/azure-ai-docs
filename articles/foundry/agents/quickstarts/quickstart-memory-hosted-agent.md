---
title: "Quickstart: Give a hosted agent persistent memory"
description: "Provision a Foundry memory store, then deploy a Python hosted agent that remembers facts about each user across sessions by using FoundryMemoryProvider."
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
# customer intent: As a developer, I want to add a persistent memory store to my hosted agent so that it remembers facts a user shared in earlier sessions.
---

# Quickstart: Give a hosted agent persistent memory

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this quickstart, you give a [hosted agent](../concepts/hosted-agents.md) persistent, semantic memory backed by a Foundry [memory store](../concepts/runtime-components.md#attach-memory-to-an-agent-preview). Without memory, every conversation starts from scratch. With a memory store, the agent retains stable facts about a user, such as a name or a dietary preference, and recalls them in later sessions.

You complete two parts:

- **Provision a memory store** and wire it to the agent. In the Azure Developer CLI path, a bundled provisioning hook runs after `azd provision`. In the Python path, you create the store directly with the SDK. The store uses a chat model and an embedding model to extract and index user-profile memories.
- **Deploy a hosted agent** that reads and writes the store through `FoundryMemoryProvider`. The provider retrieves relevant memories before each model call and updates the store with new facts after each turn.

The agent code, memory provider, and authentication come from the Foundry memory sample, so you focus on the workflow rather than the implementation.

## Prerequisites

This quickstart builds on the hosted-agent toolchain. Complete the [Prerequisites](quickstart-hosted-agent.md#prerequisites) in the hosted agent quickstart first, which cover the Azure subscription, project roles, Python, the Azure Developer CLI (`azd`), and the `microsoft.foundry` extension.

:::zone pivot="azd"

You use Azure Developer CLI in this path to scaffold the sample, provision the memory store through a bundled `postprovision` hook, run the agent locally, and deploy it.

:::zone-end

:::zone pivot="python"

You use the Python SDK in this path to create the memory store with `AIProjectClient.beta.memory_stores.create(...)`, upload the hosted-agent code as a new version, route traffic to it temporarily, and validate that the same signed-in user is remembered across separate calls.

Install the Python packages used in this path:

```bash
pip install "azure-ai-projects>=2.3.0" azure-identity python-dotenv
```

:::zone-end

You also need an embedding model deployment in your Foundry project, such as `text-embedding-3-small`. The memory store uses it to index memories. The agent's chat model, such as `gpt-4o`, can be the deployment you already use for hosted agents.

Your identity needs the **Foundry User** role on the Foundry project scope through the hosted-agent prerequisites, and it also needs the **Cognitive Services OpenAI User** role on the same scope. The memory store uses Foundry project data-plane access plus the embedding deployment. Without the OpenAI role, memory writes fail with a `401` error and the store stays empty.

:::zone pivot="azd"

## Step 1: Initialize the hosted agent

Initialize a hosted agent from the Foundry memory sample. Initialization copies the sample files, including the memory-store provisioning script and the provisioning hook, into a new service directory under `src/`. Run these commands in an empty directory.

```powershell
mkdir my-memory-agent
cd my-memory-agent
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/13-foundry-memory/azure.yaml"
```

Follow the prompts to select your subscription, project, and a model deployment. If you don't have a Foundry project, `azd ai agent init` guides you through creating one.

## Step 2: Enable one-command provisioning

The sample includes a `postprovision` hook that creates the memory store and wires it to the agent automatically each time you run `azd provision`. Register the hook at the top level of the `azure.yaml` file that `azd ai agent init` generated.

Open `azure.yaml` and add the following top-level block. Replace `<agent-name>` with the service folder that initialization created under `src/`:

```yaml
hooks:
  postprovision:
    posix:
      shell: sh
      run: ./src/<agent-name>/hooks/postprovision.sh
    windows:
      shell: pwsh
      run: ./src/<agent-name>/hooks/postprovision.ps1
```

The hook is self-locating and idempotent. It runs correctly no matter which directory `azd` invokes it from, and reruns leave an existing store as-is.

> [!NOTE]
> Register `postprovision` at the top level of `azure.yaml`. Service-scoped hooks support only the package and deploy lifecycle, not provisioning.

## Step 3: Provision the memory store and Azure resources

1. Point the hook at the embedding model deployment that powers the store's semantic memory:

    ```powershell
    azd env set AZURE_AI_EMBEDDING_MODEL_DEPLOYMENT_NAME "text-embedding-3-small"
    ```

1. Provision:

    ```powershell
    azd provision
    ```

`azd provision` creates or reuses your Foundry project and chat model deployment. Then the `postprovision` hook:

- Creates the memory store with the user-profile capability enabled and verifies it on the service.
- Sets `MEMORY_STORE_NAME` so the agent reads and writes that store. The hook persists the name to your `azd` environment for local runs and into the service environment in `azure.yaml` so `azd deploy` ships it to the container.

The CLI path doesn't show a separate `create memory store` command because the bundled hook runs that creation logic for you as part of `azd provision`.

The hook defaults the store name to `agent_framework_memory`. To use a different name, set it before you provision:

```powershell
azd env set MEMORY_STORE_NAME "<your-store-name>"
```

## Step 4: Run the agent locally

1. Start the agent:

    ```powershell
    azd ai agent run
    ```

    This command creates a virtual environment, installs dependencies, and serves the agent on `http://localhost:8088`. The hook already sets `MEMORY_STORE_NAME` in your `azd` environment, so you don't need extra configuration. Preview packages can produce pip warnings during setup. These warnings are nonblocking.

1. In a separate terminal, tell the agent a fact about yourself:

    ```powershell
    azd ai agent invoke --local "Hi! My name is Linda and I'm vegetarian. Please remember that."
    ```

1. Start a new session and confirm the agent recalls the fact from the store rather than from conversation history:

    ```powershell
    azd ai agent invoke --local --new-session "Do you remember my name and any dietary preference I told you earlier?"
    ```

    The agent answers with your name and preference, which proves it retrieved them from the memory store.

## Step 5: Deploy to Foundry Agent Service

Build and deploy the agent container. The `postprovision` hook already writes `MEMORY_STORE_NAME` into `azure.yaml`, so the deployed container reads the same store:

```powershell
azd deploy
```

When the command finishes, the output shows links to the agent playground and the agent endpoint. Verify memory across sessions on the deployed agent. Store a fact:

```powershell
azd ai agent invoke --new-session "Hi! My name is Marco and I'm allergic to peanuts. Please remember this about me."
```

Then recall it in a fresh session:

```powershell
azd ai agent invoke --new-session "What's my name, and is there any food I should avoid?"
```

The deployed agent answers with the remembered name and allergy.

:::zone-end

:::zone pivot="python"

## Step 1: Create or choose a Foundry project

1. Open [Azure AI Foundry](https://ai.azure.com) and create a Foundry project, or select an existing one.
1. In the project, deploy:
   * A chat-capable model such as `gpt-5.4-mini`.
   * An embedding model such as `text-embedding-3-small`.
1. Copy the project endpoint from **Overview** and the deployment names from **Build** > **Deployments**.

## Step 2: Download the Foundry memory sample

Clone the Foundry samples repo:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
```

Create a working folder for the deployment scripts. In that folder, create a `.env` file with these values:

```text
FOUNDRY_PROJECT_ENDPOINT=<your-project-endpoint>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-chat-model-deployment-name>
AZURE_AI_EMBEDDING_MODEL_DEPLOYMENT_NAME=<your-embedding-model-deployment-name>
FOUNDRY_HOSTED_AGENT_NAME=memory-agent
MEMORY_STORE_NAME=agent_framework_memory
FOUNDRY_SAMPLE_PATH=<full-path-to-foundry-samples/samples/python/hosted-agents/agent-framework/responses/13-foundry-memory/src/agent-framework-agent-foundry-memory-responses>
```

## Step 3: Provision the memory store with Python

This script is safe to rerun. It first calls `get(...)` to see whether the memory store already exists. Only if the store isn't found does it call `create(...)`.

Create a file named `provision_memory_store.py` in the same working folder as `.env`:

```python
import asyncio
import os

from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import MemoryStoreDefaultDefinition, MemoryStoreDefaultOptions
from azure.core.exceptions import ResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    memory_store_name = os.environ["MEMORY_STORE_NAME"]
    chat_model = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]
    embedding_model = os.environ["AZURE_AI_EMBEDDING_MODEL_DEPLOYMENT_NAME"]

    async with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential, allow_preview=True) as project,
    ):
        try:
            existing = await project.beta.memory_stores.get(name=memory_store_name)
            print(f"Memory store '{existing.name}' already exists (id={existing.id}); leaving as-is.")
            return
        except ResourceNotFoundError:
            pass

        definition = MemoryStoreDefaultDefinition(
            chat_model=chat_model,
            embedding_model=embedding_model,
            options=MemoryStoreDefaultOptions(
                chat_summary_enabled=False,
                user_profile_enabled=True,
                user_profile_details=(
                    "Avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials"
                ),
            ),
        )

        created = await project.beta.memory_stores.create(
            name=memory_store_name,
            description="Memory store for the hosted-agent memory quickstart",
            definition=definition,
        )
        print(f"Created memory store '{created.name}' (id={created.id}).")


asyncio.run(main())
```

Run the script:

```bash
python provision_memory_store.py
```

## Step 4: Deploy the hosted agent with Python

Create a file named `deploy_memory_agent.py` in the same working folder as `.env`:

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
agent_name = os.environ.get("FOUNDRY_HOSTED_AGENT_NAME", "memory-agent")
memory_store_name = os.environ["MEMORY_STORE_NAME"]
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
    AIProjectClient(endpoint=endpoint, credential=credential, allow_preview=True) as project_client,
):
    original_agent_endpoint = None
    created = None

    try:
        created = project_client.agents.create_version_from_code(
            agent_name=agent_name,
            description="Hosted agent with persistent Foundry memory.",
            definition=HostedAgentDefinition(
                cpu="0.5",
                memory="1Gi",
                code_configuration=CodeConfiguration(
                    runtime="python_3_13",
                    entry_point=["python", "main.py"],
                    dependency_resolution=CodeDependencyResolution.REMOTE_BUILD,
                ),
                environment_variables={
                    "FOUNDRY_PROJECT_ENDPOINT": endpoint,
                    "AZURE_AI_MODEL_DEPLOYMENT_NAME": model_name,
                    "MEMORY_STORE_NAME": memory_store_name,
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

        with project_client.get_openai_client(agent_name=agent_name) as openai_client:
            first_response = openai_client.responses.create(
                input="Hi! My name is Linda and I'm vegetarian. Please remember that.",
            )
            print(first_response.output_text)

            time.sleep(10)

            second_response = openai_client.responses.create(
                input="Do you remember my name and any dietary preference I told you earlier?",
            )
            print(second_response.output_text)
    finally:
        if original_agent_endpoint is not None:
            project_client.agents.update_details(agent_name=agent_name, agent_endpoint=original_agent_endpoint)

        if created is not None:
            project_client.agents.delete_version(agent_name=agent_name, agent_version=created.version, force=True)
```

Run the script:

```bash
python deploy_memory_agent.py
```

This script uploads the memory sample as a new hosted-agent version, points the hosted agent at that version temporarily, invokes it twice as the same signed-in user, and restores the previous endpoint configuration when it finishes.

## Step 5: Verify that memory persists

The first call stores the fact in the memory store. The second call asks for the remembered fact in a separate request. If the memory store is configured correctly, the response should mention the same name and dietary preference that you supplied in the first request.

:::zone-end

## Clean up resources

Delete the resources when you're finished so you stop incurring charges.

:::zone pivot="azd"

To delete the memory store, use the `AIProjectClient`. Run this script in a Python environment that has the `azure-ai-projects` and `azure-identity` packages installed (for example, run `pip install "azure-ai-projects>=2.3.0" azure-identity`):

```python
import asyncio
from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient

async def delete():
    async with (
        DefaultAzureCredential() as credential,
        AIProjectClient(
            endpoint="https://<account>.services.ai.azure.com/api/projects/<project>",
            credential=credential,
            allow_preview=True,
        ) as project,
    ):
        await project.beta.memory_stores.delete("agent_framework_memory")

asyncio.run(delete())
```

Delete the agent and its Azure resources:

> [!WARNING]
> `azd down` permanently deletes every resource in the resource group, including the Foundry project, model deployments, Container Registry, and the hosted agent. If you provisioned into a resource group that contains other resources, those resources are deleted too.

```powershell
azd down
```

:::zone-end

:::zone pivot="python"

To delete the memory store, use the same script pattern with your memory store name:

```python
import asyncio
import os

from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


async def delete() -> None:
    async with (
        DefaultAzureCredential() as credential,
        AIProjectClient(
            endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            credential=credential,
            allow_preview=True,
        ) as project,
    ):
        await project.beta.memory_stores.delete(os.environ["MEMORY_STORE_NAME"])


asyncio.run(delete())
```

If you created a dedicated resource group or project for this quickstart, delete it from the Azure portal after you no longer need the chat deployment, embedding deployment, or hosted agent.

:::zone-end

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| The deployed agent has no memory, or `MEMORY_STORE_NAME` is empty | Confirm the `postprovision` hook ran during `azd provision` and that `azure.yaml` has `MEMORY_STORE_NAME` set. Rerun `azd provision` to run the hook again. |
| Memory writes fail with a `401` error and the store stays empty | Confirm the caller already has **Foundry User** access on the Foundry project scope, and grant the **Cognitive Services OpenAI User** role on the same scope to your identity and to the deployed agent's runtime identity. |
| `azd provision` fails with a permissions error | Confirm your identity has the project roles listed in the [Prerequisites](quickstart-hosted-agent.md#prerequisites). |
| `project.beta.memory_stores.create(...)` fails with `Authentication to the Azure OpenAI resource failed` | Confirm your identity already has **Foundry User** access on the Foundry project scope, and also has the **Cognitive Services OpenAI User** role on that scope. Also verify that `AZURE_AI_EMBEDDING_MODEL_DEPLOYMENT_NAME` points to a valid embedding deployment. |
| The Python deployment succeeds but the second call doesn't recall the stored fact | Wait a few more seconds before the second call so the memory store finishes indexing, then run the script again. |
| The agent doesn't recall a fact you shared | Allow a few seconds after storing a fact before you query, so the store finishes indexing the memory. |
| The agent can't read or write memories after deployment | Confirm that the `postprovision` hook created the store against the same project the agent is deployed to. |

## What you learned

In this quickstart, you:

- Created a Foundry memory store with the user-profile capability.
- Deployed a hosted agent that reads and writes to the store through `FoundryMemoryProvider` by using Azure Developer CLI or the Python SDK.
- Verified that the agent recalls user facts across separate sessions, either locally with Azure Developer CLI or remotely with the Python SDK after deployment.

## Next step

> [!div class="nextstepaction"]
> [Evaluate your hosted agent](../../observability/quickstarts/quickstart-evaluate-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Attach memory to an agent](../concepts/runtime-components.md#attach-memory-to-an-agent-preview)
- [Quickstart: Deploy your first hosted agent](quickstart-hosted-agent.md)
- [Manage hosted agents](../how-to/manage-hosted-agent.md)
