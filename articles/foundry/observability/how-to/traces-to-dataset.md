---
title: Convert agent traces into evaluation datasets
description: Learn how to use data generation in Microsoft Foundry to turn production agent traces into evaluation datasets.
ms.service: microsoft-foundry
ms.subservice: foundry-observability
author: lgayhardt
ms.author: lagayhar
ms.reviewer: ychen
ms.topic: how-to
ms.date: 10/08/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---
# Convert agent traces into evaluation datasets

This article covers trace-based dataset generation. For all dataset preparation
options and the standard field names, see
[Evaluation datasets in Microsoft Foundry](evaluation-datasets.md) and
[Evaluation dataset schema](evaluation-dataset-schema.md).

Production traces are the most representative source of how your agent behaves
with real users. This article shows you how to use data generation in Microsoft
Foundry to turn the traces your agent already emits into a curated, versioned
dataset you can evaluate against. Set `max_samples` to use intelligent sampling
to select a representative subset, omit it to process matching traces without
sampling, or provide specific trace IDs.

Converting traces into a dataset closes the agent improvement loop: the production behavior you capture through tracing becomes the test set you use to measure and improve quality.

Trace-based and synthetic generation are complementary: production traces reflect real user behavior, while synthetic generation covers prelaunch scenarios and edge cases. If your agent doesn't have production traces yet, or you want to extend coverage beyond what production traffic exercises, see [Generate a synthetic evaluation dataset](evaluation-dataset-synthetic.md).

## Intelligent sampling

When you set `max_samples`, the service doesn't just randomly sample from the
selected window. It autoselects a representative subset by using intelligent
sampling. You don't configure individual filter stages; the service handles
selection for you. Intelligent sampling does the following tasks:

- **Filters out uninteresting traces** such as single-character messages and other low-intent traffic that add no evaluation signal.
- **Selects a diverse, representative sample** by using MinHash so the result covers the range of your agent's scenarios rather than overindexing on frequent, near-identical prompts.

This process matters because evaluations are expensive and most raw traces add little signal. A representative set produces better signal at lower cost than evaluating everything. Intelligent sampling makes trace selection practical at production scale, so you get evaluation-ready datasets without writing custom filtering or deduplication code.

Intelligent sampling uses the same trace-selection algorithm across three experiences in Foundry:

- **Creating a dataset from traces** - covered in this article.
- **Creating a trace-based evaluation** - evaluate against existing traces with a representative sample from the selected time range.
- **Generating a rubric evaluator from production traces** - the same sampling algorithm selects traces used as input.

Set `max_samples` from 1 through 1,000 to cap the generated dataset. Omit
`max_samples` to turn off sampling. To select specific traces, provide a
nonempty list of nonblank trace IDs in `trace_ids` on the trace source.

Private-content redaction is separate from sampling. By default, the service
redacts private content from traces. Set `redact_private_content` to `false`
only when your privacy, retention, and dataset-access requirements allow the
generated dataset to retain that content.

## Prerequisites

- Python SDK version `2.8.0` or later: `pip install "azure-ai-projects>=2.8.0" azure-identity` (SDK path only)
- JavaScript SDK version `2.8.0` or later: `npm install "@azure/ai-projects@^2.8.0" @azure/identity`
- A Microsoft Foundry project endpoint URL in the format `https://<your-resource>.services.ai.azure.com/api/projects/<your-project>`
- Foundry User role or higher on the project.
- Set up tracing for a deployed agent that emits traces. Foundry agents emit traces automatically, and OpenTelemetry-instrumented third-party agents are also supported. For setup steps, see [Set up tracing for your agent](trace-agent-setup.md).
- The project's managed identity must have the [Reader role](/azure/role-based-access-control/built-in-roles/general#reader) on the connected Application Insights resource so the service can query trace data. If the tables that store your traces are [protected](/azure/azure-monitor/logs/protected-tables-configure), also assign the [Privileged Monitoring Data Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader) role.
- For all trace-based evaluation role requirements, see [Set up permissions for evaluation workflows](evaluation-permissions.md#add-permissions-for-trace-based-workflows).
- A supported region. For the list, see [Supported regions for data generation](../../concepts/evaluation-regions-limits-virtual-network.md#supported-regions-for-data-generation).

## Generate an evaluation dataset from traces (portal)

You can create a dataset from traces directly in the portal without writing code. This method is the quickest way to turn recent production traffic into an evaluation dataset.

1. In the portal, open the **Data Generation** tab. Select **Create dataset** > **From traces**.

1. In the **Create from traces** dialog, configure the dataset:

    - **Agent**: Select the deployed agent whose traces you want to use.
    - **Dataset**: Select an existing dataset or create a dataset.
    - **Create dataset for**: Set to **Evaluation**.
    - **Date range**: Choose the window to pull traces from, such as the last day or last seven days.
    - **Sampling**: Enable sampling to select a representative subset of matching traces.
    - **Maximum samples**: When sampling is enabled, set a cap from 1 through 1,000 rows.

1. Select **Create** to submit the job. Dataset generation runs as a background job. You can track its status on the **Data Generation** tab.

1. When the job finishes, go to the **Data** tab and select the dataset to preview the generated rows, including the description, query, and response for each. From there you can download or delete the dataset.

1. Use the dataset. Finished evaluation data generation jobs link directly to starting an evaluation run.

## Manually add traces to a dataset (portal)

To curate specific agent interactions, select traces from the traces table and add them to a new or existing dataset.

1. In the Foundry portal, open your project and agent, and then select **Traces/Trace view**.
1. In the traces table, use the available filters to narrow the trace list and select the traces that you want to add.
1. Select **Add to dataset**.
1. Choose whether to create a new dataset or add the traces to an existing dataset:

    - For a new dataset, enter the required dataset details.
    - For an existing dataset, select the dataset that you want to update.

1. Review and select **Create** to add the traces.
1. When the dataset is ready, a dataset creation notification appears. Select the dataset link in the notification to open the dataset and view the added rows.

## Generate an evaluation dataset from traces (SDK)

Drive your deployed agent with realistic traffic, and then use those
conversations to build an evaluation dataset. Define a time window or explicit
trace IDs, point at your agent, configure sampling and private-content
redaction, choose how to write the output dataset, and submit the job.

First, create an `AIProjectClient` by using your project endpoint and
`DefaultAzureCredential`. You can find all data generation operations under
`project_client.datasets`.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

credential = DefaultAzureCredential()
project_client = AIProjectClient(
    endpoint="https://<your-resource>.services.ai.azure.com/api/projects/<your-project>",
    credential=credential,
)
```

# [JavaScript/TypeScript](#tab/javascript)

```bash
npm install "@azure/ai-projects@^2.8.0" @azure/identity
```

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const projectEndpoint =
  "https://<your-resource>.services.ai.azure.com/api/projects/<your-project>";
const projectClient = new AIProjectClient(
  projectEndpoint,
  new DefaultAzureCredential(),
);
```

Use `@azure/ai-projects` 2.8.0 or later. Access data generation operations through `projectClient.datasets`.

The following examples submit the same time-window trace source in Python and
JavaScript/TypeScript.

Reference: [AIProjectClient class](/javascript/api/@azure/ai-projects/aiprojectclient)

---

> [!NOTE]
> Application Insights takes 30–90 seconds to ingest spans. If you submit the job too quickly after capturing traffic, the job runs against an empty window and produces no samples.

# [Python](#tab/python)

```python
import time
from datetime import datetime, timedelta, timezone

from azure.ai.projects.models import (
    DataGenerationJobOutputWriteMode,
    DatasetDataGenerationJobOutput,
    EvaluationDataGenerationJobInputs,
    EvaluationDataGenerationJobOutputConfiguration,
    TracesDataGenerationJobConfiguration,
    TracesDataGenerationJobSource,
)

AGENT_NAME = "retail-agent"
poll_interval_seconds = 10

# 1. Record the window around your traffic.
end_time = datetime.now(tz=timezone.utc)
start_time = end_time - timedelta(days=7)

# 2. Define an evaluation job. The class sets scenario="evaluation".
job = EvaluationDataGenerationJobInputs(
    name="retail-agent-eval-set",
    sources=[
        TracesDataGenerationJobSource(
            description=(
                "Application Insights conversation traces for the Foundry "
                "agent."
            ),
            agent_name=AGENT_NAME,
            start_time=start_time,
            end_time=end_time,
            # agent_version="3",  # Pin to a specific version.
            # trace_ids=["trace-id-1", "trace-id-2"],  # Select exact traces.
        ),
    ],
    generation_configuration=TracesDataGenerationJobConfiguration(
        # Omit max_samples to turn off intelligent sampling.
        max_samples=100,
        # Private content is redacted by default.
        redact_private_content=True,
    ),
    output_configuration=EvaluationDataGenerationJobOutputConfiguration(
        name="retail-agent-eval-set",
        description="Representative production traces for agent evaluation.",
        tags={"source": "production-traces"},
        write_mode=DataGenerationJobOutputWriteMode.OVERWRITE,
    ),
)

# 3. Submit and wait for completion.
poller = project_client.datasets.begin_create_generation_job(job=job)
while not poller.done():
    print(f"\tstatus=`{poller.status()}`")
    time.sleep(poll_interval_seconds)
result = poller.result()

# 4. Resolve the generated dataset.
output_name = ""
output_version = ""
for output in (result.outputs if result is not None else None) or []:
    if isinstance(output, DatasetDataGenerationJobOutput):
        output_name = output.name or ""
        output_version = output.version or ""
        break

if not output_name or not output_version:
    raise RuntimeError("The data generation job didn't return a dataset output.")

dataset = project_client.datasets.get(name=output_name, version=output_version)
print(f"Generated dataset: {dataset.name} v{dataset.version} (id: {dataset.id})")
if result is not None and result.generated_samples is not None:
    print(f"Generated samples: {result.generated_samples}")
```

# [JavaScript/TypeScript](#tab/javascript)

```javascript
const agentName = "retail-agent";
const jobName = "retail-agent-eval-set";

// 1. Record the window around your traffic.
const endTime = new Date();
endTime.setMilliseconds(0);
const startTime = new Date(endTime.getTime() - 7 * 24 * 60 * 60 * 1000);

// 2. Define and submit the evaluation job.
const generationPoller = projectClient.datasets.createGenerationJob({
  name: jobName,
  scenario: "evaluation",
  sources: [
    {
      type: "traces",
      description:
        "Application Insights conversation traces for the Foundry agent.",
      agent_name: agentName,
      start_time: startTime,
      end_time: endTime,
      // agent_version: "3", // Pin to a specific version.
      // trace_ids: ["trace-id-1", "trace-id-2"], // Select exact traces.
    },
  ],
  generation_configuration: {
    type: "traces",
    // Omit max_samples to turn off intelligent sampling.
    max_samples: 100,
    // Private content is redacted by default.
    redact_private_content: true,
  },
  output_configuration: {
    name: jobName,
    description: "Representative production traces for agent evaluation.",
    tags: { source: "production-traces" },
    write_mode: "overwrite",
  },
});

await generationPoller.submitted();
const result = await generationPoller.pollUntilDone();

// 3. Resolve the generated dataset.
const datasetOutput = result.outputs?.find((output) => output.type === "dataset");
if (
  !datasetOutput ||
  !("name" in datasetOutput) ||
  !("version" in datasetOutput) ||
  !datasetOutput.name ||
  !datasetOutput.version
) {
  throw new Error("The data generation job didn't return a dataset output.");
}

const dataset = await projectClient.datasets.get(
  datasetOutput.name,
  datasetOutput.version,
);
console.log(
  `Generated dataset: ${dataset.name} v${dataset.version} (id: ${dataset.id})`,
);
if (result.generated_samples !== undefined) {
  console.log(`Generated samples: ${result.generated_samples}`);
}
```

---

The job produces a versioned dataset registered in your project. When you set
`max_samples`, the number of rows is capped by that value but might be lower if
the window doesn't contain enough distinct, high-quality traces after
intelligent sampling.

The default write mode is Python
`DataGenerationJobOutputWriteMode.OVERWRITE` or JavaScript/TypeScript
`"overwrite"`, which creates the next dataset version using only the newly
generated rows. To combine the new rows with the latest existing dataset
version and deduplicate trace rows, set `write_mode` to Python
`DataGenerationJobOutputWriteMode.MERGE` or JavaScript/TypeScript `"merge"`.
Neither mode modifies an existing dataset version in place.

Whether you created the dataset from the portal or the SDK, you can preview it on the **Data** tab to inspect the generated rows before evaluating. You can also download or delete it from there.

## Run an evaluation against the generated dataset

After the dataset exists, evaluate your agent against it. The generated dataset uses the standard query-response schema, so it works directly with the evaluation APIs. Pass the dataset's `name` and `version` (or its `id`) to your evaluation run.

For the full evaluation flow, including selecting evaluators and reviewing results, see [Evaluate an agent target](cloud-evaluation-targets.md#evaluate-an-agent-target). For a complete runnable example that generates an evaluation dataset from traces, see [sample_dataset_generation_job_traces_for_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/datasets/sample_dataset_generation_job_traces_for_evaluation.py) on GitHub.

## Manage data generation jobs

Use `project_client.datasets` APIs to list, inspect, cancel, and delete data
generation jobs.

# [Python](#tab/python)

```python
# List recent evaluation jobs.
for job in project_client.datasets.list_generation_jobs(
    limit=20,
    order="desc",
):
    if job.scenario == "evaluation":
        print(f"{job.id}  {job.status:<12}  {job.name}")

# Get a job.
job = project_client.datasets.get_generation_job(job_id="job_...")

# Cancel a running job.
project_client.datasets.cancel_generation_job(job_id="job_...")

# Delete a job record.
project_client.datasets.delete_generation_job(job_id="job_...")
```

# [JavaScript/TypeScript](#tab/javascript)

```javascript
// List recent evaluation jobs.
for await (const job of projectClient.datasets.listGenerationJobs({
  limit: 20,
})) {
  if (job.scenario === "evaluation") {
    console.log(`${job.id}  ${job.status}  ${job.scenario}  ${job.name}`);
  }
}

// Get a job.
const job = await projectClient.datasets.getGenerationJob("job_...");

// Cancel a running job.
await projectClient.datasets.cancelGenerationJob("job_...");

// Delete a job record.
await projectClient.datasets.deleteGenerationJob("job_...");
```

Reference: [datasets.listGenerationJobs](/javascript/api/@azure/ai-projects/aiprojectclient)

---

## Limitations

- The Application Insights resource connected to your Foundry project must allow public network access so the service can query Application Insights data. If Application Insights is behind an Azure Monitor Private Link Scope, make sure public network query access is enabled.
- If your Foundry project is connected to your own storage account, public network access must be enabled on that storage account for successful dataset creation.

## Best practices

- **Pin `agent_version` for trace jobs.** Without it, the job mixes spans from every active version, which can include stale behavior and weaken your evaluation signal.
- **Check `generated_samples` after sampled jobs.** When you set `max_samples`, it is a ceiling, not a guarantee. Intelligent sampling removes duplicates and low-quality traces, so you can get fewer rows than the cap.
- **Use a representative time window.** A seven-day window usually captures enough variety. Narrow windows around a known incident are useful for building targeted regression sets.

## Related content

- [Generate a synthetic evaluation dataset](evaluation-dataset-synthetic.md)—bootstrap an evaluation dataset without production traces.
- [Agent tracing in Microsoft Foundry](../concepts/trace-agent-concept.md)
- [Run cloud evaluations](cloud-evaluation.md)
- [Trace-to-dataset generation sample (Python)](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/datasets/sample_dataset_generation_job_traces_for_evaluation.py)
- [Evaluate deployed conversations from traces (preview)](cloud-evaluation-deployed-conversations.md)
