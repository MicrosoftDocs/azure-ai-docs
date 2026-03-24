---
title: Include file
description: Include file
author: msakande
ms.reviewer: rasavage
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

In this tutorial, you learn how to deploy and use a DeepSeek reasoning model in Microsoft Foundry. This tutorial uses [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek?cid=learnDocs) for illustration. However, the content also applies to the newer [DeepSeek-R1-0528](https://ai.azure.com/explore/models/deepseek-r1-0528/version/1/registry/azureml-deepseek?cid=learnDocs) reasoning model.

**What you accomplish:**

In this tutorial, you deploy the DeepSeek-R1 reasoning model, send inference requests programmatically using code, and parse the reasoning output to understand how the model arrives at its answers.

The steps you perform in this tutorial are:

* Create and configure the Azure resources to use DeepSeek-R1 in Foundry Models.
* Configure the model deployment.
* Use DeepSeek-R1 with the next generation v1 Azure OpenAI APIs to consume the model in code.

## Prerequisites

To complete this article, you need:

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. If you're using GitHub Models, you can [upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) and create an Azure subscription in the process.

- Access to Microsoft Foundry with appropriate permissions to create and manage resources. Typically requires Contributor or Owner role on the resource group for creating resources and deploying models.

- The **Cognitive Services User** role (or higher) assigned to your Azure account on the Foundry resource. This role is required to make inference calls with Microsoft Entra ID. Assign it in the Azure portal under **Access Control (IAM)** on the Foundry resource.

- Install the Azure OpenAI SDK for your programming language:
  - **Python**: `pip install openai azure-identity`
  - **.NET**: `dotnet add package OpenAI` and `dotnet add package Azure.Identity`
  - **JavaScript**: `npm install openai @azure/identity`
  - **Java**: Add the `com.openai:openai-java` and `com.azure:azure-identity` packages

DeepSeek-R1 is a reasoning model that generates explanations alongside answers. It supports text-based chat completions but doesn't support tool calling or structured output formats. See [About reasoning models](#about-reasoning-models) for details.
