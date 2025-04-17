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
> You don't need to deploy the underlying models separately. Model router works independently of your other deployed models.

## Use model router in chat

### REST API


### Portal 

## Evaluate model router performance

## Troubleshooting
