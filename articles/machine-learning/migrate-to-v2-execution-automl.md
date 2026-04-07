---
title: Upgrade AutoML to SDK v2
titleSuffix: Azure Machine Learning
description: Upgrade AutoML from v1 to v2 of Azure Machine Learning SDK
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.date: 03/26/2026
ms.reviewer: rasavage
ms.custom: migration, dev-focus
ai-usage: ai-assisted
monikerRange: 'azureml-api-1 || azureml-api-2'
---

# Upgrade AutoML to SDK v2

In SDK v2, jobs consolidate "experiments" and "runs".

In SDK v1, you primarily configure and run AutoML by using the `AutoMLConfig` class. In SDK v2, this class is now an `AutoML` job. Although some configuration options differ, most naming and functionality is preserved in V2.

This article compares scenarios in SDK v1 and SDK v2.

## Submit AutoML run

:::moniker range="azureml-api-1"
> [!IMPORTANT]
> Azure Machine Learning SDK v1 was deprecated on March 31, 2025. Support ends on June 30, 2026. Migrate to SDK v2 before that date. For more information, see [What is Azure Machine Learning CLI and Python SDK v2?](concept-v2.md)

* SDK v1: The following example shows an AutoML classification task. For the complete code, see the [examples repo](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/classification-credit-card-fraud/auto-ml-classification-credit-card-fraud.ipynb).

    ```python
    # Imports
    import logging

    import azureml.core
    from azureml.core.experiment import Experiment
    from azureml.core.workspace import Workspace
    from azureml.core.dataset import Dataset
    from azureml.train.automl import AutoMLConfig
   
    # Load tabular dataset
    data = "<url_to_data>"
    dataset = Dataset.Tabular.from_delimited_files(data)
    training_data, validation_data = dataset.random_split(percentage=0.8, seed=223)
    label_column_name = "Class"
    
    # Configure Auto ML settings
    automl_settings = {
        "n_cross_validations": 3,
        "primary_metric": "average_precision_score_weighted",
        "enable_early_stopping": True,
        "max_concurrent_iterations": 2,  
        "experiment_timeout_hours": 0.25,  
        "verbosity": logging.INFO,
    }
    
    # Put together an AutoML job constructor
    automl_config = AutoMLConfig(
        task="classification",
        debug_log="automl_errors.log",
        compute_target=compute_target,
        training_data=training_data,
        label_column_name=label_column_name,
        **automl_settings,
    )
    
    # Submit run
    remote_run = experiment.submit(automl_config, show_output=False)
    azureml_url = remote_run.get_portal_url()
    print(azureml_url)
    ```
:::moniker-end

* SDK v2: The following example shows an AutoML classification task. For the complete code, see the [examples repo](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-classification-task-bankmarketing/automl-classification-task-bankmarketing.ipynb).

    ```python
    # Imports
    from azure.ai.ml import automl, Input, MLClient
    from azure.ai.ml.constants import AssetTypes
   
    # Create MLTables for training dataset
    # Note that AutoML Job can also take in tabular data
    my_training_data_input = Input(
        type=AssetTypes.MLTABLE, path="./data/training-mltable-folder"
    )
    
    # Create the AutoML classification job with the related factory-function.
    classification_job = automl.classification(
        compute="<compute_name>",
        experiment_name="<exp_name>",
        training_data=my_training_data_input,
        target_column_name="<name_of_target_column>",
        primary_metric="accuracy",
        n_cross_validations=5,
        enable_model_explainability=True,
        tags={"my_custom_tag": "My custom value"},
    )
    
    # Limits are all optional
    classification_job.set_limits(
        timeout_minutes=600,
        trial_timeout_minutes=20,
        max_trials=5,
        max_concurrent_trials = 4,
        max_cores_per_trial= 1,
        enable_early_termination=True,
    )
    
    # Training properties are optional
    classification_job.set_training(
        blocked_training_algorithms=["LogisticRegression"],
        enable_onnx_compatible_models=True,
    )
    
    # Submit the AutoML job
    returned_job = ml_client.jobs.create_or_update(classification_job)  
    returned_job
    ```

## Mapping of key functionality in SDK v1 and SDK v2

|Functionality in SDK v1|Rough mapping in SDK v2|
|-|-|
|[`AutoMLConfig`](/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig)|[`automl.classification()` / `automl.regression()` / `automl.forecasting()`](/python/api/azure-ai-ml/azure.ai.ml.automl)|
|`experiment.submit(automl_config)`|[`ml_client.jobs.create_or_update(job)`](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-jobs)|
|`remote_run.get_portal_url()`|`returned_job.services["Studio"].endpoint`|
|`AutoMLConfig(enable_early_stopping=True)`|`job.set_limits(enable_early_termination=True)`|
|`AutoMLConfig(blocked_models=[...])`|`job.set_training(blocked_training_algorithms=[...])`|
|`AutoMLConfig(n_cross_validations=N)`|`automl.classification(n_cross_validations=N)`|

## Next steps

For more information, see:

* [How to train an AutoML model with Python SDKv2](how-to-configure-auto-train.md)
