---
title: Include file
description: Include file
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
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
# Used with ../how-to/create-projects
---

Create multiple [!INCLUDE [fdp-project-name](fdp-project-name.md)]s on an existing `Foundry` resource to enable team collaboration and shared resource access including security, deployments, and connected tools. This setup is ideal in restricted Azure subscriptions where developers need self-serve exploration ability within the setup of a preconfigured environment.

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
| OpenAI SDK and API | ✅ | Responses, Files, Conversations |
| OpenAI Batch, Fine-tuning, Stored completions | ✅ | - |
| Language fine-tuning | ✅ | ✅ |
| Speech fine-tuning | ✅ | - |
| Connections | ✅ | ✅ |

* To add a project to a Foundry resource:
    
    # [Foundry portal](#tab/foundry)
    
    ::: moniker range="foundry-classic"
    
    [!INCLUDE [tip-left-pane](tip-left-pane.md)]
    
    1. [!INCLUDE [version-sign-in](version-sign-in.md)] 
    1. Select either the [!INCLUDE [fdp-project-name](fdp-project-name.md)] or its associated resource.
    1. In the left pane, select **Management center**.
    1. In the resource section, select  **Overview**.
    1. Select **New project** and provide a name.
    
        :::image type="content" source="../media/how-to/projects/second-project.png" alt-text="Screenshot shows how to create a second project on an existing resource.":::
    
    ::: moniker-end
  
    ::: moniker range="foundry"

    The Foundry (new) portal displays only the **default** project for each Foundry resource. You can't create multiple projects, or view any of the nondefault projects in the Foundry (new) portal.
        
    <!-- 1. Select **Operate** in the upper-right navigation.
    1. Select **Admin** in the left pane.
    1. Select the Parent resource you want to add a project to.
    1. Select **Add project**. -->
      
    ::: moniker-end
    
    # [Python SDK](#tab/python)

    ::: moniker range="foundry"
    While this code can add additional projects to a resource, you won't be able to view them in the Foundry (new) portal. Only the default project for a resource is available in the Foundry (new) portal.
    ::: moniker-end
    
    Add this code to your script to create a new project on your existing resource:

    :::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/create_project.py" id="create_additional":::
    
    
    # [Azure CLI](#tab/azurecli)

    ::: moniker range="foundry"
    While this code can add additional projects to a resource, you won't be able to view them in the Foundry (new) portal. Only the default project for a resource is available in the Foundry (new) portal.
    ::: moniker-end

    To add a new project to `my-foundry-resource`:
    
    ```azurecli
     az cognitiveservices account project create \
     --name my-foundry-resource \
     --project-name {new_project_name} \
     --location eastus
    ```

    ---

* If you delete your Foundry resource's default project, the next project created will become the default project. 