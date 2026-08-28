---
title: "Evaluate deployed interactions with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to evaluate deployed agent and model interactions by response ID or Application Insights trace."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 08/26/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to evaluate deployed interactions so that I can assess real application behavior without replaying requests.
---

# Evaluate deployed agent and model interactions

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Evaluate stored responses or OpenTelemetry traces from deployed agents and models without replaying the original requests.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- Stored response IDs for response evaluation, or an Application Insights resource connected to your Foundry project for trace evaluation.
- OpenTelemetry spans that meet the trace data requirements when you evaluate traces.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Evaluate interactions by response ID

Retrieve and evaluate Foundry agent responses by response IDs using the `azure_ai_responses` data source type. Use this scenario to evaluate specific agent interactions after they occur.

> [!TIP]
> Before you begin, complete [client setup](cloud-evaluation.md#set-up-the-sdk-client).

A **response ID** is a unique identifier returned each time a Foundry agent generates a response. You can collect response IDs from agent interactions by using the [Responses API](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1&preserve-view=true) or from your application's trace logs. Provide the IDs inline as file content.

> [!IMPORTANT]
> Agent response evaluations (`azure_ai_responses`) support only `file_content` for providing response IDs. The `file_id` source type isn't supported and returns a `400 Bad Request` error.

### Collect response IDs

Each call to the Responses API returns a response object with a unique `id` field. Collect these IDs from your application's interactions, or generate them directly:

```python
# Generate response IDs by calling a model through the Responses API
response = openai_client.responses.create(
    model=model_deployment_name,
    input="What is machine learning?",
)
print(response.id)  # Example: resp_abc123
```

You can also collect response IDs from agent interactions in your application's trace logs or monitoring pipeline. Each response ID uniquely identifies a stored response that the evaluation service can retrieve.

### Create evaluation and run

# [Python](#tab/python)

```python
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

data_source_config = {"type": "azure_ai_source", "scenario": "responses"}

testing_criteria = [
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="coherence",
        evaluator_name="builtin.coherence",
        initialization_parameters={"model": model_deployment_name},
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="violence",
        evaluator_name="builtin.violence",
    ),
]

eval_object = openai_client.evals.create(
    name="Agent Response Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_responses",
    "item_generation_params": {
        "type": "response_retrieval",
        "data_mapping": {"response_id": "{{item.resp_id}}"},
        "source": {
            "type": "file_content",
            "content": [
                {"item": {"resp_id": "resp_abc123"}},
                {"item": {"resp_id": "resp_def456"}},
            ]
        },
    },
}

eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-response-evaluation",
    data_source=data_source,
)
```

# [JavaScript/TypeScript](#tab/javascript)

```javascript
const evalObject = await openaiClient.evals.create({
    name: "Agent Response Evaluation",
    data_source_config: { type: "azure_ai_source", scenario: "responses" },
    testing_criteria: [
        {
            type: "azure_ai_evaluator",
            name: "coherence",
            evaluator_name: "builtin.coherence",
            initialization_parameters: { model: modelDeploymentName },
        },
        {
            type: "azure_ai_evaluator",
            name: "violence",
            evaluator_name: "builtin.violence",
        },
    ],
});

const responseEvalRun = await openaiClient.evals.runs.create(evalObject.id, {
    name: "agent-response-evaluation",
    data_source: {
        type: "azure_ai_responses",
        item_generation_params: {
            type: "response_retrieval",
            data_mapping: { response_id: "{{item.resp_id}}" },
            source: {
                type: "file_content",
                content: [
                    { item: { resp_id: "resp_abc123" } },
                    { item: { resp_id: "resp_def456" } },
                ],
            },
        },
    },
});
console.log(`Evaluation run created: ${responseEvalRun.id}`);
```

# [cURL](#tab/curl) 

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals/${EVAL_ID}/runs" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "agent-response-evaluation",
    "data_source": {
      "type": "azure_ai_responses",
      "item_generation_params": {
        "type": "response_retrieval",
        "data_mapping": {"response_id": "{{item.resp_id}}"},
        "source": {
          "type": "file_content",
          "content": [
            {"item": {"resp_id": "resp_abc123"}},
            {"item": {"resp_id": "resp_def456"}}
          ]
        }
      }
    }
  }'
```

---

For a complete runnable example, see [sample_agent_response_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_agent_response_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).

## Evaluate traces (preview)

Evaluate agent interactions that Application Insights already captured. Use the `azure_ai_traces` data source type. This scenario is useful for post-deployment evaluation of real production traffic. You select traces from your monitoring pipeline and run evaluators against them without replaying any requests.

> [!IMPORTANT]
> Trace evaluation is the recommended approach for evaluating **agents not built with the Microsoft Foundry Agent Service** - including LangChain and custom frameworks. As long as your agent emits [OpenTelemetry spans following the GenAI semantic conventions](#trace-data-requirements) to Application Insights, trace evaluation can assess its interactions by using the same evaluators available for Foundry agents.

Trace evaluation supports two modes:

- **By trace IDs** - Evaluate specific agent interactions by providing their `operation_Id` values from Application Insights.
- **By agent filter** - Automatically discover and evaluate recent traces for a given agent, without manually collecting trace IDs.

> [!TIP]
> Before you begin, complete [client setup](cloud-evaluation.md#set-up-the-sdk-client). This scenario also requires an [Application Insights resource connected to your Foundry project](../../observability/how-to/trace-agent-setup.md).

### Intelligent sampling
 
Trace evaluation supports intelligent sampling, which selects a representative subset of traces for evaluation instead of evaluating every captured trace. Turn on the **Intelligent sampling** toggle in the Foundry portal when you configure a trace evaluation run. Intelligent sampling reduces evaluation cost while preserving trace diversity - ensuring that edge cases, error paths, and varied conversation patterns are included in the evaluated set.

#### How intelligent sampling works

The sampling algorithm uses a MinHash farthest-first diversity approach that runs in multiple stages:

1. **Exact deduplication** - Removes duplicate traces from the pool.
1. **Hard filters** - Removes broken sessions, truncated traces, and malformed tool calls that aren't suitable for evaluation.
1. **Aggregation** - Combines trace-level signals into a unified representation.
1. **MinHash farthest-first selection** - Computes locality-sensitive hashes (MinHash signatures) of user text to estimate similarity between traces, then iteratively selects the most dissimilar trace from the remaining pool. Each successive pick maximizes distance from all previously selected traces.

This approach produces significantly higher lexical diversity and broader vocabulary coverage compared to random sampling, which means the evaluated set better represents the full range of agent interactions - including rare, hard, and novel cases that random sampling tends to miss.

Intelligent sampling is particularly effective for:

- **Evaluation and benchmarks** - Maximizes coverage of the input distribution so evaluation scores reflect real-world diversity.
- **Rubric generation** - Produces more focused and actionable rubrics by exposing diverse conversation patterns.
- **Finetuning dataset curation** - Selects traces that help models learn more efficiently.

The algorithm runs entirely on local compute with no extra API calls, so it doesn't incur extra model inference costs beyond the evaluation itself.

#### Intelligent sampling example

```python
# Eval group for trace-based evaluations
data_source_config = {
    "type": "azure_ai_source",
    "scenario": "traces",
}

print("Creating trace-based evaluation group")
eval_object = client.evals.create(
    name="Trace Evaluation (Agent Smart Filter)",
    data_source_config=data_source_config,  # type: ignore
    testing_criteria=testing_criteria,
)
print(f"Evaluation created (id: {eval_object.id})")

# Compute time window in unix seconds
# Pad end_time by +600s (10 min) to avoid ingestion-delay edge exclusion
now_unix = int(time.time())
end_time = now_unix + 600
start_time = now_unix - (args.lookback_hours * 3600)

# Build trace_source based on mode
trace_source: dict = {
    "type": "agent_filter",
    "start_time": start_time,
    "end_time": end_time,
    "max_traces": args.max_traces,
    "filter_strategy": "smart_filtering"
}

# Add agent name/version or agent id
trace_source["agent_name"] = agent_name
trace_source["agent_version"] = agent_version
## trace_source["agent_id"] = args.agent_id

data_source = {
    "type": "azure_ai_trace_data_source_preview",
    "trace_source": trace_source,
}

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="trace-evaluation-agent-smart-filter-run",
    data_source=data_source,  # type: ignore
)
```

### Trace data requirements

Trace evaluation requires your agent to emit spans that follow the [OpenTelemetry semantic conventions for generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/). Specifically, the evaluation service reads **`invoke_agent` spans** from Application Insights and extracts conversation data from their attributes.

The following span attributes are used:

| Attribute | Required | Description |
|-----------|----------|-------------|
| `gen_ai.operation.name` | **Yes** | Must equal `"invoke_agent"`. The service ignores all other spans. |
| `gen_ai.agent.id` | For agent filter mode | Unique agent identifier (format: `agent-name:version`). |
| `gen_ai.agent.name` | For agent filter mode | Human-readable agent name. |
| `gen_ai.input.messages` | For evaluators query inputs | JSON array of input messages following the [GenAI semantic conventions message format](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/#invoke-agent-span). Messages with role `user` or `system` map to `query`. Messages with role `assistant` or `tool` map to `response`. |
| `gen_ai.output.messages` | For evaluators query inputs | JSON array of model-generated output messages. All output messages map to `response`. If output also contains `type: tool_call` or `type: tool_result`, it maps to `tool_calls`. |
| `gen_ai.tool.definitions` | Optional | JSON array of tool schemas available to the agent. If absent, the service attempts to infer tool definitions from tool call messages, but inferred schemas might be incomplete. |
| `gen_ai.conversation.id` | Optional | Conversation identifier, passed through to evaluation results for correlation. |

> [!NOTE]
> If `gen_ai.input.messages` and `gen_ai.output.messages` are empty or missing, quality evaluators (coherence, fluency, relevance, intent resolution) return `score=None`. Safety evaluators (violence, self-harm, sexual, hate/unfairness) can still produce scores with partial data but they might not produce meaningful results.

For Python agents built with the Azure AI Agent Server SDK, add the `[tracing]` extra to enable automatic span emission:

```bash
pip install "azure-ai-agentserver-core[tracing]"
```

### Prerequisites for trace evaluation

In addition to the general [prerequisites](cloud-evaluation.md#prerequisites), trace evaluation requires:

- An [Application Insights resource](/azure/azure-monitor/app/app-insights-overview) connected to your Foundry project. See [Set up tracing in Microsoft Foundry](../../observability/how-to/trace-agent-setup.md).
- The project's managed identity must have the **Log Analytics Reader** role on both the Application Insights resource and its linked Log Analytics workspace. If the tables that store your traces are [protected](/azure/azure-monitor/logs/protected-tables-configure) (their protection level is set to **Protected**), also assign the [Privileged Monitoring Data Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader) role at the same scopes so the service can read the protected trace tables.
- The `azure-monitor-query` Python package (only needed if you collect trace IDs manually).

```bash
pip install "azure-ai-projects>=2.2.0" azure-monitor-query
```

Set these environment variables:

- `APPINSIGHTS_RESOURCE_ID` — The Application Insights resource ID (for example, `/subscriptions/<subscription_id>/resourceGroups/<rg_name>/providers/Microsoft.Insights/components/<resource_name>`).
- `AGENT_ID` — The agent identifier emitted by the tracing integration (`gen_ai.agent.id` attribute), used to filter traces. Format: `agent-name:version`.
- `TRACE_LOOKBACK_HOURS` — (Optional) Number of hours to look back when querying traces. Defaults to `1`.

### Option A: Evaluate by agent filter

The simplest approach is to let the service automatically discover and evaluate recent traces for a specific agent. You don't need to manually collect trace IDs.

```python
import os

agent_id = os.environ["AGENT_ID"]  # e.g., "my-weather-agent:1"
trace_lookback_hours = int(os.environ.get("TRACE_LOOKBACK_HOURS", "1"))

# Create the evaluation
data_source_config = {
    "type": "azure_ai_source",
    "scenario": "traces",
}

eval_object = openai_client.evals.create(
    name="Agent Trace Evaluation (by agent)",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,  # See "Set up evaluators" below
)

# Create a run — the service queries App Insights for matching traces
data_source = {
    "type": "azure_ai_traces",
    "agent_id": agent_id,
    "max_traces": 50,           # Maximum number of traces to evaluate
    "lookback_hours": trace_lookback_hours,
}

eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-trace-eval-run",
    data_source=data_source,
)

print(f"Evaluation run started: {eval_run.id}")
```

The service filters `invoke_agent` spans by the `gen_ai.agent.id` attribute, samples up to `max_traces` unique trace IDs, and evaluates all spans from those traces.

### Option B: Evaluate by trace IDs

For more control, collect specific trace IDs from Application Insights and evaluate them. This method is useful when you want to evaluate a curated set of interactions, such as traces flagged by alerts or sampled for quality review.

#### Collect trace IDs from Application Insights

Query Application Insights for `operation_Id` values from your agent's traces. Each `operation_Id` represents a complete agent interaction:

```python
import os
from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

appinsights_resource_id = os.environ["APPINSIGHTS_RESOURCE_ID"]
agent_id = os.environ["AGENT_ID"]
trace_query_hours = int(os.environ.get("TRACE_LOOKBACK_HOURS", "1"))

end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(hours=trace_query_hours)

query = f"""dependencies
| where timestamp between (datetime({start_time.isoformat()}) .. datetime({end_time.isoformat()}))
| extend agent_id = tostring(customDimensions["gen_ai.agent.id"])
| where agent_id == "{agent_id}"
| distinct operation_Id"""

credential = DefaultAzureCredential()
logs_client = LogsQueryClient(credential)
response = logs_client.query_resource(
    appinsights_resource_id,
    query=query,
    timespan=None,  # Time range is specified in the query itself
)

trace_ids = []
if response.status == LogsQueryStatus.SUCCESS:
    for table in response.tables:
        for row in table.rows:
            trace_ids.append(row[0])

print(f"Found {len(trace_ids)} trace IDs")
```

#### Create evaluation and run with trace IDs

```python
# Create the evaluation
data_source_config = {
    "type": "azure_ai_source",
    "scenario": "traces",
}

eval_object = openai_client.evals.create(
    name="Agent Trace Evaluation (by trace IDs)",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,  # See "Set up evaluators" below
)

# Create a run using the collected trace IDs
data_source = {
    "type": "azure_ai_traces",
    "trace_ids": trace_ids,
    "lookback_hours": trace_query_hours,
}

eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-trace-eval-run",
    metadata={
        "agent_id": agent_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    },
    data_source=data_source,
)

print(f"Evaluation run started: {eval_run.id}")
```

### Set up evaluators and data mappings

When you evaluate traces, the service automatically extracts conversation data from the OpenTelemetry span attributes. Use these field names directly in `data_mapping` (without the `item.` or `sample.` prefixes used in other scenarios):

| Variable | Source attribute | Description |
|----------|----------------|-------------|
| `{{item.query}}` | `gen_ai.input.messages` (user/system roles) | The user query extracted from the trace. |
| `{{item.response}}` | `gen_ai.input.messages` (assistant/tool roles) + `gen_ai.output.messages` | The agent's response extracted from the trace. |
| `{{item.tool_definitions}}` | `gen_ai.tool.definitions` | Tool schemas available to the agent. Only required for tool-related evaluators. |
| `{{item.tool_calls}}` | Extracted from assistant messages in `gen_ai.input.messages` / `gen_ai.output.messages` | Tool calls made by the agent during the interaction. Used by tool evaluators. Only required for tool-related evaluators. |

```python
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

testing_criteria = [
    # Quality evaluators — require query and response from trace data
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="intent_resolution",
        evaluator_name="builtin.intent_resolution",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
        initialization_parameters={"model": model_deployment_name},
    ),
    # Tool evaluators — assess tool usage quality
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="tool_call_accuracy",
        evaluator_name="builtin.tool_call_accuracy",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "tool_calls": "{{item.tool_calls}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
        initialization_parameters={"model": model_deployment_name},
    ),
    # Safety evaluators — work even with partial trace data
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="violence",
        evaluator_name="builtin.violence",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        initialization_parameters={"threshold": 4},
    ),
]
```

## Next steps

- To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).
- For a complete runnable example, see [sample_evaluations_builtin_with_traces.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_traces.py) on GitHub. 


