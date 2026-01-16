---
title: Manage and increase quotas for hub resources
titleSuffix: Foundry
description: Manage and increase quotas for hub-level resources in Microsoft Foundry. Scale your deployments with detailed steps for quota requests and governance.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
  - dev-focus
ms.topic: how-to
ms.date: 01/16/2026
ms.reviewer: haakar
ms.author: mopeakande
author: msakande
manager: nitinme
ai-usage: ai-assisted
# Hub-focused copy of quota article. Project (fdp) version remains in quota.md
---
# Manage and increase quotas for hub resources

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

> [!TIP]
> An alternate quota article focused on Foundry projects is available. Learn more in [Manage and increase quotas for resources with Microsoft Foundry](quota.md).

This article shows you how to view current quota allocations and request increases for hub-level resources in Foundry. Quotas apply to virtual machines and model deployments and let you manage rate limits across deployments within your subscription.

## Prerequisites

To view and manage quotas, you need:

- An Azure subscription with an active Foundry hub resource. If you don't have one, see [How to create and manage a Microsoft Foundry hub](create-azure-ai-resource.md).
- Access to the Foundry portal with appropriate permissions. You need one of the following Azure role-based access control (RBAC) roles:
  - **Owner** or **Contributor** role on the subscription to request quota increases
  - **Reader** role to view current quota allocations
- For managing compute quotas, make sure you have the required permissions on the Azure Machine Learning workspace that's associated with your hub.


## Special considerations 

Quotas apply per subscription and per region. Request quota increases separately for each subscription and region.

A quota is a credit limit, not a capacity guarantee. For large-scale capacity needs, contact Azure support.

> [!NOTE]
> Foundry compute has a separate quota from the core compute quota.

Default limits vary by offer category, such as Free Trial, serverless API deployment, and VM series.

## Foundry quota 

The following actions in the portal consume quota: 

- Creating a compute instance
- Building a vector index
- Deploying open models from the model catalog

## Foundry compute 

[Foundry compute](./create-manage-compute.md) has default limits on cores and unique compute resources per region.

- Core quota is split by VM family and cumulative total cores.
- Unique compute resources quota is separate.

To raise limits, [request a quota increase](#view-and-request-quotas-in-foundry-portal).

Available resources include:
- Dedicated cores per region: default is 24–300 (depends on subscription). Specialized GPU families might default to 0.
- Total compute limit per region: default is 500. You can increase it up to 2,500. This limit is shared between compute instances and managed online endpoint deployments.

To increase the total compute limit beyond 2,500, submit a support request by going to **Help + support** in the [Azure portal](https://ms.portal.azure.com/):

1. For **Issue type**, select **Technical**.
1. Select your subscription.
1. For **Service type**, select **Machine Learning**.
1. Select your resource.
1. For **Summary**, enter "Increase total compute limits".
1. For **Problem type**, select **Compute instance**.
1. For **Problem subtype**, select **Other features (Setup scripts, shutdown, Identity etc.)**.
1. Provide additional details, and then submit the request.

:::image type="content" source="../media/cost-management/quota-azure-portal-support.png" alt-text="Screenshot of the page to submit compute quota requests in Azure portal." lightbox="../media/cost-management/quota-azure-portal-support.png":::

## View and request quotas in Foundry portal

Use quotas to manage compute and model quota across hubs in the same subscription. By default, all hubs share subscription-level VM family quota. You can set max quota per VM family for granular governance.

1. In the Foundry portal, select **Management center**.
1. Select **Quota**.

   :::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the management center link.":::

1. Expand the groupings to view model deployments and details.

    :::image type="content" source="../media/cost-management/quotas.png" alt-text="Screenshot of the quota entry in the management center section." lightbox="../media/cost-management/quotas.png":::

    :::image type="content" source="../media/cost-management/model-quota.png" alt-text="Screenshot of the Model quota page in Foundry portal, with one of the groupings expanded." lightbox="../media/cost-management/model-quota.png":::

1. Manage your quotas by using the following options:

    - Select the **Show all quota** toggle to display all quotas or only allocated quotas.
    - Select **Group by** to change nesting options (Quota type, Region, Model, or flat view).
    - Select the pencil icon to edit the allocation for a specific quota.
    - Select the **Request quota** link to request increases for standard deployments.
    - Use the interactive charts to view usage insights.
    - Select the **Provisioned Throughput** link to open PTU information and the capacity calculator.

1. Select the **VM Quota** link to view per-region VM family quota and usage, and to request more quota for the selected family.

    > [!TIP]
    > If the VM quota link is missing, you're in a Foundry project view. Use **All resources** then select a hub-type project and return to **Management center**.

    :::image type="content" source="../media/cost-management/vm-quota.png" alt-text="Screenshot of the VM quota page in Foundry portal." lightbox="../media/cost-management/vm-quota.png":::

## Additional quota information

### Container Instances

For Container Instances quota limits, see [Container Instances limits](/azure/azure-resource-manager/management/azure-subscription-service-limits#container-instances-limits)

### Storage

Azure Storage has a limit of 250 storage accounts per region per subscription (standard and premium).

### Shared quota for testing

Shared quota provides a regional pool for temporary testing with foundry models. Use shared quota only for temporary test endpoints. For production workloads, request dedicated quota. Billing is usage-based.

## Troubleshooting

If you encounter issues when viewing or requesting quotas, try these solutions:

| Issue | Solution |
|-------|----------|
| VM quota link is missing | Verify that you're viewing a hub resource, not a Foundry project. In the portal, use **All resources**, select a hub-type resource, and return to **Management center** > **Quota**. |
| Quota increase request was denied | Check whether your subscription supports the requested quota limit in your region. Some VM families and regions have different default and maximum limits. Contact Azure support for region-specific availability. |
| Unable to see quota allocations | Verify you have at least **Reader** role on the subscription. Check whether you're viewing the correct subscription in the portal. |
| Quota increase not reflected after approval | Quota changes can take up to 15 minutes to propagate. Refresh the quota page in the portal. If the issue persists after 24 hours, contact Azure support. |
| Can't request quota beyond 2500 for compute | Use the support request process described in the [Foundry compute](#foundry-compute) section instead of the standard quota request UI. |

For additional assistance, contact [Azure support](https://azure.microsoft.com/support/options/).

## Related content

- [Manage and increase quotas for Foundry projects](./quota.md)
- [Plan to manage costs](./costs-plan-manage.md)
- [Create compute](./create-manage-compute.md)
