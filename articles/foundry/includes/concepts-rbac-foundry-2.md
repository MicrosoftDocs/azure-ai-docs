---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: meerakurup
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

Use these tabs to explore the differences between the built-in roles, assigned at the Foundry resource level (except for Owner, which is assigned at the subscription level)

# [Owner](#tab/owner)

:::image type="content" source="../media/rbac-foundry/owner.png" alt-text="Diagram shows access for Owner.":::

# [Foundry Owner](#tab/ai-owner)

:::image type="content" source="../media/rbac-foundry/foundry-owner.png" alt-text="Diagram shows access for Foundry Owner.":::

# [Foundry Account Owner](#tab/ai-account-owner)

:::image type="content" source="../media/rbac-foundry/foundry-account-owner.png" alt-text="Diagram shows access for Foundry Account Owner.":::

# [Foundry Project Manager](#tab/ai-project-manager)

:::image type="content" source="../media/rbac-foundry/foundry-project-manager.png" alt-text="Diagram shows access for Foundry Project Manager.":::

# [Foundry User](#tab/ai-user)

:::image type="content" source="../media/rbac-foundry/foundry-user.png" alt-text="Diagram shows access for Foundry User.":::


---

## Sample enterprise RBAC mappings for projects

Here's an example of how to implement role-based access control (RBAC) for an enterprise Foundry resource. 

|Persona|Role and Scope|Purpose|
|---|---|---|
|IT admin|Owner on subscription scope|The IT admin ensures the Foundry resource meets enterprise standards. Assign managers the **Foundry Account Owner** role on the resource to let them create new Foundry accounts. Assign managers the **Foundry Project Manager** role on the resource to let them create projects within an account.|
|Managers|Foundry Account Owner on Foundry resource scope|Managers manage the Foundry resource, deploy models, audit compute resources, audit connections, and create shared connections. They can't build in projects, but they can assign the **Foundry User** role to themselves and others to start building.|
|Team lead or lead developer|Foundry Project Manager on Foundry resource scope|Lead developers create projects for their team and start building in those projects. After you create a project, project owners invite other members and assign the **Foundry User** role.|
|Team members or developers|Foundry User on Foundry project scope and Reader on the Foundry resource scope|Developers build agents in a project with pre-deployed Foundry models and pre-built connections.|
