---
title: How to use model router in Azure OpenAI Service
titleSuffix: Azure OpenAI Service
description: Learn how to use the model router in Azure OpenAI Service to select the best model for your task.
author: PatrickFarley
ms.author: pafarley 
#customer intent: 
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 04/17/2025
manager: nitinme
---

# Use model router

Azure OpenAI model router is a deployable AI chat model that automatically selects the best underlying chat model to respond to a given prompt. It uses a combination of preexisting models to provide high performance while saving on compute costs where possible. For more information on how model router works and its advantages and limitations, see the [Model router concepts guide](../concepts/model-router.md).

You can access model router through the Completions API just as you would use a single base model like GPT-4.

## Deploy a model router model

Model router is packaged as a single OpenAI model that you deploy. Follow the steps in the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource), and in the **Create new deployment** step, find `Azure OpenAI model router` in the **Model** list. Select it, and then complete the rest of the deployment steps.

> [!NOTE]
> Consider that your deployment settings apply to all underlying chat models that model router uses.
> - You don't need to deploy the underlying chat models separately. Model router works independently of your other deployed models.
> - You select a content filter when you deploy the model router model (or you can apply a filter later). The content filter is applied to all activity to and from the model router: you don't set content filters for each of the underlying chat models.
> - Your tokens-per-minute rate limit setting is applied to all activity to and from the model router: you don't set rate limits for each of the underlying chat models.

## Use model router in chat

### REST API

> [!IMPORTANT]
> Set temperature and top_p to the values you prefer, but note that reasoning models (o-series) don't support these parameters. If model router selects a reasoning model for your prompt, it will drop the temperature and top_p input parameters. TBD

> [!IMPORTANT]
> The reasoning parameter is not supported in model router. If model router selects a reasoning model for your prompt, it will also select a value for the reasoning parameter based on TBD

### Portal

Playground .  in the conversation it displays the underlying model version of each response TBD

## Evaluate model router performance


you can create a custom metric, and submit a job to compare the router to other models. then in foundry portal you can compare the performances. 

We provide custom metric test via notebooks.
in azmon, you can monitor all the standard metrics
cost analysis page (only in the azure portal). it will show the costs of each underlying model. (no extra charges for model router, above the underlying charges)

## Troubleshooting
