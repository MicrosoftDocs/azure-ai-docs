---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 02/06/2026
ms.author: lajanuar
ai-usage: ai-assisted
---
## Prerequisites

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned the Azure AI Account Owner role at the subscription level. Alternatively, the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, see [Role based access control (RBAC)](../../../../../ai-foundry/openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* **Foundry resource**. Create a [Foundry resource](../../../../multi-service-resource.md) or see [Configure a Foundry resource](../../../concepts/configure-azure-resources.md). Alternatively, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project**. For more information, see [Create a Foundry project](../../../../../ai-foundry/how-to/create-projects.md).

### [Foundry (classic)](#tab/foundry-classic)

> [!NOTE]
> This content refers to the [Foundry (classic)](https://ai.azure.com/) portal, which supports hub-based projects and other resource types. To confirm that you're using Foundry (classic), make sure the version toggle in the portal banner is in the **off** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/classic-foundry.png" border="false":::

You can use [Foundry (classic)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Detect the language of input text
> * Review confidence scores and ISO language codes
> * Configure country/region hints for improved accuracy

## Navigate to the Foundry (classic) playground

1. In the left pane, select **Playgrounds**.
1. Select the **Try Azure Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="Screenshot showing the Playgrounds navigation and the Try Azure Language Playground button in Foundry (classic)." lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Detect language in the Foundry playground

The **Language playground** consists of four sections:

| Section | Purpose |
| --- | --- |
| **Top banner** | Select the **Detect language** tile. |
| **Left pane** | Set **Configuration** options such as API version, model version, and country hint. |
| **Center pane** | Enter text for processing and review results. |
| **Right pane** | View **Details** for detected language and script. |

1. Select the **Detect language** tile from the top banner.
1. Enter or paste text in the center pane.
1. In the **Configuration** pane, set the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select country hint| Select the origin country/region of the input text. |

1. Select the **Run** button to detect the language.

After the operation completes, the **Details** section displays the following fields for the detected language and script:

| Field | Description |
| --- | --- |
| ISO 639-1 Code | The ISO 639-1 two-letter code for the detected language. |
| Confidence Score | The model's level of certainty that the language identification is correct. |
| Script Name | The name of the detected script in the text. |
| ISO 15924 Script Code | The ISO 15924 code for the detected script (writing system). |

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/language-detection.png" alt-text="A screenshot showing language detection results with confidence scores and ISO codes displayed in the Details pane of the Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/language-detection.png":::

Verify that the detected language matches the language of your input text. If the result shows `unknown`, provide a longer text sample or set a **Country hint** for better accuracy.

### [Foundry (new)](#tab/foundry-new)

> [!NOTE]
> This content refers to the [Foundry (new)](https://ai.azure.com/) portal, which supports only Foundry projects and provides streamlined access to models, agents, and tools. For more information, see [What is Microsoft Foundry?](../../../../../ai-foundry/what-is-foundry.md). To confirm that you're using Foundry (new), make sure the version toggle in the portal banner is in the **on** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/new-foundry.png" border="false":::

You can use [Foundry (new)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Detect the language of input text
> * Review confidence scores and ISO language codes
> * Configure country/region hints for improved accuracy

## Navigate to the Foundry (new) playground

The active project appears in the upper-left corner. To create a new project:

1. Open the project drop-down menu.
1. Enter a project name or select an existing one.
1. Select **Create project**.

   :::image type="content" source="../../../media/new-foundry-homepage.png" alt-text="Screenshot of the Foundry (new) homepage":::

There are two ways to access the Language Detection interface:

1. Select the **Discover** tab from the upper right navigation bar to go to the **Models** page.
   * In the search bar under models, enter **Azure** and press enter.
   * Next, select **Azure-Language-detection** from the search results.
   * Finally, select the **Open in Playground** button.

1. Select the **Build** tab from the upper right navigation bar.
   * From the left navigation bar, select  **Models**.
   * Select the **AI services** tab.
   * Next, select  **Azure-Language-detection** to go to the playground.

## Detect language in the Foundry playground

The **Detect Language** feature identifies the language used in written content.

1. On the **Playground** tab, select a text sample from the drop-down menu, use the paperclip icon to upload your text, or enter your own text.

1. Select the **Configure** button. In the **Configure** side panel, set the following options:

   |Option|Description|
   |---|---|
   |**API version**| Select the API version that you prefer to use.|
   |**Model version**| Select the model version that you prefer to use.|
   |**Country/region hint** (optional)| You can select the origin country/region for the source text.|

After you make your selections, choose the **Detect** button. Then review the text and accompanying details written in formatted text or as a JSON response:

   |Field | Description|
   |---|---|
   |**Confidence**| The model's level of certainty regarding whether it correctly identified a language.|
   |**ISO 639-1 code**| A two letter code for the detected language.|
   |**Detected script**| The name of the detected script in the text.|
   |**Detected script code**| The ISO 15924 script code for the detected script (writing system).|

Verify that the detected language matches the language of your input text. You can use the **Edit** button to modify the **Configure** parameters and rerun detection as needed.