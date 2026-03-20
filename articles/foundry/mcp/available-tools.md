---
title:  "Explore available tools and example prompts for Foundry MCP Server (preview)" 
description: "Reference guide for all Foundry MCP Server tools, including tool descriptions, key inputs, permissions, and example prompts for each tool."
keywords: mcp, model context protocol, foundry mcp server
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 03/12/2026
ms.topic: reference
ms.service: azure-ai-foundry
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
---

# Available tools and example prompts for Foundry MCP Server (preview)

Foundry MCP Server exposes 38 tools across 10 categories that let you manage agents, datasets, evaluations, model deployments, and more — all through conversational prompts instead of API calls. Use this reference to explore each tool and try the example prompts in your own project.

> [!TIP]
> Before using these tools, complete the [Foundry MCP Server setup](get-started.md).

[!INCLUDE [preview-feature](../openai/includes/preview-feature.md)]

## How tools work

When you type a natural-language prompt in an MCP-compliant client (for example, GitHub Copilot Agent Mode), the language model selects the appropriate tool and formulates the required parameters on your behalf. You don't call tools directly — you describe what you want, and the model translates your intent into a tool call.

Each tool is classified as **read** (retrieves information) or **write** (creates, updates, or deletes resources). Write operations affect live resources and billing immediately. Review the [security best practices](security-best-practices.md) before running write operations.

### Permissions

All operations run with the authenticated user's permissions through the Microsoft Entra ID On-Behalf-Of flow. You need the following roles:

| Operation type | Minimum Azure role | Notes |
| --- | --- | --- |
| Read tools | **Reader** on the Foundry project or account | Sufficient for listing, querying, and monitoring. |
| Write tools | **Contributor** on the Foundry project or account | Required for creating, updating, and deleting resources. |
| Conditional Access admin | **Conditional Access Administrator** in Entra ID | Only needed if configuring tenant-level access policies. |

For more information, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

### Key identifiers

Many tools require resource identifiers. The language model extracts these from your prompt context, but it helps to know the formats:

| Identifier | Format | Where to find it |
| --- | --- | --- |
| Foundry resource ID | `/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}` | Azure portal **Properties** page |
| Project endpoint | `https://{account}.services.ai.azure.com/api/projects/{project}` | Foundry project details page |
| Project resource ID | `/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}` | Azure portal **Properties** page |

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

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `agent_get` | read | List all agents in a Foundry project, or get a specific agent by name. | Agent name (optional) | Agent list or single agent definition with model, instructions, and tool configuration. |
| `agent_update` | write | Create, update, or clone an agent. Use `agent_definition_schema_get` to discover the full definition schema first. | Agent name, model, instructions, tool definitions | Created or updated agent definition. |
| `agent_invoke` | write | Send a message to an agent and get a response. Works for both prompt-based and hosted container agents. | Agent name, message text | Agent response message. |
| `agent_delete` | write | Permanently delete an agent. For hosted agents, this also deletes the container. | Agent name | Deletion confirmation. |
| `agent_container_control` | write | Start or stop a hosted agent container. Use before invoking a hosted agent. | Agent name, action (start or stop) | Container operation status. |
| `agent_container_status_get` | read | Check the current status of a hosted agent container (Starting, Running, Stopped, Failed, and so on). | Agent name | Current container status. |
| `agent_definition_schema_get` | read | Return the complete JSON schema for agent definitions, including all tool types. | None | Full JSON schema for agent definitions. |

## Dataset management

Create, retrieve, and version evaluation datasets in a Foundry project.

Example prompts:

- "Upload my customer support Q&A dataset from this Azure Blob Storage URL."
- "Show me all datasets in my Foundry project."
- "Get details for the `customer-support-qa` dataset version 2."
- "List all versions of my `product-reviews` dataset."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `evaluation_dataset_create` | write | Create or update a dataset version from an Azure Blob Storage URI. | Dataset name, version, Blob Storage URI | Dataset metadata with name, version, and URI. |
| `evaluation_dataset_get` | read | Get a dataset by name and version, or list all datasets in the project. | Dataset name and version (optional) | Dataset details or list of all datasets. |
| `evaluation_dataset_versions_get` | read | List all versions of a specific dataset. | Dataset name | List of version numbers with metadata. |

## Evaluation operations

Run batch evaluations against agents or datasets, and compare results across runs.

Example prompts:

- "Evaluate my `customer-support-agent` v2 using Relevance, Groundedness, and Coherence evaluators."
- "Run a batch evaluation on my JSONL dataset with Violence and HateUnfairness evaluators."
- "Generate 50 synthetic test queries and evaluate my agent with them."
- "Show me all evaluation runs in my Foundry project."
- "Compare run-baseline-123 against treatment runs run-124 and run-125."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `evaluation_agent_batch_eval_create` | write | Create a batch evaluation run that calls a specific agent. Supports built-in and custom evaluators, plus synthetic data generation. | Agent name/version, evaluator names, dataset (optional for synthetic generation), number of synthetic queries (optional) | Evaluation run ID and status. |
| `evaluation_dataset_batch_eval_create` | write | Create a batch evaluation run against a JSONL dataset. Supports built-in and custom evaluators. | Dataset name/version, evaluator names | Evaluation run ID and status. |
| `evaluation_get` | read | List evaluation runs in the Foundry project. | Evaluation run ID (optional) | List of evaluation runs with status and scores, or details for a specific run. |
| `evaluation_comparison_create` | write | Create comparison results between a baseline and treatment evaluation runs. | Baseline run ID, treatment run IDs | Comparison insight ID. |
| `evaluation_comparison_get` | read | Get or list evaluation comparison insights. | Comparison insight ID (optional) | Comparison results with statistical analysis. |

## Evaluator catalog

Browse built-in evaluators and manage custom evaluators for use in evaluation runs.

Example prompts:

- "List all built-in evaluators available in my project."
- "Show me the full definition of the `coherence` evaluator."
- "Create a custom prompt-based evaluator called `tone-check` that scores responses on a 1-5 scale."
- "Update the description of my `tone-check` evaluator."
- "Delete version 1 of my `old-evaluator`."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `evaluator_catalog_get` | read | List evaluators in the catalog, or get the full definition of a specific evaluator. Filter by built-in or custom type. | Evaluator name (optional), type filter (built-in or custom, optional) | Evaluator list or full evaluator definition with scoring logic. |
| `evaluator_catalog_create` | write | Create a custom prompt-based or code-based evaluator. | Evaluator name, type (prompt or code), definition | Created evaluator metadata. |
| `evaluator_catalog_update` | write | Update metadata (display name, description, category) for an existing custom evaluator. | Evaluator name, fields to update | Updated evaluator metadata. |
| `evaluator_catalog_delete` | write | Delete a specific version of a custom evaluator. | Evaluator name, version | Deletion confirmation. |

## Model catalog and details

Explore and get details about models in the Foundry model catalog.

Example prompts:

- "Show me all GPT-5.4 models available in the catalog."
- "List all Microsoft-published models with MIT license."
- "Get detailed information and code samples for GPT-5-mini."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `model_catalog_list` | read | List models from the Foundry model catalog with optional filters (publisher, license, task). | Search keywords, publisher, license type, task type (all optional) | List of models with name, publisher, license, and capabilities. |
| `model_details_get` | read | Get full model details and code samples. | Model name or ID | Model specifications, pricing, supported regions, and code samples. |

## Model deployment management

Deploy, inspect, and remove model deployments in a Foundry account.

Example prompts:

- "Deploy GPT-5-mini as `production-chatbot` with 20 capacity units."
- "Show me all my current model deployments."
- "Delete the `old-test-deployment` that I'm no longer using."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `model_deploy` | write | Create or update a model deployment with specified capacity. | Model name, deployment name, capacity units | Deployment details with endpoint and provisioned capacity. |
| `model_deployment_get` | read | Get one or more model deployments from a Foundry account. | Deployment name (optional) | List of deployments or single deployment details with status and quota. |
| `model_deployment_delete` | write | Delete a specific model deployment by name. | Deployment name | Deletion confirmation. |

## Model analytics and recommendations

Compare model benchmarks and get recommendations for switching to more cost-effective or higher-quality models.

Example prompts:

- "Show me benchmark data for all available models."
- "Compare benchmark performance between GPT-5.4 and GPT-4."
- "Find models similar to my current GPT-4 deployment."
- "What models would give me better quality/cost ratio than what I'm using now?"

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `model_benchmark_get` | read | Fetch benchmark data for Foundry models. | Model filters (optional) | Benchmark scores, accuracy, cost, and latency metrics. |
| `model_benchmark_subset_get` | read | Get benchmark data for specific model name and version pairs. | Model name and version pairs | Benchmark comparison data for specified models. |
| `model_similar_models_get` | read | Find similar models based on deployment or model details. | Deployment name or model name | List of similar models with capability comparison. |
| `model_switch_recommendations_get` | read | Get model switch recommendations based on benchmark data. | Current deployment name | Recommended models with quality/cost trade-off analysis. |

## Model monitoring and operations

Track deployment health, monitor metrics, check deprecation status, and view quota usage.

Example prompts:

- "Show me the request metrics for my `production-chatbot` deployment."
- "Check if any of my deployments are using deprecated model versions."
- "Show me quota usage across all regions for my subscription."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `model_monitoring_metrics_get` | read | Get monitoring metrics (requests, latency, errors, quota) for a model deployment. | Deployment name, time range (optional) | Request count, latency percentiles, error rates, and token usage. |
| `model_deprecation_info_get` | read | Get deployment info enriched with deprecation and retirement schedules. | Deployment name (optional) | Deployment details with deprecation dates and suggested replacements. |
| `model_quota_list` | read | List available deployment quota and usage for a subscription in a region. | Region (optional) | Quota limits, current usage, and available capacity per model family. |

## Project connections

Manage connections to external services (Azure OpenAI, Azure Blob Storage, search, and others) within a Foundry project.

Example prompts:

- "List all connections in my Foundry project."
- "Show me the details for my `azure-search` connection."
- "What connection types and authentication methods are supported?"
- "Create a new AzureOpenAI connection called `my-openai` using AAD auth."
- "Delete the `old-storage` connection from my project."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `project_connection_list` | read | List all connections in a Foundry project, with optional filtering by category or target. | Category filter, target filter (both optional) | List of connections with name, type, and status. |
| `project_connection_get` | read | Get a specific connection by name. | Connection name | Connection details including category, target, and auth type. |
| `project_connection_list_metadata` | read | List all supported connection categories and authentication types. Call this first to discover valid values. | None | Supported categories (for example, AzureOpenAI, AzureBlobStorage) and auth types (for example, AAD, key). |
| `project_connection_create` | write | Create or replace a project connection. | Connection name, category, target, auth type | Created connection details. |
| `project_connection_update` | write | Update an existing project connection. | Connection name, fields to update | Updated connection details. |
| `project_connection_delete` | write | Delete a project connection by name. | Connection name | Deletion confirmation. |

## Prompt optimization

Optimize system prompts and developer messages for better LLM performance.

Example prompts:

- "Optimize my system prompt: 'You are a helpful customer service agent' using `gpt-5.4`."
- "Improve my agent instructions to get more concise responses."
- "Refine my optimized prompt to also handle follow-up questions."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `prompt_optimize` | write | Optimize a developer prompt (system message) for better LLM performance using the Azure OpenAI Prompt Optimizer. | Prompt text, target model, refinement instructions (optional) | Optimized prompt text with explanation of changes. |

## Example workflows

**Agent evaluation workflow:**

1. "List all agents in my project."
1. "Evaluate my `customer-support-agent` v2 using Relevance, Groundedness, and Safety evaluators."
1. "Compare my baseline evaluation against the new run."
1. "Show me the comparison results with statistical significance."

**Model deployment and optimization:**

1. "Show me all GPT-5.4 models available in the catalog."
1. "Deploy GPT-5.4 as `customer-service-bot` with 15 capacity units."
1. "Monitor the request latency for my new deployment."
1. "Recommend more cost-effective alternatives based on current usage."

**Resource management and cleanup:**

1. "List all my current deployments and their usage."
1. "Check which deployments are using deprecated model versions."
1. "Show me my quota usage across all regions."
1. "Delete unused test deployments to free up capacity."

## Preview limitations

Foundry MCP Server is in public preview. The following limitations apply:

- **No network isolation** — The server uses the public endpoint `https://mcp.ai.azure.com`. Resources behind Azure Private Links aren't accessible.
- **Data residency** — Requests and responses might be processed in EU or US data centers. The server itself doesn't store data, but cross-region processing can occur.
- **No SLA** — Preview features don't include a service-level agreement. Don't use the server for production workloads that require guaranteed availability.
- **Tool set might change** — Tools, parameters, and return values might change during the preview period without notice.

For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Common errors

| Error | Cause | Resolution |
| --- | --- | --- |
| Access denied | Insufficient Azure RBAC role on the Foundry project or account. | Assign at least **Reader** for read tools or **Contributor** for write tools. See [RBAC for Microsoft Foundry](../concepts/rbac-foundry.md). |
| Authentication failure | Expired or invalid Entra ID token. | Sign out and sign back in to your Azure account in Visual Studio Code, or the tool you're using. |
| Quota exceeded | Not enough capacity to create a deployment or run an evaluation. | Use `model_quota_list` to check available quota before the operation. |
| Resource not found | The specified deployment, dataset, agent, or connection doesn't exist. | Use the corresponding `get` or `list` tool to verify the resource name. |
| Private endpoint not reachable | Foundry resources use Azure Private Links that the server can't reach. | Remove private endpoint restrictions or use SDKs/REST APIs instead. |

For more troubleshooting guidance, see [Foundry MCP Server security and best practices](security-best-practices.md#troubleshooting).

## Related content

- Get started with [Foundry MCP Server](get-started.md)
- Learn how to [build your own MCP server](build-your-own-mcp-server.md)
- Review [security best practices for MCP servers](security-best-practices.md)
