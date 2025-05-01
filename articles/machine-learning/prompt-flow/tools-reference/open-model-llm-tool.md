---
title: Open Model LLM tool in Azure Machine Learning prompt flow
titleSuffix: Azure Machine Learning
description: The prompt flow Open Model LLM tool enables you to utilize various open-source and foundational models.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom: ignite-2023
ms.topic: reference
author: lgayhardt
ms.author: lagayhar
ms.reviewer: GEWOODS
ms.date: 11/02/2023
---

# Open Model LLM tool

The Open Model LLM tool enables the utilization of various Open Model and Foundational Models, such as [Falcon](https://ml.azure.com/models/tiiuae-falcon-7b/version/4/catalog/registry/azureml) and [Llama 2](https://ml.azure.com/models/Llama-2-7b-chat/version/14/catalog/registry/azureml-meta), for natural language processing in Azure Machine Learning prompt flow.

> [!CAUTION]
> **Deprecation notice:** The Open Model LLM tool has been deprecated in favor of the [LLM tool](llm-tool.md), which provide support for all the models supported by the [Azure AI model inference API](https://aka.ms/azureai/modelinference) and hence it provider greater flexibility.

Here's how it looks in action on the Visual Studio Code prompt flow extension. In this example, the tool is being used to call a LlaMa-2 chat endpoint and asking "What is CI?".

:::image type="content" source="./media/open-model-llm-tool/open-model-llm-on-vscode-prompt-flow.png" alt-text="Screenshot that shows the Open Model LLM tool on Visual Studio Code prompt flow extension." lightbox = "./media/open-model-llm-tool/open-model-llm-on-vscode-prompt-flow.png":::

This prompt flow tool supports two different LLM API types:

- **Chat**: Shown in the preceding example. The chat API type facilitates interactive conversations with text-based inputs and responses.
- **Completion**: The Completion API type is used to generate single response text completions based on provided prompt input.

## Quick overview: How do I use the Open Model LLM tool?

1. Choose a model from the Azure Machine Learning Model Catalog and get it deployed.
2. Connect to the model deployment.
3. Configure the open model llm tool settings.
4. [Prepare the prompt](https://microsoft.github.io/promptflow/reference/tools-reference/prompt-tool.html#how-to-write-prompt).
5. Run the flow.

## Prerequisites: Model deployment

- Pick the model that matched your scenario from the [Azure Machine Learning model catalog](https://ml.azure.com/model/catalog).
- Use the **Deploy** button to deploy the model to an Azure Machine Learning online inference endpoint.
   - Use one of the Pay as you go deployment options.

To learn more, see [Deploy foundation models to endpoints for inferencing](../../how-to-use-foundation-models.md#deploying-foundation-models-to-endpoints-for-inferencing).

## Prerequisites: Connect to the model

In order for prompt flow to use your deployed model, you need to connect to it. There are two ways to connect.

### Endpoint connections

Once your flow is associated to an Azure Machine Learning or Azure AI Foundry workspace, the Open Model LLM tool can use the endpoints on that workspace.

- **Using Azure Machine Learning or Azure AI Foundry workspaces**: If you're using prompt flow in one of the web page based browsers workspaces, the online endpoints available on that workspace who up automatically.

- **Using VS Code or code first**: If you're using prompt flow in VS Code or one of the Code First offerings, you need to connect to the workspace. The Open Model LLM tool uses the azure.identity DefaultAzureCredential client for authorization. One way is through [setting environment credential values](/python/api/azure-identity/azure.identity.environmentcredential).

### Custom connections

The Open Model LLM tool uses the CustomConnection. Prompt flow supports two types of connections:

- **Workspace connections** - Connections that are stored as secrets on an Azure Machine Learning workspace. While these connections can be used, in many places, the are commonly created and maintained in the Studio UI. To learn how to create a custom connection in Studio UI, see [how to create a custom connection](./python-tool.md#create-a-custom-connection).

- **Local connections** - Connections that are stored locally on your machine. These connections aren't available in the Studio UX, but can be used with the VS Code extension. To learn how to create a local Custom Connection, see [how to create a local connection](https://microsoft.github.io/promptflow/how-to-guides/manage-connections.html#create-a-connection).

The required keys to set are:

- **endpoint_url**
    - This value can be found at the previously created Inferencing endpoint.
- **endpoint_api_key**
    - Ensure to set it as a secret value.
    - This value can be found at the previously created Inferencing endpoint.
- **model_family**
    - Supported values: LLAMA, DOLLY, GPT2, or FALCON
    - This value is dependent on the type of deployment you're targeting.

## Running the tool: Inputs

The Open Model LLM tool has many parameters, some of which are required. See the following table for details, you can match these parameters to the preceding screenshot for visual clarity.

| Name | Type | Description | Required |
|------|------|-------------|----------|
| api | string | The API mode that depends on the model used and the scenario selected. *Supported values: (Completion \| Chat)* | Yes |
| endpoint_name | string | Name of an Online Inferencing Endpoint with a supported model deployed on it. Takes priority over connection. | Yes |
| temperature | float | The randomness of the generated text. Default is 1. | No |
| max_new_tokens | integer | The maximum number of tokens to generate in the completion. Default is 500. | No |
| top_p | float | The probability of using the top choice from the generated tokens. Default is 1. | No |
| model_kwargs | dictionary | This input is used to provide configuration specific to the model used. For example, the Llama-02 model may use {\"temperature\":0.4}. *Default: {}* | No |
| deployment_name | string | The name of the deployment to target on the Online Inferencing endpoint. If no value is passed, the Inferencing load balancer traffic settings are used. | No |
| prompt | string | The text prompt that the language model uses to generate its response. | Yes |

## Outputs

| API        | Return Type | Description                              |
|------------|-------------|------------------------------------------|
| Completion | string      | The text of one predicted completion     |
| Chat       | string      | The text of one response int the conversation |

## Deploying to an online endpoint

When you deploy a flow containing the Open Model LLM tool to an online endpoint, there's an extra step to set up permissions. During deployment through the web pages, there's a choice between System-assigned and User-assigned Identity types. Either way, using the Azure portal (or a similar functionality), add the "Reader" Job function role to the identity on the Azure Machine Learning workspace or Ai Studio project, which is hosting the endpoint. The prompt flow deployment may need to be refreshed.
