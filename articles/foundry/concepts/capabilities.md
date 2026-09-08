---
title: "Microsoft Foundry product and capability map"
description: "Find where to start in Microsoft Foundry. Match your goal to a starting point, then compare the major products and capabilities and who each one is for."
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: concept-article
ms.date: 08/12/2026
ai-usage: ai-assisted
# customer intent: As a developer or administrator new to Foundry, I want to match my goal to the right product or capability so that I know where to start.
---

# Microsoft Foundry product and capability map

Microsoft Foundry covers a wide range of features, and the hardest part is often knowing where to start. This article maps common goals to a starting point, then summarizes the major Foundry products and capabilities so you can tell them apart.

For an exhaustive list of everything in Foundry, see the [capability reference](capability-reference.md).

## Start with your goal

Find the row closest to what you're trying to do.

| I want to | Start here | Why |
|---|---|---|
| Send a prompt to a model, with no agent or tools | [Build with models and agents](../quickstarts/get-started-code.md) | The shortest path to a working call. Add an agent later only if you need tools or orchestration. |
| Build my first agent | [Choose how to build](../what-is-foundry.md#start-by-building-an-agent) | Decides prompt agent versus hosted agent before you invest in either. That choice shapes everything after it. |
| Host an agent I already wrote | [Deploy a hosted agent](../agents/quickstarts/quickstart-hosted-agent.md) | Runs your existing code or container with a managed endpoint, scaling, and identity. |
| Use an open-source framework with Foundry | [Frameworks for hosted agents](../how-to/develop/framework-hosted-agents.md) | Shows how LangGraph, Microsoft Agent Framework, and Semantic Kernel map onto Foundry hosting. |
| Evaluate agent quality | [Evaluate generative AI apps](../how-to/evaluate-generative-ai-app.md) | Establishes a baseline score first, so later changes are measurable rather than anecdotal. |
| Add observability | [Foundry Observability](observability.md) | Tracing, monitoring, and evaluation share one data model, so set them up together. |
| Deploy and operate an application | [Set up CI/CD for agents](../agents/quickstarts/set-up-cicd-hosted-agent.md) | Gets a repeatable release path before you scale. For fleet-wide governance, see the [control plane](../control-plane/overview.md). |

## Major products and capabilities

Each row names one decision-level entry point. The **When to use it** column states the fit first, then the boundary where another option is a better match.

| Product or capability | What it is | When to use it | Who it's for |
|---|---|---|---|
| [Foundry portal](general-availability.md) | Web experience for models, agents, evaluations, and resources. | Use to explore and prototype without writing code. If you need repeatable builds, move to the SDKs or CLI. | Anyone evaluating Foundry |
| [Prompt agents](../agents/quickstarts/prompt-agent.md) | Declarative agents defined by instructions, a model, and tools. | Use when you want an agent with no runtime to manage. If you need custom code or a container, use hosted agents instead. | Agent developer |
| [Hosted agents](../agents/concepts/hosted-agents.md) | Your own agent code or framework, run by Foundry. | Use when you need full control of agent logic and dependencies. If instructions and tools are enough, prompt agents are simpler. | Agent developer |
| [Foundry Models](foundry-models-overview.md) | Catalog of models from Microsoft, OpenAI, Anthropic, Meta, and others. | Use to choose and deploy the model behind your app or agent. If a model needs your domain data, consider fine-tuning. | Application developer |
| [Fine-tuning](../fine-tuning/fine-tune-cli.md) | Customization of a model on your own data. | Use when prompting and retrieval can't reach the quality you need. If the gap is missing context, use retrieval instead. | ML engineer |
| [Toolbox](../agents/concepts/toolbox-overview.md) | Managed endpoint that packages the tools an agent can call. | Use to give an agent actions and to govern tools centrally. If the agent only needs your own data, start with Foundry IQ. | Agent developer |
| [Foundry IQ](../agents/concepts/what-is-foundry-iq.md) | Agentic retrieval over a knowledge base. | Use to ground answers in your content. If you only need a few uploaded files, file search is lighter weight. | Agent developer |
| [Memory](../agents/concepts/what-is-memory.md) (preview) | Persistent agent recall across sessions. | Use when an agent must remember prior turns or user context. If each request stands alone, skip it. | Agent developer |
| [Workflows](../agents/concepts/workflow.md) | Orchestration of multiple agents and steps. | Use when one task spans several agents or stages. If a single agent with tools can finish the job, stay simpler. | Agent developer |
| [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md) | Client libraries for Python, C#, JavaScript, and Java. | Use to build Foundry into an application. If you're scaffolding and deploying agent projects, add the Azure Developer CLI. | Application developer |
| [Azure Developer CLI (azd)](../agents/concepts/cli-agent-development.md) | Command-line scaffolding, deployment, and environment management. | Use to create, run, and ship agent projects repeatably. If you only call models from an app, the SDKs are enough. | Platform engineer |
| [Visual Studio Code extension](../how-to/develop/get-started-projects-vs-code.md) | Foundry projects, models, and agents inside the editor. | Use to build and debug without leaving VS Code. If you want an AI assistant to drive Foundry, use coding agents. | Application developer |
| [Coding agents and MCP](../how-to/develop/use-microsoft-foundry-skill.md) | Model Context Protocol access to Foundry for coding agents. | Use to let GitHub Copilot or Claude Code work against Foundry. If you prefer direct authoring, use the VS Code extension. | Application developer |
| [LangChain and LangGraph](../how-to/develop/langchain.md) | Integration of Foundry models, tools, memory, and tracing. | Use when your team already builds on LangChain or LangGraph. If you're starting fresh, native agents need less glue code. | Agent developer |
| [Foundry Observability](observability.md) | Tracing, monitoring, and dashboards for agents and models. | Use to see what agents actually did in production. If you're comparing versions before release, start with evaluations. | AI quality engineer |
| [Evaluations](../how-to/evaluate-generative-ai-app.md) | Scoring for generative AI apps and agents. | Use to measure quality and catch regressions before release. If you need adversarial coverage, add AI red teaming. | AI quality engineer |
| [AI red teaming](ai-red-teaming-agent.md) | Automated adversarial scans against a model or agent. | Use to probe for unsafe or exploitable behavior. If you're measuring everyday quality, evaluations fit better. | Security administrator |
| [Guardrails and controls](../guardrails/guardrails-overview.md) | Content filters and safety controls for models and agents. | Use to enforce safety at run time. If you're testing safety before release, pair it with AI red teaming. | Security administrator |
| [Foundry control plane](../control-plane/overview.md) | Governance for agents, models, and tools across your estate. | Use to set limits, policy, and oversight across many projects. If you're governing a single project, project settings are enough. | Platform engineer |

## Related content

- [Microsoft Foundry capability reference](capability-reference.md)
- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Choose how to build with Microsoft Foundry](../what-is-foundry.md#start-by-building-an-agent)
- [Service architecture](architecture.md)
