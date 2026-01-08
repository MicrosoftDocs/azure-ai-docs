---
title: Deploy a custom speech model - Speech service
titleSuffix: Foundry Tools
description: Learn how to deploy custom speech models. 
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/29/2025
ms.author: pafarley
zone_pivot_groups: foundry-speech-studio-cli-rest
#Customer intent: As a developer, I want to learn how to deploy a custom speech model so that I can use it in my applications.
---

# Deploy a custom speech model

In this article, you learn how to deploy an endpoint for a custom speech model. Except for [batch transcription](batch-transcription.md), you must deploy a custom endpoint to use a custom speech model.

> [!TIP]
> The [Batch transcription API](batch-transcription.md) doesn't require a hosted deployment endpoint for custom speech. You can conserve resources by only using the [custom speech model](how-to-custom-speech-train-model.md) for batch transcription. For more information, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

You can deploy an endpoint for a base or custom model, and then [update](#change-model-and-redeploy-endpoint) the endpoint later to use a better trained model.

> [!NOTE]
> Endpoints used by `F0` Speech resources are deleted after seven days. 

## Add a deployment endpoint

> [!TIP]
> Bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). In Microsoft Foundry portal, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-studio/ai-services/how-to/connect-ai-services.md#connect-azure-ai-services-after-you-create-a-project).

::: zone pivot="ai-foundry-portal"

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the custom speech fine-tuning task (by model name) that you [started as described in the how to start custom speech fine-tuning article](./how-to-custom-speech-create-project.md).
1. Select **Deploy models** > **+ Deploy models**. 

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-deploy-model.png" alt-text="Screenshot of the page with an option to deploy the custom speech model." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-deploy-model.png":::

1. In the **Deploy a new model** wizard, select the model that you want to deploy. 

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-deploy-model-select-and-deploy.png" alt-text="Screenshot of the page with an option to select the model that you want to deploy." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-deploy-model-select-and-deploy.png":::

1. Enter a name and description for the deployment. Select the box to agree to the terms of use. Then select **Deploy**.

1. After the deployment status is **Succeeded**, you can view the deployment details. Select the deployment to view the details like the endpoint ID. 

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-deploy-model-status-succeeded.png" alt-text="Screenshot of the page with an option to select the deployment to view the details like the endpoint ID." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-deploy-model-status-succeeded.png":::


::: zone-end

::: zone pivot="speech-studio"

To create a custom endpoint, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Deploy models**.

   If this is your first endpoint, notice that the table has no endpoints listed. After you create an endpoint, use this page to track each deployed endpoint.

1. Select **Deploy model** to start the new endpoint wizard.

1. On the **New endpoint** page, enter a name and description for your custom endpoint. 

1. Select the custom model that you want to associate with the endpoint. 

1. Optionally, check the box to enable audio and diagnostic [logging](#view-logging-data) of the endpoint's traffic.

    :::image type="content" source="./media/custom-speech/custom-speech-deploy-model.png" alt-text="Screenshot of the New endpoint page that shows the checkbox to enable logging.":::

1. Select **Add** to save and deploy the endpoint. 

On the main **Deploy models** page, details about the new endpoint are displayed in a table, such as name, description, status, and expiration date. It can take up to 30 minutes to instantiate a new endpoint that uses your custom models. When the status of the deployment changes to **Succeeded**, the endpoint is ready to use.

> [!IMPORTANT]
> Take note of the model expiration date. This date is the last day that you can use your custom model for speech recognition. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

Select the endpoint link to view information specific to it, such as the endpoint key, endpoint URL, and sample code. 

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To create an endpoint and deploy a model, use the `spx csr endpoint create` command. Construct the request parameters according to the following instructions:

- Set the `project` property to the ID of an existing project. Use the `project` property so you can manage fine-tuning for custom speech in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api).
- Set the required `model` property to the ID of the model that you want deployed to the endpoint. 
- Set the required `language` property. The endpoint locale must match the locale of the model. You can't change the locale later. The Speech CLI `language` property corresponds to the `locale` property in the JSON request and response.
- Set the required `name` property. This name appears in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). The Speech CLI `name` property corresponds to the `displayName` property in the JSON request and response.
- Optionally, set the `logging` property. Set this property to `enabled` to enable audio and diagnostic [logging](#view-logging-data) of the endpoint's traffic. The default is `false`. 

Here's an example Speech CLI command to create an endpoint and deploy a model:

```azurecli-interactive
spx csr endpoint create --api-version v3.2 --project YourProjectId --model YourModelId --name "My Endpoint" --description "My Endpoint Description" --language "en-US"
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API but doesn't yet support versions later than `v3.2`.

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "properties": {
    "loggingEnabled": true
  },
  "lastActionDateTime": "2024-07-15T16:29:36Z",
  "status": "NotStarted",
  "createdDateTime": "2024-07-15T16:29:36Z",
  "locale": "en-US",
  "displayName": "My Endpoint",
  "description": "My Endpoint Description"
}
```

The top-level `self` property in the response body is the endpoint's URI. Use this URI to get details about the endpoint's project, model, and logs. You also use this URI to update the endpoint.

For Speech CLI help with endpoints, run the following command:

```azurecli-interactive
spx help csr endpoint
```

::: zone-end

::: zone pivot="rest-api"

To create an endpoint and deploy a model, use the [Endpoints_Create](/rest/api/speechtotext/endpoints/create) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the `project` property to the URI of an existing project. Set this property so you can view and manage the endpoint in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api).
- Set the required `model` property to the URI of the model that you want deployed to the endpoint. 
- Set the required `locale` property. The endpoint locale must match the locale of the model. You can't change the locale later.
- Set the required `displayName` property. This name appears in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
- Optionally, set the `loggingEnabled` property within `properties`. Set this property to `true` to enable audio and diagnostic [logging](#view-logging-data) of the endpoint's traffic. The default is `false`. 

Make an HTTP POST request using the URI as shown in the following [Endpoints_Create](/rest/api/speechtotext/endpoints/create) example. Replace `YourSpeechResoureKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "properties": {
    "loggingEnabled": true
  },
  "displayName": "My Endpoint",
  "description": "My Endpoint Description",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "locale": "en-US",
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints"
```

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "properties": {
    "loggingEnabled": true
  },
  "lastActionDateTime": "2024-07-15T16:29:36Z",
  "status": "NotStarted",
  "createdDateTime": "2024-07-15T16:29:36Z",
  "locale": "en-US",
  "displayName": "My Endpoint",
  "description": "My Endpoint Description"
}
```

The top-level `self` property in the response body is the endpoint's URI. Use this URI to [get](/rest/api/speechtotext/endpoints/get) details about the endpoint's project, model, and logs. You also use this URI to [update](/rest/api/speechtotext/endpoints/update) or [delete](/rest/api/speechtotext/endpoints/delete) the endpoint.

::: zone-end

## Change model and redeploy endpoint

You can update an endpoint to use another model created by the same Speech resource. As previously mentioned, you must update the endpoint's model before the [model expires](./how-to-custom-speech-model-and-endpoint-lifecycle.md). 

::: zone pivot="ai-foundry-portal"



::: zone-end

::: zone pivot="speech-studio"

To use a new model and redeploy the custom endpoint:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Deploy models**.
1. Select the link to an endpoint by name, and then select **Change model**.
1. Select the new model that you want the endpoint to use.
1. Select **Done** to save and redeploy the endpoint.

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To redeploy the custom endpoint with a new model, use the `spx csr model update` command. Construct the request parameters according to the following instructions:

- Set the required `endpoint` property to the ID of the endpoint that you want deployed.
- Set the required `model` property to the ID of the model that you want deployed to the endpoint.

Here's an example Speech CLI command that redeploys the custom endpoint with a new model:

```azurecli-interactive
spx csr endpoint update --api-version v3.2 --endpoint YourEndpointId --model YourModelId
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API but doesn't yet support versions later than `v3.2`.

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "properties": {
    "loggingEnabled": true
  },
  "lastActionDateTime": "2024-07-15T16:30:12Z",
  "status": "Succeeded",
  "createdDateTime": "2024-07-15T16:29:36Z",
  "locale": "en-US",
  "displayName": "My Endpoint",
  "description": "My Endpoint Description"
}
```

For Speech CLI help with endpoints, run the following command:

```azurecli-interactive
spx help csr endpoint
```

::: zone-end

::: zone pivot="rest-api"

To redeploy the custom endpoint with a new model, use the [Endpoints_Update](/rest/api/speechtotext/endpoints/update) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the `model` property to the URI of the model that you want deployed to the endpoint.

Make an HTTP PATCH request using the URI as shown in the following example. Replace `YourSpeechResoureKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, replace `YourEndpointId` with your endpoint ID, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X PATCH -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/YourEndpointId"
```

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "properties": {
    "loggingEnabled": true
  },
  "lastActionDateTime": "2024-07-15T16:30:12Z",
  "status": "Succeeded",
  "createdDateTime": "2024-07-15T16:29:36Z",
  "locale": "en-US",
  "displayName": "My Endpoint",
  "description": "My Endpoint Description"
}
```

::: zone-end

The redeployment takes several minutes to complete. In the meantime, your endpoint uses the previous model without interruption of service. 

## View logging data

You can export logging data if you configured it when creating the endpoint. 

::: zone pivot="ai-foundry-portal"



::: zone-end

::: zone pivot="speech-studio"

To download the endpoint logs:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Deploy models**.
1. Select the link by endpoint name.
1. Under **Content logging**, select **Download log**.

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To get logs for an endpoint, use the `spx csr endpoint list` command. Construct the request parameters according to the following instructions:

- Set the required `endpoint` property to the ID of the endpoint that you want to get logs.

Here's an example Speech CLI command that gets logs for an endpoint:

```azurecli-interactive
spx csr endpoint list --api-version v3.2 --endpoint YourEndpointId
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API but doesn't yet support versions later than `v3.2`.

The response body returns the locations of each log file with more details.

::: zone-end

::: zone pivot="rest-api"

To get logs for an endpoint, start by using the [Endpoints_Get](/rest/api/speechtotext/endpoints/get) operation of the [Speech to text REST API](rest-speech-to-text.md).

Make an HTTP GET request using the URI as shown in the following example. Replace `YourEndpointId` with your endpoint ID, replace `YourSpeechResoureKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/YourEndpointId" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/aaaabbbb-0000-cccc-1111-dddd2222eeee",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "properties": {
    "loggingEnabled": true
  },
  "lastActionDateTime": "2024-07-15T16:30:12Z",
  "status": "Succeeded",
  "createdDateTime": "2024-07-15T16:29:36Z",
  "locale": "en-US",
  "displayName": "My Endpoint",
  "description": "My Endpoint Description"
}
```

Make an HTTP GET request using the "logs" URI from the previous response body. Replace `YourEndpointId` with your endpoint ID, replace `YourSpeechResoureKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.


```curl
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/YourEndpointId/files/logs" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

The response body returns the locations of each log file with more details.

::: zone-end

Microsoft-owned storage keeps logging data for 30 days, and then it removes the data. If you link your own storage account to the Foundry Tools subscription, the logging data isn't automatically deleted.

## Related content

- [Custom speech overview](custom-speech-overview.md)
- [Custom speech model lifecycle](how-to-custom-speech-model-and-endpoint-lifecycle.md)
