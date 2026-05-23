---
title: Create a project for personal voice - Speech service
titleSuffix: Foundry Tools
description: Learn how to create a project for personal voice.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 05/22/2026
ms.author: pafarley
zone_pivot_groups: foundry-portal-rest
#Customer intent: As a developer, I want to learn how to create a project for personal voice.
ai-usage: ai-assisted
---

# Create a project for personal voice

Personal voice projects contain the user consent statement and the personal voice ID. You can create a personal voice project in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) or by using the custom voice REST API.

::: zone pivot="ai-foundry-portal"

## Create a project

To create a personal voice fine-tuning project in the Microsoft Foundry portal, follow these steps:

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. In the upper right, select **Build**, and then select **Models** from the left pane.
1. Select the **AI Services** tab.
1. Select **Azure Speech - Text to Speech**.
1. In the upper right, select **Fine-tune**. The **Fine-tune a model** wizard opens.
1. On the **Basic details** pane of the wizard:
   - Verify that **Select model** is set to the personal voice model.
   - Verify that **Type** is set to **Personal voice**.
   - Enter a **Name** and **Description** for the fine-tuning task.
   - Select the **Language** of the voice you want to create.
1. Select **Next**.

The wizard continues to the **Register voice talent** step, where you [add user consent](./personal-voice-create-consent.md).

::: zone-end

::: zone pivot="rest-api"

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

You use the project `id` in subsequent API requests to [add user consent](./personal-voice-create-consent.md) and [get a speaker profile ID](./personal-voice-create-voice.md).

::: zone-end

## Next steps

> [!div class="nextstepaction"]
> [Add user consent to the personal voice project.](./personal-voice-create-consent.md)
