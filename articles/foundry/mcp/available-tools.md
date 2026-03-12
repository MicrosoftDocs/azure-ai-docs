---
title:  "Explore available tools and example prompts for Foundry MCP Server (preview)" 
description: "Reference guide for all Foundry MCP Server tools, including dataset management, evaluation, model deployment, and monitoring, with example prompts for each tool."
keywords: mcp, model context protocol, foundry mcp server
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 03/12/2026
ms.topic: reference
ms.service: azure-ai-foundry
ai-usage: ai-assisted
---

# Available tools and example prompts for Foundry MCP Server (preview)
Foundry MCP Server exposes a set of tools that let you manage datasets, run evaluations, deploy and monitor models, and more — all through conversational prompts instead of API calls. Use this reference to explore each tool and try the example prompts in your own project.

> [!TIP]
> Before using these tools, complete the [Foundry MCP Server setup](get-started.md).

[!INCLUDE [preview-feature](../openai/includes/preview-feature.md)]

## Agent management

Manage the full lifecycle of agents in a Foundry project, including creation, invocation, container orchestration, and deletion.

Example prompts:

- "List all agents in my Foundry project."
- "Create a new agent named `faq-agent` using model `gpt-4o-mini`."
- "Send 'Hello, how can you help?' to my `customer-support-agent`."
- "Start the container for my hosted agent `triage-agent`."
- "Check the container status for `triage-agent`."
- "Show me the agent definition schema for prompt agents."
- "Delete the `old-test-agent` from my project."

| Tool | Access | Description |
| --- | --- | --- |
| `agent_get` | read | List all agents in a Foundry project, or get a specific agent by name. |
| `agent_update` | write | Create, update, or clone an agent. Use `agent_definition_schema_get` to discover the full definition schema first. |
| `agent_invoke` | write | Send a message to an agent and get a response. Works for both prompt-based and hosted container agents. |
| `agent_delete` | write | Permanently delete an agent. For hosted agents, this also deletes the container. |
| `agent_container_control` | write | Start or stop a hosted agent container. Use before invoking a hosted agent. |
| `agent_container_status_get` | read | Check the current status of a hosted agent container (Starting, Running, Stopped, Failed, and so on). |
| `agent_definition_schema_get` | read | Return the complete JSON schema for agent definitions, including all tool types. |

## Dataset management

Create, retrieve, and version evaluation datasets in a Foundry project.

Example prompts:

- "Upload my customer support Q&A dataset from this Azure Blob Storage URL."
- "Show me all datasets in my Foundry project."
- "Get details for the `customer-support-qa` dataset version 2."
- "List all versions of my `product-reviews` dataset."

| Tool | Access | Description |
| --- | --- | --- |
| `evaluation_dataset_create` | write | Create or update a dataset version from an Azure Blob Storage URI. |
| `evaluation_dataset_get` | read | Get a dataset by name and version, or list all datasets in the project. |
| `evaluation_dataset_versions_get` | read | List all versions of a specific dataset. |

## Evaluation operations

Run batch evaluations against agents or datasets, and compare results across runs.

Example prompts:

- "Evaluate my `customer-support-agent` v2 using Relevance, Groundedness, and Coherence evaluators."
- "Run a batch evaluation on my JSONL dataset with Violence and HateUnfairness evaluators."
- "Generate 50 synthetic test queries and evaluate my agent with them."
- "Show me all evaluation runs in my Foundry project."
- "Compare run-baseline-123 against treatment runs run-124 and run-125."

| Tool | Access | Description |
| --- | --- | --- |
| `evaluation_agent_batch_eval_create` | write | Create a batch evaluation run that calls a specific agent. Supports built-in and custom evaluators, plus synthetic data generation. |
| `evaluation_dataset_batch_eval_create` | write | Create a batch evaluation run against a JSONL dataset. Supports built-in and custom evaluators. |
| `evaluation_get` | read | List evaluation runs in the Foundry project. |
| `evaluation_comparison_create` | write | Create comparison results between a baseline and treatment evaluation runs. |
| `evaluation_comparison_get` | read | Get or list evaluation comparison insights. |

## Evaluator catalog

Browse built-in evaluators and manage custom evaluators for use in evaluation runs.

Example prompts:

- "List all built-in evaluators available in my project."
- "Show me the full definition of the `coherence` evaluator."
- "Create a custom prompt-based evaluator called `tone-check` that scores responses on a 1-5 scale."
- "Update the description of my `tone-check` evaluator."
- "Delete version 1 of my `old-evaluator`."

| Tool | Access | Description |
| --- | --- | --- |
| `evaluator_catalog_get` | read | List evaluators in the catalog, or get the full definition of a specific evaluator. Filter by built-in or custom type. |
| `evaluator_catalog_create` | write | Create a custom prompt-based or code-based evaluator. |
| `evaluator_catalog_update` | write | Update metadata (display name, description, category) for an existing custom evaluator. |
| `evaluator_catalog_delete` | write | Delete a specific version of a custom evaluator. |

## Model catalog and details

Explore and get details about models in the Foundry model catalog.

Example prompts:

- "Show me all GPT-4 models available in the catalog."
- "List all Microsoft-published models with MIT license."
- "Get detailed information and code samples for GPT-4o-mini."

| Tool | Access | Description |
| --- | --- | --- |
| `model_catalog_list` | read | List models from the Foundry model catalog with optional filters (publisher, license, task). |
| `model_details_get` | read | Get full model details and code samples. |

## Model deployment management

Deploy, inspect, and remove model deployments in a Foundry account.

Example prompts:

- "Deploy GPT-4o-mini as `production-chatbot` with 20 capacity units."
- "Show me all my current model deployments."
- "Delete the `old-test-deployment` that I'm no longer using."

| Tool | Access | Description |
| --- | --- | --- |
| `model_deploy` | write | Create or update a model deployment with specified capacity. |
| `model_deployment_get` | read | Get one or more model deployments from a Foundry account. |
| `model_deployment_delete` | write | Delete a specific model deployment by name. |

## Model analytics and recommendations

Compare model benchmarks and get recommendations for switching to more cost-effective or higher-quality models.

Example prompts:

- "Show me benchmark data for all available models."
- "Compare benchmark performance between GPT-4 and GPT-3.5-turbo."
- "Find models similar to my current GPT-4 deployment."
- "What models would give me better quality/cost ratio than what I'm using now?"

| Tool | Access | Description |
| --- | --- | --- |
| `model_benchmark_get` | read | Fetch benchmark data for Foundry models. |
| `model_benchmark_subset_get` | read | Get benchmark data for specific model name and version pairs. |
| `model_similar_models_get` | read | Find similar models based on deployment or model details. |
| `model_switch_recommendations_get` | read | Get model switch recommendations based on benchmark data. |

## Model monitoring and operations

Track deployment health, monitor metrics, check deprecation status, and view quota usage.

Example prompts:

- "Show me the request metrics for my `production-chatbot` deployment."
- "Check if any of my deployments are using deprecated model versions."
- "Show me quota usage across all regions for my subscription."

| Tool | Access | Description |
| --- | --- | --- |
| `model_monitoring_metrics_get` | read | Get monitoring metrics (requests, latency, errors, quota) for a model deployment. |
| `model_deprecation_info_get` | read | Get deployment info enriched with deprecation and retirement schedules. |
| `model_quota_list` | read | List available deployment quota and usage for a subscription in a region. |

## Project connections

Manage connections to external services (Azure OpenAI, Azure Blob Storage, search, and others) within a Foundry project.

Example prompts:

- "List all connections in my Foundry project."
- "Show me the details for my `azure-search` connection."
- "What connection types and authentication methods are supported?"
- "Create a new AzureOpenAI connection called `my-openai` using AAD auth."
- "Delete the `old-storage` connection from my project."

| Tool | Access | Description |
| --- | --- | --- |
| `project_connection_list` | read | List all connections in a Foundry project, with optional filtering by category or target. |
| `project_connection_get` | read | Get a specific connection by name. |
| `project_connection_list_metadata` | read | List all supported connection categories and authentication types. Call this first to discover valid values. |
| `project_connection_create` | write | Create or replace a project connection. |
| `project_connection_update` | write | Update an existing project connection. |
| `project_connection_delete` | write | Delete a project connection by name. |

## Prompt optimization

Optimize system prompts and developer messages for better LLM performance.

Example prompts:

- "Optimize my system prompt: 'You are a helpful customer service agent' using `gpt-4o`."
- "Improve my agent instructions to get more concise responses."
- "Refine my optimized prompt to also handle follow-up questions."

| Tool | Access | Description |
| --- | --- | --- |
| `prompt_optimize` | write | Optimize a developer prompt (system message) for better LLM performance using the Azure OpenAI Prompt Optimizer. |

## Example workflows

**Agent evaluation workflow:**

1. "List all agents in my project."
1. "Evaluate my `customer-support-agent` v2 using Relevance, Groundedness, and Safety evaluators."
1. "Compare my baseline evaluation against the new run."
1. "Show me the comparison results with statistical significance."

**Model deployment and optimization:**

1. "Show me all GPT-4 models available in the catalog."
1. "Deploy GPT-4o as `customer-service-bot` with 15 capacity units."
1. "Monitor the request latency for my new deployment."
1. "Recommend more cost-effective alternatives based on current usage."

**Resource management and cleanup:**

1. "List all my current deployments and their usage."
1. "Check which deployments are using deprecated model versions."
1. "Show me my quota usage across all regions."
1. "Delete unused test deployments to free up capacity."

## Related content

- Get started with [Foundry MCP Server](get-started.md)
- Learn how to [build your own MCP server](build-your-own-mcp-server.md)
- Review [security best practices for MCP servers](security-best-practices.md)
