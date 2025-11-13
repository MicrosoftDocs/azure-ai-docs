---
title: Resource types for Foundry
description: Include file that describes Azure AI resource types and kinds.
author: Blackmist
ms.author: larryfr
ms.reviewer: larryfr
ms.date: 12/05/2024
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include
  - build-2024
  - build-aifnd
  - build-2025
---


|Resource type|Resource provider and type|Kind|Supported capabilities|
|---|---|---|
|Microsoft Foundry|`Microsoft.CognitiveServices/account`|`AIServices`|Agents, Evaluations, Azure OpenAI, Speech, Vision, Language, and Content Understanding|
|Foundry project|`Microsoft.CognitiveServices/account/project`|`AIServices`| **Subresource to the above** |
|Azure Speech|`Microsoft.CognitiveServices/account`|`Speech`|Speech|
|Azure Language in Foundry Tools|`Microsoft.CognitiveServices/account`|`Language`|Language|
|Azure Vision in Foundry Tools|`Microsoft.CognitiveServices/account`|`Vision`|Vision|
|Azure OpenAI service|`Microsoft.CognitiveServices/account`|`OpenAI`|Azure OpenAI models and their customization|
|Azure AI Hub|`Microsoft.MachineLearningServices/workspace`|`hub`|Connectivity hub and security configuration holder for hub-based projects|
|Azure AI Hub project|`Microsoft.MachineLearningServices/workspace`|`project`|Custom ML model training and model hosting|