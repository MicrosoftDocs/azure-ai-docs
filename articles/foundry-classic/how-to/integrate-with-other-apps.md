---
title: "Integrate Microsoft Foundry with your applications (classic)"
description: "Learn how to retrieve and use Microsoft Foundry endpoints for third-party integrations, including comparison with Azure OpenAI v1 endpoints. (classic)"
ms.topic: how-to
ms.date: 04/08/2026
ms.service: azure-ai-foundry
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ms.custom:
  - devx-track-ai
  - classic-and-new
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
#customer intent: As a developer, I want to understand how to retrieve Microsoft Foundry endpoints and integrate them with third-party applications, similar to Azure OpenAI.
ROBOTS: NOINDEX, NOFOLLOW
---

# Integrate Microsoft Foundry with your applications (Microsoft or third-party services) (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/integrate-with-other-apps.md)

[!INCLUDE [classic-links](../includes/classic-links.md)]

Microsoft Foundry is a developer platform that lets you embed AI models, agents, evaluation tools, and Responsible AI capabilities into your workflows and applications. You can build complete solutions in Foundry or selectively integrate its features into your custom apps and Microsoft or partner solutions.

In this article, you learn how to choose an integration pattern and send your first REST API request to a Foundry endpoint.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](create-projects.md). Note your resource endpoint (for example, `https://{resource}.services.ai.azure.com`). 
- A [deployed model](../foundry-models/how-to/deploy-foundry-models.md) for inference calls.
- Authentication credentials: either a [Microsoft Entra ID token](../concepts/rbac-foundry.md) or an API key from the Foundry portal.

[!INCLUDE [integrate-with-other-apps content](../../foundry/includes/how-to-integrate-with-other-apps-content.md)]

## Related content

- [Authentication and authorization options in Foundry](../concepts/rbac-foundry.md)
- [Import a Foundry API in API Management](/azure/api-management/azure-ai-foundry-api)
- [AI gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [Consume Fabric data agent from Foundry Services](/fabric/data-science/data-agent-foundry)