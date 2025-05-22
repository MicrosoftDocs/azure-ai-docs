---
title: View AI red teaming results in Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to view the results of the AI red teaming agent's scan of a Generative AI application in Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 05/29/2025
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
---

## Viewing AI red teaming results in Azure AI Foundry project (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

After your automated scan is finished running [locally](develop/run-scans-ai-red-teaming-agent.md) or [remotely](develop/run-ai-red-teaming-cloud.md), the results also get logged to your Azure AI Foundry project which you specified in the creation of your AI Red Teaming Agent.

## View report of each scan

In your Azure AI Foundry project, navigate to the **Evaluations** page and select the **AI red teaming** tab to view the comprehensive report with a detailed drill-down of each scan.

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team.png" alt-text="Screenshot of AI Red Teaming tab in Azure AI Foundry project page." lightbox="../../media/evaluations/red-teaming-agent/ai-red-team.png":::

Once you select into the scan, you can view the report by risk categories, which shows you the overall number of successful attacks and a breakdown of successful attacks per risk categories:

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team-report-risk.png" alt-text="Screenshot of AI Red Teaming report view by risk category in Azure AI Foundry." lightbox="../../media/evaluations/red-teaming-agent/ai-red-team-report-risk.png":::

Or by attack complexity classification:

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team-report-attack.png" alt-text="Screenshot of AI Red Teaming report view by attack complexity category in Azure AI Foundry." lightbox="../../media/evaluations/red-teaming-agent/ai-red-team-report-attack.png":::

Drilling down further into the data tab provides a row-level view of each attack-response pair, enabling deeper insights into system issues and behaviors. For each attack-response pair, you can see additional information such as whether or not the attack was successful, what attack strategy was used and its attack complexity. There's also an option for a human in the loop reviewer to provide human feedback by selecting the thumbs up or thumbs down icon.

:::image type="content" source="../../media/evaluations/red-teaming-agent/ai-red-team-data.png" alt-text="Screenshot of AI Red Teaming data page in Azure AI Foundry." lightbox="../../media/evaluations/red-teaming-agent/ai-red-team-data.png":::

To view each conversation, selecting **View more** opens up the full conversation for more detailed analysis of the AI system's response.

:::image type="content" source="../media/evaluations/red-teaming-agent/ai-red-team-data-conversation.png" alt-text="Screenshot of AI Red Teaming data page with a conversation history opened in Azure AI Foundry." lightbox="../../media/evaluations/red-teaming-agent/ai-red-team-data-conversation.png":::

## Next steps

Try out an [example workflow](https://aka.ms/airedteamingagent-sample) in our GitHub samples.
