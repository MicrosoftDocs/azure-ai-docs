---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/23/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

## Deploy Claude models

Deploy a Claude model by following these steps in the Foundry portal:

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. From the Foundry portal homepage, select **Discover** in the upper-right navigation, and then select **Models** in the left pane.

1. Select a Claude model and review its details in the model card. If the model is available in both versions, you land on the **Hosted on Azure** (version 2) version of the model by default. You can confirm the version that's open by looking for the **Hosted on** information in the **Quick facts** pane of the model card.

    > [!TIP]
    > If your selected Claude model is available in both versions, the model card contains a link that takes you to the alternate version of the model.

1. Select **Deploy** > **Custom settings** to customize your deployment. 

1. Read the Azure Marketplace terms, select an industry, and select **Agree and Proceed** to accept the terms to subscribe to Azure Marketplace.

1. If both versions are available, the deployment page has the **Model version** set to version **2: Hosted on Azure** by default. Change this selection to **1: Hosted on Anthropic infrastructure**, if desired.

    > [!NOTE]
    > If you select the **Deploy** > **Default settings** option, your deployment is automatically set to version **2: Hosted on Azure**.


1. Configure other deployment settings:

   - By default, the deployment uses the model name. You can modify this name before deploying. During inference, use the deployment name in the `model` parameter to route requests to this particular deployment.
   - Select the **Region scope**: **Global** (available for all Claude models and versions) or **Data Zone** (if available for your model and version combination). 

1. Select **Deploy** to create your deployment.

1. When the deployment completes, you land on the [Foundry Playgrounds](../../concepts/concept-playgrounds.md) where you can interactively test the model. Your project and resource must be in one of the supported regions of deployment for the model. 

1. Select the **Details** tab to verify your deployment details and check that the deployment status shows **Succeeded**.