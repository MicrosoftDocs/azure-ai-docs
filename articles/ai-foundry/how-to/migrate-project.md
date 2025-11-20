---
title: Migrate From Hub-based to Foundry Projects
description: Learn how to migrate from existing hub-based projects to new Microsoft Foundry projects to access the latest platform capabilities, unified workflows, and enhanced governance features.
author: sdgilley
ms.topic: how-to
ms.date: 09/15/2025
ms.author: sgilley
ms.reviewer: deeikele
ms.service: azure-ai-foundry
---


# Migrate from hub-based to Foundry projects

This guide helps existing customers with [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]s migrate to the new [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]s to access the latest platform capabilities.

Microsoft Foundry is transitioning to a unified platform-as-a-service, replacing the previous resource model that required management of multiple Azure services. As we see AI workloads grow more complex, the [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]:

- Simplifies platform setup and governance
- Enhances workflows that span multiple models and Foundry tools
- Reinforces governance capabilities

[Learn more](https://techcommunity.microsoft.com/blog/AIPlatformBlog/build-recap-new-azure-ai-foundry-resource-developer-apis-and-tools/4427241).

> [!IMPORTANT]
> New generative AI and model-centric features are available only through the Foundry resource and its Foundry projects. Currently, some capabilities still require a hub next to your Foundry resource.  For a comparison of capabilities, see [What type of project do I need?](../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need)

## New Foundry projects overview

Foundry projects are designed to unify and simplify the composition of developer workflows, and the management of core building blocks of AI applications:

- Models
- Agents & their tools
- Observability, security, and trust

Previously, Foundry project's capabilities required the management of multiple Azure resources and SDKs for workflows in the backend to compose these components.

:::image type="content" source="../media/migrate-project/project-structure.svg" alt-text="Screenshot of a diagram showing Foundry architecture.":::

New capabilities include:

- **Access to [Foundry API](/rest/api/aifoundry/aiprojects/)** which is designed to build and evaluate API-first agentic applications that compose Agents, Evaluations, Models Indexes, Data in a unified experience, and with a consistent contract across model providers.

- **[Microsoft Foundry SDK](./develop/sdk-overview.md)** wraps the Foundry API making it easy to integrate capabilities into code whether your application is built in Python, C#, JavaScript/TypeScript or Java.

- **Agents, Models and Tooling connections** are managed together on Foundry for permission management, networking, cost analysis, and policy configuration. Previously certain tools and models were accessed via Azure Machine Learning's hub, requiring also the provisioning of extra storage and key vault resources.

- **Projects are now child resources**; they might be assigned their own admin controls like Azure RBAC, but by default share common settings from their parent resource. This principle aims to take IT admins out of the day-to-day loop. Once security, resource connectivity and governance are established at the resource level, as developer you can create your own project as a folder to organize your work.

> [!IMPORTANT]
> Foundry projects feature set aren't yet on full parity with [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]s. For an up-to-date view on supported features, see [this support matrix](/azure/ai-foundry/what-is-azure-ai-foundry#which-type-of-project-do-i-need).

## How to switch to Foundry project

You'll create new [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]s in the Foundry models resource from your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. This process allows the new projects to access work originally done in the [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].

:::image type="content" source="../media/migrate-project/upgrade.svg" alt-text="Screenshot shows the upgrade path from hub-based to Foundry project types.":::

What can you take forward to the new project type?

- Model deployments
- Data files
- Fine-tuned models
- Assistants
- Vector stores

Limitations:

- Your Preview Agent's state, including messages, thread, and files can't be moved. However, you can recreate your agent using code in your new project.
- Open-source model deployments aren't currently supported in Foundry projects.
- Your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] will not have access to any of the new projects created on the Foundry models resource.

In the following sections, we walk through how you can move from [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]s to [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]s:

1. [Locate your existing Foundry resource](#1-locate-your-existing-foundry-resource)
1. [Create a new [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]](#2-create-your-new-project) on the AI resource.

Once you have your new project, you might want to:

- (Optional) [Recreate connections](#optional-recreate-connections)
- (Optional) [Migrate agents](#optional-migrate-code-agents)

## 1. Locate your existing Foundry resource

Most Foundry users already have an 'Foundry' (formerly called 'AI Services') resource, which was previously created alongside your hub-based project to access model deployments.

> [!NOTE]
> If you don't have an existing Foundry resource, most common because your hub was using Azure OpenAI for accessing model deployments, you must [create a new Foundry resource first](./create-azure-ai-resource.md). You can [connect](./connections-add.md) your existing Azure OpenAI resource for continued access to existing model deployments. Other configuration steps apply for use with Agent service. See details in [Create a project to build with agents (Bicep)](#2-create-your-new-project) and [Agent standard setup](../agents/concepts/standard-agent-setup.md).

# [Foundry portal](#tab/azure-ai-foundry)

1.  In [Foundry portal](https://ai.azure.com/?cid=learnDocs), open your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].
1.  In the left pane, select **Management center**.
1.  Select **Connected resources** under the **Hub** section.
1.  Find the **Foundry models** connection, and select the link to view its details.

    :::image type="content" source="../media/migrate-project/find-resource.png" alt-text="Screenshot of Foundry connection details.":::

1.  Follow the link in the connection details to open your Foundry resource overview page.

    :::image type="content" source="../media/migrate-project/resource-details.png" alt-text="Screenshot of Foundry resource in management center.":::

# [Azure portal](#tab/azure)

1.  In [Azure portal](https://portal.azure.com), select the resource group that contains your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].
1.  Locate your resource with 'Foundry' resource type. (This resource type used to be shown as 'AI Services.')

    :::image type="content" source="../media/migrate-project/resource-azure-portal.png" alt-text="Screenshot of Foundry resource in Azure portal.":::

1. Follow the link to open the Foundry resource overview page.

# [Bicep](#tab/bicep)

1. If you use infrastructure-as-code templates such as Bicep (or Azure Resource Manager template, or Terraform), your template typically contains multiple Azure resources.

1. Locate the resource of the *type CognitiveServices/account/kind=AIServices*. This resource is your 'Foundry resource,' as it's displayed in Foundry portal or Azure portal.

--- 

## 2. Create your new project

New capabilities, including Agent service, are only accessible via projects, which organize your development work as a folder for each use case. You can create multiple of them, to organize the work for use cases with similar setup and connectivity requirements.

# [Foundry portal](#tab/azure-ai-foundry)

You can create a new project in one of two ways:

- In the Management center:

    1. In the left pane, select **Management center** to manage the Foundry resource.
    1. Select **Overview** under the **Resource** section.
    1. Select **New project** to create a project in this resource.  This will create a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)].
    
        :::image type="content" source="../media/migrate-project/create-project.png" alt-text="Screenshot of creating a project in management center.":::
    
    1. Once the project is created, in the left pane, select **Go to project**.

- In the **Agents** section of your resource:

    1. In the left pane, select **Agents**
    1. Since the resource doesn't yet have a project, you are prompted to create one.

        :::image type="content" source="../media/migrate-project/create-from-agent.png" alt-text="Screenshot of Agents tab prompting to create a new Foundry project.":::

# [Azure portal](#tab/azure)

1. In the left pane, select **Projects** under the **Resource management** section.
1. Select **New** to create a new project.
1. Supply a name and select **Create**.

:::image type="content" source="../media/migrate-project/new-project-azure-portal.png" alt-text="Screenshot of projects navigation in Azure portal.":::

# [Bicep](#tab/bicep)

1. In your template, a project is declared as a child resource under your Foundry resource as shown in [this example](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/42-basic-agent-setup-with-customization).

1. By default, in the basic configuration, Agent service uses deployments and storage capabilities that come with your Foundry resource.

1. Optionally, Agent service supports the ability to use existing Azure OpenAI resources for model deployments, and to bring your own storage resources for storing threads, messages, and files. This is also referred as 'Standard' setup. See [this example](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/43-standard-agent-setup-with-customization) for reference Bicep templates.

---

You're now ready to start building agents in general availability and with the latest capabilities. [Get started](/azure/ai-foundry/agents/quickstart?pivots=ai-foundry-portal) using SDK or Agent playground.

:::image type="content" source="../media/migrate-project/agent-playground.png" alt-text="Screenshot of agent building interface.":::

## (Optional) Recreate connections

If your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] used connections to access tools, data sources, or models, you can recreate those connections on your Foundry resource, without the use of a hub.

# [Foundry portal](#tab/azure-ai-foundry)

 In the **Management center**, [add any connections](/azure/ai-foundry/how-to/connections-add) to tools and data you used before in your initial [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].

# [Azure portal](#tab/azure)

You can't add connections in the Azure portal.  Use either the Foundry portal or Bicep template to add your connections.

# [Bicep](#tab/bicep)

If you prefer using Bicep templates, see [this repository with examples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/01-connections).

Connections are now defined as instances of type *CognitiveServices/account/connections,* and *CognitiveServices/account/project/connections.* Choose account-level connections for shared access across projects.

---

## (Optional) Migrate code agents

Any code agents build using the preview of Agent service require the following upgrades as you move to Agent service in general availability on Foundry projects:

1. Install the [latest version](/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure) of your preferred SDK client.

1. Update your project client to  use the Foundry API. Instead of a connection string, you now use the Foundry project endpoint. For example, in Python:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    
    project = AIProjectClient(
      endpoint="your_project_endpoint",  # Replace with your endpoint
      credential=DefaultAzureCredential())
    ```

1. Update your script to reflect any class structure changes between the preview and stable SDK packages.

See the [SDK migration guide](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/AGENTS_MIGRATION_GUIDE.md) on how to update your existing code.

## (Optional) Clean up hub-based projects

If you no longer require access to your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]s, delete them from your Azure subscription.

There are some reasons you might want to keep hubs and [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]s around in your subscription:

- Access to select features that aren't supported yet in [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]s. See [this support matrix](/azure/ai-foundry/what-is-azure-ai-foundry#which-type-of-project-do-i-need).

- Use cases that are focused on custom machine learning model training. A [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] is built on the Azure Machine Learning stack and continues to be accessible via Azure Machine Learning Studio/CLI/SDK.

# [Foundry portal](#tab/azure-ai-foundry)

1. In [Foundry portal](https://ai.azure.com/?cid=learnDocs), open your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. 

1. Select **Management center**.
1. Select **Overview** under the **Hub** section.
1. Select any projects you no longer want to keep.
1. Select **Delete project**.
1. Delete any projects you no longer want to keep.
1. In the **Hub properties** section on the right, select **Delete hub** if you want to delete the hub and all its projects. This link will open the Azure portal for you to delete the hub.

# [Azure portal](#tab/azure)

1. In [Azure portal](https://portal.azure.com), select the resource group that contains your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].
1. Select the link for the **Azure AI hub** resource.
1. Select **Delete** to delete the hub and all its associated projects.

> [!CAUTION]
> Make sure you don't delete the Foundry (AI Services) resource, since this contains your existing deployments, files, fine-tuning jobs, and going forward will manage your Foundry projects.

# [Bicep](#tab/bicep)

1. Keep *CognitiveServices/account/kind=AIServices* resource type. This is your Foundry resource.

1. Remove *Microsoft.MachineLearningServices/workspace/kind=project* and *Microsoft.MachineLearningServices/workspace/kind=hub* from your template definition.

1. Use alternative methods for resource deletion, since this isn't supported via Bicep.

---



## Learn more

- [Foundry rollout across my organization](/azure/ai-foundry/concepts/planning)

- [Sample Bicep templates](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/01-connections)

- [Sample Terraform templates](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup-terraform)

- [SDK Migration guide](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/AGENTS_MIGRATION_GUIDE.md)
