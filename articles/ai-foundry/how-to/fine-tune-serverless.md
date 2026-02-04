---
title: Deploy Fine-Tuned Models with Serverless API in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Deploy fine-tuned models using serverless API in Microsoft Foundry. Learn how to fine-tune, train, and deploy custom large language models with cost-effective serverless options.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 01/28/2026
ms.reviewer: rasavage
reviewer: RSavage2
ms.author: ssalgado
manager: nitinme
author: ssalgadodev
ms.custom: references_regions
zone_pivot_groups: azure-ai-model-fine-tune
ai-usage: ai-assisted
---

# Fine-tune models by using serverless API deployments in Microsoft Foundry

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

Learn how to deploy fine-tuned models by using serverless API deployments in Microsoft Foundry. This comprehensive guide shows you how to fine-tune large language models (LLMs) to your specific datasets and deploy them with serverless infrastructure, offering improved performance, cost efficiency, reduced latency, and tailored outputs.

**Cost efficiency**: Foundry's fine-tuning can be more cost-effective, especially for large-scale deployments, thanks to pay-as-you-go pricing.

**Model variety**: Foundry's serverless API deployment fine-tuning offers support for both proprietary and open-source models, providing users with the flexibility to select the models that best suit their needs without being restricted to a single type.

**Customization and control**: Foundry provides greater customization and control over the fine-tuning process, which allows users to tailor models more precisely to their specific requirements.

This article explains how to fine-tune models that are deployed using serverless API deployments in [Foundry](https://ai.azure.com/?cid=learnDocs).

## Prerequisites

- A [Foundry project](create-projects.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Foundry portal. To perform the steps in this article, your user account must be assigned the __Owner__ or __Contributor__ role for the Azure subscription. For more information on permissions, see [role-based access control in Foundry portal](../concepts/rbac-foundry.md).

## Verify registration of subscription provider

Verify that your subscription is registered to the *Microsoft.Network* resource provider.

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Select the subscription you want to use.
1. Under **Settings** in the sidebar menu, select **Resource providers**.
1. Select **Microsoft.Network** and choose **Register** if it's not registered.

::: zone pivot="foundry-portal"

## Find models with fine-tuning support

The Foundry model catalog offers fine-tuning support for multiple types of models, including chat completions and text generation. For a list of models and regions that support fine-tuning, see [region availability for models in serverless APIs](deploy-models-serverless-availability.md).

Fine-tuning tasks are available only to users whose Azure subscription belongs to a billing account in a region where the model provider makes the offer available. If the offer is available in the relevant region, the user then must have a project resource in the Azure region where the model is available for deployment or fine-tuning, as applicable.

Go to the Foundry portal to view all models that contain fine-tuning support:

1. [!INCLUDE [classic-sign-in](../includes/classic-sign-in.md)]

1. If you're not already in your project, select it. 

1. Navigate to the model catalog.

1. Select the **Fine-tuning tasks** filter. 

    :::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-filters.png" alt-text="Screenshot of model catalog fine-tuning filter options." lightbox="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-filters.png":::

1. Select **All** or select a specific task.

## Prepare data for fine-tuning

Prepare your training and validation data to fine-tune your model. Your training and validation data consist of input and output examples for how you would like the model to perform.

Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a diverse dataset by maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations. These actions ultimately lead to more accurate and balanced model responses.

> [!TIP]
> Different model types require training data in different formats.

# [Chat completion](#tab/chat-completion)

### Example file format

The supported file type is JSON Lines (JSONL). Files are uploaded to the default datastore and made available in your project.

```json
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Is Xbox better than PlayStation?"}, {"role": "assistant", "content": "I apologize, but I cannot provide personal opinions. My primary job is to assist you with any issues related to your Xbox device. Do you have any Xbox-related issues that need addressing?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Can I play PC games on my Xbox?"}, {"role": "assistant", "content": "While Xbox consoles don't natively support PC games, they can play an array of Xbox games, many of which are also available on PC. Can I assist you with finding games compatible with your Xbox device?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "I'm having trouble connecting my Xbox to the Wi-Fi."}, {"role": "assistant", "content": "No worries, let's go through the network settings on your Xbox. Can you please tell me what happens when you try to connect it to the Wi-Fi?"}]}
```

# [Text generation](#tab/text-generation)

The training and validation data you use *must* be formatted as a JSON Lines (JSONL) document in which each line represents a single prompt-completion pair.

### Example file format

```json
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
```

Here are some example datasets on Hugging Face to use to fine-tune your model:

- [dair-ai/emotion](https://huggingface.co/datasets/dair-ai/emotion)

    :::image type="content" source="../media/how-to/fine-tune/dataset-dair-ai-emotion.png" alt-text="Screenshot of example emotion data on Hugging Face." lightbox="../media/how-to/fine-tune/dataset-dair-ai-emotion.png":::

- [SetFit/mrpc](https://huggingface.co/datasets/SetFit/mrpc)

    :::image type="content" source="../media/how-to/fine-tune/dataset-setfit-mrpc.png" alt-text="Screenshot of example Microsoft Research Paraphrase Corpus (MRPC) data on Hugging Face." lightbox="../media/how-to/fine-tune/dataset-setfit-mrpc.png":::

*Single text classification* requires the training data to include at least two fields such as `text1` and `label`. *Text pair classification* requires the training data to include at least three fields such as `text1`, `text2`, and `label`. 

The supported file type is JSON Lines. Files are uploaded to the default datastore and made available in your project.

---

## Use the fine-tune model wizard

Foundry portal provides a custom model wizard, to interactively create and train a fine-tuned model for your Azure resource.

### Select the base model

1. Select **Fine-tuning** from the sidebar menu, then choose **+ Fine-tune model**.
1. Select the model you want to fine-tune from the list under **Base models**, then select **Next**.

### Choose your training data

The next step is to either choose existing prepared training data or upload new prepared training data to use when customizing your model. The **Training data** pane displays any existing, previously uploaded datasets and also provides options to upload new training data.

Select **+ Add training data**.

- If your training data is already uploaded to the service, select **Existing files on this resource**.
    - Select the file from the dropdown list shown.
- To upload new training data, use one of the following options:
    - Select **Upload files** to upload training data from a local file.
    - Select **Azure blob or other shared web locations** to import training data from Azure Blob or another shared web location.
- To use a ready-to-go dataset for quick fine-tuning, choose from the list under **Select data**.

For large data files, we recommend that you import from an Azure Blob store. For more information about Azure Blob Storage, see [What is Azure Blob Storage?](/azure/storage/blobs/storage-blobs-overview)

### Choose your validation data

The next step provides options to configure the model to use validation data in the training process. If you don't want to use validation data, choose **Submit** to continue to the advanced options for the model. Otherwise, if you have a validation dataset, either choose existing prepared validation data or upload new prepared validation data to use when customizing your model.

Select **+ Add validation data**. The **Validation data** pane displays any existing, previously uploaded training and validation datasets and provides options by which you can upload new validation data.

- If your validation data is already uploaded to the service, select **Existing files on this resource**.
    - Select the file from the list shown in the **Validation data** pane.
- To upload new validation data, use one of the following options:
    - Select **Upload files** to upload validation data from a local file.
    - Select **Azure blob or other shared web locations** to import validation data from Azure Blob or another shared web location.

For large data files, we recommend that you import from an Azure Blob store. Large files can become unstable when uploaded through multipart forms because the requests are atomic and can't be retried or resumed.

> [!Note]
>- Similar to training data files, validation data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be smaller than 512 MB.

### Configure task parameters

The **Fine-tune model** wizard shows the parameters for training your fine-tuned model on the **Task parameters** pane. The following parameters are available:

|**Name**| **Type**| **Description**|
|---|---|---|
| **Batch size (1-32)** |integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, larger batch sizes tend to work better for larger datasets. The default value and the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. |
| **Learning rate multiplier (0.0-10.0)** | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pretraining multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. A smaller learning rate might be useful to avoid overfitting. |
| **Number of epochs (1-10)** | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. |

Select **Default** to use the default values for the fine-tuning job, or select **Custom** to display and edit the hyperparameter values. When defaults are selected, we determine the correct value algorithmically based on your training data.

After you configure the advanced options, select **Submit**.

### Check the status of your custom model

The **Fine-tuning tab** displays information about your custom model. The tab includes information about the status and job ID of the fine-tuned job for your custom model. When the job completes, the tab displays the file ID of the result file. You might need to select **Refresh** in order to see an updated status for the model training job.

:::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/project-running.png" alt-text="Screenshot of the running projects dashboard." lightbox="../media/how-to/fine-tune/fine-tune-serverless/project-running.png":::

After you start a fine-tuning job, it can take some time to complete. Your job might be queued behind other jobs on the system. Training your model can take minutes or hours depending on the model and dataset size.
Here are some of the tasks to do on the **Models** tab:

- Check the status of the fine-tuning job for your custom model in the **Status** column of the **Customized models** tab.
- In the model name column, select the model’s name to view more information about the custom model. You can see the status of the fine-tuning job, training results, training events, and hyperparameters used in the job.
- Select **Refresh** to update the information on the page.

:::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-details.png" alt-text="Screenshot of the fine-tuning details dashboard." lightbox="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-details.png":::

### Supported enterprise scenarios for fine-tuning

Several enterprise scenarios are supported for serverless API deployment fine-tuning. The following table outlines the supported configurations for user storage networking and authentication to ensure smooth operation within enterprise scenarios:

>[!Note]  
>- Data connections authentication can be changed via Foundry by selecting the datastore connection where your dataset is stored, and navigating to the **Access details** > **Authentication Method** setting.
>- Storage authentication can be changed in Azure Storage > **Settings** > **Configurations** page > **Allow storage account key access**.  
>- Storage networking can be changed in Azure Storage > **Networking** page.

| **Storage networking** | **Storage auth** | **Data connection auth** | **Support** |
|--|--|--|--|
| Public network access = Enabled | Account key enabled | SAS/Account key | Yes, UX and SDK |
| Public network access = Enabled | Account key disabled | Entra-based auth (credentialless) | Yes, UX and SDK <br><br> *Note:* for UX, you might need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use Account key/SAS token | 
| Enabled from selected virtual networks and IP addresses | Account key enabled | Account key | Yes, UX and SDK <br><br> *Note:* for UX, the IP of the compute running the browser must be in the selected list |
| Enabled from selected virtual networks and IP addresses | Account key enabled | SAS | Yes, UX and SDK  <br><br> *Note:* for UX, the IP of the compute running the browser must be in the selected list |
| Enabled from selected virtual networks and IP addresses | Account key disabled | Entra-based auth (credentialless) | Yes, UX and SDK. <br><br>*Note:* for UX, you might need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use account key/SAS token. Also ensure the IP of the compute running the browser must be in the selected list |
| Public network access = Disabled | Account key enabled | SAS/Account key | Yes, UX and SDK. <br><br> *Note:*  for UX data upload and submission to work, the workspace _needs to be accessed from within the virtual network_ that has appropriate access to the storage |
| Public network access = Disabled | Account key disabled | Entra-based auth (credentialless) | Yes, UX and SDK. <br><br> *Note:* for UX data upload and submission to work, the workspace _needs to be accessed from within the virtual network_ that has appropriate access to the storage |

The preceding scenarios should work in a managed virtual network workspace as well. To learn how to set up managed virtual network Foundry hub, see [How to configure a managed network for Foundry hubs](./configure-managed-network.md).

Using customer-managed keys (CMKs) is *not* a supported enterprise scenario with serverless API deployment fine-tuning.

Issues fine-tuning with unique network setups on the workspace and storage usually point to a networking setup issue.

---

## Deploy a fine-tuned model

After the fine-tuning job succeeds, deploy the custom model from the **Fine-tuning** tab. You must deploy your custom model to make it available for use with completion calls.

> [!IMPORTANT]
> After you deploy a customized model and finish with the endpoint, remember to clean up any inactive endpoints. The deletion of an inactive deployment doesn't delete or affect the underlying customized model, and the customized model can be redeployed at any time. As described in Foundry pricing, each customized (fine-tuned) model that's deployed incurs an hourly hosting cost regardless of whether completions or chat completions calls are being made to the model.
>
> To learn more about planning and managing costs with Foundry, refer to the guidance in [Plan and manage costs for Foundry Service](./costs-plan-manage.md).

> [!NOTE]
> Only one deployment is permitted for a custom model. An error message is displayed if you select an already-deployed custom model.
> To deploy your custom model, select the custom model to deploy, and then select Deploy model.

The **Deploy model** dialog box opens. In the dialog box, enter your **Deployment name** and then select **Deploy** to start the deployment of your custom model.

You can also deploy a fine-tuned model through the **Models + endpoints** tab by selecting the **Deploy model** button and then selecting **Deploy Fine-tuned model** from the dropdown

:::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/manage-deployments.png" alt-text="Screenshot of the fine-tuning manage deployments dashboard." lightbox="../media/how-to/fine-tune/fine-tune-serverless/manage-deployments.png":::

Next, select the fine-tuned model you wish to deploy and select **Deploy**.

### Cross region deployment

Fine-tuning supports deploying a fine-tuned model to a different region than where the model was originally fine-tuned. You can also deploy to a different subscription or region.

The only limitations are that the new region must also support fine-tuning, and when deploying cross subscription, the account generating the authorization token for the deployment must have access to both the source and destination subscriptions.

Cross subscription or region deployment can be accomplished via [Python](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat_completion_with_model_as_service.ipynb).

### Use a deployed custom model

After your custom model deploys, you can use it like any other deployed model. You can use the **Playgrounds** in [Foundry portal](https://ai.azure.com/?cid=learnDocs) to experiment with your new deployment. You can continue to use the same parameters with your custom model, such as temperature and max_tokens, as you can with other deployed models.

### Clean up your fine-tuned models 

You can delete a fine-tuned model from the fine-tuning model list in [Foundry](https://ai.azure.com/?cid=learnDocs) or from the model details page. To delete the fine-tuned model from the Fine-tuning page,

1. Select __Fine-tuning__ from the sidebar menu in your Foundry project.
1. Select the __Delete__ button to delete the fine-tuned model.

>[!NOTE]
> You can't delete a custom model if it has an existing deployment. You must first delete your model deployment before you delete your custom model.

::: zone-end

::: zone pivot="programming-language-python"

### Create a client to consume the model

The following sections walk you through how to fine-tune a model in python. To find a notebook example of this code, see [Fine-tuning LLM with model as a service](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat_completion_with_model_as_service.ipynb).

1. Install dependencies to start fine-tuning your model. 

```python
%pip install azure-ai-ml
%pip install azure-identity

%pip install mlflow
%pip install azureml-mlflow
```

1. Create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables. Replace *<SUBSCRIPTION_ID>*, *<RESOURCE_GROUP_NAME>*, and *<WORKSPACE_NAME>* with your own values.

```python
from azure.ai.ml import MLClient
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)

try:
    credential = DefaultAzureCredential()
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    credential = InteractiveBrowserCredential()

try:
    workspace_ml_client = MLClient.from_config(credential=credential)
except:
    workspace_ml_client = MLClient(
        credential,
        subscription_id="<SUBSCRIPTION_ID>",
        resource_group_name="<RESOURCE_GROUP_NAME>",
        workspace_name="<PROJECT_NAME OR WORKSPACE_NAME>",
    )

# The models, fine tuning pipelines and environments are available in various AzureML system registries,
# Example: Phi family of models are in "azureml", Llama family of models are in "azureml-meta" registry.
registry_ml_client = MLClient(credential, registry_name="azureml")

# Get AzureML workspace object.
workspace = workspace_ml_client._workspaces.get(workspace_ml_client.workspace_name)
workspace.id
```

### Find models with fine-tuning support

The Foundry model catalog offers fine-tuning support for multiple types of models, including chat completions and text generation. For a list of models and regions that support fine-tuning, see [Region availability for models in serverless APIs](deploy-models-serverless-availability.md).

Fine-tuning tasks are available only to users whose Azure subscription belongs to a billing account in a region where the model provider makes the offer available. If the offer is available in the relevant region, the user then must have a project resource in the Azure region where the model is available for deployment or fine-tuning, as applicable.

This example uses a *Phi-4-mini-instruct* model. In this code snippet, the model ID property of the model is passed as input to the fine tuning job. This is also available as the **Asset ID** field in model details page in the Foundry model catalog.

```python
model_name = "Phi-4-mini-instruct"
model_to_finetune = registry_ml_client.models.get(model_name, label="latest")
print(
    "\n\nUsing model name: {0}, version: {1}, id: {2} for fine tuning".format(
        model_to_finetune.name, model_to_finetune.version, model_to_finetune.id
    )
)
```

### Prepare data for fine-tuning

Prepare your training and validation data to fine-tune your model. Your training and validation data consist of input and output examples for how you would like the model to perform.

Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a diverse dataset by maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations. These actions ultimately lead to more accurate and balanced model responses.

> [!TIP]
> Different model types require a different format of training data.

# [Chat completion](#tab/chat-completion)

#### Example file format

The supported file type is JSON Lines (JSONL). Files are uploaded to the default datastore and made available in your project.

```json
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Is Xbox better than PlayStation?"}, {"role": "assistant", "content": "I apologize, but I cannot provide personal opinions. My primary job is to assist you with any issues related to your Xbox device. Do you have any Xbox-related issues that need addressing?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Can I play PC games on my Xbox?"}, {"role": "assistant", "content": "While Xbox consoles don't natively support PC games, they can play an array of Xbox games, many of which are also available on PC. Can I assist you with finding games compatible with your Xbox device?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "I'm having trouble connecting my Xbox to the Wi-Fi."}, {"role": "assistant", "content": "No worries, let's go through the network settings on your Xbox. Can you please tell me what happens when you try to connect it to the Wi-Fi?"}]}
```

# [Text generation](#tab/text-generation)

The training and validation data you use *must* be formatted as a JSON Lines (JSONL) document in which each line represents a single prompt-completion pair.

#### Example file format

```json
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
```

Here are some example datasets on Hugging Face that you can use to fine-tune your model:

- [dair-ai/emotion](https://huggingface.co/datasets/dair-ai/emotion)

    :::image type="content" source="../media/how-to/fine-tune/dataset-dair-ai-emotion.png" alt-text="Screenshot of example emotion data on Hugging Face." lightbox="../media/how-to/fine-tune/dataset-dair-ai-emotion.png":::

- [SetFit/mrpc](https://huggingface.co/datasets/SetFit/mrpc)

    :::image type="content" source="../media/how-to/fine-tune/dataset-setfit-mrpc.png" alt-text="Screenshot of example Microsoft Research Paraphrase Corpus (MRPC) data on Hugging Face." lightbox="../media/how-to/fine-tune/dataset-setfit-mrpc.png":::

*Single text classification* requires the training data to include at least two fields such as `text1` and `label`. *Text pair classification* requires the training data to include at least three fields such as `text1`, `text2`, and `label`. 

The supported file type is JSON Lines. Files are uploaded to the default datastore and made available in your project.

---

### Create training data inputs

This code snippet shows you how to define a training dataset.

```python
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data

dataset_version = "1"
train_dataset_name = "chat_training_small"
try:
    train_data_asset = workspace_ml_client.data.get(
        train_dataset_name, version=dataset_version
    )
    print(f"Dataset {train_dataset_name} already exists")
except:
    print("creating dataset")
    train_data = Data(
        path=f"./train.jsonl",
        type=AssetTypes.URI_FILE,
        description="Training dataset",
        name=train_dataset_name,
        version="1",
    )
    train_data_asset = workspace_ml_client.data.create_or_update(train_data)
```

### Create validation data

The next step provides options to configure the model to use validation data in the training process. If you don't want to use validation data, you can skip this step and continue to the next section. Otherwise, if you have a validation dataset, you can either choose existing prepared validation data or upload new prepared validation data to use when customizing your model.

```python
from azure.ai.ml.entities import Data

dataset_version = "1"
validation_dataset_name = "chat_validation_small"
try:
    validation_data_asset = workspace_ml_client.data.get(
        validation_dataset_name, version=dataset_version
    )
    print(f"Dataset {validation_dataset_name} already exists")
except:
    print("creating dataset")
    validation_data = Data(
        path=f"./validation.jsonl",
        type=AssetTypes.URI_FILE,
        description="Validation dataset",
        name=validation_dataset_name,
        version="1",
    )
    validation_data_asset = workspace_ml_client.data.create_or_update(validation_data)
```

### Create marketplace subscription for partner models

This step is required for all non-Microsoft models. An example of a Microsoft model is the Phi family of models.

```python
model_id_to_subscribe = "/".join(model_to_finetune.id.split("/")[:-2])
print(model_id_to_subscribe)

normalized_model_name = model_name.replace(".", "-")
```

```python

from azure.ai.ml.entities import MarketplaceSubscription


subscription_name = f"{normalized_model_name}-sub"

marketplace_subscription = MarketplaceSubscription(
    model_id=model_id_to_subscribe,
    name=subscription_name,
)

# note: this will throw exception if the subscription already exists or subscription is not required (for example, if the model is not in the marketplace like Phi family)
try:
    marketplace_subscription = (
        workspace_ml_client.marketplace_subscriptions.begin_create_or_update(
            marketplace_subscription
        ).result()
    )
except Exception as ex:
    print(ex)
```

### Submit the fine-tuning job using the model and data as inputs

The following set of parameters are required to fine-tune your model.

- `model`: Base model to fine-tune
- `training_data`: Training data for fine-tuning the base model
- `validation_data`: Validation data for fine-tuning the base model
- `task`: Fine-tuning task to perform, for example, CHAT_COMPLETION for chat-completion fine-tuning jobs
- `outputs`: Output registered model name

The following parameters are optional:

- `hyperparameters`: Parameters that control the fine-tuning behavior at run time
- `name`: Fine-tuning job name
- `experiment_name`: Experiment name for fine-tuning job
- `display_name`: Fine-tuning job display name

```python
from azure.ai.ml.finetuning import FineTuningTaskType, create_finetuning_job
import uuid

guid = uuid.uuid4()
short_guid = str(guid)[:8]
display_name = f"{model_name}-display-name-{short_guid}-from-sdk"
name = f"{model_name}t-{short_guid}-from-sdk"
output_model_name_prefix = f"{model_name}-{short_guid}-from-sdk-finetuned"
experiment_name = f"{model_name}-from-sdk"

finetuning_job = create_finetuning_job(
    task=FineTuningTaskType.CHAT_COMPLETION,
    training_data=train_data_asset.id,
    validation_data=validation_data_asset.id,
    hyperparameters={
        "per_device_train_batch_size": "1",
        "learning_rate": "0.00002",
        "num_train_epochs": "1",
    },
    model=model_to_finetune.id,
    display_name=display_name,
    name=name,
    experiment_name=experiment_name,
    tags={"foo_tag": "bar"},
    properties={"my_property": "my_value"},
    output_model_name_prefix=output_model_name_prefix,
```

```python
created_job = workspace_ml_client.jobs.create_or_update(finetuning_job)
workspace_ml_client.jobs.get(created_job.name)
```

```python

status = workspace_ml_client.jobs.get(created_job.name).status

import time

while True:
    status = workspace_ml_client.jobs.get(created_job.name).status
    print(f"Current job status: {status}")
    if status in ["Failed", "Completed", "Canceled"]:
        print("Job has finished with status: {0}".format(status))
        break
    else:
        print("Job is still running. Checking again in 30 seconds.")
        time.sleep(30)
```

```python
finetune_model_name = created_job.outputs["registered_model"]["name"]
finetune_model_name
```

### Deploy a fine-tuned model

After the fine-tuning job succeeds, you can deploy the custom model.

> [!IMPORTANT]
> After you deploy a customized model and finish with the endpoint, remember to clean up any inactive endpoints. The deletion of an inactive deployment doesn't delete or affect the underlying customized model, and the customized model can be redeployed at any time. As described in Foundry pricing, each customized (fine-tuned) model that's deployed incurs an hourly hosting cost regardless of whether completions or chat completions calls are being made to the model.
>
> To learn more about planning and managing costs with Foundry, refer to the guidance in [Plan and manage costs for Foundry hubs](./costs-plan-manage.md).  

```python
# Deploy the model as a serverless endpoint

endpoint_name = f"{normalized_model_name}-ft-{short_guid}"  # Name must be unique
model_id = f"azureml://locations/{workspace.location}/workspaces/{workspace._workspace_id}/models/{finetune_model_name}/versions/1"
```

### Supported enterprise scenarios for fine-tuning

Several enterprise scenarios are supported for serverless API deployment fine-tuning. The following table outlines the supported configurations for user storage networking and authentication to ensure smooth operation within enterprise scenarios:

>[!Note]  
>- Data connections authentication can be changed via Foundry by selecting the datastore connection where your dataset is stored, and navigating to the **Access details** > **Authentication Method** setting.
>- Storage authentication can be changed in Azure Storage > **Settings** > **Configurations** page > **Allow storage account key access**.  
>- Storage networking can be changed in Azure Storage > **Networking** page.

| **Storage networking**     |  **Storage auth**   | **Data connection auth**         | **Support**             |
| -------------------------- | ------------------- | -------------------------------- | ----------------------- |
| Public network access = Enabled  | Account key enabled  | SAS/Account Key    | Yes, UX and SDK         |
| Public network access = Enabled  | Account key disabled | Entra-based auth (credentialless) | Yes, UX and SDK <br><br> *Note:* for UX, you might need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use Account key/SAS token | 
| Enabled from selected virtual networks and IP addresses    | Account key enabled       | Account key   | Yes, UX and SDK <br><br> *Note:* for UX, the IP of the compute running the browser must be in the selected list        |
| Enabled from selected virtual networks and IP addresses    | Account key enabled       | SAS           | Yes, UX and SDK  <br><br> *Note:* for UX, the IP of the compute running the browser must be in the selected list       |
| Enabled from selected virtual networks and IP addresses    | Account key disabled      | Entra-based auth (credentialless) | Yes, UX and SDK. <br><br>*Note:* for UX, you might need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use Account key/SAS token. Also ensure the IP of the compute running the browser must be in the selected list |
| Public network access = Disabled    | Account key enabled  | SAS/Account key   | Yes, UX and SDK. <br><br> *Note:* for UX data upload and submission to work, the workspace _needs to be accessed from within the virtual network_ that has appropriate access to the storage  |
| Public network access = Disabled    | Account key disabled | Entra-based auth (credentialless) | Yes, UX and SDK. <br><br> *Note:* for UX data upload and submission to work, the workspace _needs to be accessed from within the virtual network_ that has appropriate access to the storage  |

The preceding scenarios should work in a managed virtual network workspace, as well. To learn how to set up managed virtual network Foundry hub, see [How to set up a managed network for Foundry hubs](./configure-managed-network.md).

Using customer-managed keys (CMKs) is *not* a supported enterprise scenario with serverless API deployment fine-tuning.

Issues fine-tuning with unique network setups on the workspace and storage usually point to a networking setup issue.

### Cross-region deployment

Fine-tuning supports deployment of a fine-tuned model to a different region than where the model was originally fine-tuned. You can also deploy to a different subscription or region.

The only limitations are that the new region must also support fine-tuning, and when deploying cross subscription, the account generating the authorization token for the deployment must have access to both the source and destination subscriptions.

Cross subscription or region deployment can be accomplished via [Python](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat_completion_with_model_as_service.ipynb).

```python

# Create Cross region FT deployment client
from azure.ai.ml.entities import ServerlessEndpoint
from azure.ai.ml import MLClient
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)

try:
    credential = DefaultAzureCredential()
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    credential = InteractiveBrowserCredential()
try:
    workspace_ml_client = MLClient.from_config(credential=credential)
except:
    workspace_ml_client = MLClient(
        credential,
        subscription_id="<TARGET_SUBSCRIPTION_ID>",
        resource_group_name="<TARGET_RESOURCE_GROUP_NAME>",
        workspace_name="<TARGET_PROJECT_NAME>",
    )

workspace = workspace_ml_client._workspaces.get(workspace_ml_client.workspace_name)
```

```python
workspace_region = workspace.location
model_to_finetune.tags
supported_regions = model_to_finetune.tags["maas-finetuning-deploy-regions"]
supported_regions
if workspace_region in supported_regions:
    print(f"Creating endpoint in the region:{workspace_region}")
    serverless_endpoint = ServerlessEndpoint(name=endpoint_name, model_id=model_id)
    created_endpoint = workspace_ml_client.serverless_endpoints.begin_create_or_update(
        serverless_endpoint
    ).result()
else:
    raise ValueError(
        f"For the model : {model_to_finetune}, the target region: {workspace_region} is not supported for deployment, the supported regions: {supported_regions}"
    )
```

### Use a deployed custom model

After your custom model deploys, you can use it like any other deployed model. You can continue to use the same parameters with your custom model, such as `temperature` and `max_tokens`, as you can with other deployed models.

```python
endpoint = workspace_ml_client.serverless_endpoints.get(endpoint_name)
endpoint_keys = workspace_ml_client.serverless_endpoints.get_keys(endpoint_name)
auth_key = endpoint_keys.primary_key
```

```python

import requests

url = f"{endpoint.scoring_uri}/v1/chat/completions"

payload = {
    "max_tokens": 1024,
    "messages": [
        {
            "content": "This script is great so far. Can you add more dialogue between Amanda and Thierry to build up their chemistry and connection?",
            "role": "user",
        }
    ],
}
headers = {"Content-Type": "application/json", "Authorization": f"{auth_key}"}

response = requests.post(url, json=payload, headers=headers)

response.json()
```

### Clean up your fine-tuned models 

After you finish with your model, run the following code to clean up your fine-tuned model. 

```python
workspace_ml_client.serverless_endpoints.begin_delete(endpoint_name).result()
```

::: zone-end

## Cost and quota considerations for models deployed as a serverless API deployment

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

#### Cost for Microsoft models

You can find the pricing information on the __Pricing and terms__ tab of the deployment wizard when deploying Microsoft models (such as Phi-3 models) as a serverless API deployment.

#### Cost for non-Microsoft models

Non-Microsoft models deployed as a serverless API deployment are offered through Azure Marketplace and integrated with Foundry for use. You can find Azure Marketplace pricing when deploying or fine-tuning these models.

Each time a project subscribes to a given offer from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through Azure Marketplace](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

:::image type="content" source="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png" alt-text="Screenshot showing different resources corresponding to different model offers and their associated meters." lightbox="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png":::

## Sample notebook

You can use this [sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat_completion_with_model_as_service.ipynb) to create a standalone fine-tuning job to enhance a model's ability to summarize dialogues between two people using the Samsum dataset.

The training data is the ultrachat_200k dataset, which is divided into four splits suitable for supervised fine-tuning (sft) and generation ranking (gen). The notebook employs the available Azure AI models for the chat-completion task (If you would like to use a different model than what's used in the notebook, you can replace the model name).

The notebook includes setting up prerequisites, selecting a model to fine-tune, creating training and validation datasets, configuring and submitting the fine-tuning job, and finally, creating a serverless deployment using the fine-tuned model for sample inference.

## Sample CLI

Additionally, you can use this [sample CLI](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat-completion-finetuning.yaml) to create a standalone fine-tuning job to enhance a model's ability to summarize dialogues between two people using a dataset. 

```yaml
type: finetuning

name: "Phi-3-mini-4k-instruct-with-amlcompute"
experiment_name: "Phi-3-mini-4k-instruct-finetuning-experiment"
display_name: "Phi-3-mini-4k-instruct-display-name"
task: chat_completion
model_provider: custom
model: 
  path: "azureml://registries/azureml/models/Phi-3-mini-4k-instruct/versions/14"
  type: mlflow_model
training_data: train.jsonl
validation_data:
  path: validation.jsonl
  type: uri_file
hyperparameters:
  num_train_epochs: "1"
  per_device_train_batch_size: "1"
  learning_rate: "0.00002"
properties:
  my_property: "my_value"
tags:
  foo_tag: "bar"
outputs:
  registered_model:
    name: "Phi-3-mini-4k-instruct-finetuned-model"
    type: mlflow_model 
```

The training data used is the same as demonstrated in the SDK notebook. The CLI employs the available Azure AI models for the chat-completion task. If you prefer to use a different model than the one in the CLI sample, you can update the arguments, such as `model path`, accordingly.

## Content filtering

Serverless API deployment models are protected by Azure AI Content Safety. When deployed to real-time endpoints, you can opt out of this capability.

With Azure AI Content Safety enabled, both the prompt and completion pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

To learn more about Azure AI Content Safety, see [Content filtering in Foundry portal](../concepts/content-filtering.md).

## Related content

- [What is Foundry?](../what-is-foundry.md)
- [Learn more about deploying Mistral models](../concepts/models-inference-examples.md)
- [Foundry frequently asked questions](../faq.yml)
