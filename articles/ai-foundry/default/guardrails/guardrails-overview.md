---
title: 'Guardrails and controls overview in Microsoft Foundry'
titleSuffix: Microsoft Foundry
description: Learn about safety and security guardrails that can be applied to models and agents in Microsoft Foundry, including risks, intervention points, and response actions.
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 11/05/2025
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: azure-ai-guardrails
# customer intent: As a developer, I want to understand how guardrails work in Microsoft Foundry so that I can implement appropriate safety measures for my models and agents.
---

# Guardrails and controls overview in Microsoft Foundry

Microsoft Foundry offers safety and security guardrails that can be applied to core models, including image generation models, and agents.  Agent guardrails are in preview. Guardrails consist of a set of controls. The controls define a risk to be detected, intervention points to scan for the risk, and the response action to take in the model or agent when the risk is detected. For example, a risk detection could be the annotation of the risk or blocking the model or agent from further output.

Risks are flagged via a set of classification models designed to detect and prevent the output of undesirable behavior and/or harmful content. Four intervention points are currently supported: user input, tool call (Preview), tool response (Preview), and output. Tool call and tool responses intervention points are applicable to agents only and scan the tool call made as well as content sent to the tool, and the output back from the tool, respectively.

Variations in API configurations and application design might affect completions and thus filtering behavior.

> [!IMPORTANT]
> The guardrail system applies to all Models sold directly by Azure, except for prompts and completions processed by the audio models such as Whisper. For more information, see [Audio models in Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure.md#audio-models). The guardrail system currently applies only to agents developed in the Foundry Agent Service, not to other agents registered in the Foundry Control Plane.

## Guardrails for agents vs models

An individual Foundry guardrail can be applied to one or many models and one or many agents in a project. Some controls within a guardrail may not be relevant to models because the risk, intervention point, or action is specific to agentic behavior or tool calls. Those controls aren't run on models using that guardrail.

Some risks in Preview aren't yet supported for agents. When controls involving that risks are created in a guardrail, and the guardrail is applied to an agent, that control won't take effect in that agent. It's still applied to models using the same guardrail.

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
| Spotlighting (Preview) | ✅  | ❌ |
| Protected material for code | ✅ | ✅ |
| Protected material for text | ✅ | ✅ |
| Groundedness (Preview) | ✅ | ❌ |
| Personally identifiable information (Preview) | ✅ | ✅ |

### Intervention point applicability

The following table summarizes which intervention points are applicable to models and agents:

| Intervention point | Applicable to Models | Applicable to Agents (Preview) |
|-------------------|---------------------|---------------------|
| User input (prompt) | ✅ | ✅ |
| Tool call (Preview) | ❌ | ✅ |
| Tool response (Preview) | ❌ | ✅ |
| Output (completion) | ✅ | ✅ |

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
- A model deployment has a control with Violence detection set to **High** for user input and output
- An agent using that model has a control with Violence detection set to **Low** for user input and output. The agent has no controls for Violence detection at all for tool calls and responses

**Expected behavior for Violence detection in that agent:**
- User queries to the agent are scanned for Violence at a **Low** level
- Tool calls generated internally to the agent by its underlying model, including the content then sent to that tool during the tool call's execution, will **not** be scanned for Violence
- The response back from the tool will **not** be scanned for Violence
- The final output returned to the user in response to their original query are scanned for Violence at a **Low** level

## Default guardrails

By default, models are assigned the **Microsoft.DefaultV2** guardrail. For more information on what is included in the Microsoft Default, see Default safety policy.

Unless another custom guardrail is specified upon creation, agents are assigned by default the guardrails of the model deployment being used by that agent. In other words, if no custom guardrails are specified for an agent, and that agent leverages a GPT-4o mini deployment using a guardrail named "MyCustomGuardrails," the agent will also use "MyCustomGuardrails" until another guardrail is specifically assigned to the agent. An agent will only inherit the Microsoft Default guardrails if its model is using that guardrail or if it's specifically assigned the default manually.


## Next steps

- [Understand content filtering in Azure OpenAI](../../openai/concepts/content-filter.md)
- [Learn about intervention points and controls](intervention-points.md)
- [Configure content filters for Azure OpenAI](../../openai/how-to/content-filters.md)
