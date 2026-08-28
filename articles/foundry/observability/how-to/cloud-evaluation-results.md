---
title: "Get cloud evaluation results with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to poll cloud evaluation runs, interpret item and aggregate results, cancel runs, and troubleshoot errors."
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
# customer intent: As a developer, I want to retrieve and interpret cloud evaluation results so that I can diagnose failures and compare application quality.
---

# Get cloud evaluation results

Poll asynchronous evaluation runs, retrieve item and aggregate output, cancel runs, and resolve common evaluation errors.

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
    if run.status in ("completed", "failed"):
        break
    time.sleep(5)
    print("Waiting for eval run to complete...")

# Retrieve results
output_items = list(
    openai_client.evals.runs.output_items.list(
        run_id=run.id, eval_id=eval_object.id
    )
)
pprint(output_items)
print(f"Report URL: {run.report_url}")
```

# [JavaScript/TypeScript](#tab/javascript)

```javascript
let run = evalRun;
while (!["completed", "failed"].includes(run.status)) {
  run = await openaiClient.evals.runs.retrieve(run.id, {
    eval_id: evalObject.id,
  });
  console.log(`Waiting for eval run to complete... ${run.status}`);
  await new Promise((resolve) => setTimeout(resolve, 5000));
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

## Cancel a run

Cancel a run that you no longer need:

```python
openai_client.evals.runs.cancel(
    run_id=eval_run.id,
    eval_id=eval_object.id,
)
```

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
- [Trace-based evaluation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_traces.py)
- [Set up tracing in Microsoft Foundry](../../observability/how-to/trace-agent-setup.md)
- [Set up continuous evaluation](../../observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation)
- [See evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Foundry](../../quickstarts/get-started-code.md)
- [REST API reference](https://ai.azure.com/api-reference)
