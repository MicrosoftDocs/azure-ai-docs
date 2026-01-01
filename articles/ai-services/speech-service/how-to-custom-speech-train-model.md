---
title: Train a custom speech model - Speech service
titleSuffix: Foundry Tools
description: Learn how to train custom speech models. Training a speech to text model can improve recognition accuracy for the Microsoft base model or a custom model.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/19/2025
ms.author: pafarley
zone_pivot_groups: foundry-speech-studio-cli-rest
#Customer intent: As a developer, I want to train a custom speech model to improve recognition accuracy for the Microsoft base model or a custom model.
---

# Train a custom speech model

In this article, you learn how to train a custom model to improve recognition accuracy from the Microsoft base model. The speech recognition accuracy and quality of a custom speech model remains consistent, even when a new base model is released.

> [!NOTE]
> You pay for custom speech model usage and [endpoint hosting](how-to-custom-speech-deploy-model.md). You'll also be charged for custom speech model training if the base model was created on October 1, 2023 and later. You are not charged for training if the base model was created prior to October 2023. For more information, see  [Azure Speech in Foundry Tools pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/) and the [Charge for adaptation section in the speech to text 3.2 migration guide](./migrate-v3-1-to-v3-2.md#charge-for-adaptation).

Training a model is typically an iterative process. You first select a base model that is the starting point for a new model. You train a model with [datasets](./how-to-custom-speech-test-and-train.md) that can include text and audio, and then you test. If the recognition quality or accuracy doesn't meet your requirements, you can create a new model with more or modified training data, and then test again.

You can use a custom model for a limited time after it was trained. You must periodically recreate and adapt your custom model from the latest base model to take advantage of the improved accuracy and quality. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

> [!IMPORTANT]
> If you train a custom model with audio data, select a service resource in a region with dedicated hardware for training audio data. After a model is trained, you can [copy it to a Foundry resource for Speech](#copy-a-model) in another region as needed. 
> 
> In regions with dedicated hardware for custom speech training, the Speech service will use up to 100 hours of your audio training data, and can process about 10 hours of data per day. See footnotes in the [regions](regions.md#regions) table for more information.  

## Create a model

> [!TIP]
> Bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). In Microsoft Foundry portal, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-studio/ai-services/how-to/connect-ai-services.md#connect-azure-ai-services-after-you-create-a-project).

::: zone pivot="ai-foundry-portal"

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the custom speech fine-tuning task (by model name) that you [started as described in the how to start custom speech fine-tuning article](./how-to-custom-speech-create-project.md).
1. Select **Train model** > **+ Train model**. 

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-train-model.png" alt-text="Screenshot of the page with an option to start training for a custom speech model." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-train-model.png":::

1. In the **Train a new model** wizard, select the base model that you want to fine-tune. Then select **Next**.

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-train-model-select-base.png" alt-text="Screenshot of the page with an option to select the base model that you want to fine-tune." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-train-model-select-base.png":::

1. Select the data that you want to use for training. Then select **Next**.
1. Enter a name and description for the model. Then select **Next**.
1. Review the settings and select **Train a new model**. You're taken back to the **Train model** page. The status of the data is **Processing**.

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-train-model-status-processing.png" alt-text="Screenshot of the page that shows the status of the training as processing." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-train-model-status-processing.png":::

::: zone-end

::: zone pivot="speech-studio"

After you upload [training datasets](./how-to-custom-speech-test-and-train.md), follow these instructions to start training your model:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech). 
1. Select **Custom speech** > Your project name > **Train custom models**.
1. Select **Train a new model**.
1. On the **Select a baseline model** page, select a base model, and then select **Next**. If you aren't sure, select the most recent model from the top of the list. The name of the base model corresponds to the date when it was released in YYYYMMDD format. The customization capabilities of the base model are listed in parenthesis after the model name in Speech Studio. 

    > [!IMPORTANT]
    > Take note of the **Expiration for adaptation** date. This is the last date that you can use the base model for training. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

1. On the **Choose data** page, select one or more datasets that you want to use for training. If there aren't any datasets available, cancel the setup, and then go to the **Speech datasets** menu to [upload datasets](how-to-custom-speech-upload-data.md).
1. Enter a name and description for your custom model, and then select **Next**.
1. Optionally, check the **Add test in the next step** box. If you skip this step, you can run the same tests later. For more information, see [Test recognition quality](how-to-custom-speech-inspect-data.md) and [Test model quantitatively](how-to-custom-speech-evaluate-data.md).
1. Select **Save and close** to kick off the build for your custom model.
1. Return to the **Train custom models** page.

    > [!IMPORTANT]
    > Take note of the **Expiration** date. This is the last date that you can use your custom model for speech recognition. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To create a model with datasets for training, use the `spx csr model create` command. Construct the request parameters according to the following instructions:

- Set the `project` property to the ID of an existing project. The `project` property is recommended so that you can also manage fine-tuning for custom speech in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.
- Set the required `dataset` property to the ID of a dataset that you want used for training. To specify multiple datasets, set the `datasets` (plural) parameter and separate the IDs with a semicolon.
- Set the required `language` property. The dataset locale must match the locale of the project. The locale can't be changed later. The Speech CLI `language` property corresponds to the `locale` property in the JSON request and response.
- Set the required `name` property. This parameter is the name that is displayed in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). The Speech CLI `name` property corresponds to the `displayName` property in the JSON request and response.
- Optionally, you can set the `base` property. For example: `--base bbbbcccc-1111-dddd-2222-eeee3333ffff`. If you don't specify the `base`, the default base model for the locale is used. The Speech CLI `base` property corresponds to the `baseModel` property in the JSON request and response.

Here's an example Speech CLI command that creates a model with datasets for training:

```azurecli-interactive
spx csr model create --api-version v3.2 --project YourProjectId --name "My Model" --description "My Model Description" --dataset YourDatasetId --language "en-US"
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API, but doesn't yet support versions later than `v3.2`.

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "baseModel": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "datasets": [
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/ccccdddd-2222-eeee-3333-ffff4444aaaa"
    }
  ],
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd/manifest",
    "copy": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd:copy",
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd/files"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "properties": {
    "deprecationDates": {
      "transcriptionDateTime": "2026-07-15T00:00:00Z"
    },
    "customModelWeightPercent": 30,
    "features": {
      "supportsTranscriptions": true,
      "supportsEndpoints": true,
      "supportsTranscriptionsOnSpeechContainers": false,
      "supportedOutputFormats": [
        "Display",
        "Lexical"
      ]
    }
  },
  "lastActionDateTime": "2024-07-14T21:38:40Z",
  "status": "Running",
  "createdDateTime": "2024-07-14T21:38:40Z",
  "locale": "en-US",
  "displayName": "My Model",
  "description": "My Model Description"
}
```

> [!IMPORTANT]
> Take note of the date in the `adaptationDateTime` property. This is the last date that you can use the base model for training. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md). 
> 
> Take note of the date in the `transcriptionDateTime` property. This is the last date that you can use your custom model for speech recognition. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

The top-level `self` property in the response body is the model's URI. Use this URI to get details about the model's project, manifest, and deprecation dates. You also use this URI to update or delete a model.

For Speech CLI help with models, run the following command:

```azurecli-interactive
spx help csr model
```

::: zone-end

::: zone pivot="rest-api"

To create a model with datasets for training, use the [Models_Create](/rest/api/speechtotext/models/create) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the `project` property to the URI of an existing project. This property is recommended so that you can also view and manage the model in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.
- Set the required `datasets` property to the URI of the datasets that you want used for training.
- Set the required `locale` property. The model locale must match the locale of the project and base model. The locale can't be changed later.
- Set the required `displayName` property. This property is the name that is displayed in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
- Optionally, you can set the `baseModel` property. For example: `"baseModel": {"self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/bbbbcccc-1111-dddd-2222-eeee3333ffff"}`. If you don't specify the `baseModel`, the default base model for the locale is used. 

Make an HTTP POST request using the URI as shown in the following example. Replace `YourSpeechResoureKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "displayName": "My Model",
  "description": "My Model Description",
  "baseModel": null,
  "datasets": [
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/ccccdddd-2222-eeee-3333-ffff4444aaaa"
    }
  ],
  "locale": "en-US"
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/models"
```

> [!NOTE]
> In this example, the `baseModel` isn't set, so the default base model for the locale is used. The base model URI is returned in the response.

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "baseModel": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "datasets": [
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/ccccdddd-2222-eeee-3333-ffff4444aaaa"
    }
  ],
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd/manifest",
    "copy": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd:copy",
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd/files"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "properties": {
    "deprecationDates": {
      "transcriptionDateTime": "2026-07-15T00:00:00Z"
    },
    "customModelWeightPercent": 30,
    "features": {
      "supportsTranscriptions": true,
      "supportsEndpoints": true,
      "supportsTranscriptionsOnSpeechContainers": false,
      "supportedOutputFormats": [
        "Display",
        "Lexical"
      ]
    }
  },
  "lastActionDateTime": "2024-07-14T21:38:40Z",
  "status": "Running",
  "createdDateTime": "2024-07-14T21:38:40Z",
  "locale": "en-US",
  "displayName": "My Model",
  "description": "My Model Description"
}
```

> [!IMPORTANT]
> Take note of the date in the `adaptationDateTime` property. This is the last date that you can use the base model for training. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md). 
> 
> Take note of the date in the `transcriptionDateTime` property. This is the last date that you can use your custom model for speech recognition. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

The top-level `self` property in the response body is the model's URI. Use this URI to [get](/rest/api/speechtotext/models/get-custom-model) details about the model's project, manifest, and deprecation dates. You also use this URI to [update](/rest/api/speechtotext/models/update) or [delete](/rest/api/speechtotext/models/delete) the model.

::: zone-end


## Copy a model

You can copy a model to another project that uses the same locale. For example, after a model is trained with audio data in a [region](regions.md#regions) with dedicated hardware for training, you can copy it to a Foundry resource for Speech in another region as needed. 

::: zone pivot="ai-foundry-portal"



::: zone-end

::: zone pivot="speech-studio"

Follow these instructions to copy a model to a project in another region:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech). 
1. Select **Custom speech** > Your project name > **Train custom models**.
1. Select **Copy to**.
1. On the **Copy speech model** page, select a target region where you want to copy the model.
    :::image type="content" source="./media/custom-speech/custom-speech-copy-to-zoom.png" alt-text="Screenshot of a phrase list applied in Speech Studio." lightbox="./media/custom-speech/custom-speech-copy-to-full.png":::
1. Select a Foundry resource for Speech in the target region, or create a new Speech resource.
1. Select a project where you want to copy the model, or create a new project.
1. Select **Copy**. 

After the model is successfully copied, you'll be notified and can view it in the target project.

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

Copying a model directly to a project in another region isn't supported with the Speech CLI. You can copy a model to a project in another region using the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), [Speech Studio](https://aka.ms/speechstudio/customspeech), or [Speech to text REST API](rest-speech-to-text.md).

::: zone-end

::: zone pivot="rest-api"

To copy a model to another Speech resource, use the [Models_Copy](/rest/api/speechtotext/models/copy) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the required `targetSubscriptionKey` property to the key of the destination Speech resource.

Make an HTTP POST request using the URI as shown in the following example. Use the region and URI of the model you want to copy from. Replace `YourModelId` with the model ID, replace `YourSpeechResoureKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "targetSubscriptionKey": "ModelDestinationSpeechResourceKey"
} '  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/models/YourModelId:copy"
```

> [!NOTE]
> Only the `targetSubscriptionKey` property in the request body has information about the destination Speech resource.

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/eeeeffff-4444-aaaa-5555-bbbb6666cccc",
  "baseModel": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9df35ddb-edf9-4e91-8d1a-576d09aabdae/manifest",
    "copy": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9df35ddb-edf9-4e91-8d1a-576d09aabdae:copy"
  },
  "properties": {
    "deprecationDates": {
      "adaptationDateTime": "2023-01-15T00:00:00Z",
      "transcriptionDateTime": "2024-07-15T00:00:00Z"
    }
  },
  "lastActionDateTime": "2022-05-22T23:15:27Z",
  "status": "NotStarted",
  "createdDateTime": "2022-05-22T23:15:27Z",
  "locale": "en-US",
  "displayName": "My Model",
  "description": "My Model Description",
  "customProperties": {
    "PortalAPIVersion": "3",
    "Purpose": "",
    "VadKind": "None",
    "ModelClass": "None",
    "UsesHalide": "False",
    "IsDynamicGrammarSupported": "False"
  }
}
```

::: zone-end


## Connect a model

Models might have been copied from one project using the Speech CLI or REST API, without being connected to another project. Connecting a model is a matter of updating the model with a reference to the project.

::: zone pivot="ai-foundry-portal"



::: zone-end

::: zone pivot="speech-studio"

If you're prompted in Speech Studio, you can connect them by selecting the **Connect** button. 

:::image type="content" source="./media/custom-speech/custom-speech-connect-model.png" alt-text="Screenshot of the connect training page that shows models that can be connected to the current project.":::

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To connect a model to a project, use the `spx csr model update` command. Construct the request parameters according to the following instructions:

- Set the `project` property to the ID of an existing project. The `project` property is recommended so that you can also manage fine-tuning for custom speech in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.
- Set the required `modelId` property to the ID of the model that you want to connect to the project.

Here's an example Speech CLI command that connects a model to a project:

```azurecli-interactive
spx csr model update --api-version v3.2 --model YourModelId --project YourProjectId
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API, but doesn't yet support versions later than `v3.2`.

You should receive a response body in the following format:

```json
{
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
}
```

For Speech CLI help with models, run the following command:

```azurecli-interactive
spx help csr model
```

::: zone-end

::: zone pivot="rest-api"

To connect a new model to a project of the Speech resource where the model was copied, use the [Models_Update](/rest/api/speechtotext/models/update) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the required `project` property to the URI of an existing project. This property is recommended so that you can also view and manage the model in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.

Make an HTTP PATCH request using the URI as shown in the following example. Use the URI of the new model. You can get the new model ID from the `self` property of the [Models_Copy](/rest/api/speechtotext/models/copy) response body. Replace `YourSpeechResoureKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X PATCH -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/models"
```

You should receive a response body in the following format:

```json
{
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
}
```

::: zone-end


## Next steps

- [Test recognition quality](how-to-custom-speech-inspect-data.md)
- [Test model quantitatively](how-to-custom-speech-evaluate-data.md)
- [Deploy a model](how-to-custom-speech-deploy-model.md)
