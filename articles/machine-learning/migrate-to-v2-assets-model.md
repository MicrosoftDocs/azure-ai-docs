---
title:  Upgrade model management to SDK v2
titleSuffix: Azure Machine Learning
description: Compare model registration and management patterns between Azure Machine Learning SDK v1 and SDK v2.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.date: 03/30/2026
ms.reviewer: kritifaujdar
ms.custom: migration, dev-focus
ai-usage: ai-assisted
monikerRange: 'azureml-api-1 || azureml-api-2'
---

# Upgrade model management to SDK v2

> [!IMPORTANT]
> This article references Azure Machine Learning SDK v1. SDK v1 is deprecated as of March 31, 2025. Support for it ends on June 30, 2026. Your existing workflows that use SDK v1 continue to operate after the end-of-support date, but they could be exposed to security risks or breaking changes. Transition to SDK v2 before June 30, 2026. For more information, see [What is Azure Machine Learning CLI and Python SDK v2?](concept-v2.md)

This article provides a comparison of scenarios in SDK v1 and SDK v2.

## Create model

* SDK v1

    ```python
    from azureml.core.model import Model
    
    # Register model
    model = Model.register(ws, model_name="local-file-example", model_path="mlflow-model/model.pkl")
    ```

* SDK v2
    
    ```python
    from azure.ai.ml.entities import Model
    from azure.ai.ml.constants import AssetTypes
    
    file_model = Model(
        path="mlflow-model/model.pkl",
        type=AssetTypes.CUSTOM_MODEL,
        name="local-file-example",
        description="Model created from local file.",
        stage="Development"  # Optional lifecycle stage: Development, Production, or Archived
    )
    ml_client.models.create_or_update(file_model)
    ```

## Use model in an experiment or job

* SDK v1

    ```python
    model = run.register_model(model_name='run-model-example',
                               model_path='outputs/model/')
    print(model.name, model.id, model.version, sep='\t')
    ```

* SDK v2

    ```python
    from azure.ai.ml.entities import Model
    from azure.ai.ml.constants import AssetTypes
    
    run_model = Model(
        path="azureml://jobs/$RUN_ID/outputs/artifacts/paths/model/",
        name="run-model-example",
        description="Model created from run.",
        type=AssetTypes.CUSTOM_MODEL
    )
    
    ml_client.models.create_or_update(run_model)
    ```

For more information about models, see [Work with models in Azure Machine Learning](how-to-manage-models.md).

## Mapping of key functionality in SDK v1 and SDK v2

|Functionality in SDK v1|Rough mapping in SDK v2|
|-|-|
|[Model.register](/python/api/azureml-core/azureml.core.model(class)#azureml-core-model-register)|[ml_client.models.create_or_update](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-create-or-update)|
|[run.register_model](/python/api/azureml-core/azureml.core.run.run#azureml-core-run-run-register-model)|[ml_client.models.create_or_update](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-create-or-update)|
|[Model.deploy](/python/api/azureml-core/azureml.core.model(class)#azureml-core-model-deploy)|[ml_client.begin_create_or_update(blue_deployment)](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-begin-create-or-update)|

## Next steps

For more information, see the following documentation:

* [Create a model in v1](v1/how-to-deploy-and-where.md?tabs=python#register-a-model-from-a-local-file)
* [Deploy a model in v1](v1/how-to-deploy-and-where.md?tabs=azcli#workflow-for-deploying-a-model)
* [Create a model in v2](how-to-manage-models.md)
* [Deploy a model in v2](how-to-deploy-online-endpoints.md)

