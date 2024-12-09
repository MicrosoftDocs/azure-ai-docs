---
title: "Build and train a custom model - Document Intelligence "
titleSuffix: Azure AI services
description: Learn how to build, label, and train a custom model.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: how-to
ms.date: 08/07/2024
ms.author: lajanuar
monikerRange: '<=doc-intel-4.0.0'
---
<!-- markdownlint-disable DOCSMD006 -->

# Build and train a custom extraction model

:::moniker range=">=doc-intel-3.0.0"

[!INCLUDE [applies to v4.0 v3.1 v3.0](../includes/applies-to-v40-v31-v30.md)]   ![blue-checkmark](../media/blue-yes-icon.png) [v2.1](?view=doc-intel-2.1.0&preserve-view=true)

> [!IMPORTANT]
> Custom generative model training behavior is different from custom template and neural model training. The following document covers training only for custom template and neural models. For guidance on custom generative, refer to [custom generative model](../train/custom-generative-extraction.md)

Document Intelligence custom models require a handful of training documents to get started. If you have at least five documents, you can get started training a custom model. You can train either a [custom template model (custom form)](../train/custom-template.md) or a [custom neural model (custom document)](../train/custom-neural.md) or [custom template model (custom form)](../train/custom-generative-extraction.md). This document walks you through the process of training the custom models.

## Custom model input requirements

First, make sure your training data set follows the input requirements for Document Intelligence.

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Training data tips

Follow these tips to further optimize your data set for training:

* Use text-based PDF documents instead of image-based documents. Scanned PDFs are handled as images.
* Use examples that have all of the fields completed for forms with input fields.
* Use forms with different values in each field.
* Use a larger data set (10-15 images) if your form images are of lower quality.

## Upload your training data

Once you gather a set of forms or documents for training, you need to upload it to an Azure blob storage container. If you don't know how to create an Azure storage account with a container, following the [Azure Storage quickstart for Azure portal](/azure/storage/blobs/storage-quickstart-blobs-portal). You can use the free pricing tier (F0) to try the service, and upgrade later to a paid tier for production.

## Video: Train your custom model

* Once you gather and upload your training dataset, you're ready to train your custom model. In the following video, we create a project and explore some of the fundamentals for successfully labeling and training a model.

> [!VIDEO https://www.microsoft.com/en-us/videoplayer/embed/RE5fX1c]

## Create a project in the Document Intelligence Studio

The Document Intelligence Studio provides and orchestrates all the API calls required to complete your dataset and train your model.

1. Start by navigating to the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio). The first time you use the Studio, you need to [initialize your subscription, resource group, and resource](../quickstarts/try-document-intelligence-studio.md). Then, follow the [prerequisites for custom projects](../quickstarts/try-document-intelligence-studio.md#added-prerequisites-for-custom-projects) to configure the Studio to access your training dataset.

1. In the Studio, select the **Custom extraction model** tile and select the **Create a project** button.

    :::image type="content" source="../media/how-to/studio-custom-create-project.png" alt-text="Screenshot of Create a project in the Document Intelligence Studio.":::

    1. On the `create project` dialog, provide a name for your project, optionally a description, and select continue.

    1. On the next step in the workflow, choose or create a Document Intelligence resource before you select continue.

    > [!IMPORTANT]
    > Custom neural models are only available in a few regions. If you plan on training a neural model, please select or create a resource in one of [these supported regions](../train/custom-neural.md#supported-regions).

    :::image type="content" source="../media/how-to/studio-custom-configure-resource.png" alt-text="Screenshot of Select the Document Intelligence resource.":::

1. Next select the storage account you used to upload your custom model training dataset. The **Folder path** should be empty if your training documents are in the root of the container. If your documents are in a subfolder, enter the relative path from the container root in the **Folder path** field. Once your storage account is configured, select continue.

    :::image type="content" source="../media/how-to/studio-add-training-source.png" alt-text="Screenshot of Select the storage account.":::

1. Finally, review your project settings and select **Create Project** to create a new project. You should now be in the labeling window and see the files in your dataset listed.

## Label your data

In your project, your first task is to label your dataset with the fields you wish to extract.

The files you uploaded to storage are listed on the left of your screen, with the first file ready to be labeled.

1. Start labeling your dataset and creating your first field by selecting the plus (➕) button on the top-right of the screen.

    :::image type="content" source="../media/how-to/studio-add-field.png" alt-text="Screenshot of Create a label.":::

1. Enter a name for the field.

1. Assign a value to the field by choosing a word or words in the document. Select the field in either the dropdown or the field list on the right navigation bar. The labeled value is below the field name in the list of fields.

1. Repeat the process for all the fields you wish to label for your dataset.

1. Label the remaining documents in your dataset by selecting each document and selecting the text to be labeled.

You now have all the documents in your dataset labeled. The *.labels.json* and *.ocr.json* files correspond to each document in your training dataset and a new fields.json file. This training dataset is submitted to train the model.

## Train your model

With your dataset labeled, you're now ready to train your model. Select the train button in the upper-right corner.

1. On the train model dialog, provide a unique model ID and, optionally, a description. The model ID accepts a string data type.

1. For the build mode, select the type of model you want to train. Learn more about the [model types and capabilities](../train/custom-model.md).

    :::image type="content" source="../media/how-to/studio-train-model.png" alt-text="Screenshot of Train model dialog.":::

1. Select **Train** to initiate the training process.

1. Template models train in a few minutes. Neural models can take up to 30 minutes to train.

1. Navigate to the *Models* menu to view the status of the train operation.

## Test the model

Once the model training is complete, you can test your model by selecting the model on the models list page.

1. Select the model and select on the **Test** button.

1. Select the `+ Add` button to select a file to test the model.

1. With a file selected, choose the **Analyze** button to test the model.

1. The model results are displayed in the main window and the fields extracted are listed in the right navigation bar.

1. Validate your model by evaluating the results for each field.

1. The right navigation bar also has the sample code to invoke your model and the JSON results from the API.

Congratulations you learned to train a custom model in the Document Intelligence Studio! Your model is ready for use with the REST API or the SDK to analyze documents.

::: moniker-end

::: moniker range="doc-intel-2.1.0"

**Applies to:** ![Document Intelligence v2.1 checkmark](../media/yes-icon.png) **v2.1**. **Other versions:** [v3.0](../how-to-guides/build-a-custom-model.md?view=doc-intel-3.0.0&preserve-view=true?view=doc-intel-3.0.0&preserve-view=true)

When you use the Document Intelligence custom model, you provide your own training data to the [Train Custom Model](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true) operation, so that the model can train to your industry-specific forms. Follow this guide to learn how to collect and prepare data to train the model effectively.

You need at least five completed forms of the same type.

If you want to use manually labeled training data, you must start with at least five completed forms of the same type. You can still use unlabeled forms in addition to the required data set.

## Custom model input requirements

First, make sure your training data set follows the input requirements for Document Intelligence.

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Training data tips

Follow these tips to further optimize your data set for training.

* Use text-based PDF documents instead of image-based documents. Scanned PDFs are handled as images.
* Use examples that have all of their fields filled in for completed forms.
* Use forms with different values in each field.
* Use a larger data set (10-15 images) for completed forms.

## Upload your training data

Once you gather the set of documents for training, you need to upload it to an Azure blob storage container. If you don't know how to create an Azure storage account with a container, follow the [Azure Storage quickstart for Azure portal](/azure/storage/blobs/storage-quickstart-blobs-portal). Use the standard performance tier.

If you want to use manually labeled data, upload the *.labels.json* and *.ocr.json* files that correspond to your training documents. You can use the [Sample Labeling tool](../label-tool.md) (or your own UI) to generate these files.

### Organize your data in subfolders (optional)

By default, the [Train Custom Model](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true) API only uses documents that are located at the root of your storage container. However, you can train with data in subfolders if you specify it in the API call. Normally, the body of the [Train Custom Model](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true) call has the following format, where `<SAS URL>` is the Shared access signature URL of your container:

```json
{
  "source":"<SAS URL>"
}
```

If you add the following content to the request body, the API trains with documents located in subfolders. The `"prefix"` field is optional and limits the training data set to files whose paths begin with the given string. So a value of `"Test"`, for example, causes the API to look at only the files or folders that begin with the word *Test*.

```json
{
  "source": "<SAS URL>",
  "sourceFilter": {
    "prefix": "<prefix string>",
    "includeSubFolders": true
  },
  "useLabelFile": false
}
```

::: moniker-end

## Next steps

Now that you learned how to build a training data set, follow a quickstart to train a custom Document Intelligence model and start using it on your forms.

:::moniker range=">=doc-intel-3.0.0"

> [!div class="nextstepaction"]
> [Learn about custom model types](../train/custom-model.md)

> [!div class="nextstepaction"]
> [Learn about accuracy and confidence with custom models](../concept/accuracy-confidence.md)
:::moniker-end

:::moniker range="doc-intel-2.1.0"

  > [!div class="nextstepaction"]
  > [Train with labels using the Sample Labeling tool](../label-tool.md)
:::moniker-end

### See also

* [Train a model and extract document data using the client library or REST API](../quickstarts/get-started-sdks-rest-api.md)
* [Custom generative model](../train/custom-generative-extraction.md)
* [What is Document Intelligence?](../overview.md)
