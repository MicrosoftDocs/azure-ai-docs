---
title: Bring your own cross-resource capacity in Content Understanding
titleSuffix: Foundry Tools
description: Connect an Azure OpenAI or Foundry resource to Content Understanding and configure cross-resource model deployments for analyzer operations.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 03/04/2026
ms.service: azure-ai-content-understanding
ms.topic: how-to
ai-usage: ai-assisted
---

# Bring your own cross-resource capacity in Content Understanding

Use this guide to connect an external Azure OpenAI or Foundry resource to your Content Understanding resource and route model usage through that connected resource. This setup helps you reuse existing model capacity across resources.

## Cross-resource flow overview

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
|  | gpt-4.1 -> connA/gpt41    |                                |
|  +-------------+-------------+                                |
|                |                                              |
|    analyze API | uses default deployment mapping              |
|                v                                              |
|  +---------------------------+                                |
|  | Connected resource        |                                |
|  | (Azure OpenAI or Foundry) |                                |
|  |                           |                                |
|  | deployments:              |                                |
|  | - gpt-4.1                 |                                |
|  | - text-embedding-3-large  |                                |
|  +---------------------------+                                |
|                                                               |
|  Authentication path: API key or Microsoft Entra ID           |
+---------------------------------------------------------------+
```

## Prerequisites

To get started, make sure you have the following resources and permissions:

- An active Azure subscription. If you don't have one, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource created in a [supported region](../language-region-support.md#region-support).
- An Azure OpenAI or Foundry resource with supported chat completion and embeddings deployments. For model and deployment requirements, see [Connect your Content Understanding resource with Foundry models](../concepts/models-deployments.md) and [Service quotas and limits](../service-limits.md#supported-generative-models).
- Access to configure both resources in the Azure portal, including permissions to create connected resources.
- For Microsoft Entra ID authentication, a managed identity enabled on the Content Understanding resource and an assigned role such as `Cognitive Services User` on the connected resource. For more information, see [Security features in Azure Content Understanding in Foundry Tools](../concepts/secure-communications.md).

## Connect an Azure OpenAI or Foundry resource

Connect your model resource from the management center of your Content Understanding resource.

1. Open your Content Understanding resource in the Azure portal.
1. Select **Go to Azure AI Foundry portal**.

  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/open-foundry-portal-from-content-understanding-resource.png" alt-text="Screenshot of selecting Go to Azure AI Foundry portal from the Content Understanding resource.":::

1. Open **Management center**.

  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/open-management-center.png" alt-text="Screenshot of opening Management center in the Azure AI Foundry portal.":::

1. Select **Connected resources**.

  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/open-connected-resources.png" alt-text="Screenshot of the Connected resources page in Management center.":::

1. Select **New connection**.

  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/select-new-connection.png" alt-text="Screenshot of selecting New connection in Connected resources.":::

1. Select **Azure OpenAI** or **Microsoft Foundry**.

1. Search for and select your resource.

  :::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/search-and-select-target-resource.png" alt-text="Screenshot of searching for and selecting the target resource for the connection.":::

1. Select an authentication type, and then select **Add connection**.

After the operation completes, the connection appears in **Connected resources**.

## Choose an authentication method

You can authenticate the connected resource with an API key or with Microsoft Entra ID.

- **API key**: Content Understanding uses the API key from the connected resource.
  - The connected resource must allow API key authentication.
  - If API key authentication is disabled on the connected resource, requests fail.
- **Microsoft Entra ID**: Content Understanding uses the managed identity of the Content Understanding resource.
  - Enable managed identity on the Content Understanding resource.
  - Grant the managed identity access to the connected resource, such as **Cognitive Services User**.

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
    "gpt-4.1": "{ConnectionName}/{DeploymentName}",
    "text-embedding-3-large": "{ConnectionName}/{EmbeddingDeploymentName}"
  }
}
```

:::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/find-connection-name-in-connected-resources.png" alt-text="Screenshot of finding the connection name in Connected resources.":::

:::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/find-deployment-name-in-models-endpoints.png" alt-text="Screenshot of finding deployment names in Models plus endpoints.":::

## Verify the configuration

Test your setup by running the REST quickstart with your configured resource.

1. Follow [Quickstart: Use Azure Content Understanding in Foundry Tools REST API](../quickstart/use-rest-api.md).
1. Run the sample request in [Send a file for analysis](../quickstart/use-rest-api.md#send-a-file-for-analysis).
1. Confirm the operation succeeds by checking [Get analyze result](../quickstart/use-rest-api.md#get-analyze-result) and verifying `status` is `Succeeded`.

If the quickstart request succeeds, your Content Understanding resource is using the connected cross-resource capacity.

:::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/verify-cross-resource-configuration-success.png" alt-text="Screenshot of a successful setup result after applying defaults.":::

## Related content

- [Connect your Content Understanding resource with Foundry models](../concepts/models-deployments.md)
- [Service quotas and limits](../service-limits.md)
- [Language and region support](../language-region-support.md)
