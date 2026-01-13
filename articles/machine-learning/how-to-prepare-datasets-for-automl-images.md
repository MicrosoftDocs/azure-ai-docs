---
title: Prepare data for computer vision tasks
titleSuffix: Azure Machine Learning
description: Learn about image data preparation for Azure Machine Learning to train computer vision models on classification, object detection, and segmentation.
author: s-polly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: how-to
ms.reviewer: sooryar
ms.date: 09/06/2024
ms.custom:
  - template-how-to
  - update-code
  - sdkv2
  - sfi-image-nochange
#customer intent: As a data scientist, I want to prepare image data for training computer vision models.
---

# Prepare data for computer vision tasks with automated machine learning

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

> [!IMPORTANT]
> Support for training computer vision models with automated ML in Azure Machine Learning is an experimental public preview feature. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

In this article, you learn how to prepare image data for training computer vision models with [automated machine learning in Azure Machine Learning](concept-automated-ml.md). To generate models for computer vision tasks with automated machine learning, you need to bring labeled image data as input for model training in the form of an `MLTable`.

You can create an `MLTable` from labeled training data in JSONL format. If your labeled training data is in a different format, like Pascal Visual Object Classes (VOC) or COCO, you can use a [conversion script](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/image-object-detection/coco2jsonl.py) to convert it to JSONL, and then create an `MLTable`. Alternatively, you can use Azure Machine Learning's data labeling tool to manually label images. Then export the labeled data to use for training your AutoML model.

## Prerequisites

- Familiarize yourself with the accepted [schemas for JSONL files for AutoML computer vision experiments](reference-automl-images-schema.md).

## Get labeled data

In order to train computer vision models using AutoML, you need to get labeled training data. The images need to be uploaded to the cloud. Label annotations need to be in JSONL format. You can either use the Azure Machine Learning Data Labeling tool to label your data or you could start with prelabeled image data.

### Use Azure Machine Learning Data Labeling tool to label your training data

If you don't have prelabeled data, you can use Azure Machine Learning's data labeling tool to manually label images. This tool automatically generates the data required for training in the accepted format. For more information, see [Set up an image labeling project](how-to-create-image-labeling-projects.md).

The tool helps to create, manage, and monitor data labeling tasks for:

- Image classification (multi-class and multi-label)
- Object detection (bounding box)
- Instance segmentation (polygon)

If you already have labeled data to use, export that labeled data as an Azure Machine Learning Dataset and access the dataset under the **Datasets** tab in Azure Machine Learning studio. You can pass this exported dataset as an input using `azureml:<tabulardataset_name>:<version>` format. For more information, see [Export the labels](how-to-manage-labeling-projects.md#export-the-labels).

Here's an example of how to pass existing dataset as input for training computer vision models.

# [Azure CLI](#tab/cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```yaml
training_data:
  path: azureml:odFridgeObjectsTrainingDataset:1
  type: mltable
  mode: direct
```

# [Python SDK](#tab/python)

 [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml.constants import AssetTypes, InputOutputModes
from azure.ai.ml import Input

# Training MLTable with v1 TabularDataset
my_training_data_input = Input(
    type=AssetTypes.MLTABLE, path="azureml:odFridgeObjectsTrainingDataset:1",
    mode=InputOutputModes.DIRECT
)
```

# [Studio](#tab/Studio)

Refer to CLI/SDK tabs for reference.

---

### Use prelabeled training data from local machine

If you have labeled data that you want to use to train your model, upload the images to Azure. You can upload your images to the default Azure Blob Storage of your Azure Machine Learning Workspace. Register it as a *data asset*. For more information, see [Create and manage data assets](how-to-create-data-assets.md).

The following script uploads the image data on your local machine at path *./data/odFridgeObjects* to datastore in Azure Blob Storage. It then creates a new data asset with the name `fridge-items-images-object-detection` in your Azure Machine Learning Workspace.

If there already exists a data asset with the name `fridge-items-images-object-detection` in your Azure Machine Learning Workspace, the code updates the version number of the data asset and points it to the new location where the image data uploaded.

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

Create an *.yml* file with the following configuration.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/data.schema.json
name: fridge-items-images-object-detection
description: Fridge-items images Object detection
path: ./data/odFridgeObjects
type: uri_folder
```

To upload the images as a data asset, run the following CLI v2 command with the path to your *.yml* file, workspace name, resource group, and subscription ID.

```azurecli
az ml data create -f [PATH_TO_YML_FILE] --workspace-name [YOUR_AZURE_WORKSPACE] --resource-group [YOUR_AZURE_RESOURCE_GROUP] --subscription [YOUR_AZURE_SUBSCRIPTION]
```

# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb?name=upload-data)]

# [Studio](#tab/Studio)

:::image type="content" source="media\how-to-prepare-datasets-for-automl-images\ui-dataset-local.gif" alt-text="Animation showing how to register a dataset from local files.":::

---

If you already have your data in an existing datastore, you can create a data asset out of it. Provide the path to the data in the datastore instead of the path of your local machine. Update [the preceding code](#use-prelabeled-training-data-from-local-machine) with the following snippet.

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

Create a *.yml* file with the following configuration.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/data.schema.json
name: fridge-items-images-object-detection
description: Fridge-items images Object detection
path: azureml://subscriptions/<my-subscription-id>/resourcegroups/<my-resource-group>/workspaces/<my-workspace>/datastores/<my-datastore>/paths/<path_to_image_data_folder>
type: uri_folder
```

# [Python SDK](#tab/python)

```Python
my_data = Data(
    path="azureml://subscriptions/<my-subscription-id>/resourcegroups/<my-resource-group>/workspaces/<my-workspace>/datastores/<my-datastore>/paths/<path_to_image_data_folder>",
    type=AssetTypes.URI_FOLDER,
    description="Fridge-items images Object detection",
    name="fridge-items-images-object-detection",
)
```

# [Studio](#tab/Studio)

:::image type="content" source="media\how-to-prepare-datasets-for-automl-images\ui-dataset-datastore.gif" alt-text="Animation showing how to register a dataset from data already present in datastore.":::

---

Next, get the label annotations in JSONL format. The schema of labeled data depends on the computer vision task at hand. To learn more about the required JSONL schema for each task type, see [Data schemas to train computer vision models with automated machine learning](reference-automl-images-schema.md).

If your training data is in a different format, like pascal VOC or COCO, [helper scripts](https://github.com/Azure/azureml-examples/blob/v1-archive/v1/python-sdk/tutorials/automl-with-azureml/image-object-detection/coco2jsonl.py) can convert the data to JSONL. The scripts are available in [notebook examples](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs).

After you create the *.jsonl* file, you can register it as a data asset using the UI. Make sure that you select `stream` type in schema section as shown in this animation.

:::image type="content" source="media\how-to-prepare-datasets-for-automl-images\ui-dataset-jsnol.gif" alt-text="Animation showing how to register a data asset from the jsonl files.":::

### Use prelabeled training data from Azure Blob storage

If your labeled training data is present in a container in Azure Blob storage, you can access it directly. Create a datastore to that container. For more information, see [Create and manage data assets](how-to-datastore.md#create-an-azure-blob-datastore).

## Create MLTable

After your labeled data is in JSONL format, you can use it to create `MLTable` as shown in this yaml snippet. MLtable packages your data into a consumable object for training.

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

You can then pass in the `MLTable` as a data input for your AutoML training job. For more information, see [Set up AutoML to train computer vision models](./how-to-auto-train-image-models.md#consume-data).

## Related content

- [Set up AutoML to train computer vision models](how-to-auto-train-image-models.md).
- [Train a small object detection model with AutoML](how-to-use-automl-small-object-detect.md).
- [Tutorial: Train an object detection model with AutoML and Python](tutorial-auto-train-image-models.md).
