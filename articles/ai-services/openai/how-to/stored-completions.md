---
title: 'How to use Azure OpenAI Service stored completions & distillation'
titleSuffix: Azure OpenAI
description: Learn how to use stored completions & distillation with Azure OpenAI
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.custom: references_regions
ms.date: 12/12/2024
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Azure OpenAI stored completions & distillation (preview)

Stored completions allow you to capture the conversation history from chat completions sessions to use as datasets for [evaluations](./evaluations.md) and [fine-tuning](./fine-tuning.md).

## Stored completions support

### API support

- `2024-10-01-preview`

### Model support

- `gpt-4o-2024-08-06`

### Regional availability

- Sweden Central

## Configure stored completions

To enable stored completions for your Azure OpenAI deployment set the `store` parameter to `True`. Use the `metadata` parameter to enrich your stored completion dataset with additional information.


# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2024-10-01-preview"
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
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-10-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

ompletion = client.chat.completions.create(
    
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
---

Once stored completions are enabled for an Azure OpenAI deployment, they'll begin to show up in the [Azure AI Foundry portal](https://oai.azure.com) in the **Stored Completions** pane.

:::image type="content" source="../media/stored-completions/stored-completions.png" alt-text="Screenshot of the stored completions User Experience." lightbox="../media/stored-completions/stored-completions.png":::

## Distillation

Distillation allows you to turn your stored completions into a fine-tuning dataset. A common use case is to use stored completions with a larger more powerful model for a particular task and then use the stored completions to train a smaller model on high quality examples of model interactions.

Distillation requires a minimum of 10 stored completions, though it's recommended to provide hundreds to thousands of stored completions for the best results.

1. From the **Stored Completions** pane in the [Azure AI Foundry portal](https://oai.azure.com) use the **Filter** options to select the completions you want to train your model with.

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

1. From the **Stored Completions** pane in the [Azure AI Foundry portal](https://oai.azure.com) use the **Filter** options to select the completions you want to be part of your evaluation dataset.

2. To configure the evaluation, select **Evaluate**

    :::image type="content" source="../media/stored-completions/evaluate.png" alt-text="Screenshot of the stored completion pane with evaluate selected." lightbox="../media/stored-completions/evaluate.png":::

3. This launches the **Evaluations** pane with a prepopulated `.jsonl` file with a randomly generated name that is created as an evaluation dataset from your stored completions.

    > [!Note]
    > Stored completion evaluation data files cannot be accessed directly and cannot be exported externally/downloaded.

    :::image type="content" source="../media/stored-completions/evaluation-data.png" alt-text="Screenshot of the evaluations pane." lightbox="../media/stored-completions/evaluation-data.png":::

To learn more about evaluation see, [getting started with evaluations](./evaluations.md)

## Troubleshooting

### Do I need special permissions to use stored completions?

Stored completions access is controlled via two DataActions:

- `Microsoft.CognitiveServices/accounts/OpenAI/stored-completions/read`
- `Microsoft.CognitiveServices/accounts/OpenAI/stored-completions/action`

By default `Cognitive Services OpenAI Contributor` has access to both these permissions:

:::image type="content" source="../media/stored-completions/permissions.png" alt-text="Screenshot of stored completions permissions." lightbox="../media/stored-completions/permissions.png":::

### How do I delete stored data?

Data can be deleted by deleting the associated Azure OpenAI resource. If you wish to only delete stored completion data you must open a case with customer support.

### How much stored completion data can I store?

You can store a maximum 10 GB of data.

### Can I prevent stored completions from ever being enabled on a subscription?

You'll need to open a case with customer support to disable stored completions at the subscription level.

### TypeError: Completions.create() got an unexpected argument 'store'

This error occurs when you're running an older version of the OpenAI client library that predates the stored completions feature being released. Run  `pip install openai --upgrade`.

