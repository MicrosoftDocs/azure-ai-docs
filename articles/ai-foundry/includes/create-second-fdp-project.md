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


Create multiple [!INCLUDE [fdp-project-name](fdp-project-name.md)]s on an existing `AI Foundry` resource to enable team collaboration and shared resource access including security, deployments, and connected tools. This setup is ideal in restricted Azure subscriptions where developers need self-serve exploration ability within the setup of a pre-configured environment.

:::image type="content" source="../media/how-to/projects/projects-multi-setup.png" alt-text="Diagram shows how a team could share resource access with multiple projects on a Foundry resource.":::

[!INCLUDE [fdp-project-name](fdp-project-name.md)]s as Azure child resources may get assigned their own access controls, but share common settings such as network security, deployments, and Azure tool integration from their parent resource.

While not all Foundry capabilities support organizing work in projects yet, your resource's first "default" project is more powerful. You can identify it by the tag "default" in UX experiences and the resource property "is_default" when using code options.

| Feature | Default project | Other projects |
|--|--|--|
| Model inference | ✅ | ✅ |
| Playgrounds | ✅ | ✅ |
| Agents | ✅ | ✅ |
| Evaluations | ✅ | ✅ |
| Tracing | ✅ | ✅ |
| Datasets | ✅ | ✅ |
| Indexes | ✅ | ✅ |
| Foundry SDK and API | ✅ | ✅ |
| Content understanding | ✅ | ✅ |
| OpenAI SDK and API | ✅ | - |
| OpenAI Batch, Fine-tuning, Stored completions | ✅ | - |
| Language fine-tuning | ✅ | ✅ |
| Speech fine-tuning | ✅ | - |
| Connections | ✅ | ✅ |

* To add a project to a Foundry resource:
    
    # [Azure AI Foundry portal](#tab/ai-foundry)
    
    [!INCLUDE [tip-left-pane](tip-left-pane.md)]
    
    1. In [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), select either the [!INCLUDE [fdp-project-name](fdp-project-name.md)] or its associated resource.
    1. In the left pane, select **Management center**.
    1. In the resource section, select  **Overview**.
    1. Select **New project** and provide a name.
    
        :::image type="content" source="../media/how-to/projects/second-project.png" alt-text="Screenshot shows how to create a second project on an existing resource.":::
    
    
    # [Python SDK](#tab/python)
    
    Add this code to your script to create a new project on your existing resource:

    :::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/create_project.py" id="create_additional":::
    
    
    # [Azure CLI](#tab/azurecli)
    
    <!-- Use your existing values for {my_resource_group} and {foundry_resource_name} to add another project to the resource:
    
    ```azurecli
     az cognitiveservices account project create --resource-group {my_resource_group} --name {my_project_name} --account-name {foundry_resource_name} 
    ```
     -->
    CLI commands not currently available for creating a [!INCLUDE [fdp-project-name](fdp-project-name.md)].

    ---

* If you delete your Foundry resource's default project, the next project created will become the default project. 
