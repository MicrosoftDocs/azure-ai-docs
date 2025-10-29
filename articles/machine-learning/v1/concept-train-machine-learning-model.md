---
title: 'Build & train models (v1)'
titleSuffix: Azure Machine Learning
description: Learn how to train models with Azure Machine Learning (v1). Explore the different training methods and choose the right one for your project.
services: machine-learning
ms.service: azure-machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: ssalgado
ms.subservice: core
ms.topic: concept-article
ms.date: 09/10/2025
ms.custom: UpdateFrequency5, devx-track-python, devx-track-azurecli
ms.devlang: azurecli
---

# Train models with Azure Machine Learning (v1)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

Azure Machine Learning offers multiple ways to train models, including code-first solutions with the SDK and low-code options like automated machine learning and the visual designer. Use the following list to determine which training method fits your needs:

+ [Azure Machine Learning SDK for Python](#python-sdk): The Python SDK provides several ways to train models, each with different capabilities.

    | Training method | Description |
    | ----- | ----- |
    | [Run configuration](#run-configuration) | A **common way to train models** is to use a training script and job configuration. The job configuration defines the training environment, including your script, compute target, and Azure Machine Learning environment. You can run a training job by specifying these details. |
    | [Automated machine learning](#automated-machine-learning) | Automated machine learning lets you **train models without deep data science or programming expertise**. For experienced users, it saves time by automating algorithm selection and hyperparameter tuning. Job configuration is not required when using automated machine learning. |
    | [Machine learning pipeline](#machine-learning-pipeline) | Pipelines are not a separate training method, but a **way to define workflows using modular, reusable steps** that can include training. Pipelines support both automated machine learning and run configuration. Use a pipeline when you want to:<br>* **Schedule unattended processes** like long-running training jobs or data preparation.<br>* Coordinate **multiple steps** across different compute resources and storage locations.<br>* Create a **reusable template** for scenarios such as retraining or batch scoring.<br>* **Track and version data sources, inputs, and outputs** for your workflow.<br>* Enable **different teams to work on specific steps independently** and combine them in a pipeline. |

+ **Designer**: Azure Machine Learning designer is an easy entry point for building proof of concepts or for users with limited coding experience. Train models using a drag-and-drop web UI. You can include Python code or train models without writing any code.

+ **Azure CLI**: The machine learning CLI offers commands for common Azure Machine Learning tasks and is often used for **scripting and automation**. For example, after creating a training script or pipeline, you can use the CLI to start a training job on a schedule or when training data is updated. The CLI can submit jobs using run configurations or pipelines.

Each training method can use different types of compute resources, called [__compute targets__](concept-azure-machine-learning-architecture.md#compute-targets). A compute target can be a local machine or a cloud resource, such as Azure Machine Learning Compute, Azure HDInsight, or a remote virtual machine.

## Python SDK

The Azure Machine Learning SDK for Python lets you build and run machine learning workflows. You can interact with the service from an interactive Python session, Jupyter Notebooks, Visual Studio Code, or other IDE.

* [What is the Azure Machine Learning SDK for Python](/python/api/overview/azure/ml/intro)
* [Install/update the SDK](/python/api/overview/azure/ml/install)
* [Configure a development environment for Azure Machine Learning](how-to-configure-environment.md)

### Run configuration


A typical training job in Azure Machine Learning is defined using [ScriptRunConfig](/python/api/azureml-core/azureml.core.scriptrunconfig). The script run configuration, together with your training script(s), is used to train a model on a compute target.

You can start with a run configuration for your local computer and switch to a cloud-based compute target as needed. To change the compute target, update the run configuration. Each run logs information about the training job, including inputs, outputs, and logs.

* [What is a run configuration?](concept-azure-machine-learning-architecture.md#run-configurations)
* [Tutorial: Train your first ML model](tutorial-1st-experiment-sdk-train.md)
* [Examples: Jupyter Notebook and Python examples of training models](https://github.com/Azure/azureml-examples)
* [How to: Configure a training run](how-to-set-up-training-targets.md)

### Automated Machine Learning

Define iterations, hyperparameter settings, featurization, and other options. During training, Azure Machine Learning tests different algorithms and parameters in parallel. Training stops when it meets the exit criteria you set.


> [!TIP]
> You can also use Automated ML through [Azure Machine Learning studio](https://ml.azure.com), in addition to the Python SDK.

* [What is automated machine learning?](../concept-automated-ml.md)
* [Tutorial: Create your first classification model with automated machine learning](../tutorial-first-experiment-automated-ml.md)
* [Examples: Jupyter Notebook examples for automated machine learning](https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/automated-machine-learning)
* [How to: Configure automated ML experiments in Python](how-to-configure-auto-train.md)
* [How to: Autotrain a time-series forecast model](../how-to-auto-train-forecast.md)
* [How to: Create, explore, and deploy automated machine learning experiments with Azure Machine Learning studio](../how-to-use-automated-ml-for-ml-models.md)

### Machine learning pipeline


Machine learning pipelines can use the training methods described above. Pipelines focus on creating workflows, so they cover more than just model training. In a pipeline, you can train a model using automated machine learning or run configurations.

* [What are ML pipelines in Azure Machine Learning?](../concept-ml-pipelines.md)
* [Create and run machine learning pipelines with Azure Machine Learning SDK](how-to-create-machine-learning-pipelines.md)
* [Tutorial: Use Azure Machine Learning Pipelines for batch scoring](tutorial-pipeline-python-sdk.md)
* [Examples: Jupyter Notebook examples for machine learning pipelines](https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/machine-learning-pipelines)
* [Examples: Pipeline with automated machine learning](https://aka.ms/pl-automl)

### Understand what happens when you submit a training job


The Azure training lifecycle includes:

1. Zipping the files in your project folder, ignoring those specified in _.amlignore_ or _.gitignore_
2. Scaling up your compute cluster
3. Building or downloading the Docker image to the compute node
    1. The system calculates a hash of:
        - The base image
        - The conda definition YAML (see [Create & use software environments in Azure Machine Learning](how-to-use-environments.md))
    2. The system uses this hash to look up the workspace Azure Container Registry (ACR)
    3. If not found, it checks the global ACR
    4. If still not found, the system builds a new image (which is cached and registered with the workspace ACR)
4. Downloading your zipped project file to temporary storage on the compute node
5. Unzipping the project file
6. The compute node executes `python <entry script> <arguments>`
7. Saving logs, model files, and other files written to `./outputs` to the storage account associated with the workspace
8. Scaling down compute, including removing temporary storage

If you train on your local machine ("configure as local run"), Docker is not required. You can use Docker locally if you prefer (see [Configure ML pipeline](how-to-debug-pipelines.md) for an example).

## Azure Machine Learning designer


The designer lets you train models using a drag-and-drop interface in your web browser.

+ [What is the designer?](concept-designer.md)
+ [Tutorial: Predict automobile price](tutorial-designer-automobile-price-train-score.md)

## Azure CLI


The machine learning CLI is an extension for the Azure CLI. It provides cross-platform commands for working with Azure Machine Learning. Typically, you use the CLI to automate tasks, such as training a machine learning model.

* [Use the CLI extension for Azure Machine Learning](reference-azure-machine-learning-cli.md)
* [MLOps on Azure](https://github.com/microsoft/MLOps)


## Next steps

Learn how to [configure a training run](how-to-set-up-training-targets.md).
