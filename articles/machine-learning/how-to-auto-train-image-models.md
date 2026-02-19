---
title: Set up AutoML for computer vision
titleSuffix: Azure Machine Learning
description: Set up Azure Machine Learning automated ML to train computer vision models  with the CLI v2 and Python SDK v2.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.service: azure-machine-learning
ms.subservice: automl
ms.custom: devx-track-azurecli, update-code, devx-track-python
ms.topic: how-to
ms.date: 01/28/2026
#Customer intent: I'm a data scientist with ML knowledge in the computer vision space, looking to build ML models using image data in Azure Machine Learning with full control of the model architecture, hyperparameters, and training and deployment environments.
---

# Set up AutoML to train computer vision models

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]


In this article, you learn how to train computer vision models on image data by using automated ML. You can train models by using the Azure Machine Learning CLI extension v2 or the Azure Machine Learning Python SDK v2.

Automated ML supports model training for computer vision tasks like image classification, object detection, and instance segmentation. Authoring AutoML models for computer vision tasks is currently supported through the Azure Machine Learning Python SDK. You can access the resulting experimentation trials, models, and outputs from the Azure Machine Learning studio UI. [Learn more about automated ml for computer vision tasks on image data](concept-automated-ml.md).

## Prerequisites

# [Azure CLI](#tab/cli)
 [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]


* An Azure Machine Learning workspace. To create the workspace, see [Create workspace resources](quickstart-create-resources.md).
* Install and [set up CLI (v2)](how-to-configure-cli.md#prerequisites) and make sure you install the `ml` extension.

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

* Python 3.10 or later.

* An Azure Machine Learning workspace. To create the workspace, see [Create workspace resources](quickstart-create-resources.md).

* The Azure Machine Learning Python SDK v2 installed.

    To install the SDK, you can either:  
    * Create a compute instance, which automatically installs the SDK and is preconfigured for ML workflows. For more information, see [Create an Azure Machine Learning compute instance](how-to-create-compute-instance.md).

    * Use the following command to install Azure Machine Learning Python SDK v2:
       * Uninstall previous preview version:
       ```python
       pip uninstall azure-ai-ml
       ```
       * Install the Azure Machine Learning Python SDK v2:
       ```python
       pip install azure-ai-ml azure-identity
       ```
   
---

## Select your task type

Automated ML for images supports the following task types:

Task type | AutoML Job syntax
---|---
 image classification | CLI v2: `image_classification` <br> SDK v2: `image_classification()`
image classification multi-label | CLI v2: `image_classification_multilabel` <br> SDK v2: `image_classification_multilabel()`
image object detection | CLI v2: `image_object_detection` <br> SDK v2: `image_object_detection()`
image instance segmentation| CLI v2: `image_instance_segmentation` <br> SDK v2: `image_instance_segmentation()`

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

Set the task type as a required parameter. Use the `task` key to set this parameter.

For example:

```yaml
task: image_object_detection
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]


Create AutoML image jobs by using task-specific `automl` functions based on the task type.

For example:

```python
from azure.ai.ml import automl
image_object_detection_job = automl.image_object_detection()
```
---

## Training and validation data

To generate computer vision models, bring labeled image data as input for model training in the form of an `MLTable`. You can create an `MLTable` from training data in JSONL format.

If your training data is in a different format, such as pascal VOC or COCO, you can use the helper scripts included with the sample notebooks to convert the data to JSONL. For more information, see [prepare data for computer vision tasks with automated ML](how-to-prepare-datasets-for-automl-images.md). 

> [!Note]
> The training data needs to have at least 10 images to submit an AutoML job. 

> [!Warning]
> For this capability, the SDK and CLI support creating an `MLTable` from data in JSONL format. Creating the `MLTable` via the UI isn't supported at this time. 


### JSONL schema samples

The structure of the TabularDataset depends upon the task at hand. For computer vision task types, it consists of the following fields:

Field| Description
---|---
`image_url`| Contains filepath as a StreamInfo object
`image_details`|Image metadata information consists of height, width, and format. This field is optional.
`label`| A json representation of the image label, based on the task type.

The following code is a sample JSONL file for image classification:

```json
{
      "image_url": "azureml://subscriptions/<my-subscription-id>/resourcegroups/<my-resource-group>/workspaces/<my-workspace>/datastores/<my-datastore>/paths/image_data/Image_01.png",
      "image_details":
      {
          "format": "png",
          "width": "2230px",
          "height": "4356px"
      },
      "label": "cat"
  }
  {
      "image_url": "azureml://subscriptions/<my-subscription-id>/resourcegroups/<my-resource-group>/workspaces/<my-workspace>/datastores/<my-datastore>/paths/image_data/Image_02.jpeg",
      "image_details":
      {
          "format": "jpeg",
          "width": "3456px",
          "height": "3467px"
      },
      "label": "dog"
  }
  ```

  The following code is a sample JSONL file for object detection:

  ```json
  {
      "image_url": "azureml://subscriptions/<my-subscription-id>/resourcegroups/<my-resource-group>/workspaces/<my-workspace>/datastores/<my-datastore>/paths/image_data/Image_01.png",
      "image_details":
      {
          "format": "png",
          "width": "2230px",
          "height": "4356px"
      },
      "label":
      {
          "label": "cat",
          "topX": "1",
          "topY": "0",
          "bottomX": "0",
          "bottomY": "1",
          "isCrowd": "true",
      }
  }
  {
      "image_url": "azureml://subscriptions/<my-subscription-id>/resourcegroups/<my-resource-group>/workspaces/<my-workspace>/datastores/<my-datastore>/paths/image_data/Image_02.png",
      "image_details":
      {
          "format": "jpeg",
          "width": "1230px",
          "height": "2356px"
      },
      "label":
      {
          "label": "dog",
          "topX": "0",
          "topY": "1",
          "bottomX": "0",
          "bottomY": "1",
          "isCrowd": "false",
      }
  }
  ```


### Consume data

After converting your data to JSONL format, create training and validation `MLTable` files as shown in the following example.

```yaml
paths:
  - file: ./train_annotations.jsonl
transformations:
  - read_json_lines:
        encoding: utf8
        invalid_lines: error
        include_path_column: false
  - convert_column_types:
      - columns: image_url
        column_type: stream_info
```

Automated ML doesn't impose any constraints on training or validation data size for computer vision tasks. The storage layer behind the dataset (for example, blob store) sets the maximum dataset size. There's no minimum number of images or labels. However, start with a minimum of 10 to 15 samples per label to ensure the output model is sufficiently trained. The higher the total number of labels or classes, the more samples you need per label.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

Pass the required training data parameter by using the `training_data` key. Optionally, specify another MLTable as validation data by using the `validation_data` key. If you don't specify validation data, 20% of your training data is used for validation by default, unless you pass `validation_data_size` argument with a different value.

Pass the required target column name parameter by using the `target_column_name` key. Use this parameter as the target for the supervised ML task. For example,

```yaml
target_column_name: label
training_data:
  path: data/training-mltable-folder
  type: mltable
validation_data:
  path: data/validation-mltable-folder
  type: mltable
```

# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

Use the following code to create data inputs from training and validation MLTable from your local directory or cloud storage:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=data-load)]

Pass the required training data parameter by using the `training_data` parameter of the task specific `automl` type function. Optionally, specify another MLTable as validation data by using the `validation_data` parameter. If you don't specify validation data, 20% of your training data is used for validation by default, unless you pass `validation_data_size` argument with a different value.

Pass the required target column name parameter by using the `target_column_name` parameter of the task specific `automl` function. For example,

```python
from azure.ai.ml import automl
image_object_detection_job = automl.image_object_detection(
    training_data=my_training_data_input,
    validation_data=my_validation_data_input,
    target_column_name="label"
)
```
---

## Compute to run experiment

Provide a [compute target](concept-azure-machine-learning-architecture.md#compute-targets) for automated ML to conduct model training. Automated ML models for computer vision tasks require GPU SKUs and support NC and ND families. Use the NCsv3-series (with v100 GPUs) for faster training. A compute target with a multi-GPU VM SKU uses multiple GPUs to also speed up training. Additionally, when you set up a compute target with multiple nodes you can conduct faster model training through parallelism when tuning hyperparameters for your model.

> [!NOTE]
> If you're using a [compute instance](concept-compute-instance.md) as your compute target, make sure that multiple AutoML jobs don't run at the same time. Also, make sure that `max_concurrent_trials` is set to 1 in your [job limits](#job-limits).

Pass in the compute target by using the `compute` parameter. For example:

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
compute: azureml:gpu-cluster
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml import automl

compute_name = "gpu-cluster"
image_object_detection_job = automl.image_object_detection(
    compute=compute_name,
)
```
---

## Configure experiments

For computer vision tasks, you can launch either [individual trials](#individual-trials), [manual sweeps](#manually-sweeping-model-hyperparameters), or [automatic sweeps](#automatically-sweeping-model-hyperparameters-automode). Start with an automatic sweep to get a first baseline model. Then, try individual trials with certain models and hyperparameter configurations. Finally, use manual sweeps to explore multiple hyperparameter values near the more promising models and hyperparameter configurations. This three step workflow (automatic sweep, individual trials, manual sweeps) avoids searching the entirety of the hyperparameter space, which grows exponentially in the number of hyperparameters.

Automatic sweeps can yield competitive results for many datasets. Additionally, they don't require advanced knowledge of model architectures. They take into account hyperparameter correlations and they work seamlessly across different hardware setups. All these reasons make them a strong option for the early stage of your experimentation process.

### Primary metric

An AutoML training job uses a primary metric for model optimization and hyperparameter tuning. The primary metric depends on the task type as shown in the following list. Other primary metric values aren't currently supported. 

* [Accuracy](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html) for image classification
* [Intersection over union](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html) for image classification multilabel
* [Mean average precision](how-to-understand-automated-ml.md#object-detection-and-instance-segmentation-metrics) for image object detection
* [Mean average precision](how-to-understand-automated-ml.md#object-detection-and-instance-segmentation-metrics) for image instance segmentation
    
### Job limits

You can control the resources spent on your AutoML Image training job by specifying the `timeout_minutes`, `max_trials`, and the `max_concurrent_trials` for the job in limit settings as described in the following example.

Parameter | Detail
-----|----
`max_trials` |  Parameter for maximum number of trials to sweep. Must be an integer between 1 and 1,000. When you explore just the default hyperparameters for a given model architecture, set this parameter to 1. The default value is 1.
`max_concurrent_trials`| Maximum number of trials that run concurrently. If specified, must be an integer between 1 and 100. The default value is 1. <br><br> **NOTE:** <li> The number of concurrent trials depends on the resources available in the specified compute target. Ensure that the compute target has the available resources for the desired concurrency.  <li> `max_concurrent_trials` is capped at `max_trials` internally. For example, if you set `max_concurrent_trials=4` and `max_trials=2`, the values are updated internally as `max_concurrent_trials=2` and `max_trials=2`.
`timeout_minutes`| The amount of time in minutes before the experiment terminates. If you don't specify a value, the default experiment timeout_minutes is seven days (maximum 60 days).

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
limits:
  timeout_minutes: 60
  max_trials: 10
  max_concurrent_trials: 2
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=limit-settings)]

---

### Automatically sweeping model hyperparameters (AutoMode)

> [!IMPORTANT]
> This feature is currently in public preview. This preview version is provided without a service-level agreement. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

It's hard to predict the best model architecture and hyperparameters for a dataset. Also, in some cases, the human time allocated to tuning hyperparameters is limited. For computer vision tasks, you can specify any number of trials and the system automatically determines the region of the hyperparameter space to sweep. You don't have to define a hyperparameter search space, a sampling method, or an early termination policy.

#### Triggering AutoMode

Run automatic sweeps by setting `max_trials` to a value greater than one in `limits` and by not specifying the search space, sampling method, and termination policy. This functionality is AutoMode. See the following example.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
limits:
  max_trials: 10
  max_concurrent_trials: 2
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
image_object_detection_job.set_limits(max_trials=10, max_concurrent_trials=2)
```
---

Running between 10 and 20 trials works well on many datasets. You can still set the [time budget](#job-limits) for the AutoML job, but only set this value if each trial might take a long time.

> [!Warning]
> The UI doesn't currently support launching automatic sweeps.


### Individual trials

In individual trials, you directly control the model architecture and hyperparameters. Pass the model architecture through the `model_name` parameter.

#### Supported model architectures

The following table summarizes the supported legacy models for each computer vision task. Using only these legacy models triggers runs that use the legacy runtime, where each individual run or trial is submitted as a command job. For information about HuggingFace and MMDetection support, see the next section.

| Task | Model architectures | String literal syntax<br> ***`default_model`\**** denoted with \*
---|----------|----------
| Image classification<br> (multi-class and multi-label) | **MobileNet**: Lightweight models for mobile applications <br> **ResNet**: Residual networks<br> **ResNeSt**: Split attention networks<br> **SE-ResNeXt50**: Squeeze-and-Excitation networks<br> **ViT**: Vision transformer networks | `mobilenetv2`   <br>`resnet18` <br>`resnet34` <br> `resnet50`  <br> `resnet101` <br> `resnet152`    <br> `resnest50` <br> `resnest101`  <br> `seresnext`  <br> `vits16r224` (small) <br> ***`vitb16r224`\**** (base) <br>`vitl16r224` (large)|
| Object detection | **YOLOv5**: One stage object detection model   <br>  **Faster RCNN ResNet FPN**: Two stage object detection models  <br> **RetinaNet ResNet FPN**: address class imbalance with Focal Loss <br> <br>*Note: Refer to [`model_size` hyperparameter](reference-automl-images-hyperparameters.md#model-specific-hyperparameters) for YOLOv5 model sizes.*| ***`yolov5`\**** <br> `fasterrcnn_resnet18_fpn` <br> `fasterrcnn_resnet34_fpn` <br> `fasterrcnn_resnet50_fpn` <br> `fasterrcnn_resnet101_fpn` <br> `fasterrcnn_resnet152_fpn` <br> `retinanet_resnet50_fpn` | 
| Instance segmentation | **MaskRCNN ResNet FPN**| `maskrcnn_resnet18_fpn` <br> `maskrcnn_resnet34_fpn` <br> ***`maskrcnn_resnet50_fpn`\****  <br> `maskrcnn_resnet101_fpn` <br> `maskrcnn_resnet152_fpn`|

#### Supported model architectures - HuggingFace and MMDetection

By using the new backend that runs on [Azure Machine Learning pipelines](concept-ml-pipelines.md), you can use any image classification model from the [HuggingFace Hub](https://huggingface.co/models?pipeline_tag=image-classification&library=transformers) that's part of the transformers library (such as microsoft/beit-base-patch16-224). You can also use any object detection or instance segmentation model from the [MMDetection Version 3.1.0 Model Zoo](https://mmdetection.readthedocs.io/en/v3.1.0/model_zoo.html) (such as `atss_r50_fpn_1x_coco`). 

In addition to supporting any model from HuggingFace Transformers and MMDetection 3.1.0, the Azure Machine Learning registry offers a list of curated models from these libraries. These curated models are thoroughly tested and use default hyperparameters selected from extensive benchmarking to ensure effective training. The following table summarizes these curated models.

| Task | Model architectures | String literal syntax |
---|----------|----------
| Image classification<br> (multi-class and multi-label) | **BEiT** <br> **ViT** <br> **DeiT** <br> **SwinV2** | [`microsoft/beit-base-patch16-224-pt22k-ft22k`](https://ml.azure.com/registries/azureml/models/microsoft-beit-base-patch16-224-pt22k-ft22k/version/5)<br> [`google/vit-base-patch16-224`](https://ml.azure.com/registries/azureml/models/google-vit-base-patch16-224/version/5)<br> [`facebook/deit-base-patch16-224`](https://ml.azure.com/registries/azureml/models/facebook-deit-base-patch16-224/version/5)<br> [`microsoft/swinv2-base-patch4-window12-192-22k`](https://ml.azure.com/registries/azureml/models/microsoft-swinv2-base-patch4-window12-192-22k/version/5) |
| Object Detection | **Sparse R-CNN** <br> **Deformable DETR** <br> **VFNet** <br> **YOLOF** | [`mmd-3x-sparse-rcnn_r50_fpn_300-proposals_crop-ms-480-800-3x_coco`](https://ml.azure.com/registries/azureml/models/mmd-3x-sparse-rcnn_r50_fpn_300-proposals_crop-ms-480-800-3x_coco/version/8)<br> [`mmd-3x-sparse-rcnn_r101_fpn_300-proposals_crop-ms-480-800-3x_coco`](https://ml.azure.com/registries/azureml/models/mmd-3x-sparse-rcnn_r101_fpn_300-proposals_crop-ms-480-800-3x_coco/version/8) <br> [`mmd-3x-deformable-detr_refine_twostage_r50_16xb2-50e_coco`](https://ml.azure.com/registries/azureml/models/mmd-3x-deformable-detr_refine_twostage_r50_16xb2-50e_coco/version/8) <br> [`mmd-3x-vfnet_r50-mdconv-c3-c5_fpn_ms-2x_coco`](https://ml.azure.com/registries/azureml/models/mmd-3x-vfnet_r50-mdconv-c3-c5_fpn_ms-2x_coco/version/8) <br> [`mmd-3x-vfnet_x101-64x4d-mdconv-c3-c5_fpn_ms-2x_coco`](https://ml.azure.com/registries/azureml/models/mmd-3x-vfnet_x101-64x4d-mdconv-c3-c5_fpn_ms-2x_coco/version/8) <br> [`mmd-3x-yolof_r50_c5_8x8_1x_coco`](https://ml.azure.com/registries/azureml/models/mmd-3x-yolof_r50_c5_8x8_1x_coco/version/8) |
| Instance Segmentation | **Mask R-CNN** | [`mmd-3x-mask-rcnn_swin-t-p4-w7_fpn_1x_coco`](https://ml.azure.com/registries/azureml/models/mmd-3x-mask-rcnn_swin-t-p4-w7_fpn_1x_coco/version/8) |

The list of curated models is constantly updated. You can get the most up-to-date list of curated models for a given task by using the Python SDK.
```
credential = DefaultAzureCredential()
ml_client = MLClient(credential, registry_name="azureml")

models = ml_client.models.list()
classification_models = []
for model in models:
    model = ml_client.models.get(model.name, label="latest")
    if model.tags['task'] == 'image-classification': # choose an image task
        classification_models.append(model.name)

classification_models
```
Output:
```
['google-vit-base-patch16-224',
 'microsoft-swinv2-base-patch4-window12-192-22k',
 'facebook-deit-base-patch16-224',
 'microsoft-beit-base-patch16-224-pt22k-ft22k']
```
Using any HuggingFace or MMDetection model triggers runs that use pipeline components. If you use both legacy and HuggingFace/MMdetection models, all runs and trials use components. 


In addition to controlling the model architecture, you can also tune hyperparameters used for model training. While many of the exposed hyperparameters are model-agnostic, some hyperparameters are task-specific or model-specific. [Learn more about the available hyperparameters for these instances](reference-automl-images-hyperparameters.md). 

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

To use the default hyperparameter values for a given architecture, such as yolov5, specify the architecture with the `model_name` key in the `training_parameters` section. For example,

```yaml
training_parameters:
    model_name: yolov5
```
# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

To use the default hyperparameter values for a given architecture, such as yolov5, specify the architecture with the `model_name` parameter in the `set_training_parameters` method of the task specific `automl` job. For example,

```python
image_object_detection_job.set_training_parameters(model_name="yolov5")
```
---

### Manually sweeping model hyperparameters

When training computer vision models, model performance depends heavily on the hyperparameter values you select. Often, you need to tune the hyperparameters to get optimal performance. For computer vision tasks, you can sweep hyperparameters to find the optimal settings for your model. This feature applies the hyperparameter tuning capabilities in Azure Machine Learning. [Learn how to tune hyperparameters](how-to-tune-hyperparameters.md).

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
search_space:
  - model_name:
      type: choice
      values: [yolov5]
    learning_rate:
      type: uniform
      min_value: 0.0001
      max_value: 0.01
    model_size:
      type: choice
      values: [small, medium]

  - model_name:
      type: choice
      values: [fasterrcnn_resnet50_fpn]
    learning_rate:
      type: uniform
      min_value: 0.0001
      max_value: 0.001
    optimizer:
      type: choice
      values: [sgd, adam, adamw]
    min_size:
      type: choice
      values: [600, 800]
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=search-space-settings)]

---

#### Define the parameter search space

Define the model architectures and hyperparameters to sweep in the parameter space. You can specify either a single model architecture or multiple architectures. 

* For the list of supported model architectures for each task type, see [Individual trials](#individual-trials). 
* For hyperparameters for each computer vision task type, see [Hyperparameters for computer vision tasks](reference-automl-images-hyperparameters.md). 
* For details on supported distributions for discrete and continuous hyperparameters, see [how to tune hyperparameters](how-to-tune-hyperparameters.md#define-the-search-space).

#### Sampling methods for the sweep

When you sweep hyperparameters, specify the sampling method to use for sweeping over the defined parameter space. Currently, the `sampling_algorithm` parameter supports the following sampling methods:

| Sampling type | AutoML Job syntax |
|-------|---------|
|[Random Sampling](how-to-tune-hyperparameters.md#random-sampling)| `random` |
|[Grid Sampling](how-to-tune-hyperparameters.md#grid-sampling)| `grid` |
|[Bayesian Sampling](how-to-tune-hyperparameters.md#bayesian-sampling)| `bayesian` |
    
> [!NOTE]
> Currently, only random and grid sampling support conditional hyperparameter spaces.

#### Early termination policies

Automatically end poorly performing trials by using an early termination policy. Early termination improves computational efficiency by saving compute resources that would be otherwise spent on less promising trials. Automated ML for images supports the following early termination policies by using the `early_termination` parameter. If you don't specify a termination policy, all trials run to completion.


| Early termination policy | AutoML Job syntax |
|-------|---------|
|[Bandit policy](how-to-tune-hyperparameters.md#bandit-policy)| CLI v2: `bandit` <br> SDK v2: `BanditPolicy()` |
|[Median stopping policy](how-to-tune-hyperparameters.md#median-stopping-policy)| CLI v2: `median_stopping` <br> SDK v2: `MedianStoppingPolicy()` |
|[Truncation selection policy](how-to-tune-hyperparameters.md#truncation-selection-policy)| CLI v2: `truncation_selection` <br> SDK v2: `TruncationSelectionPolicy()` |

For more information, see [how to configure the early termination policy for your hyperparameter sweep](how-to-tune-hyperparameters.md#early-termination).

> [!NOTE]
> For a complete sweep configuration sample, see [tutorial](tutorial-auto-train-image-models.md#manual-hyperparameter-sweeping-for-image-tasks).


You can configure all the sweep related parameters as shown in the following example.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
sweep:
  sampling_algorithm: random
  early_termination:
    type: bandit
    evaluation_interval: 2
    slack_factor: 0.2
    delay_evaluation: 6
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=sweep-settings)]

---

#### Fixed settings

Pass fixed settings or parameters that don't change during the parameter space sweep as shown in the following example.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
training_parameters:
  early_stopping: True
  evaluation_frequency: 1
```


# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]
 
[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=pass-arguments)]


---

## Data augmentation 

In general, deep learning model performance can often improve with more data. Data augmentation is a practical technique to amplify the data size and variability of a dataset. This technique helps prevent overfitting and improves the model's generalization ability on unseen data. Automated ML applies different data augmentation techniques based on the computer vision task, before feeding input images to the model. Currently, no hyperparameter controls data augmentations. 

|Task | Impacted dataset | Data augmentation techniques applied |
|-------|----------|---------|
|Image classification (multiclass and multilabel) | Training <br><br><br> Validation and test| Random resize and crop, horizontal flip, color jitter (brightness, contrast, saturation, and hue), normalization by using channel-wise ImageNet's mean and standard deviation <br><br><br>Resize, center crop, normalization |
|Object detection, instance segmentation| Training <br><br> Validation and test |Random crop around bounding boxes, expand, horizontal flip, normalization, resize <br><br><br>Normalization, resize
|Object detection using yolov5| Training <br><br> Validation and test  |Mosaic, random affine (rotation, translation, scale, shear), horizontal flip <br><br><br> Letterbox resizing|

The model applies the augmentations defined in the previous table by default for an Automated ML for image job. To provide control over augmentations, Automated ML for images exposes the following two flags to turn off certain augmentations. Currently, these flags support only object detection and instance segmentation tasks. 
 1. **apply_mosaic_for_yolo:** This flag is specific to the Yolo model. Set it to False to turn off the mosaic data augmentation. The model applies this augmentation at training time.
 1. **apply_automl_train_augmentations:** Set this flag to false to turn off the augmentation that the model applies during training time for the object detection and instance segmentation models. For augmentations, see the details in the table above.
    - For non-yolo object detection model and instance segmentation models, this flag turns off only the first three augmentations. For example: *Random crop around bounding boxes, expand, horizontal flip*. The normalization and resize augmentations are still applied regardless of this flag.
    - For Yolo model, this flag turns off the random affine and horizontal flip augmentations.

You can set these two flags through *advanced_settings* under *training_parameters*.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
training_parameters:
  advanced_settings: >
    {"apply_mosaic_for_yolo": false}
```
```yaml
training_parameters:
  advanced_settings: >
    {"apply_automl_train_augmentations": false}
```
 These two flags are independent of each other. You can also use them in combination by using the following settings.
 ```yaml
training_parameters:
  advanced_settings: >
    {"apply_automl_train_augmentations": false, "apply_mosaic_for_yolo": false}
```

# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]
 
```python
from azure.ai.ml import automl

image_object_detection_job = automl.image_object_detection(...)

image_object_detection_job.set_training_parameters(
    ...,
    advanced_settings='{"apply_mosaic_for_yolo": false}'
)
```

```python
from azure.ai.ml import automl

image_object_detection_job = automl.image_object_detection(...)

image_object_detection_job.set_training_parameters(
    ...,
    advanced_settings='{"apply_automl_train_augmentations": false}'
)
```
 These two flags are independent of each other. You can also use them in combination by using the following settings.

```python
from azure.ai.ml import automl

image_object_detection_job = automl.image_object_detection(...)

image_object_detection_job.set_training_parameters(
    ...,
    advanced_settings='{"apply_automl_train_augmentations": false, "apply_mosaic_for_yolo": false}'
)
```

---

In our experiments, these augmentations help the model to generalize better. If you switch off these augmentations, combine them with other offline augmentations to get better results.


##  Incremental training (optional)

After the training job finishes, you can further train the model by loading the trained model checkpoint. Use the same dataset or a different dataset for incremental training. If you're satisfied with the model, stop training and use the current model. 


### Pass the checkpoint via job ID

Pass the job ID to load the checkpoint from.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
training_parameters:
  checkpoint_run_id : "target_checkpoint_run_id"
```


# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

To find the job ID from the desired model, use the following code. 

```python
# find a job id to get a model checkpoint from
import mlflow

# Obtain the tracking URL from MLClient
MLFLOW_TRACKING_URI = ml_client.workspaces.get(
    name=ml_client.workspace_name
).mlflow_tracking_uri
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

from mlflow.tracking.client import MlflowClient

mlflow_client = MlflowClient()
mlflow_parent_run = mlflow_client.get_run(automl_job.name)

# Fetch the id of the best automl child trial.
target_checkpoint_run_id = mlflow_parent_run.data.tags["automl_best_child_run_id"]
```

To pass a checkpoint through the job ID, use the `checkpoint_run_id` parameter in the `set_training_parameters` function.

```python
image_object_detection_job = automl.image_object_detection(
    compute=compute_name,
    experiment_name=exp_name,
    training_data=my_training_data_input,
    validation_data=my_validation_data_input,
    target_column_name="label",
    primary_metric=ObjectDetectionPrimaryMetrics.MEAN_AVERAGE_PRECISION,
    tags={"my_custom_tag": "My custom value"},
)

image_object_detection_job.set_training_parameters(checkpoint_run_id=target_checkpoint_run_id)

automl_image_job_incremental = ml_client.jobs.create_or_update(
    image_object_detection_job
) 
```

---


## Submit the AutoML job



# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

To submit your AutoML job, run the following CLI v2 command with the path to your .yml file, workspace name, resource group, and subscription ID.

```azurecli
az ml job create --file ./hello-automl-job-basic.yml --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

When you configure your AutoML Job, submit the job.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=submit-run)]
---

## Outputs and evaluation metrics

The automated ML training job generates output model files, evaluation metrics, logs, and deployment artifacts like the scoring file and the environment file. You can view these files and metrics from the outputs and logs and metrics tab of the child jobs.

> [!TIP]
> Check how to navigate to the job results from the  [View job results](how-to-understand-automated-ml.md#view-job-results) section.

For definitions and examples of the performance charts and metrics provided for each job, see [Evaluate automated machine learning experiment results](how-to-understand-automated-ml.md#metrics-for-image-models-preview).

## Register and deploy model

When the job finishes, register the model created from the best trial (configuration that results in the best primary metric). You can register the model after downloading it or by specifying the azureml path with the corresponding job ID.  If you want to change the inference settings, download the model, change `settings.json`, and register the updated model folder.

### Get the best trial

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
CLI example not available, please use Python SDK.
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=best_run)] 

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=create_local_dir)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=download_model)]
---

### Register the model

Register the model by using either the azureml path or your locally downloaded path. 

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
 az ml model create --name od-fridge-items-mlflow-model --version 1 --path azureml://jobs/$best_run/outputs/artifacts/outputs/mlflow-model/ --type mlflow_model --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```
# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=register_model)]    
---

After you register the model, you can deploy it by using the managed online endpoint [deploy-managed-online-endpoint](how-to-deploy-managed-online-endpoint-sdk-v2.md).

### Configure online endpoint

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/managedOnlineEndpoint.schema.json
name: od-fridge-items-endpoint
auth_mode: key
```
    
# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=endpoint)]    

---

### Create the endpoint

Use the previously created `MLClient` to create the endpoint in the workspace. This command starts the endpoint creation and returns a confirmation response while the endpoint creation continues.


# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
```azurecli
az ml online-endpoint create --file .\create_endpoint.yml --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=create_endpoint)]
---

### Configure online deployment

A deployment is a set of resources required for hosting the model that does the actual inferencing. Create a deployment for your endpoint by using the `ManagedOnlineDeployment` class. You can use either GPU or CPU VM versions for your deployment cluster.


# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
name: od-fridge-items-mlflow-deploy
endpoint_name: od-fridge-items-endpoint
model: azureml:od-fridge-items-mlflow-model@latest
instance_type: Standard_DS3_v2
instance_count: 1
liveness_probe:
    failure_threshold: 30
    success_threshold: 1
    timeout: 2
    period: 10
    initial_delay: 2000
readiness_probe:
    failure_threshold: 10
    success_threshold: 1
    timeout: 10
    period: 10
    initial_delay: 2000 
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=deploy)]
---


### Create the deployment

Use the `MLClient` you created earlier to create the deployment in the workspace. This command starts the deployment creation and returns a confirmation response while the deployment creation continues.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml online-deployment create --file .\create_deployment.yml --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=create_deploy)]
---

### Update traffic

By default, the current deployment is set to receive 0% traffic. Set the traffic percentage the current deployment should receive. The sum of traffic percentages of all the deployments with one endpoint can't exceed 100%.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml online-endpoint update --name 'od-fridge-items-endpoint' --traffic 'od-fridge-items-mlflow-deploy=100' --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=update_traffic)]
---


Alternatively, you can deploy the model from the [Azure Machine Learning studio UI](https://ml.azure.com/). 
Navigate to the model you want to deploy in the **Models** tab of the automated ML job. Select **Deploy** and then select **Deploy to real-time endpoint**.  

![Screenshot of how the Deployment page looks like after selecting the Deploy option.](./media/how-to-auto-train-image-models/deploy-end-point.png).

This is how your review page looks. You can select the instance type, instance count, and set the traffic percentage for the current deployment.

![Screenshot of how the top of review page looks like after selecting the options to deploy.](./media/how-to-auto-train-image-models/review-deploy-1.png).
![Screenshot of how the bottom of review page looks like after selecting the options to deploy.](./media/how-to-auto-train-image-models/review-deploy-2.png).

### Update inference settings

In the previous step, you downloaded the `mlflow-model/artifacts/settings.json` file from the best model. Use this file to update the inference settings before registering the model. For the best performance, use the same parameters as training.

Each task (and some models) has a set of parameters. By default, the same values are used for the parameters during training and validation. Depending on the behavior you need when using the model for inference, you can change these parameters. The following list shows the parameters for each task type and model.  

| Task | Parameter name | Default  |
|--------- |------------- | --------- |
|Image classification (multiclass and multilabel) | `valid_resize_size`<br>`valid_crop_size` | 256<br>224 |
|Object detection | `min_size`<br>`max_size`<br>`box_score_thresh`<br>`nms_iou_thresh`<br>`box_detections_per_img` | 600<br>1333<br>0.3<br>0.5<br>100 |
|Object detection using `yolov5`| `img_size`<br>`model_size`<br>`box_score_thresh`<br>`nms_iou_thresh` | 640<br>medium<br>0.1<br>0.5 |
|Instance segmentation| `min_size`<br>`max_size`<br>`box_score_thresh`<br>`nms_iou_thresh`<br>`box_detections_per_img`<br>`mask_pixel_score_threshold`<br>`max_number_of_polygon_points`<br>`export_as_image`<br>`image_type` | 600<br>1333<br>0.3<br>0.5<br>100<br>0.5<br>100<br>False<br>JPG|

For a detailed description on task specific hyperparameters, refer to [Hyperparameters for computer vision tasks in automated machine learning](./reference-automl-images-hyperparameters.md).
    
If you want to use tiling and control tiling behavior, the following parameters are available: `tile_grid_size`, `tile_overlap_ratio`, and `tile_predictions_nms_thresh`. For more details on these parameters, see [Train a small object detection model using AutoML](./how-to-use-automl-small-object-detect.md).

###  Test the deployment
To test the deployment and visualize the detections from the model, see [Test the deployment](./tutorial-auto-train-image-models.md#test-the-deployment).

## Generate explanations for predictions

> [!IMPORTANT]
> These settings are currently in public preview. They're provided without a service-level agreement. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

> [!WARNING]
>  **Model Explainability** supports only **multiclass classification** and **multilabel classification**.

Some advantages of using Explainable AI (XAI) with AutoML for images include:
- Improved transparency in the complex vision model predictions
- Helps users understand the important features or pixels in the input image that contribute to the model predictions
- Helps troubleshoot the models
- Helps discover bias

### Explanations
Explanations are **feature attributions** or weights you give to each pixel in the input image based on its contribution to the model's prediction. Each weight can be negative (negatively correlated with the prediction) or positive (positively correlated with the prediction). You calculate these attributions against the predicted class. For multiclass classification, you generate exactly one attribution matrix of size `[3, valid_crop_size, valid_crop_size]` per sample. For multilabel classification, you generate an attribution matrix of size `[3, valid_crop_size, valid_crop_size]` for each predicted label or class for each sample.

By using Explainable AI in AutoML for Images on the deployed endpoint, you can get **visualizations** of explanations (attributions overlaid on an input image) and **attributions** (multidimensional array of size `[3, valid_crop_size, valid_crop_size]`) for each image. Apart from visualizations, you can also get attribution matrices to gain more control over the explanations, like generating custom visualizations using attributions or scrutinizing segments of attributions. All the explanation algorithms use cropped square images with size `valid_crop_size` for generating attributions.


You can generate explanations from either an **online endpoint** or a **batch endpoint**. Once you deploy the endpoint, you can use it to generate the explanations for predictions. In online deployments, make sure to pass the `request_settings = OnlineRequestSettings(request_timeout_ms=90000)` parameter to `ManagedOnlineDeployment` and set `request_timeout_ms` to its maximum value to avoid **timeout issues** while generating explanations (refer to the [register and deploy model section](#register-and-deploy-model)). Some of the explainability (XAI) methods, like `xrai`, consume more time, especially for multilabel classification as you need to generate attributions and visualizations against each predicted label. Use any GPU instance for faster explanations. For more information on input and output schema for generating explanations, see the [schema docs](reference-automl-images-schema.md#data-format-for-online-scoring-and-explainability-xai).


AutoML for images supports the following state-of-the-art explainability algorithms:
   - [XRAI](https://arxiv.org/abs/1906.02825) (xrai)
   - [Integrated Gradients](https://arxiv.org/abs/1703.01365) (integrated_gradients)
   - [Guided GradCAM](https://arxiv.org/abs/1610.02391v4) (guided_gradcam)
   - [Guided BackPropagation](https://arxiv.org/abs/1412.6806) (guided_backprop)

The following table describes the explainability algorithm specific tuning parameters for XRAI and Integrated Gradients. Guided backpropagation and guided gradcam don't require any tuning parameters.

| XAI algorithm | Algorithm specific parameters  | Default Values |
|--------- |------------- | --------- |
| `xrai` | 1. `n_steps`: The number of steps used by the approximation method. A larger number of steps lead to better approximations of attributions (explanations). The range of n_steps is [2, inf), but the performance of attributions starts to converge after 50 steps. <br> `Optional, Int` <br><br> 2. `xrai_fast`: Whether to use faster version of XRAI. if `True`, then computation time for explanations is faster but leads to less accurate explanations (attributions) <br>`Optional, Bool` <br> | `n_steps = 50` <br> `xrai_fast = True` |
| `integrated_gradients` | 1. `n_steps`: The number of steps used by the approximation method. A larger number of steps lead to better attributions (explanations). The range of n_steps is [2, inf), but the performance of attributions starts to converge after 50 steps.<br> `Optional, Int` <br><br> 2. `approximation_method`: Method for approximating the integral. Available approximation methods are `riemann_middle` and `gausslegendre`.<br> `Optional, String` | `n_steps = 50` <br> `approximation_method = riemann_middle` |


Internally, the XRAI algorithm uses integrated gradients. So, both integrated gradients and XRAI algorithms require the `n_steps` parameter. A larger number of steps consumes more time for approximating the explanations and it might result in timeout problems on the online endpoint.

For better explanations, use XRAI > Guided GradCAM > Integrated Gradients > Guided BackPropagation algorithms. For faster explanations, use Guided BackPropagation > Guided GradCAM > Integrated Gradients > XRAI in the specified order.

A sample request to the online endpoint looks like the following. This request generates explanations when `model_explainability` is set to `True`. The following request generates visualizations and attributions by using the faster version of the XRAI algorithm with 50 steps.

```python
import base64
import json

def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()

sample_image = "./test_image.jpg"

# Define explainability (XAI) parameters
model_explainability = True
xai_parameters = {"xai_algorithm": "xrai",
                  "n_steps": 50,
                  "xrai_fast": True,
                  "visualizations": True,
                  "attributions": True}

# Create request json
request_json = {"input_data": {"columns":  ["image"],
                               "data": [json.dumps({"image_base64": base64.encodebytes(read_image(sample_image)).decode("utf-8"),
                                                    "model_explainability": model_explainability,
                                                    "xai_parameters": xai_parameters})],
                               }
                }

request_file_name = "sample_request_data.json"

with open(request_file_name, "w") as request_file:
    json.dump(request_json, request_file)

resp = ml_client.online_endpoints.invoke(
    endpoint_name=online_endpoint_name,
    deployment_name=deployment.name,
    request_file=request_file_name,
)
predictions = json.loads(resp)
```

For more information on generating explanations, see [GitHub notebook repository for automated machine learning samples](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs).

### Interpreting visualizations
The deployed endpoint returns a base64 encoded image string if both `model_explainability` and `visualizations` are set to `True`. Decode the base64 string as described in the [notebooks](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs) or use the following code to decode and visualize the base64 image strings in the prediction.

```python
import base64
from io import BytesIO
from PIL import Image

def base64_to_img(base64_img_str):
    base64_img = base64_img_str.encode("utf-8")
    decoded_img = base64.b64decode(base64_img)
    return BytesIO(decoded_img).getvalue()

# For Multi-class classification:
# Decode and visualize base64 image string for explanations for first input image
# img_bytes = base64_to_img(predictions[0]["visualizations"])

# For  Multi-label classification:
# Decode and visualize base64 image string for explanations for first input image against one of the classes
img_bytes = base64_to_img(predictions[0]["visualizations"][0])
image = Image.open(BytesIO(img_bytes))
```

The following picture shows the visualization of explanations for a sample input image.
![Screenshot of visualizations generated by XAI for AutoML for images.](./media/how-to-auto-train-image-models/xai-visualization.jpg)

The decoded base64 figure has four image sections within a 2 x 2 grid.

- Image at top-left corner (0, 0) is the cropped input image.
- Image at top-right corner (0, 1) is the heatmap of attributions on a color scale bgyw (blue green yellow white) where the contribution of white pixels on the predicted class is the highest and blue pixels is the lowest.
- Image at bottom-left corner (1, 0) is blended heatmap of attributions on cropped input image.
- Image at bottom-right corner (1, 1) is the cropped input image with top 30 percent of the pixels based on attribution scores.


### Interpreting attributions
The deployed endpoint returns attributions if both `model_explainability` and `attributions` are set to `True`. For more details, refer to [multi-class classification and multi-label classification notebooks](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs).

These attributions give users more control to generate custom visualizations or to scrutinize pixel level attribution scores.
The following code snippet describes a way to generate custom visualizations using attribution matrix. For more information on the schema of attributions for multi-class classification and multi-label classification, see the [schema docs](reference-automl-images-schema.md#data-format-for-online-scoring-and-explainability-xai).

Use the exact `valid_resize_size` and `valid_crop_size` values of the selected model to generate the explanations (default values are 256 and 224 respectively). The following code uses [Captum](https://captum.ai/) visualization functionality to generate custom visualizations. Users can utilize any other library to generate visualizations. For more details, please refer to the [captum visualization utilities](https://captum.ai/api/utilities.html#visualization).

```python
import colorcet as cc
import numpy as np
from captum.attr import visualization as viz
from PIL import Image
from torchvision import transforms

def get_common_valid_transforms(resize_to=256, crop_size=224):

    return transforms.Compose([
        transforms.Resize(resize_to),
        transforms.CenterCrop(crop_size)
    ])

# Load the image
valid_resize_size = 256
valid_crop_size = 224
sample_image = "./test_image.jpg"
image = Image.open(sample_image)
# Perform common validation transforms to get the image used to generate attributions
common_transforms = get_common_valid_transforms(resize_to=valid_resize_size,
                                                crop_size=valid_crop_size)
input_tensor = common_transforms(image)

# Convert output attributions to numpy array

# For Multi-class classification:
# Selecting attribution matrix for first input image
# attributions = np.array(predictions[0]["attributions"])

# For  Multi-label classification:
# Selecting first attribution matrix against one of the classes for first input image
attributions = np.array(predictions[0]["attributions"][0])

# visualize results
viz.visualize_image_attr_multiple(np.transpose(attributions, (1, 2, 0)),
                                  np.array(input_tensor),
                                  ["original_image", "blended_heat_map"],
                                  ["all", "absolute_value"],
                                  show_colorbar=True,
                                  cmap=cc.cm.bgyw,
                                  titles=["original_image", "heatmap"],
                                  fig_size=(12, 12))
```

## Large datasets

If you're using AutoML to train on large datasets, some experimental settings might be useful.

> [!IMPORTANT]
> These settings are currently in public preview. They're provided without a service-level agreement. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

### Multi-GPU and multinode training

By default, each model trains on a single VM. If training a model takes too much time, using VMs that contain multiple GPUs might help. The time to train a model on large datasets decreases in roughly linear proportion to the number of GPUs used. For instance, a model trains roughly twice as fast on a VM with two GPUs as on a VM with one GPU. If the time to train a model is still high on a VM with multiple GPUs, you can increase the number of VMs used to train each model. Similar to multi-GPU training, the time to train a model on large datasets also decreases in roughly linear proportion to the number of VMs used. When you train a model across multiple VMs, be sure to use a compute SKU that supports [InfiniBand](how-to-train-distributed-gpu.md#accelerating-distributed-gpu-training-with-infiniband) for best results. You can configure the number of VMs used to train a single model by setting the `node_count_per_trial` property of the AutoML job.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
properties:
  node_count_per_trial: "2"
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

All tasks support multinode training. You can specify the `node_count_per_trial` property by using the task-specific `automl` functions. For example, for object detection:

```python
from azure.ai.ml import automl

image_object_detection_job = automl.image_object_detection(
    ...,
    properties={"node_count_per_trial": 2}
)
```
---

### Streaming image files from storage

By default, the training process downloads all image files to disk before it starts. If the size of the image files is greater than the available disk space, the job fails. To avoid this problem, select the option to stream image files from Azure storage during training. The training process streams image files from Azure storage directly to system memory, bypassing disk. At the same time, the process caches as many files as possible from storage on disk to minimize the number of requests to storage.

> [!NOTE]
> If you enable streaming, make sure the Azure storage account is in the same region as the compute resource to minimize cost and latency.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
training_parameters:
  advanced_settings: >
    {"stream_image_files": true}
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml import automl

image_object_detection_job = automl.image_object_detection(...)

image_object_detection_job.set_training_parameters(
    ...,
    advanced_settings='{"stream_image_files": true}'
)
```
---


## Example notebooks
For detailed code examples and use cases, see the [GitHub notebook repository for automated machine learning samples](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs). Check the folders with the 'automl-image-' prefix for samples specific to building computer vision models.


## Code examples

# [Azure CLI](#tab/cli)

For detailed code examples and use cases, see the [azureml-examples repository for automated machine learning samples](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/automl-standalone-jobs). 


# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

For detailed code examples and use cases, see the [GitHub notebook repository for automated machine learning samples](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs). 

---
## Next steps

* [Tutorial: Train an object detection model with AutoML and Python](tutorial-auto-train-image-models.md).
