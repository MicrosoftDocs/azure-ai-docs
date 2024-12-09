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
ms.reviewer: keli19
ms.date: 11/02/2023
---

# LLM tool

The large language model (LLM) tool in prompt flow enables you to take advantage of widely used large language models like [OpenAI](https://platform.openai.com/), or [Azure OpenAI Service](../../../ai-services/openai/overview.md), or any language model supported by the [Azure AI model inference API](https://aka.ms/azureai/modelinference) for natural language processing.

Prompt flow provides a few different large language model APIs:

- [Completion](https://platform.openai.com/docs/api-reference/completions): OpenAI's completion models generate text based on provided prompts. 
- [Chat](https://platform.openai.com/docs/api-reference/chat): OpenAI's chat models and the [Azure AI](https://aka.ms/azureai/modelinference) chat models facilitate interactive conversations with text-based inputs and responses.

> [!NOTE]
> We removed the `embedding` option from the LLM tool API setting. You can use an embedding API with the [embedding tool](embedding-tool.md).
> Only key-based authentication is supported for Azure OpenAI connection.
> Please don't use non-ascii characters in resource group name of Azure OpenAI resource, prompt flow didn't support this case.

## Prerequisites

Create OpenAI resources:

- **OpenAI**:

    - Sign up your account on the [OpenAI website](https://openai.com/).
    - Sign in and [find your personal API key](https://platform.openai.com/account/api-keys).

- **Azure OpenAI**:

    - Create Azure OpenAI resources with [these instructions](../../../ai-services/openai/how-to/create-resource.md).

- **Models deployed to Serverless API endpoints**

  - Create an endpoint with the model from the catalog you are interested [and deploy it with a serverless API endpoint](../../how-to-deploy-models-serverless.md).
  - To use models deployed to serverless API endpoints supported by the [Azure AI model inference API](https://aka.ms/azureai/modelinference), like Mistral, Cohere, Meta Llama, or Microsoft family of models (among others), you need to [create a connection in your project to your endpoint](../../how-to-connect-models-serverless.md?#create-a-serverless-api-endpoint-connection)

## Connections

Set up connections to provisioned resources in prompt flow.

| Type        | Name     | API key  | API type | API version |
|-------------|----------|----------|----------|-------------|
| OpenAI      | Required | Required | -        | -           |
| Azure OpenAI - API key| Required | Required | Required | Required    |
| Azure OpenAI - Microsoft Entra ID| Required | - | - | Required    |
| Serverless model | Required | Required | - | - |

  > [!TIP]
  > - To use Microsoft Entra ID auth type for Azure OpenAI connection, you need assign either the `Cognitive Services OpenAI User` or `Cognitive Services OpenAI Contributor role` to user or user assigned managed identity.
  > - Learn more about [how to specify to use user identity to submit flow run](../how-to-create-manage-runtime.md#create-an-automatic-runtime-preview-on-a-flow-page).
  > - Learn more about [How to configure Azure OpenAI Service with managed identities](../../../ai-services/openai/how-to/managed-identity.md).

## Inputs

The following sections show various inputs.

### Text completion

| Name                   | Type        | Description                                                                             | Required |
|------------------------|-------------|-----------------------------------------------------------------------------------------|----------|
| prompt                 | string      | Text prompt for the language model.                                     | Yes      |
| model, deployment_name | string      | Language model to use.                                                               | Yes      |
| max\_tokens            | integer     | Maximum number of tokens to generate in the completion. Default is 16.              | No       |
| temperature            | float       | Randomness of the generated text. Default is 1.                                     | No       |
| stop                   | list        | Stopping sequence for the generated text. Default is null.                          | No       |
| suffix                 | string      | Text appended to the end of the completion.                                              | No       |
| top_p                  | float       | Probability of using the top choice from the generated tokens. Default is 1.        | No       |
| logprobs               | integer     | Number of log probabilities to generate. Default is null.                           | No       |
| echo                   | boolean     | Value that indicates whether to echo back the prompt in the response. Default is false. | No       |
| presence\_penalty      | float       | Value that controls the model's behavior for repeating phrases. Default is 0.                              | No       |
| frequency\_penalty     | float       | Value that controls the model's behavior for generating rare phrases. Default is 0.                             | No       |
| best\_of               | integer     | Number of best completions to generate. Default is 1.                               | No       |
| logit\_bias            | dictionary  | Logit bias for the language model. Default is an empty dictionary.                     | No       |

### Chat

| Name                   | Type        | Description                                                                                    | Required |
|------------------------|-------------|------------------------------------------------------------------------------------------------|----------|
| prompt                 | string      | Text prompt that the language model uses for a response.                                              | Yes      |
| model, deployment_name | string      | Language model to use. This parameter is not required if the model is deployed to a serverless API endpoint.  | Yes*      |
| max\_tokens            | integer     | Maximum number of tokens to generate in the response. Default is inf.                      | No       |
| temperature            | float       | Randomness of the generated text. Default is 1.                                            | No       |
| stop                   | list        | Stopping sequence for the generated text. Default is null.                                 | No       |
| top_p                  | float       | Probability of using the top choice from the generated tokens. Default is 1.               | No       |
| presence\_penalty      | float       | Value that controls the model's behavior for repeating phrases. Default is 0.      | No       |
| frequency\_penalty     | float       | Value that controls the model's behavior for generating rare phrases. Default is 0. | No       |
| logit\_bias            | dictionary  | Logit bias for the language model. Default is an empty dictionary.                            | No       |

## Outputs

| API        | Return type | Description                              |
|------------|-------------|------------------------------------------|
| Completion | string      | Text of one predicted completion     |
| Chat       | string      | Text of one response of conversation |

## Use the LLM tool

1. Set up and select the connections to OpenAI resources or to a serverless API endpoint.
1. Configure the large language model API and its parameters.
1. Prepare the prompt with [guidance](prompt-tool.md#write-a-prompt).
