---
title: 'Upgrade from v1 to v2'
titleSuffix: Azure Machine Learning
description: Upgrade from v1 to v2 of Azure Machine Learning REST APIs, CLI extension, and Python SDK.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.date: 02/03/2025
ms.reviewer: paulsh
ms.custom: devplatv2, devx-track-python
monikerRange: 'azureml-api-2 || azureml-api-1'
#customer intent: As a developer, I want to understand the differences between v1 and v2 of Azure Machine Learning REST APIs, CLI extension, and Python SDK, to decide which I should use.
---

# Upgrade to v2

Azure Machine Learning's v2 REST APIs, Azure CLI extension, and Python SDK introduce consistency and a set of new features to accelerate the production machine learning lifecycle. This article provides an overview of upgrading to v2 with recommendations to help you decide on v1, v2, or both.

> [!IMPORTANT]
> The designations "v1" and "v2" refer to the API, SDK, and CLI extension used by clients to interact with the service, and not the Azure Machine Learning service itself. There is no upgrade process for the service or your existing workspaces, only for your client code. Your Azure Machine Learning workspaces can be used with both the v1 and v2 APIs. However, new features will only be available through the v2 APIs.
>
> Support for the CLI v1 will end on September 30, 2025 and support for the Python SDK v1 will end on June 30, 2026.
>
> For more information on v2, see [what is v2](concept-v2.md?view=azureml-api-2&preserve-view=true). For a mapping of differences between v1 and v2 SDKs, with links to articles with example code, see [Mapping of Python SDK v1 to v2](#mapping-of-python-sdk-v1-to-v2).

## Prerequisites

- General familiarity with Azure Machine Learning and the v1 Python SDK.
- Understand [what is v2?](concept-v2.md?view=azureml-api-2&preserve-view=true)

## Should I use v2?

You should use v2 if you're starting a new machine learning project or workflow. You should use v2 if you want to use the new features offered in v2. The features include:
* Managed Inferencing
* Reusable components in pipelines
* Improved scheduling of pipelines
* Responsible AI dashboard
* Registry of assets

A new v2 project can reuse existing v1 resources like workspaces and compute and existing assets like models and environments created using v1. 

> [!IMPORTANT]
> New features in Azure Machine Learning will only be launched in v2.

## Which v2 API should I use?

In v2 interfaces via REST API, CLI, and Python SDK are available. The interface you should use depends on your scenario and preferences.

|API|Notes|
|-|-|
|REST|Fewest dependencies and overhead. Use for building applications on Azure Machine Learning as a platform, directly in programming languages without an SDK provided, or per personal preference.|
|CLI|Recommended for automation with CI/CD or per personal preference. Allows quick iteration with YAML files and straightforward separation between Azure Machine Learning and ML model code.|
|Python SDK|Recommended for complicated scripting (for example, programmatically generating large pipeline jobs) or per personal preference. Allows quick iteration with YAML files or development solely in Python.|

## Mapping of Python SDK v1 to v2

See each of the following articles for a comparison code mapping for SDK v1 vs v2.

|Resources and assets  |Article  |
|---------|---------|
|Workspace     |  [Workspace management in SDK v1 and SDK v2](migrate-to-v2-resource-workspace.md)  |
|Datastore     |   [Datastore management in SDK v1 and SDK v2](migrate-to-v2-resource-datastore.md)      |
|Data     |   [Data assets in SDK v1 and v2](migrate-to-v2-assets-data.md)      |
|Compute     |  [Compute management in SDK v1 and SDK v2](migrate-to-v2-resource-compute.md)       |
|Training     | [Run a script](migrate-to-v2-command-job.md) |
|Training     | [Local runs](migrate-to-v2-local-runs.md) |
|Training     | [Hyperparameter tuning](migrate-to-v2-execution-hyperdrive.md) |
|Training     | [Parallel Run](migrate-to-v2-execution-parallel-run-step.md) |
|Training     | [Pipelines](migrate-to-v2-execution-pipeline.md) |
|Training     | [AutoML](migrate-to-v2-execution-automl.md) |
| Models | [Model management in SDK v1 and SDK v2](migrate-to-v2-assets-model.md) |
| Deployment | [Upgrade deployment endpoints to SDK v2](migrate-to-v2-deploy-endpoints.md) |


## Resources and assets in v1 and v2

This section gives an overview of specific resources and assets in Azure Machine Learning. See the concept article for each entity for details on their usage in v2.

### Workspace

Workspaces don't need to be upgraded with v2. You can use the same workspace, regardless of whether you're using v1 or v2. 

If you create workspaces using automation, do consider upgrading the code for creating a workspace to v2. Typically Azure resources are managed via Azure Resource Manager (and Bicep) or similar resource provisioning tools. Alternatively, you can use the [CLI (v2) and YAML files](how-to-manage-workspace-cli.md?view=azureml-api-2&preserve-view=true#create-a-workspace).

For a comparison of SDK v1 and v2 code, see [Workspace management in SDK v1 and SDK v2](migrate-to-v2-resource-workspace.md).

> [!IMPORTANT]
> If your workspace uses a private endpoint, it will automatically have the `v1_legacy_mode` flag enabled, preventing usage of v2 APIs. See [how to configure network isolation with v2](how-to-configure-network-isolation-with-v2.md) for details.

### Connection (workspace connection in v1)

Workspace connections from v1 are persisted on the workspace, and fully available with v2.

For a comparison of SDK v1 and v2 code, see [Workspace management in SDK v1 and SDK v2](migrate-to-v2-resource-workspace.md).


### Datastore

Object storage datastore types created with v1 are fully available for use in v2. Database datastores aren't supported; export to object storage (usually Azure Blob) is the recommended migration path.

For a comparison of SDK v1 and v2 code, see [Datastore management in SDK v1 and SDK v2](migrate-to-v2-resource-datastore.md).

### Data (datasets in v1)

Datasets are renamed to data assets. *Backwards compatibility* is provided, which means you can use V1 Datasets in V2. When you consume a V1 Dataset in a V2 job, you'll notice they're automatically mapped into V2 types as follows:

* V1 FileDataset = V2 Folder (`uri_folder`)
* V1 TabularDataset = V2 Table (`mltable`)

It should be noted that *forwards compatibility* is **not** provided, which means you **cannot** use V2 data assets in V1.

This article talks more about handling data in v2 - [Read and write data in a job](how-to-read-write-data-v2.md?view=azureml-api-2&preserve-view=true)

For a comparison of SDK v1 and v2 code, see [Data assets in SDK v1 and v2](migrate-to-v2-assets-data.md).


### Compute

Compute of type `AmlCompute` and `ComputeInstance` are fully available for use in v2.

For a comparison of SDK v1 and v2 code, see [Compute management in SDK v1 and SDK v2](migrate-to-v2-resource-compute.md).

### Jobs (experiments, runs, pipelines in v1)

In v2, "experiments," "runs," and "pipelines" are consolidated into jobs. A job has a type. Most jobs are `command` jobs that run a command, like `python main.py`. What runs in a job is agnostic to any programming language, so you can run `bash` scripts, invoke `python` interpreters, run a bunch of `curl` commands, or anything else. Another common type of job is `pipeline`, which defines child jobs that might have input/output relationships, forming a directed acyclic graph (DAG).

For a comparison of SDK v1 and v2 code, see 
* [Run a script](migrate-to-v2-command-job.md)
* [Local runs](migrate-to-v2-local-runs.md)
* [Hyperparameter tuning](migrate-to-v2-execution-hyperdrive.md)
* [Parallel Run](migrate-to-v2-execution-parallel-run-step.md)
* [Pipelines](migrate-to-v2-execution-pipeline.md)
* [AutoML](migrate-to-v2-execution-automl.md)

### Designer

You can use designer to build pipelines using your own v2 custom components and the new prebuilt components from registry. In this situation, you can use v1 or v2 data assets in your pipeline. 

You can continue to use designer to build pipelines using classic prebuilt components and v1 dataset types (tabular, file). You can't use existing designer classic prebuilt components with v2 data asset.

You can't build a pipeline using both existing designer classic prebuilt components and v2 custom components.


### Model

Models created from v1 can be used in v2. 

For a comparison of SDK v1 and v2 code, see [Model management in SDK v1 and SDK v2](migrate-to-v2-assets-model.md)

### Endpoint and deployment (endpoint and web service in v1)

With SDK/CLI v1, you can deploy models on ACI or AKS as web services. Your existing v1 model deployments and web services continue to function as they are, but Using SDK/CLI v1 to deploy models on ACI or AKS as web services is now considered as **legacy**. For new model deployments, we recommend upgrading to v2. In v2, we offer [managed endpoints or Kubernetes endpoints](./concept-endpoints.md?view=azureml-api-2&preserve-view=true). The following table guides our recommendation:

|Endpoint type in v2|Upgrade from|Notes|
|-|-|-|
|Local|ACI|Quick test of model deployment locally; not for production.|
|Managed online endpoint|ACI, AKS|Enterprise-grade managed model deployment infrastructure with near real-time responses and massive scaling for production.|
|Managed batch endpoint|ParallelRunStep in a pipeline for batch scoring|Enterprise-grade managed model deployment infrastructure with massively parallel batch processing for production.|
|Azure Kubernetes Service (AKS)|ACI, AKS|Manage your own AKS cluster(s) for model deployment, giving flexibility and granular control at the cost of IT overhead.|
|Azure Arc Kubernetes|N/A|Manage your own Kubernetes cluster(s) in other clouds or on-premises, giving flexibility and granular control at the cost of IT overhead.|

For a comparison of SDK v1 and v2 code, see [Upgrade deployment endpoints to SDK v2](migrate-to-v2-deploy-endpoints.md).
For migration steps from your existing ACI web services to managed online endpoints, see our [upgrade guide article](migrate-to-v2-managed-online-endpoints.md) and [blog](https://aka.ms/acimoemigration).

### Environment

Environments created from v1 can be used in v2. In v2, environments have new features like creation from a local Docker context.

## Managing secrets

The management of Key Vault secrets differs significantly in V2 compared to V1. The V1 set_secret and get_secret SDK methods aren't available in V2. Instead, direct access using Key Vault client libraries should be used. When accessing secrets from a training script, you can use either the managed identity of the compute or your identity.

For details about Key Vault, see [Use authentication credential secrets in Azure Machine Learning training jobs](how-to-use-secrets-in-runs.md?view=azureml-api-2&preserve-view=true).

## Scenarios across the machine learning lifecycle

There are a few scenarios that are common across the machine learning lifecycle using Azure Machine Learning. We'll look at a few and give general recommendations for upgrading to v2.

### Azure setup

Azure recommends Azure Resource Manager templates (often via Bicep for ease of use) to create resources. The same is a good approach for creating Azure Machine Learning resources as well.

If your team is only using Azure Machine Learning, you might consider provisioning the workspace and any other resources via YAML  files and CLI instead.

### Prototyping models

We recommend v2 for prototyping models. You might consider using the CLI for an interactive use of Azure Machine Learning, while your model training code is Python or any other programming language. Alternatively, you might adopt a full-stack approach with Python solely using the Azure Machine Learning SDK or a mixed approach with the Azure Machine Learning Python SDK and YAML files.

### Production model training

We recommend v2 for production model training. Jobs consolidate the terminology and provide a set of consistency that allows for easier transition between types (for example, `command` to `sweep`) and a GitOps-friendly process for serializing jobs into YAML files.

With v2, you should separate your machine learning code from the control plane code. This separation allows for easier iteration and allows for easier transition between local and cloud. We also recommend using MLflow for tracking and model logging. See the [MLflow concept article](concept-mlflow.md?view=azureml-api-2&preserve-view=true) for details.

### Production model deployment

We recommend v2 for production model deployment. Managed endpoints abstract the IT overhead and provide a performant solution for deploying and scoring models, both for online (near real-time) and batch (massively parallel) scenarios.

Kubernetes deployments are supported in v2 through AKS or Azure Arc, enabling Azure cloud and on-premises deployments managed by your organization.

### Machine learning operations (MLOps)

A MLOps workflow typically involves CI/CD through an external tool. Typically a CLI is used in CI/CD, though you can alternatively invoke Python or directly use REST.

The solution accelerator for MLOps with v2 is being developed at https://github.com/Azure/mlops-v2 and can be used as reference or adopted for setup and automation of the machine learning lifecycle.

### A note on GitOps with v2

A key paradigm with v2 is serializing machine learning entities as YAML files for source control with `git`, enabling better GitOps approaches than were possible with v1. For instance, you could enforce policy by which only a service principal used in CI/CD pipelines can create/update/delete some or all entities, ensuring changes go through a governed process like pull requests with required reviewers. Since the files in source control are YAML, they're easy to diff and track changes over time. You and your team might consider shifting to this paradigm as you upgrade to v2.

You can obtain a YAML representation of any entity with the CLI via `az ml <entity> show --output yaml`. This output has system-generated properties, which can be ignored or deleted.

## Should I upgrade existing v1 code to v2

You can reuse your existing v1 assets in your v2 workflows. For instance, a model created in v1 can be used to perform Managed Inferencing in v2.

Optionally, if you want to upgrade specific parts of your existing v1 code to v2, refer to the comparison links provided in this document.

## Can I use v1 and v2 together?

v1 and v2 can coexist in a workspace. You can reuse your existing assets in your v2 workflows. For instance, a model created in v1 can be used to perform Managed Inferencing in v2. Resources like workspace, compute, and datastore work across v1 and v2, with exceptions. A user can call the v1 Python SDK to change a workspace's description, then using the v2 CLI extension change it again. Jobs (experiments/runs/pipelines in v1) can be submitted to the same workspace from the v1 or v2 Python SDK. A workspace can have both v1 and v2 model deployment endpoints. 

### Using v1 and v2 code together

We don't recommend using the v1 and v2 SDKs together in the same code. It's technically possible to use v1 and v2 in the same code because they use different Azure namespaces. However, there are many classes with the same name across these namespaces (like Workspace, Model) which can cause confusion and make code readability and debuggability challenging. 

> [!IMPORTANT]
> If your workspace uses a private endpoint, it will automatically have the `v1_legacy_mode` flag enabled, preventing usage of v2 APIs. See [how to configure network isolation with v2](how-to-configure-network-isolation-with-v2.md?view=azureml-api-2&preserve-view=true) for details.

## Related content

- [Get started with the CLI (v2)](how-to-configure-cli.md?view=azureml-api-2&preserve-view=true)
- [Get started with the Python SDK (v2)](https://aka.ms/sdk-v2-install)
