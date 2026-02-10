---
title: 'Quickstart: Use vision-enabled chats with the Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Use this article to get started using Microsoft Foundry to deploy and use an image-capable model.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom: references_regions, ignite-2024
ms.date: 01/29/2026
ai-usage: ai-assisted
---

Use this article to get started using [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) to deploy and test a chat completion model with image understanding. 


## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Once you have your Azure subscription, <a href="/azure/ai-foundry/openai/how-to/create-resource?pivots=web-portal"  title="Create an Azure OpenAI resource."  target="_blank">create an Azure OpenAI resource </a>.
 For more information about resource creation, see the [resource deployment guide](/azure/ai-foundry/openai/how-to/create-resource).
- A [Foundry project](/azure/ai-foundry/how-to/create-projects) with your Azure OpenAI resource added as a connection. 

## Prepare your media

You need an image to complete this quickstart. You can use this sample image or any other image you have available.

:::image type="content" source="/azure/ai-foundry/media/quickstarts/multimodal-vision/car-accident.png" alt-text="Photo of a car accident that can be used to complete the quickstart." lightbox="/azure/ai-foundry/media/quickstarts/multimodal-vision/car-accident.png":::

## Go to Foundry

> [!TIP]
> If you already have a vision-capable model deployed, skip to [Start a chat session to analyze images](#start-a-chat-session-to-analyze-images).

1. Browse to [Foundry](https://ai.azure.com/?cid=learnDocs) and sign in with the credentials associated with your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.
1. Select the project you'd like to work in.
1. On the left nav menu, select **Models + endpoints** and select **+ Deploy model**.
1. Choose an image-capable deployment by selecting model name: **gpt-4o** or **gpt-4o-mini**. In the window that appears, select a name and deployment type. Make sure your Azure OpenAI resource is connected. For more information about model deployment, see the [resource deployment guide](/azure/ai-foundry/openai/how-to/create-resource).
1. Select **Deploy**.
1. Next, select your new model and select **Open in playground**. In the chat playground, the deployment you created should be selected in the **Deployment** dropdown.



## Playground

In this chat session, you instruct the assistant to aid you in understanding images that you input.

For general help with assistant setup, chat sessions, settings, and panels, refer to the [Chat quickstart](/azure/ai-foundry/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-studio). 


## Start a chat session to analyze images

In this chat session, you're instructing the assistant to aid in understanding images that you input. 
1. To start, make sure your image-capable deployment is selected in the **Deployment** dropdown.
1. In the context text box on the **Setup** panel, provide this prompt to guide the assistant: `"You're an AI assistant that helps people find information."` Or, you can tailor the prompt to your image or scenario.

   > [!NOTE]
    > We recommend you update the System Message to be specific to the task in order to avoid unhelpful responses from the model.

1. Select **Apply changes** to save your changes. 
1. In the chat session pane, select the attachment button and then **Upload image**. Choose your image.
1. Add the following prompt in the chat field: `Describe this image`, and then select the send icon to submit it.
1. The send icon is replaced by a stop button. If you select it, the assistant stops processing your request. For this quickstart, let the assistant finish its reply.
1. The assistant replies with a description of the image.
1. Ask a follow-up question related to the analysis of your image. You could enter, `"What should I highlight about this image to my insurance company?"`.
1. You should receive a relevant response similar to what's shown here:
    ```
    When reporting the incident to your insurance company, you should highlight the following key points from the image:  
       
    1. **Location of Damage**: Clearly state that the front end of the car, particularly the driver's side, is damaged. Mention the crumpled hood, broken front bumper, and the damaged left headlight.  
       
    2. **Point of Impact**: Indicate that the car has collided with a guardrail, which may suggest that no other vehicles were involved in the accident.  
       
    3. **Condition of the Car**: Note that the damage seems to be concentrated on the front end, and there is no visible damage to the windshield or rear of the car from this perspective.  
       
    4. **License Plate Visibility**: Mention that the license plate is intact and can be used for identification purposes.  
       
    5. **Environment**: Report that the accident occurred near a roadside with a guardrail, possibly in a rural or semi-rural area, which might help in establishing the accident location and context.  
       
    6. **Other Observations**: If there were any other circumstances or details not visible in the image that may have contributed to the accident, such as weather conditions, road conditions, or any other relevant information, be sure to include those as well.  
       
    Remember to be factual and descriptive, avoiding speculation about the cause of the accident, as the insurance company will conduct its own investigation.
    ```
## View and export code

At any point in the chat session, you can enable the **Show raw JSON** switch at the top of the chat window to see the conversation formatted as JSON. Heres' what it looks like at the beginning of the quickstart chat session:

```json
[
	{
		"role": "system",
		"content": [
			"You are an AI assistant that helps people find information."
		]
	},
]
```

<!--
## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| Model not available in deployment dropdown | Vision-capable model not deployed | Deploy **gpt-4o** or **gpt-4o-mini** from **Models + endpoints**. |
| Image upload fails | Image too large or unsupported format | Use JPEG, PNG, GIF, or WebP. Maximum 20 MB per image. |
| Response seems incomplete | `max_tokens` not set or too low | Increase the token limit in **Parameters** panel. |
| Content filtered response | Image triggered content filter | GPT-4 Turbo with Vision has mandatory content filtering that can't be disabled. |
-->

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)


