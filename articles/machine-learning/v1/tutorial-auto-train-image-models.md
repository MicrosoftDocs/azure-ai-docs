---
title: 'Tutorial: AutoML- train object detection model (v1)'
titleSuffix: Azure Machine Learning
description: Train an object detection model to identify if an image contains certain objects with automated ML and the Azure Machine Learning Python SDK  automated ML. (v1)
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: tutorial
author: swatig007
ms.author: scottpolly
ms.reviewer: sooryar
ms.date: 02/05/2026
ms.custom: UpdateFrequency5, devx-track-python, automl, sdkv1
---

# Tutorial: Train an object detection model (preview) with AutoML and Python (v1)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

>[!IMPORTANT]
> The features presented in this article are in preview. Consider them [experimental](/python/api/overview/azure/ml/#stable-vs-experimental) preview features that might change at any time.

In this tutorial, you learn how to train an object detection model by using Azure Machine Learning automated ML with the Azure Machine Learning Python SDK. This object detection model identifies whether the image contains objects, such as a can, carton, milk bottle, or water bottle.

Automated ML accepts training data and configuration settings. It automatically iterates through combinations of different feature normalization and standardization methods, models, and hyperparameter settings to find the best model.


You write code by using the Python SDK in this tutorial and learn the following tasks:

> [!div class="checklist"]
> * Download and transform data
> * Train an automated machine learning object detection model
> * Specify hyperparameter values for your model
> * Perform a hyperparameter sweep
> * Deploy your model
> * Visualize detections

## Prerequisites

* If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) of Azure Machine Learning today.

* Python 3.10 or later is supported for this feature.

* Complete the [Quickstart: Get started with Azure Machine Learning](../quickstart-create-resources.md#create-the-workspace) if you don't already have an Azure Machine Learning workspace.

* Download and unzip the [**odFridgeObjects.zip**](https://cvbp-secondary.z19.web.core.windows.net/datasets/object_detection/odFridgeObjects.zip) data file. The dataset is annotated in Pascal VOC format, where each image corresponds to an XML file. Each XML file contains information on where its corresponding image file is located and also contains information about the bounding boxes and the object labels. To use this data, you first need to convert it to the required JSONL format as seen in the [Convert the downloaded data to JSONL](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/image-object-detection/auto-ml-image-object-detection.ipynb) section of the notebook. 

This tutorial is also available in the [azureml-examples repository on GitHub](https://github.com/Azure/azureml-examples/tree/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/image-object-detection) if you wish to run it in your own [local environment](how-to-configure-environment.md). To get the required packages,
* Run `pip install azureml`
* [Install the full `automl` client](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/README.md#setup-using-a-local-conda-environment)

## Compute target setup

You first need to set up a compute target to use for your automated ML model training. Automated ML models for image tasks require GPU SKUs.

This tutorial uses the NCasT4_v3-series (with T4 GPUs) as this type of compute target leverages multiple GPUs to speed up training. Additionally, you can set up multiple nodes to take advantage of parallelism when tuning hyperparameters for your model.

The following code creates a GPU compute of size Standard_NC64as_T4_v3 with four nodes that are attached to the workspace, `ws`.

> [!WARNING]
> Ensure your subscription has sufficient quota for the compute target you want to use.

```python
from azureml.core.compute import AmlCompute, ComputeTarget

cluster_name = "gpu-nc64ast4v3"

try:
    compute_target = ComputeTarget(workspace=ws, name=cluster_name)
    print('Found existing compute target.')
except KeyError:
    print('Creating a new compute target...')
    compute_config = AmlCompute.provisioning_configuration(vm_size='Standard_NC64as_T4_v3',
                                                           idle_seconds_before_scaledown=1800,
                                                           min_nodes=0,
                                                           max_nodes=4)

    compute_target = ComputeTarget.create(ws, cluster_name, compute_config)

#If no min_node_count is provided, the scale settings are used for the cluster.
compute_target.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)
```

## Experiment setup
Next, create an `Experiment` in your workspace to track your model training runs.

```python

from azureml.core import Experiment

experiment_name = 'automl-image-object-detection'
experiment = Experiment(ws, name=experiment_name)
```

## Visualize input data

After preparing the input image data in [JSONL](https://jsonlines.org/) (JSON Lines) format, you can visualize the ground truth bounding boxes for an image. To do this visualization, make sure you have `matplotlib` installed.

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
            # Generate a random color. If you want to use a specific color, you can use something like "red".
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

def plot_ground_truth_boxes_dataset(image_file, dataset_pd):
    image_base_name = os.path.basename(image_file)
    image_pd = dataset_pd[dataset_pd['portable_path'].str.contains(image_base_name)]
    if not image_pd.empty:
        ground_truth_boxes = image_pd.iloc[0]["label"]
        plot_ground_truth_boxes(image_file, ground_truth_boxes)
    else:
        print("Unable to find ground truth information for image: {}".format(image_file))
```

By using the preceding helper functions, you can display the bounding boxes for any given image.

```python
image_file = "./odFridgeObjects/images/31.jpg"
jsonl_file = "./odFridgeObjects/train_annotations.jsonl"

plot_ground_truth_boxes_jsonl(image_file, jsonl_file)
```

## Upload data and create dataset

To use the data for training, upload it to your workspace through a datastore. The datastore provides a mechanism for you to upload or download data, and interact with it from your remote compute targets.

```python
ds = ws.get_default_datastore()
ds.upload(src_dir='./odFridgeObjects', target_path='odFridgeObjects')
```

After uploading the data to the datastore, create an Azure Machine Learning dataset from the data. Datasets package your data into a consumable object for training.

The following code creates a dataset for training. Since you didn't specify a validation dataset, the default behavior uses 20% of your training data for validation.

``` python
from azureml.core import Dataset
from azureml.data import DataType

training_dataset_name = 'odFridgeObjectsTrainingDataset'
if training_dataset_name in ws.datasets:
    training_dataset = ws.datasets.get(training_dataset_name)
    print('Found the training dataset', training_dataset_name)
else:
    # create training dataset
        # create training dataset
    training_dataset = Dataset.Tabular.from_json_lines_files(
        path=ds.path('odFridgeObjects/train_annotations.jsonl'),
        set_column_types={"image_url": DataType.to_stream(ds.workspace)},
    )
    training_dataset = training_dataset.register(workspace=ws, name=training_dataset_name)

print("Training dataset name: " + training_dataset.name)
```

### Visualize dataset

You can also visualize the ground truth bounding boxes for an image from this dataset.

Load the dataset into a pandas dataframe.

```python
import azureml.dataprep as dprep

from azureml.dataprep.api.functions import get_portable_path

# Get pandas dataframe from the dataset
dflow = training_dataset._dataflow.add_column(get_portable_path(dprep.col("image_url")),
                                              "portable_path", "image_url")
dataset_pd = dflow.to_pandas_dataframe(extended_types=True)
```

For any given image, run the following code to display the bounding boxes.

```python
image_file = "./odFridgeObjects/images/31.jpg"
plot_ground_truth_boxes_dataset(image_file, dataset_pd)
```

## Configure your object detection experiment

To configure automated ML runs for image-related tasks, use the `AutoMLImageConfig` object. In your `AutoMLImageConfig`, specify the model algorithms by using the `model_name` parameter. Configure the settings to perform a hyperparameter sweep over a defined parameter space to find the optimal model.

In this example, use the `AutoMLImageConfig` to train an object detection model with `yolov5` and `fasterrcnn_resnet50_fpn`, both of which are pretrained on COCO, a large-scale object detection, segmentation, and captioning dataset that contains over thousands of labeled images with over 80 label categories.

### Hyperparameter sweeping for image tasks

Perform a hyperparameter sweep over a defined parameter space to find the optimal model.

The following code defines the parameter space in preparation for the hyperparameter sweep for each defined algorithm, `yolov5` and `fasterrcnn_resnet50_fpn`. In the parameter space, specify the range of values for `learning_rate`, `optimizer`, `lr_scheduler`, and other parameters for AutoML to choose from as it attempts to generate a model with the optimal primary metric. If you don't specify hyperparameter values, default values are used for each algorithm.

For the tuning settings, use random sampling to pick samples from this parameter space by importing the `GridParameterSampling`, `RandomParameterSampling`, and `BayesianParameterSampling` classes. By using these classes, you tell automated ML to try a total of 20 iterations with these different samples, running four iterations at a time on your compute target, which you set up by using four nodes. The more parameters the space has, the more iterations you need to find optimal models.

Also use the Bandit early termination policy. This policy terminates poor performing configurations - those configurations that aren't within 20% slack of the best performing configuration - which significantly saves compute resources.

```python
from azureml.train.hyperdrive import RandomParameterSampling
from azureml.train.hyperdrive import BanditPolicy, HyperDriveConfig
from azureml.train.hyperdrive import choice, uniform

parameter_space = {
    'model': choice(
        {
            'model_name': choice('yolov5'),
            'learning_rate': uniform(0.0001, 0.01),
            #'model_size': choice('small', 'medium'), # model-specific
            'img_size': choice(640, 704, 768), # model-specific
        },
        {
            'model_name': choice('fasterrcnn_resnet50_fpn'),
            'learning_rate': uniform(0.0001, 0.001),
            #'warmup_cosine_lr_warmup_epochs': choice(0, 3),
            'optimizer': choice('sgd', 'adam', 'adamw'),
            'min_size': choice(600, 800), # model-specific
        }
    )
}

tuning_settings = {
    'iterations': 20,
    'max_concurrent_iterations': 4,
    'hyperparameter_sampling': RandomParameterSampling(parameter_space),
    'policy': BanditPolicy(evaluation_interval=2, slack_factor=0.2, delay_evaluation=6)
}
```

After you define the parameter space and tuning settings, pass them into your `AutoMLImageConfig` object. Then submit the experiment to train an image model by using your training dataset.

```python
from azureml.train.automl import AutoMLImageConfig
automl_image_config = AutoMLImageConfig(task='image-object-detection',
                                        compute_target=compute_target,
                                        training_data=training_dataset,
                                        validation_data=validation_dataset,
                                        primary_metric='mean_average_precision',
                                        **tuning_settings)

automl_image_run = experiment.submit(automl_image_config)
automl_image_run.wait_for_completion(wait_post_processing=True)
```

When you do a hyperparameter sweep, it can be useful to visualize the different configurations that you tried by using the HyperDrive UI. You can navigate to this UI by going to the **Child runs** tab in the UI of the main `automl_image_run` from above, which is the HyperDrive parent run. Then you can go into the **Child runs** tab of this one. Alternatively, the following section shows the HyperDrive parent run and you can navigate to its **Child runs** tab:

```python
from azureml.core import Run
hyperdrive_run = Run(experiment=experiment, run_id=automl_image_run.id + '_HD')
hyperdrive_run
```

## Register the best model

When the run completes, register the model that the best run creates.

```python
best_child_run = automl_image_run.get_best_child()
model_name = best_child_run.properties['model_name']
model = best_child_run.register_model(model_name = model_name, model_path='outputs/model.pt')
```

## Deploy model as a web service

After you train your model, deploy it to Azure. Deploy your trained model as a web service on Azure Container Instances (ACI) or Azure Kubernetes Service (AKS). ACI is the perfect option for testing deployments, while AKS is better suited for high-scale, production usage.

In this tutorial, you deploy the model as a web service in AKS.

1. Create an AKS compute cluster. In this example, use a GPU virtual machine SKU for the deployment cluster.

    ```python
    from azureml.core.compute import ComputeTarget, AksCompute
    from azureml.exceptions import ComputeTargetException

    # Choose a name for your cluster
    aks_name = "cluster-aks-gpu"

    # Check to see if the cluster already exists
    try:
        aks_target = ComputeTarget(workspace=ws, name=aks_name)
        print('Found existing compute target')
    except ComputeTargetException:
        print('Creating a new compute target...')
        # Provision AKS cluster with GPU machine
        prov_config = AksCompute.provisioning_configuration(vm_size="STANDARD_NC6",
                                                            location="eastus2")
        # Create the cluster
        aks_target = ComputeTarget.create(workspace=ws,
                                          name=aks_name,
                                          provisioning_configuration=prov_config)
        aks_target.wait_for_completion(show_output=True)
    ```

1. Define the inference configuration that describes how to set up the web-service containing your model. You can use the scoring script and the environment from the training run in your inference config.

    > [!NOTE]
    > To change the model's settings, open the downloaded scoring script and modify the `model_settings` variable before deploying the model.

    ```python
    from azureml.core.model import InferenceConfig

    best_child_run.download_file('outputs/scoring_file_v_1_0_0.py', output_file_path='score.py')
    environment = best_child_run.get_environment()
    inference_config = InferenceConfig(entry_script='score.py', environment=environment)
    ```

1. Deploy the model as an AKS web service.

    ```python

    from azureml.core.webservice import AksWebservice
    from azureml.core.webservice import Webservice
    from azureml.core.model import Model
    from azureml.core.environment import Environment

    aks_config = AksWebservice.deploy_configuration(autoscale_enabled=True,
                                                    cpu_cores=1,
                                                    memory_gb=50,
                                                    enable_app_insights=True)

    aks_service = Model.deploy(ws,
                               models=[model],
                               inference_config=inference_config,
                               deployment_config=aks_config,
                               deployment_target=aks_target,
                               name='automl-image-test',
                               overwrite=True)
    aks_service.wait_for_deployment(show_output=True)
    print(aks_service.state)
    ```

## Test the web service

Test the deployed web service to predict new images. For this tutorial, pass a random image from the dataset to the scoring URI.

```python
import requests

# URL for the web service
scoring_uri = aks_service.scoring_uri

# If the service is authenticated, set the key or token
key, _ = aks_service.get_keys()

sample_image = './test_image.jpg'

# Load image data
data = open(sample_image, 'rb').read()

# Set the content type
headers = {'Content-Type': 'application/octet-stream'}

# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Bearer {key}'

# Make the request and display the response
resp = requests.post(scoring_uri, data, headers=headers)
print(resp.text)
```
## Visualize detections
Now that you scored a test image, you can visualize the bounding boxes for this image. To do so, be sure you have matplotlib installed.

```
%pip install --upgrade matplotlib
```

```python
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import json

IMAGE_SIZE = (18,12)
plt.figure(figsize=IMAGE_SIZE)
img_np=mpimg.imread(sample_image)
img = Image.fromarray(img_np.astype('uint8'),'RGB')
x, y = img.size

fig,ax = plt.subplots(1, figsize=(15,15))
# Display the image
ax.imshow(img_np)

# draw box and label for each detection
detections = json.loads(resp.text)
for detect in detections['boxes']:
    label = detect['label']
    box = detect['box']
    conf_score = detect['score']
    if conf_score > 0.6:
        ymin, xmin, ymax, xmax =  box['topY'],box['topX'], box['bottomY'],box['bottomX']
        topleft_x, topleft_y = x * xmin, y * ymin
        width, height = x * (xmax - xmin), y * (ymax - ymin)
        print('{}: [{}, {}, {}, {}], {}'.format(detect['label'], round(topleft_x, 3),
                                                round(topleft_y, 3), round(width, 3),
                                                round(height, 3), round(conf_score, 3)))

        color = np.random.rand(3) #'red'
        rect = patches.Rectangle((topleft_x, topleft_y), width, height,
                                 linewidth=3, edgecolor=color,facecolor='none')

        ax.add_patch(rect)
        plt.text(topleft_x, topleft_y - 10, label, color=color, fontsize=20)

plt.show()
```

## Clean up resources

Don't complete this section if you plan on running other Azure Machine Learning tutorials.

If you don't plan to use the resources you created, delete them so you don't incur any charges.

1. In the Azure portal, select **Resource groups** on the far left.
1. From the list, select the resource group you created.
1. Select **Delete resource group**.
1. Enter the resource group name. Then select **Delete**.

You can also keep the resource group but delete a single workspace. Display the workspace properties and select **Delete**.

## Next steps

In this automated machine learning tutorial, you completed the following tasks:

> [!div class="checklist"]
> * Configured a workspace and prepared data for an experiment.
> * Trained an automated object detection model.
> * Specified hyperparameter values for your model.
> * Performed a hyperparameter sweep.
> * Deployed your model.
> * Visualized detections.

* [Learn more about computer vision in automated ML](../concept-automated-ml.md#computer-vision).
* [Learn how to set up AutoML to train computer vision models with Python](../how-to-auto-train-image-models.md).
* [Learn how to configure incremental training on computer vision models](../how-to-auto-train-image-models.md#incremental-training-optional).
* See [what hyperparameters are available for computer vision tasks](../reference-automl-images-hyperparameters.md).
* Review detailed code examples and use cases in the [GitHub notebook repository for automated machine learning samples](https://github.com/Azure/azureml-examples/tree/v1-archive/v1/python-sdk/tutorials/automl-with-azureml). Check the folders with the 'image-' prefix for samples specific to building computer vision models.

> [!NOTE]
> Use of the fridge objects dataset is available through the license under the [MIT License](https://github.com/microsoft/computervision-recipes/blob/master/LICENSE).
