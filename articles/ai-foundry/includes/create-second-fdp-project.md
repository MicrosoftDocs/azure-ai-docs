---
title: Include file
description: Include file
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 04/09/2025
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include
  - build-2024
  - ignite-2024
  - build-aifnd
  - build-2025
---


Create multiple [!INCLUDE [fdp-project-name-plural](fdp-project-name-plural.md)] on an existing `AI Foundry` resource, so you can share your environment with your team for collaboration. 

[!INCLUDE [fdp-project-name-plural](fdp-project-name-plural.md)] as Azure child resources may get assigned their own access controls, but share common settings such as network security, deployments, and Azure tool integration from their parent resource.

Your first project (default project) plays a special role and has access to more features:

| Feature | Default [!INCLUDE [fdp-project-name](fdp-project-name.md)] | Nondefault [!INCLUDE [fdp-project-name](fdp-project-name.md)] |
|--|--|--|
| Model inference | ✅ | ✅ |
| Playgrounds | ✅ | ✅ |
| Agents | ✅ | ✅ |
| Evaluations | ✅ | ✅ |
| Connections | ✅ | ✅ |
| AI Foundry API that works with agents and across models | ✅ | ✅ |
| Project-level isolation of files and outputs | ✅ | ✅ |
| Azure OpenAI with Batch, StoredCompletions, Fine-tuning | ✅ |  |
| Backwards compatible with project-less {account}.cognitiveservices.com data plane API | ✅ |  |
| Content safety | ✅ |  |

* To add a nondefault project to a resource:
    
    # [Azure AI Foundry portal](#tab/ai-foundry)
    
    [!INCLUDE [tip-left-pane](tip-left-pane.md)]
    
    1. In [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), select either the [!INCLUDE [fdp-project-name](fdp-project-name.md)] or its associated resource.
    1. In the left pane, select **Management center**.
    1. In the resource section, select  **Overview**.
    1. Select **New project** and provide a name.
    
        :::image type="content" source="../media/how-to/projects/second-project.png" alt-text="Screenshot shows how to create a second project on an existing resource.":::
    
    
    # [Python SDK](#tab/python)
    
    Add this code to your script to create a new project on your existing 

        :::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="create_additional":::
    
    
    # [Azure CLI](#tab/azurecli)
    
    <!-- Use your existing values for {my_resource_group} and {foundry_resource_name} to add another project to the resource:
    
    ```azurecli
     az cognitiveservices account project create --resource-group {my_resource_group} --name {my_project_name} --account-name {foundry_resource_name} 
    ```
     -->
    CLI commands not currently available for creating a [!INCLUDE [fdp-project-name](fdp-project-name.md)].

    ---

* If you delete your Foundry resource's default project, the next project created will become the default project. 
