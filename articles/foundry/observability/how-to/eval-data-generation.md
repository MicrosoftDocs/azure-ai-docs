---
title: Convert agent traces into evaluation datasets (Preview)
titleSuffix: Azure AI Foundry
description: Learn how to use the Data Generation API in Microsoft Foundry to turn production agent traces into evaluation and fine-tuning datasets.
author: ssalgadodev
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: how-to
ms.date: 05/22/2026
ms.author: ssalgado
ai-usage: ai-assisted
---

# Convert agent traces into evaluation datasets (Preview)

[!INCLUDE [preview-notice](includes/preview-notice.md)]

Production traces are the most representative source of how your agent behaves with real users. This article shows you how to use the Data Generation API in Microsoft Foundry to turn the traces your agent already emits into a curated, versioned dataset you can evaluate against, then run an evaluation on the result. When you select traces, Foundry uses intelligent sampling to auto-select a representative set, so you get a high-value dataset without manual cleanup.

Converting traces into a dataset closes the observability loop: the production behavior you capture through tracing becomes the test set you use to measure and improve quality. The same job can also produce fine-tuning data. For the fine-tuning path, see [Generate training and evaluation data from agent traces](../../fine-tuning/agent-traces.md).

> [!IMPORTANT]
> The Data Generation API is in public preview. APIs may change. You must opt in by setting `allow_preview=True` when you create the client.

## Intelligent sampling

When you select a time range of traces, the service doesn't just randomly sample from that window. A representative set is auto-selected using intelligent sampling, which curates a high-value set of traces from raw, noisy production data. You don't configure individual filter stages; the service handles selection for you. Intelligent sampling does the following:

- **Filters out uninteresting traces** such as single-character messages and other low-intent traffic that add no evaluation signal.
- **Selects a diverse, representative sample** using MinHash so the result covers the range of your agent's scenarios rather than over-indexing on frequent, near-identical prompts.
- **Handles sensitive content** including personally identifiable information (PII).
- **Optionally applies an LLM quality pass** that scores traces for difficulty and realism. This is off by default because it incurs model cost; enable it when you want a higher-signal set. See [Control quality with the LLM grading option](#control-quality-with-the-llm-grading-option).

This matters because evaluations are expensive and most raw traces add little signal. Recent research shows that careful selection can reach the same evaluation quality with a small fraction of the original traces, so a representative set produces better signal at lower cost than evaluating everything. Intelligent sampling is the mechanism that makes trace selection practical at production scale, and it's a capability competitors don't offer out of the box.

Intelligent sampling powers trace selection in three places in Foundry, each reached by toggling **Intelligent sampling** (on by default) when you pick a time range:

- **Creating an evaluation** — when you evaluate against existing traces, a representative set within your time range is auto-selected.
- **Creating a dataset from traces** — covered in this article.
- **Generating a custom evaluator rubric** — when you use production traces as context, the best traces are auto-selected to ground the generated rubric.

## When to use each source

The Data Generation API accepts several sources. Use the table below to pick the right one for your goal.

| Goal | Source to use |
|------|---------------|
| Build an evaluation set from real production behavior | **Traces** — your agent's conversations from Application Insights |
| Generate Q&A pairs from a policy document or knowledge base | **Prompt** — paste in the text |
| Bootstrap a starter dataset from an agent's instructions before it has traffic | **Agent** — point at a deployed agent by name |
| Reuse data you've already uploaded | **File** or **Dataset** |

## Prerequisites

- Python SDK version `2.2.0` or later: `pip install "azure-ai-projects>=2.2.0" azure-identity` (SDK path only)
- A Microsoft Foundry project endpoint URL in the format `https://<your-resource>.services.ai.azure.com/api/projects/<your-project>`
- Azure AI Project Contributor role or higher on the project
- Application Insights attached to your project. Configure this in the portal under **Project settings** > **Telemetry**.
- A deployed agent that emits traces. Foundry agents emit traces automatically; OpenTelemetry-instrumented third-party agents are also supported.

## Generate an evaluation dataset from traces (portal)

You can create a dataset from traces directly in the portal without writing code. This is the quickest way to turn recent production traffic into an evaluation set.

1. In the portal, open the **Data** tab and select **Create dataset from traces**.

   <!-- TODO: screenshot — Data tab with "Create dataset from traces" entry point -->
   :::image type="content" source="media/trace-to-dataset/create-dataset-entry.png" alt-text="Screenshot of the Data tab showing the option to create a dataset from traces.":::

2. Configure the dataset:

   - **Agent** — select the deployed agent whose traces you want to use.
   - **Date range** — choose the window to pull traces from, such as the last day or last 7 days.
   - **Maximum number of samples** — set the cap on rows in the dataset. The default is a manageable starting point; increase or decrease it to fit your needs.
   - **Intelligent sampling** — leave this on (the default) so a representative set is auto-selected from the window. See [Intelligent sampling](#intelligent-sampling). Turn on LLM grading only if you want the additional quality pass, which incurs model cost.

   <!-- TODO: screenshot — Create dataset from traces dialog with agent, date range, max samples, and intelligent sampling toggle -->
   :::image type="content" source="media/trace-to-dataset/create-dataset-dialog.png" alt-text="Screenshot of the create dataset from traces dialog showing agent selection, date range, maximum samples, and the intelligent sampling toggle.":::

3. Submit the job. Dataset generation runs as a background job; you can track its status on the **Data** tab.

4. When the job finishes, select the dataset to preview the generated rows, including the description, query, and response for each. From here you can download or delete the dataset.

   <!-- TODO: screenshot — generated dataset preview showing description, query, response columns -->
   :::image type="content" source="media/trace-to-dataset/dataset-preview.png" alt-text="Screenshot of the generated dataset preview with description, query, and response columns.":::

5. Use the dataset. Finished generation jobs link directly to the next step: evaluation jobs link to starting an evaluation run, and fine-tuning jobs link to starting a fine-tuning job.

> [!TIP]
> No traces yet? If your agent is new and hasn't generated production traffic, generate a synthetic starter dataset instead. In the **Data** tab, choose to generate from the agent's prompt, description, or an uploaded file to get started, then switch to traces once your agent is running.

## Generate an evaluation dataset from traces (SDK)

Drive your deployed agent with realistic traffic, then use those conversations to build an evaluation dataset. The flow is: define a time window, point at your agent, set a cap on rows, and submit the job.

First, create an `AIProjectClient` using your project endpoint and `DefaultAzureCredential`. All data generation operations are available under `project_client.beta.datasets`.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(
    endpoint="https://<your-resource>.services.ai.azure.com/api/projects/<your-project>",
    credential=DefaultAzureCredential(),
    allow_preview=True,    # required while the API is in preview
)
```

> [!NOTE]
> Application Insights takes 30–90 seconds to ingest spans. If you submit the job too quickly after capturing traffic, the job runs against an empty window and produces no samples.

```python
import time
from datetime import datetime, timedelta, timezone
from azure.ai.projects.models import (
    DataGenerationJob,
    DataGenerationJobInputs,
    DataGenerationJobScenario,
    DataGenerationJobOutputType,
    JobStatus,
    TracesDataGenerationJobOptions,
    TracesDataGenerationJobSource,
)

AGENT_NAME = "retail-agent-langgraph"

# 1. Record the window around your traffic.
window_start = datetime.now(timezone.utc) - timedelta(days=7)
window_end = datetime.now(timezone.utc)

# 2. Define the job. Note the EVALUATION scenario.
job_request = DataGenerationJob(
    inputs=DataGenerationJobInputs(
        name="retail-agent-eval-set",
        scenario=DataGenerationJobScenario.EVALUATION,
        sources=[
            TracesDataGenerationJobSource(
                agent_name=AGENT_NAME,
                start_time=window_start,
                end_time=window_end,
                # agent_version="3",   # pin to a specific version (recommended)
            )
        ],
        options=TracesDataGenerationJobOptions(
            max_samples=100,    # cap on rows in the dataset
        ),
    ),
)

# 3. Submit and poll until complete.
job = project_client.beta.datasets.create_generation_job(job_request)
print(f"Submitted {job.id}")

while job.status not in (JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELLED):
    time.sleep(10)
    job = project_client.beta.datasets.get_generation_job(job.id)
    print(f"  status: {job.status}")

if job.status != JobStatus.SUCCEEDED:
    raise RuntimeError(f"Job ended in {job.status}: {job.error}")

print(f"Generated {job.result.generated_samples} samples")
```

The job produces a versioned dataset registered in your project. The number of rows is capped by `max_samples` but may be lower if the window doesn't contain enough distinct, high-quality traces after intelligent sampling.

> [!TIP]
> No traces yet? If your agent is new and hasn't generated production traffic, use a cold-start source instead. Point the job at the agent's instructions (`AgentDataGenerationJobSource`) or paste a document or spec (`PromptDataGenerationJobSource`) to generate a synthetic starter dataset, then switch to traces once your agent is running. See [Choose a data source](#choose-a-data-source).

Whether you created the dataset from the portal or the SDK, you can preview it on the **Data** tab to inspect the generated rows before evaluating, and download or delete it from there.

## Run an evaluation against the generated dataset

Once the dataset exists, evaluate your agent against it. The generated dataset uses the standard query-response schema, so it works directly with the evaluation APIs.

```python
from azure.ai.projects.models import DatasetDataGenerationJobSource

# The generation job output includes the dataset name and version.
dataset_name = job.result.outputs[0].dataset_name
dataset_version = job.result.outputs[0].dataset_version

print(f"Evaluate against {dataset_name} v{dataset_version}")
# Pass dataset_name and dataset_version to your evaluation run.
# See the evaluation how-to for running evaluators against a dataset.
```

For the full evaluation flow, including selecting evaluators and reviewing results, see [Run evaluations in Microsoft Foundry](../../how-to/develop/evaluate-sdk.md).

## Generate a dataset and evaluator together from the command line

If you work code-first, the `azd eval init` command generates both a test dataset and a custom evaluator for your agent in a single step. It reads your agent's instructions, optionally pulls in production traces, and produces a dataset plus a rubric-based evaluator tailored to your agent's scenario.

1. From your agent's project directory, run:

   ```azdeveloper
   azd eval init
   ```

2. Answer the interactive prompts. The command reads your agent's `instruction.md` automatically; press Enter to accept the detected values.

   ```output
   ? Name for the generated assets: travel-approval-eval
   ? Use production traces to generate the evaluator? Yes
   ? Trace time range: Last day
   ? Number of data samples to generate: 15
   ```

   | Prompt | What it controls |
   |--------|------------------|
   | Name | Identifier for the generated dataset and evaluator. |
   | Use production traces | Grounds the evaluator in real agent behavior. When enabled, the best traces in your window are auto-selected using [intelligent sampling](#intelligent-sampling). |
   | Trace time range | The window to sample traces from, such as the last day. |
   | Number of samples | How many rows to generate for the dataset. |

3. Wait for the job to finish. It typically completes in about two minutes and prints links to the generated assets:

   ```output
   Generated dataset:    travel-approval-eval (15 rows)   -> view in portal
   Generated evaluator:  travel-approval-eval.rubric.yaml -> view in portal
   ```

4. Review the generated assets:

   - **Dataset** — 15 rows with description, query, and response columns.
   - **Evaluator** — a custom rubric for your agent. The rubric lists the dimensions that matter for your scenario, each with guidance and a weight. Because it's generated from your agent's context, the dimensions reflect what's important for your specific app rather than a generic metric set.

5. Adjust the rubric before evaluating, if needed. Edit dimension weights, descriptions, or guidance directly in the generated YAML:

   ```yaml
   dimensions:
     - name: policy_adherence
       guidance: Does the response respect the travel budget and approval policy?
       weight: 0.4
     - name: completeness
       guidance: Does the response address all parts of the request?
       weight: 0.3
     - name: clarity
       guidance: Is the recommendation clear and actionable?
       weight: 0.3
   ```

   Or use the same human-in-the-loop review experience in the portal, where you can view the rubric, regenerate it if your agent definition changed, and add or update dimensions. This review step is what differentiates Foundry's adaptive rubrics from auto-only approaches.

6. Run the evaluation:

   ```azdeveloper
   azd eval run
   ```

   The run finishes in a few minutes and links back to the portal. There, the custom evaluator score appears alongside built-in scores, with an overall score, an explanation of why the score was given, and a per-dimension breakdown so you can see what to fix.

## Control quality with the LLM grading option

By default, intelligent sampling uses rule-based quality filtering and deduplication, which are fast and incur no model cost. To apply an additional LLM-based quality pass that scores traces for difficulty and realism, set a grading model in the job options. This produces a higher-signal dataset at the cost of additional model calls.

```python
from azure.ai.projects.models import DataGenerationModelOptions

options = TracesDataGenerationJobOptions(
    max_samples=100,
    model_options=DataGenerationModelOptions(model="gpt-4.1-mini"),   # enables LLM grading
)
```

Leave `model_options` unset to skip the LLM pass and rely on rule-based filtering and deduplication only.

## Choose a data source

| Source class | What it uses | Required field |
|---|---|---|
| `TracesDataGenerationJobSource` | Real conversations from your deployed agent in Application Insights | `agent_name` (pin `agent_version` for stability) |
| `PromptDataGenerationJobSource` | Inline text such as a document or agent description | `prompt` |
| `AgentDataGenerationJobSource` | An agent's instructions and metadata (no traces required) | `agent_name` |
| `FileDataGenerationJobSource` | An Azure OpenAI file you've already uploaded | `id` |
| `DatasetDataGenerationJobSource` | An existing Foundry dataset | `name` |

## Configure output options

| Options class | What it produces |
|---|---|
| `TracesDataGenerationJobOptions` | Multi-turn conversations assembled from spans (system → user → tool calls → assistant) |
| `SimpleQnADataGenerationJobOptions` | Single-turn Q&A pairs |
| `ToolUseFineTuningDataGenerationJobOptions` | Tool-calling conversations (fine-tuning only) |

All options accept the following fields.

| Field | Description |
|-------|-------------|
| `max_samples` | Hard cap on output rows. The actual count may be lower if the source doesn't contain enough data after intelligent sampling. |
| `train_split` | Splits output into training and validation files. Used for fine-tuning; not typically needed for evaluation datasets. |
| `model_options` | Selects the model used for the optional LLM grading pass. Omit to skip LLM grading. |

## Manage data generation jobs

```python
from azure.ai.projects.models import DataGenerationJobScenario

# List recent evaluation jobs.
for job in project_client.beta.datasets.list_generation_jobs(
    limit=20,
    order="desc",
    scenario=DataGenerationJobScenario.EVALUATION,
):
    print(f"{job.id}  {job.status:<12}  {job.inputs.name}")

# Cancel a running job.
project_client.beta.datasets.cancel_generation_job(job_id="job_...")

# Delete a job record (produced datasets are not deleted).
project_client.beta.datasets.delete_generation_job(job_id="job_...")
```

## Best practices

- **Wait before submitting trace jobs.** Application Insights takes 30–90 seconds to ingest spans. Submitting too quickly results in an empty window and zero samples.
- **Pin `agent_version` for trace jobs.** Without it, the job mixes spans from every active version, which can include stale behavior and weaken your evaluation signal.
- **Check `generated_samples` after every job.** `max_samples` is a ceiling, not a guarantee. Intelligent sampling removes duplicates and low-quality traces, so you can get fewer rows than the cap.
- **Start without LLM grading, then add it if you need more signal.** Rule-based filtering and deduplication are free and fast. Enable `model_options` only when you want the additional difficulty and realism pass.
- **Use a representative time window.** A seven-day window usually captures enough variety. Narrow windows around a known incident are useful for building targeted regression sets.

## Related content

- [Agent tracing in Microsoft Foundry](../concepts/trace-agent-concept.md)
- [Generate training and evaluation data from agent traces](../../fine-tuning/agent-traces.md)
- [Run evaluations in Microsoft Foundry](../../how-to/develop/evaluate-sdk.md)
- [Sample notebook: data generation jobs](../../samples/datasets/sample_beta_datasets_generation_jobs.ipynb)