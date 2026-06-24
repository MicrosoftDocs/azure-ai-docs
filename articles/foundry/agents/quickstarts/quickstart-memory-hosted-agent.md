---
title: "Quickstart: Give a hosted agent persistent memory"
description: "Provision a Foundry memory store, then deploy a Python hosted agent that remembers facts about each user across sessions by using FoundryMemoryProvider."
author: aahill
ms.author: aahi
ms.date: 06/18/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to add a persistent memory store to my hosted agent so that it remembers facts a user shared in earlier sessions.
---

# Quickstart: Give a hosted agent persistent memory

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this quickstart, you give a [hosted agent](../concepts/hosted-agents.md) persistent, semantic memory backed by a Foundry [memory store](../concepts/runtime-components.md#attach-memory-to-an-agent-preview). Without memory, every conversation starts from scratch. With a memory store, the agent retains stable facts about a user, such as a name or a dietary preference, and recalls them in later sessions.

You complete two parts:

- **Provision a memory store** with a single command. A bundled provisioning hook runs after `azd provision` to create the store and wire it to the agent. The store uses a chat model and an embedding model to extract and index user-profile memories.
- **Deploy a hosted agent** that reads and writes the store through `FoundryMemoryProvider`. The provider retrieves relevant memories before each model call and updates the store with new facts after each turn.

The agent code, memory provider, provisioning hook, and authentication come from the Foundry memory sample, so you focus on the workflow rather than the implementation.

## Prerequisites

This quickstart builds on the hosted-agent toolchain. Complete the [Prerequisites](quickstart-hosted-agent.md#prerequisites) in the hosted agent quickstart first, which cover the Azure subscription, project roles, Python, the Azure Developer CLI (`azd`), and the `microsoft.foundry` extension.

You also need an embedding model deployment in your Foundry project, such as `text-embedding-3-small`. The memory store uses it to index memories. The agent's chat model, such as `gpt-4o`, can be the deployment you already use for hosted agents.

Your identity also needs the **Cognitive Services OpenAI User** role on the Foundry project scope, in addition to the roles in the hosted agent prerequisites. The memory store uses this role to call the embedding deployment. Without it, memory writes fail with a `401` error and the store stays empty.

## Step 1: Initialize the hosted agent

Initialize a hosted agent from the Foundry memory sample. Initialization copies the sample files, including the memory-store provisioning script and the provisioning hook, into a new service directory under `src/`. Run these commands in an empty directory.

```powershell
mkdir my-memory-agent
cd my-memory-agent
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/13-foundry-memory/agent.manifest.yaml"
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
- Sets `MEMORY_STORE_NAME` so the agent reads and writes that store. The hook persists the name to your `azd` environment for local runs and into the agent's `agent.yaml` so `azd deploy` ships it to the container.

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

Build and deploy the agent container. The `postprovision` hook already writes `MEMORY_STORE_NAME` into the agent's `agent.yaml`, so the deployed container reads the same store:

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

## Clean up resources

Delete the resources when you're finished so you stop incurring charges.

Delete the memory store by using the `AIProjectClient`. Run this script in a Python environment that has the `azure-ai-projects` and `azure-identity` packages installed (for example, run `pip install azure-ai-projects azure-identity`):

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

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| The deployed agent has no memory, or `MEMORY_STORE_NAME` is empty | Confirm the `postprovision` hook ran during `azd provision` and that the agent's `agent.yaml` has `MEMORY_STORE_NAME` set. Rerun `azd provision` to run the hook again. |
| Memory writes fail with a `401` error and the store stays empty | Grant the **Cognitive Services OpenAI User** role on the Foundry project scope to your identity and to the deployed agent's runtime identity. |
| `azd provision` fails with a permissions error | Confirm your identity has the project roles listed in the [Prerequisites](quickstart-hosted-agent.md#prerequisites). |
| The agent doesn't recall a fact you shared | Allow a few seconds after storing a fact before you query, so the store finishes indexing the memory. |
| The agent can't read or write memories after deployment | Confirm that the `postprovision` hook created the store against the same project the agent is deployed to. |

## What you learned

In this quickstart, you:

- Created a Foundry memory store with the user-profile capability.
- Deployed a hosted agent that reads and writes to the store through `FoundryMemoryProvider`.
- Verified that the agent recalls user facts across separate sessions, both locally and after deployment.

## Next step

> [!div class="nextstepaction"]
> [Evaluate your hosted agent](../../observability/quickstarts/quickstart-evaluate-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Attach memory to an agent](../concepts/runtime-components.md#attach-memory-to-an-agent-preview)
- [Quickstart: Deploy your first hosted agent](quickstart-hosted-agent.md)
- [Manage hosted agents](../how-to/manage-hosted-agent.md)
