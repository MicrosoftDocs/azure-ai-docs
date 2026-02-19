---
title: Manage resources and quotas
titleSuffix: Azure Machine Learning
description: Learn about the quotas and limits on resources for Azure Machine Learning and how to request quota and limit increases.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
author: s-polly
ms.author: scottpolly
ms.reviewer: shshubhe
ms.date: 01/27/2026
ms.topic: how-to
ms.custom:
  - troubleshooting
  - sfi-image-nochange
# Customer intent: As an admin, I want to understand how to manage and increase quotas and limits for resources with Azure Machine Learning.
---

# Manage and increase quotas and limits for resources with Azure Machine Learning

Azure uses quotas and limits to prevent budget overruns due to fraud and to honor Azure capacity constraints. Consider these limits as you scale for production workloads. In this article, you learn about:

- Default limits on Azure resources related to [Azure Machine Learning](overview-what-is-azure-machine-learning.md).
- Creating workspace-level quotas.
- Viewing your quotas and limits.
- Requesting quota increases.

Along with managing quotas and limits, you can learn how to [plan and manage costs for Azure Machine Learning](concept-plan-manage-cost.md) or learn about the [service limits in Azure Machine Learning](resource-limits-capacity.md).

## Special considerations

+ Quotas apply to each subscription in your account. If you have multiple subscriptions, you must request a quota increase for each subscription.

+ A quota is a *credit limit* on Azure resources, *not a capacity guarantee*. If you have large-scale capacity needs, [contact Azure support to increase your quota](#request-quota-and-limit-increases).

+ A quota is shared across all the services in your subscriptions, including Azure Machine Learning. Calculate usage across all services when you're evaluating capacity.
 
  > [!NOTE]
  > Azure Machine Learning compute is an exception. It has a separate quota from the core compute quota. 

+ **Default limits vary by offer category type**, such as free trial, Standard, and virtual machine (VM) series (such as Dv2, F, and G).

## Default resource quotas and limits

This section describes the default and maximum quotas and limits for the following resources:

+ Azure Machine Learning assets
+ Azure Machine Learning computes (including serverless Spark)
+ Azure Machine Learning shared quota
+ Azure Machine Learning online endpoints (both managed and Kubernetes) and batch endpoints
+ Azure Machine Learning pipelines
+ Virtual machines
+ Azure Container Instances
+ Azure Storage

> [!IMPORTANT]
> Limits can change. For the latest information, see [Service limits in Azure Machine Learning](resource-limits-capacity.md).

### Azure Machine Learning assets
The following limits on assets apply on a *per-workspace* basis. 

| **Resource** | **Maximum limit** |
| --- | --- |
| Datasets | 10 million |
| Runs | 10 million |
| Models | 10 million|
| Component | 10 million|
| Artifacts | 10 million |

The maximum **run time** is 30 days and the maximum number of **metrics logged per run** is 1 million.

### Azure Machine Learning Compute
[Azure Machine Learning Compute](concept-compute-target.md#azure-machine-learning-compute-managed) has default quota limits on both the *number of cores* and the *number of unique compute resources* that are allowed per region in a subscription.

> [!NOTE]
> * The *quota on the number of cores* is split by each VM family and cumulative total cores.
> * The *quota on the number of unique compute resources* per region is separate from the VM core quota, as it applies only to the managed compute resources of Azure Machine Learning.

To raise the limits for the following items, [Request a quota increase](#request-quota-and-limit-increases):

* VM family core quotas. To learn more about which VM family to request a quota increase for, see [virtual machine sizes in Azure](/azure/virtual-machines/sizes). For example, GPU VM families start with an "N" in their family name (such as the NCasT4_v3 series).
* Total subscription core quotas
* Cluster quota
* Other resources in this section

Available resources:
+ **Dedicated cores per region** have a default limit of 24 to 300, depending on your subscription offer type. You can increase the number of dedicated cores per subscription for each VM family. Specialized VM families like NCasT4_v3, NC_A100_v4, or NDv2 series start with a default of zero cores. GPUs also default to zero cores.

+ **Low-priority cores per region** have a default limit of 100 to 3,000, depending on your subscription offer type. You can increase the number of low-priority cores per subscription. This limit is a single value across VM families.

+ **Total compute limit per region** has a default limit of 500 per region within a given subscription. You can increase this limit up to a maximum value of 2,500 per region. This limit is shared between training clusters, compute instances, and managed online endpoint deployments. A compute instance is considered a single-node cluster for quota purposes. 

The following table shows more limits in the platform. Reach out to the Azure Machine Learning product team through a **technical** support ticket to request an exception.

| **Resource or Action** | **Maximum limit** |
| --- | --- |
| Workspaces per resource group | 800 |
| Nodes in a single Azure Machine Learning compute (AmlCompute) **cluster** set up as a non communication-enabled pool (that is, can't run MPI jobs) | 100 nodes but configurable up to 65,000 nodes |
| Nodes in a single Parallel Run Step **run** on an Azure Machine Learning compute (AmlCompute) cluster | 100 nodes but configurable up to 65,000 nodes if your cluster is set up to scale as mentioned previously |
| Nodes in a single Azure Machine Learning compute (AmlCompute) **cluster** set up as a communication-enabled pool | 300 nodes but configurable up to 4,000 nodes |
| Nodes in a single Azure Machine Learning compute (AmlCompute) **cluster** set up as a communication-enabled pool on an RDMA enabled VM Family | 100 nodes |
| Nodes in a single MPI **run** on an Azure Machine Learning compute (AmlCompute) cluster | 100 nodes |
| Job lifetime | 21 days<sup>1</sup> |
| Job lifetime on a low-priority node | 7 days<sup>2</sup> |
| Parameter servers per node | 1 |

<sup>1</sup> Maximum lifetime is the duration between when a job starts and when it finishes. Completed jobs persist indefinitely. Data for jobs not completed within the maximum lifetime isn't accessible.

<sup>2</sup> Jobs on a low-priority node can be preempted whenever there's a capacity constraint. Implement checkpoints in your job.

### Azure Machine Learning shared quota

Azure Machine Learning provides a shared quota pool that users across various regions can access to perform testing for a limited amount of time, depending on availability. The specific time duration depends on the use case. By temporarily using quota from the quota pool, you no longer need to file a support ticket for a short-term quota increase or wait for your quota request to be approved before you can proceed with your workload.

You can use the shared quota pool for running Spark jobs and for testing inferencing for models from the Model Catalog for a short time. Before you can deploy these models via the shared quota, you must have an [Enterprise Agreement subscription](/azure/cost-management-billing/manage/create-enterprise-subscription). For more information on how to use the shared quota for online endpoint deployment, see [How to deploy foundation models using the studio](how-to-use-foundation-models.md#deploying-using-the-studio).

Use the shared quota only for creating temporary test endpoints, not production endpoints. For endpoints in production, request dedicated quota by [filing a support ticket](https://ml.azure.com/quota). Billing for shared quota is usage-based, just like billing for dedicated virtual machine families. To opt out of shared quota for Spark jobs, fill out the [Azure Machine Learning shared capacity allocation opt out form](https://forms.office.com/r/n2DFPMeZYW).


### Azure Machine Learning online endpoints and batch endpoints

Azure Machine Learning online endpoints and batch endpoints have resource limits described in the following table.

> [!IMPORTANT]
> These limits are *regional*, meaning that you can use up to these limits for each region you're using. For example, if your current limit for number of endpoints per subscription is 100, you can create 100 endpoints in the East US region, 100 endpoints in the West US region, and 100 endpoints in each of the other supported regions in a single subscription. The same principle applies to all the other limits.

To determine the current usage for an endpoint, [view the metrics](how-to-monitor-online-endpoints.md#use-metrics). 

To request an exception from the Azure Machine Learning product team, use the steps in the [Endpoint limit increases](#endpoint-limit-increases).

| **Resource**&nbsp;&nbsp; | **Limit <sup>1</sup>** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | **Allows exception** | **Applies to** |
| --- | ---- | --- | --- |
| Endpoint name| Endpoint names must <li> Begin with a letter <li> Be 3-32 characters in length  <li> Only consist of letters and numbers <sup>2</sup> <li> For Kubernetes endpoint, the endpoint name plus deployment name must be 6-62 characters in total length | - | All types of endpoints <sup>3</sup> |
| Deployment name| Deployment names must <li> Begin with a letter <li> Be 3-32 characters in length  <li>  Only consist of letters and numbers <sup>2</sup> <li> For Kubernetes endpoint, the endpoint name plus deployment name must be 6-62 characters in total length | - | All types of endpoints <sup>3</sup> |
| Number of endpoints per subscription | 100 | Yes | All types of endpoints <sup>3</sup> |
| Number of endpoints per cluster | 60 | - | Kubernetes online endpoint |
| Number of deployments per subscription | 500 | Yes | All types of endpoints <sup>3</sup>|
| Number of deployments per endpoint | 20 | Yes | All types of endpoints <sup>3</sup> |
| Number of deployments per cluster | 100 | - | Kubernetes online endpoint |
| Number of instances per deployment | 50 <sup>4</sup> | Yes | Managed online endpoint |
| Max request time-out at endpoint level | 180 seconds <sup>5</sup> | - | Managed online endpoint |
| Max request time-out at endpoint level | 300 seconds | - | Kubernetes online endpoint |
| Total requests per second at endpoint level for all deployments  | 500 <sup>6</sup> | Yes | Managed online endpoint |
| Total connections per second at endpoint level for all deployments  | 500 <sup>6</sup> | Yes | Managed online endpoint |
| Total connections active at endpoint level for all deployments  | 500 <sup>6</sup> | Yes | Managed online endpoint |
| Total bandwidth at endpoint level for all deployments  | 5 MBPS <sup>6</sup> | Yes | Managed online endpoint |

<sup>1</sup> This is a regional limit. For example, if current limit on number of endpoints is 100, you can create 100 endpoints in the East US region, 100 endpoints in the West US region, and 100 endpoints in each of the other supported regions in a single subscription. The same principle applies to all the other limits. 

<sup>2</sup> Single dashes like `my-endpoint-name` are accepted in endpoint and deployment names.

<sup>3</sup> Endpoints and deployments can be different types, but limits apply to the sum of all types. For example, the sum of managed online endpoints, Kubernetes online endpoint, and batch endpoint under each subscription can't exceed 100 per region by default. Similarly, the sum of managed online deployments, Kubernetes online deployments, and batch deployments under each subscription can't exceed 500 per region by default.

<sup>4</sup> Azure Machine Learning reserves 20% extra compute resources for performing upgrades. For example, if you request 10 instances in a deployment, you must have a quota for 12. Otherwise, you receive an error. Some VM SKUs are exempt from extra quota. For more information on quota allocation, see [virtual machine quota allocation for deployment](#virtual-machine-quota-allocation-for-deployment).

<sup>5</sup> The request timeout maximum is 180 seconds unless it's a flow (prompt flow) deployment. The maximum request timeout for a flow deployment is 300 seconds. For more information on the timeout with flow deployments, see [deploy a flow in prompt flow](./prompt-flow/how-to-deploy-to-code.md#upstream-request-timeout-issue-when-consuming-the-endpoint).

<sup>6</sup> Requests per second, connections, bandwidth, and related limits. If you request to increase any of these limits, ensure that you estimate or calculate other related limits together.

#### Virtual machine quota allocation for deployment

[!INCLUDE [quota-allocation-online-deployment](includes/quota-allocation-online-deployment.md)]


### Azure Machine Learning pipelines
[Azure Machine Learning pipelines](concept-ml-pipelines.md) have the following limits.

| **Resource** | **Limit** |
| --- | --- |
| Steps in a pipeline | 30,000 |
| Workspaces per resource group | 800 |

### Virtual machines
Each Azure subscription has a limit on the number of virtual machines across all services. Virtual machine cores have a regional total limit and a regional limit per size series. Both limits are separately enforced.

For example, consider a subscription with a US East total VM core limit of 30, an A series core limit of 30, and a D series core limit of 30. You can deploy 30 A1 VMs, or 30 D1 VMs, or a combination of the two that doesn't exceed a total of 30 cores.

You can't raise limits for virtual machines above the values shown in the following table.

[!INCLUDE [azure-subscription-limits-azure-resource-manager](~/reusable-content/ce-skilling/azure/includes/azure-subscription-limits-azure-resource-manager.md)]

### Container Instances

For more information, see [Container Instances limits](/azure/azure-resource-manager/management/azure-subscription-service-limits#container-instances-limits).

### Storage
Azure Storage has a limit of 250 storage accounts per region, per subscription. This limit includes both Standard and Premium storage accounts.


## Workspace-level quotas

Use workspace-level quotas to manage Azure Machine Learning compute target allocation between multiple [workspaces](concept-workspace.md) in the same subscription.

By default, all workspaces share the same quota as the subscription-level quota for VM families. However, you can set a maximum quota for individual VM families on workspaces in a subscription. Quotas for individual VM families let you share capacity and avoid resource contention problems.

1. Go to any workspace in your subscription.
1. In the left pane, select **Usages + quotas**.
1. Select the **Configure quotas** tab to view the quotas.
1. Expand a VM family.
1. Set a quota limit on any workspace listed under that VM family.

You can't set a negative value or a value higher than the subscription-level quota.

[![Screenshot that shows an Azure Machine Learning workspace-level quota.](./media/how-to-manage-quotas/azure-machine-learning-workspace-quota.png)](./media/how-to-manage-quotas/azure-machine-learning-workspace-quota.png)

> [!NOTE]
> You need subscription-level permissions to set a quota at the workspace level.


## View quotas in the studio

1. When you create a new compute resource, you see only the VM sizes that you already have quota to use.  Switch the view to **Select from all options**.  

    :::image type="content" source="media/how-to-manage-quotas/select-all-options.png" alt-text="Screenshot shows select all options to see compute resources that need more quota":::

1. Scroll down until you see the list of VM sizes you don't have quota for.

    :::image type="content" source="media/how-to-manage-quotas/scroll-to-zero-quota.png" alt-text="Screenshot shows list of zero quota":::

1. Use the link to go directly to the online customer support request for more quota.

## View your usage and quotas in the Azure portal

To view your quota for various Azure resources like virtual machines, storage, or network, use the [Azure portal](https://portal.azure.com):

1. On the left pane, select **All services** and then select **Subscriptions** under the **General** category.

1. From the list of subscriptions, select the subscription whose quota you want to view.

1. Under **Settings**, select **Usage + quotas** to view your current quota limits and usage. Use the filters to select the provider and locations. 

You manage the Azure Machine Learning compute quota on your subscription separately from other Azure quotas: 

1. Go to your **Azure Machine Learning** workspace in the Azure portal.

1. On the left pane, in the **Support + troubleshooting** section, select **Usage + quotas** to view your current quota limits and usage.

    [![Screenshot of Azure portal view of current quota limits and usage.](./media/how-to-manage-quotas/portal-view-quota.png)](./media/how-to-manage-quotas/portal-view-quota.png)

1. Select a subscription to view the quota limits. Filter to the region you're interested in.

1. You can switch between a subscription-level view and a workspace-level view.


## Request quota and limit increases

A VM quota increase raises the number of cores per VM family in each region. An endpoint limit increase raises the endpoint-specific limits per subscription in each region. Make sure to choose the right category when you're submitting the quota increase request, as described in the next section.

### VM quota increases

To raise the limit for Azure Machine Learning VM quota above the default limit, request a quota increase from the **Usage + quotas** view or submit a quota increase request from Azure Machine Learning studio.

1. Go to the **Usage + quotas** page by following the instructions in the previous section. View the current quota limits. Select the SKU for which you want to request an increase. 

    [![Screenshot of the VM quota details.](./media/how-to-manage-quotas/mlstudio-request-quota.png)](./media/how-to-manage-quotas/mlstudio-request-quota.png)

1. Enter the quota you want to increase and the new limit value. Select **Submit** to continue. 

    [![Screenshot of the new VM quota request form.](./media/how-to-manage-quotas/mlstudio-new-quota-limit.png)](./media/how-to-manage-quotas/mlstudio-new-quota-limit.png)

### Endpoint limit increases

To raise the endpoint limit, [open an online customer support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest/). When requesting an endpoint limit increase, provide the following information:

1. Select **Service and subscription limits (quotas)** as the **Issue type**.
1. Select the subscription you want to use.
1. Select **Machine Learning Service: Endpoint Limits** as the **Quota type**.
1. On the **Additional details** tab, provide detailed reasons for the limit increase. Select **Enter details** and then provide the limit you'd like to increase and the new value for each limit, the reason for the limit increase request, and **location(s)** where you need the limit increase. 
Be sure to add the following information into the reason for limit increase:
    1. Description of your scenario and workload (such as text, image, and so on).
    1. Rationale for the requested increase.
        1. Provide the target throughput and its pattern (average/peak QPS, concurrent users).
        1. Provide the target latency at scale and the current latency you observe with a single instance.
        1. Provide the VM SKU and number of instances in total to support the target throughput and latency. Provide how many endpoints, deployments, and instances you plan to use in each region.
        1. Confirm if you have a benchmark test that indicates the selected VM SKU and the number of instances that meet your throughput and latency requirement.
        1. Provide the type of the payload and size of a single payload. Network bandwidth should align with the payload size and requests per second.
        1. Provide planned time plan (by when you need increased limits - provide staged plan if possible) and confirm if (1) the cost of running it at that scale is reflected in your budget and (2) the target VM SKUs are approved.
1. Select **Save and continue**.

    [![Screenshot of the endpoint limit details form.](./media/how-to-manage-quotas/quota-details.png)](./media/how-to-manage-quotas/quota-details.png)

    > [!NOTE]
    > This endpoint limit increase request is different from a VM quota increase request. If your request is related to a VM quota increase, follow the instructions in the [VM quota increases](#vm-quota-increases) section.

### Compute limit increases

To increase the total compute limit, [open an online customer support request](https://ms.portal.azure.com/#view/Microsoft_Azure_Support/NewSupportRequestV3Blade/callerWorkflowId/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb/callerName/Microsoft_Azure_Support%2FHelpAndSupportOverview.ReactView). Provide the following information:

1. Select **Technical** as the **Issue type**.
1. Select the subscription you want to use.
1. Select **Machine Learning** as the **Service**.
1. Select the resource you want to use.
1. In the summary, enter "Increase total compute limits".
1. Select **Compute Cluster** as the **Problem type** and select **Cluster does not scale up or is stuck in resizing** as the **Problem subtype**.

    :::image type="content" source="media/how-to-manage-quotas/problem-description.png" alt-text="Screenshot of the problem description tab.":::

1. On the **Additional details** tab, provide the subscription ID, region, new limit (between 500 and 2,500), and business justification if you want to increase the total compute limits in this region.

    :::image type="content" source="media/how-to-manage-quotas/additional-details.png" alt-text="Screenshot of the additional details tab.":::

1. Select **Create** to create a support request ticket.


## Related content

- [Plan and manage costs for Azure Machine Learning](concept-plan-manage-cost.md)
- [Service limits in Azure Machine Learning](resource-limits-capacity.md)
- [Troubleshooting managed online endpoints deployment and scoring](./how-to-troubleshoot-online-endpoints.md)
