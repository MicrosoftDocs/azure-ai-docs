---
title: MLOps machine learning model management
titleSuffix: Azure Machine Learning
description: Learn how Azure Machine Learning uses machine learning operations (MLOps) to help manage the lifecycle of your models.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: concept-article
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.custom: mktng-kw-nov2021, FY25Q1-Linter
ms.date: 10/06/2025
#Customer intent: As a data scientist, I want to understand how MLOps can help manage the lifecycle of my models so I can improve the quality and consistency of my machine learning solutions.
---

# MLOps model management with Azure Machine Learning

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

This article describes how Azure Machine Learning uses machine learning operations (MLOps) to manage the lifecycle of your models. Applying MLOps practices can improve the quality and consistency of your machine learning solutions.

MLOps is based on [DevOps](https://azure.microsoft.com/overview/what-is-devops/) principles and practices that increase the efficiency of workflows, such as continuous integration, continuous deployment, and continuous delivery. Applying these principles to the machine learning lifecycle results in:

- Faster experimentation and model development.
- Faster deployment of models into production.
- Better quality assurance and end-to-end lineage tracking.

## MLOps capabilities

MLOps provides the following capabilities to the machine learning process:

- **Create reproducible machine learning pipelines** to define repeatable and reusable steps for data preparation, training, and scoring processes.
- **Create reusable software environments** for training and deploying models.
- **Register, package, and deploy models** from anywhere, and track associated metadata required to use a model.
- **Log lineage data for machine learning lifecycle governance**, such as who published models, why changes were made, and when models were deployed or used in production.
- **Notify and alert on machine learning lifecycle events** such as experiment completion, model registration, model deployment, and data drift detection.
- **Monitor operational and machine learning-related issues** by comparing model inputs, exploring model-specific metrics, and viewing monitoring and alerts on machine learning infrastructure.
- **Automate the end-to-end machine learning lifecycle** by using machine learning pipelines and [Azure Pipelines](/azure/devops/pipelines/get-started/what-is-azure-pipelines) to continuously test, update, and roll out new machine learning models.

For more information on MLOps, see [Machine learning operations](/azure/cloud-adoption-framework/ready/azure-best-practices/ai-machine-learning-mlops).

## Reproducible machine learning pipelines

Use Azure Machine Learning pipelines to stitch together all the steps in your model training process. Machine learning pipeline steps can include data preparation, feature extraction, hyperparameter tuning, and model evaluation.

In the [Azure Machine Learning studio Designer](concept-designer.md), you can clone a pipeline to iterate over its design without losing your old versions. To clone a pipeline at any time in the Designer, select **Clone** in the top menu bar.

For more information on Azure Machine Learning pipelines, see [Machine learning pipelines](concept-ml-pipelines.md).

## Reusable software environments

Azure Machine Learning environments ensure that builds are reproducible without using manual software configurations. Environments can track and reproduce the pip and conda software dependencies for your projects.

You can use environments for model training and deployment. For more information on environments, see [Azure Machine Learning environments](concept-environments.md).

## Model registration, packaging, and deployment

Azure Machine Learning can use MLOps from anywhere to register, package, and deploy models.

### Register and track models

Model registration stores and versions your models in your Azure Machine Learning workspace in the Azure cloud. The model registry makes it easy to organize and keep track of your trained models.

A registered model is a logical container for one or more files that make up your model. For example, if your model is stored in multiple files, you can register the files as a single model in your Azure Machine Learning workspace. After registration, you can download or deploy the registered model and receive all the component files.

You can also register models that are trained outside of Azure Machine Learning. Azure Machine Learning supports any model that can be loaded by using Python 3.10 or higher.

You identify registered models by name and version. Whenever you register a model with the same name as an existing model, the registry increments the version number.

You can provide metadata tags during registration and use these tags to search for a model.

> [!IMPORTANT]
> You can't delete a registered model that's being used in an active deployment.

For more information on how to use models in Azure Machine Learning, see [Work with models in Azure Machine Learning](./how-to-manage-models.md).

### Package and debug models

To deploy a model into production, you must first package it into a Docker image. In most cases, image creation automatically happens in the background during deployment. However, you can manually specify the image.

It's useful to deploy to your local development environment first so you can troubleshoot and debug before deploying to the cloud. This practice can help you avoid having problems with your deployment to Azure Machine Learning. For more information on how to resolve common deployment issues, see [How to troubleshoot online endpoints](how-to-troubleshoot-online-endpoints.md).

### Convert and optimize models

You can convert your model to [Open Neural Network Exchange](https://onnx.ai) (ONNX) to try to improve performance. Typically, converting to ONNX can double performance.

For more information on ONNX with Azure Machine Learning, see [Create and accelerate machine learning models](concept-onnx.md).

### Deploy models as endpoints

You can deploy trained machine learning models as [endpoints](concept-endpoints.md) locally or in the cloud. Deployments use CPUs and GPUs for inferencing.

To deploy a model as an endpoint, you need to provide the following information:

- The **model** used to score data submitted to the service or device.
- An **entry script**, also called **scoring script**, that accepts requests, uses the models to score the data, and returns a response.
- An **environment** that describes the pip and conda dependencies required by the models and entry script.
- Any other assets, such as text and data, required by the model and entry script.

>[!IMPORTANT]
>When you deploy an [MLflow model](concept-mlflow.md), you don't need to provide an entry script or an environment for the deployment. For more information on deploying MLflow models, see [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md).

You also provide the configuration of the target deployment platform, such as the virtual machine (VM) family type, available memory, and number of cores. When Azure Machine Learning creates the image, it also adds any components it needs, such as assets needed to run the web service.

#### Batch scoring with batch endpoints

Batch scoring is supported through batch endpoints. For more information on batch scoring, see [Batch endpoints](concept-endpoints-batch.md).

#### Real-time scoring with online endpoints

You can use your models with [online endpoints](concept-endpoints-online.md) for real-time scoring. Compute targets for online endpoints can be local development environments, managed online endpoints, or Azure Kubernetes Service (AKS).

To deploy a model to an online endpoint, you need to provide the following information:

- The model or ensemble of models.
- Dependencies required to use the model, for example, a script that accepts requests and invokes the model and conda dependencies.
- Deployment configuration that describes how and where to deploy the model.

For more information on deployment for real-time scoring, see [Deploy online endpoints](how-to-deploy-online-endpoints.md).

#### Controlled rollout for online endpoints

When you deploy to an online endpoint, you can use controlled rollout to enable the following scenarios:

- Create multiple versions of an endpoint for a deployment.
- Perform A/B testing by routing traffic to different deployments within the endpoint.
- Switch between endpoint deployments by updating the traffic percentage in the endpoint configuration.

For more information on deployment using a controlled rollout, see [Perform safe rollout of new deployments for real-time inference](how-to-safely-rollout-online-endpoints.md).

## Metadata for machine learning lifecycle governance

Azure Machine Learning gives you the capability to track the end-to-end audit trail of all your machine learning assets by using metadata. For example:

- [Azure Machine Learning data assets](how-to-create-register-datasets.md) help you track, profile, and version data.
- [Model interpretability](how-to-machine-learning-interpretability.md) allows you to explain your models, meet regulatory compliance, and understand how models arrive at a result for a given input.
- Azure Machine Learning job history stores a snapshot of the code, data, and computes used to train a model.
- [Azure Machine Learning model registration](how-to-manage-models.md?tabs=use-local#create-a-model-in-the-model-registry) captures all the metadata associated with your model. For example, which experiment trained the model, where the model is being deployed, and whether the model deployments are healthy.
- [Integration with Azure](how-to-use-event-grid.md) lets you act on events in the machine learning lifecycle, such as model registration, deployment, data drift, and training job events.

Some information on models and data assets is automatically captured, but you can add more information by using *tags*. When you look for registered models and data assets in your workspace, you can use tags as filters.

>[!NOTE]
>When you use the **Tags** in the **Filter by** option on the **Models** page of Azure Machine Learning studio, be sure to use `TagName=TagValue` without spaces rather than `TagName : TagValue`.

## Machine learning lifecycle event notification and alerts

Azure Machine Learning publishes key events to Azure Event Grid, which can be used to notify and automate on events in the machine learning lifecycle. For more information on how to set up event-driven processes based on Azure Machine Learning events, see [Custom CI/CD and event-driven workflows](how-to-use-event-grid.md).

## Machine learning lifecycle automation

You can use Git and [Azure Pipelines](/azure/devops/pipelines/get-started/what-is-azure-pipelines) to create a continuous integration process that trains a machine learning model. In a typical scenario, when a data scientist checks a change into a project's Git repository, Azure Pipelines starts the training job.

You can inspect the job results to see the performance characteristics of the trained model. You can also create a pipeline that deploys the model as a web service.

The [Machine Learning extension](https://marketplace.visualstudio.com/items?itemName=ms-air-aiagility.vss-services-azureml) makes it easier to work with Azure Pipelines. The extension provides the following enhancements to Azure Pipelines:

- Enables Azure Machine Learning workspace selection when you define a service connection.
- Enables trained model creation in a training pipeline to trigger a deployment in Azure Pipelines.

For more information on using Azure Pipelines with Azure Machine Learning, see [Use Azure Pipelines with Azure Machine Learning](how-to-devops-machine-learning.md).

## Analytics

Microsoft Power BI supports using machine learning models for data analytics. For more information, see [AI with dataflows](/power-bi/transform-model/dataflows/dataflows-machine-learning-integration).

## Related content

- [Set up MLOps with Azure DevOps](how-to-setup-mlops-azureml.md)
- [Learning path: End-to-end MLOps with Azure Machine Learning](/training/paths/build-first-machine-operations-workflow/)
- [CI/CD of machine learning models with Azure Pipelines](/azure/devops/pipelines/targets/azure-machine-learning)

