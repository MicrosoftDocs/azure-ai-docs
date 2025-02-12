---
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 02/11/2025
ms.author: jboback
ms.custom: language-service-pii
---

## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* A [conversational language understanding](../../../conversational-language-understanding/quickstart.md) project.



## Sign in to Language Studio

[!INCLUDE [Sign in to Language studio](../language-studio/sign-in-studio.md)]







## Train your model
 
To train a model, you need to start a training job. The output of a successful training job is your trained model.

[!INCLUDE [Train model](../language-studio/train-model.md)]



## Deploy your model

Generally after training a model you would review its evaluation details. In this quickstart, you will just deploy your model, and make it available for you to try in Language Studio, or you can call the [prediction API](https://aka.ms/clu-apis).

[!INCLUDE [Deploy model](../language-studio/deploy-model.md)]



## Test model

After your model is deployed, you can start using it to make predictions through [Prediction API](https://aka.ms/clu-apis). For this quickstart, you will use the [Language Studio](https://aka.ms/LanguageStudio) to submit an utterance, get predictions and visualize the results.


[!INCLUDE [Test model](../language-studio/test-model.md)]



## Clean up resources

[!INCLUDE [Delete project using Language studio](../language-studio/delete-project.md)]