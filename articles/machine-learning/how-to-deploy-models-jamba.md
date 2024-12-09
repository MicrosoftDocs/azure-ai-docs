---
title: How to deploy AI21's Jamba family models with Azure Machine Learning studio
titleSuffix: Azure Machine Learning studio
description: How to deploy AI21's Jamba family models with Azure Machine Learning studio
manager: scottpolly
ms.service: azure-machine-learning
ms.topic: how-to
ms.date: 09/06/2024
ms.author: ssalgado
ms.reviewer: tgokal
author: ssalgadodev
ms.custom: references_regions
ms.collection: ce-skilling-ai-copilot
---

# How to deploy AI21's Jamba family models with Azure Machine Learning studio

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

In this article, you learn how to use Azure Machine Learning studio to deploy AI21's Jamba family models as a serverless API with pay-as-you-go billing.

The Jamba family models are AI21's production-grade Mamba-based large language model (LLM) which leverages AI21's hybrid Mamba-Transformer architecture. It's an instruction-tuned version of AI21's hybrid structured state space model (SSM) transformer Jamba model. The Jamba family models are built for reliable commercial use with respect to quality and performance.

> [!TIP]
> See our announcements of AI21's Jamba family models available now on Azure AI Model Catalog through [AI21's blog](https://aka.ms/ai21-jamba-1.5-large-announcement) and [Microsoft Tech Community Blog](https://aka.ms/ai21-jamba-1.5-large-microsoft-annnouncement).


## Deploy the Jamba family models as a serverless API

Certain models in the model catalog can be deployed as a serverless API with pay-as-you-go billing, providing a way to consume them as an API without hosting them on your subscription, while keeping the enterprise security and compliance organizations need. This deployment option doesn't require quota from your subscription. 

# [AI21 Jamba 1.5 Large](#tab/ai21-jamba-1-5-large)

The [AI21-Jamba 1.5 Large model](https://aka.ms/aistudio/landing/ai21-labs-jamba-1.5-large) deployed as a serverless API with pay-as-you-go billing is [offered by AI21 through Microsoft Azure Marketplace](https://aka.ms/azure-marketplace-offer-ai21-jamba-1.5-large). AI21 can change or update the terms of use and pricing of this model.

To get started with Jamba 1.5 large deployed as a serverless API, explore our integrations with [LangChain](https://aka.ms/ai21-jamba-1.5-large-langchain-sample), [LiteLLM](https://aka.ms/ai21-jamba-1.5-large-litellm-sample), [OpenAI](https://aka.ms/ai21-jamba-1.5-large-openai-sample) and the [Azure API](https://aka.ms/ai21-jamba-1.5-large-azure-api-sample).


# [AI21 Jamba 1.5 Mini](#tab/ai21-jamba-1-5)

The [AI21 Jamba 1.5 Mini model](https://aka.ms/aistudio/landing/ai21-labs-jamba-1.5-mini) deployed as a serverless API with pay-as-you-go billing is [offered by AI21 through Microsoft Azure Marketplace](https://aka.ms/azure-marketplace-offer-ai21-jamba-1.5-mini). AI21 can change or update the terms of use and pricing of this model.

To get started with Jamba 1.5 mini deployed as a serverless API, explore our integrations with [LangChain](https://aka.ms/ai21-jamba-1.5-mini-langchain-sample), [LiteLLM](https://aka.ms/ai21-jamba-1.5-mini-litellm-sample), [OpenAI](https://aka.ms/ai21-jamba-1.5-mini-openai-sample) and the [Azure API](https://aka.ms/ai21-jamba-1.5-mini-azure-api-sample).

---


### Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- An Azure Machine Learning workspace and a compute instance. If you don't have these, use the steps in the [Quickstart: Create workspace resources](quickstart-create-resources.md) article to create them. The serverless API model deployment offering for the Jamba family of models is only available with workspaces created in these regions:

     * East US
     * East US 2
     * North Central US
     * South Central US
     * West US
     * West US 3
     * Sweden Central

    For a list of  regions that are available for each of the models supporting serverless API endpoint deployments, see [Region availability for models in serverless API endpoints](concept-endpoint-serverless-availability.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure Machine Learning. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. Alternatively, your account can be assigned a custom role that has the following permissions:

    - On the Azure subscription—to subscribe the workspace to the Azure Marketplace offering, once for each workspace, per offering:
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/read`
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action`
      - `Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.SaaS/register/action`
 
    - On the resource group—to create and use the SaaS resource:
      - `Microsoft.SaaS/resources/read`
      - `Microsoft.SaaS/resources/write`
 
    - On the workspace—to deploy endpoints (the Azure Machine Learning data scientist role contains these permissions already):
      - `Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*`  
      - `Microsoft.MachineLearningServices/workspaces/serverlessEndpoints/*`

    For more information on permissions, see [Manage access to an Azure Machine Learning workspace](how-to-assign-roles.md).


### Create a new deployment

These steps demonstrate the deployment of `AI21 Jamba 1.5 Large` or `AI21 Jamba 1.5 Mini` models. To create a deployment:

1. Go to [Azure Machine Learning studio](https://ml.azure.com/home).
1. Select the workspace in which you want to deploy your models. To use the Serverless API model deployment offering, your workspace must belong to one of the supported regions that are listed in the pre-requisites.
1. Search for and select an AI21 model like `AI21 Jamba 1.5 Large` or `AI21 Jamba 1.5 Mini` or `AI21 Jamba Instruct` from the [model catalog](https://ml.azure.com/model/catalog).

   Alternatively, you can initiate deployment by going to your workspace and selecting **Endpoints** > **Serverless endpoints** > **Create**.

1. On the model's overview page in the model catalog, select **Deploy** and then **Serverless API with Azure AI Content Safety**.

1. In the deployment wizard, select the link to **Azure Marketplace Terms** to learn more about the terms of use.

1. You can also select the **Marketplace offer details** tab to learn about pricing for the selected model.

1. If this is your first time deploying the model in the workspace, you have to subscribe your workspace for the particular offering from Azure Marketplace. This step requires that your account has the Azure subscription permissions and resource group permissions listed in the [prerequisites](#prerequisites). Each workspace has its own subscription to the particular Azure Marketplace offering, which allows you to control and monitor spending. Select **Subscribe and Deploy**. Currently you can have only one deployment for each model within a workspace.

1. Once you sign up the workspace for the particular Azure Marketplace offering, subsequent deployments of the _same_ offering in the _same_ workspace don't require subscribing again. Therefore, you don't need to have the subscription-level permissions for subsequent deployments. If this scenario applies to you, select **Continue to deploy**.

1. Give the deployment a name. This name becomes part of the deployment API URL. This URL must be unique in each Azure region.

1. Select **Deploy**. Wait until the deployment is finished and you're redirected to the serverless endpoints page.
1. Select the endpoint to open its Details page.
1. Select the **Test** tab to start interacting with the model.
1. You can also take note of the **Target** URL and the **Secret Key** to call the deployment and generate completions.   
1. You can always find the endpoint's details, URL, and access keys by navigating to **Workspace** > **Endpoints** > **Serverless endpoints**.


To learn about billing for the AI21-Jamba family models deployed as a serverless API with pay-as-you-go token-based billing, see [Cost and quota considerations for Jamba family of models deployed as a serverless API](#cost-and-quota-considerations-for-jamba-family-models-deployed-as-a-serverless-api).

### Consume Jamba family models as a serverless API

You can consume Jamba family models as follows:

1. In the **workspace**, select **Endpoints** > **Serverless endpoints**.
1. Find and select the deployment you created.
1. Copy the **Target** URL and the **Key** token values.
1. Make an API request using either the [Azure AI Model Inference API](reference-model-inference-api.md) on the route `/chat/completions` or the [AI21's Azure Client](https://docs.ai21.com/reference/jamba-instruct-api) on `/v1/chat/completions`.

For more information on using the APIs, see the [reference](#reference-for-jamba-family-models-deployed-as-a-serverless-api) section.



## Reference for Jamba family models deployed as a serverless API

Jamba family models accept both of these APIs:

- The [Azure AI model inference API](reference-model-inference-api.md) [Azure AI Model Inference API] on the route `/chat/completions` for multi-turn chat or single-turn question-answering. This API is supported because Jamba family models are fine-tuned for chat completion.
- [AI21's Azure Client](https://docs.ai21.com/reference/jamba-instruct-api). For more information about the REST endpoint being called, visit [AI21's REST documentation](https://docs.ai21.com/reference/jamba-instruct-api).

### Azure AI model inference API

The  [Azure AI Model Inference API](reference-model-inference-api.md) schema can be found in the [reference for Chat Completions](reference-model-inference-chat-completions.md) article and an [OpenAPI specification can be obtained from the endpoint itself](reference-model-inference-api.md?tabs=rest#getting-started).

Single-turn and multi-turn chat have the same request and response format, except that question answering (single-turn) involves only a single user message in the request, while multi-turn chat requires that you send the entire chat message history in each request. 

In a multi-turn chat, the message thread has the following attributes:

- Includes all messages from the user and the model, ordered from oldest to newest.
- Messages alternate between `user` and `assistant` role messages
- Optionally, the message thread starts with a system message to provide context. 

The following pseudocode is an example of the message stack for the fourth call in a chat request that includes an initial system message.

```json
[
    {"role": "system", "message": "Some contextual information here"},
    {"role": "user", "message": "User message 1"},
    {"role": "assistant", "message": "System response 1"},
    {"role": "user", "message": "User message 2"},
    {"role": "assistant"; "message": "System response 2"},
    {"role": "user", "message": "User message 3"},
    {"role": "assistant", "message": "System response 3"},
    {"role": "user", "message": "User message 4"}
]
```

### AI21's Azure client

Use the method `POST` to send the request to the `/v1/chat/completions` route:

__Request__

```HTTP/1.1
POST /v1/chat/completions HTTP/1.1
Host: <DEPLOYMENT_URI>
Authorization: Bearer <TOKEN>
Content-type: application/json
```

#### Request schema

Payload is a JSON formatted string containing the following parameters:

| Key           | Type           | Required/Default | Allowed values    | Description                                                                                                                                                                                                                                                                                         |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`       | `string`       | Y    | `jamba-instruct` or `AI21 Jamba 1.5 Large` or `AI21 Jamba 1.5 Mini`                                                                                                                                                                                                                                                                           |
| `messages`    | `list[object]` | Y     | A list of objects, one per message, from oldest to newest. The oldest message can be role `system`. All later messages must alternate between user and assistant roles. See the message object definition below.                                                                                    |
| `max_tokens`  | `integer`      | N <br>`4096` |  0 – 4096     | The maximum number of tokens to allow for each generated response message. Typically the best way to limit output length is by providing a length limit in the system prompt (for example, "limit your answers to three sentences")                                                                 |
| `temperature` | `float`        | N <br>`1`  |  0.0 – 2.0      | How much variation to provide in each answer. Setting this value to 0 guarantees the same response to the same question every time. Setting a higher value encourages more variation. Modifies the distribution from which tokens are sampled. We recommend altering this or `top_p`, but not both. |
| `top_p`       | `float`        | N <br>`1`  | 0 < _value_ <=1.0 | Limit the pool of next tokens in each step to the top N percentile of possible tokens, where 1.0 means the pool of all possible tokens, and 0.01 means the pool of only the most likely next tokens.                                                                                                |
| `stop`        | `string` OR `list[string]`      | N <br>  | ""  | String or list of strings containing the word(s) where the API should stop generating output. Newlines are allowed as "\n". The returned text won't contain the stop sequence. |
| `n`           | `integer`      | N <br>`1`  | 1 – 16          | How many responses to generate for each prompt. With Azure AI Foundry's Playground, `n=1` as we work on multi-response Playground.                                                                                                                                                                                              |
| `stream`   | `boolean`      | N <br>`False` | `True` OR `False` | Whether to enable streaming. If true, results are returned one token at a time. If set to true, `n` must be 1, which is automatically set.                                                                                                                                                                                     |

The `messages` object has the following fields:
  - `role`: [_string, required_] The author or purpose of the message. One of the following values:
    - `user`:  Input provided by the user. Any instructions given here that conflict with instructions given in the `system` prompt take precedence over the `system` prompt instructions.
    - `assistant`:  A response generated by the model.
    - `system`:  Initial instructions to provide general guidance on the tone and voice of the generated message. An initial system message is optional, but recommended to provide guidance on the tone of the chat. For example, "You are a helpful chatbot with a background in earth sciences and a charming French accent."
  - `content`: [_string, required_] The content of the message.


#### Request example

__Single-turn example__

```JSON
{
    "model": "jamba-instruct",
    "messages": [
    {
      "role":"user",
      "content":"Who was the first emperor of rome?"}
  ],
    "temperature": 0.8,
    "max_tokens": 512
}
```

__Chat example (fourth request containing third user response)__

```JSON
{
  "model": "jamba-instruct",
  "messages": [
     {"role": "system",
      "content": "You are a helpful genie just released from a bottle. You start the conversation with 'Thank you for freeing me! I grant you one wish.'"},
     {"role":"user",
      "content":"I want a new car"},
     {"role":"assistant",
      "content":"🚗 Great choice, I can definitely help you with that! Before I grant your wish, can you tell me what kind of car you're looking for?"},
     {"role":"user",
      "content":"A corvette"},
     {"role":"assistant",
      "content":"Great choice! What color and year?"},
     {"role":"user",
      "content":"1963 black split window Corvette"}
  ],
  "n":3
}
```

#### Response schema

The response depends slightly on whether the result is streamed or not.

In a _non-streamed result_, all responses are delivered together in a single response, which also includes a `usage` property.

In a _streamed result_,

* Each response includes a single token in the `choices` field.
* The `choices` object structure is different.
* Only the last response includes a `usage` object.
* The entire response is wrapped in a `data` object.
* The final response object is `data: [DONE]`.

The response payload is a dictionary with the following fields.

| Key       | Type      | Description                                                         |
| --------- | --------- | ------------------------------------------------------------------- |
| `id`      | `string`  | A unique identifier for the request.                                |
| `model`   | `string`  | Name of the model used.                                   |
| `choices` | `list[object`]|The model-generated response text. For a non-streaming response it is a list with `n` items. For a streaming response, it is a single object containing a single token. See the object description below. |
| `created` | `integer` | The Unix timestamp (in seconds) of when the completion was created. |
| `object`  | `string`  | The object type, which is always `chat.completion`.                 |
| `usage`   | `object`  | Usage statistics for the completion request. See below for details. |

The `choices` response object contains the model-generated response. The object has the following fields:

| Key             | Type      | Description                                                                                                                                                                                                                                                                                                                                      |
| --------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `index`         | `integer` | Zero-based index of the message in the list of messages. Might not correspond to the position in the list. For streamed messages this is always zero.                                                                                                                                                                                           |
| `message` OR `delta`      | `object`  | The generated message (or token in a streaming response). Same object type as described in the request with two changes:<br> - In a non-streaming response, this object is called `message`. <br>- In a streaming response, it is called `delta`, and contains either `message` or `role` but never both.                                                                                                                                                                                                                                        |
| `finish_reason` | `string`  | The reason the model stopped generating tokens: <br>- `stop`: The model reached a natural stop point, or a provided stop sequence. <br>- `length`: Max number of tokens have been reached. <br>- `content_filter`: The generated response violated a responsible AI policy. <br>- `null`: Streaming only. In a streaming response, all responses except the last will be `null`. |

The `usage` response object contains the following fields. 

| Key                 | Type      | Value                                                                                                                                                                                                                                                                                                                   |
| ------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt_tokens`     | `integer` | Number of tokens in the prompt. Note that the prompt token count includes extra tokens added by the system to format the prompt list into a single string as required by the model. The number of extra tokens is typically proportional to the number of messages in the thread, and should be relatively small. |
| `completion_tokens` | `integer` | Number of tokens generated in the completion.                                                                                                                                                                                                                                                                           |
| `total_tokens`      | `integer` | Total tokens. 

#### Non-streaming response example

```JSON
{
  "id":"cmpl-524c73beb8714d878e18c3b5abd09f2a",
  "choices":[
    {
      "index":0,
      "message":{
        "role":"assistant",
        "content":"The human nose can detect over 1 trillion different scents, making it one of the most sensitive smell organs in the animal kingdom."
      },
      "finishReason":"stop"
    }
  ],
  "created": 1717487036,
  "usage":{
    "promptTokens":116,
    "completionTokens":30,
    "totalTokens":146
  }
}
```
#### Streaming response example

```JSON
data: {"id": "cmpl-8e8b2f6556f94714b0cd5cfe3eeb45fc", "choices": [{"index": 0, "delta": {"role": "assistant"}, "created": 1717487336, "finish_reason": null}]}
data: {"id": "cmpl-8e8b2f6556f94714b0cd5cfe3eeb45fc", "choices": [{"index": 0, "delta": {"content": ""}, "created": 1717487336, "finish_reason": null}]}
data: {"id": "cmpl-8e8b2f6556f94714b0cd5cfe3eeb45fc", "choices": [{"index": 0, "delta": {"content": " The"}, "created": 1717487336, "finish_reason": null}]}
data: {"id": "cmpl-8e8b2f6556f94714b0cd5cfe3eeb45fc", "choices": [{"index": 0, "delta": {"content": " first e"}, "created": 1717487336, "finish_reason": null}]}
data: {"id": "cmpl-8e8b2f6556f94714b0cd5cfe3eeb45fc", "choices": [{"index": 0, "delta": {"content": "mpe"}, "created": 1717487336, "finish_reason": null}]}
... 115 responses omitted for sanity ...
data: {"id": "cmpl-8e8b2f6556f94714b0cd5cfe3eeb45fc", "choices": [{"index": 0, "delta": {"content": "me"}, "created": 1717487336, "finish_reason": null}]}
data: {"id": "cmpl-8e8b2f6556f94714b0cd5cfe3eeb45fc", "choices": [{"index": 0, "delta": {"content": "."}, "created": 1717487336,"finish_reason": "stop"}], "usage": {"prompt_tokens": 107, "completion_tokens": 121, "total_tokens": 228}}
data: [DONE]
```

## Cost and quotas

### Cost and quota considerations for Jamba family models deployed as a serverless API

The Jamba family models are deployed as a serverless API and is offered by AI21 through Azure Marketplace and integrated with Azure AI Foundry for use. You can find Azure Marketplace pricing when deploying or fine-tuning models.

Each time a workspace subscribes to a given model offering from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through the Azure Marketplace](/azure/ai-studio/how-to/costs-plan-manage#monitor-costs-for-models-offered-through-the-azure-marketplace).

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

## Content filtering

Models deployed as a serverless API are protected by Azure AI content safety. With Azure AI content safety enabled, both the prompt and completion pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions. Learn more about [Azure AI Content Safety](/azure/ai-services/content-safety/overview).

## Related content

- [Model Catalog and Collections](concept-model-catalog.md)
- [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md)
- [Plan and manage costs for Azure AI Foundry](/azure/ai-studio/how-to/costs-plan-manage)
- [Region availability for models in serverless API endpoints](concept-endpoint-serverless-availability.md)
