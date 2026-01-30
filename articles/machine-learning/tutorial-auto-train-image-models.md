---
title: 'Tutorial: AutoML- Train an Object Detection Model'
titleSuffix: Azure Machine Learning
description: Train an object detection model to determine whether an image contains certain objects by using automated ML and the Azure Machine Learning CLI v2 or Python SDK v2.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: tutorial
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.date: 01/28/2026
ms.custom: devx-track-python, automl, devx-track-azurecli, update-code, build-2023
---

# Tutorial: Train an object detection model with AutoML and Python

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this tutorial, you learn how to train an object detection model by using Azure Machine Learning automated ML with the Azure Machine Learning CLI extension v2 or the Azure Machine Learning Python SDK v2.
This object detection model identifies whether an image contains objects, such as a can, carton, milk bottle, or water bottle.

Automated ML accepts training data and configuration settings and automatically iterates through combinations of different feature normalization/standardization methods, models, and hyperparameter settings to arrive at the best model.

You write code by using the Python SDK in this tutorial and learn the following tasks:

> [!div class="checklist"]
> * Download and transform data
> * Train an automated machine learning object detection model
> * Specify hyperparameter values for your model
> * Perform a hyperparameter sweep
> * Deploy your model
> * Visualize detections

## Prerequisites

* [!INCLUDE [prereq-workspace](includes/prereq-workspace.md)]

* Use Python 3.10 or later.

* Download and unzip the [odFridgeObjects.zip](https://automlsamplenotebookdata.blob.core.windows.net/image-object-detection/odFridgeObjects.zip) data file. The dataset is annotated in Pascal VOC format, where each image corresponds to an XML file. Each XML file contains information on where its corresponding image file is located and also contains information about the bounding boxes and the object labels. To use this data, you first need to convert it to the required JSONL format, as shown in the [Convert the downloaded data to JSONL](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb) section of the automl-image-object-detection-task-fridge-items.ipynb
notebook.

* Use a compute instance to complete this tutorial without further installation. (See [Create a compute instance](./quickstart-create-resources.md#create-a-compute-instance).) Or install the CLI or SDK to use your own local environment.
    
    # [Azure CLI](#tab/cli)
    
    [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
    
    
    This tutorial is also available in the [azureml-examples repository on GitHub](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/automl-standalone-jobs/cli-automl-image-object-detection-task-fridge-items). If you want to run it in your local environment, install and [set up CLI (v2)](how-to-configure-cli.md#prerequisites) and make sure you install the `ml` extension.
    
    # [Python SDK](#tab/python)
    
    [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]
    
    
    This tutorial is also available in the [azureml-examples repository on GitHub](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items). If you want to run it in your local environment, use the following commands to install Azure Machine Learning Python SDK v2:

    * Uninstall previous preview version:
        ```python
        pip uninstall azure-ai-ml
        ```
    * Install the Azure Machine Learning Python SDK v2:
        ```python
        pip install azure-ai-ml azure-identity
        ```
    
    ---

## Compute target setup

> [!NOTE]
> To try [serverless compute](how-to-use-serverless-compute.md), skip this step and go to [Experiment setup](#experiment-setup).

You first need to set up a compute target to use for your automated ML model training. Automated ML models for image tasks require GPU SKUs.

This tutorial uses the NCsv3-series (with V100 GPUs) because this type of compute target uses multiple GPUs to speed up training. Additionally, you can set up multiple nodes to take advantage of parallelism when tuning hyperparameters for your model.

The following code creates a GPU compute of size Standard_NC64as_T4_v3 with four nodes.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

Create a .yml file with the following configuration.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/amlCompute.schema.json 
name: gpu-cluster
type: amlcompute
size: Standard_NC64as_T4_v3
min_instances: 0
max_instances: 4
idle_time_before_scale_down: 120
```

To create the compute, you run the following CLI v2 command with the path to your .yml file, workspace name, resource group, and subscription ID.

```azurecli
az ml compute create -f [PATH_TO_YML_FILE] --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```



# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml.entities import AmlCompute
compute_name = "gpu-cluster"
cluster_basic = AmlCompute(
    name=compute_name,
    type="amlcompute",
    size="Standard_NC64as_T4_v3",
    min_instances=0,
    max_instances=4,
    idle_time_before_scale_down=120,
)
ml_client.begin_create_or_update(cluster_basic)
```
This compute is used later when you create the task-specific AutoML job.

---

## Experiment setup

You can use an experiment to track your model training jobs.

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
You can provide the experiment name by using the `experiment_name` key: 

```yaml
experiment_name: dpv2-cli-automl-image-object-detection-experiment
```

# [Python SDK](#tab/python)
 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

The experiment name is used later when you create the task-specific AutoML job.
```python
exp_name = "dpv2-image-object-detection-experiment"
```
---

## Visualize input data

After you have the input image data prepared in [JSONL](https://jsonlines.org/) (JSON Lines) format, you can visualize the ground truth bounding boxes for an image. To do so, be sure you have `matplotlib` installed.

```
%pip install --upgrade matplotlib
```

```python

%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from PIL import Image as pil_image
import numpy as np
import json
import os

def plot_ground_truth_boxes(image_file, ground_truth_boxes):
    # Display the image
    plt.figure()
    img_np = mpimg.imread(image_file)
    img = pil_image.fromarray(img_np.astype("uint8"), "RGB")
    img_w, img_h = img.size

    fig,ax = plt.subplots(figsize=(12, 16))
    ax.imshow(img_np)
    ax.axis("off")

    label_to_color_mapping = {}

    for gt in ground_truth_boxes:
        label = gt["label"]

        xmin, ymin, xmax, ymax =  gt["topX"], gt["topY"], gt["bottomX"], gt["bottomY"]
        topleft_x, topleft_y = img_w * xmin, img_h * ymin
        width, height = img_w * (xmax - xmin), img_h * (ymax - ymin)

        if label in label_to_color_mapping:
            color = label_to_color_mapping[label]
        else:
            # Generate a random color. If you want to use a specific color, you can use something like "red."
            color = np.random.rand(3)
            label_to_color_mapping[label] = color

        # Display bounding box
        rect = patches.Rectangle((topleft_x, topleft_y), width, height,
                                 linewidth=2, edgecolor=color, facecolor="none")
        ax.add_patch(rect)

        # Display label
        ax.text(topleft_x, topleft_y - 10, label, color=color, fontsize=20)

    plt.show()

def plot_ground_truth_boxes_jsonl(image_file, jsonl_file):
    image_base_name = os.path.basename(image_file)
    ground_truth_data_found = False
    with open(jsonl_file) as fp:
        for line in fp.readlines():
            line_json = json.loads(line)
            filename = line_json["image_url"]
            if image_base_name in filename:
                ground_truth_data_found = True
                plot_ground_truth_boxes(image_file, line_json["label"])
                break
    if not ground_truth_data_found:
        print("Unable to find ground truth information for image: {}".format(image_file))
```

By using the preceding helper functions, for any given image, you can run the following code to display the bounding boxes.

```python
image_file = "./odFridgeObjects/images/31.jpg"
jsonl_file = "./odFridgeObjects/train_annotations.jsonl"

plot_ground_truth_boxes_jsonl(image_file, jsonl_file)
```

## Upload data and create an MLTable

To use data for training, upload it to the default blob storage of your Azure Machine Learning workspace and register it as an asset. The benefits of registering data are:
- Easy to share with other members of the team.
- Versioning of the metadata (location, description, and so on).
- Lineage tracking.

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

Create a .yml file with the following configuration.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/data.schema.json
name: fridge-items-images-object-detection
description: Fridge-items images Object detection
path: ./data/odFridgeObjects
type: uri_folder
```

To upload the images as a data asset, run the following CLI v2 command with the path to your .yml file, workspace name, resource group, and subscription ID.

```azurecli
az ml data create -f [PATH_TO_YML_FILE] --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)
 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=upload-data)]

---

The next step is to create an MLTable from your data in JSONL format, as shown in the following example. An MLTable packages your data into a consumable object for training.

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

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

The following configuration creates training and validation data from the MLTable.

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


You can create data inputs from the training and validation MLTable by using the following code:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=data-load)]

---

## Configure your object detection experiment

To configure automated ML jobs for image-related tasks, create a task-specific AutoML job.

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

> [!note]
> To use [serverless compute](how-to-use-serverless-compute.md), replace the line `compute: azureml:gpu-cluster` with this code:
> ```yml
> resources:
>  instance_type: Standard_NC64as_T4_v3
>  instance_count: 4
> ```

```yaml
task: image_object_detection
primary_metric: mean_average_precision
compute: azureml:gpu-cluster
```

# [Python SDK](#tab/python)
 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]


[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=image-object-detection-configuration)]

> [!NOTE]
> To use [serverless compute](how-to-use-serverless-compute.md), replace the line `compute="cpu-cluster"` with this code:
> ```python
> image_object_detection_job.resources = ResourceConfiguration(instance_type="Standard_NC64as_T4_v3",instance_count =4)
> 
> image_object_detection_job.set_limits(
>     max_trials=10,
>     max_concurrent_trials=2,
> )
> ```

---

### Automatic hyperparameter sweeping for image tasks (AutoMode)

In your AutoML job, you can perform an automatic hyperparameter sweep to find the optimal model. (This functionality is called AutoMode). You only specify the number of trials. The hyperparameter search space, sampling method, and early termination policy aren't needed. The system automatically determines the region of the hyperparameter space to sweep based on the number of trials. A value between 10 and 20 will probably work well on many datasets.

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
# Trigger AutoMode
image_object_detection_job.set_limits(max_trials=10, max_concurrent_trials=2)
```
---

You can then submit the job to train an image model.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

To submit your AutoML job, you run the following CLI v2 command with the path to your .yml file, workspace name, resource group, and subscription ID.

```azurecli
az ml job create --file ./hello-automl-job-basic.yml --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)
 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

After you configure your AutoML job with the settings you want, you can submit the job.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=submit-run)]

---

### Manual hyperparameter sweeping for image tasks

In your AutoML job, you can specify the model architectures by using the `model_name` parameter and configure the settings to perform a hyperparameter sweep over a defined search space to find the optimal model.

In this example, you train an object detection model with YOLOv5 and FasterRCNN ResNet50 FPN, both of which are pretrained on COCO, a large-scale object detection, segmentation, and captioning dataset that contains thousands of labeled images with more than 80 label categories.

You can perform a hyperparameter sweep over a defined search space to find the optimal model.

#### Job limits

You can control the resources spent on your AutoML image training job by specifying the `timeout_minutes`, `max_trials`, and `max_concurrent_trials` for the job in limit settings. For more information, see the [description of job limits parameters](./how-to-auto-train-image-models.md#job-limits).
# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
limits:
  timeout_minutes: 60
  max_trials: 10
  max_concurrent_trials: 2
```

# [Python SDK](#tab/python)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=limit-settings)]

---

The following code defines the search space in preparation for the hyperparameter sweep for each defined architecture, YOLOv5 and FasterRCNN ResNet50 FPN. In the search space, specify the range of values for `learning_rate`, `optimizer`, `lr_scheduler`, and so on, for AutoML to choose from as it attempts to generate a model with the optimal primary metric. If hyperparameter values aren't specified, default values are used for each architecture.

For the tuning settings, use random sampling to pick samples from this parameter space by using the `random` sampling algorithm. The job limits specified in the preceding code configure automated ML to try a total of 10 trials with these different samples, running two trials at a time on the compute target, which is set up using four nodes. The more parameters the search space has, the more trials you need to find optimal models.

The Bandit early termination policy is also used. This policy terminates poorly performing trials. That is, trials that aren't within 20% slack of the best performing trial. This termination significantly saves compute resources.

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


[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=sweep-settings)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=search-space-settings)]

---

After you define the search space and sweep settings, you can submit the job to train an image model by using your training dataset.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

To submit your AutoML job, run the following CLI v2 command with the path to your .yml file, the workspace name, the resource group, and the subscription ID.

```azurecli
az ml job create --file ./hello-automl-job-basic.yml --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

After you configure your AutoML job with the settings you want, you can submit the job.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=submit-run)]

---

When you do a hyperparameter sweep, it can be useful to visualize the different trials that were tried by using the Hyperdrive UI. You can get to this UI by going to the **Child jobs** tab in the UI of the main AutoML image job that appears earlier, which is the Hyperdrive parent job. You can then go to the **Child jobs** tab of this one.

Alternatively, here you can directly see the Hyperdrive parent job and navigate to its **Child jobs** tab:

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
```yaml
CLI example not available. Use the the Python SDK.
```


# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
hd_job = ml_client.jobs.get(returned_job.name + '_HD')
hd_job
```

---

## Register and deploy the model

After the job finishes, you can register the model that was created from the best trial (the configuration that resulted in the best primary metric). You can either register the model after downloading or by specifying the `azureml` path with a corresponding `jobid`.  

### Get the best trial


# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
```yaml
CLI example not available. Use the Python SDK.
```


# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=best_run)] 

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=create_local_dir)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=download_model)]
---

### Register the model

Register the model by using either the `azureml` path or your locally downloaded path. 

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
 az ml model create --name od-fridge-items-mlflow-model --version 1 --path azureml://jobs/$best_run/outputs/artifacts/outputs/mlflow-model/ --type mlflow_model --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```
# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=register_model)]    
---

After you register the model you want to use, you can deploy it by using the [managed online endpoint](how-to-deploy-managed-online-endpoint-sdk-v2.md).

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

By using the `MLClient` created earlier, you'll now create the endpoint in the workspace. This command starts the endpoint creation and returns a confirmation response while the endpoint creation continues.


# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml online-endpoint create --file .\create_endpoint.yml --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=create_endpoint)]
---
You can also create a batch endpoint for batch inferencing on large volumes of data over a period of time. See the [object detection batch scoring](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items-batch-scoring) notebook for an example of batch inferencing using the batch endpoint.

### Configure online deployment

A deployment is a set of resources required for hosting the model that does the actual inferencing. The following code creates a deployment for the endpoint. You can use either GPU or CPU VM SKUs for your deployment cluster.

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

Using the `MLClient` created earlier, you'll create the deployment in the workspace. This command starts the deployment creation and returns a confirmation response while the deployment creation continues.

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

By default, the current deployment is set to receive 0% traffic. You can set the traffic percentage that the current deployment should receive. The sum of the traffic percentages of all the deployments with one endpoint shouldn't exceed 100%.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml online-endpoint update --name 'od-fridge-items-endpoint' --traffic 'od-fridge-items-mlflow-deploy=100' --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=update_traffic)]
---

## Test the deployment
# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
```yaml
CLI example not available. Use the Python SDK.
```

# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=create_inference_request)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=dump_inference_request)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=invoke_inference)]
---

## Visualize detections

Now that you've scored a test image, you can visualize the bounding boxes for the image. To do so, you need to have Matplotlib installed.
# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
```yaml
CLI example not available. Use the Python SDK.
```

# [Python SDK](#tab/python)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=visualize_detections)]
---

## Clean up resources

Don't complete this section if you plan to complete other Azure Machine Learning tutorials.

If you don't plan to use the resources you created, delete them so that you don't incur any charges.

1. In the Azure portal, select **Resource groups** in the left pane.
1. In the list of resource groups, select the resource group that you created.
1. Select **Delete resource group**.
1. Enter the resource group name. Then select **Delete**.

You can also keep the resource group but delete a single workspace. Go to the workspace page, and then select **Delete**.

## Next steps

In this automated machine learning tutorial, you completed the following tasks:

> [!div class="checklist"]
> * Configured a workspace and prepared data for an experiment
> * Trained an automated object detection model
> * Specified hyperparameter values for your model
> * Performed a hyperparameter sweep
> * Deployed your model
> * Visualized detections

* [Learn more about computer vision in automated ML](concept-automated-ml.md#computer-vision).
* [Learn how to set up AutoML to train computer vision models by using Python](how-to-auto-train-image-models.md).
* [Learn how to configure incremental training on computer vision models](how-to-auto-train-image-models.md#incremental-training-optional).
* See [what hyperparameters are available for computer vision tasks](reference-automl-images-hyperparameters.md).
* View code examples:

    # [Azure CLI](#tab/cli)
    [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
    
    * Review detailed code examples and use cases in the [azureml-examples repository for automated machine learning samples](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/automl-standalone-jobs). See the folders that have the *cli-automl-image-* prefix for samples that are specific to creating computer vision models.
    
    # [Python SDK](#tab/python)
    [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

    * Review detailed code examples and use cases in the [GitHub notebook repository for automated machine learning samples](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs). See the folders that have the *automl-image-* prefix for samples that are specific to creating computer vision models.
    
    ---

> [!NOTE]
> Use of the fridge objects dataset is available through the license under the [MIT License](https://github.com/microsoft/computervision-recipes/blob/master/LICENSE).
