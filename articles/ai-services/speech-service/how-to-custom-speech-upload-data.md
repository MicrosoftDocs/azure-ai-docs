---
title: "Upload training and testing datasets for custom speech - Speech service"
titleSuffix: Foundry Tools
description: Learn about how to upload data to test or train a custom speech model.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/29/2025
ms.author: pafarley
zone_pivot_groups: foundry-speech-studio-cli-rest
#Customer intent: As a developer, I need to understand how to upload data to test or train a custom speech model so that I can improve the accuracy of speech recognition.
---

# Upload training and testing datasets for custom speech 

You need audio or text data for testing the accuracy of speech recognition or training your custom models. For information about the data types supported for testing or training your model, see [Training and testing datasets](how-to-custom-speech-test-and-train.md).

## Upload datasets

Follow these steps to upload datasets for training (fine-tuning) your custom speech model.

> [!IMPORTANT]
> Repeat the steps to upload testing datasets (such as **Audio** only) that you need [later when you create a test](./how-to-custom-speech-inspect-data.md). You can upload multiple datasets for training and testing.

::: zone pivot="ai-foundry-portal"

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the custom speech fine-tuning task (by model name) that you [started as described in the how to start custom speech fine-tuning article](./how-to-custom-speech-create-project.md).
1. Select **Manage data** > **Add dataset**. 

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-add-data.png" alt-text="Screenshot of the page with an option to add data to the custom speech project." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-add-data.png":::

1. In the **Add data** wizard, select the type of training data you want to add. In this example, select **Audio + human-labeled transcript**. Then select **Next**.

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-add-data-select-type.png" alt-text="Screenshot of the page with an option to select the type of training data you want to add." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-add-data-select-type.png":::

1. On the **Upload your data** page, select local files, Azure Blob Storage, or other shared web locations. Then select **Next**. 


    If you select a remote location and you don't use trusted Azure services security mechanism, the remote location should be a URL that can be retrieved by using a simple anonymous GET request. For example, a [SAS URL](/azure/storage/common/storage-sas-overview) or a publicly accessible URL. URLs that require extra authorization or expect user interaction aren't supported.

    > [!NOTE]
    > If you use Azure Blob URL, you can ensure maximum security of your dataset files by using trusted Azure services security mechanism. You use the same techniques as for batch transcription and plain Storage Account URLs for your dataset files. See details [here](batch-transcription-audio-data.md#trusted-azure-services-security-mechanism). 

1. Enter a name and description for the data. Then select **Next**.
1. Review the data and select **Upload**. You're taken back to the **Manage data** page. The status of the data is **Processing**.

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-add-data-status-processing.png" alt-text="Screenshot of the page that shows the status of the data as processing." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-add-data-status-processing.png":::

1. Repeat the steps to upload testing datasets (such as **Audio** only) that you need [later when you create a test](./how-to-custom-speech-inspect-data.md). You can upload multiple datasets for training and testing.

1. Repeat the previous steps to upload audio data [that you use later for testing](./how-to-custom-speech-inspect-data.md). In the **Add data** wizard, select **Audio** for the type of data you want to add. 

::: zone-end

::: zone pivot="speech-studio"

To upload your own datasets in Speech Studio, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech). 
1. Select **Custom speech** > Your project name > **Speech datasets** > **Upload data**.
1. Select the **Training data** or **Testing data** tab.
1. Select a dataset type, and then select **Next**.
1. Specify the dataset location, and then select **Next**. You can choose a local file or enter a remote location such as Azure Blob URL. If you select a remote location and you don't use trusted Azure services security mechanism, the remote location should be a URL that can be retrieved by using a simple anonymous GET request. For example, a [SAS URL](/azure/storage/common/storage-sas-overview) or a publicly accessible URL. URLs that require extra authorization or expect user interaction aren't supported.

    > [!NOTE]
    > If you use Azure Blob URL, you can ensure maximum security of your dataset files by using trusted Azure services security mechanism. You use the same techniques as for Batch transcription and plain Storage Account URLs for your dataset files. See details [here](batch-transcription-audio-data.md#trusted-azure-services-security-mechanism). 

1. Enter the dataset name and description, and then select **Next**.
1. Review your settings, and then select **Save and close**.

After your dataset is uploaded, go to the **Train custom models** page to [train a custom model](how-to-custom-speech-train-model.md).

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

[!INCLUDE [Map CLI and API kind to portal options](includes/how-to/custom-speech/cli-api-kind.md)]

To create a dataset and connect it to an existing project, use the `spx csr dataset create` command. Construct the request parameters according to the following instructions:

- Set the `project` property to the ID of an existing project. Use the `project` property so that you can also manage fine-tuning for custom speech in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.
- Set the required `kind` property. The possible set of values for a training dataset kind are: Acoustic, AudioFiles, Language, LanguageMarkdown, and Pronunciation.
- Set the required `contentUrl` property. This parameter is the location of the dataset. If you don't use trusted Azure services security mechanism (see next Note), then the `contentUrl` property should be a URL that can be retrieved with a simple anonymous GET request. For example, a [SAS URL](/azure/storage/common/storage-sas-overview) or a publicly accessible URL. URLs that require extra authorization, or expect user interaction aren't supported.

    > [!NOTE]
    > If you use Azure Blob URL, you can ensure maximum security of your dataset files by using trusted Azure services security mechanism. You use the same techniques as for Batch transcription and plain Storage Account URLs for your dataset files. See details [here](batch-transcription-audio-data.md#trusted-azure-services-security-mechanism).

- Set the required `language` property. The dataset locale must match the locale of the project. The locale can't be changed later. The Speech CLI `language` property corresponds to the `locale` property in the JSON request and response.
- Set the required `name` property. This parameter is the name that is displayed in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). The Speech CLI `name` property corresponds to the `displayName` property in the JSON request and response.

Here's an example Speech CLI command that creates a dataset and connects it to an existing project:

```azurecli-interactive
spx csr dataset create --api-version v3.2 --kind "Acoustic" --name "My Acoustic Dataset" --description "My Acoustic Dataset Description" --project YourProjectId --content YourContentUrl --language "en-US"
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API, but doesn't yet support versions later than `v3.2`.

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "kind": "Acoustic",
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/23b6554d-21f9-4df1-89cb-f84510ac8d23/files"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "properties": {
    "textNormalizationKind": "Default",
    "acceptedLineCount": 2,
    "rejectedLineCount": 0,
    "duration": "PT59S"
  },
  "lastActionDateTime": "2024-07-14T17:36:30Z",
  "status": "Succeeded",
  "createdDateTime": "2024-07-14T17:36:14Z",
  "locale": "en-US",
  "displayName": "My Acoustic Dataset",
  "description": "My Acoustic Dataset Description",
  "customProperties": {
    "PortalAPIVersion": "3"
  }
}
```

The top-level `self` property in the response body is the dataset's URI. Use this URI to get details about the dataset's project and files. You also use this URI to update or delete a dataset.

For Speech CLI help with datasets, run the following command:

```azurecli-interactive
spx help csr dataset
```

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [Map CLI and API kind to portal options](includes/how-to/custom-speech/cli-api-kind.md)]

To create a dataset and connect it to an existing project, use the [Datasets_Create](/rest/api/speechtotext/datasets/create) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the `project` property to the ID of an existing project. Use the `project` property so that you can also manage fine-tuning for custom speech in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.
- Set the required `kind` property. The possible set of values for a training dataset kind are: Acoustic, AudioFiles, Language, LanguageMarkdown, and Pronunciation. 
- Set the required `contentUrl` property. This property is the location of the dataset. If you don't use trusted Azure services security mechanism (see next Note), then the `contentUrl` property should be a URL that can be retrieved with a simple anonymous GET request. For example, a [SAS URL](/azure/storage/common/storage-sas-overview) or a publicly accessible URL. URLs that require extra authorization, or expect user interaction aren't supported. 

    > [!NOTE]
    > If you use Azure Blob URL, you can ensure maximum security of your dataset files by using trusted Azure services security mechanism. You use the same techniques as for Batch transcription and plain Storage Account URLs for your dataset files. See details [here](batch-transcription-audio-data.md#trusted-azure-services-security-mechanism). 

- Set the required `locale` property. The dataset locale must match the locale of the project. The locale can't be changed later. 
- Set the required `displayName` property. This property is the name that is displayed in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).

Make an HTTP POST request using the URI as shown in the following example. Replace `YourSpeechResoureKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "kind": "Acoustic",
  "displayName": "My Acoustic Dataset",
  "description": "My Acoustic Dataset Description",
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "contentUrl": "https://contoso.com/mydatasetlocation",
  "locale": "en-US",
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/datasets"
```

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "kind": "Acoustic",
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/23b6554d-21f9-4df1-89cb-f84510ac8d23/files"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "properties": {
    "textNormalizationKind": "Default",
    "acceptedLineCount": 2,
    "rejectedLineCount": 0,
    "duration": "PT59S"
  },
  "lastActionDateTime": "2024-07-14T17:36:30Z",
  "status": "Succeeded",
  "createdDateTime": "2024-07-14T17:36:14Z",
  "locale": "en-US",
  "displayName": "My Acoustic Dataset",
  "description": "My Acoustic Dataset Description",
  "customProperties": {
    "PortalAPIVersion": "3"
  }
}
```

The top-level `self` property in the response body is the dataset's URI. Use this URI to [get](/rest/api/speechtotext/datasets/get) details about the dataset's project and files. You also use this URI to [update](/rest/api/speechtotext/datasets/update) or [delete](/rest/api/speechtotext/datasets/delete) the dataset.

::: zone-end

> [!IMPORTANT] 
> You don't need to connect a dataset to a custom speech project to train and test a custom model by using the REST API or Speech CLI. However, if you don't connect the dataset to a project, you can't select it for training or testing in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). 

## Next steps

* [Test recognition quality](how-to-custom-speech-inspect-data.md)
* [Test model quantitatively](how-to-custom-speech-evaluate-data.md)
* [Train a custom model](how-to-custom-speech-train-model.md)
