---
title: Migrate from hub-based to Foundry projects
description: Learn how to migrate from existing hub-based projects to new Azure AI Foundry projects to access the latest platform capabilities, unified workflows, and enhanced governance features.
author: sdgilley
ms.topic: how-to
ms.date: 07/21/2025
ms.author: sgilley
ms.reviewer: deeikele
---

# Migrate from hub-based to Foundry projects

This guide is for existing customers with hub-based projects and explains the steps for switching from a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]to the new [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)] to access the latest platform capabilities.

Azure AI Foundry is transitioning to a unified platform-as-a-service, replacing the previous resource model that required management of multiple Azure services. These changes simplify platform setup and governance, enhance workflows that span multiple models and Foundry tools, and reinforce governance capabilities, as we see AI workloads grow more complex. [Learn more](https://techcommunity.microsoft.com/blog/AIPlatformBlog/build-recap-new-azure-ai-foundry-resource-developer-apis-and-tools/4427241ljQ7vS7hdrIhNLjmw?e=PU9gmv).

> [!IMPORTANT]
> New generative AI and model-centric features will be available only through the AI Foundry resource and its Foundry projects. Currently, some capabilities still require a hub next to your Foundry resource.

## New Foundry projects overview

Foundry projects are designed to unify and simplify the composition of developer workflows, and the management of core building blocks of AI applications:

- Models
- Agents & their tools
- Observability, security and trust

Previously, AI Foundry project's capabilities required the management of multiple Azure resources and SDKs for workflows in the backend to compose these components.

:::image type="content" source="../media/migrate-project/project-structure.png" alt-text="Screenshot of a diagram showing Azure AI Foundry architecture.":::

New capabilities include:

- **Access to Foundry API** which is designed to build and evaluate API-first agentic applications that compose Agents, Evaluations, Models Indexes, Data in a unified experience, and with a consistent contract across model providers.

- **Azure AI Foundry SDK** wraps the Foundry API making it easy to integrate capabilities into code whether your application is built in Python, C#, JavaScript/TypeScript or Java.

- **Agents, Models and Tooling connections** are managed together on Foundry for permission management, networking, cost analysis and policy configuration. Previously certain tools and models were accessed via Azure ML's hub, requiring also the provisioning of additional storage and key vault resources.

- **Projects are now child resources**; they may be assigned their own admin controls like Azure RBAC, but by default share common settings from their parent resource. This principle aims to take IT admins out of the day-to-day loop. Once security, resource connectivity and governance are established at the resource level, as developer you can create your own project as a folder to organize your work.

> [!IMPORTANT]
> Foundry projects feature set are not yet on full parity with hub-based projects. For an up-to-date view on supported features, see [this support matrix](/azure/ai-foundry/what-is-azure-ai-foundry#which-type-of-project-do-i-need).

## How to switch to Foundry project

In the following sections, we will walk step-by-step by how you can move from hub-based projects to Foundry projects:

1. [Locate your existing AI Foundry resource)(#locate)
1. [Create a project](#create-project)
1. (optional) [Recreate connections](#recreate-connections)
1. (optional) [Migrate agents](#migrate-agents)

What can you take forward to the new project type?

- Model deployments
- Data files
- Fine-tuned models
- Assistants
- Vector stores

Limitations:

- Preview Agent's state, including messages, thread, and files cannot be moved. However, you can recreate your agent using code in your new project.
- Open-source model deployments are not yet supported in Foundry projects.

## <a name="locate"></a> 1. Locate your existing AI Foundry resource

Most AI Foundry users will already have an 'AI Foundry' (formerly called 'AI Services') resource, which was previously created alongside your hub-based project to access model deployments.

> [!NOTE]
> If you don't have an existing AI Foundry resource, most common because your hub was using Azure OpenAI for accessing model deployments, you must [create a new AI Foundry resource first](./create-azure-ai-resource.md). You may [connect](./connections-add.md) your existing Azure OpenAI resource for continued access to existing model deployments. Additional configuration steps apply for use with Agent service, see [below](#link-to-bicep-section) and [Agent standard setup](../agents/concepts/standard-agent-setup).

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

Starting with your hub-based project, locate your existing AI Foundry resource:

- Navigate to 'management center' > hub 'connected resources'.

- Find the 'AI Foundry' connection, and follow the link to view its details.

:::image type="content" source="../media/migrate-project/find-resource.png" alt-text="Screenshot of AI Foundry connection details.":::

- Follow the link in the connection details to switch to your Foundry resource in management center.

:::image type="content" source="../media/migrate-project/resource-details.png" alt-text="Screenshot of Foundry resource in management center.":::

# [Azure portal](#tab/azure)

- From your Foundry deployment resource group, locate your resource with 'Azure AI Foundry' resource type. Note that previously this was shown as 'AI Services'.

:::image type="content" source="../media/migrate-project/resource-azure-portal.png" alt-text="Screenshot of Azure AI Foundry resource in Azure Portal.":::

- Follow its link to open its resource overview page.

# [Bicep](#tab/bicep)

- If you use infrastructure-as-code templates such as Bicep (or Azure Resource Manager template, or Terraform), your template will typically contain multiple Azure resources.

- Locate the resource of the *type CognitiveServices/account/kind=AIServices*. This is your 'AI Foundry resource', as it's displayed in Foundry Portal or Azure Portal.

--- 

## <a name="create-project"></a> 2. Create a project to build with agents

New capabilities, including Agent service, are only accessible via projects, which organize your development work as a folder for each use case. You can create multiple of them, to organize the work for use cases with similar setup and connectivity requirements.

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

- Picking up from management center overview, create a project.

:::image type="content" source="../media/migrate-project/create-project.png" alt-text="Screenshot of creating a project in management center.":::

- Post-creation, follow its link, and return to resource build view 'go to project'.

- Alternatively, if you started in the regular resource view, under the `Agents` tab, you'll be automatically prompted to create a new Foundry project.

:::image type="content" source="../media/migrate-project/create-from-agent.png" alt-text="Screenshot of Agents tab prompting to create a new Foundry project.":::

# [Azure portal](#tab/azure)

- Navigate to 'projects' in the left side nav and add your first project.

:::image type="content" source="../media/migrate-project/new-project-azure-portal.png" alt-text="Screenshot of projects navigation in Azure Portal.":::

# [Bicep](#tab/bicep)

- In your template, a project is declared as a child resource under your Foundry resource as shown in [this example](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/42-basic-agent-setup-with-customization).

- By default, in the basic configuration, Agent service uses deployments and storage capabilities that come with your AI Foundry resource.

- Optionally, Agent service supports the ability to use existing Azure OpenAI resources for model deployments, and to bring your own storage resources for storing threads, messages and files. This is also referred as 'Standard' setup. See [this example](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/43-standard-agent-setup-with-customization) for reference Bicep templates.

---

You are now ready to start building agents in general availability and with the latest capabilities. [Get started](/azure/ai-foundry/agents/quickstart?pivots=ai-foundry-portal) using SDK or Agent playground.

:::image type="content" source="../media/migrate-project/agent-playground.png" alt-text="Screenshot of agent building interface.":::

## <a name="recreate-connections"></a> 3. (Optional) Recreate connections

If your hub based project used connections to access tools, data sources or models, you can recreate those on your upgraded Foundry resource, without the use of a hub.

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

  Navigate to 'management center' to [add any connections](/azure/ai-foundry/how-to/connections-add?pivots=fdp-project) to tools and data you used before in your hub-based project.

# [Azure portal](#tab/azure)

Use either the Azure AI Foundry portal or Bicep template to add your connections.

# [Bicep](#tab/bicep)

If you prefer using Bicep templates, see [this repository with examples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/01-connections).

Note that connections are now defined as instances of type *CognitiveServices/account/connections,* and *CognitiveServices/account/project/connections.* Choose account-level connections for shared access across projects.

---

## <a name="migrate-agents"></a>  4. (Optional) Migrate code agents

Any code agents build using the preview of Agent service, require the following upgrades as you move to Agent service in general availability on Foundry projects:

1. Install the [latest version](/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure) of your preferred SDK client.

1. Update your project client to  use the Foundry API.  Instead of a connection string, you'll now use the Azure AI Foundry project endpoint. For example, in Pyton:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    
    project = AIProjectClient(
      endpoint="your_project_endpoint",  # Replace with your endpoint
      credential=DefaultAzureCredential())
    ```

1. Update your script to reflect any class structure changes between the preview and stable SDK packages.

See the [SDK migration guide](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/AGENTS_MIGRATION_GUIDE.md) on how to update your existing code.

## 5. (Optional) Clean up hub-based projects

If you no longer require access to your hub-based projects, delete them from your Azure subscription.

There are some reasons you might want to keep hubs and hub-based projects around in your subscription:

- Access to select features that are not supported yet in Foundry projects, see [this support matrix](/azure/ai-foundry/what-is-azure-ai-foundry#which-type-of-project-do-i-need).

- Use cases that are focused on custom machine learning model training. Hub-based projects as built on Azure ML stack and continue to be accessible via Azure ML Studio/CLI/SDK.

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

- Navigate to management center from a hub-based project.

- Navigate to 'hub' -> overview in left side nav.

- Delete any projects you no longer want to keep.

- Delete your hub.

# [Azure portal](#tab/azure)

- In your resource group, locate your 'AI Hub' resource.

- Azure Portal deletion flow will guide into its deletion and its associated projects.

# [Bicep](#tab/bicep)

- Keep *CognitiveServices/account/kind=AIServices* resource type. This is your Foundry resource.

- Remove *Microsoft.MachineLearningServices/workspace/kind=project* and *Microsoft.MachineLearningServices/workspace/kind=hub* from your template definition.

- Use alternative methods for resource deletion, since this is not supported via Bicep.

---

## Learn more

- [Azure AI Foundry rollout across my organization](/azure/ai-foundry/concepts/planning)

- [Sample Bicep templates](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/01-connections)

- [Sample Terraform templates](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup-terraform)

- [SDK Migration guide](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/AGENTS_MIGRATION_GUIDE.md)
