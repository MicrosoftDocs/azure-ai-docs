---
title: 'Standard setup and your own vnet overview'
titleSuffix: Azure OpenAI
description: Concept page for how to use your own vnet with the Azure AI Agent Service. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 02/22/2025
author: fosteramanda
ms.author: fosteramanda
ms.custom: azure-ai-agents
---
# Overview Standard setup with Virtual Networking

Azure AI Agent Service offers a standard agent configuration with private networking, allowing you to bring your own (BYO) private virtual network.

> [!NOTE]
> Standard setup with private networking can only be configured by deploying the Bicep template. Once deployed, agents must be created using the SDK. You can't use the UI to create agents in a project with private networking enabled.

### Security Benefits of BYO Virtual Network

- **No public egress**: foundational infrastructure ensures the right authentication and security for your agents and tools, without you having to do trusted service bypass.

- **Container injection**: allows the platform network to host APIs and inject a subnet into your network, enabling local communication of your Azure resources within the same virtual network (VNet).

- **Private resource access**: If your resources are marked as private and nondiscoverable from the Internet, the platform network can still access them, provided the necessary credentials and authorization are in place.

### Known Limitations

- Azure Blob Storage: Using Azure Blob Storage files with the File Search tool isn't supported.
