---
title: 'What are machine learning pipelines?'
titleSuffix: Azure Machine Learning
description: Learn how machine learning pipelines help you build, optimize, and manage machine learning workflows.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: concept-article
ms.author: lagayhar
author: lgayhardt
ms.reviewer: lagayhar
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


An Azure Machine Learning pipeline is an independently executable workflow for a complete machine learning task. It helps standardize best practices for building machine learning models, enables teams to work at scale, and improves model-building efficiency.

## Why are Azure Machine Learning pipelines needed?


The core of a machine learning pipeline is to break a complete machine learning task into a multistep workflow. Each step is a manageable component that can be developed, optimized, configured, and automated individually. Steps connect through well-defined interfaces. The Azure Machine Learning pipeline service automatically manages dependencies between steps. This modular approach brings two key benefits:
- [Standardizes machine learning operations (MLOps) and supports scalable team collaboration](#standardize-the-mlops-practice-and-support-scalable-team-collaboration)
- [Improves training efficiency and reduces cost](#training-efficiency-and-cost-reduction)

### Standardize the MLOps practice and support scalable team collaboration


Machine learning operations (MLOps) automate building and deploying machine learning models. This process is complex and usually requires collaboration among teams with different skills. A well-defined machine learning pipeline abstracts this complexity into a multistep workflow, mapping each step to a specific task so each team can work independently.  


For example, a typical machine learning project includes data collection, data preparation, model training, model evaluation, and model deployment. Data engineers focus on data steps, data scientists work on training and evaluation, and machine learning engineers handle deployment and workflow automation. With a machine learning pipeline, each team builds their own steps. The best way to build steps is by using an [Azure Machine Learning component (v2)](concept-component.md), a self-contained piece of code for one pipeline step. Steps from different users are integrated into one workflow through the pipeline definition. The pipeline serves as a collaboration tool for everyone in the project. Defining a pipeline and its steps can be standardized by each company's DevOps practices. The pipeline can also be versioned and automated. If ML projects are described as pipelines, best MLOps practices are already in place.  

### Training efficiency and cost reduction


In addition to supporting MLOps, machine learning pipelines improve training efficiency and reduce costs for large models. For example, training modern natural language models requires preprocessing large datasets and running GPU-intensive training. This process can take hours or days. Data scientists often test different code or hyperparameters and run training many times to optimize performance. Usually, only small changes occur between runs. Without pipelines, retraining from scratch wastes time and resources. Machine learning pipelines automatically detect unchanged steps and reuse outputs from previous runs. Pipelines also let you run each step on different compute resources—memory-heavy data processing on high-memory CPUs, and compute-intensive training on GPUs. By choosing the right resources for each step, you can significantly reduce training costs.

## Getting started best practices


Depending on your machine learning project's starting point, you can use several approaches to build a pipeline.


The first approach is for teams new to pipelines who want to benefit from MLOps. Data scientists may have developed models locally using their preferred tools. Machine learning engineers then take these outputs to production. This process involves cleaning up unnecessary code, changing training inputs from local data to parameterized values, splitting code into multiple steps, unit testing each step, and wrapping all steps into a pipeline.


Once teams are familiar with pipelines and want to scale, the second approach is to set up pipeline templates for specific machine learning problems. Templates define the pipeline structure, including steps, inputs, outputs, and connections. To start a new project, the team forks a template repository. The team leader assigns steps to members. Data scientists and engineers do their work, then structure their code to fit the predefined steps. Once code is checked in, the pipeline can be executed or automated. If changes are needed, each member only updates their part without affecting the rest of the pipeline.


After building a collection of pipelines and reusable components, teams can create new pipelines by cloning previous ones or combining existing components. At this stage, overall productivity improves significantly.  

:::moniker range="azureml-api-2"

Azure Machine Learning offers several ways to build a pipeline. If you are familiar with DevOps, use the [CLI](how-to-create-component-pipelines-cli.md). If you prefer Python, use the [Azure Machine Learning SDK v2](how-to-create-component-pipeline-python.md). If you prefer a UI, use the [designer to build pipelines with registered components](how-to-create-component-pipelines-ui.md).


:::moniker-end

<a name="compare"></a>
## Which Azure pipeline technology should I use?


Azure provides several types of pipelines, each with a different purpose. The following table lists the different pipelines and their uses:

| Scenario | Primary persona | Azure offering | OSS offering | Canonical pipe | Strengths |
| -------- | --------------- | -------------- | ------------ | -------------- | --------- |
| Model orchestration (Machine learning) | Data scientist | Azure Machine Learning Pipelines | Kubeflow Pipelines | Data -> Model | Distribution, caching, code-first, reuse | 
| Data orchestration (Data prep) | Data engineer | [Azure Data Factory pipelines](/azure/data-factory/concepts-pipelines-activities) | Apache Airflow | Data -> Data | Strongly typed movement, data-centric activities |
| Code & app orchestration (CI/CD) | App Developer / Ops | [Azure Pipelines](https://azure.microsoft.com/services/devops/pipelines/) | Jenkins | Code + Model -> App/Service | Most open and flexible activity support, approval queues, phases with gating |

## Next steps


Azure Machine Learning pipelines deliver value from the early stages of development.

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
