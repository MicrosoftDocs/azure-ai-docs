---
title: Migrate from Foundry (classic)
description: Map classic terminology, features, SDKs, and portal navigation to their current equivalents in Microsoft Foundry so you can plan and execute your migration.
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/10/2026
ms.custom:
  - classic-and-new
  - build-2025
ai-usage: ai-assisted
#customer intent: As a developer using Foundry (classic), I want to understand the differences in terminology, features, SDKs, and portal layout so I can migrate my workflows to the current Microsoft Foundry experience.
---

# Migrate from Foundry (classic) portal

Microsoft Foundry evolved through several naming and architectural changes. If you're moving from the classic experience, this article provides a reference mapping between classic and new terminology, capabilities, SDKs, and portal navigation to help you plan and execute the transition.

> [!NOTE]
> **Naming history:** Azure AI Studio (Nov 2023) &rarr; Azure AI Foundry (Nov 2024) &rarr; Microsoft Foundry (Nov 2025). Azure AI Services &rarr; Foundry Tools. The Azure resource type remains `Microsoft.CognitiveServices/accounts`. All names in this documentation refer to the same evolving platform.

## Prerequisites

- An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Foundry project](create-projects.md).

## Terminology mapping

The following table maps classic concepts to their current equivalents.

| Concept | Classic term | Current term | Notes |
| --------- | ------------- | ---------- | ------- |
| Portal (main) | Foundry (classic) | Foundry (new) | Toggle in portal banner switches between them. |
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
| Documentation | Foundry (classic) docs | Foundry (new) docs | Version selector in documentation banner. |

## SDK mapping

Use the following table to identify which SDK packages map to the current Foundry experience and which ones they replace.

| SDK package | Classic equivalent | Status | Notes |
| --- | --- | --- | --- |
| `openai` | `azure-ai-inference` | Use for model inference | `azure-ai-inference` retiring May 30, 2026. |
| `OpenAI()` with `base_url` | `AzureOpenAI()` | Use standard client | Azure-specific code eliminated. |
| `azure-ai-projects` 2.x | `azure-ai-projects` 1.x | Preview &mdash; targets Foundry (new) | 1.x targets Foundry (classic). |
| `azure-ai-projects` 2.x | `azure-ai-generative` | Preview | Capabilities merged into project client. |
| `azure-ai-projects` 2.x | `azure-ai-ml` | Preview | For hub-to-project migration scenarios. |
| `azure-ai-projects` (remote) + `azure-ai-evaluation` (local) | `azure-ai-evaluation` (standalone) | Stable | Remote evaluations via project client; local evaluations unchanged. |
| `azure-search-documents` (via project connections) | `azure-search-documents` | Stable | Separate package, discoverable through project client. |

> [!WARNING]
> Ensure the SDK version matches your portal experience. Using a 2.x SDK sample with a 1.x setup (or vice versa) causes errors.

## Feature comparison

The following table compares feature availability between the classic and current portal experiences.

| Feature | Foundry (classic) | Foundry (new) |
| --------- | ------------------- | --------------- |
| Azure OpenAI resources | &#x2705; | Use Foundry resource (upgrade available) |
| Hub-based projects | &#x2705; | Not visible (use classic portal) |
| Foundry projects | &#x2705; | &#x2705; |
| Chat completions | &#x2705; | &#x2705; |
| Responses API | &#x274C; | &#x2705; |
| Agents v2 (Responses API) | &#x274C; | &#x2705; |
| Multi-agent workflows | &#x274C; | &#x2705; |
| Tool catalog (1,400+ tools) | &#x274C; | &#x2705; |
| Agent memory | &#x274C; | &#x2705; |
| Foundry IQ | &#x274C; | &#x2705; (preview) |
| Hosted agents | &#x274C; | &#x2705; (preview) |
| A2A protocol | &#x274C; | &#x2705; (preview) |
| Foundry Control Plane | &#x274C; | &#x2705; (preview) |
| Agent publishing to M365/Teams | &#x274C; | &#x2705; |
| Fine-tuning | &#x2705; | &#x2705; |
| Evaluations | &#x2705; | &#x2705; (enhanced) |
| Model catalog | &#x2705; | &#x2705; (expanded) |

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
| Build agents | **Agents** in the left pane | **Build** > **Agents** |
| Browse the model catalog | **Model catalog** in the left pane | **Discover** > **Model catalog** |
| View evaluations | **Evaluation** in the left pane | **Build** > **Evaluations** |
| Fine-tune a model | **Fine-tuning** in the left pane | **Build** > **Fine-tuning** |
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

## Related content

- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Use a screen reader with Microsoft Foundry](../tutorials/screen-reader.md)
