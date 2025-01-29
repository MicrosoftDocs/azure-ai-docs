---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 11/13/2024
---

### RBAC roles

Make sure both developers and end users have the following permissions: 

* `Microsoft.MachineLearningServices/workspaces/agents/read`
* `Microsoft.MachineLearningServices/workspaces/agents/action`
* `Microsoft.MachineLearningServices/workspaces/agents/delete`

If you want to create custom permissions, make sure they have: 

* `agents/*/read` 
* `agents/*/action` 
* `agents/*/delete` 