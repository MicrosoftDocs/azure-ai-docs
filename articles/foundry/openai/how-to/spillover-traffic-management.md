---
title: "Manage traffic with spillover for provisioned deployments"
description: "Learn how to configure spillover for provisioned deployments of Azure OpenAI models to automatically route overflow requests to a standard deployment and reduce disruptions during traffic bursts."
#customer intent: As a developer, I want to enable spillover for my provisioned deployments so that I can manage traffic bursts effectively.
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.reviewer: seramasu
reviewer: rsethur
ms.topic: how-to
ms.date: 06/18/2026
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to manage traffic bursts on my provisioned deployments by routing overage traffic to standard deployments using spillover.
---

# Manage traffic with spillover for provisioned deployments

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **New Foundry portal version** - [Switch to version for the classic Foundry portal](../../../foundry-classic/openai/how-to/spillover-traffic-management.md)

[!INCLUDE [how-to-spillover-traffic-management-1](../includes/how-to-spillover-traffic-management-1.md)]

## Enable spillover for all requests on a provisioned deployment

# [Foundry portal](#tab/portal)

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Select the subscription and the resource in the region where you have quota.
1. Select **Discover** in the upper-right navigation, then **Models** in the left pane.
1. Select the **Collections** filter and filter by **Direct from Azure** to see models sold directly by Azure. A selection of these models support the provisioned throughput deployment option.
1. Select the model you want to deploy to open its model card.
1. Select **Deploy** > **Custom settings** to configure your deployment. The **Deployment type** dropdown menu lists provisioned deployment types that are available for the selected model. 

    > [!NOTE]
    > To enable spillover, your account must have at least one active pay-as-you-go deployment that matches the model and version of your current provisioned deployment.

1. Set the **Deployment type** to one of the provisioned options, for example **Global Provisioned Throughput**.

1. Select **Traffic spillover** to enable spillover for your provisioned deployment.


# [REST API](#tab/rest-api)

To enable spillover for all requests on a provisioned deployment, set the deployment property `spilloverDeploymentName` to the standard deployment target for spillover requests. This property can be set during the creation of a new provisioned deployment or added to an existing provisioned deployment. The `spilloverDeploymentName` property must be set to the name of a standard deployment within the same Azure OpenAI resource as your provisioned deployment.

```bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/spillover-ptu-deployment?api-version=2024-10-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"GlobalProvisionedManaged","capacity":100},"properties": {"spilloverDeploymentName": "spillover-standard-deployment", "model":{"format": "OpenAI","name": "gpt-4o-mini","version": "2024-07-18"}}}'
```

A successful request returns HTTP status `200` or `201` with a JSON response containing the deployment details.

**Reference:** [Deployments - Create Or Update](/rest/api/aiservices/accountmanagement/deployments/create-or-update)

---

[!INCLUDE [how-to-spillover-traffic-management-2](../includes/how-to-spillover-traffic-management-2.md)]