---
title: Data Featurization in Automated Machine Learning
titleSuffix: Azure Machine Learning
description: Learn how to customize data featurization settings for your automated machine learning experiments in Azure Machine Learning.
author: manashgoswami
ms.author: manashg
ms.reviewer: ssalgado
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: how-to
ms.custom: UpdateFrequency5, automl, sdkv1
ms.date: 04/02/2025
monikerRange: 'azureml-api-1'
---

# Data featurization in automated machine learning (AutoML)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

This article explains how to customize the data featurization settings in Azure Machine Learning for your [automated machine learning (AutoML) experiments](../concept-automated-ml.md).

## Feature engineering and featurization

Training data consists of rows and columns. Each row is an observation or record, and the columns of each row are the features that describe each record. Typically, the features that best characterize the patterns in the data are selected to create predictive models.

Although many of the raw data fields can be used directly to train a model, it's often necessary to create other (engineered) features that provide information to better differentiate patterns in the data. This process is called *feature engineering*, where the use of domain knowledge of the data is used to create features that, in turn, help machine learning algorithms to learn better.

In Azure Machine Learning, data-scaling and normalization techniques are applied to make feature engineering easier. Collectively, these techniques and this feature engineering are called *featurization* in AutoML experiments.

## Prerequisites

This article assumes that you already know how to configure an AutoML experiment.

[!INCLUDE [automl-sdk-version](../includes/machine-learning-automl-sdk-version.md)]

For information about configuration, see the following articles:

- For a code-first experience: [Set up AutoML training with Python](how-to-configure-auto-train.md)
- For a no-code experience: [Set up no-code AutoML training for tabular data with the studio UI](../how-to-use-automated-ml-for-ml-models.md)

## Configure featurization

In every AutoML experiment, [automatic scaling and normalization techniques](#featurization) are applied to your data by default. These techniques are types of featurization that help *certain* algorithms that are sensitive to features on different scales. You can enable more featurization, such as *missing-values imputation*, *encoding*, and *transforms*.

> [!NOTE]
> Steps for AutoML featurization (such as feature normalization, handling missing data,
> or converting text to numeric) become part of the underlying model. When you use the model for
> predictions, the same featurization steps that are applied during training are applied to
> your input data automatically.

For experiments that you configure with the Python SDK, you can enable or disable the featurization setting and further specify the featurization steps to be used for your experiment. If you're using the Azure Machine Learning studio, see the [steps to enable featurization](../how-to-use-automated-ml-for-ml-models.md#customize-featurization).

The following table shows the accepted settings for `featurization` in the [AutoMLConfig class](/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig):

|Featurization configuration | Description|
------------- | ------------- |
|`"featurization": 'auto'`| Specifies that, as part of preprocessing, [data guardrails](#data-guardrails) and [featurization steps](#featurization) are to be done automatically. This setting is the default.|
|`"featurization": 'off'`| Specifies that featurization steps aren't to be done automatically.|
|`"featurization": 'FeaturizationConfig'`| Specifies that customized featurization steps are to be used. To learn more, see [Customize featurization](#customize-featurization).|

<a name="featurization"></a>

## Automatic featurization

The following table summarizes techniques that are automatically applied to your data. These techniques are applied for experiments that are configured by using the SDK or the studio UI. To disable this behavior, set `"featurization": 'off'` in your `AutoMLConfig` object.

|Featurization steps| Description |
| ------------- | ------------- |
|**Drop high cardinality or no variance features*** |Drop these features from training and validation sets. Applies to features with all values missing, with the same value across all rows, or with high cardinality (for example, hashes, IDs, or GUIDs).|
|**Impute missing values*** |For numeric features, impute with the average of values in the column.<br><br>For categorical features, impute with the most frequent value.|
|**Generate more features*** |For *DateTime* features: year, month, day, day of week, day of year, quarter, week of the year, hour, minute, second.<br><br> *For forecasting tasks*, these additional DateTime features are created: ISO year, half - half-year, calendar month as string, week, day of week as string, day of quarter, day of year, AM/PM (0 for am, 1 for pm), AM/PM as string, hour of day (12-hr basis).<br><br>For *Text* features: term frequency based on unigrams, bigrams, and trigrams. To learn more, see [BERT integration](#bert-integration).|
|**Transform and encode***|Transform numeric features that have few unique values into categorical features.<br><br>*One-hot encoding* is used for low-cardinality categorical features. *One-hot-hash encoding* is used for high-cardinality categorical features.|
|**Word embeddings**|A text featurizer converts vectors of text tokens into sentence vectors by using a pretrained model. Each word's embedding vector in a document is aggregated with the rest to produce a document feature vector.|
|**Cluster distance**|Trains a k-means clustering model on all numeric columns. Produces *k* new features (one new numeric feature per cluster) that contain the distance of each sample to the centroid of each cluster.|

> [!NOTE]
> \*If you plan to export your AutoML-created models to an [ONNX model](../concept-onnx.md), only the featurization options indicated with an asterisk are supported in the ONNX format. To learn more, see [Make predictions with an AutoML ONNX model](../how-to-use-automl-onnx-model-dotnet.md).

In every AutoML experiment, your data is automatically scaled or normalized to help algorithms perform well. During model training, one of the following scaling or normalization techniques are applied to each model.

|Scaling & processing| Description |
| ------------- | ------------- |
| [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)  | Standardizes features by removing the mean and scaling to unit variance.  |
| [MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)  | Transforms features by scaling each feature by that column's minimum and maximum.  |
| [MaxAbsScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MaxAbsScaler.html#sklearn.preprocessing.MaxAbsScaler) |Scales each feature by its maximum absolute value. |
| [RobustScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html) | Scales features by their quantile range. |
| [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) |Principal component analysis. Linear dimensionality reduction using Singular Value Decomposition of the data to project it to a lower dimensional space. |
| [TruncatedSVD](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html) |This transformer performs linear dimensionality reduction by using truncated singular value decomposition (SVD). Contrary to PCA, this estimator doesn't center the data before computing the singular value decomposition, which means it can work with `scipy.sparse` matrices efficiently. |
| [Normalizer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html) | Each sample (that is, each row of the data matrix) with at least one nonzero component is rescaled independently of other samples so that its norm (l1 or l2) equals one. |

## Data guardrails

*Data guardrails* help you identify potential issues with your data, such as missing values or [imbalanced data](../concept-manage-ml-pitfalls.md#identify-models-with-imbalanced-data). They also help you take corrective actions for improved results.

Data guardrails are applied:

- **For SDK experiments**: When the parameters `"featurization": 'auto'` or `validation=auto` are specified in your `AutoMLConfig` object.
- **For studio experiments**: When automatic featurization is enabled.

You can review the data guardrails for your experiment:

- By setting `show_output=True` when you submit an experiment by using the SDK.
- In the studio, on the **Data guardrails** tab of your AutoML run.

### Data guardrail states

Data guardrails display one of three states:

|State| Description |
|----|---- |
|**Passed**| No data problems were detected and no action is required by you. |
|**Done**| Changes were applied to your data. We encourage you to review the corrective actions that AutoML took, to ensure that the changes align with the expected results. |
|**Alerted**| A data issue was detected but couldn't be remedied. We encourage you to revise and fix the issue.|

### Supported data guardrails

The following table describes the data guardrails that are currently supported and the associated statuses that you might see when you submit your experiment:

|Guardrail|Status|Condition for trigger|
|---|---|---|
|**Missing feature values imputation** |Passed <br><br><br> Done| No missing feature values were detected in your training data. To learn more, see [Configure featurization settings](../how-to-use-automated-ml-for-ml-models.md#customize-featurization). <br><br> Missing feature values were detected in your training data and were imputed. |
|**High cardinality feature detection** |Passed <br><br><br> Done| Your inputs were analyzed, and no high-cardinality features were detected. <br><br> High-cardinality features were detected in your inputs and were handled. |
|**Validation split handling** |Done| The validation configuration was set to `'auto'` and the training data contained *fewer than 20,000 rows*. <br> Each iteration of the trained model was validated by using cross-validation. Learn more about [validation data](how-to-configure-auto-train.md#training-validation-and-test-data). <br><br> The validation configuration was set to `'auto'`, and the training data contained *more than 20,000 rows*. <br> The input data has been split into a training dataset and a validation dataset for validation of the model. |
|**Class balancing detection** |Passed <br><br><br><br><br> Alerted <br><br><br><br> Done | Your inputs were analyzed, and all classes are balanced in your training data. A dataset is considered to be balanced if each class has good representation in the dataset, as measured by number and ratio of samples. <br><br> Imbalanced classes were detected in your inputs. To fix model bias, fix the balancing problem. Learn more about [imbalanced data](../concept-manage-ml-pitfalls.md#identify-models-with-imbalanced-data).<br><br> Imbalanced classes were detected in your inputs and the sweeping logic has determined to apply balancing. |
|**Memory issues detection** |Passed <br><br><br><br> Done |The selected values (horizon, lag, rolling window) were analyzed, and no potential out-of-memory issues were detected. Learn more about time-series [forecasting configurations](how-to-auto-train-forecast.md#configuration-settings). <br><br>The selected values (horizon, lag, rolling window) were analyzed and will potentially cause your experiment to run out of memory. The lag or rolling-window configurations are turned off. |
|**Frequency detection** |Passed <br><br><br> Done |The time series was analyzed, and all data points are aligned with the detected frequency. <br> <br> The time series was analyzed, and data points that don't align with the detected frequency were detected. These data points were removed from the dataset.|
|**Cross validation** |Done| In order to accurately evaluate the model trained by AutoML, we use a dataset that the model isn't trained on. Hence, if the user doesn't provide an explicit validation dataset, a part of the training dataset is used to achieve this. For smaller datasets (fewer than 20,000 samples), cross-validation is used, else a single hold-out set is split from the training data to serve as the validation dataset. Hence, for your input data we use cross-validation with 10 folds, if the number of training samples are fewer than 1000, and 3 folds in all other cases.|
|**Train-test data split** |Done| In order to accurately evaluate the model trained by AutoML, we use a dataset that the model isn't trained on. Hence, if the user doesn't provide an explicit validation dataset, a part of the training dataset is used to achieve this. For smaller datasets (fewer than 20,000 samples), cross-validation is used, else a single hold-out set is split from the training data to serve as the validation dataset. Hence, your input data is split into a training dataset and a holdout validation dataset.|
|**Time series ID detection** |Passed <br><br><br> Fixed |The data set was analyzed, and no duplicate time index were detected. <br> <br> Multiple time series were found in the dataset, and the time series identifiers were automatically created for your dataset.|
|**Time series aggregation** |Passed <br><br><br> Fixed |The dataset frequency is aligned with the user specified frequency. No aggregation was performed. <br> <br> The data was aggregated to comply with user provided frequency.|
|**Short series handling** |Passed <br><br><br> Fixed |AutoML detected enough data points for each series in the input data to continue with training. <br> <br> AutoML detected that some series didn't contain enough data points to train a model. To continue with training, these short series were dropped or padded.|

## Customize featurization

You can customize your featurization settings to ensure that the data and features that are used to train your machine learning model result in relevant predictions.

To customize featurizations, specify `"featurization": FeaturizationConfig` in your `AutoMLConfig` object. If you're using the Azure Machine Learning studio for your experiment, see the [Configure featurization settings](../how-to-use-automated-ml-for-ml-models.md#customize-featurization). To customize featurization for forecastings task types, refer to the [Customize featurization](how-to-auto-train-forecast.md#customize-featurization).

Supported customizations include:

|Customization|Definition|
|--|--|
|**Column purpose update**|Override the autodetected feature type for the specified column.|
|**Transformer parameter update** |Update the parameters for the specified transformer. Currently supports *Imputer* (mean, most frequent, and median) and *HashOneHotEncoder*.|
|**Drop columns*** |Specifies columns to drop from being featurized.|
|**Block transformers**| Specifies block transformers to be used in the featurization process.|

>[!NOTE]
> *The **drop columns** functionality is deprecated as of SDK version 1.19. Drop columns from your dataset as part of data cleansing, before consuming it in your AutoML experiment.

You can create the `FeaturizationConfig` object by using API calls:

```python
featurization_config = FeaturizationConfig()
featurization_config.blocked_transformers = ['LabelEncoder']
featurization_config.drop_columns = ['aspiration', 'stroke']
featurization_config.add_column_purpose('engine-size', 'Numeric')
featurization_config.add_column_purpose('body-style', 'CategoricalHash')
#default strategy mean, add transformer param for 3 columns
featurization_config.add_transformer_params('Imputer', ['engine-size'], {"strategy": "median"})
featurization_config.add_transformer_params('Imputer', ['city-mpg'], {"strategy": "median"})
featurization_config.add_transformer_params('Imputer', ['bore'], {"strategy": "most_frequent"})
featurization_config.add_transformer_params('HashOneHotEncoder', [], {"number_of_bits": 3})
```

## Featurization transparency

Every AutoML model has featurization automatically applied. Featurization includes automated feature engineering (when `"featurization": 'auto'`) and scaling and normalization, which then impacts the selected algorithm and its hyperparameter values. AutoML supports different methods to ensure you have visibility into what was applied to your model.

Consider this forecasting example:

+ There are four input features: A (Numeric), B (Numeric), C (Numeric), D (DateTime).
+ Numeric feature C is dropped because it's an ID column with all unique values.
+ Numeric features A and B have missing values and hence are imputed by the mean.
+ DateTime feature D is featurized into 11 different engineered features.

To get this information, use the `fitted_model` output from your AutoML experiment run.

```python
automl_config = AutoMLConfig(…)
automl_run = experiment.submit(automl_config …)
best_run, fitted_model = automl_run.get_output()
```

### Automated feature engineering

The `get_engineered_feature_names()` returns a list of engineered feature names.

>[!Note]
>Use `'timeseriestransformer'` for `task='forecasting'`, else use `'datatransformer'` for `'regression'` or `'classification'` task.

```python
fitted_model.named_steps['timeseriestransformer']. get_engineered_feature_names ()
```

This list includes all engineered feature names.

```
['A', 'B', 'A_WASNULL', 'B_WASNULL', 'year', 'half', 'quarter', 'month', 'day', 'hour', 'am_pm', 'hour12', 'wday', 'qday', 'week']
```

The `get_featurization_summary()` gets a featurization summary of all the input features.

```python
fitted_model.named_steps['timeseriestransformer'].get_featurization_summary()
```

Output

```
[{'RawFeatureName': 'A',
  'TypeDetected': 'Numeric',
  'Dropped': 'No',
  'EngineeredFeatureCount': 2,
  'Tranformations': ['MeanImputer', 'ImputationMarker']},
 {'RawFeatureName': 'B',
  'TypeDetected': 'Numeric',
  'Dropped': 'No',
  'EngineeredFeatureCount': 2,
  'Tranformations': ['MeanImputer', 'ImputationMarker']},
 {'RawFeatureName': 'C',
  'TypeDetected': 'Numeric',
  'Dropped': 'Yes',
  'EngineeredFeatureCount': 0,
  'Tranformations': []},
 {'RawFeatureName': 'D',
  'TypeDetected': 'DateTime',
  'Dropped': 'No',
  'EngineeredFeatureCount': 11,
  'Tranformations': ['DateTime','DateTime','DateTime','DateTime','DateTime','DateTime','DateTime','DateTime',ateTime','DateTime','DateTime']}]
```

|Output|Definition|
|----|--------|
|RawFeatureName|Input feature/column name from the dataset provided.|
|TypeDetected|Detected datatype of the input feature.|
|Dropped|Indicates if the input feature was dropped or used.|
|EngineeringFeatureCount|Number of features generated through automated feature engineering transforms.|
|Transformations|List of transformations applied to input features to generate engineered features.|

### Scaling and normalization

To understand scaling/normalization and the selected algorithm with its hyperparameter values, use `fitted_model.steps`.

The following sample output is from running `fitted_model.steps` for a chosen run:

```
[('RobustScaler', 
  RobustScaler(copy=True, 
  quantile_range=[10, 90], 
  with_centering=True, 
  with_scaling=True)), 

  ('LogisticRegression', 
  LogisticRegression(C=0.18420699693267145, class_weight='balanced', 
  dual=False, 
  fit_intercept=True, 
  intercept_scaling=1, 
  max_iter=100, 
  multi_class='multinomial', 
  n_jobs=1, penalty='l2', 
  random_state=None, 
  solver='newton-cg', 
  tol=0.0001, 
  verbose=0, 
  warm_start=False))]
```

To get more details, use this helper function:

```python
from pprint import pprint

def print_model(model, prefix=""):
    for step in model.steps:
        print(prefix + step[0])
        if hasattr(step[1], 'estimators') and hasattr(step[1], 'weights'):
            pprint({'estimators': list(e[0] for e in step[1].estimators), 'weights': step[1].weights})
            print()
            for estimator in step[1].estimators:
                print_model(estimator[1], estimator[0]+ ' - ')
        elif hasattr(step[1], '_base_learners') and hasattr(step[1], '_meta_learner'):
            print("\nMeta Learner")
            pprint(step[1]._meta_learner)
            print()
            for estimator in step[1]._base_learners:
                print_model(estimator[1], estimator[0]+ ' - ')
        else:
            pprint(step[1].get_params())
            print()   
```

This helper function returns the following output for a particular run using `LogisticRegression with RobustScalar` as the specific algorithm.

```
RobustScaler
{'copy': True,
'quantile_range': [10, 90],
'with_centering': True,
'with_scaling': True}

LogisticRegression
{'C': 0.18420699693267145,
'class_weight': 'balanced',
'dual': False,
'fit_intercept': True,
'intercept_scaling': 1,
'max_iter': 100,
'multi_class': 'multinomial',
'n_jobs': 1,
'penalty': 'l2',
'random_state': None,
'solver': 'newton-cg',
'tol': 0.0001,
'verbose': 0,
'warm_start': False}
```

### Predict class probability

Models produced using AutoML all have wrapper objects that mirror functionality from their open-source origin class. Most classification model wrapper objects returned by AutoML implement the `predict_proba()` function, which accepts an array-like or sparse matrix data sample of your features (X values), and returns an n-dimensional array of each sample and its respective class probability.

Assuming you retrieved the best run and fitted model using the same calls, you can call `predict_proba()` directly from the fitted model, supplying an `X_test` sample in the appropriate format depending on the model type.

```python
best_run, fitted_model = automl_run.get_output()
class_prob = fitted_model.predict_proba(X_test)
```

If the underlying model doesn't support the `predict_proba()` function or the format is incorrect, a model class-specific exception is thrown. See the [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier.predict_proba) and [XGBoost](https://xgboost.readthedocs.io/en/latest/python/python_api.html) reference docs for examples of how this function is implemented for different model types.

<a name="bert-integration"></a>

## BERT integration in AutoML

[Bidirectional Encoder Representations from Transformers (BERT)](https://techcommunity.microsoft.com/t5/azure-ai/how-bert-is-integrated-into-azure-automated-machine-learning/ba-p/1194657) is used in the featurization layer of AutoML. In this layer, if a column contains free text or other types of data like timestamps or simple numbers, then featurization is applied accordingly.

For BERT, the model is fine-tuned and trained by utilizing the user-provided labels. From here, document embeddings are output as features alongside others, like timestamp-based features, day of week.

Learn how to [Set up AutoML to train a natural language processing model with Python](how-to-auto-train-nlp-models.md).

### Steps to invoke BERT

In order to invoke BERT, set `enable_dnn: True` in your `automl_settings` and use a GPU compute (`vm_size = "STANDARD_NC6"` or higher GPU). If a CPU compute is used, then instead of BERT, AutoML enables the BiLSTM DNN featurizer.

AutoML takes the following steps for BERT.

1. **Preprocesses and tokenizes all text columns**. For example, the `StringCast` transformer can be found in the final model's featurization summary. An example of how to produce the model's featurization summary can be found in this [Jupyter notebook](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/classification-text-dnn/auto-ml-classification-text-dnn.ipynb).

1. **Concatenates all text columns into a single text column**, hence the `StringConcatTransformer` in the final model.

    Our implementation of BERT limits total text length of a training sample to 128 tokens. That means, all text columns when concatenated, should ideally be at most 128 tokens in length. If multiple columns are present, each column should be pruned so this condition is satisfied. Otherwise, for concatenated columns of length >128 tokens BERT's tokenizer layer truncates this input to 128 tokens.

1. **As part of feature sweeping, AutoML compares BERT against the baseline (bag of words features) on a sample of the data.** This comparison determines if BERT would give accuracy improvements. If BERT performs better than the baseline, AutoML then uses BERT for text featurization for the whole data. In that case, you see the `PretrainedTextDNNTransformer` in the final model.

BERT generally runs longer than other featurizers. For better performance, we recommend using *STANDARD_NC24r* or *STANDARD_NC24rs_V3* for their RDMA capabilities.

AutoML distributes BERT training across multiple nodes if they're available (up to a max of eight nodes). This can be done in your `AutoMLConfig` object by setting the `max_concurrent_iterations` parameter to higher than 1.

## Supported languages for BERT

AutoML currently supports around 100 languages. Depending on the dataset's language, AutoML chooses the appropriate BERT model. For German data, we use the German BERT model. For English, we use the English BERT model. For all other languages, we use the multilingual BERT model.

In the following code, the German BERT model is triggered because the dataset language is specified to `deu`, the three-letter language code for German according to [ISO classification](https://iso639-3.sil.org/code/deu):

```python
from azureml.automl.core.featurization import FeaturizationConfig

featurization_config = FeaturizationConfig(dataset_language='deu')

automl_settings = {
    "experiment_timeout_minutes": 120,
    "primary_metric": 'accuracy',
# All other settings you want to use
    "featurization": featurization_config,
    
    "enable_dnn": True, # This enables BERT DNN featurizer
    "enable_voting_ensemble": False,
    "enable_stack_ensemble": False
}
```

## Related content

* [Deploy machine learning models to Azure](how-to-deploy-and-where.md)
* [Train a regression model with AutoML and Python](how-to-auto-train-models-v1.md)
