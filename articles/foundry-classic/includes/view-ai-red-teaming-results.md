---
title: Include file
description: Include file
author: lgayhardt
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 10/20/2025
ms.author: lagayhar
ms.custom: include file
---

## Viewing AI red teaming results in Microsoft Foundry project (preview)

After your automated scan finishes, the results also get logged to your Foundry project, which you specified in the creation of your AI red teaming agent.

### View report of each scan

In your Foundry project or hub-based project, navigate to the **Evaluation** page. Select **AI red teaming** to view the report with detailed drill-down results of each scan.

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team.png" alt-text="Screenshot of AI Red Teaming tab in Foundry project page." lightbox="../media/evaluations/red-teaming-agent/ai-red-team.png":::

When you select into the scan, you can view the report by risk categories, which shows the overall number of successful attacks and a breakdown of successful attacks per risk categories:

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team-report-risk.png" alt-text="Screenshot of AI Red Teaming report view by risk category in Foundry." lightbox="../media/evaluations/red-teaming-agent/ai-red-team-report-risk.png":::

Or by attack complexity classification:

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team-report-attack.png" alt-text="Screenshot of AI Red Teaming report view by attack complexity category in Foundry." lightbox="../media/evaluations/red-teaming-agent/ai-red-team-report-attack.png":::

Drilling down further into the data tab provides a row-level view of each attack-response pair. This information offers deeper insights into system issues and behaviors. For each attack-response pair, you can see more information, such as whether or not the attack was successful, what attack strategy was used, and its attack complexity. A human in the loop reviewer can provide human feedback by selecting the thumbs up or thumbs down icon.

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team-data.png" alt-text="Screenshot of AI Red Teaming data page in Foundry." lightbox="../media/evaluations/red-teaming-agent/ai-red-team-data.png":::

To view each conversation, select **View more** to see the full conversation for more detailed analysis of the AI system's response.

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team-data-conversation.png" alt-text="Screenshot of AI Red Teaming data page with a conversation history opened in Foundry." lightbox="../media/evaluations/red-teaming-agent/ai-red-team-data-conversation.png":::

