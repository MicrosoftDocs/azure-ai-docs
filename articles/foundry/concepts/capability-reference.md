---
title: "Microsoft Foundry capability reference"
description: "Reference list of Microsoft Foundry capabilities by area, including models, agents, tools, knowledge, observability, evaluation, guardrails, and governance."
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: reference
ms.date: 08/12/2026
ai-usage: ai-assisted
# customer intent: As a developer or administrator, I want an exhaustive list of Foundry capabilities by area so that I can find the canonical documentation for a specific capability.
---

# Microsoft Foundry capability reference

This article lists Microsoft Foundry capabilities by area and links each one to its canonical documentation. Use it when you know roughly what you need and want to find the right article.

If you're deciding where to start instead, see [Microsoft Foundry product and capability map](capabilities.md).

Each entry is a capability family rather than an individual article, model, or API operation. Capabilities marked (preview) are offered under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) and aren't recommended for production workloads. Preview status can vary by feature, region, and API version, so check the linked article for current details.

## Build surfaces and developer tools

Where you author, test, and ship Foundry work.

| Capability | What it does |
|---|---|
| [Foundry portal](general-availability.md) | Web experience for exploring models, building prompt agents, running evaluations, and managing resources. |
| [Playgrounds](concept-playgrounds.md) | Try models, prompts, and agents interactively before you write code. |
| [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md) | Client libraries for Python, C#, JavaScript, and Java. |
| [Azure Developer CLI (azd) extensions](../agents/concepts/cli-agent-development.md) | Scaffold, run, test, and deploy agent projects from the command line. |
| [Visual Studio Code extension](../how-to/develop/get-started-projects-vs-code.md) | Work with Foundry projects, models, and agents inside VS Code. |
| [Foundry Agent Canvas](../agents/concepts/foundry-agent-canvas.md) | Visual surface for composing and inspecting agents. |
| [Coding agent integration](../agents/how-to/use-cli-with-coding-agents.md) | Build Foundry projects with AI coding agents such as GitHub Copilot, including Model Context Protocol access through the Foundry MCP Server. |
| [Templates and samples](../how-to/develop/ai-template-get-started.md) | Start from prebuilt application templates and GitHub samples. |
| [LangChain and LangGraph integration](../how-to/develop/langchain.md) | Use Foundry models, tools, memory, and tracing from LangChain and LangGraph apps. |

## Models

Model selection, deployment, and lifecycle.

| Capability | What it does |
|---|---|
| [Foundry Models catalog](foundry-models-overview.md) | Discover and compare models from Microsoft, OpenAI, Anthropic, Meta, and others, across models sold by Azure and models from partners and community. |
| [Model deployment](../foundry-models/how-to/create-model-deployments.md) | Create and manage model endpoints from the portal or code. |
| [Deployment types](../foundry-models/concepts/deployment-types.md) | Choose how capacity is served, including standard, global, data zone, provisioned throughput (PTU), batch, and priority processing. |
| [Managed compute](managed-compute-overview.md) (preview) | Deploy models to dedicated virtual machine capacity in your resource. |
| [Instant access models](instant-models.md) (preview) | Use selected models without provisioning a deployment first. |
| [Model router](../openai/concepts/model-router.md) | Route requests automatically to the best model for cost and quality. |
| [Model benchmarks and leaderboards](model-benchmarks.md) | Compare model quality, cost, and performance before you commit. |
| [Fine-tuning](../fine-tuning/fine-tune-cli.md) | Customize models on your own data, including synthetic data generation. |
| [Model versions and lifecycle](../foundry-models/concepts/model-versions.md) | Track versions, automatic updates, retirement schedules, and support policy. |
| [Healthcare AI models](../how-to/healthcare-ai/healthcare-ai-models.md) | Domain-specific models for medical imaging and reporting scenarios. |
| [Hugging Face models](../foundry-models/how-to/hugging-face-models.md) | Deploy open models from Hugging Face into Foundry. |
| [Fireworks on Foundry](../how-to/fireworks/enable-fireworks-models.md) | Use Fireworks models and import custom models. |
| [Quotas and region availability](../foundry-models/quotas-limits.md) | Understand and manage capacity limits by model and region. |

## Agents

Foundry Agent Service and the agent development lifecycle.

| Capability | What it does |
|---|---|
| [Foundry Agent Service](../agents/overview.md) | Build, run, and operate agents as a managed service. |
| [Prompt agents](../agents/quickstarts/prompt-agent.md) | Declarative agents defined by instructions, a model, and attached tools. |
| [Hosted agents](../agents/concepts/hosted-agents.md) | Run your own agent code or framework in a Foundry-managed runtime. |
| [Agent development lifecycle](../agents/concepts/development-lifecycle.md) | End-to-end build, test, deploy, and iterate workflow for agents. |
| [Agent identity](../agents/concepts/agent-identity.md) | Give agents a Microsoft Entra identity for authenticated access to resources. |
| [Workflows](../agents/concepts/workflow.md) | Coordinate multiple agents and steps into a single orchestrated process. |
| [Routines](../agents/concepts/routines.md) (preview) | Package repeatable agent procedures for reuse. |
| [Agent-to-agent (A2A)](../agents/how-to/tools/agent-to-agent.md) | Let agents call other agents across services and vendors. |
| [Responses API](../agents/quickstarts/responses-api.md) | Stateful API for model and agent interactions. |
| [Voice agents](../agents/how-to/build-voice-agent.md) | Add speech input and output to agents. |
| [Microsoft Agent 365 integration](../agents/concepts/agent-365-integration.md) | Manage and observe Foundry agents alongside Microsoft 365 agents. |
| [Continuous integration and deployment](../agents/quickstarts/set-up-cicd-hosted-agent.md) | Ship agents through automated pipelines. |
| [Agent debugging tools](../agents/how-to/agent-inspector.md) | Inspect and diagnose agent behavior locally and in the cloud. |

## Tools

Capabilities you attach to an agent so it can act.

| Capability | What it does |
|---|---|
| [Tool catalog](../agents/concepts/tool-catalog.md) | Browse every tool an agent can use, with setup requirements. |
| [Function calling](../agents/how-to/tools/function-calling.md) | Let an agent call your own functions with structured arguments. |
| [Code interpreter](../agents/how-to/tools/code-interpreter.md) | Run generated code in a sandbox to analyze data and produce files. |
| [File search](../agents/how-to/tools/file-search.md) | Ground answers in uploaded files through managed vector stores. |
| [Web search and Grounding with Bing](../agents/how-to/tools/web-overview.md) | Ground answers in current web results. |
| [Browser automation](../agents/how-to/tools/browser-automation.md) (preview) | Let an agent navigate and act on websites. |
| [Computer use](../agents/how-to/tools/computer-use.md) (preview) | Let an agent operate a virtual computer interface. |
| [Image generation](../agents/how-to/tools/image-generation.md) (preview) | Generate images from an agent. |
| [OpenAPI tool](../agents/how-to/tools/openapi.md) | Call any REST API described by an OpenAPI specification. |
| [Model Context Protocol (MCP)](../agents/how-to/tools/model-context-protocol.md) | Connect agents to MCP servers, including managed servers and your own. |
| [Azure Functions](../agents/how-to/tools/azure-functions.md) | Trigger serverless functions as agent actions. |
| [SharePoint and Fabric connectors](../agents/how-to/tools/connectors.md) (preview) | Reach enterprise data sources from an agent. |
| [Toolbox](../agents/concepts/toolbox-overview.md) | Bundle and manage the tools available to an agent, including tool search for large tool sets and a private catalog of organization-approved tools. |
| [Skills](../agents/how-to/tools/skills.md) (preview) | Package reusable agent behavior beyond a single tool call. |
| [Foundry Tools: Speech, Language, Translator](../agents/how-to/tools/azure-ai-speech.md) | Add speech, language understanding, PII detection, and translation. |

## Knowledge and retrieval

How agents and applications ground responses in your data.

| Capability | What it does |
|---|---|
| [Retrieval-augmented generation (RAG)](retrieval-augmented-generation.md) | Patterns for grounding model responses in your own content. |
| [Azure AI Search integration](../agents/how-to/tools/ai-search.md) | Use Azure AI Search indexes as agent knowledge. |
| [Vector stores](../agents/concepts/vector-stores.md) | Managed storage and indexing for file search. |
| [Foundry IQ](../agents/concepts/what-is-foundry-iq.md) | Agentic retrieval over a knowledge base, including private networking. |
| [Fabric IQ](../agents/how-to/tools/fabric-iq.md) (preview) | Reason over Microsoft Fabric data and semantic models. |
| [Work IQ](../agents/how-to/tools/work-iq.md) (preview) | Reason over Microsoft 365 work data. |
| [Memory](../agents/concepts/what-is-memory.md) (preview) | Give agents persistent memory across sessions. |

## Observability

Understand what your agents and models are doing in production.

| Capability | What it does |
|---|---|
| [Foundry Observability](observability.md) | Unified monitoring, tracing, and evaluation for agents and models. |
| [Tracing](../observability/concepts/trace-agent-concept.md) | Capture and replay agent execution traces, including client-side spans. |
| [Agent monitoring dashboard](../observability/how-to/how-to-monitor-agents-dashboard.md) | Track agent health, usage, quality, and cost over time. |
| [Model deployment monitoring](../foundry-models/how-to/monitor-models.md) | Watch latency, throughput, and errors for model endpoints. |
| [End-user feedback logging](../observability/how-to/log-end-user-feedback.md) | Collect and analyze feedback signals from your application. |
| [Notification Center](concept-notification-center.md) | See service and resource notifications in the portal. |
| [External agent registration](../agents/how-to/register-external-agent.md) (preview) | Bring agents that run outside Foundry into Foundry observability. |
| [Diagnostic logging](../how-to/diagnostic-logging.md) | Send platform logs and metrics to Azure Monitor. |

## Evaluation and optimization

Measure and improve quality, safety, and cost.

| Capability | What it does |
|---|---|
| [Evaluations](../how-to/evaluate-generative-ai-app.md) | Score generative AI apps and agents from the portal, SDK, or CI/CD. |
| [Built-in evaluators](built-in-evaluators.md) | Use general purpose, similarity, RAG, agent, safety, and rubric evaluators. |
| [Custom evaluators](evaluation-evaluators/custom-evaluators.md) | Define your own scoring logic. |
| [Agent evaluation](../observability/how-to/evaluate-agent.md) | Evaluate agent trajectories, tool calls, and task completion. |
| [Continuous evaluation](../observability/how-to/cloud-evaluation.md) | Evaluate production traffic on an ongoing basis. |
| [Evaluation datasets](../observability/how-to/evaluation-dataset-synthetic.md) | Generate synthetic test data or build datasets from agent traces when you don't have labeled examples. |
| [Human evaluation](../observability/how-to/human-evaluation.md) | Collect structured human judgments and annotate traces. |
| [Prompt optimizer](../observability/how-to/prompt-optimizer.md) | Improve agent instructions automatically from evaluation results. |
| [Agent optimizer](../agents/concepts/agent-optimizer-overview.md) (preview) | Tune hosted agent instructions and skills against a target dataset. |
| [AI red teaming](ai-red-teaming-agent.md) | Run automated adversarial scans locally or in the cloud. |
| [Evaluations in CI/CD](../how-to/evaluation-github-action.md) | Gate releases with evaluations in GitHub Actions or Azure DevOps. |

## Trust and safety

Guardrails, content safety, and responsible AI.

| Capability | What it does |
|---|---|
| [Guardrails and controls](../guardrails/guardrails-overview.md) | Filter and control content across models and agents. Includes harm category filters, Prompt Shields for jailbreak and prompt injection, groundedness detection, sensitive data (PII) detection, and protected material detection. |
| [Custom filtering](../guardrails/how-to-create-guardrails.md) | Extend the built-in filters with your own block lists and custom categories. |
| [Task adherence](../guardrails/task-adherence.md) | Detect when an agent strays from its assigned task. |
| [Guided Guardrail](../guardrails/guided-set-up.md) (preview) | Configure guardrails through a guided setup experience. |
| [Third-party guardrail integrations](../guardrails/third-party-integrations.md) | Plug partner safety systems into Foundry intervention points. |
| [Responsible AI transparency notes](../responsible-ai/agents/transparency-note.md) | Understand intended uses, limitations, and data handling. |
| [Customer Copyright Commitment](../responsible-ai/openai/customer-copyright-commitment.md) | Review Microsoft's copyright commitment for covered services. |

## Manage, secure, and govern

Platform administration for Foundry at scale.

| Capability | What it does |
|---|---|
| [Foundry resources and projects](../how-to/create-projects.md) | Organize work with Foundry resources and projects. |
| [Foundry control plane](../control-plane/overview.md) | Govern agents, models, and tools across your estate. |
| [Fleet monitoring](../control-plane/monitoring-across-fleet.md) | Track health and performance across many agents. |
| [Token limit enforcement](../control-plane/how-to-enforce-limits-models.md) | Cap model consumption per agent, project, or team. |
| [AI gateway integration](../agents/how-to/ai-gateway.md) | Front Foundry with Azure API Management for routing and policy. |
| [Role-based access control](rbac-foundry.md) | Assign Foundry roles and scope permissions. |
| [Keyless authentication](../foundry-models/how-to/configure-entra-id.md) | Use Microsoft Entra identities instead of API keys. |
| [Network isolation](../agents/concepts/networking-options.md) | Use private endpoints, managed virtual networks, and network security perimeter. |
| [Customer-managed keys](encryption-keys-portal.md) | Encrypt data with keys you control. |
| [Azure Policy support](../how-to/model-deployment-policy.md) | Apply built-in and custom policy definitions to Foundry resources. |
| [Cost management](manage-costs.md) | Plan, monitor, and optimize Foundry spend. |
| [High availability and disaster recovery](../how-to/high-availability-resiliency.md) | Design for resiliency and recover from outages or data loss. |
| [Azure Government support](foundry-azure-government.md) | Run Foundry workloads in Azure Government. |
| [Infrastructure as code](../how-to/create-resource-template.md) | Deploy Foundry with Bicep, Terraform, or the Azure CLI. |

## APIs and SDKs

Programmatic surfaces for building on Foundry.

| Capability | What it does |
|---|---|
| [Foundry API reference](https://ai.azure.com/api-reference/) | Browse the interactive reference for Foundry data plane operations. |
| [Foundry Models endpoints](../foundry-models/concepts/endpoints.md) | Call deployed models over a consistent inference endpoint. |
| [Foundry v1 REST API](/rest/api/microsoft-foundry/?view=rest-microsoft-foundry-v1&preserve-view=true) | Use the OpenAI-compatible surface for chat, responses, embeddings, files, and fine-tuning. |
| [Resource management API](/azure/templates/microsoft.cognitiveservices/accounts?pivots=deployment-language-bicep) | Create and configure Foundry resources with ARM, Bicep, or the Azure CLI. |

## Related content

- [Microsoft Foundry product and capability map](capabilities.md)
- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Choose how to build with Microsoft Foundry](../what-is-foundry.md#start-by-building-an-agent)
