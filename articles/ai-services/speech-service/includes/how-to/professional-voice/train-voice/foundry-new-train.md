---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 09/07/2026
ms.custom: include
ai-usage: ai-assisted
---

In the new Microsoft Foundry portal, the **Customize a model** page uses a single **Training method** dropdown that covers all variants. These steps continue from the page you opened in [Set up a professional voice](../../../../professional-voice-create-project.md), after you upload training data on the **Training data** step.

If you closed the page, [resume your draft customization](../../../../professional-voice-create-project.md?tabs=foundry-new&pivots=ai-foundry-portal#resume-an-unfinished-customization) before continuing.

1. On the **Training data** step, select the **Training method** that matches your scenario. Options include **Neural - HD**, **Neural - Default**, **Neural - Multi lingual**, and **Neural - Multi style**. For details about each method, see [Choose a training method](#choose-a-training-method).
1. Select the training recipe **Version**. The latest version is selected by default. The supported features and training time can vary by version. In some cases, you can choose an earlier version to reduce training time.
1. Confirm the **Model language**.
1. From the **Select dataset** dropdown, select an eligible dataset that you uploaded. The portal evaluates dataset eligibility for the selected training method and version because data-size and duration requirements vary by recipe.

   :::image type="content" source="../../../../media/custom-voice/professional-voice/foundry-new-training-configuration.png" alt-text="Screenshot of the Training data step with Training method, Version, and Select dataset outlined beside the dataset validation summary." lightbox="../../../../media/custom-voice/professional-voice/foundry-new-training-configuration.png":::

1. Select **Next**.
1. On the **Review** step, review the basic details, voice talent, training configuration, data size, test information, estimated training time, and cost warning.
1. Select the acknowledgment that training incurs account usage.
1. Select the acknowledgment to agree to the terms of use.
1. Select **Submit** to start training the model.
