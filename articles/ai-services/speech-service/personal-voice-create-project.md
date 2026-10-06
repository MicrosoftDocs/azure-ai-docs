---
title: Set up a personal voice - Speech service
titleSuffix: Foundry Tools
description: Learn how to set up a personal voice by using Microsoft Foundry or the custom voice REST API.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 09/09/2026
ms.author: pafarley
zone_pivot_groups: foundry-portal-rest
#Customer intent: As a developer, I want to learn how to set up a personal voice.
ai-usage: ai-assisted
---

# Set up a personal voice

Set up a personal voice before you add the voice talent's consent and audio prompt.

## Prerequisites

- Your use case must be approved for [limited access to custom voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access).
- You must have explicit permission from the voice talent to create and use a synthetic version of their voice.

::: zone pivot="ai-foundry-portal"

# [Foundry (new)](#tab/foundry-new)

## Prepare your Foundry project

Use a Foundry project associated with a resource in a region that supports personal voice. Check the **Personal voice** column in the [Speech service regions table](./regions.md?tabs=tts). To create a project, see [Create a Foundry project](../../foundry/how-to/create-projects.md?tabs=foundry#create-a-foundry-project).

Personal voice isn't available on the Free (F0) tier. For supported tiers and limits, see [Personal voice quotas](./speech-services-quotas-and-limits.md#custom-personal-voice).

## Start a personal voice customization

In Foundry (new), you create a personal voice as a customization. To start, follow these steps:

> [!TIP]
> To start from **Build**, select **Services** > **Customizations**. Select **Create**, and then complete **Basic details** in this procedure.

1. [!INCLUDE [foundry-sign-in](../../foundry/includes/foundry-sign-in.md)]
1. Open the Foundry project associated with the resource you want to use for personal voice.
1. Select **Discover**.
1. On **Overview**, under **Experiment with prebuilt services**, select **Azure Speech**.
1. On the **Services** page, under **Customize**, select **Personal voice** to open the **Customize a model** page.

   :::image type="content" source="./media/personal-voice/foundry-new-personal-voice-entry.png" alt-text="Screenshot of Azure Speech services in Foundry with Personal voice outlined under Customize." lightbox="./media/personal-voice/foundry-new-personal-voice-entry.png":::

1. On the **Basic details** step, fill in these settings:

   - **Select model**: Select **Azure Speech - Text to Speech** if it isn't already selected.
   - **Type**: Select **Personal voice** if it isn't already selected.
   - **Voice name**: Enter a name for your voice.
   - **Description**: Optionally enter a description.

   :::image type="content" source="./media/personal-voice/foundry-new-personal-voice-basic-details.png" alt-text="Screenshot of the Customize a model page with Personal voice selected and the Type and Voice name fields outlined." lightbox="./media/personal-voice/foundry-new-personal-voice-basic-details.png":::

1. Select **Next**.

The wizard continues to the **Register voice talent** step, where you [add user consent](./personal-voice-create-consent.md?pivots=ai-foundry-portal&tabs=foundry-new).

## Next steps

> [!div class="nextstepaction"]
> [Add user consent for personal voice.](./personal-voice-create-consent.md?pivots=ai-foundry-portal&tabs=foundry-new)

# [Foundry (classic)](#tab/foundry-classic)

## Create a project

To create a personal voice fine-tuning project in the Microsoft Foundry portal, follow these steps:

1. Go to your Microsoft Foundry project in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To create a project, see [Create a Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects).
1. Select **Fine-tuning** from the left pane.
1. Select the **AI Service** tab, and then select the **Fine-tune** button. The **Fine-tune a model** wizard opens.
1. On the **Basic details** pane of the wizard:
   - Select **Azure Speech - Text to Speech** as the model to fine-tune.
   - Set **Type** to **Personal voice**.
   - Enter a **Name** and **Description** for the fine-tuning task.
   - Select the **Language** of the voice you want to create.
1. Select **Next**.

The wizard continues to the **Register voice talent** step, where you [add user consent](./personal-voice-create-consent.md?pivots=ai-foundry-portal&tabs=foundry-classic).

## Next steps

> [!div class="nextstepaction"]
> [Add user consent for personal voice.](./personal-voice-create-consent.md?pivots=ai-foundry-portal&tabs=foundry-classic)

---

::: zone-end

::: zone pivot="rest-api"

The custom voice REST API organizes the user consent statement and personal voice ID in a Personal Voice project.

## Create a project

To create a personal voice project, use the [Projects_Create](/rest/api/aiservices/speechapi/projects/create) operation of the custom voice API. Construct the request body according to the following instructions:

- Set the required `kind` property to `PersonalVoice`. The kind can't be changed later.
- Optionally, set the `description` property for the project description. The project description can be changed later.

Make an HTTP PUT request using the URI as shown in the following [Projects_Create](/rest/api/aiservices/speechapi/projects/create) example. 
- Replace `YourResourceKey` with your Speech resource key.
- Replace `YourResourceName` with your Speech resource name.
- Replace `ProjectId` with a project ID of your choice. The case sensitive ID must be unique within your Speech resource. The ID will be used in the project's URI and can't be changed later. 

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: YourResourceKey" -H "Content-Type: application/json" -d '{
  "description": "Project description",
  "kind": "PersonalVoice"
} '  "https://YourResourceName.cognitiveservices.azure.com/customvoice/projects/ProjectId?api-version=2026-01-01"
```

You should receive a response body in the following format:

```json
{
  "id": "ProjectId",
  "description": "Project description",
  "kind": "PersonalVoice",
  "createdDateTime": "2024-09-01T05:30:00.000Z"
}
```

You use the project `id` in subsequent API requests to [add user consent](./personal-voice-create-consent.md?pivots=rest-api) and [get a speaker profile ID](./personal-voice-create-voice.md?pivots=rest-api).

## Next steps

> [!div class="nextstepaction"]
> [Add user consent for personal voice.](./personal-voice-create-consent.md?pivots=rest-api)

::: zone-end
