---
title: Data splits and cross-validation in automated machine learning
titleSuffix: Azure Machine Learning
description: Learn how to configure training, validation, cross-validation, and test data for automated machine learning experiments.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: how-to
ms.custom: UpdateFrequency5, automl, sdkv1
ms.author: scottpolly
author: s-polly
ms.reviewer: sooryar
ms.date: 10/04/2024
monikerRange: 'azureml-api-1'

#customer intent: As a data scientist, I want to explore options for applying data splits and cross-validation to my automated ML experiments.
---

# Configure training, validation, cross-validation, and test data in automated machine learning

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

This article describes options for configuring training data and validation data splits along with cross-validation settings for your automated machine learning (automated ML) experiments. In Azure Machine Learning, when you use automated ML to build multiple machine learning models, each child run needs to validate the related model by calculating the quality metrics for that model, such as accuracy or area under the curve (AUC) weighted. These metrics are calculated by comparing the predictions made with each model with real labels from past observations in the validation data. Automated ML experiments perform model validation automatically.

The following sections describe how you can customize validation settings with the [Azure Machine Learning Python SDK](/python/api/overview/azure/ml/). To learn more about how metrics are calculated based on validation type, see the [Set metric calculation for cross validation](#set-metric-calculation-for-cross-validation) section. If you're interesting in a low-code or no-code experience, see [Create your automated ML experiments in Azure Machine Learning studio](../how-to-use-automated-ml-for-ml-models.md#create-and-run-experiment). 

## Prerequisites

- An Azure Machine Learning workspace. To create the workspace, see [Create workspace resources](../quickstart-create-resources.md).

- Familiarity with setting up an automated ML experiment with the Azure Machine Learning SDK. To see the fundamental automated machine learning experiment design patterns, complete the [Train an object detection model](../tutorial-auto-train-image-models.md) tutorial or the [Set up AutoML training with Python](how-to-configure-auto-train.md) guide.

- An understanding of train/validation data splits and cross-validation as machine learning concepts. For a high-level explanation, see the following articles:

   - [About training, validation, and testing datasets in machine learning](https://medium.com/towards-data-science/train-validation-and-test-sets-72cb40cba9e7)

   - [Understanding cross validation in machine learning](https://towardsdatascience.com/understanding-cross-validation-419dbd47e9bd) 

[!INCLUDE [automl-sdk-version](../includes/machine-learning-automl-sdk-version.md)]

## Set default data splits and cross-validation in machine learning

To set default data splits and cross-validation in machine learning, use the [AutoMLConfig](/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig) Class object to define your experiment and training settings. In the following example, only the required parameters are defined. The `n_cross_validations` and `validation_data` parameters aren't included.

> [!NOTE]
> In forecasting scenarios, default data splits and cross-validation aren't supported. 

```python
data = "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/creditcard.csv"

dataset = Dataset.Tabular.from_delimited_files(data)

automl_config = AutoMLConfig(compute_target = aml_remote_compute,
                             task = 'classification',
                             primary_metric = 'AUC_weighted',
                             training_data = dataset,
                             label_column_name = 'Class'
                            )
```

If you don't explicitly specify a `validation_data` or `n_cross_validations` parameter, automated ML applies default techniques depending on the number of rows provided in the single dataset `training_data`.

| Training data size | Validation technique |
| --- | --- |
| **Larger than 20,000 rows**  | Train/validation data split is applied. The default is to take 10% of the initial training data set as the validation set. In turn, that validation set is used for metrics calculation. |
| **Smaller than 20,000 rows** | Cross-validation approach is applied. The default number of folds depends on the number of rows. <br> - If the dataset is less than 1,000 rows, 10 folds are used. <br> - If the rows are between 1,000 and 20,000, three folds are used. |

## Provide validation dataset

You have two options for providing validation data. You can start with a single data file and split it into training data and validation data sets, or you can provide a separate data file for the validation set. Either way, the `validation_data` parameter in your `AutoMLConfig` object assigns which data to use as your validation set. This parameter only accepts data sets in the form of an [Azure Machine Learning dataset](how-to-create-register-datasets.md) or pandas dataframe.   

Here are some other considerations for working with validation parameters:

- You can set only one validation parameter, either the `validation_data` parameter or the `n_cross_validations` parameter, but not both.
- When you use the `validation_data` parameter, you must also specify the `training_data` and `label_column_name` parameters.

The following example explicitly defines which portion of the `dataset` to use for training (`training_data`) and for validation (`validation_data`):

```python
data = "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/creditcard.csv"

dataset = Dataset.Tabular.from_delimited_files(data)

training_data, validation_data = dataset.random_split(percentage=0.8, seed=1)

automl_config = AutoMLConfig(compute_target = aml_remote_compute,
                             task = 'classification',
                             primary_metric = 'AUC_weighted',
                             training_data = training_data,
                             validation_data = validation_data,
                             label_column_name = 'Class'
                            )
```

## Provide validation dataset size

When you provide the validation set size, you supply only a single dataset for the experiment. The `validation_data` parameter isn't specified, and the provided dataset is assigned to the `training_data` parameter.  

In your `AutoMLConfig` object, you can set the `validation_size` parameter to hold out a portion of the training data for validation. For this strategy, the automated ML job splits the validation set from the initial `training_data` that you supply. The value should be between 0.0 and 1.0 noninclusive (for example, 0.2 means 20% of the data is held out for validation data).

> [!NOTE]
> In forecasting scenarios, the `validation_size` parameter isn't supported. 

The following example supplies a single `dataset` for the experiment. The `training_data` accesses the full dataset, and 20% of the dataset is allocated for validation (`validation_size = 0.2`):

```python
data = "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/creditcard.csv"

dataset = Dataset.Tabular.from_delimited_files(data)

automl_config = AutoMLConfig(compute_target = aml_remote_compute,
                             task = 'classification',
                             primary_metric = 'AUC_weighted',
                             training_data = dataset,
                             validation_size = 0.2,
                             label_column_name = 'Class'
                            )
```

## Perform k-fold cross-validation

To perform k-fold cross-validation, you include the `n_cross_validations` parameter and define the number of folds. This parameter sets how many cross validations to perform, based on the same number of folds.

> [!NOTE]
> In classification scenarios that use deep neural networks (DNN), the `n_cross_validations` parameter isn't supported.
> 
> For forecasting scenarios, see how cross validation is applied in [Set up AutoML to train a time-series forecasting model](how-to-auto-train-forecast.md#training-and-validation-data).
 
The following example defines five folds for cross-validation. The process runs five different trainings, where each training uses 4/5 of the data. Each validation uses 1/5 of the data with a different holdout fold each time. As a result, metrics are calculated with the average of the five validation metrics.

```python
data = "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/creditcard.csv"

dataset = Dataset.Tabular.from_delimited_files(data)

automl_config = AutoMLConfig(compute_target = aml_remote_compute,
                             task = 'classification',
                             primary_metric = 'AUC_weighted',
                             training_data = dataset,
                             n_cross_validations = 5
                             label_column_name = 'Class'
                            )
```

## Perform Monte Carlo cross-validation

To perform Monte Carlo cross validation, you include both the `validation_size` and `n_cross_validations` parameters in your `AutoMLConfig` object. 

For Monte Carlo cross validation, automated ML sets aside the portion of the training data specified by the `validation_size` parameter for validation, and then assigns the rest of the data for training. This process is then repeated based on the value specified in the `n_cross_validations` parameter, which generates new training and validation splits, at random, each time.

> [!NOTE]
> In forecasting scenarios, Monte Carlo cross-validation isn't supported.

The following example defines seven folds for cross-validation and 20% of the training data for validation. The process runs seven different trainings, where each training uses 80% of the data. Each validation uses 20% of the data with a different holdout fold each time.

```python
data = "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/creditcard.csv"

dataset = Dataset.Tabular.from_delimited_files(data)

automl_config = AutoMLConfig(compute_target = aml_remote_compute,
                             task = 'classification',
                             primary_metric = 'AUC_weighted',
                             training_data = dataset,
                             n_cross_validations = 7
                             validation_size = 0.2,
                             label_column_name = 'Class'
                            )
```

## Specify custom cross-validation data folds

You can also provide your own cross-validation (CV) data folds. This approach is considered a more advanced scenario because you specify which columns to split and use for validation. You include custom CV split columns in your training data and specify which columns by populating the column names in the `cv_split_column_names` parameter. Each column represents one cross-validation split and has an integer value of 1 or 0. A value of 1 indicates the row should be used for training. A value of 0 indicates the row should be used for validation.

> [!NOTE]
> In forecasting scenarios, the `cv_split_column_names` parameter isn't supported. 

The following example contains bank marketing data with two CV split columns `cv1` and `cv2`:

```python
data = "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_with_cv.csv"

dataset = Dataset.Tabular.from_delimited_files(data)

automl_config = AutoMLConfig(compute_target = aml_remote_compute,
                             task = 'classification',
                             primary_metric = 'AUC_weighted',
                             training_data = dataset,
                             label_column_name = 'y',
                             cv_split_column_names = ['cv1', 'cv2']
                            )
```

> [!NOTE]
> To use `cv_split_column_names` with `training_data` and `label_column_name`, please upgrade your Azure Machine Learning Python SDK version 1.6.0 or later. For previous SDK versions, please refer to using `cv_splits_indices`, but note that it is used with `X` and `y` dataset input only. 

## Set metric calculation for cross validation

When either k-fold or Monte Carlo cross validation is used, metrics are computed on each validation fold and then aggregated. The aggregation operation is an average for scalar metrics and a sum for charts. Metrics computed during cross validation are based on all folds and therefore all samples from the training set. For more information, see [Evaluate automated ML experiment results](../how-to-understand-automated-ml.md).

When either a custom validation set or an automatically selected validation set is used, model evaluation metrics are computed from only that validation set, not the  training data.

## Provide test dataset (preview)

[!INCLUDE [preview disclaimer](../includes/machine-learning-preview-generic-disclaimer.md)]

You can also provide test data to evaluate the recommended model that automated ML generates for you upon completion of the experiment. When you provide test data, the data is considered to be separate from training and validation to prevent any bias effect on the results of the test run of the recommended model. For more information, see [Training, validation, and test data](concept-automated-ml.md#training-validation-and-test-data).

> [!WARNING]
> The test dataset feature isn't available for the following automated ML scenarios:
>
> - [Computer vision tasks](../how-to-auto-train-image-models.md)
> - [Many models and hiearchical time-series (HTS) forecasting training (preview)](how-to-auto-train-forecast.md)
> - [Forecasting tasks where deep learning neural networks (DNN) are enabled](how-to-auto-train-forecast.md#enable-deep-learning)
> - [Automated ML runs from local computes or Azure Databricks clusters](how-to-configure-auto-train.md#compute-to-run-experiment)

Test datasets must be in the form of an [Azure Machine Learning TabularDataset](how-to-create-register-datasets.md#tabulardataset). You can specify a test dataset with the `test_data` and `test_size` parameters in your `AutoMLConfig` object. These parameters are mutually exclusive and can't be specified at the same time or with the `cv_split_column_names` or `cv_splits_indices` parameters.

In your `AutoMLConfig` object, use the `test_data` parameter to specify an existing dataset:

```python
automl_config = AutoMLConfig(task='forecasting',
                             ...
                             # Provide an existing test dataset
                             test_data=test_dataset,
                             ...
                             forecasting_parameters=forecasting_parameters)
```

To use a train/test split instead of providing test data directly, use the `test_size` parameter when creating the `AutoMLConfig`. This parameter must be a floating point value between 0.0 and 1.0 exclusive. It specifies the percentage of the training dataset to use for the test dataset.

```python
automl_config = AutoMLConfig(task = 'regression',
                             ...
                             # Specify train/test split
                             training_data=training_data,
                             test_size=0.2)
```

Here are some other considerations for working with a test dataset:

- For regression tasks, random sampling is used.
- For classification tasks, stratified sampling is used, but random sampling is used as a fallback when stratified sampling isn't feasible.

> [!NOTE]
> In forecasting scenarios, you can't currently specify a test dataset by using a train/test split with the `test_size` parameter.

Passing the `test_data` or `test_size` parameters into the `AutoMLConfig` object automatically triggers a remote test run upon completion of your experiment. This test run uses the provided test data to evaluate the best model that automated ML recommends. For more information, see [Get test job results](how-to-configure-auto-train.md#get-test-job-results).

## Related content

- [Prevent overfitting and imbalanced data with automated ML](../concept-manage-ml-pitfalls.md)
- [Set up automated ML to train a time-series forecasting model with the Python SDK (v1)](how-to-auto-train-forecast.md)
