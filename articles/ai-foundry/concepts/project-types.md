---
title: Understand Azure AI Foundry projects
titleSuffix: Azure AI Foundry
description: This article describes the different types of projects in Azure AI Foundry, and when to use which type of project.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 03/25/2025
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
# customer intent: As a developer, I want to create an Azure AI Foundry project so I can work with generative AI.
---

# Understand Azure AI Foundry projects

This article describes the different types of projects that are available in Azure AI Foundry. A project is used to organize your work and save state while building customized AI apps

A [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] is hosted by an Azure AI Foundry hub. If your company has an administrative team that has created a hub for you, you can create a project from that hub. If you are working on your own, you can create a project and a default hub will automatically be created for you.

For more information about the projects and hubs model, see [Azure AI Foundry hubs](../concepts/ai-resources.md).

A [!INCLUDE [service-project-name](../includes/service-project-name.md)] is built on an Azure AI Foundry resource. This project type does not use a hub. Something here about the advantages of this new project type.


## Which project type do I need?

In general, you should use a [!INCLUDE [service-project-name](../includes/service-project-name.md)].  You only need to use a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] for features that are not available in a [!INCLUDE [service-project-name](../includes/service-project-name.md)]. 

Most features are available in both project types, but there are a few exceptions.  The table below summarizes the differences between the two project types. Other than these differences, you can use either project type for your work. 

The following table summarizes the differences between the two project types.

| Feature | [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] | [!INCLUDE [service-project-name](../includes/service-project-name.md)] |
| --- | --- | --- |
| Prompt flow | Yes | No |


