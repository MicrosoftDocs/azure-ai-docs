---
title: Set up AutoML for NLP
titleSuffix: Azure Machine Learning
description: Set up Azure Machine Learning AutoML to train natural language processing models with the Azure Machine Learning Python SDK or the Azure Machine Learning CLI.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.reviewer: sooryar
ms.subservice: automl
ms.topic: how-to
ms.custom: devplatv2, sdkv2, cliv2, build-2023, build-2023-dataai, devx-track-python
ms.date: 01/15/2026
#Customer intent: As a data scientist with machine learning knowledge in natural language processing, I need to build models using language specific data in Azure Machine Learning so I can control model algorithm, hyperparameters, and training and deployment environments.
---

# Set up AutoML to train a natural language processing model 

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn how to train natural language processing (NLP) models in Azure Machine Learning by using [automated machine learning](concept-automated-ml.md) (AutoML). You can create NLP models by using AutoML via the Azure Machine Learning CLI v2 or the Azure Machine Learning Python SDK v2.

NLP in AutoML lets machine-learning professionals and data scientists use their own text data and build custom models for multiclass text classification, multilabel text classification, and named entity recognition (NER). You can seamlessly integrate with [Azure Machine Learning data labeling](how-to-create-text-labeling-projects.md) to label your text data, or use existing labeled data.

AutoML provides the option to use distributed training on multi-GPU compute clusters for faster model training. The resulting model can be operationalized at scale using Azure Machine Learning MLOps capabilities.

## Prerequisites

- Azure subscription. If you don't have an Azure subscription, sign up to try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An Azure Machine Learning workspace with a GPU training compute. To create the workspace, see [Create workspace resources](quickstart-create-resources.md). For more information about Azure-provided GPU instances, see [GPU optimized virtual machine sizes](/azure/virtual-machines/sizes-gpu).

  > [!NOTE]
  > Some NLP use cases, such as non-English datasets and longer range documents, require using multilingual models or models with longer max sequence length. These scenarios might require higher GPU memory for model training to succeed, such as the NCv3 or NDv2 series.
  
- Some familiarity with setting up AutoML experiments. For more information about the AutoML experiment design pattern, see [Set up AutoML training for tabular data](how-to-configure-auto-train.md).

# [Azure CLI](#tab/cli)

- The Azure Machine Learning CLI v2 installed. For guidance to update and install the latest version, see [Install and set up the CLI (v2)](how-to-configure-cli.md).

# [Python SDK](#tab/python)

- The Azure Machine Learning Python SDK v2 installed. 

  To install the SDK, you can either:

  - Create a compute instance, which automatically installs the SDK and is preconfigured for machine learning workflows. For more information, see [Create an Azure Machine Learning compute instance](how-to-create-compute-instance.md). 

  - [Install the AutoML package](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/README.md#setup-using-a-local-conda-environment), which includes the [default SDK installation](/python/api/overview/azure/ml/install#default-install).

  [!INCLUDE [automl-sdk-version](includes/machine-learning-automl-sdk-version.md)]

---

## Select your NLP task 

Decide what NLP task you want to accomplish. AutoML supports the follow deep neural network NLP tasks:

|Task |AutoML job syntax| Description |
----|----|---|
|Multiclass text classification | CLI v2: `text_classification`  <br> SDK v2: `text_classification()`| There are multiple possible classes and each sample can be classified as exactly one class. The task is to predict the correct class for each sample. <br> <br> For example, classify a movie script as `Comedy` or `Romantic`. |
|Multilabel text classification | CLI v2: `text_classification_multilabel`  <br> SDK v2: `text_classification_multilabel()`| There are multiple possible classes and each sample can be assigned any number of classes. The task is to predict all the classes for each sample.<br> <br> For example, classify a movie script as `Comedy`, `Romantic`, and `Comedy and Romantic`. |
|Named Entity Recognition (NER)| CLI v2:`text_ner` <br> SDK v2: `text_ner()`| There are multiple possible tags for tokens in sequences. The task is to predict the tags for all the tokens for each sequence. <br> <br> For example, extract domain-specific entities from unstructured text, such as contracts or financial documents.|

### Thresholding

Thresholding is a multilabel text classification feature that determines the threshold at which the predicted probabilities produce a positive label. Lower values allow more labels, which is better when users care about recall, but can lead to more false positives. Higher values allow fewer labels, which are better when users care about precision, but could lead to more false negatives.

<a name="preparing-data"></a>
## Prepare data

For AutoML NLP experiments, you can provide your data in `.csv` format for multiclass and multilabel classification tasks. For NER tasks, provide two-column `.txt` files that use a space as the separator and adhere to the `CoNLL` format. The following sections provide details about the data format accepted for each task.

### Multiclass

For multiclass classification, the dataset can contain up to several text columns and exactly one label column. The following example has only one text column.

```text
text,labels
"I love watching Chicago Bulls games.","NBA"
"Tom Brady is a great player.","NFL"
"There is a game between Yankees and Orioles tonight","MLB"
"Stephen Curry made the highest number of three-pointers","NBA"
```

<a name="multi-label"></a>
### Multilabel

For multilabel classification, the dataset columns can be the same as multiclass, but there are special format requirements for data in the label column. The following table shows the two accepted formats with examples.

|Label column format options |Multiple labels| One label | No labels|
|---|---|---|---|
|Plain text|`"label1, label2, label3"`| `"label1"`| `""`|
|Python list with quotes| `"['label1','label2','label3']"`| `"['label1']"`|`"[]"`|

> [!IMPORTANT]
> Different parsers read labels for these formats. For the plain text format, all nonalphanumeric characters except for `_` are read as label separators. For example, the label `"cs.AI"` is read as `"cs"` and `"AI"`. With the Python list format, the label is `"['cs.AI']"`, which is read as `"cs.AI"`.

The following example shows multilabel data in plain text format:

```text
text,labels
"I love watching Chicago Bulls games.","basketball"
"The four most popular leagues are NFL, MLB, NBA and NHL","football,baseball,basketball,hockey"
"I like drinking beer.",""
```

The following example shows multilabel data in Python list with quotes format. 

``` python
text,labels
"I love watching Chicago Bulls games.","['basketball']"
"The four most popular leagues are NFL, MLB, NBA and NHL","['football','baseball','basketball','hockey']"
"I like drinking beer.","[]"
```

### Named entity recognition (NER)

Unlike multiclass or multilabel classification, which take `.csv` format datasets, NER requires `CoNLL` format. The data file must contain exactly two columns, and the token and the label in each row are separated by a single space.

For example,

```text
Hudson B-loc
Square I-loc
is O
a O
famous O
place O
in O
New B-loc
York I-loc
City I-loc

Stephen B-per
Curry I-per
got O
three O
championship O
rings O
```

### Data validation

Before it trains models, AutoML applies data validation checks on the input data to ensure that the data can be preprocessed correctly. If any of these checks fail, the run fails with the relevant error message. The following factors are required to pass data validation checks for each task.

> [!Note]
> Some data validation checks are applicable to both the training and the validation set and others apply only to the training set. If the test dataset doesn't pass data validation, AutoML can't capture it, and model inference failure or a decline in model performance are possible.

|Task | Data validation check|
|---|---|
|All tasks | At least 50 training samples are required. |
|Multiclass and multilabel | The training data and validation data must have: <br>- The same set of columns. <br>- The same column order from left to right. <br>- The same data type for columns with the same name. <br>- At least two unique labels. <br>- Unique column names within each dataset. For example, the training set can't have multiple columns named `Age`.|
|Multiclass only | None.|
|Multilabel only | - The label column format must be in the [accepted format](#multi-label). <br>- At least one sample should have 0 or 2+ labels; otherwise it should be a multiclass task. <br>- All labels should be in `str` or `int` format, with no overlaps. <br>- You can't have both label `1` and label `'1'`.|
|NER only | - The file can't start with an empty line. <br>- Each line must be an empty line, or follow the format `{token} {label}` where there's exactly one space between the token and the label and no white space after the label. <br>- All labels must start with `I-` `B-`, or be exactly `O`, and are case-sensitive. <br>- There must be exactly one empty line between two samples, and exactly one empty line at the end of the file.|

## Configure the experiment

AutoML NLP capability is triggered through task-specific `automl` type jobs, the same workflow used for submitting classification, regression, and forecasting AutoML tasks. You set parameters such as `experiment_name`, `compute_name`, and data inputs the same as for those experiments. However, there are the following key differences:

- You can ignore `primary_metric`, because it's only for reporting. AutoML trains only one model per run for NLP, and there's no model selection.
- The `label_column_name` parameter is required only for multiclass and multilabel text classification tasks.
- If more than 10% of the samples in your dataset contain more than 128 tokens, it's long-range. To use the long-range text feature, you need an NC6 or higher GPU SKU such as: [NCv3](/azure/virtual-machines/ncv3-series) or [NDv2](/azure/virtual-machines/sizes/gpu-accelerated/ndv2-series) series.

# [Azure CLI](#tab/cli)

For CLI v2 AutoML jobs, you configure your experiment in a YAML file. See the following examples:

- [YAML: AutoML text classification job](reference-automl-nlp-cli-text-classification.md#yaml-automl-text-classification-job)
- [YAML: AutoML text classification multilabel job](reference-automl-nlp-cli-multilabel-classification.md#yaml-automl-text-classification-multilabel-job)
- [YAML: AutoML text NER job](reference-automl-nlp-cli-ner.md#yaml-automl-text-ner-job)

# [Python SDK](#tab/python)

For AutoML jobs via the SDK, you configure the job by using the specific NLP task function. The following example demonstrates the configuration for `text_classification`.

```python
# general job parameters
compute_name = "gpu-cluster"
exp_name = "dpv2-nlp-text-classification-experiment"

# Create the AutoML job with the related factory-function.
text_classification_job = automl.text_classification(
    compute=compute_name,
    # name="dpv2-nlp-text-classification-multiclass-job-01",
    experiment_name=exp_name,
    training_data=my_training_data_input,
    validation_data=my_validation_data_input,
    target_column_name="Sentiment",
    primary_metric="accuracy",
    tags={"my_custom_tag": "My custom value"},
)

text_classification_job.set_limits(timeout=120)

```

### Distributed training

AutoML handles distributed training automatically when the parameters `max_concurrent_iterations = number_of_vms` and `enable_distributed_dnn_training = True` are provided in your `AutoMLConfig` during experiment setup. These parameters schedule distributed training of the NLP models and automatically scale to every GPU on your virtual machine (VM) or cluster of virtual machines (VMs). The maximum number of VMs allowed is 32. The VMs for training are scheduled in powers of two.

```python
max_concurrent_iterations = number_of_vms
enable_distributed_dnn_training = True
```

In AutoML NLP only, hold-out validation is supported and requires a validation dataset.

---

### Language settings

As part of the NLP functionality, AutoML supports language-specific and multilingual pretrained text in 104 languages for Deep Neural Network (DNN) models such as Bidirectional Encoder Representations from Transformers (BERT) models. Language selection defaults to English. 

The following table summarizes which model is applied based on task type and language. For more information, see [supported languages and their codes](/python/api/azureml-automl-core/azureml.automl.core.constants.textdnnlanguages#azureml-automl-core-constants-textdnnlanguages-supported).

|Task |Syntax for `dataset_language` | Text model algorithm|
|----|----|---|
|Multilabel text classification|`"eng"` <br>  `"deu"` <br> `"mul"`|  English&nbsp;BERT&nbsp;[uncased](https://huggingface.co/bert-base-uncased) <br>  [German BERT](https://huggingface.co/bert-base-german-cased)<br>  [Multilingual BERT](https://huggingface.co/bert-base-multilingual-cased) <br><br>For all other languages, AutoML applies multilingual BERT.|
|Multiclass text classification|`"eng"` <br>  `"deu"` <br> `"mul"`|  English&nbsp;BERT&nbsp;[cased](https://huggingface.co/bert-base-cased)<br>  [Multilingual BERT](https://huggingface.co/bert-base-multilingual-cased) <br><br>For all other languages, AutoML applies multilingual BERT.|
|Named entity recognition (NER)|`"eng"` <br>  `"deu"` <br> `"mul"`|  English&nbsp;BERT&nbsp;[cased](https://huggingface.co/bert-base-cased) <br>  [German BERT](https://huggingface.co/bert-base-german-cased)<br>  [Multilingual BERT](https://huggingface.co/bert-base-multilingual-cased) <br><br>For all other languages, AutoML applies multilingual BERT.|

BERT is also used in the featurization process of AutoML experiment training. For more information, see [BERT integration and featurization in AutoML (SDK v1)](./v1/how-to-configure-auto-features.md#bert-integration-in-automl).

# [Azure CLI](#tab/cli)

You can specify your dataset language in the featurization section of your configuration YAML file. 

```azurecli
featurization:
   dataset_language: "eng"
```

# [Python SDK](#tab/python)

You can specify your dataset language with the `set_featurization()` method.

```python
text_classification_job.set_featurization(dataset_language='eng')
```

---

## Submit the AutoML job

# [Azure CLI](#tab/cli)

To submit your AutoML job, run the following CLI v2 command. Replace the placeholders with your YAML filename and path, workspace name, resource group, and subscription ID.

```azurecli

az ml job create --file ./<YAML filename> --workspace-name <machine-learning-workspace> --resource-group <resource-group> --subscription <subscription ID>
```

You can also run your NLP experiments with distributed training on an Azure Machine Learning compute cluster. 

# [Python SDK](#tab/python)

To submit your AutoML job, run the following `CommandJob` in the workspace using the `MLClient` you created earlier.

```python
returned_job = ml_client.jobs.create_or_update(
    text_classification_job
)  # submit the job to the backend

print(f"Created job: {returned_job}")
ml_client.jobs.stream(returned_job.name)
```

---

## Code examples

# [Azure CLI](#tab/cli)

For more examples, see the following sample YAML files for each NLP task and other examples at [https://github.com/Azure/azureml-examples/cli/jobs/automl-standalone-jobs](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/automl-standalone-jobs).

- [Multiclass text classification](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/automl-standalone-jobs/cli-automl-text-classification-newsgroup/cli-automl-text-classification-newsgroup.yml)
- [Multilabel text classification](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/automl-standalone-jobs/cli-automl-text-classification-multilabel-paper-cat/cli-automl-text-classification-multilabel-paper-cat.yml)
- [Named entity recognition](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/automl-standalone-jobs/cli-automl-text-ner-conll/cli-automl-text-ner-conll2003.yml)

# [Python SDK](#tab/python)

For more examples, see the following sample notebooks for each NLP task and other examples at [https://github.com/Azure/azureml-examples/python/jobs/automl-standalone-jobs](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs).

* [Multiclass text classification](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-nlp-text-classification-multiclass-task-sentiment-analysis/automl-nlp-multiclass-sentiment.ipynb)
* [Multilabel text classification](
https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-nlp-text-classification-multilabel-task-paper-categorization/automl-nlp-multilabel-paper-cat.ipynb)
* [Named entity recognition](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-nlp-text-named-entity-recognition-task/automl-nlp-text-ner-task.ipynb)

---

## Model sweeping and hyperparameter tuning (preview) 

[!INCLUDE [preview disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

AutoML NLP lets you provide a list of models and combinations of hyperparameters via the hyperparameter search space in the config. Hyperdrive generates several child runs. Each child run is a fine-tuning run for a given NLP model and set of hyperparameter values that were chosen and swept over based on the provided search space.

### Supported model algorithms

The following list shows all the pretrained text DNN models available in AutoML NLP for fine-tuning: 

* bert-base-cased 
* bert-large-uncased 
* bert-base-multilingual-cased 
* bert-base-german-cased 
* bert-large-cased 
* distilbert-base-cased 
* distilbert-base-uncased 
* roberta-base 
* roberta-large 
* distilroberta-base 
* xlm-roberta-base 
* xlm-roberta-large 
* xlnet-base-cased 
* xlnet-large-cased 

The large models are larger than their base counterparts and are typically more performant, but take up more GPU memory and time for training. Large model SKU requirements are more stringent and require using NDv2-series VMs for the best results. 

### Supported Hugging Face model algorithms (preview)

With the new backend that runs on [Azure Machine Learning pipelines](concept-ml-pipelines.md), you can use any text/token classification models from the Hugging Face Hub for [text classification](https://huggingface.co/models?pipeline_tag=text-classification&library=transformers) and [token classification](https://huggingface.co/models?pipeline_tag=token-classification&sort=trending) that are part of the transformers library, such as microsoft/deberta-large-mnli. You can also find a curated list of models in the [Azure Machine Learning model registry](concept-model-catalog.md?view=azureml-api-2&preserve-view=true) that are validated with the pipeline components.

Using any Hugging Face model triggers runs using pipeline components. If you use both legacy and Hugging Face models, all runs and trials are triggered using components.

### Supported hyperparameters 

The following table describes the hyperparameters that AutoML NLP supports. 

| Parameter name | Description | Syntax |
|-------|---------|---------| 
|`gradient_accumulation_steps`| The number of backward operations whose gradients are to be summed up before performing one step of gradient descent by calling the optimizer's step function. <br><br> An effective batch size is `gradient_accumulation_steps` times larger than the maximum size that fits the GPU. | Must be a positive integer.|
|`learning_rate`| Initial learning rate. | Must be a float in the range `[0, 1]`. |
|`learning_rate_scheduler`|Type of learning rate scheduler. | Must choose from `linear`, `cosine`, `cosine_with_restarts`, `polynomial`, `constant`, `constant_with_warmup`.  |
|`model_name`| Name of one of the supported models.  | Must choose from `bert_base_cased`, `bert_base_uncased`, `bert_base_multilingual_cased`, `bert_base_german_cased`, `bert_large_cased`, `bert_large_uncased`, `distilbert_base_cased`, `distilbert_base_uncased`, `roberta_base`, `roberta_large`, `distilroberta_base`, `xlm_roberta_base`, `xlm_roberta_large`, `xlnet_base_cased`, `xlnet_large_cased`. |
|`number_of_epochs`| Number of training epochs. | Must be a positive integer. |
|`training_batch_size`| Training batch size. | Must be a positive integer. |
|`validation_batch_size`| Validation batch size. | Must be a positive integer. |
|`warmup_ratio`| Ratio of total training steps used for a linear warmup from `0` to `learning_rate`.  | Must be a float in the range `[0, 1]`. |
|`weight_decay`| Value of weight decay when optimizer is `sgd`, `adam`, or `adamw`. | Must be a float in the range `[0, 1]`. |

All discrete hyperparameters only allow choice distributions, such as the integer-typed `training_batch_size` and the string-typed `model_name` hyperparameters. All continuous hyperparameters like `learning_rate` support all distributions. 

### Configure sweep settings 

You can configure all the sweep-related parameters. Multiple model subspaces can be constructed with hyperparameters conditional to the respective model, as shown in each hyperparameter tuning example.

The same discrete and continuous distribution options that are available for general HyperDrive jobs are supported. For all nine options, see [Hyperparameter tuning a model](how-to-tune-hyperparameters.md#define-the-search-space).

# [Azure CLI](#tab/cli)

```yaml
limits: 
  timeout_minutes: 120  
  max_trials: 4 
  max_concurrent_trials: 2 

sweep: 
  sampling_algorithm: grid 
  early_termination: 
    type: bandit 
    evaluation_interval: 10 
    slack_factor: 0.2 

search_space: 
  - model_name: 
      type: choice 
      values: [bert_base_cased, roberta_base] 
    number_of_epochs: 
      type: choice 
      values: [3, 4] 
  - model_name: 
      type: choice 
      values: [distilbert_base_cased] 
    learning_rate: 
      type: uniform 
      min_value: 0.000005 
      max_value: 0.00005 
```

# [Python SDK](#tab/python)

Set the limits for your model sweeping job: 

```python
text_ner_job.set_limits( 
                        timeout_minutes=120, 
                        trial_timeout_minutes=20, 
                        max_trials=4, 
                        max_concurrent_trials=2, 
                        max_nodes=4) 
```

Define a search space with customized settings:

```python 
text_ner_job.extend_search_space( 
    [ 
        SearchSpace( 
            model_name=Choice([NlpModels.BERT_BASE_CASED, NlpModels.ROBERTA_BASE]) 
        ), 
        SearchSpace( 
            model_name=Choice([NlpModels.DISTILROBERTA_BASE]), 
            learning_rate_scheduler=Choice([NlpLearningRateScheduler.LINEAR,  
                                            NlpLearningRateScheduler.COSINE]), 
            learning_rate=Uniform(5e-6, 5e-5) 
        ) 
    ] 
) 
 ```

You can configure the sweep procedure via sampling algorithm early termination: 
```python
text_ner_job.set_sweep( 
    sampling_algorithm="Random", 
    early_termination=BanditPolicy( 
        evaluation_interval=2, slack_factor=0.05, delay_evaluation=6 
    ) 
) 
```

---

### Sampling methods for the sweep 

When you sweep hyperparameters, you need to specify the sampling method to use for sweeping over the defined parameter space. The following sampling methods are supported with the `sampling_algorithm` parameter:

| Sampling type | AutoML job syntax |
|-------|---------|
|[Random](how-to-tune-hyperparameters.md#random-sampling)| `random` |
|[Grid](how-to-tune-hyperparameters.md#grid-sampling)| `grid` |
|[Bayesian](how-to-tune-hyperparameters.md#bayesian-sampling)| `bayesian` |

### Experiment budget 

You can optionally specify the experiment budget for your AutoML NLP training job using the `timeout_minutes` parameter in the `limits`. This parameter defines the amount of time in minutes before the experiment terminates. If no timeout is specified, the default experiment timeout is seven days and the maximum is 60 days.

AutoML NLP also supports `trial_timeout_minutes`, the maximum amount of time in minutes an individual trial can run before being terminated, and `max_nodes`, the maximum number of nodes from the backing compute cluster to use for the job. These parameters are also set in the `limits` section.

```yaml
limits: 
  timeout_minutes: 60 
  trial_timeout_minutes: 20 
  max_nodes: 2 
```

### Early termination policies  

You can automatically end poorly performing runs with an early termination policy. Early termination improves computational efficiency, saving compute resources that would otherwise be spent on less promising configurations.

AutoML NLP supports early termination policies using the `early_termination` parameter. If no termination policy is specified, all configurations are run to completion. For more information, see [Specify early termination policy](how-to-tune-hyperparameters.md#early-termination).

### Resources for the sweep

You can control the resources spent on your hyperparameter sweep by specifying the `max_trials` and the `max_concurrent_trials` for the sweep.

|Parameter | Detail
-----|----
|`max_trials` | Maximum number of configurations to sweep. Must be an integer between 1 and 1000. When exploring just the default hyperparameters for a given model algorithm, set this parameter to 1. The default value is 1.
|`max_concurrent_trials`| Maximum number of runs that can run concurrently. If specified, must be an integer between 1 and 100. The default value is 1. <br><br> **NOTE:**<br>- The number of concurrent runs is gated on the resources available in the specified compute target. Ensure that the compute target has the available resources for the desired concurrency.<br>- The `max_concurrent_trials` value is capped at `max_trials` internally. For example, if you set `max_concurrent_trials=4`, `max_trials=2`, values are internally updated as `max_concurrent_trials=2`, `max_trials=2`.|

The following example shows how to configure the sweep related parameters.

```yaml
sweep:
  limits:
    max_trials: 10
    max_concurrent_trials: 2
  sampling_algorithm: random
  early_termination:
    type: bandit
    evaluation_interval: 2
    slack_factor: 0.2
    delay_evaluation: 6
```

### Known issues

Certain datasets produce low scores, even zero, regardless of the NLP task. High loss values accompany these scores, implying that the neural network failed to converge. Such cases are uncommon but possible, and can happen more frequently on certain GPU series.

The best way to handle these cases is to use hyperparameter tuning and provide a wider range of values, especially for hyperparameters like learning rates. Until hyperparameter tuning capability is available in production, use the NC6 or ND6 compute clusters if you experience these issues. These clusters typically have fairly stable training outcomes.

## Related content

- [How to deploy an AutoML model to an online endpoint](how-to-deploy-automl-endpoint.md)
- [Hyperparameter tuning a model (v2)](how-to-tune-hyperparameters.md)
