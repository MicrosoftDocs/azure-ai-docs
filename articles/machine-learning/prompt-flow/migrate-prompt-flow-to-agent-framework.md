---
title: Migrate from Prompt Flow to Microsoft Agent Framework
titleSuffix: Azure Machine Learning
description: Learn how to migrate your Prompt Flow workflows to Microsoft Agent Framework with a structured plan covering audit, rebuild, validation, operations, and cutover.
author: scottpolly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: overview
ms.date: 04/15/2026
ai-usage: ai-assisted
#CustomerIntent: As a developer running Prompt Flow workloads on Azure Machine Learning, I want to understand how to migrate to Microsoft Agent Framework so that I can transition before Prompt Flow is retired.
---

# Migrate from Prompt Flow to Microsoft Agent Framework

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

Prompt Flow is a development tool that streamlines the entire development cycle of AI applications powered by large language models (LLMs). Prompt Flow provides a comprehensive solution that simplifies the process of prototyping, experimenting, iterating, and deploying your AI applications.

This article explains the key differences between Prompt Flow and Agent Framework, maps Prompt Flow concepts to their Agent Framework equivalents, covers Azure Machine Learning–specific considerations, and outlines a migration plan.

To begin your migration, review the [concept mapping](#key-concept-mapping) to understand Agent Framework equivalents for your current flow, then follow [Rebuild and validate your Prompt Flow workflow in Microsoft Agent Framework](how-to-migrate-prompt-flow-to-agent-framework.md) for step-by-step instructions.

## Prerequisites

- An existing Prompt Flow application running on Azure Machine Learning.
- Python 3.10 or later.
- An Azure subscription with an Azure OpenAI resource.
- Microsoft Agent Framework SDK: `pip install agent-framework`.


## Why migrate

Agent Framework replaces Prompt Flow's YAML-based visual graph with a code-first Python (and .NET) framework that provides:

- **Type-safe workflows**: `WorkflowBuilder` validates your execution graph at build time, catching type mismatches and unreachable nodes before runtime.
- **Built-in agent support**: Create AI agents with `AzureOpenAIChatClient().as_agent()` and register Python functions as tools without separate tool registration YAML.
- **Native OpenTelemetry tracing**: Agent Framework automatically emits spans for every executor invocation and LLM call. Connect to Application Insights with a single `configure_azure_monitor()` call.
- **Flexible deployment**: Package workflows as standard FastAPI applications and deploy to Azure Container Apps, Azure Functions, or any container host.
- **Multi-agent orchestration**: Route, fan-out, fan-in, and conditionally branch between specialized agents using `add_edge()`, `add_fan_out_edges()`, and `add_fan_in_edges()`.

> [!NOTE]
> Agent Framework is a code-first framework and doesn't include a visual graph editor. If your team relies on Prompt Flow's visual authoring experience, plan for the transition to code-based workflow definition.

## Azure Machine Learning considerations

### Use AzureOpenAIChatClient for Azure OpenAI endpoints

Azure Machine Learning Prompt Flow connects to Azure OpenAI endpoints (`https://<resource>.openai.azure.com`). In Agent Framework, use `AzureOpenAIChatClient` for these endpoints.

```python
import os

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential

client = AzureOpenAIChatClient(
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    credential=DefaultAzureCredential(),
)
```

> [!NOTE]
> If you migrate to a Microsoft Foundry project endpoint (`https://<resource>.services.ai.azure.com`), use `FoundryChatClient` instead. 

### Environment variables

Prompt Flow uses Azure Machine Learning workspace connections to store credentials. Agent Framework reads credentials from environment variables. Export your connection values and store them in a `.env` file:

```text
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT=<your-deployment-name>
APPLICATIONINSIGHTS_CONNECTION_STRING=<your-connection-string>
```

Load these variables at the start of your application with `load_dotenv()` from the `python-dotenv` package. For production deployments, store secrets in Azure Key Vault instead of `.env` files.

### Tracing

Prompt Flow uses Azure Machine Learning's built-in run history to monitor flow executions. Agent Framework replaces this feature with OpenTelemetry-based tracing. Call `configure_azure_monitor()` with your Application Insights connection string to send traces, spans, and metrics.

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"],
)
```

### Managed online endpoints

Prompt Flow deployments on Azure Machine Learning managed online endpoints don't have a direct Agent Framework equivalent. Package your Agent Framework workflow as a FastAPI application and deploy to Azure Container Apps, Azure Functions, or any container host.

## Key concept mapping

The following table maps Prompt Flow concepts to their Agent Framework equivalents.

| Prompt Flow concept | Agent Framework equivalent | Details |
|---|---|---|
| Flow (YAML / visual graph) | `WorkflowBuilder` | Fluent builder that wires executor instances with `.add_edge()`, then `.build()`. Pass the start executor to the constructor via `start_executor=`. |
| Node (any step) | `Executor` class with a `@handler` method | One class per logical step. |
| LLM node | `AzureOpenAIChatClient().as_agent(instructions=...)` | The agent replaces the system prompt template. |
| Python node | Python logic inside an `Executor` `@handler` | No YAML snippet or separate file registration. |
| Prompt node | String formatting inside an `Executor` `@handler` | Inline template logic. |
| Embed Text + Vector Lookup nodes | `AzureAISearchContextProvider` via `context_providers=[...]` | Handles embedding and search automatically. |
| If / conditional node | `.add_edge(source, target, condition=fn)` | The condition function receives the outgoing message. |
| Parallel nodes (no dependencies) | `.add_fan_out_edges(source, [targetA, targetB])` | Broadcasts one message to multiple executors concurrently. |
| Merge / aggregate node | `.add_fan_in_edges([sourceA, sourceB], target)` | Waits for all listed sources before proceeding. |
| Flow inputs | Type annotation on the start `Executor`'s `@handler` parameter | The first handler's parameter type defines the workflow input. |
| Flow outputs | `await ctx.yield_output(value)` in the terminal `Executor` | Use `WorkflowContext[Never, str]` for terminal executors. |
| Connections (credentials) | Environment variables read automatically by Agent Framework clients | Store in `.env`; load with `load_dotenv()`. |
| Evaluation flow | Evaluators from Azure AI Evaluation SDK | Use `SimilarityEvaluator`, `CoherenceEvaluator`, `GroundednessEvaluator`, and others to score outputs. |
| Managed Online Endpoint | FastAPI wrapper + Azure Container Apps | Standard container deployment. |

### WorkflowContext type parameters

`WorkflowContext` uses type parameters to control how an executor communicates:

| Type | Behavior |
|---|---|
| `WorkflowContext` (no type parameters) | Side effects only. No message sent downstream and no workflow output yielded. |
| `WorkflowContext[str]` | Sends a `str` downstream via `ctx.send_message()`. |
| `WorkflowContext[Never, str]` | Yields a `str` as the final workflow output via `ctx.yield_output()`. |
| `WorkflowContext[str, str]` | Both send a message downstream and yields a workflow output. |

Import `Never` from `typing` (Python 3.11+) or `typing_extensions` (Python 3.10). The `Never` type indicates that an executor doesn't send messages downstream. Use it in terminal executors that only yield final workflow output.

## Migration plan

A typical migration moves through five steps. Work through them in order. Each step has a gate that confirms you're ready to proceed. The early steps (audit, rebuild, validate) focus on achieving functional parity with your existing flow. The later steps (ops, cutover) handle production readiness and traffic migration.

For the full hands-on procedures for each step, see the following articles:

- [Rebuild and validate your Prompt Flow workflow in Microsoft Agent Framework](how-to-migrate-prompt-flow-to-agent-framework.md) (audit, rebuild, validate)
- [Deploy and operate your migrated Agent Framework workflow](how-to-deploy-migrated-agent-framework-workflow.md) (migrate ops, cut over)

1. **Audit and map.** Export your `flow.dag.yaml` and map every node to its Agent Framework equivalent using the [concept mapping](#key-concept-mapping) table in this article. Identify nodes that need custom logic versus nodes that map directly to built-in Agent Framework components. Before moving on, confirm your node-mapping table accounts for every node in your flow.

1. **Rebuild.** Re-implement the workflow using `WorkflowBuilder` and `Executor` classes. Start with a single linear path through your flow, then add branches, fan-out, and conditional edges. Proceed when your Python files produce working output that mirrors your Prompt Flow behavior.

1. **Validate.** Run your original Prompt Flow and the new Agent Framework workflow side-by-side with the same inputs. Use evaluators from the Azure AI Evaluation SDK (such as `SimilarityEvaluator`) to score output parity. Aim for a mean similarity score of at least 3.5 (out of 5) in your `parity_results.csv` before continuing.

1. **Migrate ops.** Wire up OpenTelemetry tracing with `configure_azure_monitor()`, deploy to Azure Container Apps, and add a CI/CD quality gate that runs the parity evaluation on every pull request. Confirm that traces appear in Application Insights, the deployment is healthy, and the pipeline passes.

1. **Cut over.** Switch production traffic to the Agent Framework deployment. After confirming stable operation, decommission your Prompt Flow managed online endpoints, workspace connections, and compute resources.

## Related content

Start with the hands-on how-to guide, then set up tracing for your deployment. Use the Agent Framework documentation and migration samples as reference.

- [Rebuild and validate your Prompt Flow workflow in Microsoft Agent Framework](how-to-migrate-prompt-flow-to-agent-framework.md)
- [Deploy and operate your migrated Agent Framework workflow](how-to-deploy-migrated-agent-framework-workflow.md)
- [What is Azure Machine Learning prompt flow?](overview-what-is-prompt-flow.md)
- [Microsoft Agent Framework documentation](/agent-framework/)
- [Microsoft Agent Framework GitHub repository](https://github.com/microsoft/agent-framework)
- [PromptFlow-to-MAF migration samples](https://github.com/microsoft/agent-framework/tree/main/migration-guide/PromptFlow-to-MAF)
- [Azure AI Evaluation SDK](/python/api/overview/azure/ai-evaluation-readme)
