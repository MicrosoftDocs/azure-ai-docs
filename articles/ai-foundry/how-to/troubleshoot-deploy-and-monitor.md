---
title: How to troubleshoot your deployments and monitors in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: Learn how to troubleshoot and monitor model deployments in Microsoft Foundry portal to quickly resolve errors and optimize performance.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 08/26/2025
ms.reviewer: fasantia
reviewer: santiagxf
ms.author: mopeakande
manager: nitinme
author: msakande

#CustomerIntent: As a developer or data scientist, I want to troubleshoot and monitor model deployments in Microsoft Foundry so that I can quickly resolve errors, optimize performance, and ensure my AI solutions run smoothly.
---

# How to troubleshoot your deployments and monitors in Microsoft Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

This article provides instructions on how to troubleshoot your deployments and monitors in Microsoft Foundry portal. 

## Deployment issues

For general deployment error code reference, see [Troubleshooting online endpoints deployment and scoring](/azure/machine-learning/how-to-troubleshoot-online-endpoints) in the Azure Machine Learning documentation. Much of the information there also applies to Foundry deployments.


### Error: Use of Azure OpenAI models in Azure Machine Learning requires Azure OpenAI in Foundry Models resources

The full error message states: "Use of Azure OpenAI models in Azure Machine Learning requires Azure OpenAI in Foundry Models resources. This subscription or region doesn't have access to this model."

This error means that you might not have access to the particular Azure OpenAI model. For example, your subscription might not have access to the latest GPT model yet or this model isn't offered in the region you want to deploy to. You can learn more about it on [Azure OpenAI in Foundry Models](../../ai-foundry/foundry-models/concepts/models-sold-directly-by-azure.md?toc=/azure/ai-foundry/toc.json&bc=/azure/ai-foundry/breadcrumb/toc.json).

### Error: Out of quota

For more information about managing quota, see:

- [Quota for deploying and inferencing a model](../foundry-models/how-to/deploy-foundry-models.md)
- [Manage Azure OpenAI in Foundry Models quota documentation](/azure/ai-foundry/openai/how-to/quota?tabs=rest)
- [Manage and increase quotas for resources with Foundry](quota.md)

### Error: `ToolLoadError`

After you deploy a prompt flow, you might get the error message: "Tool load failed in 'search_question_from_indexed_docs': (ToolLoadError) Failed to load package tool 'Vector Index Lookup': (HttpResponseError) (AuthorizationFailed)." 

To fix this error, manually assign the **Azure ML Data Scientist** role to your endpoint by following these steps. It might take several minutes for the new role to take effect.

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

1. Go to your project in [Foundry](https://ai.azure.com/?cid=learnDocs) and select **Management center** from the left pane to open the settings page.
1. Under the **Project** heading, select **Overview**.
1. Under **Project properties**, select the link to your resource group to open it in the Azure portal. 
1. Select **Access control (IAM)** from the left pane in the Azure portal.
1. Select **Add role assignment**.
1. Select the **Azure ML Data Scientist** role. You might have to search for it in the search box.
1. Select **Next** to go to the **Members** page.
1. For **Assign access to**, select **Managed Identity**.
1. For **Members**, select **+ Select members**. This action opens up the right pane where you can select managed identities.
    1. Select **Machine learning online endpoint** in the Managed identity dropdown field.
    1. Select your endpoint's name.
    1. Select **Select** to choose the endpoint and close the right pane.
1. Select **Review + assign**. Then select **Review + assign** again to confirm the role assignment.
1. Return to your project in Foundry portal and select **Models + endpoints** from the left pane.
1. On the **Model deployments** page, select your deployment.
1. Test the prompt flow deployment.

### Error: Deployment failure

The full error message is as follows: 

"ResourceNotFound: Deployment failed due to timeout while waiting for Environment Image to become available. Check Environment Build Log in ML Studio Workspace or Workspace storage for potential failures. Image build summary: [N/A]. Environment info: Name: CliV2AnonymousEnvironment, Version: 'Ver', you might be able to find the build log under the storage account 'NAME' in the container 'CONTAINER_NAME' at the Path 'PATH/PATH/image_build_aggregate_log.txt'."

You might come across an `ImageBuildFailure` error. This error happens when the environment (docker image) is being built. For more information about the error, you can check the build log for your `<CONTAINER NAME>` environment. 

This error message refers to a situation where the deployment build failed. You want to read the build log to troubleshoot further. There are two ways to access the build log.

__Option 1: Find the build log for the Azure default blob storage.__

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

1. Go to your project in [Foundry](https://ai.azure.com/?cid=learnDocs) and select **Management center** from the left pane to open the overview page of your hub.
1. In the section for **Connected resources**, select the link to your storage account name. This name should be the name of the storage account listed in the error message you received. 
1. On the details page of the storage account, select **View in Azure portal** to open up the storage account page in the [Azure portal](https://portal.azure.com).
1. Alternatively, go to the Azure portal, and from the home page, select **Storage accounts** from the list of Azure services.
1. Select your storage account from the list. You might want to search for it in the search box to find it quickly.
1. On the storage account page, select **Data Storage** > **Containers** from the left pane.
1. Select the container name that's listed in the error message you received.
1. Select through folders to find the build logs.

__Option 2: Find the build log within Azure Machine Learning studio.__

> [!NOTE]
> This option to access the build log uses [Azure Machine Learning studio](https://ml.azure.com), which is a different portal than [Foundry](https://ai.azure.com/?cid=learnDocs).

1. Go to [Azure Machine Learning studio](https://ml.azure.com).
1. Go to your workspace or hub.
1. Select **Endpoints** from the left pane.
1. Select your endpoint name. It might be identical to your deployment name.
1. Select the link to **Environment** from the deployment section.
1. Select **Build log** at the top of the environment details page.

### Error: `UserErrorFromQuotaService`

The full error message is: "UserErrorFromQuotaService: Simultaneous count exceeded for subscription."

This error message means that the shared quota pool reached the maximum number of requests it can handle. Try again later when the shared quota is freed up for use.

### Question: I deployed a web app but I don't see a way to launch it or find it

We're working on improving the user experience of web app deployment. In the meantime, here's a tip: if your web app launch button doesn't become active after a while, try to deploy it again, using the **update an existing app** option. If you properly deploy the web app, it appears on the dropdown list of your existing web apps.

### Question: I deployed a model but I don't see it in the playground

The playground only supports select models, such as Azure OpenAI models and Llama-2. If the playground supports a model, you see the **Open in playground** button on the model deployment's **Details** page. 

## Related content

- [Foundry overview](../what-is-foundry.md)
- [Azure AI FAQ](../faq.yml)
