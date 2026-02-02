---
title: Manage and optimize costs
titleSuffix: Azure Machine Learning
description: Use these tips to optimize your cost when you build machine learning models in Azure Machine Learning.
ms.reviewer: None
author: s-polly
ms.author: scottpolly
ms.custom: subject-cost-optimization
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: how-to
ms.date: 09/05/2024
#customer intent: As a data scientist or engineer, I want to optimize my cost for training learning modules.
---

# Manage and optimize Azure Machine Learning costs

This article shows you how to manage and optimize costs when you train and deploy machine learning models to Azure Machine Learning.

Use the following tips to help you manage and optimize your compute resource costs.

- Use Azure Machine Learning compute cluster
- Configure your training clusters for autoscaling
- Configure your managed online endpoints for autoscaling
- Set quotas on your subscription and workspaces
- Set termination policies on your training job
- Use low-priority virtual machines (VM)
- Schedule compute instances to shut down and start up automatically
- Use an Azure Reserved VM Instance
- Parallelize training
- Set data retention and deletion policies
- Deploy resources to the same region
- Delete failed deployments

For information on planning and monitoring costs, see [Plan to manage costs for Azure Machine Learning](concept-plan-manage-cost.md).

> [!IMPORTANT]
> Items marked (preview) in this article are currently in public preview.
> The preview version is provided without a service level agreement. We don't recommend preview versions for production workloads. Certain features might not be supported or might have constrained capabilities.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## <a id="use-azure-machine-learning-compute-cluster-amlcompute"></a>Use the Azure Machine Learning compute cluster

With constantly changing data, you need fast and streamlined model training and retraining to maintain accurate models. However, continuous training comes at a cost, especially for deep learning models on GPUs.

Azure Machine Learning users can use the managed Azure Machine Learning compute cluster, also called *AmlCompute*. AmlCompute supports various GPU and CPU options. The AmlCompute is internally hosted on behalf of your subscription by Azure Machine Learning. It provides the same enterprise grade security, compliance, and governance at Azure IaaS cloud scale.

Because these compute pools are inside of Azure's IaaS infrastructure, you can deploy, scale, and manage your training with the same security and compliance requirements as the rest of your infrastructure. These deployments occur in your subscription and obey your governance rules. For more information, see [Plan to manage costs for Azure Machine Learning](concept-plan-manage-cost.md).

## Configure training clusters for autoscaling

Autoscaling clusters based on the requirements of your workload helps reduce your costs so you only use what you need.

AmlCompute clusters are designed to scale dynamically based on your workload. The cluster can be scaled up to the maximum number of nodes you configure. As each job finishes, the cluster releases nodes and scales to your configured minimum node count.

[!INCLUDE [min-nodes-note](includes/machine-learning-min-nodes.md)]

You can also configure the amount of time the node is idle before scale down. By default, idle time before scale down is set to 120 seconds.

- If you perform less iterative experimentation, reduce this time to save costs.
- If you perform highly iterative dev/test experimentation, you might need to increase the time so that you don't pay for constant scaling up and down after each change to your training script or environment.

You can configure AmlCompute clusters for your changing workload requirements by using:

- The Azure portal
- The [AmlCompute SDK class](/python/api/azure-ai-ml/azure.ai.ml.entities.amlcompute)
- [AmlCompute CLI](/cli/azure/ml/compute#az-ml-compute-create)
- [REST APIs](https://github.com/Azure/azure-rest-api-specs/tree/master/specification/machinelearningservices/resource-manager/Microsoft.MachineLearningServices/stable).

## Configure managed online endpoints for autoscaling

Autoscale automatically runs the right amount of resources to handle the load on your application. Managed online endpoints support autoscaling through integration with the Azure Monitor autoscale feature. For more information, see [Online endpoints and deployments for real-time inference](concept-endpoints-online.md).

Azure Monitor autoscaling supports a rich set of rules:

- Metrics-based scaling, for instance, CPU utilization >70%
- Schedule-based scaling, for example, scaling rules for peak business hours
- A combination of the two

For more information, see [Autoscale online endpoints](how-to-autoscale-endpoints.md).

## Set quotas on resources

AmlCompute comes with a quota, or limit, configuration. This quota is by VM family, for example, Dv2 series or NCv3 series. The quota varies by region for each subscription. Subscriptions start with small defaults. Use this setting to control the amount of AmlCompute resources available to be spun up in your subscription. For more information, see [Azure Machine Learning Compute](how-to-manage-quotas.md#azure-machine-learning-compute).

Also, you can configure workspace level quota by VM family for each workspace within a subscription. This approach gives you more granular control on the costs that each workspace might incur and restricts certain VM families. For more information, see [Workspace-level quotas](how-to-manage-quotas.md#workspace-level-quotas).

To set quotas at the workspace level:

1. Open the [Azure portal](https://portal.azure.com) and then select any workspace in your subscription.
1. Select **Support + Troubleshooting** > **Usage + quotas** in the workspace menu.
1. Select **View quota** to view quotas in Azure Machine Learning studio.
1. From this page, you can find your subscription and region in order to set quotas.

   Because this setting affects multiple workspaces, you need privileges at the subscription scope to set the quota.

## Set job termination policies

In some cases, you should configure your training runs to limit their duration or terminate them early. For example, when you use Azure Machine Learning's built-in hyperparameter tuning or automated machine learning.

Here are a few options that you have:

- Define a parameter called `max_run_duration_seconds` in your RunConfiguration to control the maximum duration a run can extend to on the compute you choose, either local or remote cloud compute.
- For *hyperparameter tuning*, define an early termination policy from a Bandit policy, a Median stopping policy, or a Truncation selection policy. To further control hyperparameter sweeps, use parameters such as `max_total_runs` or `max_duration_minutes`. For more information, see [Specify early termination policy](how-to-tune-hyperparameters.md#early-termination).
- For automated machine learning, set similar termination policies using the  `enable_early_stopping` flag. You can also use properties such as `iteration_timeout_minutes` and `experiment_timeout_minutes` to control the maximum duration of a job or for the entire experiment. For more information, see [Exit criteria](how-to-configure-auto-train.md#exit-criteria).

## <a id="low-pri-vm"></a>Use low-priority virtual machines

Azure allows you to use excess unused capacity as Low-Priority VMs across virtual machine scale sets, Batch, and the Machine Learning service. These allocations are preemptible but come at a reduced price compared to dedicated VMs. In general, we recommend that you use Low-Priority VMs for Batch workloads. You should also use them where interruptions are recoverable either through resubmits for Batch Inferencing or through restarts for deep learning training with checkpointing.

Low-Priority VMs have a single quota separate from the dedicated quota value, which is by VM family. For more information about more about AmlCompute quotas, see [Manage and increase quotas ](how-to-manage-quotas.md).

Low-Priority VMs don't work for compute instances, since they need to support interactive notebook experiences.

## Schedule compute instances

When you create a [compute instance](concept-compute-instance.md), the VM stays on so it's available for your work.  

- Enable idle shutdown (preview) to save on cost when the VM is idle for a specified time period. See [Configure idle shutdown](how-to-create-compute-instance.md#configure-idle-shutdown).
- Set up a schedule to automatically start and stop the compute instance (preview) when not in use to save cost. See [Schedule automatic start and stop](how-to-create-compute-instance.md#schedule-automatic-start-and-stop).

## Use reserved instances

Another way to save money on compute resources is Azure Reserved VM Instance. With this offering, you commit to one-year or three-year terms. These discounts range up to 72% of the Standard prices and are applied directly to your monthly Azure bill.

Azure Machine Learning Compute supports reserved instances inherently. If you purchase a one-year or three-year reserved instance, we automatically apply discount against your Azure Machine Learning managed compute.

## Parallelize training

One of the key methods to optimize cost and performance is to parallelize the workload with the help of a parallel component in Azure Machine Learning. A parallel component allows you to use many smaller nodes to run the task in parallel, which allows you to scale horizontally. There's an overhead for parallelization. Depending on the workload and the degree of parallelism that can be achieved, this approach might be an option. For more information, see [ParallelComponent Class](/python/api/azure-ai-ml/azure.ai.ml.entities.parallelcomponent).

## Set data retention and deletion policies

Every time a pipeline runs, intermediate datasets are generated at each step. Over time, these intermediate datasets take up space in your storage account. Consider setting up policies to manage your data throughout its lifecycle to archive and delete your datasets. For more information, see [Optimize costs by automatically managing the data lifecycle](/azure/storage/blobs/lifecycle-management-overview).

## Deploy resources to the same region

Computes located in different regions can experience network latency and increased data transfer costs. Azure network costs are incurred from outbound bandwidth from Azure data centers. To help reduce network costs, deploy all your resources in the region. Provisioning your Azure Machine Learning workspace and dependent resources in the same region as your data can help lower cost and improve performance.

For hybrid cloud scenarios like those that use Azure ExpressRoute, it can sometimes be more cost effective to move all resources to Azure to optimize network costs and latency.

## Delete failed deployments

Managed online endpoints use VMs for the deployments. If you submitted request to create an online deployment and it failed, the request might have passed the stage when compute is created. In that case, the failed deployment would incur charges. When you finish debugging or investigation for the failure, delete the failed deployments to save the cost.

## Related content

- [Plan to manage costs for Azure Machine Learning](concept-plan-manage-cost.md)
- [Manage budgets, costs, and quota for Azure Machine Learning at organizational scale](/azure/cloud-adoption-framework/ready/azure-best-practices/optimize-ai-machine-learning-cost)
