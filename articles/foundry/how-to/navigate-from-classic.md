---
title: Migrate from the Foundry (classic) portal
description: Map classic terminology, features, SDKs, and portal navigation to their current equivalents in Microsoft Foundry so you can plan and execute your migration.
author: sdgilley
ms.author: sgilley
ms.reviewer: nbrady
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/10/2026
ms.custom:
  - classic-and-new
  - build-2025
ai-usage: ai-assisted
#customer intent: As a developer using the Foundry (classic) portal, I want to understand the differences in terminology, features, SDKs, and portal layout so I can migrate my workflows to the current Microsoft Foundry portal experience.
---

# Migrate from the Foundry (classic) portal

Microsoft Foundry evolved through several naming and architectural changes. If you're moving from the classic portal experience, this article helps you plan and execute the transition with reference mappings for terminology, capabilities, SDKs, and portal navigation.

> [!NOTE]
> **Product naming**: Microsoft's AI Platform has evolved from Azure AI Studio → Azure AI Foundry → to Microsoft Foundry (current). Similarly, our AI services portfolio evolved with the platform from Azure Cognitive Services → Azure AI Services → to Foundry Tools (current). Despite the platform evolution, the Azure resource type remains `Microsoft.CognitiveServices/accounts`. All names in this documentation refer to the same evolving platform.

## Prerequisites

- An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Foundry project](create-projects.md).
- **For SDK migration:** Python 3.9+ or .NET 8+, with `azure-ai-projects` 2.x and `openai` packages installed.
- **For resource upgrade:** Owner or Contributor role on the Azure OpenAI resource you plan to upgrade.

> [!IMPORTANT]
> **Key migration dates:**
> - **May 30, 2026** &mdash; `azure-ai-inference` package retires. [Migrate to the `openai` package](./model-inference-to-openai-migration).
> - **August 26, 2026** &mdash; Assistants API sunsets.  Use the generally available [Microsoft Foundry Agents service](../agents/overview.md). Follow the [migration guide](../agents/how-to/migrate.md#migrate-classic-agents-to-new-agents) to update your workloads. [Learn more](../agents/how-to/migrate.md).

## Plan your migration

Follow these steps to move from the classic portal experience to the current Foundry portal:

1. **Review terminology changes.** Scan the [terminology mapping](#terminology-mapping) to understand renamed concepts and new resource types.
1. **Check the feature comparison.** Use the [feature comparison](#feature-comparison) table to identify capabilities that are new, enhanced, or classic-only.
1. **Update your SDK packages.** Replace deprecated packages using the [SDK mapping](#sdk-mapping) table.
1. **Migrate agents to the Responses API.** Rewrite agents that use the Assistants API to use the [Responses API](../foundry-models/how-to/generate-responses.md) before the August 2026 sunset.
1. **Validate in the new portal.** Use the [portal navigation](#navigate-the-portal) reference to verify your workflows in the current experience.

## Terminology mapping

The following table maps classic concepts to their current equivalents.

| Concept | Classic term | Current term | Notes |
| --------- | ------------- | ---------- | ------- |
| Portal (main) | Foundry (classic) portal | Foundry portal | Toggle in portal banner switches between them. |
| Portal settings | Management Center | Operate section | Navigation reorganized. |
| Resource type | Azure OpenAI + Hub | Foundry Resource | Single `AIServices` kind with child projects. |
| AI services | Azure AI Services | Foundry Tools | Speech, Vision, Language, Content Safety, Content Understanding. |
| Model billing | Model-as-a-Service (MaaS) | Foundry Direct Models | First-party models billed directly via Azure meters. |
| RBAC roles | Cognitive Services OpenAI User | Azure AI User, Azure AI Project Manager, Azure AI Owner | New roles with control/data plane separation. |
| API wire protocol | Assistants API | Responses API | Assistants API sunset: August 26, 2026. |
| API versioning | Monthly `api-version` params | v1 stable routes | No version parameter required. |
| Conversation state | Threads | Conversations | Conversations store items (messages, tool calls, outputs), not just messages. |
| Chat messages | Messages | Items | Items are a superset of messages. |
| Execution | Runs (async, polled) | Responses (sync by default) | No polling loop required. |
| Agent definition | Assistants / Agents | Agent Versions | Versioned, with explicit kind (prompt, workflow, hosted). |
| Agent creation | `create_agent()` | `create_version()` | Uses `PromptAgentDefinition`. |
| Endpoints | Multiple (openai, azureml, cognitiveservices, search, speech) | Single project endpoint + OpenAI v1 endpoint | Simplified endpoint management. |
| Documentation | [Classic docs](../../foundry-classic/what-is-foundry.md) | [Current docs](../what-is-foundry.md) | Content in two separate doc sets. |

## SDK mapping

Use the following table to identify which SDK packages map to the current Foundry experience and which ones they replace.

| SDK package | Classic equivalent | Status | Notes |
| --- | --- | --- | --- |
| `openai` | `azure-ai-inference` | Use for model inference | `azure-ai-inference` retiring May 30, 2026. |
| `OpenAI()` with `base_url` | `AzureOpenAI()` | Use standard client | Azure-specific code eliminated. |
| `azure-ai-projects` 2.x | `azure-ai-projects` 1.x | Stable &mdash; targets the new portal | 1.x targets the classic portal experience. |
| `azure-ai-projects` 2.x | `azure-ai-generative` | Stable | Capabilities merged into project client. |
| `azure-ai-projects` 2.x | `azure-ai-ml` | Stable | For hub-to-project migration scenarios. |
| `azure-ai-projects` (remote) + `azure-ai-evaluation` (local) | `azure-ai-evaluation` (standalone) | Stable | Remote evaluations via project client; local evaluations unchanged. |
| `azure-search-documents` (via project connections) | `azure-search-documents` | Stable | Separate package, discoverable through project client. |

> [!WARNING]
> Ensure the SDK version matches your portal experience. Using a 2.x SDK sample with a 1.x setup (or vice versa) causes errors.

The following example shows the most common SDK migration &mdash; replacing the Azure-specific `AzureOpenAI` client with the standard `OpenAI` client.

**Classic (before):**

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://my-resource.openai.azure.com",
    api_key="my-key",
    api_version="2024-12-01-preview"
)
```

**Current (after):**

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

client = OpenAI(
    base_url="https://my-project.services.ai.azure.com/openai/v1",
    default_headers={"Authorization": f"Bearer {get_bearer_token_provider(DefaultAzureCredential(), 'https://cognitiveservices.azure.com/.default')()}"}
)
```

## Feature comparison

The following tables compare feature availability between the classic and current portal experiences.

### Available in both portals

| Feature | Classic | Current | Notes |
| --- | --- | --- | --- |
| Foundry projects | &#x2705; | &#x2705; | |
| Chat completions | &#x2705; | &#x2705; | |
| Fine-tuning | &#x2705; | &#x2705; | |
| Evaluations | &#x2705; | &#x2705; | Enhanced in current portal |
| Model catalog | &#x2705; | &#x2705; | Expanded in current portal |

### New in the current portal

These features are available only in the current Foundry portal:

| Feature | Status |
| --- | --- |
| Responses API | GA |
| Agents v2 (Responses API) | GA |
| Tool catalog (1,400+ tools) | GA  (check label on individual tools in the catalog to determine if they are GA or Preview)
| Multi-agent workflows | Preview |
| Agent memory | Preview |
| Agent publishing to M365/Teams | GA |
| Foundry IQ | Preview |
| Hosted agents | Preview |
| A2A protocol | Preview |
| Foundry Control Plane | Preview |

### Classic-only (migration required)

| Feature | Classic | Current | Migration action |
| --- | --- | --- | --- |
| Azure OpenAI resources | &#x2705; | Use Foundry resource | Upgrade to a Foundry resource |
| Hub-based projects | &#x2705; | Not visible | Switch to classic portal or migrate to Foundry projects |

## Navigate the portal

The classic portal uses a single customizable left pane for all navigation, with **Management center** at the bottom. The current portal splits features across five top-level sections, each with its own left pane.

:::image type="content" source="../media/navigate-from-classic/foundry-home.png" alt-text="Screenshot of home page of the current Foundry portal.":::

| Section | Scope | What you find there |
| --- | --- | --- |
| **Home** | Selected project | Project overview and quick actions |
| **Discover** | Selected project | Model catalog and model benchmarks |
| **Build** | Selected project | Agents, models, playgrounds, evaluations, fine-tuning |
| **Operate** | All projects | Admin, quota, compliance, fleet health, tracing |
| **Docs** | N/A | Documentation links |

The following table maps frequently used classic portal locations to their current equivalents.

| Task | Classic portal location | Current portal location |
| --- | --- | --- |
| View model deployments | **Models + endpoints** in the left pane | **Build** > **Models** |
| Open a playground | **Playgrounds** in the left pane | **Build** > **Models** > select a model |
| Build agents | **Agents** in the left pane | **Build** > [**Agents**](../agents/quickstarts/quickstart-hosted-agent.md) |
| Browse the model catalog | **Model catalog** in the left pane | **Discover** > **Model catalog** |
| View evaluations | **Evaluation** in the left pane | **Build** > [**Evaluations**](evaluate-generative-ai-app.md) |
| Fine-tune a model | **Fine-tuning** in the left pane | **Build** > [**Fine-tuning**](../openai/how-to/fine-tuning.md) |
| Tracing and monitoring | **Tracing** in the left pane | **Operate** > **Tracing** |
| Manage quotas | **Management center** > **Quota** | **Operate** > **Quota** |
| Manage users and permissions | **Management center** > **Users** | **Operate** > **Admin** |
| View all projects and resources | **Management center** > **All resources** | **Operate** > **Admin** |
| Connected resources | **Management center** > **Connected resources** | **Operate** > **Admin** > select a project |
| Guardrails and content filters | **Guardrails + controls** in the left pane | **Operate** > **Compliance** |

## Switch between portal experiences

You can switch between the classic and current portal experiences at any time. The toggle preserves your current context, such as the project you're working in.

> [!TIP]
> The current portal shows only Foundry projects. If you need to access hub-based projects or other resource types, switch back to the classic portal.

1. Look for the **New Foundry** toggle in the top banner.
1. Select the toggle to switch between the classic and current experiences.
1. The page reloads with the selected portal interface.

## Troubleshoot common migration issues

| Symptom | Cause | Resolution |
| --- | --- | --- |
| `ModuleNotFoundError` or unexpected API behavior | SDK version doesn't match your portal target | Check the [SDK mapping](#sdk-mapping) table and install the correct package version |
| Projects missing from the new portal | Hub-based projects aren't visible in the current portal | Switch to the classic portal to access hub-based projects, or [migrate to Foundry projects (article appears in the classic documentation)](../../foundry-classic/how-to/migrate-project.md) |
| Endpoint connection failures | Old multi-endpoint URLs no longer resolve | Update to the single project endpoint format (`https://<project>.services.ai.azure.com`) |
| `AuthenticationError` with new client | API key used with `OpenAI()` client without proper header | Use `DefaultAzureCredential` with a bearer token provider as shown in the [SDK migration example](#sdk-mapping) |
| Agent code returns `404` or `MethodNotAllowed` | Assistants API calls sent to a Responses API endpoint | Rewrite agent code to use the Responses API (`create_version()` instead of `create_agent()`) |

## Related content

- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Get started with Foundry Agent Service](../agents/quickstarts/quickstart-hosted-agent.md)
- [Develop with the Responses API](../openai/how-to/responses.md)
- [Deploy models from the model catalog](../foundry-models/how-to/deploy-foundry-models.md)
- [Use a screen reader with Microsoft Foundry](../tutorials/screen-reader.md)
