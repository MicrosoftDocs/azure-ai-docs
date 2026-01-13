---
title: Publish Agents to Agents 365.
description: Learn how to publish agents to Agents 365.
author: aahill
ms.author: aahi
ms.date: 11/17/2025
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
---

# Publish an agent to Agent 365

Microsoft Agent 365 is the control plane for enterprise AI agents, allowing developers to register, secure, and scale agents across Microsoft 365 and Non-Microsoft environments. With Agent 365, organizations can: 

* Manage hosted agents at scale with unified identity and lifecycle controls 
* Enforce least-privilege access and compliance with Defender, Microsoft Entra, and Purview 
* Boost productivity through native integration with Microsoft 365 apps and Work IQ 
* Monitor activity and apply policies from a single, secure registry 

Through its native integration with Microsoft Agent 365, Microsoft Foundry also provides: 

* Foundry-hosted runtime for seamless agent execution 
* Azure Bot Service and Microsoft 365 app integration (such as Microsoft Teams, Outlook, Microsoft 365 Copilot) 
* MCP-connected tools from Microsoft Agent 365 

## Prerequisites 

* Access to the [frontier preview program](https://adoption.microsoft.com/copilot/frontier-program/). 
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd)  
* [Docker](https://www.docker.com/) 
* The [.NET 9.0 SDK](https://dotnet.microsoft.com/download) or later  

## Run the sample

Publish an agent to Agent 365 by running the available script on [GitHub](https://go.microsoft.com/fwlink/?linkid=2343518). The Script will

1. Create a Microsoft Foundry project that supports hosted agents. Working with hosted agents requires that the project has permissions with Azure Container Registry for building and storing Docker images. 

1. Create an application in the project. Applications have stable endpoints and identity that are used to expose your agent to users while retaining the ability to iterate on the implementation inside Microsoft Foundry. For Agent 365, the application needs to be configured to allow requests from Azure Bot Service. 

1. Create an Azure Bot Service, which acts as a relay between agent interactions through the Microsoft 365 ecosystem and the Microsoft Foundry application. The bot needs to be configured with the application's endpoint and its app ID needs to be set to the application's agent blueprint identity. 

1. Create a hosted agent from the sample code. It builds the sample code into a Docker container and registers it as a hosted agent with the project. 

1. Deploy the agent to the application. Hosted agents need to be deployed before they can be used. Deploying it to the application grants it access to the application's identity and configures it to serve requests made to the application. 

1. Publish the application to your organization. To make the agent a usable in Agent 365, the application needs to be published to Microsoft 365 through the Microsoft Foundry API. This API call specifies the metadata of the digital worker and its agent blueprint ID. It also needs to mark the agent as a digital worker. 

    The agent then needs to be [approved by an organization admin](/entra/identity/enterprise-apps/review-admin-consent-requests#review-and-take-action-on-admin-consent-requests-1) before it's available. 
