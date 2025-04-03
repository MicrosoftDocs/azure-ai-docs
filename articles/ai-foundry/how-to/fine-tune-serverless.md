---
title: Fine-tune models using serverless APIs in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to fine-tune models deployed via serverless APIs in Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/11/2025
ms.reviewer: rasavage
reviewer: RSavage2
ms.author: ssalgado
author: ssalgadodev
ms.custom: references_regions
---

# Fine-tune models using serverless APIs in Azure AI Foundry

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

Azure AI Foundry enables you to customize large language models to your specific datasets through a process called fine-tuning. This process offers significant benefits by allowing for customization and optimization tailored to specific tasks and applications. The advantages include improved performance, cost efficiency, reduced latency, and tailored outputs.

**Cost Efficiency**: Azure AI Foundry's fine-tuning can be more cost-effective, especially for large-scale deployments, thanks to pay-as-you-go pricing.

**Model Variety**: Azure AI Foundry's Serverless API finetuning  offers support for both proprietary and open-source models, providing users with the flexibility to select the models that best suit their needs without being restricted to a single type.

**Customization and Control**: Azure AI Foundry provides greater customization and control over the fine-tuning process, enabling users to tailor models more precisely to their specific requirements.

In this article, you will discover how to fine-tune models that are deployed using serverless API's in [Azure AI Foundry](https://ai.azure.com).


## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- Access to the [Azure portal](https://portal.azure.com).

- An [Azure AI Foundry project](create-projects.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-foundry.md).

## Verify registration of subscription provider
Verify the subscription is registered to the Microsoft.Network resource provider.
1.	Sign in to the [Azure portal](https://portal.azure.com).
1.	Select **Subscriptions** from the left menu.
1.	Select the subscription you want to use.
1.	Select **Settings** > **Resource providers** from the left menu.
1.	Add Microsoft.Network to the list of resource providers if it is not in the list.



## Find models with fine-tuning support

The AI Foundry model catalog offers fine-tuning support for multiple types of models, including chat completions and text generation. For a list of models that support fine-tuning and the Azure regions of support for fine-tuning, see [region availability for models in serverless API endpoints.](deploy-models-serverless-availability.md) Fine-tuning tasks are available only to users whose Azure subscription belongs to a billing account in a country/region where the model provider has made the offer available. If the offer is available in the relevant region, the user then must have a project resource in the Azure region where the model is available for deployment or fine-tuning, as applicable.


You can also go to the Azure AI Foundry portal to view all models that contain fine-tuning support:

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
1. If you're not already in your project, select it. 
1. Navigate to the model catalog.
1. Select the **Fine-tuning tasks** filter. 
    
    :::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-filters.png" alt-text="Screenshot of model catalog finetuning filter options." lightbox="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-filters.png":::

1. Select **All** or select a specific task.


## Prepare data for fine-tuning

Prepare your training and validation data to fine-tune your model. Your training and validation data consist of input and output examples for how you would like the model to perform.

Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a diverse dataset by maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations. These actions ultimately lead to more accurate and balanced model responses.

> [!TIP]
> Different model types require a different format of training data.

# [Chat completion](#tab/chat-completion)

### Example file format

The supported file type is JSON Lines. Files are uploaded to the default datastore and made available in your project.

```json
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Is Xbox better than PlayStation?"}, {"role": "assistant", "content": "I apologize, but I cannot provide personal opinions. My primary job is to assist you with any issues related to your Xbox device. Do you have any Xbox-related issues that need addressing?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Can I play PC games on my Xbox?"}, {"role": "assistant", "content": "While Xbox consoles don't natively support PC games, they can play an array of Xbox games, many of which are also available on PC. Can I assist you with finding games compatible with your Xbox device?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "I'm having trouble connecting my Xbox to the Wi-Fi."}, {"role": "assistant", "content": "No worries, let's go through the network settings on your Xbox. Can you please tell me what happens when you try to connect it to the Wi-Fi?"}]}
```

# [Text generation](#tab/text-generation)

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document in which each line represents a single prompt-completion pair.

### Example file format

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

Single text classification requires the training data to include at least two fields such as `text1` and `label`. Text pair classification requires the training data to include at least three fields such as `text1`, `text2`, and `label`. 

The supported file type is JSON Lines. Files are uploaded to the default datastore and made available in your project.

---

## Use the Fine-tune model wizard

Azure AI Foundry portal provides the Create custom model wizard, so you can interactively create and train a fine-tuned model for your Azure resource.

### Select the base model

1. Choose the model you want to fine-tune from the Azure AI Foundry [model catalog](https://ai.azure.com/explore/models).
2. On the model's **Details page**, select **fine-tune**. Some foundation models support both **Serverless API** and **Managed compute**, while others support one or the other.
3. If you're presented the options for **Serverless API** and [**Managed compute**](./fine-tune-managed-compute.md), select **Serverless API** for fine-tuning. This action opens up a wizard that shows information about **pay-as-you-go** fine-tuning for your model.

### Choose your training data
The next step is to either choose existing prepared training data or upload new prepared training data to use when customizing your model. The **Training data** pane displays any existing, previously uploaded datasets and also provides options to upload new training data.

- If your training data is already uploaded to the service, select **Files from Azure AI Foundry**.
    - Select the file from the dropdown list shown.
- To upload new training data, use one of the following options:
    - Select **Local file** to upload training data from a local file.
    - Select **Azure blob or other shared web locations** to import training data from Azure Blob or another shared web location.
      
For large data files, we recommend that you import from an Azure Blob store. For more information about Azure Blob Storage, see [What is Azure Blob Storage](/azure/storage/blobs/storage-blobs-overview)?

### Upload training data from local file

You can upload a new training dataset to the service from a local file by using one of the following methods:
- Drag and drop the file into the client area of the **Training data pane**, and then select **Upload file**.
- Select **Browse for a file** from the client area of the **Training data pane**, choose the file to upload from the **Open** dialog, and then select **Upload file**.
After you select and upload the training dataset, select **Next** to continue.

### Choose your validation data
The next step provides options to configure the model to use validation data in the training process. If you don't want to use validation data, you can choose **Next** to continue to the advanced options for the model. Otherwise, if you have a validation dataset, you can either choose existing prepared validation data or upload new prepared validation data to use when customizing your model.
The **Validation data** pane displays any existing, previously uploaded training and validation datasets and provides options by which you can upload new validation data.

### Split training data
You can automatically divide your training data to generate a validation dataset.
After you select Automatic split of training data, select **Next** to continue.

### Use existing data in Azure AI Foundry

-	If your validation data is already uploaded to the service, select **Choose dataset**.
    -	Select the file from the list shown in the **Validation data** pane.
-	To upload new validation data, use one of the following options:
    -	Select **Local file** to upload validation data from a local file.
    -	Select **Azure blob or other shared web locations** to import validation data from Azure Blob or another shared web location.
For large data files, we recommend that you import from an Azure Blob store. Large files can become unstable when uploaded through multipart forms because the requests are atomic and can't be retried or resumed.

> [!Note]  
>- Similar to training data files, validation data files must be formatted as JSONL files,   
>- encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size.  

### Upload validation data from local file

You can upload a new validation dataset to the service from a local file by using one of the following methods:
-	Drag and drop the file into the client area of the **Validation data** pane, and then select **Upload file**.
-	Select **Browse for a file** from the client area of the **Validation data** pane, choose the file to upload from the **Ope**n dialog, and then select **Upload file**.
After you select and upload the validation dataset, select **Next** to continue.

### Configure task parameters

The **Fine-tune model** wizard shows the parameters for training your fine-tuned model on the **Task parameters** pane. The following parameters are available:

|**Name**| **Type**| **Description**|
|---|---|---|
|`batch_size` |integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we've found that larger batch sizes tend to work better for larger datasets. The default value as well as the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. |
| `learning_rate_multiplier` | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. A smaller learning rate may be useful to avoid overfitting. |
|`n_epochs` | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. |

Select **Default** to use the default values for the fine-tuning job, or select **Custom** to display and edit the hyperparameter values. When defaults are selected, we determine the correct value algorithmically based on your training data.
After you configure the advanced options, select **Next** to [review your choices and train your fine-tuned model](#review-your-choices-and-train-your-model).

### Review your choices and train your model

The **Review** pane of the wizard displays information about your configuration choices.

If you're ready to train your model, select **Start Training job** to start the fine-tuning job and return to the **Models** Tab.


### Check the status of your custom model

The **Fine-tuning tab** displays information about your custom model. The tab includes information about the status and job ID of the fine-tune job for your custom model. When the job completes, the tab displays the file ID of the result file. You might need to select **Refresh** in order to see an updated status for the model training job.

:::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/project-running.png" alt-text="Screenshot of the running projects dashboard." lightbox="../media/how-to/fine-tune/fine-tune-serverless/project-running.png":::


After you start a fine-tuning job, it can take some time to complete. Your job might be queued behind other jobs on the system. Training your model can take minutes or hours depending on the model and dataset size.
Here are some of the tasks you can do on the **Models** tab:

-	Check the status of the fine-tuning job for your custom model in the Status column of the Customized models tab.
-	In the Model name column, select the model’s name to view more information about the custom model. You can see the status of the fine-tuning job, training results, training events, and hyperparameters used in the job.
-	Select **Refresh** to update the information on the page.

---

:::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-details.png" alt-text="Screenshot of the fine-tuning details dashboard." lightbox="../media/how-to/fine-tune/fine-tune-serverless/fine-tune-details.png":::


### Supported enterprise scenarios for finetuning

Several enterprise scenarios are supported for MaaS finetuning. The table below outlines the supported configurations for user storage networking and authentication to ensure smooth operation within enterprise scenarios:

>[!Note]  
>- Data connections auth can be changed via AI Foundry by clicking on the datastore connection which your dataset is stored in, and navigating to the **Access details** > **Authentication Method** setting.  
>- Storage auth can be changed in Azure Storage > **Settings** > **Configurations** page > **Allow storage account key access**.  
>- Storage networking can be changed in Azure Storage > **Networking** page.

| **Storage Networking**                                       |  **Storage Auth**               | **Data Connection Auth**         | **Support**             |
| ------------------------------------------------------------ | ------------------------------ | --------------------------------- | ----------------------- |
| Public Network Access = Enabled                               | Account key enabled            | SAS/Account Key                  | Yes, UX and SDK         |
| Public Network Access = Enabled                               | Account key disabled           | Entra-Based Auth (Credentialless) | Yes, UX and SDK <br><br> *Note:* for UX, you may need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use Account key/SAS token |                               |                                   |                         |
| Enabled from selected virtual networks and IP addresses      | Account key enabled            | Account key                      | Yes, UX and SDK <br><br> *Note:*: for UX, the IP of the compute running the browser must be in the selected list        |
| Enabled from selected virtual networks and IP addresses      | Account key enabled            | SAS                               | Yes, UX and SDK  <br><br> *Note:*: for UX, the IP of the compute running the browser must be in the selected list       |
| Enabled from selected virtual networks and IP addresses      | Account key disabled           | Entra-Based Auth (Credentialless) | Yes, UX and SDK. <br><br>*Note:* for UX, you may need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use Account key/SAS token. Also ensure the IP of the compute running the browser must be in the selected list |                               |                                   |                         |
| Public Network Access = Disabled                              | Account key enabled            | SAS/Account Key                  | Yes, UX and SDK. <br><br> *Note:*  for UX data upload and submission to work, the workspace _needs to be accessed from within the Vnet_ that has appropriate access to the storage           |
| Public Network Access = Disabled                              | Account key disabled           | Entra-Based Auth (Credentialless) | Yes, UX and SDK. <br><br> *Note:* for UX data upload and submission to work, the workspace _needs to be accessed from within the Vnet_ that has appropriate access to the storage                |


The scenarios above should work in a Managed Vnet workspace as well. See setup of Managed Vnet AI Foundry hub here: [How to configure a managed network for Azure AI Foundry hubs](./configure-managed-network.md)

Customer-Managed Keys (CMKs) is **not** a supported enterprise scenario with MaaS finetuning.

Issues finetuning with unique network setups on the workspace and storage usually points to a networking setup issue.

---

## Deploy a fine-tuned model
When the fine-tuning job succeeds, you can deploy the custom model from the **Fine-tune** tab. You must deploy your custom model to make it available for use with completion calls.

> [!IMPORTANT]
> After you deploy a customized model and finishing with the endpoint, please remember to clean up any inactive endpoints. The deletion of an inactive deployment doesn't
> delete or affect the underlying customized model, and the customized model can be redeployed at any time. As described in Azure AI Foundry pricing, each customized (fine-
> tuned) model that's deployed incurs an hourly hosting cost regardless of whether completions or chat completions calls are being made to the model. To learn more about
> planning and managing costs with Azure AI Foundry, refer to the guidance in [Plan to manage costs for Azure AI Foundry Service](./costs-plan-manage.md).  

> [!NOTE]
> Only one deployment is permitted for a custom model. An error message is displayed if you select an already-deployed custom model.
> To deploy your custom model, select the custom model to deploy, and then select Deploy model.


The **Deploy model** dialog box opens. In the dialog box, enter your **Deployment name** and then select **Deploy** to start the deployment of your custom model.


You can also deploy a finetuned model through the **Models + endpoints** tab by selecting the **Deploy model** button and then selecting **Deploy Fine-tuned model** from the dropdown

:::image type="content" source="../media/how-to/fine-tune/fine-tune-serverless/manage-deployments.png" alt-text="Screenshot of the fine-tuning manage deployments dashboard." lightbox="../media/how-to/fine-tune/fine-tune-serverless/manage-deployments.png":::

Next select the fine-tuned model you wish to deploy and select **Deploy**.

### Cross region deployment
Fine-tuning supports deploying a fine-tuned model to a different region than where the model was originally fine-tuned. You can also deploy to a different subscription/region.
The only limitations are that the new region must also support fine-tuning and when deploying cross subscription, the account generating the authorization token for the deployment must have access to both the source and destination subscriptions.
Cross subscription/region deployment can be accomplished via [Python](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat_completion_with_model_as_service.ipynb) 

### Use a deployed custom model
After your custom model deploys, you can use it like any other deployed model. You can use the **Playgrounds** in [Azure AI Foundry portal](https://portal.azure.com) to experiment with your new deployment. You can continue to use the same parameters with your custom model, such as temperature and max_tokens, as you can with other deployed models.

### Clean up your fine-tuned models 

You can delete a fine-tuned model from the fine-tuning model list in [Azure AI Foundry](https://ai.azure.com) or from the model details page. To delete the fine-tuned model from the Fine-tuning page,

1. Select __Fine-tuning__ from the left navigation in your Azure AI Foundry project.
1. Select the __Delete__ button to delete the fine-tuned model.

>[!NOTE]
> You can't delete a custom model if it has an existing deployment. You must first delete your model deployment before you delete your custom model.

## Cost and quota considerations for models deployed as serverless API endpoints

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

#### Cost for Microsoft models

You can find the pricing information on the __Pricing and terms__ tab of the deployment wizard when deploying Microsoft models (such as Phi-3 models) as serverless API endpoints.

#### Cost for non-Microsoft models

Non-Microsoft models deployed as serverless API endpoints are offered through Azure Marketplace and integrated with Azure AI Foundry for use. You can find Azure Marketplace pricing when deploying or fine-tuning these models.

Each time a project subscribes to a given offer from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through Azure Marketplace](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

:::image type="content" source="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png" alt-text="A screenshot showing different resources corresponding to different model offers and their associated meters." lightbox="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png":::

## Sample notebook

You can use this [sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat_completion_with_model_as_service.ipynb) to create a standalone fine-tuning job to enhance a model's ability to summarize dialogues between two people using the Samsum dataset. The training data utilized is the ultrachat_200k dataset, which is divided into four splits suitable for supervised fine-tuning (sft) and generation ranking (gen). The notebook employs the available Azure AI models for the chat-completion task (If you would like to use a different model than what's used in the notebook, you can replace the model name). The notebook includes setting up prerequisites, selecting a model to fine-tune, creating training and validation datasets, configuring and submitting the fine-tuning job, and finally, creating a serverless deployment using the fine-tuned model for sample inference.

## Sample CLI

Additionally, you can use this sample [CLI](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/finetuning/standalone/model-as-a-service/chat-completion/chat-completion-finetuning.yaml) to create a standalone fine-tuning job to enhance a model's ability to summarize dialogues between two people using a dataset. 

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

The training data used is the same as demonstrated in the SDK notebook. The CLI employs the available Azure AI models for the chat-completion task. If you prefer to use a different model than the one in the CLI sample, you can update the arguments, such as 'model path,' accordingly.

## Content filtering

Models deployed as a service with pay-as-you-go billing are protected by Azure AI Content Safety. When deployed to real-time endpoints, you can opt out of this capability. With Azure AI content safety enabled, both the prompt and completion pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions. Learn more about [Azure AI Content Safety](../concepts/content-filtering.md).


## Next steps
- [What is Azure AI Foundry?](../what-is-ai-foundry.md)
- [Learn more about deploying Mistral models](./deploy-models-mistral.md)
- [Azure AI FAQ article](../faq.yml)
