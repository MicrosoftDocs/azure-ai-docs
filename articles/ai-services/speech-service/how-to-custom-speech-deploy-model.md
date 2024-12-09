---
title: Deploy a custom speech model - Speech service
titleSuffix: Azure AI services
description: Learn how to deploy custom speech models. 
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/19/2024
ms.author: eur
zone_pivot_groups: speech-studio-cli-rest
#Customer intent: As a developer, I want to learn how to deploy a custom speech model so that I can use it in my applications.
---

# Deploy a custom speech model

In this article, you learn how to deploy an endpoint for a custom speech model. Except for [batch transcription](batch-transcription.md), you must deploy a custom endpoint to use a custom speech model.

> [!TIP]
> A hosted deployment endpoint isn't required to use custom speech with the [Batch transcription API](batch-transcription.md). You can conserve resources if the [custom speech model](how-to-custom-speech-train-model.md) is only used for batch transcription. For more information, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

You can deploy an endpoint for a base or custom model, and then [update](#change-model-and-redeploy-endpoint) the endpoint later to use a better trained model.

> [!NOTE]
> Endpoints used by `F0` Speech resources are deleted after seven days. 

## Add a deployment endpoint

::: zone pivot="speech-studio"

To create a custom endpoint, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Deploy models**.

   If this is your first endpoint, you notice that there are no endpoints listed in the table. After you create an endpoint, you use this page to track each deployed endpoint.

1. Select **Deploy model** to start the new endpoint wizard.

1. On the **New endpoint** page, enter a name and description for your custom endpoint. 

1. Select the custom model that you want to associate with the endpoint. 

1. Optionally, you can check the box to enable audio and diagnostic [logging](#view-logging-data) of the endpoint's traffic.

    :::image type="content" source="./media/custom-speech/custom-speech-deploy-model.png" alt-text="Screenshot of the New endpoint page that shows the checkbox to enable logging.":::

1. Select **Add** to save and deploy the endpoint. 

On the main **Deploy models** page, details about the new endpoint are displayed in a table, such as name, description, status, and expiration date. It can take up to 30 minutes to instantiate a new endpoint that uses your custom models. When the status of the deployment changes to **Succeeded**, the endpoint is ready to use.

> [!IMPORTANT]
> Take note of the model expiration date. This is the last date that you can use your custom model for speech recognition. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

Select the endpoint link to view information specific to it, such as the endpoint key, endpoint URL, and sample code. 

::: zone-end

::: zone pivot="speech-cli"

To create an endpoint and deploy a model, use the `spx csr endpoint create` command. Construct the request parameters according to the following instructions:

- Set the `project` parameter to the ID of an existing project. This is recommended so that you can also view and manage the endpoint in Speech Studio. You can run the `spx csr project list` command to get available projects.
- Set the required `model` parameter to the ID of the model that you want deployed to the endpoint. 
- Set the required `language` parameter. The endpoint locale must match the locale of the model. The locale can't be changed later. The Speech CLI `language` parameter corresponds to the `locale` property in the JSON request and response.
- Set the required `name` parameter. This is the name that is displayed in the Speech Studio. The Speech CLI `name` parameter corresponds to the `displayName` property in the JSON request and response.
- Optionally, you can set the `logging` parameter. Set this to `enabled` to enable audio and diagnostic [logging](#view-logging-data) of the endpoint's traffic. The default is `false`. 

Here's an example Speech CLI command to create an endpoint and deploy a model:

```azurecli-interactive
spx csr endpoint create --api-version v3.2 --project YourProjectId --model YourModelId --name "My Endpoint" --description "My Endpoint Description" --language "en-US"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52"
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

- Set the `project` property to the URI of an existing project. This is recommended so that you can also view and manage the endpoint in Speech Studio. You can make a [Projects_List](/rest/api/speechtotext/projects/list) request to get available projects.
- Set the required `model` property to the URI of the model that you want deployed to the endpoint. 
- Set the required `locale` property. The endpoint locale must match the locale of the model. The locale can't be changed later.
- Set the required `displayName` property. This is the name that is displayed in the Speech Studio.
- Optionally, you can set the `loggingEnabled` property within `properties`. Set this to `true` to enable audio and diagnostic [logging](#view-logging-data) of the endpoint's traffic. The default is `false`. 

Make an HTTP POST request using the URI as shown in the following [Endpoints_Create](/rest/api/speechtotext/endpoints/create) example. Replace `YourSubscriptionKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSubscriptionKey" -H "Content-Type: application/json" -d '{
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52"
  },
  "properties": {
    "loggingEnabled": true
  },
  "displayName": "My Endpoint",
  "description": "My Endpoint Description",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ae8d1643-53e4-4554-be4c-221dcfb471c5"
  },
  "locale": "en-US",
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52"
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

An endpoint can be updated to use another model that was created by the same Speech resource. As previously mentioned, you must update the endpoint's model before the [model expires](./how-to-custom-speech-model-and-endpoint-lifecycle.md). 

::: zone pivot="speech-studio"

To use a new model and redeploy the custom endpoint:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Deploy models**.
1. Select the link to an endpoint by name, and then select **Change model**.
1. Select the new model that you want the endpoint to use.
1. Select **Done** to save and redeploy the endpoint.

::: zone-end

::: zone pivot="speech-cli"

To redeploy the custom endpoint with a new model, use the `spx csr model update` command. Construct the request parameters according to the following instructions:

- Set the required `endpoint` parameter to the ID of the endpoint that you want deployed.
- Set the required `model` parameter to the ID of the model that you want deployed to the endpoint.

Here's an example Speech CLI command that redeploys the custom endpoint with a new model:

```azurecli-interactive
spx csr endpoint update --api-version v3.2 --endpoint YourEndpointId --model YourModelId
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52"
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

Make an HTTP PATCH request using the URI as shown in the following example. Replace `YourSubscriptionKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, replace `YourEndpointId` with your endpoint ID, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X PATCH -H "Ocp-Apim-Subscription-Key: YourSubscriptionKey" -H "Content-Type: application/json" -d '{
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd"
  },
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/YourEndpointId"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52"
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

Logging data is available for export if you configured it while creating the endpoint. 

::: zone pivot="speech-studio"

To download the endpoint logs:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Deploy models**.
1. Select the link by endpoint name.
1. Under **Content logging**, select **Download log**.

::: zone-end

::: zone pivot="speech-cli"

To get logs for an endpoint, use the `spx csr endpoint list` command. Construct the request parameters according to the following instructions:

- Set the required `endpoint` parameter to the ID of the endpoint that you want to get logs.

Here's an example Speech CLI command that gets logs for an endpoint:

```azurecli-interactive
spx csr endpoint list --api-version v3.2 --endpoint YourEndpointId
```

The locations of each log file with more details are returned in the response body.

::: zone-end

::: zone pivot="rest-api"

To get logs for an endpoint, start by using the [Endpoints_Get](/rest/api/speechtotext/endpoints/get) operation of the [Speech to text REST API](rest-speech-to-text.md).

Make an HTTP GET request using the URI as shown in the following example. Replace `YourEndpointId` with your endpoint ID, replace `YourSubscriptionKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/YourEndpointId" -H "Ocp-Apim-Subscription-Key: YourSubscriptionKey"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/9e240dc1-3d2d-4ac9-98ec-1be05ba0e9dd"
  },
  "links": {
    "logs": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/a07164e8-22d1-4eb7-aa31-bf6bb1097f37/files/logs",
    "restInteractive": "https://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restConversation": "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "restDictation": "https://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketInteractive": "wss://eastus.stt.speech.microsoft.com/speech/recognition/interactive/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketConversation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37",
    "webSocketDictation": "wss://eastus.stt.speech.microsoft.com/speech/recognition/dictation/cognitiveservices/v1?cid=a07164e8-22d1-4eb7-aa31-bf6bb1097f37"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52"
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

Make an HTTP GET request using the "logs" URI from the previous response body. Replace `YourEndpointId` with your endpoint ID, replace `YourSubscriptionKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.


```curl
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/endpoints/YourEndpointId/files/logs" -H "Ocp-Apim-Subscription-Key: YourSubscriptionKey"
```

The locations of each log file with more details are returned in the response body.

::: zone-end

Logging data is available on Microsoft-owned storage for 30 days, and then it's removed. If your own storage account is linked to the Azure AI services subscription, the logging data isn't automatically deleted.

## Related content

- [Custom speech overview](custom-speech-overview.md)
- [Custom speech model lifecycle](how-to-custom-speech-model-and-endpoint-lifecycle.md)
