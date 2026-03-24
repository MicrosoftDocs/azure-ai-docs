---
title: Include file
description: Include file
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 03/24/2026
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include
  - classic-and-new
---

This code uses the variables and `client` connection from the prerequisites. To delete a single project:

```python
client.projects.begin_delete(
    resource_group_name, foundry_resource_name, foundry_project_name
)
```

References: [CognitiveServicesManagementClient](/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.CognitiveServicesManagementClient).

Delete a Foundry resource and all of its projects:

```python
# Delete projects
projects = client.projects.list(resource_group_name, foundry_resource_name)

for project in projects: 
    print("Deleting project:", project.name)
    client.projects.begin_delete(resource_group_name, foundry_resource_name,
        project_name=project.name.split('/')[-1]
    ).wait()

# Delete resource
print("Deleting resource:", foundry_resource_name)
client.accounts.begin_delete(resource_group_name, foundry_resource_name).wait()
```

References: [CognitiveServicesManagementClient](/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.CognitiveServicesManagementClient).
