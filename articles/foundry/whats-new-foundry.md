---
title: "Microsoft Foundry docs: What's new for May 2026"
description: "Discover documentation and product updates in Microsoft Foundry for May 2026."
ms.author: smcdowell
author: skpmcdowell
ms.topic: whats-new
ms.subject: ai-foundry
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
  - doc-kit-assisted
ms.date: 05/26/2026
---

# What's new in Microsoft Foundry?
Welcome! This article highlights key article and product updates in Microsoft Foundry for May 2026.
<br>

## New articles

- Azure OpenAI
  - [Quickstart: Create a provisioned throughput deployment](openai/provisioned-quickstart.md)
  - [Determine provisioned throughput unit (PTU) sizing for a workload](openai/how-to/provisioned-throughput-sizing.md)
  - [Auto and direct model routing with the Responses API](openai/how-to/responses-model-routing.md)
  - [Use model router with Foundry agents](openai/how-to/model-router-agents.md)
  - [Automate Azure OpenAI deployments with quota](openai/how-to/automate-quota-deployments.md)
  - [Get started with Azure OpenAI audio generation](openai/audio-completions-quickstart.md)
- Foundry Agent Service
  - [Enable incoming A2A on a Foundry agent (preview)](agents/how-to/enable-agent-to-agent-endpoint.md)
  - [Routines in Microsoft Foundry (preview)](agents/concepts/routines.md)
  - [Automate agents with routines (preview)](agents/how-to/use-routines.md)
  - [Build a voice agent with hosted agents (preview)](agents/how-to/build-voice-agent.md)
  - [Add managed MCP servers powered by connector namespaces (preview)](agents/how-to/tools/connectors.md)
  - [Connect agents to Microsoft Fabric with Fabric IQ (preview)](agents/how-to/tools/fabric-iq.md)
  - [Connect agents to Microsoft 365 with Work IQ (preview)](agents/how-to/tools/work-iq.md)
  - [Enable tool search in a toolbox (preview)](agents/how-to/tools/tool-search.md)
  - [What is the agent optimizer? (preview)](agents/concepts/agent-optimizer-overview.md)
  - [Quickstart: Optimize a hosted agent (preview)](agents/quickstarts/quickstart-optimize-hosted-agent.md)
  - [Make your agent optimizer-ready (preview)](agents/how-to/make-agent-optimizer-ready.md)
  - [Create an evaluation dataset for the agent optimizer (preview)](agents/how-to/create-optimizer-dataset.md)
  - [Optimize agent instructions, skills, tools, and models (preview)](agents/how-to/optimize-agent-targets.md)
- Evaluations and observability
  - [Rubric evaluators (preview)](concepts/evaluation-evaluators/rubric-evaluators.md)
  - [Run agent evaluations with the azd CLI (preview)](observability/how-to/azure-developer-cli-evaluation.md)
  - [Run benchmark evaluations in Microsoft Foundry (preview)](observability/how-to/benchmark-evaluations.md)
  - [Generate a synthetic evaluation dataset (preview)](observability/how-to/evaluation-dataset-synthetic.md)
  - [Review agent interactions with Trace Replay (preview)](observability/how-to/trace-agent-replay.md)
  - [Convert agent traces into evaluation datasets (preview)](observability/how-to/traces-to-dataset.md)
  - [Microsoft Foundry Tracing and Data Handling](observability/concepts/trace-data.md)
- Guardrails
  - [Configure guided guardrail set-up for an agent (preview)](guardrails/guided-set-up.md)
- Foundry Models and platform
  - [Govern model router deployments with Azure Policy](how-to/model-router-policy.md)
  - [Instant models in Microsoft Foundry (preview)](concepts/instant-models.md)
  - [Region availability for Foundry Models sold directly by Azure](foundry-models/concepts/models-sold-directly-by-azure-region-availability.md)

## Updated articles

- Azure OpenAI
  - [What is provisioned throughput for Foundry Models?](openai/concepts/provisioned-throughput.md)
  - [Provisioned throughput billing and cost management](openai/concepts/provisioned-throughput-billing.md)
  - [Operate provisioned deployments in production](openai/how-to/provisioned-get-started.md)
  - [Manage traffic with spillover for provisioned deployments](openai/how-to/spillover-traffic-management.md)
  - [Latency and performance optimization](openai/how-to/latency.md)
  - [Monitor Azure OpenAI reference](openai/monitor-openai-reference.md)
  - [Priority processing for model deployments](openai/concepts/priority-processing.md)
  - [Quota management and rate limits](openai/how-to/quota.md)
  - [Model router for Microsoft Foundry concepts](openai/concepts/model-router.md)
  - [How to use model router for Microsoft Foundry](openai/how-to/model-router.md)
- Foundry Agent Service
  - [Connect to an A2A agent endpoint from Foundry Agent Service](agents/how-to/tools/agent-to-agent.md)
  - [Deploy a hosted agent](agents/how-to/deploy-hosted-agent.md)
  - [Hosted agents in Foundry Agent Service (preview)](agents/concepts/hosted-agents.md)
  - [Tool support by model and region](agents/concepts/tool-best-practice.md)
  - [Use skills with Microsoft Foundry agents (preview)](agents/how-to/tools/skills.md)
  - [Automate browser tasks with Foundry agents](agents/how-to/tools/browser-automation.md)
  - [Curate intent-based toolbox in Foundry (preview)](agents/how-to/tools/toolbox.md)
  - [What is Microsoft Foundry Agent Service?](agents/overview.md)
  - [Agent development lifecycle](agents/concepts/development-lifecycle.md)
  - [Quickstart: Deploy your first hosted agent](agents/quickstarts/quickstart-hosted-agent.md)
- Evaluations and observability
  - [Built-in Evaluators Reference](concepts/built-in-evaluators.md)
  - [Agent Evaluators for Generative AI](concepts/evaluation-evaluators/agent-evaluators.md)
  - [Custom Evaluators](concepts/evaluation-evaluators/custom-evaluators.md)
  - [General Purpose Evaluators for Generative AI](concepts/evaluation-evaluators/general-purpose-evaluators.md)
  - [Retrieval-Augmented Generation (RAG) Evaluators for Generative AI](concepts/evaluation-evaluators/rag-evaluators.md)
  - [Cloud Evaluation with the Microsoft Foundry SDK](how-to/develop/cloud-evaluation.md)
  - [Run evaluations from the Microsoft Foundry portal](how-to/evaluate-generative-ai-app.md)
- Foundry Models and platform
  - [Customer-managed key encryption](concepts/encryption-keys-portal.md)
  - [Foundry Models sold directly by Azure](foundry-models/concepts/models-sold-directly-by-azure.md)


