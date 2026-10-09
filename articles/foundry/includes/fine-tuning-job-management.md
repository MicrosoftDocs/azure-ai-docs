---
title: Include file
description: Monitor, evaluate, and clean up managed fine-tuning jobs.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/25/2026
ms.custom: include
ai-usage: ai-assisted
---

## Monitor the job and select a checkpoint

Inspect training progress before choosing a model or checkpoint to deploy.

::: zone pivot="programming-language-studio"

In the portal, open the job details:

1. Check the **Status** and event logs. Jobs can queue before training starts; inspect error details if a job fails.
1. Open **Monitor** to compare training and validation metrics using the guidance above.
1. Open **Checkpoints** to inspect available model versions and their metrics. Compare candidates on held-out tasks before choosing one to deploy.

::: zone-end

::: zone pivot="programming-language-python"

### Inspect logs and checkpoints with Python

Use the Python `client` from your submission example. Replace `<JOB_ID>` with your job ID. Repeat the status check until the job finishes; don't resubmit a queued job.

Retrieve the status, event logs, available checkpoints, and result-file IDs:

```python
job = client.fine_tuning.jobs.retrieve("<JOB_ID>")
print("Status:", job.status)
print("Error:", job.error)
print("Model:", job.fine_tuned_model)
print("Result files:", job.result_files)

for event in client.fine_tuning.jobs.list_events(job.id).data:
    print(event.created_at, event.message)

checkpoints = client.fine_tuning.jobs.checkpoints.list(job.id)
print(checkpoints.model_dump_json(indent=2))
```

Reference: [Fine-tuning API](/rest/api/azureopenai/fine-tuning).

After completion, if the job returns a CSV metrics file, replace `<RESULT_FILE_ID>` with its ID and download it:

```python
with open("results.csv", "wb") as result_file:
    result_file.write(client.files.content("<RESULT_FILE_ID>").read())
```

Reference: [Files API](/rest/api/azureopenai/files).

::: zone-end

::: zone pivot="rest-api"

### Inspect logs and checkpoints with REST

Use the resource endpoint and key for REST. Replace `<JOB_ID>` with your job ID. Repeat the status check until the job finishes; don't resubmit a queued job.

Retrieve the job, event logs, and available checkpoints:

```bash
JOB_URL="$AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs/<JOB_ID>"
curl "$JOB_URL" -H "api-key: $AZURE_OPENAI_API_KEY"
curl "$JOB_URL/events" -H "api-key: $AZURE_OPENAI_API_KEY"
curl "$JOB_URL/checkpoints" -H "api-key: $AZURE_OPENAI_API_KEY"
```

Reference: [Fine-tuning API](/rest/api/azureopenai/fine-tuning).

After completion, inspect `result_files` in the job response. If it includes a CSV metrics file, replace `<RESULT_FILE_ID>` with its ID and download it:

```bash
curl "$AZURE_OPENAI_ENDPOINT/openai/v1/files/<RESULT_FILE_ID>/content" \
  -H "api-key: $AZURE_OPENAI_API_KEY" --output results.csv
```

Reference: [Files API](/rest/api/azureopenai/files).

::: zone-end

::: zone pivot="azd"

Use the [Azure Developer CLI job workflow](#use-the-azure-developer-cli) to inspect the job status.

::: zone-end

Checkpoints appear as training progresses; a queued job might have none. Inspect the returned checkpoint identifiers and metrics rather than assuming the latest version performs best.

When training succeeds, retain the trained model or your chosen checkpoint. Compare candidates on held-out tasks before selecting one for deployment.

## Deploy the model

Use the Foundry portal to deploy the model, regardless of how you submit the training job. Follow [Deploy fine-tuned models](../fine-tuning/deploy-fine-tuned-models.md) for your model's supported serving option and inference procedure.

::: zone pivot="programming-language-studio"

After deployment, use [Run evaluations from the Foundry portal](../how-to/evaluate-generative-ai-app.md) to compare candidates on held-out tasks.

::: zone-end

::: zone pivot="programming-language-python"

For SDK evaluation, see [Cloud evaluation with the Microsoft Foundry SDK](../observability/how-to/cloud-evaluation.md).

::: zone-end

## Stop training and clean up

::: zone pivot="programming-language-studio"

Cancel an unneeded job from its portal view. Delete uploaded files separately through the portal when you no longer need them.

::: zone-end

::: zone pivot="programming-language-python"

Cancel an unneeded job with `client.fine_tuning.jobs.cancel("<JOB_ID>")`. Delete unused uploaded files separately with `client.files.delete("<FILE_ID>")`.

Reference: [Job cancellation](/rest/api/azureopenai/fine-tuning/cancel) and [file deletion](/rest/api/azureopenai/files/delete).

::: zone-end

::: zone pivot="rest-api"

Cancel an unneeded job with the [fine-tuning cancellation API](/rest/api/azureopenai/fine-tuning/cancel). Delete unused uploaded files separately with the [Files API](/rest/api/azureopenai/files/delete).

::: zone-end

::: zone pivot="azd"

Cancel an unneeded job with the [CLI commands above](#pause-resume-or-cancel). For available cleanup operations, see the [fine-tuning CLI reference](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/cli/finetuning/README.md).

::: zone-end

Delete unused deployments with the [deployment cleanup procedure](../fine-tuning/deploy-fine-tuned-models.md#clean-up-your-deployment). Cancelling training doesn't delete deployments or stop their charges.

Retain any data and job records you need to reproduce the experiment.
