---
title: Publish Agents to Microsoft Copilot 365 and Microsoft Teams.
description: Learn how to publish agents to Microsoft Copilot 365 and Microsoft Teams.
author: aahill
ms.author: aahi
ms.date: 11/17/2025
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
---

# Publish agents to Microsoft 365 Copilot and Microsoft Teams 

Use this article to make your Microsoft Foundry agent available in Microsoft 365 Copilot and Microsoft Teams.

## Prerequisites 

* Access to Microsoft Foundry 
* A tested agent that you want to publish 
* Azure subscription and permissions to create Azure Bot Service and Microsoft Entra ID apps

## Publish your agent as an agent application  

> [!NOTE]
> You can also use the [available C# sample](https://github.com/OfficeDev/microsoft-365-agents-toolkit-samples/tree/dev/ProxyAgent-CSharp) to work programmatically. 

1. In the Microsoft Foundry portal, select your agent version. 
1. Select **Publish** and create an agent application.   

    :::image type="content" source="../media/publish-agent.png" alt-text="A screenshot showing the button to publish an agent in the Microsoft Foundry." lightbox="../media/publish-agent.png":::

1. Select **Publish** again, and then select **Publish to Teams and Microsoft 365 Copilot**.
1. Enter the information in the window that appears. An application ID and tenant ID will be provisioned automatically. 
    1. Select **Create an Azure Bot Service** in the drop-down menu. An Azure Bot Service will be automatically generated.  
1. Fill in the required metadata, including a name, description, icons, publisher info, privacy policy, and terms of use. 
1. Select **Prepare Agent** to start packaging the agent.
1. Once the Microsoft 365 publishing package is prepared, you can download the package for local testing or manual deployment to Microsoft Partner Center. You can also continue publishing to Microsoft Teams and Microsoft 365 Copilot. 

1. Choose your publish scope:  

    **Shared Scope**: The agent will appear under **Your agents** in the agent store for Microsoft 365 Copilot.  
    
    **Organization Scope**: The agent will appear under **Built by your org** in the agent store for Microsoft 365 Copilot. This requires admin approval in the Microsoft Admin Center.    
    
    :::image type="content" source="../media/agent-store.png" alt-text="A screenshot showing the agent store in Microsoft 365." lightbox="../media/agent-store.png":::