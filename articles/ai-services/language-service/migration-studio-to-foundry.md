---
title: Migrate from Azure Language Studio to Microsoft Foundry
titleSuffix: Foundry Tools
description: Learn how to migrate your Azure AI Language projects from Language Studio to Microsoft Foundry, including export, import, and validation steps.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: upgrade-and-migration-article
ms.date: 01/26/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# Migrate from Language Studio to Microsoft Foundry

Azure Language Studio will migrate to Microsoft Foundry on February 16, 2026. All existing capabilities, along with new feature enhancements, are fully available in Microsoft Foundry. After February 16, 2026, Language Studio will no longer be available, but none of your existing projects, data, or service endpoints are impacted. This guide provides step-by-step migration instructions to ensure uninterrupted access to Azure AI Language features and seamless project continuity within the Foundry environment.

## Why migrate to Microsoft Foundry?

Microsoft Foundry offers a unified platform for building, managing, and deploying AI solutions with a wide array of models and tools. Migrating to Foundry provides the following benefits:

* **Unified development experience**. Access all Azure AI Language features alongside other AI services in one environment.
* **Enhanced capabilities**. Use features like **Quick Deploy** for rapid fine-tuning with generative AI.
* **Continuous updates**. Benefit from new features continually added to Foundry.
* **Integration with Foundry Tools**. Build conversational AI applications using the Azure Language `MCP` server, Intent Routing agent, and Exact Question Answering agent.

## Prerequisites

**Before you begin the migration process, ensure that the following resources and permissions are in place to complete the steps in this guide:**

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* **Azure account** with a role that allows you to create resources, such as **Contributor** or **Owner** at the subscription level.

## Migration overview

You can migrate to Microsoft Foundry using one of two approaches:

* **[Option I: Use your existing Language resource](#option-i-start-using-foundry-with-an-existing-language-resource)**. Create a Foundry hub, connect your existing Azure Language resource, and access your projects directly in Foundry. This approach preserves your current resource configuration and requires no data export or import.

* **[Option II: Migrate to a new Foundry resource](#option-ii-migrate-to-a-new-foundry-resource)**. Export your projects from Language Studio and import them into a new Foundry resource. This approach consolidates your AI capabilities into a single resource and provides access to both Foundry classic and the new Foundry experiences.



---



## Option I: Start using Foundry with an existing Language resource

If you have an existing Azure Language resource with custom projects, you can continue using it within Microsoft Foundry by creating a Foundry hub and connecting your resource. This approach preserves your current resource configuration and allows you to access your projects in Foundry without exporting or reimporting data.

> [!IMPORTANT]
> This configuration is supported only in Foundry classic.
> Microsoft Foundry can automatically provision and manage Azure Language resources. However, manually configuring your hub-based Foundry resource in the Azure portal ensures correct role-based access control (RBAC) assignments, managed identity configurations, and network security settings.

### Step 1: Create a Foundry hub and project

To use Azure AI Language capabilities with a Language resource, you need a Foundry hub and an associated hub-based project. Set up these resources using either of the following approaches:

* **Azure portal**. Create a hub first, then create an associated project. This approach provides explicit control over resource configuration settings. For step-by-step instructions, *see* [Create a hub in the Azure portal](/azure/ai-foundry/how-to/create-azure-ai-resource?view=foundry-classic&preserve-view=true&tabs=portal#create-a-hub-in-the-azure-portal). After creating your hub, navigate to your hub resource, select **Projects** or **Management center** under **Resource management**, and then select **+ New project**.

* **Microsoft Foundry portal**. Create a hub-based project directly in Microsoft Foundry, which automatically provisions the underlying hub. This approach streamlines setup by handling hub creation automatically. For step-by-step instructions, *see* [Create a project](/azure/ai-foundry/how-to/create-projects?view=foundry-classic&preserve-view=true&tabs=foundry).

### Step 2: Confirm prerequisites and region support

The following table lists the custom capabilities available in Microsoft Foundry along with their required prerequisites and supported regions. Ensure these prerequisites are in place before proceeding with the migration.

|Capability|Required prerequisites|Region support|
|---|---|---|
|[**Conversational Language Understanding (CLU)**](conversational-language-understanding/quickstart.md)|&bullet; Foundry resource and Foundry project created in the Azure portal.|Limited to select Azure regions. Some regions support both authoring and prediction; others support prediction only. For more information, *see* [Region support for CLU](concepts/regional-support.md).|
|[**Custom Question Answering (CQA)**](question-answering/quickstart/sdk.md)|&bullet; Foundry resource and Foundry project created in the Azure portal.</br>&bullet; Azure AI Search resource connected to your hub or hub-based project via the Foundry Management Center. For more information, *see* [Create a new connection](/azure/ai-foundry/how-to/connections-add?view=foundry-classic&preserve-view=true&tabs=foundry-portal#create-a-new-connection).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|[**Orchestration workflow**](orchestration-workflow/quickstart.md)|&bullet; Foundry resource and Foundry project, or Language resource and Foundry hub-based project.</br>&bullet; A `CLU` or `CQA` project created in the same resource.|Limited to select Azure regions. Some regions support both authoring and prediction; others support prediction only. For more information, *see* [Region support for Orchestration workflow](concepts/regional-support.md).|
|[**Custom Named Entity Recognition (CNER)**](custom-named-entity-recognition/quickstart.md)|&bullet; Language resource with a storage account linked during resource creation.</br>&bullet; Foundry hub-based project created in the Azure portal.|Limited to select Azure regions. Some regions support both authoring and prediction; others support prediction only. For more information, *see* [Region support for CNER](concepts/regional-support.md).|

### Step 3: Connect your Azure Language resource to your Foundry hub

> [!IMPORTANT]
> This step is required only if you're using an existing Azure Language resource with a Foundry hub-based project.

To access and manage your existing Language resource projects in Microsoft Foundry, you must establish a connection between your Azure Language resource and your Foundry hub. This connection enables Microsoft Foundry to authenticate with your resources and provides access to your custom models, training data, and deployed endpoints.

1. Sign in to [**Microsoft Foundry**](https://ai.azure.com/) using your Azure account.
1. Select or create the project where you want to connect your Language resource.
1. In the bottom left corner, select **Management Center**.
1. Under **Connected resources**, select **+ New connection**.
1. Select **Azure Language** or **Foundry** as the resource type.
1. Select your Azure Language resource or Foundry resource from the list.
1. Select **Add connection**.

For more information, *see* [Connect Foundry Tools to a Foundry project](/azure/ai-foundry/how-to/connections-add?view=foundry-classic&preserve-view=true&tabs=foundry-portal).

### Step 4: Validate and test your migrated projects

After importing your projects, validate that the migration is successful:

1. **Review project contents**. Verify that all intents, entities, question-answer pairs, and training data are correctly imported.
1. **Test your models**. Use the Foundry test panel to validate model responses.
1. **Deploy and monitor**. Deploy your models and monitor performance to ensure they function as expected.

---

## Option II: Migrate to a new Foundry resource

This option enables you to create a new Foundry resource and migrate your projects by exporting them from Language Studio and importing them into the new environment. With a Foundry resource, you can access both Foundry classic and the new Foundry experiences, and take advantage of the latest features and unified resource management capabilities.

### Step 1: Export your projects from Language Studio

Before migrating to Microsoft Foundry, export all custom projects you want to transfer. The export process preserves your project configuration, training data, and model settings for import into Foundry:

:::image type="content" source="media/export-studio-project.png" alt-text="Screenshot of Export Studio Project button.":::

#### Export a Custom Question Answering project

1. Sign in to [Language Studio](https://language.azure.com/).
1. Select the Azure Language resource containing the project you want to export.
1. Navigate to **Custom Question Answering**.
1. On the **Projects** page, select the project to export.
1. Choose the export format (**Excel** or **TSV**). The file is exported as a **`.zip`** file containing your project contents.

#### Export a Conversational Language Understanding, Custom Named Entity Recognition, Custom Text Classification, or Orchestration Workflow project

1. Sign in to [Language Studio](https://language.azure.com/).
1. Select the Azure Language resource containing your CLU project.
1. Navigate to your project.
1. On the project home page, select your project from the right page ribbon area.
1. Select **Download config file** to download the project as a **`config.json`** file.

### Step 2: Set up your Foundry environment

Before migrating your Azure Language projects to Microsoft Foundry, you need to complete several configuration tasks:

* **Configure Azure resources**. Create the required Foundry or Language resources in the Azure portal.
* **Establish access control**. Assign the appropriate role-based access control (RBAC) permissions to your resources.
* **Verify region availability**. Confirm that your target capabilities are supported in your chosen Azure region.

The following sections outline the necessary prerequisites and permissions for custom model training (fine-tuning) in Microsoft Foundry.

> [!IMPORTANT]
> This configuration is supported in both Foundry classic and new Foundry.
> Microsoft Foundry can automatically provision and manage Foundry resources. However, manually configuring your Foundry resource for Language capabilities in the Azure portal ensures correct role-based access control (RBAC) assignments, managed identity configurations, and network security settings.

### Create a Foundry resource

To use Azure AI Language capabilities with a Foundry resource, you need both the resource and an associated Foundry project. Set up these resources using either of the following approaches:

* **Azure portal**. Create a Foundry resource first, then create an associated Foundry project. This approach provides explicit control over resource configuration settings. For step-by-step instructions, *see* [Create a Foundry resource in the Azure portal](/azure/ai-services/multi-service-resource?pivots=azportal#create-a-new-microsoft-foundry-resource).

* **Microsoft Foundry portal**. Create a Foundry project directly, which automatically provisions the underlying Foundry resource. This approach streamlines setup by handling resource creation automatically. For step-by-step instructions, *see* [Create a Foundry project](/azure/ai-foundry/how-to/create-projects?view=foundry-classic&preserve-view=true&tabs=foundry).

> [!IMPORTANT]
> **Custom NER (CNER)** requires a storage account to be linked to the Foundry resource during initial resource creation. To establish this link, you must configure the Foundry resource in the [Azure portal](https://portal.azure.com/).

### Step 3: Import your projects into Foundry

After you connect your Language resource or Foundry resource, your existing projects are accessible within Foundry. For new projects or to import exported projects:

#### Import Custom Named Entity Recognition (CNER) project assets

1. In the Azure portal, grant the Foundry managed identity permissions to the storage account by assigning the **Storage Blob Data Contributor** role under **Access Control (IAM)**.
1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/) and select your project.
1. In the left pane, select **Management Center**, and then select **Connected Resources**.
1. Select **+ New connection**, choose **Azure Blob Storage**, and provide a name, subscription, and the specific storage account name.
1. Select **Create**.

You can now train and deploy your `CNER` project using the **Getting started** workflow in Foundry.

#### Import a Custom Question Answering (CQA) project

1. In Foundry, navigate to your project.
1. Select **Fine-tuning** from the left navigation pane.
1. From the main window, select the **AI Service fine-tuning** tab, and then select **+ Fine-tune**.
1. In the **Create CQA fine-tuning task** window, select your connected Azure AI Search resource.
1. Enter a **Name** for your project and select the **Language**.
1. Optionally, update the **Default answer when no answer is returned** field (default is "No answer found").
1. Select **Create**.
1. From the **Getting started** menu, select **Manage sources**.
1. Select **+ Add source**, and then select **Add Files** to upload your exported question-answer pairs.

After adding your source files, you can train and deploy the `CQA` project using the **Getting started** workflow in Foundry.

#### Import a Conversational Language Understanding (CLU) project

1. In Foundry, navigate to your project.
1. Select **Fine-tuning** from the left navigation pane.
1. From the main window, select the **AI Service fine-tuning** tab, and then select **+ Fine-tune**.
1. In the **Create service fine-tuning** window, select the **Conversational language understanding** tab, and then select **Next**.
1. In the **Create CLU fine-tuning task** window, select **Import an existing fine-tuning task**.
1. Enter a name for your imported project.
1. Drag and drop or browse to the `config.json` file you exported from Language Studio.
1. Select **Create** to import the project.

After importing, you can train and deploy your `CLU` project using the **Getting started** workflow in Foundry.

#### Import an Orchestration Workflow project

1. In Foundry, navigate to your project.
1. Select **Fine-tuning** from the left navigation pane.
1. From the main window, select the **AI Service fine-tuning** tab, and then select **+ Fine-tune**.
1. In the **Create fine-tuning task** window, select **Import an existing fine-tuning task**.
1. Enter a name for your imported project.
1. Drag and drop or browse to the **CLU** or **CQA** `config.json` file you exported from Language Studio.
1. Select **Create** to import the project.

After importing, you can train and deploy the Orchestration project using the **Getting started** workflow in Foundry.

### Step 4: Validate and test your imported projects

After importing your projects, validate that the migration is successful:

1. **Review project contents**. Verify that all intents, entities, question-answer pairs, and training data are correctly imported.
1. **Test your models**. Use the Foundry test panel to validate model responses.
1. **Deploy and monitor**. Deploy your models and monitor performance to ensure they function as expected.

> [!IMPORTANT]
>
> **Post-retirement project recreation**. After the February 16, 2026 retirement date, Language Studio export functionality is no longer available. However, you can recreate your custom projects directly in Microsoft Foundry:
>
> * **Existing Azure Language resources**. You can access and continue to use your current Azure Language resources within the Microsoft Foundry portal by creating a **Foundry hub** and an associated **hub-based project**. For more information, *see* [Create a hub in the Azure portal](/azure/ai-foundry/how-to/create-azure-ai-resource?view=foundry-classic&preserve-view=true&tabs=portal#create-a-hub-in-the-azure-portal).
>
> * **Existing Foundry resource-based projects**. You can access your current **Foundry projects** directly in the Microsoft Foundry portal. Alternatively, create a new project and transfer your project assets to the new environment. For more information, *see* [Create a Foundry project](/azure/ai-foundry/how-to/create-projects?view=foundry-classic&preserve-view=true&tabs=foundry).

#### Pretrained models (prebuilt) supported in Microsoft Foundry

The following table lists the pretrained (prebuilt) capabilities available in Microsoft Foundry, required prerequisites, and supported regions. Ensure these prerequisites are in place before proceeding with the migration.

|Capability|Input|Region support|
|---|---|---|
|**Language detection (Foundry classic)**|On the Playground tab, you can choose a text sample from the drop-down menu, choose the paperclip icon to upload your own text, or type your text directly into the sample window. For more information, *see* [**Language detection in Foundry**](language-detection/quickstart.md).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|**Language detection (Foundry new)**|On the Playground tab, you can choose a text sample from the drop-down menu, choose the paperclip icon to upload your own text, or type your text directly into the sample window. For more information, *see* [**Language detection in Foundry**](language-detection/quickstart.md).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|**Key phrase extraction (Foundry classic)**|On the Playground tab, you can upload a file or type text directly into the sample window. For more information, *see* [**Key phrase extraction**](key-phrase-extraction/quickstart.md).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|**Named Entity Recognition (Foundry classic)**|On the Playground tab, you can upload a file or type text directly into the sample window. For more information, *see* [**Named Entity Recognition in Foundry**](named-entity-recognition/quickstart.md).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|**PII detection for text or conversation (Foundry classic)**|On the Playground tab, you can choose a text sample from the drop-down menu, choose the paperclip icon to upload your own text, or type your text directly into the sample window. For more information, *see* [**PII detection in Foundry**](personally-identifiable-information/quickstart.md).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|**PII detection for text (Foundry new)**|On the Playground tab, you can choose a text sample from the drop-down menu, choose the paperclip icon to upload your own text, or type your text directly into the sample window. For more information, *see* [**PII detection in Foundry**](personally-identifiable-information/quickstart.md).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|**Sentiment analysis (Foundry classic)**|On the Playground tab, you can upload a file or type text directly into the sample window. For more information, *see* [**Sentiment analysis in Foundry**](sentiment-opinion-mining/quickstart.md).|Available in all [supported Azure regions](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=cognitive-services).|
|**Summarization (Foundry classic)**</br></br>&bullet;    **Conversation**</br>&bullet;    **Call center**</br>&bullet;    **Text**|On the Playground tab, you can choose a text sample from the drop-down menu, choose the paperclip icon to upload your own text, or type your text directly into the sample window. For more information, *see* [**Summarization in Foundry**](summarization/quickstart.md).|Region support is limited to select Azure regions. For more information, *see* [Region support for summarization](concepts/regional-support.md#summarization)|
|**Text Analytics for health (Foundry classic)**|On the Playground tab, you can upload a file or type text directly into the sample window. A storage account isn't required. For more information, *see* [**Text Analytics for health in Foundry**](text-analytics-for-health/quickstart.md).|Available in all [supported Azure regions](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=cognitive-services).|

#### Custom features supported in Microsoft Foundry

> [!NOTE]
> In the Foundry, a **fine-tuning task** serves as your workspace when customizing your custom models. Previously, a **fine-tuning task** was referred to as a project. You might encounter both terms used interchangeably in some documentation.

|Capability|Required prerequisites|Region support|
|---|---|---|
|[**Conversational Language Understanding (CLU)**](conversational-language-understanding/quickstart.md)|&bullet; Foundry resource and Foundry project created in the Azure portal.|Limited to select Azure regions. Some regions support both authoring and prediction; others support prediction only. For more information, *see* [Region support for Conversational Language Understanding](concepts/regional-support.md#conversational-language-understanding-and-orchestration-workflow).|
|[**Custom Question Answering (CQA)**](question-answering/quickstart/sdk.md)|&bullet; Foundry resource and Foundry project created in the Azure portal.</br>&bullet; Azure AI Search resource connected to your project via the Foundry Management Center. For more information, *see* [Create a new connection](/azure/ai-foundry/how-to/connections-add?view=foundry-classic&preserve-view=true&tabs=foundry-portal#create-a-new-connection).|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|[**Custom Question Answering agent**](question-answering/how-to/deploy-agent.md)|&bullet; Foundry resource and Foundry project created in the Azure portal.</br>&bullet; Azure AI Search resource connected to your project via the Foundry Management Center. For more information, *see* [Create a new connection](/azure/ai-foundry/how-to/connections-add?view=foundry-classic&preserve-view=true&tabs=foundry-portal#create-a-new-connection).</br>&bullet; Deployed knowledge base.</br>&bullet; Deployed Azure OpenAI model in Microsoft Foundry.</br>&bullet; API key connected to your project.|Available in supported Azure regions. For more information, *see* [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).|
|[**Custom Named Entity Recognition (CNER)**](custom-named-entity-recognition/quickstart.md)|&bullet; Language resource with a storage account **linked during resource creation** in the Foundry portal.</br>&bullet; Foundry project created in the Azure portal.|Limited to select Azure regions. Some regions support both authoring and prediction; others support prediction only. For more information, *see* [Region support for CNER](concepts/regional-support.md#custom-named-entity-recognition).|
|[**Orchestration Workflow**](orchestration-workflow/quickstart.md)|&bullet; Foundry resource and Foundry project, or Language resource and Foundry hub-based project.</br>&bullet; A `CLU` or `CQA` project created in the same resource.|Limited to select Azure regions. Some regions support both authoring and prediction; others support prediction only. For more information, *see* [Region support for Orchestration workflow](concepts/regional-support.md#conversational-language-understanding-and-orchestration-workflow).|

> [!NOTE]
> The following Azure AI Language features aren't available in the Microsoft Foundry portal. To use these capabilities, call the [**Azure Language REST API**](/rest/api/language/) directly:
>
> * [**Custom Text Classification**](/azure/ai-services/language-service/custom-text-classification/quickstart?tabs=multi-classification). For regional availability, *see* [Region support for Custom Text Classification](concepts/regional-support.md).
> * [**Entity linking**](/azure/ai-services/language-service/entity-linking/quickstart?tabs=windows&pivots=rest-api). Available in all [supported Azure regions](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=cognitive-services).

## Troubleshooting

If you encounter issues during the migration process, use the following guidance to diagnose and resolve common problems. For issues not covered here, consult the [Azure AI Language documentation](overview.md) or contact [Azure Support](https://azure.microsoft.com/support/).

### Connection issues

If you encounter issues connecting your Language resource to Foundry:

* Verify that you have the correct role assignments (Cognitive Services User or higher).
* Ensure the Language resource and Foundry project are in compatible regions.
* Check that managed identity is properly configured.

### Import failures

If project import fails:

* Verify the export file format matches the expected import format.
* Check for any data corruption in the exported `.zip` or `config,json` file.
* Ensure the project name doesn't conflict with existing projects.

## Related content

* [Azure Language role-based access control](concepts/role-based-access-control.md)

* [Steps to assign an Azure role](/azure/role-based-access-control/role-assignments-steps)

* [Configure your environment for Azure AI resources and permissions](concepts/configure-azure-resources.md)

* [Connect Foundry Tools to a Foundry project](/azure/ai-services/connect-services-foundry-portal#connect-foundry-tools-after-you-create-a-project)
