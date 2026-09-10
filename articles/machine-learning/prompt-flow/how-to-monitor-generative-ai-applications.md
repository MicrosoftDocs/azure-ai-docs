---
title: Monitor generative AI applications (preview)
titleSuffix: Azure Machine Learning
description: Learn how to monitor the safety and quality of generative AI applications deployed to Azure Machine Learning managed online endpoints.
services: machine-learning
author: s-polly
ms.author: lagayhar
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.reviewer: sooryar
reviewer: s-polly
ms.topic: how-to
ms.date: 08/31/2026
ai-usage: ai-assisted
ms.custom:
  - devplatv2
  - ignite-2023
  - doc-kit-assisted
ms.update-cycle: 365-days
---


# Monitor generative AI applications (preview)

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

Use Azure Machine Learning model monitoring to track the quality of an existing generative AI application deployed to a managed online endpoint. The monitor evaluates collected prompts and completions on a recurring schedule and displays metric trends and alerts in Azure Machine Learning studio.

Prompt Flow deployments on Azure Machine Learning managed online endpoints don't have a direct Microsoft Agent Framework equivalent. Review the [migration options](migrate-prompt-flow-to-agent-framework.md#managed-online-endpoints) before you change an existing deployment.

> [!IMPORTANT]
> Model monitoring for generative AI applications is currently in public preview. This preview is provided without a service-level agreement and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Prerequisites

- An Azure Machine Learning workspace.
- An Azure OpenAI resource with quota for an evaluator model deployment. Model availability changes over time. Review [Azure OpenAI model retirements and deprecations](../../foundry/openai/concepts/model-retirements.md) before you create the deployment.
- A user-assigned managed identity attached to the workspace. Grant the identity the least-privileged permissions required to access the workspace and the connected Azure OpenAI resource. To create role assignments, your identity needs the `Microsoft.Authorization/roleAssignments/write` permission at the required scope.
- An Azure OpenAI [workspace connection](get-started-prompt-flow.md#set-up-a-connection) that uses the managed identity. Keep this connection for as long as the monitor uses it.
- An existing prompt flow deployment on an Azure Machine Learning managed online endpoint. This procedure is intended for workloads that you maintain until you migrate from prompt flow.

## Prepare the deployment

Configure the deployed flow to collect the inputs and outputs required by the monitoring metrics:

1. [Create a compute session](how-to-manage-compute-session.md), and run your prompt flow.
1. [Deploy the flow to a managed online endpoint](how-to-deploy-for-real-time-inference.md).
1. Under **Basic settings**, enable **Inference data collection**.
1. Under **Advanced settings** > **Outputs & Connections**, select `completion` and any outputs required by the metrics that you plan to use, such as `context` or `ground_truth`.
1. Confirm that the collected input data contains a prompt column and that the collected output data contains a completion column. Record the exact column names for the monitor configuration.

> [!NOTE]
> If your compute instance is behind a VNet, see [Network isolation in prompt flow](how-to-secure-prompt-flow.md).

## Understand evaluation metrics

The monitor uses an Azure OpenAI model deployment as an evaluator. It applies evaluation instructions to the collected prompt, completion, and supporting data. For detailed metric definitions and interpretation guidance, see [Monitoring evaluation metrics descriptions and use cases](concept-model-monitoring-generative-ai-evaluation-metrics.md).

| Metric | Prompt | Completion | Context | Ground truth |
|---|---|---|---|---|
| Coherence | Required | Required | Not required | Not required |
| Fluency | Required | Required | Not required | Not required |
| Groundedness | Required | Required | Required | Not required |
| Relevance | Required | Required | Required | Not required |
| Similarity | Required | Required | Not required | Required |

## Create the monitor

Create a generation safety and quality signal from the data collected by your deployed flow:

1. In Azure Machine Learning studio, go to the monitoring overview for your workspace, and create a model monitor.
1. For the model task type, select **Prompt & completion**.
1. Select the input and output data assets created by Model Data Collector, and add a generation safety and quality monitoring signal.
1. Select the workspace connection for the Azure OpenAI evaluator resource, enter the evaluator deployment name, and map the prompt and completion columns. Map the context or ground-truth columns required by the metrics you select.
1. Keep the automatically generated join configuration unless your data assets use a custom identifier. Model Data Collector generates `correlationid` to correlate input and output records. Confirm the exact field name in each data asset before you customize the join.
1. Configure the available metric thresholds, sampling rate, schedule, and notification recipients. Then review the configuration, and create the monitor.

## Confirm the monitoring status

On the monitor overview, confirm that the scheduled monitoring pipeline job completes successfully. If the job fails, review its logs and verify the workspace connection, evaluator deployment, data assets, and mapped column names.

## Review monitoring results

Use the signal details to review metric trends and respond to alerts:

1. On the monitor overview, review the status and performance of each monitoring signal.
1. Open the generation safety and quality signal to view metric trends and score distributions.
1. Review alerts for metrics that don't meet the configured thresholds.
1. Adjust the thresholds or notification settings when your monitoring requirements change.

## Related content

- [Model monitoring with Azure Machine Learning](../concept-model-monitoring.md)
- [Collect production inference data](../how-to-collect-production-data.md)
- [Migrate prompt flow to Microsoft Agent Framework](migrate-prompt-flow-to-agent-framework.md)
