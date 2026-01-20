---
title: include file
description: include file
author: PatrickFarley
ms.reviewer: pafarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/05/2025
ms.custom: include
---


## Create a content filter in Microsoft Foundry

For any model deployment in [Foundry](https://ai.azure.com/?cid=learnDocs), you can directly use the default content filter, but you might want to have more control. For example, you could make a filter stricter or more lenient, or enable more advanced capabilities like prompt shields and protected material detection.

> [!TIP]
> For guidance with content filters in your Foundry project, you can read more at [Foundry content filtering](/azure/ai-studio/concepts/content-filtering).

Follow these steps to create a content filter:

[!INCLUDE [tip-left-pane](tip-left-pane.md)]

1. [!INCLUDE [classic-sign-in](classic-sign-in.md)]
1. Navigate to your project. Then select the **Guardrails + controls** page from the left menu and select the **Content filters** tab.

    :::image type="content" source="../media/content-safety/content-filter/create-content-filter.png" alt-text="Screenshot of the button to create a new content filter." lightbox="../media/content-safety/content-filter/create-content-filter.png":::
1. Select **+ Create content filter**.
1. On the **Basic information** page, enter a name for your content filtering configuration. Select a connection to associate with the content filter. Then select **Next**.

    :::image type="content" source="../media/content-safety/content-filter/create-content-filter-basic.png" alt-text="Screenshot of the option to select or enter basic information such as the filter name when creating a content filter." lightbox="../media/content-safety/content-filter/create-content-filter-basic.png":::

    Now you can configure the input filters (for user prompts) and output filters (for model completion). 
1. On the **Input filters** page, you can set the filter for the input prompt. For the first four content categories there are three severity levels that are configurable: Low, medium, and high. You can use the sliders to set the severity threshold if you determine that your application or usage scenario requires different filtering than the default values. 
    Some filters, such as Prompt Shields and Protected material detection, enable you to determine if the model should annotate and/or block content. Selecting **Annotate only** runs the respective model and returns annotations via API response, but it will not filter content. In addition to annotate, you can also choose to block content.

    If your use case was approved for modified content filters, you receive full control over content filtering configurations. You can choose to turn filtering partially or fully off, or enable annotate only for the content harms categories (violence, hate, sexual, and self-harm).

    Content is annotated by category and blocked according to the threshold you set. For the violence, hate, sexual, and self-harm categories, adjust the slider to block content of high, medium, or low severity.

    :::image type="content" source="../media/content-safety/content-filter/input-filter.png" alt-text="Screenshot of input filter screen.":::
1. On the **Output filters** page, you can configure the output filter, which is applied to all output content the model generates. Configure the individual filters as before. The page provides the Streaming mode option, letting you filter content in near-real-time as the model generates it and reducing latency. When you're finished select **Next**. 
    
    Content is annotated by each category and blocked according to the threshold. For violent content, hate content, sexual content, and self-harm content category, adjust the threshold to block harmful content with equal or higher severity levels.

    :::image type="content" source="../media/content-safety/content-filter/output-filter.png" alt-text="Screenshot of output filter screen.":::
   
1. Optionally, on the **Connection** page, you can associate the content filter with a deployment. If a selected deployment already has a filter attached, you must confirm that you want to replace it. You can also associate the content filter with a deployment later. Select **Create**.

    Content filtering configurations are created at the hub level in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). Learn more about configurability in the [Azure OpenAI in Foundry Models documentation](/azure/ai-foundry/openai/how-to/content-filters).


1. On the **Review** page, review the settings and then select **Create filter**.

### Use a blocklist as a filter

You can apply a blocklist as either an input or output filter, or both. Enable the **Blocklist** option on the **Input filter** and/or **Output filter** page. Select one or more blocklists from the dropdown, or use the built-in profanity blocklist. You can combine multiple blocklists into the same filter.

## Apply a content filter

The filter creation process gives you the option to apply the filter to the deployments you want. You can also change or remove content filters from your deployments at any time.

Follow these steps to apply a content filter to a deployment:

1. Go to [Foundry](https://ai.azure.com/?cid=learnDocs) and select a project.
1. Select **Models + endpoints** on the left pane and choose one of your deployments, then select **Edit**.

    :::image type="content" source="../media/content-safety/content-filter/deployment-edit.png" alt-text="Screenshot of the button to edit a deployment." lightbox="../media/content-safety/content-filter/deployment-edit.png":::

1. In the **Update deployment** window, select the content filter you want to apply to the deployment. Then select **Save and close**.

    :::image type="content" source="../media/content-safety/content-filter/apply-content-filter.png" alt-text="Screenshot of apply content filter." lightbox="../media/content-safety/content-filter/apply-content-filter.png":::

    You can also edit and delete a content filter configuration if necessary. Before you delete a content filtering configuration, you need to unassign and replace it from any deployment in the **Deployments** tab.

Now, you can go to the playground to test whether the content filter works as expected.

> [!TIP]
> You can also create and update content filters using the REST APIs. For more information, see the [API reference](/rest/api/aiservices/accountmanagement/rai-policies/create-or-update). Content filters can be configured at the resource level. Once a new configuration is created, it can be associated with one or more deployments. For more information about model deployment, see the resource [deployment guide](../openai/how-to/create-resource.md). 
