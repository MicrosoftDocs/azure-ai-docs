---
title: Bring your own cross-resource capacity in Content Understanding
titleSuffix: Foundry Tools
description: Connect an Azure OpenAI or Foundry resource to Content Understanding and configure cross-resource model deployments for analyzer operations.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 08/03/2026
ms.service: azure-content-understanding-foundry-tools
ms.topic: how-to
ai-usage: ai-assisted
---

# Bring your own cross-resource capacity in Content Understanding

Connect an external Azure OpenAI or Foundry resource to your Content Understanding resource. Route model usage through the connected resource to reuse existing capacity.

## Prerequisites

- An active Azure subscription. If you don't have one, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource created in a [supported region](../language-region-support.md#region-support).
- An Azure OpenAI or Foundry resource with supported chat completion and embeddings deployments. For model and deployment requirements, see [Connect your Content Understanding resource with Foundry models](../concepts/models-deployments.md) and [Service quotas and limits](../service-limits.md#supported-generative-models).
- Access to configure both resources in the Azure portal, including permissions to create connected resources and add role assignments.
- One of the following supported authentication configurations:
    - **API key** authentication with key-based authentication and public network access enabled on the connected resource.
    - **Account Managed Identity** authentication with a system-assigned managed identity enabled on the Content Understanding resource.

## Review the cross-resource flow

Use this high-level diagram to understand how Content Understanding uses a connected resource for model inference.

```text
+---------------------------------------------------------------+
| Azure subscription                                            |
|                                                               |
|  +---------------------------+                                |
|  | Content Understanding     |                                |
|  | resource                  |                                |
|  |                           |                                |
|  | defaults:                 |                                |
|  | gpt-5.2 -> connA/gpt52    |                                |
|  +-------------+-------------+                                |
|                |                                              |
|    analyze API | uses default deployment mapping              |
|                v                                              |
|  +---------------------------+                                |
|  | Connected resource        |                                |
|  | (Azure OpenAI or Foundry) |                                |
|  |                           |                                |
|  | deployments:              |                                |
|  | - gpt-5.2                 |                                |
|  | - text-embedding-3-large  |                                |
|  +---------------------------+                                |
|                                                               |
|  Authentication path: API key or Account Managed Identity     |
+---------------------------------------------------------------+
```

## Connect an Azure OpenAI or Foundry resource

Connect your model resource from the management center of your Content Understanding resource.

> [!NOTE] 
> The portal might require a project to open the management center, but the connection must be associated with the resource, not under a specific project.

1. Open the Foundry resourse  where you're using Content Understanding in the Azure portal.
1. Open the Foundry resource where you're using Content Understanding in the Azure portal.
1. Select **Go to Azure AI Foundry portal**.
  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/foundry-resource-overview-go-to-foundry-portal-button.png" alt-text="Screenshot of the Foundry resource overview page with Go to Foundry portal highlighted.":::
1. Open **Management center**. You need to open management center at the resource level, not the project level.
  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/foundry-overview-open-management-center.png" alt-text="Screenshot of the Foundry overview page with Open in management center highlighted.":::
1. Select **Connected resources**.
  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/manage-connected-resources-connected-resources-button.png" alt-text="Screenshot of the Management center navigation with Connected resources highlighted.":::
1. Select **New connection**.
  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/foundry-project-overview-open-in-management-center-new-connection-button.png" alt-text="Screenshot of the Manage connected resources page with New connection highlighted.":::
1. Select **Azure OpenAI** or **Microsoft Foundry**.
  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/add-connection-external-assets-select-azure-openai-or-microsoft-foundry.png" alt-text="Screenshot of the Add a connection to external assets dialog with Azure OpenAI and Microsoft Foundry highlighted.":::
1. Search for and select your resource.
  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/connect-microsoft-foundry-resource-search-select-and-add-connection.png" alt-text="Screenshot of the Connect a Microsoft Foundry resource dialog with resource search and Add connection controls.":::
1. Select a supported authentication type, and then select **Add connection**.

   Authentication details:

    - **API key**: Content Understanding uses the API key from the connected resource.
        - The connected resource must allow API key authentication.
        - The public endpoint of the connected resource must be available. API key authentication isn't supported when the connected resource restricts access to selected networks or a virtual network.
    - **Account Managed Identity**: Content Understanding uses the system-assigned managed identity of the Content Understanding resource.
        - Enable the system-assigned managed identity on the Content Understanding resource.
        - Complete the role assignment in [Grant access to the connected resource](#grant-access-to-the-connected-resource).
   :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/connect-microsoft-foundry-resource-connecting-status.png" alt-text="Screenshot of the Connect a Microsoft Foundry resource dialog showing Connecting status.":::

   After the operation completes, the connection appears in **Connected resources**.
   :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/manage-connected-resources-resource-added.png" alt-text="Screenshot showing the connected resource listed in Connected resources after setup.":::

Creating the connection doesn't grant the Content Understanding resource access to the connected resource.

## Grant access to the connected resource

If you select **Account Managed Identity**, grant the Content Understanding resource's system-assigned managed identity access to the connected resource.

1. In the Azure portal, open the connected Azure OpenAI or Foundry resource.
1. Select **Access control (IAM)**.
1. Select **Add** > **Add role assignment**.
1. Select the **Cognitive Services User** role.
1. For **Assign access to**, select **Managed identity**, and then select **Select members**.
1. Select the system-assigned managed identity of your Content Understanding resource.
1. Select **Review + assign**.

For more information about managed identities, see [Security features in Azure Content Understanding in Foundry Tools](../concepts/secure-communications.md).

## Configure network access

Configure network access on the connected resource for the authentication type that you selected:

- **API key** requires public network access to the connected resource.
- **Account Managed Identity** supports a connected resource that uses selected networks. On the connected resource's **Networking** page, select **Allow Azure services on the trusted services list to access this account**, and then save the change.

## Set default deployments for cross-resource usage

Set resource defaults so analyzers can use the connected deployment with the `{ConnectionName}/{DeploymentName}` format.

Before you start:

- Get the **connection name** from **Connected resources**.
- Get the **deployment name** from **Models + endpoints** in the connected resource.

Use the defaults API to set model deployments:

```http
PATCH {endpoint}/contentunderstanding/defaults?api-version=2025-11-01
Content-Type: application/json

{
  "modelDeployments": {
    "prebuilt-analyzer-completion": "MyConnection/MyGPTDeployment",
    "prebuilt-analyzer-embedding": "MyConnection/MyEmbeddingsDeployment"
  }
}
```

## Verify the configuration

Choose one of the following options to verify your setup.

### Option 1: Verify with Content Understanding Studio

1. Follow [Quickstart: Try out Content Understanding Studio](../quickstart/content-understanding-studio.md) with the primary resource.
1. In Studio, run a prebuilt analyzer on a sample file.
1. Confirm the analysis completes and returns structured results in the results pane.

### Option 2: Verify with the REST quickstart

1. Follow [Quickstart: Use Azure Content Understanding in Foundry Tools REST API](../quickstart/use-rest-api.md).
1. Run the sample request in [Send a file for analysis](../quickstart/use-rest-api.md#send-a-file-for-analysis).
1. Confirm the operation succeeds by checking [Get analyze result](../quickstart/use-rest-api.md#get-analyze-result) and verifying `status` is `Succeeded`.

If either verification path succeeds, your Content Understanding resource is using the connected cross-resource capacity.

## Related content

- [Connect your Content Understanding resource with Foundry models](../concepts/models-deployments.md)
- [Service quotas and limits](../service-limits.md)
- [Language and region support](../language-region-support.md)
