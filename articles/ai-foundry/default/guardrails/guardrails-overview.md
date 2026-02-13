---
title: 'Guardrails and controls overview in Microsoft Foundry'
titleSuffix: Microsoft Foundry
description: Learn about safety and security guardrails that can be applied to models and agents in Microsoft Foundry, including risks, intervention points, and response actions.
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 02/13/2026
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: azure-ai-guardrails
# customer intent: As a developer, I want to understand how guardrails work in Microsoft Foundry so that I can implement appropriate safety measures for my models and agents.
---

# Guardrails and controls overview in Microsoft Foundry

Microsoft Foundry provides safety and security guardrails that you can apply to model deployments and agents. Use guardrails to detect harmful content, prevent undesirable outputs, and enforce responsible AI policies across your applications.

A **guardrail** is a named collection of **controls**. Variations in API configurations and application design might affect completions and thus filtering behavior.

Risks are flagged by classification models designed to detect harmful content. Four intervention points are supported:

- **User input** — The prompt sent to a model or agent.
- **Tool call** (Preview) — The action and data the agent proposes to send to a tool. Agents only.
- **Tool response** (Preview) — The content returned from a tool to the agent. Agents only.
- **Output** — The final completion returned to the user.

For more information about intervention points, see [Intervention points and controls](intervention-points.md).

> [!IMPORTANT]
> The guardrail system applies to all [Models sold directly by Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md), except for prompts and completions processed by audio models such as Whisper. For more information, see [Audio models](../../foundry-models/concepts/models-sold-directly-by-azure.md#audio-models). The guardrail system currently applies only to agents developed in the [Foundry Agent Service](/azure/ai-foundry/agents/overview), not to other agents registered in the Foundry Control Plane.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry project](../../how-to/create-projects.md).
- At least one model deployment in your project.
- Azure AI Account Owner role.
  - [!INCLUDE [rbac-create](../includes/rbac-create.md)]

## Guardrails for agents vs models

An individual Foundry guardrail can be applied to one or many models and one or many agents in a project. Some controls within a guardrail may not be relevant to models because the risk, intervention point, or action is specific to agentic behavior or tool calls. Those controls aren't run on models using that guardrail.

Some risks in Preview aren't yet supported for agents. When controls involving those risks are added to a guardrail and the guardrail is applied to an agent, those controls don't take effect for that agent. They still apply to models that use the same guardrail.

### Risk applicability

The following table summarizes which risks are applicable to models and agents:

| Risk | Applicable to Models | Applicable to Agents (Preview) |
|------|---------------------|---------------------|
| Hate | ✅ | ✅ |
| Sexual | ✅ | ✅ |
| Self-harm | ✅ | ✅ |
| Violence | ✅ | ✅ |
| User prompt attacks | ✅ | ✅ |
| Indirect attacks | ✅ | ✅ |
| Spotlighting (Preview) | ✅ | ❌ |
| Protected material for code | ✅ | ✅ |
| Protected material for text | ✅ | ✅ |
| Groundedness (Preview) | ✅ | ❌ |
| Personally identifiable information (Preview) | ✅ | ✅ |

### Severity levels

For content risks (Hate, Sexual, Self-harm, Violence), each control uses a severity level threshold that determines which content is flagged:

| Severity level | Behavior |
|---------------|----------|
| **Off** | Detection is disabled for this risk. Only available for approved customers, see [content filters](../../foundry-models/how-to/configure-content-filters.md |
| **Low** | Flags content at low severity and above. Most restrictive. |
| **Medium** | Flags content at medium severity and above. |
| **High** | Flags only the most severe content. Least restrictive. |

For a detailed breakdown of what each severity level detects, see [Content filtering categories](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new#risk-categories).

### Intervention point applicability

The following table summarizes which intervention points are applicable to models and agents:

> [!IMPORTANT]
> Risks are detected in an agent based on the guardrail it's assigned, not the guardrail of its underlying model. The agentic guardrail fully overrides the model's guardrail.

- A model deployment has a control with Violence detection set to **High** for user input and output
- An agent using that model has a control with Violence detection set to **Low** for user input and output. The agent has no controls for Violence detection at all for tool calls and responses

### Action applicability

The following table summarizes which actions are applicable to models and agents:

| Action | Applicable to Models | Applicable to Agents (Preview) |
|--------|---------------------|---------------------|
| Annotate | ✅ | ❌ |
| Annotate and block | ✅ | ✅ |

### Guardrail inheritance and override

> [!IMPORTANT]
> Risks are detected in an agent based on the guardrail it's assigned, not the guardrail of its underlying model. The agentic guardrail fully overrides the model's guardrail.

**Example scenario:**

| Component | Violence detection setting |
|-----------|---------------------------|
| Model deployment | **High** for user input and output |
| Agent (using that model) | **Low** for user input and output; no Violence controls for tool calls or responses |

**Expected behavior for Violence detection in that agent:**

| Intervention point | Scanned? | Severity level |
|-------------------|----------|----------------|
| User input | Yes | **Low** (agent's setting) |
| Tool call | No | Not configured |
| Tool response | No | Not configured |
| Output | Yes | **Low** (agent's setting) |

## Default guardrails

By default, models are assigned the **Microsoft.DefaultV2** guardrail. For more information about what controls are included, see [Content filtering](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new).

Default guardrail assignment for agents follows these rules:

1. If you assign a custom guardrail to an agent, that guardrail is used.
1. If no custom guardrail is assigned, the agent inherits the guardrail of its underlying model deployment.
1. An agent only uses the **Microsoft.DefaultV2** guardrail if its model deployment uses that guardrail, or if you explicitly assign it.

> [!NOTE]
> For example, if no custom guardrails are specified for an agent and that agent uses a GPT-4o mini deployment with a guardrail named "MyCustomGuardrails," the agent also uses "MyCustomGuardrails" until you assign a different guardrail.

## Next steps

- [Configure guardrails and controls](how-to-create-guardrails.md)
- [Learn about intervention points and controls](intervention-points.md)
- [Understand content filtering in Azure OpenAI](../../openai/concepts/content-filter.md)
- [Configure content filters for Azure OpenAI](../../openai/how-to/content-filters.md)
