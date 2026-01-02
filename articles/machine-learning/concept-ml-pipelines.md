---
title: 'What are machine learning pipelines?'
titleSuffix: Azure Machine Learning
description: Learn how machine learning pipelines help you build, optimize, and manage machine learning workflows.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: concept-article
ms.author: scottpolly
author: lgayhardt
ms.reviewer: jturuk
ms.date: 09/09/2025
monikerRange: 'azureml-api-2 || azureml-api-1'
---

# What are Azure Machine Learning pipelines?

:::moniker range="azureml-api-1"
[!INCLUDE [dev v1](includes/machine-learning-dev-v1.md)]

[!INCLUDE [v1 deprecation](includes/sdk-v1-deprecation.md)]

[!INCLUDE [cli v1 deprecation](./includes/machine-learning-cli-v1-deprecation.md)]
:::moniker-end
:::moniker range="azureml-api-2"
[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]
:::moniker-end



An Azure Machine Learning pipeline is a workflow that automates a complete machine learning task. It standardizes best practices, supports team collaboration, and improves efficiency.

## Why are Azure Machine Learning pipelines needed?


- [Standardizes machine learning operations (MLOps) and supports scalable team collaboration](#standardize-the-mlops-practice-and-support-scalable-team-collaboration)
- [Improves training efficiency and reduces cost](#training-efficiency-and-cost-reduction)

A pipeline breaks a machine learning task into steps. Each step is a manageable component that can be developed and automated separately. Azure Machine Learning manages dependencies between steps. This modular approach:
- Standardizes MLOps and supports team collaboration
- Improves training efficiency and reduces cost
- [Standardizes machine learning operations (MLOps) and supports scalable team collaboration](#standardize-the-mlops-practice-and-support-scalable-team-collaboration)
- [Improves training efficiency and reduces cost](#training-efficiency-and-cost-reduction)

### Standardize the MLOps practice and support scalable team collaboration



MLOps automates building and deploying models. Pipelines simplify this process by mapping each step to a specific task, so teams can work independently.



For example, a project may include data collection, preparation, training, evaluation, and deployment. Data engineers, scientists, and ML engineers each own their steps. Steps are best built as [components](concept-component.md), then integrated into a single workflow. Pipelines can be versioned, automated, and standardized by DevOps practices.

### Training efficiency and cost reduction



Pipelines also improve efficiency and reduce costs. They reuse outputs from unchanged steps and let you run each step on the best compute resource for the task.

## Getting started best practices



You can build a pipeline in several ways, depending on your starting point.



If you are new to pipelines, start by splitting existing code into steps, parameterizing inputs, and wrapping everything into a pipeline.



To scale, use pipeline templates for common problems. Teams fork a template, work on assigned steps, and update only their part as needed.



With reusable pipelines and components, teams can quickly create new workflows by cloning or combining existing pieces.

:::moniker range="azureml-api-2"


You can build pipelines using the [CLI](how-to-create-component-pipelines-cli.md), [Python SDK](how-to-create-component-pipeline-python.md), or [Designer UI](how-to-create-component-pipelines-ui.md).


:::moniker-end

<a name="compare"></a>
## Which Azure pipeline technology should I use?



Azure provides several types of pipelines for different purposes:

| Scenario | Primary persona | Azure offering | OSS offering | Canonical pipe | Strengths |
| -------- | --------------- | -------------- | ------------ | -------------- | --------- |
| Model orchestration (Machine learning) | Data scientist | Azure Machine Learning Pipelines | Kubeflow Pipelines | Data -> Model | Distribution, caching, code-first, reuse | 
| Data orchestration (Data prep) | Data engineer | [Azure Data Factory pipelines](/azure/data-factory/concepts-pipelines-activities) | Apache Airflow | Data -> Data | Strongly typed movement, data-centric activities |
| Code & app orchestration (CI/CD) | App Developer / Ops | [Azure Pipelines](https://azure.microsoft.com/services/devops/pipelines/) | Jenkins | Code + Model -> App/Service | Most open and flexible activity support, approval queues, phases with gating |

## Next steps



Azure Machine Learning pipelines add value from the start of development.

:::moniker range="azureml-api-2"
+ [Define pipelines with the Azure Machine Learning CLI v2](./how-to-create-component-pipelines-cli.md)
+ [Define pipelines with the Azure Machine Learning SDK v2](./how-to-create-component-pipeline-python.md)
+ [Define pipelines with Designer](./how-to-create-component-pipelines-ui.md)
+ Try out [CLI v2 pipeline example](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components)
+ Try out [Python SDK v2 pipeline example](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines)
+ Learn about [SDK and CLI v2 expressions](concept-expressions.md) that can be used in a pipeline.
:::moniker-end
:::moniker range="azureml-api-1"
+ [Create and run machine learning pipelines](v1/how-to-create-machine-learning-pipelines.md)
+ [Define pipelines with Designer](./how-to-create-component-pipelines-ui.md)
:::moniker-end
