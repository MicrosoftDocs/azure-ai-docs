---
title: "What is Microsoft Foundry?"
description: "Microsoft Foundry is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way."
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.date: 04/29/2026
ms.service: microsoft-foundry
ms.topic: overview
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
  - build-aifnd
  - build-2025
  - doc-kit-assisted
keywords:
  - Foundry Tools
  - cognitive
# customer intent: As a developer, I want to understand what Microsoft Foundry is so that I can use it to build AI applications.
---

# What is Microsoft Foundry?

**Microsoft Foundry** is a unified Azure platform-as-a-service offering for enterprise AI operations, model builders, and application development. This foundation combines production-grade infrastructure with friendly interfaces, enabling developers to focus on building applications rather than managing infrastructure.

Microsoft Foundry unifies agents, models, and tools under a single management grouping with built-in enterprise-readiness capabilities including tracing, monitoring, evaluations, and customizable enterprise setup configurations. The platform provides streamlined management through unified role-based access control (RBAC), networking, and policies under one Azure resource provider namespace.

> [!TIP]
> * Coming from Azure OpenAI? [Upgrade your Azure OpenAI resource to a Foundry resource](./how-to/upgrade-azure-openai.md) while preserving your endpoint, API keys, and existing state. 
> * Using hub-based projects? Hub-based projects are accessible in the [Foundry (classic) portal](../foundry-classic/what-is-foundry.md). New investments are focused on Foundry projects in the new portal.

[!INCLUDE [previous-current](includes/previous-current.md)]

## Your first API call

**Get started now** — [Quickstart: Build with models and agents](./quickstarts/get-started-code.md) | [Open Foundry portal](https://ai.azure.com) | [Get an Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account)

Send a prompt and get a response from a model in a few lines of code:

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/responses/quickstart-responses.py":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/responses/quickstart-responses.cs":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/responses/src/quickstart-responses.ts":::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-responses.sh":::

---

For the full walkthrough, see the [Microsoft Foundry quickstart](./quickstarts/get-started-code.md).

## Available models

Foundry gives you access to over 1,900 models from Microsoft, OpenAI, Anthropic, Mistral, xAI, Meta, DeepSeek, Hugging Face, and more. The following table highlights popular model families to help you choose a starting point.

| Model family | Best for | 
|---|---|
| **GPT-5** | Most capable — complex reasoning, multi-step tasks, and multimodal scenarios |
| **GPT-4.1** | Best balance of capability and cost for production workloads |
| **GPT-4.1 mini** | Fastest — low-latency, high-throughput scenarios |
| **Claude** | Advanced reasoning, code generation, and multimodal tasks |
| **Grok** | Reasoning, coding, and data extraction |
| **Mistral** | Code generation, multilingual, and general-purpose chat |
| **DeepSeek-R1** | Open-weight reasoning at scale |
| **Phi-4** | Small language model — on-device or resource-constrained environments |
| **Meta Llama** | Open models — customization and fine-tuning |

For help choosing between models, see the [GPT-5 vs GPT-4.1 model choice guide](./foundry-models/how-to/model-choice-guide.md). Browse the full catalog in the [Foundry Models overview](./concepts/foundry-models-overview.md).

## What's new

Foundry is evolving fast. Here are some of the latest additions:

- [Prompt Optimizer (preview)](./observability/how-to/prompt-optimizer.md) — Automatically improve agent prompts based on evaluation results.
- [Task Adherence guardrails (preview)](./guardrails/task-adherence.md) — Keep agentic workflows on track with built-in adherence controls.
- [LangChain and LangGraph integration](./how-to/develop/langchain.md) — Build and trace agents with popular open-source frameworks.
- [Fireworks model import (preview)](./how-to/fireworks/enable-fireworks-models.md) — Bring custom models into Foundry through Fireworks.

See [What's new in Microsoft Foundry](./whats-new-foundry.md) for the full list.

## Choose your path

Foundry supports multiple developer surfaces. Use the following table to find the right starting point for your scenario.

| I want to... | Start here |
|---|---|
| Call a model from code | [Quickstart: Your first API call](./quickstarts/get-started-code.md) |
| Build an agent with tools and memory | [Agent Service overview](./agents/concepts/workflow.md) |
| Explore models in the browser | [Foundry portal playgrounds](./concepts/concept-playgrounds.md) |
| Deploy and manage models at scale | [Foundry Models overview](./concepts/foundry-models-overview.md) |
| Develop in VS Code | [Foundry for VS Code](./how-to/develop/get-started-projects-vs-code.md) |
| Set up governance and security | [Foundry Control Plane](./control-plane/overview.md) |

## Who is Foundry for?

Microsoft Foundry serves three primary audiences:

* **Application developers** building AI-powered products with agents, models, and tools. Start with the [quickstart](./quickstarts/get-started-code.md).
* **ML engineers and data scientists** who [fine-tune models](./openai/concepts/fine-tuning-considerations.md), [run evaluations](./observability/concepts/trace-agent-concept.md), and [manage model deployments](./foundry-models/how-to/monitor-models.md).
* **IT administrators and platform engineers** who govern AI resources, enforce policies, and manage access across teams. See [security](./concepts/architecture.md#security-driven-separation-of-concerns) and governance and [Foundry Control Plane](./control-plane/overview.md).

## Key capabilities

### Build agents

**[Multi-agent orchestration](agents/concepts/workflow.md)** — Build collaborative agent behavior and complex workflow execution using SDKs for C# and Python.

**[Tool catalog](agents/concepts/tool-catalog.md)** — Connect over 1,400 tools through public and private catalogs.

**[Memory](agents/concepts/what-is-memory.md)** — Retain and recall contextual information across interactions without requiring repeated input.

**[Foundry IQ knowledge integration](agents/concepts/what-is-foundry-iq.md)** — Ground agent responses in enterprise or web content with citation-backed answers.

**[Publishing](agents/how-to/publish-copilot.md)** — Publish agents to Microsoft 365, Teams, BizChat, or containerized deployments.

### Operate and govern

**[Real-time observability](observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation)** — Monitor performance and governance with built-in metrics and model tracking.

**Centralized AI asset management** — Manage all agents, models, and tools from the **Operate** section, including agents registered from other clouds.

**Enterprise controls** — Full authentication support for MCP and A2A, AI gateway integration, and Azure Policy integration.

## Microsoft Foundry API and SDKs

The [Microsoft Foundry API](/rest/api/aifoundry/) provides a consistent contract for building agentic applications across different model providers. [SDK client libraries](how-to/develop/sdk-overview.md) are available for:

- Python
- C#
- JavaScript/TypeScript (preview)
- Java (preview)

The [Microsoft Foundry for VS Code Extension](how-to/develop/get-started-projects-vs-code.md) helps you explore models and develop agents directly in your development environment.

## Foundry portal

The [Microsoft Foundry portal](https://ai.azure.com) is where you manage projects, deploy models, build agents, and monitor your AI assets. To use the current version, make sure the **New Foundry** toggle in the banner is set to on.

:::image type="icon" source="media/version-banner/new-foundry.png" alt-text="Screenshot of New Foundry toggle in the banner.":::

> [!TIP]
> See [Find features in the Foundry portal](how-to/navigate-from-classic.md) if you're used to the Foundry (classic) portal and not sure where to find things now.

For details on switching between projects or finding resources created in Foundry (classic), see [Find features in the Foundry portal](how-to/navigate-from-classic.md).

## Pricing and billing

The platform is free to use and explore. Pricing occurs at the deployment level. Each product within Foundry (models, agents, tools) has its own billing model and price.

Using Foundry also incurs costs associated with the underlying services. To learn more, read [Plan and manage costs for Foundry Tools](./concepts/manage-costs.md).

Use the [Total Economic Impact calculator for Foundry](https://aka.ms/Foundry-ROI-Calculator) to estimate your return on investment.

## Region availability

Foundry is available in most regions where Foundry Tools are available. For more information, see [region support for Microsoft Foundry](reference/region-support.md).

## How to get access

You need an [Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). Then sign in to [Microsoft Foundry](https://ai.azure.com?cid=learnDocs).

## Related content

- [Quickstart: Get started with Microsoft Foundry](./quickstarts/get-started-code.md)
- [Quickstart: Set up Foundry resources](./tutorials/quickstart-create-foundry-resources.md)
- [Create a project](./how-to/create-projects.md)
- [Get started with an AI template](how-to/develop/ai-template-get-started.md)
- [What's new in Microsoft Foundry documentation?](whats-new-foundry.md)
