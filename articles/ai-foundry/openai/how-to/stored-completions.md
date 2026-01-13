---
title: 'How to use Azure OpenAI in Microsoft Foundry Models stored completions & distillation'
titleSuffix: Azure OpenAI
description: Learn how to use stored completions & distillation with Azure OpenAI
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom: references_regions
ms.date: 12/6/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Azure OpenAI stored completions & distillation (preview)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Stored completions allow you to capture the conversation history from chat completions sessions to use as datasets for [evaluations](./evaluations.md) and [fine-tuning](./fine-tuning.md).

## Stored completions support

### Model & region availability

As long as you're using the Chat Completions API for inferencing, you can leverage stored completions. It is supported for all Azure OpenAI models, and in all supported regions (including global-only regions).

## Configure stored completions

To enable stored completions for your Azure OpenAI deployment set the `store` parameter to `True`. Use the `metadata` parameter to enrich your stored completion dataset with additional information.

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider,
)

completion = client.chat.completions.create(
    
    model="gpt-4o", # replace with model deployment name
    store= True,
    metadata =  {
    "user": "admin",
    "category": "docs-test",
  },
    messages=[
    {"role": "system", "content": "Provide a clear and concise summary of the technical content, highlighting key concepts and their relationships. Focus on the main ideas and practical implications."},
    {"role": "user", "content": "Ensemble methods combine multiple machine learning models to create a more robust and accurate predictor. Common techniques include bagging (training models on random subsets of data), boosting (sequentially training models to correct previous errors), and stacking (using a meta-model to combine base model predictions). Random Forests, a popular bagging method, create multiple decision trees using random feature subsets. Gradient Boosting builds trees sequentially, with each tree focusing on correcting the errors of previous trees. These methods often achieve better performance than single models by reducing overfitting and variance while capturing different aspects of the data."}
    ]   
)

print(completion.choices[0].message)


```

# [Python (API Key)](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import OpenAI
    
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
    )

completion = client.chat.completions.create(
    
    model="gpt-4o", # replace with model deployment name
    store= True,
    metadata =  {
    "user": "admin",
    "category": "docs-test",
  },
    messages=[
    {"role": "system", "content": "Provide a clear and concise summary of the technical content, highlighting key concepts and their relationships. Focus on the main ideas and practical implications."},
    {"role": "user", "content": "Ensemble methods combine multiple machine learning models to create a more robust and accurate predictor. Common techniques include bagging (training models on random subsets of data), boosting (sequentially training models to correct previous errors), and stacking (using a meta-model to combine base model predictions). Random Forests, a popular bagging method, create multiple decision trees using random feature subsets. Gradient Boosting builds trees sequentially, with each tree focusing on correcting the errors of previous trees. These methods often achieve better performance than single models by reducing overfitting and variance while capturing different aspects of the data."}
    ]   
)

print(completion.choices[0].message)
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "gpt-4o",
    "store": true,
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
```

### API Key

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "store": true,
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
```

# [Output](#tab/output)

```json
{
  "id": "chatcmpl-B4eQ716S5wGUyFpGgX2MXnJEC5AW5",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Ensemble methods enhance machine learning performance by combining multiple models to create a more robust and accurate predictor. The key techniques include:\n\n1. **Bagging (Bootstrap Aggregating)**: Involves training multiple models on random subsets of the data to reduce variance and overfitting. A popular method within bagging is Random Forests, which build numerous decision trees using random subsets of features and data samples.\n\n2. **Boosting**: Focuses on sequentially training models, where each new model attempts to correct the errors made by previous ones. Gradient Boosting is a common boosting technique that builds trees sequentially, concentrating on the mistakes of earlier trees to improve accuracy.\n\n3. **Stacking**: Uses a meta-model to combine predictions from various base models, leveraging their strengths to enhance overall predictions.\n\nThese ensemble methods generally outperform individual models because they effectively handle overfitting, reduce variance, and capture diverse aspects of the data. In practical applications, they are valued for their ability to improve model accuracy and stability.",
        "refusal": null,
        "role": "assistant",
        "audio": null,
        "function_call": null,
        "tool_calls": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "filtered": false,
          "detected": false
        },
        "protected_material_text": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1740448387,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_b705f0c291",
  "usage": {
    "completion_tokens": 205,
    "prompt_tokens": 157,
    "total_tokens": 362,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 0,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    }
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

---

Once stored completions are enabled for an Azure OpenAI deployment, they'll begin to show up in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) in the **Stored Completions** pane.

:::image type="content" source="../media/stored-completions/stored-completions.png" alt-text="Screenshot of the stored completions User Experience." lightbox="../media/stored-completions/stored-completions.png":::

## Distillation

Distillation allows you to turn your stored completions into a fine-tuning dataset. A common use case is to use stored completions with a larger more powerful model for a particular task and then use the stored completions to train a smaller model on high quality examples of model interactions.

Distillation requires a minimum of 10 stored completions, though it's recommended to provide hundreds to thousands of stored completions for the best results.

1. From the **Stored Completions** pane in the [Foundry portal](https://ai.azure.com/?cid=learnDocs) use the **Filter** options to select the completions you want to train your model with.

2. To begin distillation, select **Distill**

    :::image type="content" source="../media/stored-completions/distill.png" alt-text="Screenshot of the stored completions User Experience with distill highlighted." lightbox="../media/stored-completions/distill.png":::

3. Pick which model you would like to fine-tune with your stored completion dataset.

    :::image type="content" source="../media/stored-completions/fine-tune.png" alt-text="Screenshot of the stored completion distillation model selection." lightbox="../media/stored-completions/fine-tune.png":::

4. Confirm which version of the model you want to fine-tune:

    :::image type="content" source="../media/stored-completions/version.png" alt-text="Screenshot of the stored completion distillation version." lightbox="../media/stored-completions/version.png":::

5. A `.jsonl` file with a randomly generated name will be created as a training dataset from your stored completions. Select the file > **Next**.

    > [!Note]
    > Stored completion distillation training files cannot be accessed directly and cannot be exported externally/downloaded.

    :::image type="content" source="../media/stored-completions/file-name.png" alt-text="Screenshot of the stored completion training dataset jsonl file." lightbox="../media/stored-completions/file-name.png":::

The rest of the steps correspond to the typical Azure OpenAI fine-tuning steps. To learn more, see our [fine-tuning getting started guide](./fine-tuning.md).

## Evaluation

The [evaluation](./evaluations.md) of large language models is a critical step in measuring their performance across various tasks and dimensions. This is especially important for fine-tuned models, where assessing the performance gains (or losses) from training is crucial. Thorough evaluations can help your understanding of how different versions of the model may impact your application or scenario.

Stored completions can be used as a dataset for running evaluations.

1. From the **Stored Completions** pane in the [Foundry portal](https://ai.azure.com/?cid=learnDocs) use the **Filter** options to select the completions you want to be part of your evaluation dataset.

2. To configure the evaluation, select **Evaluate**

    :::image type="content" source="../media/stored-completions/evaluate.png" alt-text="Screenshot of the stored completion pane with evaluate selected." lightbox="../media/stored-completions/evaluate.png":::

3. This launches the **Evaluations** pane with a prepopulated `.jsonl` file with a randomly generated name that is created as an evaluation dataset from your stored completions.

    > [!Note]
    > Stored completion evaluation data files cannot be accessed directly and cannot be exported externally/downloaded.

    :::image type="content" source="../media/stored-completions/evaluation-data.png" alt-text="Screenshot of the evaluations pane." lightbox="../media/stored-completions/evaluation-data.png":::

To learn more about evaluation see, [getting started with evaluations](./evaluations.md)

## Stored completions API

To access the stored completions API commands you may need to upgrade your version of the OpenAI library.

```cmd
pip install --upgrade openai
```

### List stored completions

# [Python (Microsoft Entra ID)](#tab/python-secure)

Additional parameters:

* `metadata`: Filter by the key/value pair in the stored completions
* `after`: Identifier for the last stored completion message from the previous pagination request.
* `limit`: Number of stored completions messages to retrieve.
* `order`: Order of the results by index (ascending or descending).

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider,
)

response = client.chat.completions.list()

print(response.model_dump_json(indent=2))
```

# [Python (API Key)](#tab/python-key)

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/", 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
)

response = client.chat.completions.list()

print(response.model_dump_json(indent=2))
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
```

### API Key

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
```

# [Output](#tab/output)

```json
{
  "data": [
    {
      "id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u",
      "choices": [
        {
          "finish_reason": null,
          "index": 0,
          "logprobs": null,
          "message": {
            "content": "Ensemble methods enhance machine learning performance by combining multiple models to create a more robust and accurate predictor. The key techniques include:\n\n1. **Bagging (Bootstrap Aggregating):** This involves training models on random subsets of the data to reduce variance and prevent overfitting. Random Forests, a popular bagging method, build multiple decision trees using random feature subsets, leading to robust predictions.\n\n2. **Boosting:** This sequential approach trains models to correct the errors of their predecessors, thereby focusing on difficult-to-predict data points. Gradient Boosting is a common implementation that sequentially builds decision trees, each improving upon the prediction errors of the previous ones.\n\n3. **Stacking:** This technique uses a meta-model to combine the predictions of multiple base models, leveraging their diverse strengths to enhance overall prediction accuracy.\n\nThe practical implications of ensemble methods include achieving superior model performance compared to single models by capturing various data patterns and reducing overfitting and variance. These methods are widely used in applications where high accuracy and model reliability are critical.",
            "refusal": null,
            "role": "assistant",
            "audio": null,
            "function_call": null,
            "tool_calls": null
          }
        }
      ],
      "created": 1740447656,
      "model": "gpt-4o-2024-08-06",
      "object": null,
      "service_tier": null,
      "system_fingerprint": "fp_b705f0c291",
      "usage": {
        "completion_tokens": 208,
        "prompt_tokens": 157,
        "total_tokens": 365,
        "completion_tokens_details": null,
        "prompt_tokens_details": null
      },
      "request_id": "0000aaaa-11bb-cccc-dd22-eeeeee333333",
      "seed": -430976584126747957,
      "top_p": 1,
      "temperature": 1,
      "presence_penalty": 0,
      "frequency_penalty": 0,
      "metadata": {
        "user": "admin",
        "category": "docs-test"
      }
    }
  ],
  "has_more": false,
  "object": "list",
  "total": 1,
  "first_id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u",
  "last_id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u"
}
```

---

### Get stored completion

Get stored completion by ID.

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider
)

response = client.chat.completions.retrieve("chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u")

print(response.model_dump_json(indent=2))
```

# [Python (API Key)](#tab/python-key)

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=os.getenv("AZURE_OPENAI_API_KEY"), 

)

response = client.chat.completions.retrieve("chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u")

print(response.model_dump_json(indent=2))
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
```

### API Key

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
```

# [Output](#tab/output)

```json
{
  "id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u",
  "choices": [
    {
      "finish_reason": null,
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Ensemble methods enhance machine learning performance by combining multiple models to create a more robust and accurate predictor. The key techniques include:\n\n1. **Bagging (Bootstrap Aggregating):** This involves training models on random subsets of the data to reduce variance and prevent overfitting. Random Forests, a popular bagging method, build multiple decision trees using random feature subsets, leading to robust predictions.\n\n2. **Boosting:** This sequential approach trains models to correct the errors of their predecessors, thereby focusing on difficult-to-predict data points. Gradient Boosting is a common implementation that sequentially builds decision trees, each improving upon the prediction errors of the previous ones.\n\n3. **Stacking:** This technique uses a meta-model to combine the predictions of multiple base models, leveraging their diverse strengths to enhance overall prediction accuracy.\n\nThe practical implications of ensemble methods include achieving superior model performance compared to single models by capturing various data patterns and reducing overfitting and variance. These methods are widely used in applications where high accuracy and model reliability are critical.",
        "refusal": null,
        "role": "assistant",
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1740447656,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_b705f0c291",
  "usage": {
    "completion_tokens": 208,
    "prompt_tokens": 157,
    "total_tokens": 365,
    "completion_tokens_details": null,
    "prompt_tokens_details": null
  },
  "request_id": "0000aaaa-11bb-cccc-dd22-eeeeee333333",
  "seed": -430976584126747957,
  "top_p": 1,
  "temperature": 1,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "metadata": {
    "user": "admin",
    "category": "docs-test"
  }
}
```

---

### Get stored chat completion messages

Additional parameters:

* `after`: Identifier for the last stored completion message from the previous pagination request.
* `limit`: Number of stored completions messages to retrieve.
* `order`: Order of the results by index (ascending or descending).

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider,
)

response = client.chat.completions.messages.list("chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u", limit=2)

print(response.model_dump_json(indent=2))
```

# [Python (API Key)](#tab/python-key)

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/", 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
)

response = client.chat.completions.messages.list("chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u", limit=2)

print(response.model_dump_json(indent=2))
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
```

### API Key

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u/messages \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
```

# [Output](#tab/output)

```json
{
  "data": [
    {
      "content": "Provide a clear and concise summary of the technical content, highlighting key concepts and their relationships. Focus on the main ideas and practical implications.",
      "refusal": null,
      "role": "system",
      "audio": null,
      "function_call": null,
      "tool_calls": null,
      "id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u-0"
    },
    {
      "content": "Ensemble methods combine multiple machine learning models to create a more robust and accurate predictor. Common techniques include bagging (training models on random subsets of data), boosting (sequentially training models to correct previous errors), and stacking (using a meta-model to combine base model predictions). Random Forests, a popular bagging method, create multiple decision trees using random feature subsets. Gradient Boosting builds trees sequentially, with each tree focusing on correcting the errors of previous trees. These methods often achieve better performance than single models by reducing overfitting and variance while capturing different aspects of the data.",
      "refusal": null,
      "role": "user",
      "audio": null,
      "function_call": null,
      "tool_calls": null,
      "id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u-1"
    }
  ],
  "has_more": false,
  "object": "list",
  "total": 2,
  "first_id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u-0",
  "last_id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u-1"
}
```

---

### Update stored chat completion

Add metadata key:value pairs to an existing stored completion.

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider,
)

response = client.chat.completions.update(
    "chatcmpl-C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1w",
    metadata={"fizz": "buzz"}
)

print(response.model_dump_json(indent=2))
```

# [Python (API Key)](#tab/python-key)

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/", 
  api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.chat.completions.update(
    "chatcmpl-C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1w",
    metadata={"fizz": "buzz"}
)

print(response.model_dump_json(indent=2))
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl -X https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
  -d '{
    "metadata": {
      "fizz": "buzz"
    }
  }' 
```

### API Key

```bash
curl -X https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
  -d '{
    "metadata": {
      "fizz": "buzz"
    }
  }'
```

# [Output](#tab/output)

```json
  "id": "chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u",
  "choices": [
    {
      "finish_reason": null,
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Ensemble methods enhance machine learning performance by combining multiple models to create a more robust and accurate predictor. The key techniques include:\n\n1. **Bagging (Bootstrap Aggregating):** This involves training models on random subsets of the data to reduce variance and prevent overfitting. Random Forests, a popular bagging method, build multiple decision trees using random feature subsets, leading to robust predictions.\n\n2. **Boosting:** This sequential approach trains models to correct the errors of their predecessors, thereby focusing on difficult-to-predict data points. Gradient Boosting is a common implementation that sequentially builds decision trees, each improving upon the prediction errors of the previous ones.\n\n3. **Stacking:** This technique uses a meta-model to combine the predictions of multiple base models, leveraging their diverse strengths to enhance overall prediction accuracy.\n\nThe practical implications of ensemble methods include achieving superior model performance compared to single models by capturing various data patterns and reducing overfitting and variance. These methods are widely used in applications where high accuracy and model reliability are critical.",
        "refusal": null,
        "role": "assistant",
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1740447656,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_b705f0c291",
  "usage": {
    "completion_tokens": 208,
    "prompt_tokens": 157,
    "total_tokens": 365,
    "completion_tokens_details": null,
    "prompt_tokens_details": null
  },
  "request_id": "0000aaaa-11bb-cccc-dd22-eeeeee333333",
  "seed": -430976584126747957,
  "top_p": 1,
  "temperature": 1,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "metadata": {
    "user": "admin",
    "category": "docs-test"
    "fizz": "buzz"
  }
}
```

---

### Delete stored chat completion

Delete stored completion by completion ID.

### Microsoft Entra ID

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider
)

response = client.chat.completions.delete("chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u")

print(response.model_dump_json(indent=2))

```

# [Python (API Key)](#tab/python-key)

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/", 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
)

response = client.chat.completions.delete("chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u")

print(response.model_dump_json(indent=2))
```

# [REST API](#tab/rest-api)

```bash
curl -X DELETE -D - https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
```

### API Key

```bash
curl -X DELETE -D - https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/chatcmpl-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

# [Output](#tab/output)

```json
"id"• "chatcmp1-A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u", 
"deleted": true, 
"object": "chat. completion. deleted" 
```

---

## Troubleshooting

### Do I need special permissions to use stored completions?

Stored completions access is controlled via two DataActions:

- `Microsoft.CognitiveServices/accounts/OpenAI/stored-completions/read`
- `Microsoft.CognitiveServices/accounts/OpenAI/stored-completions/action`

By default `Azure AI User` role has access to both these permissions:

:::image type="content" source="../media/stored-completions/permissions.png" alt-text="Screenshot of stored completions permissions." lightbox="../media/stored-completions/permissions.png":::

### How do I delete stored data?

Data can be deleted by deleting the associated Azure OpenAI resource. If you wish to only delete stored completion data you must open a case with customer support.

### How much stored completion data can I store?

You can store a maximum 10 GB of data.

### Can I prevent stored completions in my project?

Users of Azure OpenAI resources can disable stored completions within the Azure portal. Within the Azure OpenAI resource, navigate to the Stored Completions panel in the Resource Management view. Toggle the Stored Completions control to Disabled and click Save.

Users of Foundry resources must open a case with customer support to disable Stored Completions at the Azure subscription level.

### TypeError: Completions.create() got an unexpected argument 'store'

This error occurs when you're running an older version of the OpenAI client library that predates the stored completions feature being released. Run  `pip install openai --upgrade`.
