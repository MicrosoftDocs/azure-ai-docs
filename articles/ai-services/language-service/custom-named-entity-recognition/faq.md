---
title: Custom Named Entity Recognition (NER) FAQ
titleSuffix: Foundry Tools
description: Learn about Frequently asked questions when using custom Named Entity Recognition.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: faq
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner
---
# Frequently asked questions for Custom Named Entity Recognition

Find answers to commonly asked questions about concepts, and scenarios related to custom NER in Azure Language in Foundry Tools.

## How do I get started with the service?

For more information, *see* our [quickstart](./quickstart.md) or [how to create projects](how-to/create-project.md).

## What are the service limits?

For more information, *see* [service limits](service-limits.md).

## How many tagged files are needed?

Generally, diverse and representative [tagged data](how-to/tag-data.md) leads to better results, given that the tagging is done precisely, consistently and completely. There's no set number of tagged instances for a model to perform well. Performance highly dependent on your schema, and the ambiguity of your schema. Ambiguous entity types need more tags. Performance also depends on the quality of your tagging. The recommended number of tagged instances per entity is 50.

## How long should it take to train a model?

The training process can take a long time. As a rough estimate, the expected training time for files with a combined length of 12,800,000 chars is 6 hours.

## How do I build my custom model programmatically?

[!INCLUDE [SDK limitations](includes/sdk-limitations.md)]

You can use the [REST APIs](https://westus.dev.cognitive.microsoft.com/docs/services/language-authoring-clu-apis-2022-03-01-preview/operations/Projects_TriggerImportProjectJob) to build your custom models. Follow this [quickstart](quickstart.md?pivots=rest-api) to get started with creating a project and creating a model through APIs for examples of how to call the Authoring API.

When you're ready to start [using your model to make predictions](#how-do-i-use-my-trained-model-for-predictions), you can use the REST API, or the client library.

## What is the recommended CI/CD process?

Here's a list of actions you take within [Microsoft Foundry](https://ai.azure.com/):

* Train multiple models on the same dataset within a single project.
* View your model's performance.
* Deploy and test your model and add or remove labels from your data.
* Choose how your dataset is split into training and testing sets.<br><br> 

Your data can be split randomly into training and testing sets, but this means model evaluation may not be based on the same test set, making results noncomparable. We recommended that you develop your own test set and use it to evaluate both models to accurately measure improvements.<br><br> 

Make sure to review service limits to understand the maximum number of trained models allowed per project.

## Does a low or high model score guarantee bad or good performance in production?

Model evaluation may not always be comprehensive. The scope depends on the following factors:

* The size of the **test set**. If the test set is too small, the good/bad scores aren't as representative of model's actual performance. Also if a specific entity type is missing or under-represented in your test set it affects model performance.
* The **diversity of your data**. If your data only includes a limited number of scenarios or examples of the text you anticipate in production, your model may not encounter every possible situation. As a result, the model could perform poorly when faced with unfamiliar scenarios.
* The **representation within your data**. If the dataset used to train the model isn't representative of the data that would be introduced to the model in production, model performance is affected greatly.

For more information, *see* [data selection and schema design](how-to/design-schema.md).

## How do I improve model performance?

* View the model [confusion matrix](how-to/view-model-evaluation.md). If you notice that a certain entity type is frequently not predicted correctly, consider adding more tagged instances for this class. 

When two different entity types are often being predicted as one another, it indicates that the schema lacks clarity. To improve performance, you should think about combining these two entity types into a single, unified type. If two entity types are consistently mistaken for each other during prediction, this result suggests ambiguity in your schema. Merging them into one entity type can help enhance overall model accuracy.

* [Review test set predictions](how-to/view-model-evaluation.md). If one of the entity types has a lot more tagged instances than the others, your model may be biased towards this type. Add more data to the other entity types or remove examples from the dominating type.

* Learn more about [data selection and schema design](how-to/design-schema.md).

* [Review your test set](how-to/view-model-evaluation.md). Review the predicted entities alongside the tagged entities and gain a clearer understanding of your model's accuracy. This comparison can help you determine whether adjustments to the schema or tag set are needed.

## Why do I get different results when I retrain my model?

* When you [train your model](how-to/train-model.md), you can determine if you want your data to be split randomly into train and test sets. If you choose to proceed, there's no assurance that the model evaluation is performed on the same test set, which means the results may not be directly comparable. By doing so, you risk evaluating the model on a different test set, making it impossible to reliably compare the outcomes.


* If you're retraining the same model, your test set is the same, but you might notice a slight change in predictions made by the model. The issue arises because the trained model lacks sufficient robustness. This outcome is dependent on how well your data represents different scenarios, how distinct the data points are, and the overall quality of your data tagging. Several factors influence the model's performance. The model's robustness, the distinctiveness and diversity of the dataset, and the precision and uniformity of the tags assigned to the data all play important roles. To achieve optimal results, you must ensure your dataset not only accurately represents the target domain but also offers unique examples, and that all tags are applied with both consistency and accuracy throughout the data.


## How do I get predictions in different languages?

First, you need to enable the multilingual option when [creating your project](how-to/create-project.md) or you can enable it later from the project settings page. After you train and deploy your model, you can start querying it in [multiple languages](language-support.md#multi-lingual-option). You may get varied results for different languages. To improve the accuracy of any language, add more tagged instances to your project in that language to introduce the trained model to more syntax of that language.

## I trained my model, but I can't test it

You need to [deploy your model](quickstart.md#deploy-your-model) before you can test it. 

## How do I use my trained model for predictions?

After deploying your model, you [call the prediction API](how-to/call-api.md), using either the [REST API](how-to/call-api.md?tabs=rest-api) or [client libraries](how-to/call-api.md?tabs=client).

## Data privacy and security

Your data is only stored in your Azure Storage account. Custom NER only has access to read from it during training. Custom NER users have full control to view, export, or delete any user content either through the [Foundry](https://ai.azure.com/) or programmatically by using [REST APIs](https://westus.dev.cognitive.microsoft.com/docs/services/language-authoring-clu-apis-2022-03-01-preview/operations/Projects_TriggerImportProjectJob). For more information, *see* [Data, privacy, and security for Language](/azure/ai-foundry/responsible-ai/language-service/data-privacy)


## How to clone my project?

To clone your project, you need to use the export API  to export the project assets, and then import them into a new project. See the [REST API](https://westus.dev.cognitive.microsoft.com/docs/services/language-authoring-clu-apis-2022-03-01-preview/operations/Projects_TriggerImportProjectJob) reference for both operations.

## Next steps

* [Custom NER overview](overview.md)
* [Quickstart](quickstart.md)
