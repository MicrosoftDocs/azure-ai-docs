---
title: Set up AutoML with Python
titleSuffix: Azure Machine Learning
description: Learn how to set up an AutoML training run with the Azure Machine Learning Python SDK using Azure Machine Learning automated ML.
author: CESARDELATORRE
ms.author: scottpolly
ms.reviewer: sooryar
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.date: 02/05/2026
ms.topic: how-to
ms.custom: UpdateFrequency5, devx-track-python, automl, sdkv1, dev-focus
ai-usage: ai-assisted
---

# Set up AutoML training with Python

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

In this article, you learn how to set up an automated machine learning (AutoML) training run by using the [Azure Machine Learning Python SDK](/python/api/overview/azure/ml/intro) and Azure Machine Learning automated ML. Automated ML selects an algorithm and hyperparameters for you and generates a model ready for deployment. This article provides details of the various options that you can use to configure automated ML experiments.

For an end-to-end example, see [Tutorial: AutoML- train regression model](how-to-auto-train-models-v1.md).

If you prefer a no-code experience, you can also [Set up no-code AutoML training in the Azure Machine Learning studio](../how-to-use-automated-ml-for-ml-models.md).

## Prerequisites

For this article, you need: 
* An Azure Machine Learning workspace. To create the workspace, see [Create workspace resources](../quickstart-create-resources.md).

* The Azure Machine Learning Python SDK installed.
    To install the SDK, use one of the following options: 
    * Create a compute instance. The compute instance automatically installs the SDK and is preconfigured for ML workflows. For more information, see [Create and manage an Azure Machine Learning compute instance](../how-to-create-compute-instance.md). 

    * [Install the `automl` package yourself](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/README.md#setup-using-a-local-conda-environment). The package includes the [default installation](/python/api/overview/azure/ml/install#default-install) of the SDK.

    [!INCLUDE [automl-sdk-version](../includes/machine-learning-automl-sdk-version.md)]
    
    > [!WARNING]
    > As of SDK v1.61.0, Python 3.10 is the minimum supported version for all automl packages. For the latest Python version support, see the [SDK release notes](/azure/machine-learning/azure-machine-learning-release-notes).

## Select your experiment type

Before you begin your experiment, determine the kind of machine learning problem you're solving. Automated machine learning supports task types of `classification`, `regression`, and `forecasting`. For more information, see [task types](../concept-automated-ml.md#when-to-use-automl-classification-regression-forecasting-computer-vision-and-nlp).

>[!NOTE]
>Support for natural language processing (NLP) tasks: image classification (multiclass and multilabel) and named entity recognition is available in public preview. [Learn more about NLP tasks in automated ML](../concept-automated-ml.md#nlp). 
>
> These preview capabilities are provided without a service-level agreement. Certain features might not be supported or might have constrained functionality. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

The following code uses the `task` parameter in the `AutoMLConfig` constructor to specify the experiment type as `classification`.

```python
from azureml.train.automl import AutoMLConfig

# task can be one of classification, regression, forecasting
automl_config = AutoMLConfig(task = "classification")
```

## Data source and format

Automated machine learning supports data that resides on your local desktop or in the cloud, such as Azure Blob Storage. You can read the data into a **Pandas DataFrame** or an **Azure Machine Learning TabularDataset**. [Learn more about datasets](../how-to-create-register-datasets.md).

Training data requirements for machine learning:
- Data must be in tabular form.
- The value to predict, or target column, must be in the data.

> [!IMPORTANT]
> Automated ML experiments don't support training with datasets that use [identity-based data access](../how-to-identity-based-data-access.md).

**For remote experiments**, the remote compute must access the training data. When working on a remote compute, Automated ML only accepts [Azure Machine Learning TabularDatasets](/python/api/azureml-core/azureml.data.tabulardataset). 

Azure Machine Learning datasets provide functionality to:

* Easily transfer data from static files or URL sources into your workspace.
* Make your data available to training scripts when running on cloud compute resources. See [How to train with datasets](how-to-train-with-datasets.md#mount-files-to-remote-compute-targets) for an example of using the `Dataset` class to mount data to your remote compute target.

The following code creates a TabularDataset from a web URL. See [Create a TabularDataset](how-to-create-register-datasets.md) for code examples on how to create datasets from other sources like local files and datastores.

```python
from azureml.core.dataset import Dataset
data = "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/creditcard.csv"
dataset = Dataset.Tabular.from_delimited_files(data)
```

**For local compute experiments**, use pandas dataframes for faster processing times.

  ```python
  import pandas as pd
  from sklearn.model_selection import train_test_split

  df = pd.read_csv("your-local-file.csv")
  train_data, test_data = train_test_split(df, test_size=0.1, random_state=42)
  label = "label-col-name"
  ```

## Training, validation, and test data

You can specify separate **training data and validation data sets** directly in the `AutoMLConfig` constructor. For more information, see [how to configure training, validation, cross validation, and test data](how-to-configure-cross-validation-data-splits.md) for your AutoML experiments. 

If you don't explicitly specify a `validation_data` or `n_cross_validation` parameter, automated ML applies default techniques to determine how validation is performed. This determination depends on the number of rows in the dataset assigned to your `training_data` parameter. 

|Training&nbsp;data&nbsp;size| Validation technique |
|---|-----|
|**Larger&nbsp;than&nbsp;20,000&nbsp;rows**| Train/validation data split is applied. The default is to take 10% of the initial training data set as the validation set. In turn, that validation set is used for metrics calculation.
|**Smaller&nbsp;than&nbsp;20,000&nbsp;rows**| Cross-validation approach is applied. The default number of folds depends on the number of rows. <br> **If the dataset is less than 1,000 rows**, 10 folds are used. <br> **If the rows are between 1,000 and 20,000**, then three folds are used.


> [!TIP] 
> You can upload **test data (preview)** to evaluate models that automated ML generated for you. These features are  [experimental](/python/api/overview/azure/ml/#stable-vs-experimental) preview capabilities, and might change at any time.
> Learn how to: 
> * [Pass in test data to your AutoMLConfig object](how-to-configure-cross-validation-data-splits.md#provide-test-dataset-preview). 
> * [Test the models automated ML generated for your experiment](#test-models-preview).
>  
> If you prefer a no-code experience, see [step 12 in Set up AutoML with the studio UI](../how-to-use-automated-ml-for-ml-models.md#create-and-run-experiment).


### Large data 

Automated ML supports a limited number of algorithms for training on large data that can successfully build models for big data on small virtual machines. Automated ML heuristics depend on properties such as data size, virtual machine memory size, experiment timeout, and featurization settings to determine if these large data algorithms should be applied. [Learn more about what models are supported in automated ML](#supported-models). 

* For regression, [Online Gradient Descent Regressor](/python/api/nimbusml/nimbusml.linear_model.onlinegradientdescentregressor?preserve-view=true&view=nimbusml-py-latest) and
[Fast Linear Regressor](/python/api/nimbusml/nimbusml.linear_model.fastlinearregressor?preserve-view=true&view=nimbusml-py-latest)

* For classification, [Averaged Perceptron Classifier](/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier?preserve-view=true&view=nimbusml-py-latest) and [Linear SVM Classifier](/python/api/nimbusml/nimbusml.linear_model.linearsvmbinaryclassifier?preserve-view=true&view=nimbusml-py-latest);  where the Linear SVM classifier has both large data and small data versions.

To override these heuristics, set the following values: 

Task | Setting | Notes
|---|---|---
Block&nbsp;data streaming algorithms | `blocked_models` in your `AutoMLConfig` object and list the models you don't want to use. | Results in either run failure or long run time
Use&nbsp;data&nbsp;streaming&nbsp;algorithms| `allowed_models` in your `AutoMLConfig` object and list the models you want to use.| 
Use&nbsp;data&nbsp;streaming&nbsp;algorithms <br> [(studio UI experiments)](../how-to-use-automated-ml-for-ml-models.md#create-and-run-experiment)|Block all models except the big data algorithms you want to use. |

## Compute to run experiment

Next, determine where the model is trained. An automated ML training experiment can run on the following compute options. 

 * **Choose a local compute**: If your scenario is about initial explorations or demos that use small data and short trains (that is, seconds or a couple of minutes per child run), training on your local computer might be a better choice.  There's no setup time, and the infrastructure resources (your PC or VM) are directly available. See [this notebook](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/local-run-classification-credit-card-fraud/auto-ml-classification-credit-card-fraud-local.ipynb) for a local compute example. 

 * **Choose a remote ML compute cluster**: If you're training with larger datasets like in production training creating models that need longer trains, remote compute provides better end-to-end time performance because `AutoML` parallelizes trains across the cluster's nodes. On a remote compute, the start-up time for the internal infrastructure adds around 1.5 minutes per child run, plus additional minutes for the cluster infrastructure if the VMs aren't yet up and running.[Azure Machine Learning Managed Compute](../concept-compute-target.md#azure-machine-learning-compute-managed) is a managed service that enables the ability to train machine learning models on clusters of Azure virtual machines. Compute instance is also supported as a compute target.

 * An **Azure Databricks cluster** in your Azure subscription. You can find more details in [Set up an Azure Databricks cluster for automated ML](how-to-configure-databricks-automl-environment.md). See this [GitHub site](https://github.com/Azure/azureml-examples/tree/v1-archive/v1/python-sdk/tutorials/automl-with-databricks) for examples of notebooks with Azure Databricks.

Consider these factors when choosing your compute target:

|  | Pros (Advantages)  |Cons (Handicaps)  |
|---------|---------|---------|---------|
|**Local compute target** |  <li> No environment start-up time   | <li>  Subset of features<li>  Can't parallelize runs <li> Worse for large data. <li>No data streaming while training <li>  No DNN-based featurization <li> Python SDK only |
|**Remote ML compute clusters**|  <li> Full set of features <li> Parallelize child runs <li>   Large data support<li>  DNN-based featurization <li>  Dynamic scalability of compute cluster on demand <li> No-code experience (web UI) also available  |  <li> Start-up time for cluster nodes <li> Start-up time for each child run    |

<a name='configure-experiment'></a>

## Configure your experiment settings

You can use several options to configure your automated ML experiment. Set these parameters by instantiating an `AutoMLConfig` object. For a full list of parameters, see the [AutoMLConfig class](/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig).

The following example is for a classification task. The experiment uses AUC weighted as the [primary metric](#primary-metric) and has an experiment timeout set to 30 minutes and 2 cross-validation folds.

```python
    automl_classifier=AutoMLConfig(task='classification',
                                   primary_metric='AUC_weighted',
                                   experiment_timeout_minutes=30,
                                   blocked_models=['XGBoostClassifier'],
                                   training_data=train_data,
                                   label_column_name=label,
                                   n_cross_validations=2)
```
You can also configure forecasting tasks, which requires extra setup. For more information, see [Set up AutoML for time-series forecasting](../how-to-auto-train-forecast.md). 

```python
    time_series_settings = {
                            'time_column_name': time_column_name,
                            'time_series_id_column_names': time_series_id_column_names,
                            'forecast_horizon': n_test_periods
                           }
    
    automl_config = AutoMLConfig(
                                 task = 'forecasting',
                                 debug_log='automl_oj_sales_errors.log',
                                 primary_metric='normalized_root_mean_squared_error',
                                 experiment_timeout_minutes=20,
                                 training_data=train_data,
                                 label_column_name=label,
                                 n_cross_validations=5,
                                 path=project_folder,
                                 verbosity=logging.INFO,
                                 **time_series_settings
                                )
```
    
### Supported models

Automated machine learning tries different models and algorithms during the automation and tuning process. As a user, you don't need to specify the algorithm. 

The three different `task` parameter values determine the list of algorithms, or models, to apply. Use the `allowed_models` or `blocked_models` parameters to further modify iterations by including or excluding available models. 
The following table summarizes the supported models by task type. 

> [!NOTE]
> If you plan to export your automated ML created models to an [ONNX model](../concept-onnx.md), only those algorithms indicated with an * (asterisk) can be converted to the ONNX format. Learn more about [converting models to ONNX](../concept-automated-ml.md#use-with-onnx). <br> <br> Also note, ONNX only supports classification and regression tasks at this time. 
> 
Classification | Regression | Time Series Forecasting
|-- |-- |--
[Logistic Regression](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#logisticregression----logisticregression-)* | [Elastic Net](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#elasticnet----elasticnet-)* | [AutoARIMA](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.forecasting#autoarima----autoarima-)
[Light GBM](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#lightgbmclassifier----lightgbm-)* | [Light GBM](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#lightgbmregressor----lightgbm-)* | [Prophet](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#prophet----prophet-)
[Gradient Boosting](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#gradientboosting----gradientboosting-)* | [Gradient Boosting](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#gradientboostingregressor----gradientboosting-)* | [Elastic Net](https://scikit-learn.org/stable/modules/linear_model.html#elastic-net)
[Decision Tree](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#decisiontree----decisiontree-)* |[Decision Tree](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#decisiontreeregressor----decisiontree-)* |[Light GBM](https://lightgbm.readthedocs.io/en/latest/index.html)
[K Nearest Neighbors](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#knearestneighborsclassifier----knn-)* |[K Nearest Neighbors](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#knearestneighborsregressor----knn-)* | [Gradient Boosting](https://scikit-learn.org/stable/modules/ensemble.html#regression)
[Linear SVC](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#linearsupportvectormachine----linearsvm-)* |[LARS Lasso](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#lassolars----lassolars-)* | [Decision Tree](https://scikit-learn.org/stable/modules/tree.html#regression)
[Support Vector Classification (SVC)](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#supportvectormachine----svm-)* |[Stochastic Gradient Descent (SGD)](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#sgdregressor----sgd-)* | [Arimax](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#arimax----arimax-)
[Random Forest](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#randomforest----randomforest-)* | [Random Forest](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#randomforestregressor----randomforest-) | [LARS Lasso](https://scikit-learn.org/stable/modules/linear_model.html#lars-lasso)
[Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees)* | [Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees)* | [Stochastic Gradient Descent (SGD)](https://scikit-learn.org/stable/modules/sgd.html#regression)
[Xgboost](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#xgboostclassifier----xgboostclassifier-)* |[Xgboost](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#xgboostregressor----xgboostregressor-)* | [Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)
[Averaged Perceptron Classifier](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#averagedperceptronclassifier----averagedperceptronclassifier-)| [Online Gradient Descent Regressor](/python/api/nimbusml/nimbusml.linear_model.onlinegradientdescentregressor?preserve-view=true&view=nimbusml-py-latest) | [Xgboost](https://xgboost.readthedocs.io/en/latest/parameter.html)
[Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html#bernoulli-naive-bayes)* |[Fast Linear Regressor](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#fastlinearregressor----fastlinearregressor-)| [ForecastTCN](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#tcnforecaster----tcnforecaster-)
[Stochastic Gradient Descent (SGD)](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#sgdclassifier----sgd-)* || Naive
[Linear SVM Classifier](/python/api/nimbusml/nimbusml.linear_model.linearsvmbinaryclassifier?preserve-view=true&view=nimbusml-py-latest)* || SeasonalNaive
||| Average
||| SeasonalAverage
||| [ExponentialSmoothing](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#exponentialsmoothing----exponentialsmoothing-) 

### Primary metric

The `primary_metric` parameter sets the metric used during model training for optimization. The task type you choose determines the available metrics.

Many factors influence the choice of a primary metric for automated ML optimization. Choose a metric that best represents your business needs. Then, consider if the metric fits your dataset profile, including data size, range, and class distribution. The following sections summarize the recommended primary metrics based on task type and business scenario. 

For specific definitions of these metrics, see [Understand automated machine learning results](../how-to-understand-automated-ml.md).

#### Metrics for classification scenarios 

Threshold-dependent metrics, like `accuracy`, `recall_score_weighted`, `norm_macro_recall`, and `precision_score_weighted` might not optimize as well for datasets that are small, have large class skew (class imbalance), or when the expected metric value is very close to 0.0 or 1.0. In those cases, `AUC_weighted` can be a better choice for the primary metric. After automated ML completes, you can choose the best model based on the metric that fits your business needs.

| Metric | Example use case |
| ------ | ------- |
| `accuracy` | Image classification, Sentiment analysis, Churn prediction |
| `AUC_weighted` | Fraud detection, Image classification, Anomaly detection/spam detection |
| `average_precision_score_weighted` | Sentiment analysis |
| `norm_macro_recall` | Churn prediction |
| `precision_score_weighted` |  |

#### Metrics for regression scenarios

`r2_score`, `normalized_mean_absolute_error`, and `normalized_root_mean_squared_error` all try to minimize prediction errors. `r2_score` and `normalized_root_mean_squared_error` both minimize average squared errors while `normalized_mean_absolute_error` minimizes the average absolute value of errors. Absolute value treats errors at all magnitudes alike and squared errors give a larger penalty for errors with larger absolute values. Depending on whether larger errors should be punished more or not, choose to optimize squared error or absolute error.

The main difference between `r2_score` and `normalized_root_mean_squared_error` is the way they're normalized and their meanings. `normalized_root_mean_squared_error` is root mean squared error normalized by range and can be interpreted as the average error magnitude for prediction. `r2_score` is mean squared error normalized by an estimate of variance of data. It's the proportion of variation that the model captures. 

> [!Note]
> `r2_score` and `normalized_root_mean_squared_error` also behave similarly as primary metrics. If a fixed validation set is applied, these two metrics optimize the same target, mean squared error, and the same model optimizes them. When you apply cross-validation and only a training set is available, they differ slightly as the normalizer for `normalized_root_mean_squared_error` is fixed as the range of training set, but the normalizer for `r2_score` varies for every fold as it's the variance for each fold.

If the rank, instead of the exact value is of interest, `spearman_correlation` can be a better choice as it measures the rank correlation between real values and predictions.

However, currently no primary metrics for regression address relative difference. All of `r2_score`, `normalized_mean_absolute_error`, and `normalized_root_mean_squared_error` treat a $20,000 prediction error the same for a worker with a $30,000 salary as a worker making $20 million, if these two data points belong to the same dataset for regression, or the same time series specified by the time series identifier. While in reality, predicting only $20,000 off from a $20 million salary is very close (a small 0.1% relative difference), whereas $20,000 off from $30,000 isn't close (a large 67% relative difference). To address the issue of relative difference, train a model with available primary metrics, and then select the model with best `mean_absolute_percentage_error` or `root_mean_squared_log_error`.

| Metric | Example use case |
| ------ | ------- |
| `spearman_correlation` | |
| `normalized_root_mean_squared_error` | Price prediction (house/product/tip), Review score prediction |
| `r2_score` | Airline delay, Salary estimation, Bug resolution time |
| `normalized_mean_absolute_error` |  |

#### Metrics for time series forecasting scenarios

The recommendations are similar to those noted for regression scenarios. 

| Metric | Example use case |
| ------ | ------- |
| `normalized_root_mean_squared_error` | Price prediction (forecasting), Inventory optimization, Demand forecasting | 
| `r2_score` | Price prediction (forecasting), Inventory optimization, Demand forecasting |
| `normalized_mean_absolute_error` | |

### Data featurization

In every automated ML experiment, the system automatically scales and normalizes your data to help *certain* algorithms that are sensitive to features that are on different scales. This scaling and normalization is referred to as featurization. 
See [Featurization in AutoML](how-to-configure-auto-features.md) for more detail and code examples. 

> [!NOTE]
> Automated machine learning featurization steps, such as feature normalization, handling missing data, and converting text to numeric, become part of the underlying model. When you use the model for predictions, the same featurization steps applied during training are automatically applied to your input data.

When you configure your experiments in your `AutoMLConfig` object, you can enable or disable the setting `featurization`. The following table shows the accepted settings for featurization in the [AutoMLConfig object](/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig). 

|Featurization Configuration | Description |
| ------------- | ------------- |
|`"featurization": 'auto'`| Indicates that as part of preprocessing, [data guardrails and featurization steps](how-to-configure-auto-features.md#featurization) are performed automatically. **Default setting**.|
|`"featurization": 'off'`| Indicates the featurization step shouldn't be done automatically.|
|`"featurization":`&nbsp;`'FeaturizationConfig'`| Indicates a customized featurization step should be used. [Learn how to customize featurization](how-to-configure-auto-features.md#customize-featurization).|



<a name="ensemble"></a>

### Ensemble configuration

Ensemble models are enabled by default and appear as the final run iterations in an AutoML run. Currently, **VotingEnsemble** and **StackEnsemble** are supported. 

Voting implements soft voting, which uses weighted averages. The stacking implementation uses a two-layer implementation, where the first layer has the same models as the voting ensemble, and the second layer model is used to find the optimal combination of the models from the first layer. 

If you're using ONNX models or enable model explainability, stacking is disabled and only voting is utilized.

Disable ensemble training by setting the `enable_voting_ensemble` and `enable_stack_ensemble` boolean parameters to `false`.

```python
automl_classifier = AutoMLConfig(
                                 task='classification',
                                 primary_metric='AUC_weighted',
                                 experiment_timeout_minutes=30,
                                 training_data=data_train,
                                 label_column_name=label,
                                 n_cross_validations=5,
                                 enable_voting_ensemble=False,
                                 enable_stack_ensemble=False
                                )
```

To alter the default ensemble behavior, provide multiple default arguments as `kwargs` in an `AutoMLConfig` object.

> [!IMPORTANT]
>  The following parameters aren't explicit parameters of the AutoMLConfig class. 
* `ensemble_download_models_timeout_sec`: During **VotingEnsemble** and **StackEnsemble** model generation, the process downloads multiple fitted models from the previous child runs. If you encounter this error: `AutoMLEnsembleException: Could not find any models for running ensembling`, then you might need to provide more time for the models to be downloaded. The default value is 300 seconds for downloading these models in parallel and there's no maximum timeout limit. Configure this parameter with a higher value than 300 seconds, if more time is needed. 

  > [!NOTE]
  >  If the timeout is reached and the process downloaded models, then ensembling proceeds with as many models as it has. It's not required that all the models finish downloading within that timeout.
The following parameters only apply to **StackEnsemble** models: 

* `stack_meta_learner_type`: the meta-learner is a model trained on the output of the individual heterogeneous models. Default meta-learners are `LogisticRegression` for classification tasks (or `LogisticRegressionCV` if cross-validation is enabled) and `ElasticNet` for regression, forecasting tasks (or `ElasticNetCV` if cross-validation is enabled). This parameter can be one of the following strings: `LogisticRegression`, `LogisticRegressionCV`, `LightGBMClassifier`, `ElasticNet`, `ElasticNetCV`, `LightGBMRegressor`, or `LinearRegression`.

* `stack_meta_learner_train_percentage`: specifies the proportion of the training set (when choosing train and validation type of training) to reserve for training the meta-learner. The default value is `0.2`. 

* `stack_meta_learner_kwargs`: optional parameters to pass to the initializer of the meta-learner. These parameters and parameter types mirror the parameters and parameter types from the corresponding model constructor, and are forwarded to the model constructor.

The following code shows an example of specifying custom ensemble behavior in an `AutoMLConfig` object.

```python
ensemble_settings = {
                     "ensemble_download_models_timeout_sec": 600
                     "stack_meta_learner_type": "LogisticRegressionCV",
                     "stack_meta_learner_train_percentage": 0.3,
                     "stack_meta_learner_kwargs": {
                                                    "refit": True,
                                                    "fit_intercept": False,
                                                    "class_weight": "balanced",
                                                    "multi_class": "auto",
                                                    "n_jobs": -1
                                                  }
                    }
automl_classifier = AutoMLConfig(
                                 task='classification',
                                 primary_metric='AUC_weighted',
                                 experiment_timeout_minutes=30,
                                 training_data=train_data,
                                 label_column_name=label,
                                 n_cross_validations=5,
                                 **ensemble_settings
                                )
```

<a name="exit"></a> 

### Exit criteria

You can define several options in your AutoMLConfig to end your experiment.

|Criteria| Description
|----|----
No&nbsp;criteria | If you don't define any exit parameters, the experiment continues until no further progress is made on your primary metric.
After&nbsp;a&nbsp;length&nbsp;of&nbsp;time| Use `experiment_timeout_minutes` in your settings to define how long, in minutes, your experiment should continue to run. <br><br> To help avoid experiment time out failures, there's a minimum of 15 minutes, or 60 minutes if your row by column size exceeds 10 million.
A&nbsp;score&nbsp;has&nbsp;been&nbsp;reached| Use `experiment_exit_score` completes the experiment after a specified primary metric score is reached.

## Run experiment

> [!WARNING]
> If you run an experiment with the same configuration settings and primary metric multiple times, you likely see variation in each experiment's final metrics score and generated models. The algorithms automated ML employs have inherent randomness that can cause slight variation in the models output by the experiment and the recommended model's final metrics score, like accuracy. You likely also see results with the same model name, but different hyperparameters used. 

For automated ML, you create an `Experiment` object, which is a named object in a `Workspace` used to run experiments.

```python
from azureml.core.experiment import Experiment

ws = Workspace.from_config()

# Choose a name for the experiment and specify the project folder.
experiment_name = 'Tutorial-automl'
project_folder = './sample_projects/automl-classification'

experiment = Experiment(ws, experiment_name)
```

Submit the experiment to run and generate a model. Pass the `AutoMLConfig` to the `submit` method to generate the model.

```python
run = experiment.submit(automl_config, show_output=True)
```

>[!NOTE]
>Dependencies are first installed on a new machine.  It might take up to 10 minutes before output is shown.
>Setting `show_output` to `True` results in output being shown on the console.

### Multiple child runs on clusters

Automated ML experiment child runs can be performed on a cluster that is already running another experiment. However, the timing depends on how many nodes the cluster has, and if those nodes are available to run a different experiment.

Each node in the cluster acts as an individual virtual machine (VM) that can accomplish a single training run; for automated ML this means a child run. If all the nodes are busy, the new experiment is queued. But if there are free nodes, the new experiment runs automated ML child runs in parallel in the available nodes/VMs.

To help manage child runs and when they can be performed, we recommend you create a dedicated cluster per experiment, and match the number of `max_concurrent_iterations` of your experiment to the number of nodes in the cluster. This way, you use all the nodes of the cluster at the same time with the number of concurrent child runs/iterations you want.

Configure  `max_concurrent_iterations` in your `AutoMLConfig` object. If it isn't configured, then by default only one concurrent child run/iteration is allowed per experiment.
In case of compute instance, `max_concurrent_iterations` can be set to be the same as number of cores on the compute instance VM.

## Explore models and metrics

Automated ML offers options for you to monitor and evaluate your training results. 

* You can view your training results in a widget or inline if you are in a notebook. See [Monitor automated machine learning runs](#monitor) for more details.

* For definitions and examples of the performance charts and metrics provided for each run, see [Evaluate automated machine learning experiment results](../how-to-understand-automated-ml.md).

* To get a featurization summary and understand what features were added to a particular model, see [Featurization transparency](how-to-configure-auto-features.md#featurization-transparency). 

You can view the hyperparameters, the scaling and normalization techniques, and algorithm applied to a specific automated ML run with the [custom code solution, `print_model()`](how-to-configure-auto-features.md#scaling-and-normalization). 

> [!TIP]
> Automated ML also let's you [view the generated model training code for AutoML trained models](how-to-generate-automl-training-code.md). This functionality is in public preview and can change at any time. 

## <a name="monitor"></a> Monitor automated machine learning runs

For automated ML runs, to access the charts from a previous run, replace `<<experiment_name>>` with the appropriate experiment name:

```python
from azureml.widgets import RunDetails
from azureml.core.run import Run

experiment = Experiment (workspace, <<experiment_name>>)
run_id = 'autoML_my_runID' #replace with run_ID
run = Run(experiment, run_id)
RunDetails(run).show()
```

![Jupyter notebook widget for Automated Machine Learning](../media/how-to-configure-auto-train/azure-machine-learning-auto-ml-widget.png)

## Test models (preview)

>[!IMPORTANT]
> Testing your models by using a test dataset to evaluate automated ML generated models is a preview feature. This capability is an [experimental](/python/api/overview/azure/ml/#stable-vs-experimental) preview feature, and might change at any time.

> [!WARNING]
> This feature isn't available for the following automated ML scenarios:
>  * [Computer vision tasks](../how-to-auto-train-image-models.md)
>  * [Many models and hiearchical time series forecasting training (preview)](../how-to-auto-train-forecast.md)
>  * [Forecasting tasks where deep learning neural networks (DNN) are enabled](../how-to-auto-train-forecast.md#enable-learning-for-deep-neural-networks)
>  * [Automated ML runs from local computes or Azure Databricks clusters](../how-to-configure-auto-train.md#compute-to-run-experiment)

If you pass the `test_data` or `test_size` parameters into the `AutoMLConfig`, you automatically trigger a remote test run that uses the provided test data to evaluate the best model that automated ML recommends upon completion of the experiment. This remote test run happens at the end of the experiment, once the best model is determined. For more information, see how to [pass test data into your `AutoMLConfig`](how-to-configure-cross-validation-data-splits.md#provide-test-dataset-preview). 

### Get test job results 

You can get the predictions and metrics from the remote test job from the [Azure Machine Learning studio](../how-to-use-automated-ml-for-ml-models.md#view-remote-test-job-results-preview) or by using the following code. 


```python
best_run, fitted_model = remote_run.get_output()
test_run = next(best_run.get_children(type='automl.model_test'))
test_run.wait_for_completion(show_output=False, wait_post_processing=True)

# Get test metrics
test_run_metrics = test_run.get_metrics()
for name, value in test_run_metrics.items():
    print(f"{name}: {value}")

# Get test predictions as a Dataset
test_run_details = test_run.get_details()
dataset_id = test_run_details['outputDatasets'][0]['identifier']['savedId']
test_run_predictions = Dataset.get_by_id(workspace, dataset_id)
predictions_df = test_run_predictions.to_pandas_dataframe()

# Alternatively, the test predictions can be retrieved via the run outputs.
test_run.download_file("predictions/predictions.csv")
predictions_df = pd.read_csv("predictions.csv")

```

The model test job generates the predictions.csv file that's stored in the default datastore created with the workspace. All users with the same subscription can see this datastore. Test jobs aren't recommended for scenarios where any of the information used for or created by the test job needs to remain private.

### Test existing automated ML model

To test other existing automated ML models, such as the best job or a child job, use [`ModelProxy()`](/python/api/azureml-train-automl-client/azureml.train.automl.model_proxy.modelproxy). This method tests a model after the main AutoML run finishes. `ModelProxy()` already returns the predictions and metrics, so you don't need any extra processing to get the outputs.

> [!NOTE]
> ModelProxy is an [experimental](/python/api/overview/azure/ml/#stable-vs-experimental) preview class and might change at any time.

The following code shows how to test a model from any run by using the [ModelProxy.test()](/python/api/azureml-train-automl-client/azureml.train.automl.model_proxy.modelproxy#test-test-data--azureml-data-abstract-dataset-abstractdataset--include-predictions-only--bool---false-----typing-tuple-azureml-data-abstract-dataset-abstractdataset--typing-dict-str--typing-any--) method. In the `test()` method, you can specify if you want to see only the predictions from the test run by using the `include_predictions_only` parameter. 

```python
from azureml.train.automl.model_proxy import ModelProxy

model_proxy = ModelProxy(child_run=my_run, compute_target=cpu_cluster)
predictions, metrics = model_proxy.test(test_data, include_predictions_only= True
)
```

## Register and deploy models

After you test a model and confirm you want to use it in production, register it for later use. 

To register a model from an automated ML run, use the [`register_model()`](/python/api/azureml-train-automl-client/azureml.train.automl.run.automlrun#register-model-model-name-none--description-none--tags-none--iteration-none--metric-none-) method. 

```Python

best_run = run.get_best_child()
print(fitted_model.steps)

model_name = best_run.properties['model_name']
description = 'AutoML forecast example'
tags = None

model = run.register_model(model_name = model_name, 
                                  description = description, 
                                  tags = tags)
```


For details on how to create a deployment configuration and deploy a registered model to a web service, see [how and where to deploy a model](../how-to-deploy-online-endpoints.md).

> [!TIP]
> For registered models, one-click deployment is available through the [Azure Machine Learning studio](https://ml.azure.com). See [how to deploy registered models from the studio](../how-to-use-automated-ml-for-ml-models.md#deploy-your-model). 
<a name="explain"></a>

## Model interpretability

Model interpretability helps you understand why your models made predictions and reveals the underlying feature importance values. The SDK includes various packages that enable model interpretability features during both training and inference, for local and deployed models.

See how to [enable interpretability features](how-to-machine-learning-interpretability-automl.md) specifically within automated ML experiments.

For general information on how to enable model explanations and feature importance in other areas of the SDK outside of automated machine learning, see the [concept article on interpretability](../how-to-machine-learning-interpretability.md).

> [!NOTE]
> The ForecastTCN model isn't currently supported by the Explanation Client. This model doesn't return an explanation dashboard if it's returned as the best model, and it doesn't support on-demand explanation runs.

## Next steps

+ Learn more about [how and where to deploy a model](../how-to-deploy-online-endpoints.md).

+ Learn more about [how to train a regression model with Automated machine learning](how-to-auto-train-models-v1.md).

+ [Troubleshoot automated ML experiments](how-to-troubleshoot-auto-ml.md).
