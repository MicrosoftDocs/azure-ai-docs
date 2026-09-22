---
title: "Get cloud evaluation results with the Microsoft Foundry SDK"
description: "Learn how to poll cloud evaluation runs, interpret results, review model-target latency and estimated cost, cancel runs, and troubleshoot errors."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - references_regions
  - doc-kit-assisted
ms.topic: how-to
ms.date: 09/15/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to retrieve and interpret cloud evaluation results so that I can compare quality, latency, and estimated cost.
---

# Get evaluation results with Microsoft Foundry SDK

Poll asynchronous evaluation runs, retrieve item and aggregate output, review
model-target latency and cost, cancel runs, and resolve common evaluation
errors.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- An evaluation ID and run ID from a submitted cloud evaluation.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Poll for a completed run

After an evaluation run completes, retrieve the scored results and review them in the portal or programmatically.

Evaluation runs are asynchronous. Poll the run status until it completes, then retrieve the results:

# [Python](#tab/python)

```python
import time
from pprint import pprint

while True:
    run = openai_client.evals.runs.retrieve(
        run_id=eval_run.id, eval_id=eval_object.id
    )
    if run.status in ("completed", "failed", "canceled"):
        break
    time.sleep(5)
    print("Waiting for eval run to complete...")

if run.status != "completed":
    raise RuntimeError(f"Evaluation run ended in {run.status}: {run.error}")

# Retrieve results
# Iterating the list operation retrieves all pages.
output_items = list(
    openai_client.evals.runs.output_items.list(
        run_id=run.id, eval_id=eval_object.id
    )
)
pprint(output_items)
print(f"Report URL: {run.report_url}")
```

# [C#](#tab/csharp)

```csharp
string evaluationId = "<evaluation-id>";
string runId = "<evaluation-run-id>";
ClientResult evaluationRun = await evaluationClient.GetEvaluationRunAsync(
  evaluationId: evaluationId,
  evaluationRunId: runId,
  options: new());
string runStatus = GetString(evaluationRun, "status");

while (runStatus != "completed"
  && runStatus != "failed"
  && runStatus != "canceled")
{
  await Task.Delay(TimeSpan.FromSeconds(5));
  evaluationRun = await evaluationClient.GetEvaluationRunAsync(
    evaluationId: evaluationId,
    evaluationRunId: runId,
    options: new());
  runStatus = GetString(evaluationRun, "status");
  Console.WriteLine($"Current status: {runStatus}");
}

if (runStatus != "completed")
{
  throw new InvalidOperationException(
    evaluationRun.GetRawResponse().Content.ToString());
}

// The .NET protocol method returns one page at a time.
string? after = null;
bool hasMore;
do
{
  ClientResult outputItems = await evaluationClient
    .GetEvaluationRunOutputItemsAsync(
    evaluationId: evaluationId,
    evaluationRunId: runId,
    limit: null,
    order: "asc",
    after: after,
    outputItemStatus: null,
    options: new());
  using JsonDocument page = JsonDocument.Parse(
    outputItems.GetRawResponse().Content.ToMemory());
  foreach (JsonElement item in page.RootElement
    .GetProperty("data").EnumerateArray())
  {
    Console.WriteLine(item);
  }
  hasMore = page.RootElement.GetProperty("has_more").GetBoolean();
  after = hasMore
    ? page.RootElement.GetProperty("last_id").GetString()
    : null;
}
while (hasMore);

Console.WriteLine(evaluationRun.GetRawResponse().Content);
```

Reference: [`EvaluationClient` protocol methods](https://github.com/openai/openai-dotnet/blob/main/OpenAI/src/Custom/Evals/EvaluationClient.Protocol.cs)

# [JavaScript/TypeScript](#tab/javascript)

```javascript
let run = evalRun;
while (!["completed", "failed", "canceled"].includes(run.status)) {
  run = await openaiClient.evals.runs.retrieve(run.id, {
    eval_id: evalObject.id,
  });
  console.log(`Waiting for eval run to complete... ${run.status}`);
  await new Promise((resolve) => setTimeout(resolve, 5000));
}

if (run.status !== "completed") {
  throw new Error(`Evaluation run ended in ${run.status}`);
}

// Retrieve results
const outputItems = [];
for await (const item of openaiClient.evals.runs.outputItems.list(run.id, {
  eval_id: evalObject.id,
})) {
  outputItems.push(item);
}
console.log(JSON.stringify(outputItems, null, 2));
console.log(`Report URL: ${run.report_url}`);
```

# [cURL](#tab/curl)

Use the evaluation and run IDs that the cURL create requests return with the Evals REST endpoints. For runnable polling and output-item retrieval code, use the Python or JavaScript/TypeScript tab.

---

## Interpret results

For a single data example, all evaluators output the following schema:  

- **Label**: a binary "pass" or "fail" label, similar to a unit test's output. Use this result to facilitate comparisons across evaluators.
- **Score**: a score from the natural scale of each evaluator. Some evaluators use a fine-grained rubric, scoring on a 5-point scale (quality evaluators) or a 7-point scale (content safety evaluators). Others, like textual similarity evaluators, use F1 scores, which are floats between 0 and 1. Any nonbinary "score" is binarized to "pass" or "fail" in the "label" field based on the "threshold".
- **Threshold**: any nonbinary scores are binarized to "pass" or "fail" based on a default threshold, which the user can override in the SDK experience.
- **Reason**: To improve intelligibility, all LLM-judge evaluators also output a reasoning field to explain why a certain score is given.
- **Details**: (optional) For some evaluators, such as tool_call_accuracy, there might be a "details" field or flags that contain additional information to help users debug their applications.

### Review an item result

```json
{
  "type": "azure_ai_evaluator",
  "name": "Coherence",
  "metric": "coherence",
  "score": 4.0,
  "label": "pass",
  "reason": "The response is well-structured and logically organized, presenting information in a clear and coherent manner.",
  "threshold": 3,
  "passed": true
}
```

### Review aggregate results

For aggregate results over multiple data examples (a dataset), the average rate of the examples with a "pass" forms the passing rate for that dataset.

```json
{
  "eval_id": "eval_abc123",
  "run_id": "run_xyz789",
  "status": "completed",
  "result_counts": {
    "passed": 85,
    "failed": 15,
    "total": 100
  },
  "per_testing_criteria_results": [
    {
      "name": "coherence",
      "passed": 92,
      "failed": 8,
      "pass_rate": 0.92
    },
    {
      "name": "relevance", 
      "passed": 78,
      "failed": 22,
      "pass_rate": 0.78
    }
  ]
}
```

## Review model-target latency and estimated cost

When you retrieve or list completed model-target runs, they can include run-wide
target latency under `latency.target` and estimated inference cost under
`estimated_cost.target`.

Both properties are optional. The service omits latency when no evaluation row
has a usable target latency measurement. It omits estimated cost when the run
isn't a model-target evaluation or when no target model can be priced.
Estimated cost is currently available for Global Standard model deployments
when the run has usable target token attribution and pricing data.

The following example shows the relevant part of a completed evaluation run:

```json
{
  "latency": {
    "target": {
      "p50_ms": 812.25,
      "p95_ms": 2400.5,
      "sample_count": 47
    }
  },
  "estimated_cost": {
    "target": {
      "estimated_cost": 0.012346,
      "currency": "USD",
      "completeness": "partial",
      "pricing_version": "rate-card-version",
      "model_costs": [
        {
          "model_name": "gpt-5-mini",
          "estimated_cost": 0.012346,
          "prompt_tokens": 12000,
          "cached_tokens": 2000,
          "completion_tokens": 3000
        }
      ],
      "unpriced_models": [
        "unpriced-model"
      ]
    }
  }
}
```

Latency fields have the following meanings:

| Field | Description |
|---|---|
| `p50_ms` | Median end-to-end target latency, in milliseconds. The value can include fractional milliseconds. |
| `p95_ms` | 95th-percentile end-to-end target latency, in milliseconds. The value can include fractional milliseconds. |
| `sample_count` | Number of evaluation rows that contributed a usable target latency measurement. |

Estimated cost fields have the following meanings:

| Field | Description |
|---|---|
| `estimated_cost` | Total estimated inference cost for the target models that the service could price. |
| `currency` | ISO 4217 currency code for the estimate. |
| `completeness` | `complete` when all attributed target models were priced, or `partial` when at least one model couldn't be priced. |
| `pricing_version` | Optional identifier for the price-list snapshot used for the estimate. |
| `model_costs` | Cost and token-usage breakdown for each priced target model. |
| `unpriced_models` | Optional list of target models for which no reliable price was available. |

Each entry in `model_costs` contains the backing `model_name`, its
`estimated_cost`, non-cached input `prompt_tokens`, `cached_tokens`, and output
`completion_tokens`. For a direct deployment, `model_name` is the backing model
resolved from deployment metadata. For a model-router target, the breakdown
identifies the models attributed by the runtime.

When `completeness` is `partial`, the top-level cost and `model_costs` include
only the models that the service could price. Check `unpriced_models` before
using the estimate to compare runs.

### Extract latency and estimated cost

After the evaluation run finishes and is available in `run`, convert the SDK
response to a dictionary and check the optional target latency:

# [Python](#tab/python)

```python
run_data = run.to_dict()

target_latency = (run_data.get("latency") or {}).get("target")
if not target_latency:
    print("Target latency wasn't reported.")
else:
    p50_ms = target_latency.get("p50_ms")
    p95_ms = target_latency.get("p95_ms")
    sample_count = target_latency.get("sample_count", 0)
    if p50_ms is None or p95_ms is None:
        print("Target latency percentiles weren't reported.")
    else:
        print(
            f"Target latency: p50={p50_ms:,.2f} ms, "
            f"p95={p95_ms:,.2f} ms ({sample_count:,} samples)"
        )
```

Check the estimated total for the target models that the service could price:

```python
run_data = run.to_dict()
target_cost = (run_data.get("estimated_cost") or {}).get("target")
if not target_cost:
    print("Estimated target cost wasn't reported.")
else:
    currency = target_cost.get("currency", "USD")
    estimated_cost = target_cost.get("estimated_cost", 0)
    completeness = target_cost.get("completeness", "unknown")
    print(
        f"Estimated target cost: {estimated_cost:.6f} {currency} "
        f"({completeness})"
    )
```

Use the model breakdown to review token attribution and find models that the
service couldn't price:

```python
run_data = run.to_dict()
target_cost = (run_data.get("estimated_cost") or {}).get("target")
if target_cost:
    currency = target_cost.get("currency", "USD")
    for model_cost in target_cost.get("model_costs") or []:
        prompt_tokens = model_cost.get("prompt_tokens", 0)
        cached_tokens = model_cost.get("cached_tokens", 0)
        completion_tokens = model_cost.get("completion_tokens", 0)
        total_tokens = prompt_tokens + cached_tokens + completion_tokens
        print(
            f"  {model_cost.get('model_name', 'unknown')}: "
            f"{model_cost.get('estimated_cost', 0):.6f} {currency}, "
            f"{total_tokens:,} tokens "
            f"({prompt_tokens:,} prompt, {cached_tokens:,} cached, "
            f"{completion_tokens:,} completion)"
        )

    unpriced_models = target_cost.get("unpriced_models") or []
    if unpriced_models:
        print(f"  Unpriced models: {', '.join(unpriced_models)}")
```

# [C#](#tab/csharp)

After the evaluation run finishes and is available in `evaluationRun`, parse
the protocol response and check the optional target latency:

```csharp
using JsonDocument runDocument = JsonDocument.Parse(
  evaluationRun.GetRawResponse().Content.ToMemory());
JsonElement runData = runDocument.RootElement;

if (!runData.TryGetProperty("latency", out JsonElement latency)
  || latency.ValueKind != JsonValueKind.Object
  || !latency.TryGetProperty("target", out JsonElement targetLatency)
  || targetLatency.ValueKind != JsonValueKind.Object
  || !targetLatency.EnumerateObject().MoveNext())
{
  Console.WriteLine("Target latency wasn't reported.");
}
else if (!targetLatency.TryGetProperty("p50_ms", out JsonElement p50)
  || !targetLatency.TryGetProperty("p95_ms", out JsonElement p95))
{
  Console.WriteLine("Target latency percentiles weren't reported.");
}
else
{
  long sampleCount = targetLatency.TryGetProperty(
    "sample_count", out JsonElement count)
      ? count.GetInt64()
      : 0;
  Console.WriteLine(
    $"Target latency: p50={p50.GetDouble():N2} ms, " +
    $"p95={p95.GetDouble():N2} ms ({sampleCount:N0} samples)");
}
```

Check the estimated total for the target models that the service could price:

```csharp
using JsonDocument runDocument = JsonDocument.Parse(
  evaluationRun.GetRawResponse().Content.ToMemory());
JsonElement runData = runDocument.RootElement;

if (!runData.TryGetProperty(
    "estimated_cost", out JsonElement estimatedCost)
  || estimatedCost.ValueKind != JsonValueKind.Object
  || !estimatedCost.TryGetProperty("target", out JsonElement targetCost)
  || targetCost.ValueKind != JsonValueKind.Object
  || !targetCost.EnumerateObject().MoveNext())
{
  Console.WriteLine("Estimated target cost wasn't reported.");
}
else
{
  string currency = targetCost.TryGetProperty(
    "currency", out JsonElement currencyElement)
      ? currencyElement.GetString() ?? "USD"
      : "USD";
  decimal cost = targetCost.TryGetProperty(
    "estimated_cost", out JsonElement costElement)
      ? costElement.GetDecimal()
      : 0;
  string completeness = targetCost.TryGetProperty(
    "completeness", out JsonElement completenessElement)
      ? completenessElement.GetString() ?? "unknown"
      : "unknown";
  Console.WriteLine(
    $"Estimated target cost: {cost:F6} {currency} ({completeness})");
}
```

Use the model breakdown to review token attribution and find models that the
service couldn't price:

```csharp
using JsonDocument runDocument = JsonDocument.Parse(
  evaluationRun.GetRawResponse().Content.ToMemory());
JsonElement runData = runDocument.RootElement;

if (runData.TryGetProperty("estimated_cost", out JsonElement estimatedCost)
  && estimatedCost.ValueKind == JsonValueKind.Object
  && estimatedCost.TryGetProperty("target", out JsonElement targetCost)
  && targetCost.ValueKind == JsonValueKind.Object)
{
  string currency = targetCost.TryGetProperty(
    "currency", out JsonElement currencyElement)
      ? currencyElement.GetString() ?? "USD"
      : "USD";

  if (targetCost.TryGetProperty(
      "model_costs", out JsonElement modelCosts)
    && modelCosts.ValueKind == JsonValueKind.Array)
  {
    foreach (JsonElement modelCost in modelCosts.EnumerateArray())
    {
      string modelName = modelCost.TryGetProperty(
        "model_name", out JsonElement modelNameElement)
          ? modelNameElement.GetString() ?? "unknown"
          : "unknown";
      decimal cost = modelCost.TryGetProperty(
        "estimated_cost", out JsonElement costElement)
          ? costElement.GetDecimal()
          : 0;
      long promptTokens = modelCost.TryGetProperty(
        "prompt_tokens", out JsonElement promptElement)
          ? promptElement.GetInt64()
          : 0;
      long cachedTokens = modelCost.TryGetProperty(
        "cached_tokens", out JsonElement cachedElement)
          ? cachedElement.GetInt64()
          : 0;
      long completionTokens = modelCost.TryGetProperty(
        "completion_tokens", out JsonElement completionElement)
          ? completionElement.GetInt64()
          : 0;
      long totalTokens = promptTokens + cachedTokens + completionTokens;

      Console.WriteLine(
        $"  {modelName}: {cost:F6} {currency}, {totalTokens:N0} tokens " +
        $"({promptTokens:N0} prompt, {cachedTokens:N0} cached, " +
        $"{completionTokens:N0} completion)");
    }
  }

  if (targetCost.TryGetProperty(
      "unpriced_models", out JsonElement unpricedModels)
    && unpricedModels.ValueKind == JsonValueKind.Array
    && unpricedModels.GetArrayLength() > 0)
  {
    List<string> names = new();
    foreach (JsonElement model in unpricedModels.EnumerateArray())
    {
      names.Add(model.GetString() ?? "unknown");
    }
    Console.WriteLine($"  Unpriced models: {string.Join(", ", names)}");
  }
}
```

# [JavaScript/TypeScript](#tab/javascript)

Use the Python or C# tab to extract target latency and estimated cost.

# [cURL](#tab/curl)

Use the Python or C# tab to extract target latency and estimated cost from the
completed run response.

---

For the example response, the output looks like:

```output
Target latency: p50=812.25 ms, p95=2,400.50 ms (47 samples)
Estimated target cost: 0.012346 USD (partial)
  gpt-5-mini: 0.012346 USD, 17,000 tokens (12,000 prompt, 2,000 cached, 3,000 completion)
  Unpriced models: unpriced-model
```

The top-level estimate is the sum of the entries in `model_costs`. If
`completeness` is `partial`, the output identifies the omitted models in
`unpriced_models`; don't treat the estimate as the full cost of the run.

> [!IMPORTANT]
> Target cost is an estimate based on reported token usage and published list
> prices. It excludes evaluator model usage and evaluation runtime costs, and it
> doesn't account for negotiated pricing, commitments, or discounts. Use Azure
> billing data for actual charges.

## Cancel a run

Cancel a run that you no longer need:

# [Python](#tab/python)

```python
openai_client.evals.runs.cancel(
    run_id=eval_run.id,
    eval_id=eval_object.id,
)
```

# [C#](#tab/csharp)

```csharp
await evaluationClient.CancelEvaluationRunAsync(
  evaluationId: evaluationId,
  evaluationRunId: runId,
  options: new());
```

Reference: [`EvaluationClient` protocol methods](https://github.com/openai/openai-dotnet/blob/main/OpenAI/src/Custom/Evals/EvaluationClient.Protocol.cs)

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate run cancellation. Use the Python or C# tab for this flow.

# [cURL](#tab/curl)

Use the Python or C# tab to cancel a run.

---

## Troubleshoot cloud evaluation

### Job running for a long time

Your evaluation job might stay in the **Running** state for a long time. This condition usually happens when the Azure OpenAI model deployment doesn't have enough capacity, so the service retries requests.

**Resolution:**

1. Cancel the current evaluation job by using `openai_client.evals.runs.cancel(run_id, eval_id=eval_id)`.
1. Increase the model capacity in the Azure portal.
1. Run the evaluation again.

### Authentication errors

If you get a `401 Unauthorized` or `403 Forbidden` error, check that:

- You configured your `DefaultAzureCredential` correctly. If you're using Azure CLI, run `az login`.
- Your account has the **Foundry User** role on the Foundry project.
- The project endpoint URL is correct and includes both the account and project names.

### Data format errors

If the evaluation fails with a schema or data mapping error:

- Verify your JSONL file has one valid JSON object per line.
- Confirm that field names in `data_mapping` match the field names in your JSONL file exactly (case-sensitive).
- Check that `item_schema` properties match the fields in your dataset.

### HTTP 400 error when you use file_id with agent response evaluations

Agent response evaluations (`azure_ai_responses`) support only inline data through `file_content`. If you provide response IDs by using `file_id`, the request returns a `400 Bad Request` error.

**Resolution:** Switch to `file_content` and provide the response IDs inline.

### Rate limit errors

Tenant, subscription, and project levels rate-limit evaluation run creations. If you receive a `429 Too Many Requests` response:

- Check the `retry-after` header in the response for the recommended wait time.
- Review the response body for rate limit details.
- Use exponential backoff when retrying failed requests.

If an evaluation job fails with a `429` error during execution:

- Reduce the size of your evaluation dataset or split it into smaller batches.
- Increase the tokens-per-minute (TPM) quota for your model deployment in the Azure portal.

### Agent evaluator tool errors

If an agent evaluator returns an error for unsupported tools:

- Check the [supported tools](../../concepts/evaluation-evaluators/agent-evaluators.md#supported-tools) for agent evaluators.
- As a workaround, wrap unsupported tools as user-defined function tools so the evaluator can assess them.

## Related content

- [Use admin-connected models in cloud evaluations](evaluate-admin-connected-models.md)
- [Complete working samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations)
- [Complete .NET evaluation samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/samples/Evaluations)
- [Trace-based evaluation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_traces.py)
- [Set up tracing in Microsoft Foundry](../../observability/how-to/trace-agent-setup.md)
- [Set up continuous evaluation](../../observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation)
- [See evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Foundry](../../quickstarts/get-started-code.md)
- [REST API reference](https://ai.azure.com/api-reference)
