---
title: Custom text classification FAQ
titleSuffix: Foundry Tools
description: Learn about Frequently asked questions when using the custom text classification API.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: faq
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification
---
# Frequently asked questions

Find answers to commonly asked questions about concepts, and scenarios related to custom text classification in Azure Language in Foundry Tools.

## How do I get started with the service?

See the [quickstart](./quickstart.md) to quickly create your first project, or view [how to create projects](how-to/create-project.md).

## What are the service limits?

See the [service limits article](service-limits.md).

## Which languages are supported?

See the [language support](./language-support.md) article.

## How many tagged files are needed?

Generally, diverse and representative [tagged data](how-to/tag-data.md) leads to better results, given that the tagging is done precisely, consistently and completely. There's no set number of tagged classes that make every model perform well. Performance is highly dependent on your schema and the ambiguity of your schema. Ambiguous classes need more tags. Performance also depends on the quality of your tagging. The recommended number of tagged instances per class is 50. 

## Training is taking a long time, is it to be expected?

The training process can take some time. As a rough estimate, the expected training time for files with a combined length of 12,800,000 chars is 6 hours.

## How do I build my custom model programmatically?

You can use the [REST APIs](https://westus.dev.cognitive.microsoft.com/docs/services/language-authoring-clu-apis-2022-03-01-preview/operations/Projects_TriggerImportProjectJob) to build your custom models. Follow this [quickstart](quickstart.md?pivots=rest-api) to get started with creating a project and creating a model through APIs for examples of how to call the Authoring API. 

When you're ready to start [using your model to make predictions](#how-do-i-use-my-trained-model-to-make-predictions), you can use the REST API, or the client library.

## What is the recommended CI/CD process?

You can train multiple models on the same dataset within the same project. After you train your model successfully, you can [view its evaluation](how-to/view-model-evaluation.md). You can [deploy and test](quickstart.md#deploy-your-model) your model within [Microsoft Foundry](https://ai.azure.com/). You can add or remove tags from your data and train a **new** model and test it as well. View [service limits](service-limits.md)to learn about maximum number of trained models with the same project. When you [tag your data](how-to/tag-data.md#label-your-data), you can determine how your dataset is split into training and testing sets.

## Does a low or high model score guarantee bad or good performance in production?

Model evaluation may not always be comprehensive, depending on: 
* If the **test set** is too small, the good/bad scores aren't representative of model's actual performance. Also if a specific class is missing or under-represented in your test set it affects model performance.
* **Data diversity** if your data only covers few scenarios/examples of the text you expect in production, your model isn't exposed to all possible scenarios and might perform poorly on the scenarios it isn't trained on.
* **Data representation** if the dataset used to train the model isn't representative of the data that would be introduced to the model in production, model performance is affected greatly.

See the [data selection and schema design](how-to/design-schema.md) article.

## How do I improve model performance?

* View the model [confusion matrix](how-to/view-model-evaluation.md), if you notice that a certain class is frequently classified incorrectly, consider adding more tagged instances for this class. If you notice that two classes are frequently classified as each other, it means the schema is ambiguous, consider merging them both into one class for better performance.

*  [Examine Data distribution](concepts/evaluation-metrics.md) If one of the classes has many more tagged instances than the others, your model may be biased towards this class. Add more data to the other classes or remove most of the examples from the dominating class. 

* Review the [data selection and schema design](how-to/design-schema.md) article.

* [Review your test set](how-to/view-model-evaluation.md) to see predicted and tagged classes side-by-side. Then you can get a better idea of your model performance, and decide if any changes in the schema or the tags are necessary.

## When I retrain my model, I get different results. Why?

* When you [tag your data](how-to/tag-data.md#label-your-data), you can determine how your dataset is split into training and testing sets. You can also have your data split randomly into training and testing sets. However, there's no guarantee that the reflected model evaluation is on the same test set, so results aren't comparable.

* If you're retraining the same model, your test set is the same, but you might notice a slight change in predictions made by the model. It's because the trained model isn't robust enough, which is a factor of how representative and distinct your data is, and the quality of your tagged data. 

## How do I get predictions in different languages?

First, you need to enable the multilingual option when [creating your project](how-to/create-project.md) or you can enable it later from the project settings page. After you train and deploy your model, you can start querying it in multiple languages. You may get varied results for different languages. To improve the accuracy of any language, add more tagged instances to your project in that language to introduce the trained model to more syntax of that language. See [language support](language-support.md#multi-lingual-option).

## I trained my model, but I can't test it 

You need to [deploy your model](quickstart.md#deploy-your-model) before you can test it. 

## How do I use my trained model to make predictions?

After deploying your model, you [call the prediction API](how-to/call-api.md), using either the [REST API](how-to/call-api.md?tabs=rest-api) or [client libraries](how-to/call-api.md?tabs=client).

## Data privacy and security

For more information, *see* [Data, privacy, and security for Azure Language in Foundry Tools](/azure/ai-foundry/responsible-ai/language-service/data-privacy).

## How to clone my project?

To clone your project, you need to use the export API  to export the project assets, and then import them into a new project. See [REST APIs](https://westus.dev.cognitive.microsoft.com/docs/services/language-authoring-clu-apis-2022-03-01-preview/operations/Projects_TriggerImportProjectJob) reference for both operations.

## Next steps

* [Custom text classification overview](overview.md)
* [Quickstart](quickstart.md)
