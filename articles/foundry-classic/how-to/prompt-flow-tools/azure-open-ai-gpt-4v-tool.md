---
title: Azure OpenAI GPT-4 Turbo with Vision tool in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: This article introduces you to the Azure OpenAI GPT-4 Turbo with Vision tool for flows in Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-prompt-flow
ms.custom:
  - build-2024
  - hub-only
ms.topic: article
ms.date: 01/27/2026
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---

# Azure OpenAI GPT-4 Turbo with Vision tool in Microsoft Foundry portal

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

By using the prompt flow Azure OpenAI GPT-4 Turbo with Vision tool, you can use your Azure OpenAI GPT-4 Turbo with Vision model deployment to analyze images and provide textual responses to questions about them.

## Prerequisites

[!INCLUDE [hub-only-prereq](../../includes/hub-only-prereq.md)]

- An Azure subscription. [You can create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry hub](../../how-to/create-azure-ai-resource.md) with a GPT-4 Turbo with Vision model deployed in [one of the regions that support GPT-4 Turbo with Vision](../../../ai-foundry/foundry-models/concepts/models-sold-directly-by-azure.md#model-summary-table-and-region-availability). When you deploy from your project's **Deployments** page, select `gpt-4` as the model name and `vision-preview` as the model version.

## Build with the Azure OpenAI GPT-4 Turbo with Vision tool

1. Create or open a flow in [Foundry](https://ai.azure.com/?cid=learnDocs). For more information, see [Create a flow](../flow-develop.md).
1. Select **+ More tools** > **Azure OpenAI GPT-4 Turbo with Vision** to add the Azure OpenAI GPT-4 Turbo with Vision tool to your flow.

    :::image type="content" source="../../media/prompt-flow/azure-openai-gpt-4-vision-tool.png" alt-text="Screenshot that shows the Azure OpenAI GPT-4 Turbo with Vision tool added to a flow in Foundry portal." lightbox="../../media/prompt-flow/azure-openai-gpt-4-vision-tool.png":::

1. Select the connection to your Azure OpenAI in Foundry Models. For example, you can select the **Default_AzureOpenAI** connection. For more information, see [Prerequisites](#prerequisites).
1. Enter values for the Azure OpenAI GPT-4 Turbo with Vision tool input parameters described in the [Inputs table](#inputs). For example, you can use this example prompt:

    ```jinja
    # system:
    As an AI assistant, your task involves interpreting images and responding to questions about the image.
    Remember to provide accurate answers based on the information present in the image.
    
    # user:
    Can you tell me what the image depicts?
    ![image]({{image_input}})
    ```

1. Select **Validate and parse input** to validate the tool inputs.
1. Specify an image to analyze in the `image_input` input parameter. For example, you can upload an image or enter the URL of an image to analyze. Otherwise, you can paste or drag and drop an image into the tool.
1. Add more tools to your flow, as needed. Or select **Run** to run the flow.

The outputs are described in the [Outputs table](#outputs).

Here's an example output response:

```json
{
    "system_metrics": {
        "completion_tokens": 96,
        "duration": 4.874329,
        "prompt_tokens": 1157,
        "total_tokens": 1253
    },
    "output": "The image depicts a user interface for Azure's OpenAI GPT-4 service. It is showing a configuration screen where settings related to the AI's behavior can be adjusted, such as the model (GPT-4), temperature, top_p, frequency penalty, etc. There's also an area where users can enter a prompt to generate text, and an option to include an image input for the AI to interpret, suggesting that this particular interface supports both text and image inputs."
}
```

## Inputs

The following input parameters are available.

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| connection             | AzureOpenAI | The Azure OpenAI connection to use in the tool.                                              | Yes      |
| deployment\_name       | string      | The language model to use.                                                                      | Yes      |
| prompt                 | string      | The text prompt that the language model uses to generate its response. The Jinja template for composing prompts in this tool follows a similar structure to the chat API in the large language model (LLM) tool. To represent an image input within your prompt, use the syntax `![image]({{INPUT NAME}})`. You can pass image input in the `user`, `system`, and `assistant` messages.                 | Yes      |
| max\_tokens            | integer     | The maximum number of tokens to generate in the response. Default is 512.                      | No       |
| temperature            | float       | The randomness of the generated text. Default is 1.                                            | No       |
| stop                   | list        | The stopping sequence for the generated text. Default is null.                                 | No       |
| top_p                  | float       | The probability of using the top choice from the generated tokens. Default is 1.               | No       |
| presence\_penalty      | float       | The value that controls the model's behavior regarding repeating phrases. Default is 0.      | No       |
| frequency\_penalty     | float       | The value that controls the model's behavior regarding generating rare phrases. Default is 0. | No       |

## Outputs

The following output parameters are available.

| Return type | Description                              |
|-------------|------------------------------------------|
| string      | The text of one response of conversation |

## Next steps

- Learn more about [how to process images in prompt flow](../flow-process-image.md).
- Learn more about [how to create a flow](../flow-develop.md).
