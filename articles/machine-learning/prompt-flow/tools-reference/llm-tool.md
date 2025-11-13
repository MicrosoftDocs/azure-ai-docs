---
title: LLM tool in Azure Machine Learning prompt flow
titleSuffix: Azure Machine Learning
description: The prompt flow LLM tool enables you to take advantage of widely used large language models like OpenAI or Azure OpenAI for natural language processing.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
ms.topic: reference
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 07/17/2025

ms.update-cycle: 365-days
---

# LLM tool

The large language model (LLM) tool in prompt flow enables you to use widely used large language models like [OpenAI](https://platform.openai.com/), [Azure OpenAI in Microsoft Foundry Models](../../../ai-foundry/openai/overview.md), or any language model supported by the [Azure AI model inference API](https://aka.ms/azureai/modelinference) for natural language processing.

Prompt flow provides several large language model APIs:

- [Completion](https://platform.openai.com/docs/api-reference/completions): OpenAI's completion models generate text based on provided prompts.
- [Chat](https://platform.openai.com/docs/api-reference/chat): OpenAI's chat models and the [Azure AI](https://aka.ms/azureai/modelinference) chat models facilitate interactive conversations with text-based inputs and responses.

The [Embeddings](https://platform.openai.com/docs/api-reference/embeddings) API isn't available in the LLM tool. Use the [embedding tool](embedding-tool.md) to generate embeddings with OpenAI or Azure OpenAI.

> [!NOTE]
> The LLM tool in prompt flow does not support reasoning models (such as OpenAI o1 or o3). For reasoning model integration, use the Python tool to call the model APIs directly. For more information, see [Call a reasoning model from the Python tool](python-tool.md#call-a-reasoning-model-from-the-python-tool).

## Prerequisites

Create OpenAI resources:

- **OpenAI**:

    - Sign up for an account on the [OpenAI website](https://openai.com/).
    - Sign in and [find your personal API key](https://platform.openai.com/account/api-keys).

- **Azure OpenAI**:

    - Create Azure OpenAI resources by following [these instructions](../../../ai-foundry/openai/how-to/create-resource.md). Use only ASCII characters in Azure OpenAI resource group names. Prompt flow doesn't support non-ASCII characters in resource group names.

- **Models deployed to standard deployments**:

  - Create an endpoint with the model from the catalog you want and [deploy it with a standard deployment](../../how-to-deploy-models-serverless.md).
  - To use models deployed to standard deployment supported by the [Azure AI model inference API](https://aka.ms/azureai/modelinference), like Mistral, Cohere, Meta Llama, or Microsoft family of models (among others), [create a connection in your project to your endpoint](../../how-to-connect-models-serverless.md?#create-a-standard-deployment-connection).

## Connections

Set up connections to provisioned resources in prompt flow.

| Type                                | Name     | API key  | API type | API version |
|-------------------------------------|----------|----------|----------|-------------|
| OpenAI                              | Required | Required | -        | -           |
| Azure OpenAI - API key             | Required | Required | Required | Required    |
| Azure OpenAI - Microsoft Entra ID  | Required | -        | -        | Required    |
| Serverless model                    | Required | Required | -        | -           |

  > [!TIP]
  > - To use Microsoft Entra ID auth type for Azure OpenAI connection, assign either the `Cognitive Services OpenAI User` or `Cognitive Services OpenAI Contributor` role to the user or user-assigned managed identity.
  > - Learn more about [how to specify to use user identity to submit flow run](../how-to-create-manage-runtime.md#create-an-automatic-runtime-preview-on-a-flow-page).
  > - Learn more about [how to configure Azure OpenAI with managed identities](../../../ai-foundry/openai/how-to/managed-identity.md).

## Inputs

The following sections show various inputs.

### Text completion

| Name                   | Type       | Description                                                                               | Required |
|------------------------|------------|-------------------------------------------------------------------------------------------|----------|
| prompt                 | string     | Text prompt for the language model.                                                      | Yes      |
| model, deployment_name | string     | Language model to use.                                                                    | Yes      |
| max\_tokens            | integer    | Maximum number of tokens to generate in the completion. Default is 16.                   | No       |
| temperature            | float      | Randomness of the generated text. Default is 1.                                          | No       |
| stop                   | list       | Stopping sequence for the generated text. Default is null.                               | No       |
| suffix                 | string     | Text appended to the end of the completion.                                               | No       |
| top_p                  | float      | Probability of using the top choice from the generated tokens. Default is 1.             | No       |
| logprobs               | integer    | Number of log probabilities to generate. Default is null.                                | No       |
| echo                   | boolean    | Value that indicates whether to echo back the prompt in the response. Default is false.  | No       |
| presence\_penalty      | float      | Value that controls the model's behavior for repeating phrases. Default is 0.            | No       |
| frequency\_penalty     | float      | Value that controls the model's behavior for generating rare phrases. Default is 0.      | No       |
| best\_of               | integer    | Number of best completions to generate. Default is 1.                                    | No       |
| logit\_bias            | dictionary | Logit bias for the language model. Default is an empty dictionary.                       | No       |

### Chat

| Name                   | Type       | Description                                                                                      | Required |
|------------------------|------------|--------------------------------------------------------------------------------------------------|----------|
| prompt                 | string     | Text prompt that the language model uses for a response.                                        | Yes      |
| model, deployment_name | string     | Language model to use. This parameter isn't required if the model is deployed to a standard deployment. | Yes*     |
| max\_tokens            | integer    | Maximum number of tokens to generate in the response. Default is inf.                           | No       |
| temperature            | float      | Randomness of the generated text. Default is 1.                                                 | No       |
| stop                   | list       | Stopping sequence for the generated text. Default is null.                                      | No       |
| top_p                  | float      | Probability of using the top choice from the generated tokens. Default is 1.                    | No       |
| presence\_penalty      | float      | Value that controls the model's behavior for repeating phrases. Default is 0.                   | No       |
| frequency\_penalty     | float      | Value that controls the model's behavior for generating rare phrases. Default is 0.             | No       |
| logit\_bias            | dictionary | Logit bias for the language model. Default is an empty dictionary.                              | No       |

## Outputs

| API        | Return type | Description                              |
|------------|-------------|------------------------------------------|
| Completion | string      | Text of one predicted completion         |
| Chat       | string      | Text of one response of conversation     |

## Use the LLM tool

1. Set up and select the connections to OpenAI resources or to a standard deployment.
1. Configure the large language model API and its parameters.
1. Prepare the prompt with [guidance](prompt-tool.md#write-a-prompt).
