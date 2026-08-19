---
title:  "Explore available tools and example prompts for Foundry MCP Server (preview)" 
description: "Reference guide for all Foundry MCP Server tools, including tool descriptions, key inputs, permissions, and example prompts for each tool."
keywords: mcp, model context protocol, foundry mcp server
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 08/18/2026
ms.topic: reference
ms.service: microsoft-foundry
ms.subservice: foundry-mcp
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
---

# Available tools and example prompts for Foundry MCP Server (preview)

This reference documents 79 Foundry MCP Server tools across 17 categories that let you manage agents, sessions, toolboxes, datasets, evaluations, model deployments, continuous evaluation, and more — all through conversational prompts instead of API calls. Use it to explore each tool and try the example prompts in your own project.

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

## Hosted agent sessions and files

Create and manage isolated compute sessions for hosted agents. Inspect logs and manage files in each session's filesystem.

Example prompts:

- "Create a session for my hosted agent `data-analyst`."
- "List the sessions for `data-analyst` and show the newest first."
- "Stream up to 100 log lines from session `analysis-2026`."
- "Upload `input.csv` to `/data/input.csv` in the session."
- "Download `/data/results.csv` from the session."
- "Delete session `analysis-2026` and release its compute resources."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `session_create` | write | Create a new session for a hosted agent. Sessions provide isolated compute environments for agent execution. | Agent name, session ID (optional) | Created session with its ID, status, and expiration. |
| `session_get` | read | Get details for a specific hosted agent session. | Agent name, session ID | Session status, version, creation time, and expiration. |
| `session_list` | read | List sessions for a hosted agent with pagination and sorting. | Agent name, limit, order, and `after` or `before` pagination cursor | Session list. |
| `session_delete` | write | Delete a hosted agent session and release its compute resources. | Agent name, session ID | Operation result. |
| `session_logstream` | read | Stream console output from a hosted agent session. The response is capped to prevent unbounded reads. | Agent name, session ID, maximum lines (optional) | Structured standard output and error log events. |
| `session_file_list` | read | List files and directories at a path in a hosted agent session. | Agent name, session ID, path (optional) | File and directory list. |
| `session_file_stat` | read | Get metadata for a file or directory in a hosted agent session. | Agent name, session ID, file path | Name, size, directory indicator, and last modified time. |
| `session_file_mkdir` | write | Create a directory in a hosted agent session. | Agent name, session ID, path, create-parents flag (optional), permission mode (optional) | Operation result. |
| `session_file_upload` | write | Upload base64-encoded content to a file in a hosted agent session. | Agent name, session ID, destination file path, base64 content | Operation result. |
| `session_file_download` | read | Download a file from a hosted agent session. | Agent name, session ID, file path | Base64-encoded file content. |
| `session_file_delete` | write | Delete a file or directory from a hosted agent session. | Agent name, session ID, file path, recursive flag (optional) | Operation result. |

## Toolbox management

Create, retrieve, version, update, and delete toolboxes in a Foundry project.

Example prompts:

- "Show me the `customer-support-tools` toolbox."
- "Get version 2 of `customer-support-tools`."
- "Create a new version of `customer-support-tools`."
- "Set version 2 of `customer-support-tools` as the default."
- "Set version 1 of `customer-support-tools` as the default, then delete version 2."
- "Delete the `old-support-tools` toolbox."

Toolbox versions are immutable. `toolbox_version_create` also creates the toolbox if it doesn't exist. For an existing toolbox, creating a version doesn't change the default version. Call `toolbox_update` with `defaultVersion` set to the new version to promote it. Before you delete the current default version, set another version as the default.

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `toolbox_get` | read | Retrieve a toolbox and its current default version. | Toolbox identifier | Toolbox details. |
| `toolbox_version_get` | read | List toolbox versions, or retrieve a specific version. | Toolbox identifier, version identifier for a specific version | Toolbox version list or details. |
| `toolbox_version_create` | write | Create an immutable toolbox version. If the toolbox doesn't exist, this tool also creates it. | Toolbox identifier and version details | Created toolbox version. |
| `toolbox_update` | write | Create or update a toolbox, including its default version. | Toolbox identifier, updated toolbox details, `defaultVersion` when changing the default | Created or updated toolbox details. |
| `toolbox_delete` | write | Delete a toolbox. | Toolbox identifier | Deletion confirmation. |
| `toolbox_version_delete` | write | Delete a specific toolbox version. To delete the current default, first set another version as the default. | Toolbox identifier, version identifier | Deletion confirmation. |

## Dataset management

Create, retrieve, version, and download evaluation datasets in a Foundry project.

Example prompts:

- "Upload my customer support Q&A dataset from this Azure Blob Storage URL."
- "Show me all datasets in my Foundry project."
- "Get details for the `customer-support-qa` dataset version 2."
- "List all versions of my `product-reviews` dataset."
- "Get a download URL for the latest version of `customer-support-qa`."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `evaluation_dataset_create` | write | Create or update a dataset version from an Azure Blob Storage URI. | Dataset name, version, Blob Storage URI | Dataset metadata with name, version, and URI. |
| `evaluation_dataset_get` | read | Get a dataset by name and version, or list all datasets in the project. | Dataset name and version (optional) | Dataset details or list of all datasets. |
| `evaluation_dataset_versions_get` | read | List all versions of a specific dataset. | Dataset name | List of version numbers with metadata. |
| `evaluation_dataset_sas_url_get` | read | Get a short-lived shared access signature (SAS) URL for downloading a dataset version's content. The version defaults to the latest. | Dataset name, dataset version (optional) | Short-lived dataset content URL. |

## Data generation jobs

Create and manage standalone data generation jobs for evaluation or fine-tuning data. Generate data from prompts, agents, traces, datasets, or uploaded files.

Example prompts:

- "Generate 100 evaluation question-and-answer samples from this prompt."
- "Show me the status of data generation job `job-123`."
- "Cancel data generation job `job-123`."
- "Delete the completed data generation job `job-123`."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `data_generation_job_create` | write | Start a standalone data generation job for evaluation or fine-tuning data. | Job name, generation type, scenario, maximum samples, generation model deployment, and source inputs | Operation result. |
| `data_generation_job_get` | read | Get one data generation job by ID, or list data generation jobs when the ID is omitted. | Job ID (optional) | Job details or job list. |
| `data_generation_job_cancel` | write | Cancel a data generation job. | Job ID | Operation result. |
| `data_generation_job_delete` | write | Delete a data generation job. | Job ID | Operation result. |

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
| `evaluation_get` | read | List evaluation groups or runs in the Foundry project. Set `isRequestForRuns` to true to list runs within a specific evaluation group. | Evaluation group ID (optional), evaluation run ID (optional), `isRequestForRuns` flag | List of evaluation groups or runs with status and scores, or details for a specific item. |
| `evaluation_comparison_create` | write | Create comparison results between a baseline and treatment evaluation runs. | Baseline run ID, treatment run IDs | Comparison insight ID. |
| `evaluation_comparison_get` | read | Get or list evaluation comparison insights. | Comparison insight ID (optional) | Comparison results with statistical analysis. |

## Trace evaluation

Run multi-turn conversation evaluations over agent traces or explicitly selected conversations and W3C trace IDs.

Example prompts:

- "Evaluate up to five traces from `customer-support-agent` from the last 24 hours for groundedness and task completion."
- "Evaluate these conversation IDs for customer satisfaction at the conversation level."
- "Evaluate these W3C trace IDs with my custom `tone-check` evaluator."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `evaluation_agent_traces_batch_eval_create` | write | Create a multi-turn batch evaluation over recent traces sampled from an agent. Creates an evaluation group when one isn't provided. | Evaluator names, agent name and version or agent ID, evaluation ID (optional), time range or lookback, maximum traces | Evaluation run. |
| `evaluation_traces_batch_eval_create` | write | Create a multi-turn batch evaluation over trace data selected by conversation IDs or W3C trace IDs. Creates an evaluation group when one isn't provided. | Evaluator names, trace source type, conversation IDs or trace IDs, evaluation ID (optional), evaluation level (optional) | Evaluation run. |

## Evaluation suites

Create, version, run, update, and delete evaluation suites that group datasets, target agents, and evaluators. You can also generate suites from prompts, agents, traces, datasets, or uploaded files.

Example prompts:

- "Create an evaluation suite named `support-quality` for my support dataset and agent."
- "Run version 2 of `support-quality`."
- "Update the display name and tags for version 2 of `support-quality`."
- "Generate an evaluation suite from recent traces for `customer-support-agent`."
- "Show me all evaluation suite generation jobs."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `evaluation_suite_create` | write | Create an evaluation suite version that groups evaluators and can reference a dataset and target agent. | Suite name, evaluator names, dataset and target agent (optional), evaluation settings (optional) | Evaluation suite version. |
| `evaluation_suite_get` | read | Get an evaluation suite version, list versions for a suite, or list suites. | Suite name (optional), version (optional), `listVersions` flag, and agent filter (optional) | Suite details, version list, or suite list. |
| `evaluation_suite_update` | write | Update the display name, description, or tags on an evaluation suite version. | Suite name, version, fields to update | Operation result. |
| `evaluation_suite_run` | write | Start an evaluation suite run. | Suite name, version (optional), evaluation name (optional), evaluation level (optional) | Evaluation run. |
| `evaluation_suite_delete` | write | Delete an evaluation suite version. The version defaults to the latest. | Suite name, version (optional) | Operation result. |
| `evaluation_suite_generation_job_create` | write | Start an evaluation suite generation job. | Suite name, generation model deployment, source inputs, generation settings | Generation job. |
| `evaluation_suite_generation_job_get` | read | Get one evaluation suite generation job by ID, or list jobs when the ID is omitted. | Job ID (optional), limit and continuation token (optional) | Generation job details or job list. |
| `evaluation_suite_generation_job_cancel` | write | Cancel an evaluation suite generation job. | Job ID | Operation result. |
| `evaluation_suite_generation_job_delete` | write | Delete an evaluation suite generation job. | Job ID | Operation result. |

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

## Evaluator generation jobs

Generate evaluators adaptively from prompts, agents, or datasets, and monitor or cancel the generation jobs.

Example prompts:

- "Generate an evaluator named `policy-compliance` from this policy prompt."
- "Regenerate `policy-compliance` from version 2 of my support dataset using model deployment `gpt-4o`."
- "Show me all running evaluator generation jobs."
- "Cancel evaluator generation job `job-456`."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `evaluator_generation_job_create` | write | Start an adaptive evaluator generation job. Supplying an existing evaluator name regenerates it from updated source inputs. | Model deployment, evaluator name, prompt, agent, or dataset source inputs | Generation job. |
| `evaluator_generation_job_get` | read | Get one evaluator generation job by ID, or list jobs when the ID is omitted. | Job ID (optional), status and agent filters (optional), pagination inputs (optional) | Generation job details or job list. |
| `evaluator_generation_job_cancel` | write | Cancel an evaluator generation job. | Job ID | Operation result. |

## Model catalog and details

Explore models in the Foundry model catalog, get model details, and determine whether a model can be deployed to Managed Compute.

Example prompts:

- "Show me all GPT-5.4 models available in the catalog."
- "List all Microsoft-published models with MIT license."
- "Get detailed information and code samples for GPT-5-mini."
- "Show me models advertised for Managed Compute."
- "Get Managed Compute details and deployment templates for `openai--gpt-oss-20b`."

For Managed Compute, `isManagedCompute` in `model_catalog_list` identifies an advertised candidate. Confirm deployability with `model_details_get`: `isFoundryManagedCompute` is the authoritative signal, and the resolved deployment templates identify the available deployment options and accelerators.

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `model_catalog_list` | read | List models from the Foundry model catalog with optional filters. For Managed Compute candidates, the response includes `isManagedCompute`. | Search keywords, publisher, license type, task type (all optional) | List of models with name, publisher, license, capabilities, and catalog deployment indicators. |
| `model_details_get` | read | Get full model details and code samples. For Managed Compute, use `isFoundryManagedCompute` to confirm deployability. | Model name or ID | Model specifications, pricing, supported regions, code samples, and resolved deployment templates. |

## Model deployment management

Deploy, inspect, and remove model deployments, including Managed Compute deployments, in a Foundry account.

Example prompts:

- "Use `model_deploy_azure_direct_model` to deploy GPT-5-mini as `production-chatbot` with 20 capacity units."
- "Show me all my current model deployments."
- "Show me all my Managed Compute deployments."
- "Use `model_deploy_managed_compute` to deploy `openai--gpt-oss-20b` as `gpt-oss-managed` using its A100_80GB deployment template."
- "Delete the `old-test-deployment` that I'm no longer using."

Choose explicit tools for each deployment type:

| Deployment type | Create or update |
| --- | --- |
| Foundry Models sold by Azure | `model_deploy_azure_direct_model` |
| Managed Compute | `model_deploy_managed_compute` |

Don't use the deprecated `model_deploy` alias for new calls. For Managed Compute, first use `model_catalog_list` as a candidate signal, then call `model_details_get`. Use `model_deploy_managed_compute` only when `isFoundryManagedCompute` is `true`, and pass one of the resolved deployment templates. Use `model_deployment_get` to retrieve either deployment type, and `model_deployment_delete` to delete either type.

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `model_deploy_azure_direct_model` | write | Create or update a deployment for a Foundry Model sold by Azure. | Model name, deployment name, capacity units | Deployment details with endpoint and provisioned capacity. |
| `model_deploy` | write | Deprecated backward-compatible alias of `model_deploy_azure_direct_model`. It has identical inputs and behavior. | Model name, deployment name, capacity units | Deployment details with endpoint and provisioned capacity. |
| `model_deploy_managed_compute` | write | Create a distinct Managed Compute deployment from a registry model asset and resolved deployment template. | Deployment name, `modelAssetId`, `deploymentTemplate`, `acceleratorType` (optional), `instanceCount` (optional), `versionUpgradeOption` (optional) | Managed Compute deployment details. |
| `model_deployment_get` | read | Get deployments of Foundry Models sold by Azure and Managed Compute deployments. With a name, the tool searches both resource types and can return both when they share that name. Without a name, it combines both lists. | Deployment name (optional) | Deployment details with `Kind` set to `ADM` or `Managed`. |
| `model_deployment_delete` | write | Delete either deployment type. The tool checks deployments of Foundry Models sold by Azure first, then Managed Compute deployments. | Deployment name | Deletion confirmation. |

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

Track deployment health, monitor metrics, check deprecation status, and view quota usage, including Managed Compute accelerator quota.

Example prompts:

- "Show me the request metrics for my `production-chatbot` deployment."
- "Check if any of my deployments are using deprecated model versions."
- "Show me quota usage across all regions for my subscription."
- "Show me A100_80GB, H100_80GB, MI300_192GB, and H200_141GB accelerator quota in East US 2."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `model_monitoring_metrics_get` | read | Get monitoring metrics (requests, latency, errors, quota) for a model deployment. | Deployment name, time range (optional) | Request count, latency percentiles, error rates, and token usage. |
| `model_deprecation_info_get` | read | Get deployment info enriched with deprecation and retirement schedules. | Deployment name (optional) | Deployment details with deprecation dates and suggested replacements. |
| `model_quota_list` | read | List available deployment quota and usage for a subscription in a region, including Managed Compute accelerator quota. | Subscription, region | Quota limits, current usage, and available capacity per model family or accelerator. |

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

## Continuous evaluation

Enable, monitor, and manage continuous evaluation for agents. Continuous evaluation automatically evaluates agent responses on an ongoing basis. The tool auto-detects the agent kind (prompt or hosted) and configures the appropriate evaluation mechanism — evaluation rules for prompt agents, or scheduled evaluation runs for hosted agents.

Example prompts:

- "Enable continuous evaluation for my `customer-support-agent` using Relevance and Groundedness evaluators."
- "Set up continuous evaluation for my hosted agent `triage-agent` to run every 2 hours."
- "Show me the continuous evaluation configuration for `customer-support-agent`."
- "Disable continuous evaluation for my `old-test-agent`."
- "Update continuous evaluation for `customer-support-agent` to sample 50% of responses."

| Tool | Access | Description | Key inputs | Returns |
| --- | --- | --- | --- | --- |
| `continuous_eval_create` | write | Enable or update continuous evaluation for an agent. Auto-detects agent kind and configures the appropriate evaluation mechanism. Creates the evaluation group if needed. | Agent name, evaluator names, model deployment name (for quality evaluators), enabled flag, interval hours (hosted agents), sampling rate (prompt agents), scenario (standard or business) | Continuous evaluation configuration with ID, status, and schedule details. |
| `continuous_eval_get` | read | Get continuous evaluation configuration for an agent. Returns all configurations, or filter by scenario for prompt agents. | Agent name, scenario filter (optional) | List of continuous evaluation configurations with evaluator details, schedule, and status. |
| `continuous_eval_delete` | write | Delete a continuous evaluation configuration for an agent. Use `continuous_eval_get` to find configuration IDs. | Configuration ID, agent name | Deletion confirmation. |

## Example workflows

**Model deployment and optimization:**

- "Show me the `gpt-5.6-sol` model in the catalog."
- "Deploy `gpt-5.6-sol` as `customer-service-bot` with 15 capacity units."
- "Monitor the request latency for my new deployment."
- "Recommend more cost-effective alternatives based on current usage."

**Managed Compute quota planning:**

- "Use `model_quota_list` to show my Managed Compute accelerator quota and usage for subscription `<subscription-id>` in East US 2."
- "Compare the available instances for `A100_80GB`, `H100_80GB`, `MI300_192GB`, and `H200_141GB`."
- "I need four instances. Identify which accelerators currently have enough available quota, and remind me that quota availability doesn't guarantee deployment capacity."
- "Before any deployment, show me the selected accelerator and instance count for review because Managed Compute allocates billable dedicated GPU capacity."

**Managed Compute deployment lifecycle:**

- "Use `model_catalog_list` to find models advertised for Managed Compute, where `isManagedCompute` is `true`."
- "For `openai--gpt-oss-20b`, use `model_details_get` to confirm that `isFoundryManagedCompute` is `true`, and show its registry `modelAssetId`, resolved deployment templates, and accelerators."
- "Use `model_quota_list` to check the selected accelerator in East US 2 before deployment."
- "Review the deployment template, accelerator, and instance count with me. After I confirm the billable dedicated GPU allocation, use `model_deploy_managed_compute` to create `gpt-oss-managed-test` with the registry `modelAssetId`, one resolved `deploymentTemplate`, and the approved `instanceCount`."
- "Use `model_deployment_get` to monitor `gpt-oss-managed-test` and verify that its `Kind` is `Managed`."
- "When testing is complete and I confirm cleanup, use `model_deployment_delete` to delete `gpt-oss-managed-test`."

**Agent evaluation workflow:**

- "List all agents in my project."
- "Evaluate my `customer-support-agent` v2 using Relevance, Groundedness, and Safety evaluators."
- "Compare my baseline evaluation against the new run."
- "Show me the comparison results with statistical significance."

**Continuous evaluation setup:**

- "List all agents in my project."
- "Enable continuous evaluation for my `customer-support-agent` using Relevance, Groundedness, and Safety evaluators with the existing `gpt-5.6-luna` deployment."
- "Show me the continuous evaluation configuration for `customer-support-agent`."
- "Update continuous evaluation to sample 25% of responses with a maximum of 10 runs per hour."

**Resource management and cleanup:**

- "List all my current deployments and their usage."
- "Check which deployments are using deprecated model versions."
- "Show me my quota usage across all regions."
- "Delete unused test deployments to free up capacity."

## Preview limitations

Foundry MCP Server is in public preview. The following limitations apply:

- **No network isolation** — Foundry MCP Server uses the public endpoint `https://mcp.ai.azure.com`. Resources behind Azure Private Links aren't accessible. For private MCP connectivity, [build your own MCP server](build-your-own-mcp-server.md) and connect it to Agent Service with [private networking](../agents/how-to/tools/model-context-protocol.md#public-and-private-mcp-server-endpoints).
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
| Private endpoint not reachable | Foundry resources use Azure Private Links that the hosted Foundry MCP Server can't reach. | Remove private endpoint restrictions, use SDKs/REST APIs, or use a [custom MCP server with Agent Service private networking](../agents/how-to/tools/model-context-protocol.md#public-and-private-mcp-server-endpoints). |

For more troubleshooting guidance, see [Foundry MCP Server security and best practices](security-best-practices.md#troubleshooting).

## Related content

- Get started with [Foundry MCP Server](get-started.md)
- Learn how to [build your own MCP server](build-your-own-mcp-server.md)
- Review [security best practices for MCP servers](security-best-practices.md)
- Learn how to submit your MCP server for certification at [Microsoft MCP server certification overview](/microsoft-copilot-studio/mcp-certification).
