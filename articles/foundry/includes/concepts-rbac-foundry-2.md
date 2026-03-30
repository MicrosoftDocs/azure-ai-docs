---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: meerakurup
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Sample enterprise RBAC mappings for projects

Here's an example of how to implement role-based access control (RBAC) for an enterprise Foundry resource. 

|Persona|Role and Scope|Purpose|
|---|---|---|
|IT admin|Owner on subscription scope|The IT admin ensures the Foundry resource meets enterprise standards. Assign managers the **Azure AI Account Owner** role on the resource to let them create new Foundry accounts. Assign managers the **Azure AI Project Manager** role on the resource to let them create projects within an account.|
|Managers|Azure AI Account Owner on Foundry resource scope|Managers manage the Foundry resource, deploy models, audit compute resources, audit connections, and create shared connections. They can't build in projects, but they can assign the **Azure AI User** role to themselves and others to start building.|
|Team lead or lead developer|Azure AI Project Manager on Foundry resource scope|Lead developers create projects for their team and start building in those projects. After you create a project, project owners invite other members and assign the **Azure AI User** role.|
|Team members or developers|Azure AI User on Foundry project scope and Reader on the Foundry resource scope|Developers build agents in a project with pre-deployed Foundry models and pre-built connections.|
