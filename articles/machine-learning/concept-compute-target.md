---
title: Understand compute targets
titleSuffix: Azure Machine Learning
description: Learn how to designate a compute resource or environment to train or deploy your model with Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: compute
ms.topic: concept-article
ms.author: sgilley
author: sdgilley
ms.reviewer: vijetaj
ms.date: 10/17/2024
ms.custom:
  - cliv2
  - build-2023
  - ignite-2023
monikerRange: 'azureml-api-2 || azureml-api-1'
#Customer intent: As a data scientist, I want to understand what a compute target is and why I need it.
---

# What are compute targets in Azure Machine Learning?

A *compute target* is a designated compute resource or environment where you run your training script or host your service deployment. This location might be your local machine or a cloud-based compute resource. Using compute targets makes it easy for you to later change your compute environment without having to change your code.

Azure Machine Learning has varying support across different compute targets. In a typical model development lifecycle, you might:

1. Start by developing and experimenting on a small amount of data. At this stage, use your local environment, such as a local computer or cloud-based virtual machine (VM), as your compute target.
1. Scale up to larger data, or do [distributed training](how-to-train-distributed-gpu.md) by using one of these [training compute targets](#training-compute-targets).
1. After your model is ready, deploy it to a web hosting environment with one of these [deployment compute targets](#compute-targets-for-inference).

The compute resources you use for your compute targets are attached to a [workspace](concept-workspace.md). Compute resources other than the local machine are shared by users of the workspace.

## Training compute targets

As you scale up your training on larger datasets or perform [distributed training](how-to-train-distributed-gpu.md), use Azure Machine Learning compute to create a single- or multi-node cluster that autoscales each time you submit a job. You can also attach your own compute resource, although support for different scenarios might vary.

[!INCLUDE [aml-compute-target-train](includes/aml-compute-target-train.md)]

## Compute targets for inference

When performing inference, Azure Machine Learning creates a Docker container that hosts the model and associated resources needed to use it. This container is then used in a compute target.

The compute target you use to host your model affects the cost and availability of your deployed endpoint. Use this table to choose an appropriate compute target.

:::moniker range="azureml-api-2"
| Compute target | Used for | GPU support | Description |
| ----- | ----- | ----- | ----- |
| [Azure Machine Learning endpoints](~/articles/machine-learning/concept-endpoints.md) | Real-time inference <br><br>Batch inference | Yes | Fully managed computes for real-time (managed online endpoints) and batch scoring (batch endpoints) on serverless compute. |
| [Azure Machine Learning Kubernetes](~/articles/machine-learning/how-to-attach-kubernetes-anywhere.md) | Real-time inference <br><br> Batch inference | Yes | Run inference workloads on on-premises, cloud, and edge Kubernetes clusters. |  
:::moniker-end
:::moniker range="azureml-api-1"
| Compute target | Used for | GPU support | Description |
| ----- | ----- | ----- | ----- |
| [Local web service](~/articles/machine-learning/v1/how-to-deploy-local-container-notebook-vm.md) | Testing/debugging |  &nbsp; | Use for limited testing and troubleshooting. Hardware acceleration depends on use of libraries in the local system. |
| [Azure Machine Learning Kubernetes](~/articles/machine-learning/v1/how-to-deploy-azure-kubernetes-service.md) | Real-time inference | Yes | Run inference workloads in the cloud. |
| [Azure Container Instances](~/articles/machine-learning/v1/how-to-deploy-azure-container-instance.md) | Real-time inference <br><br> Recommended for dev/test purposes only.| &nbsp;  | Use for low-scale CPU-based workloads that require less than 48 GB of RAM. Doesn't require you to manage a cluster.<br><br> Only suitable for models less than 1 GB in size.<br><br> Supported in the designer. |
:::moniker-end

> [!NOTE]
> When choosing a cluster SKU, first scale up and then scale out. Start with a machine that has 150% of the RAM your model requires, profile the result and find a machine that has the performance you need. Once you've learned that, increase the number of machines to fit your need for concurrent inference.

:::moniker range="azureml-api-2"
[Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md).
:::moniker-end
:::moniker range="azureml-api-1"
[Deploy machine learning models to Azure](./v1/how-to-deploy-and-where.md).
:::moniker-end

## Azure Machine Learning compute (managed)

Azure Machine Learning creates and manages the managed compute resources. This type of compute is optimized for machine learning workloads. Azure Machine Learning compute clusters, [serverless compute](how-to-use-serverless-compute.md), and [compute instances](concept-compute-instance.md) are the only managed computes.

There's no need to create serverless compute. You can create Azure Machine Learning compute instances or compute clusters from:

* [Azure Machine Learning studio](how-to-create-attach-compute-studio.md)
* The Python SDK and the Azure CLI:
    * [Compute instance](how-to-create-compute-instance.md)
    * [Compute cluster](how-to-create-attach-compute-cluster.md)
* An Azure Resource Manager template. For an example template, see [Create an Azure Machine Learning compute cluster](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-create-amlcompute).

[!INCLUDE [serverless compute](./includes/serverless-compute.md)]

When created, these compute resources are automatically part of your workspace, unlike other kinds of compute targets.

|Capability  |Compute cluster  |Compute instance  |
|---------|---------|---------|
|Single- or multi-node cluster     |    **&check;**       |    Single node cluster     |
|Autoscales each time you submit a job     |     **&check;**      |         |
|Automatic cluster management and job scheduling     |   **&check;**        |     **&check;**      |
|Support for both CPU and GPU resources     |  **&check;**         |    **&check;**       |

> [!NOTE]
> To avoid charges when the compute is idle:
> * For a compute *cluster*, make sure the minimum number of nodes is set to 0, or use [serverless compute](./how-to-use-serverless-compute.md).
> * For a compute *instance*, [enable idle shutdown](how-to-create-compute-instance.md#configure-idle-shutdown). While stopping the compute instance stops the billing for compute hours, you'll still be billed for disk, public IP, and standard load balancer.

### Supported VM series and sizes

[!INCLUDE [retiring vms](./includes/retiring-vms.md)]

When you select a node size for a managed compute resource in Azure Machine Learning, you can choose from among select VM sizes available in Azure. Azure offers a range of sizes for Linux and Windows for different workloads. To learn more, see [VM types and sizes](/azure/virtual-machines/sizes).

There are a few exceptions and limitations to choosing a VM size:

* Some VM series aren't supported in Azure Machine Learning.
* Some VM series, such as GPUs and other special SKUs, might not initially appear in your list of available VMs.  But you can still use them, once you request a quota change. For more information about requesting quotas, see [Request quota and limit increases](how-to-manage-quotas.md#request-quota-and-limit-increases).

See the following table to learn more about supported series.

| **Supported VM series** | **Category** | **Supported by** |
|------------|------------|------------|------------|
| [DDSv4](/azure/virtual-machines/ddv4-ddsv4-series#ddsv4-series) | General purpose | Compute clusters and instance |
| [Dv2](/azure/virtual-machines/dv2-dsv2-series#dv2-series) | General purpose | Compute clusters and instance |
| [Dv3](/azure/virtual-machines/dv3-dsv3-series#dv3-series) | General purpose | Compute clusters and instance |
| [DSv2](/azure/virtual-machines/dv2-dsv2-series#dsv2-series) | General purpose | Compute clusters and instance |
| [DSv3](/azure/virtual-machines/dv3-dsv3-series#dsv3-series) | General purpose | Compute clusters and instance |
| [EAv4](/azure/virtual-machines/eav4-easv4-series) | Memory optimized | Compute clusters and instance |
| [Ev3](/azure/virtual-machines/ev3-esv3-series) | Memory optimized | Compute clusters and instance |
| [ESv3](/azure/virtual-machines/ev3-esv3-series) | Memory optimized | Compute clusters and instance |
| [FSv2](/azure/virtual-machines/fsv2-series) | Compute optimized | Compute clusters and instance |
| [FX](/azure/virtual-machines/fx-series) | Compute optimized | Compute clusters |
| [H](/azure/virtual-machines/h-series) | High performance compute | Compute clusters and instance |
| [HB](/azure/virtual-machines/hb-series) | High performance compute | Compute clusters and instance |
| [HBv2](/azure/virtual-machines/hbv2-series) | High performance compute | Compute clusters and instance |
| [HBv3](/azure/virtual-machines/hbv3-series) |  High performance compute | Compute clusters and instance |
| [HC](/azure/virtual-machines/hc-series) |  High performance compute | Compute clusters and instance |
| [LSv2](/azure/virtual-machines/lsv2-series) |  Storage optimized | Compute clusters and instance |
| [M](/azure/virtual-machines/m-series) | Memory optimized | Compute clusters and instance |
| [NC](/azure/virtual-machines/nc-series) |  GPU | Compute clusters and instance |
| [NC Promo](/azure/virtual-machines/nc-series) | GPU | Compute clusters and instance |
| [NCv2](/azure/virtual-machines/ncv2-series) | GPU | Compute clusters and instance |
| [NCv3](/azure/virtual-machines/ncv3-series) | GPU | Compute clusters and instance |
| [ND](/azure/virtual-machines/nd-series) | GPU | Compute clusters and instance |
| [NDv2](/azure/virtual-machines/ndv2-series) | GPU | Compute clusters and instance |
| [NV](/azure/virtual-machines/nv-series) | GPU | Compute clusters and instance |
| [NVv3](/azure/virtual-machines/nvv3-series) | GPU | Compute clusters and instance |
| [NCasT4_v3](/azure/virtual-machines/nct4-v3-series) | GPU | Compute clusters and instance |
| [NDasrA100_v4](/azure/virtual-machines/nda100-v4-series) | GPU | Compute clusters and instance |

While Azure Machine Learning supports these VM series, they might not be available in all Azure regions. To check whether VM series are available, see [Products available by region](https://azure.microsoft.com/global-infrastructure/services/?products=virtual-machines).

:::moniker range="azureml-api-1"
> [!NOTE]
> Azure Machine Learning doesn't support all VM sizes that Azure Compute supports. To list the available VM sizes, use the following method:
> * [REST API](/rest/api/azureml/virtual-machine-sizes/list)
:::moniker-end
:::moniker range="azureml-api-2"
> [!NOTE]
> Azure Machine Learning doesn't support all VM sizes that Azure Compute supports. To list the available VM sizes supported by specific compute VM types, use one of the following methods:
> * [REST API](/rest/api/azureml/virtual-machine-sizes/list)
> * The [Azure CLI extension 2.0 for machine learning](how-to-configure-cli.md) command, [az ml compute list-sizes](/cli/azure/ml/compute#az-ml-compute-list-sizes).
:::moniker-end

If you use the GPU-enabled compute targets, it's important to ensure that the correct CUDA drivers are installed in the training environment. Use the following table to determine the correct CUDA version to use:

| **GPU Architecture**  | **Azure VM series** | **Supported CUDA versions** |
|------------|------------|------------|
| Ampere | NDA100_v4 | 11.0+ |
| Turing | NCT4_v3 | 10.0+ |
| Volta | NCv3, NDv2 | 9.0+ |
| Pascal | NCv2, ND | 9.0+ |
| Maxwell | NV, NVv3 | 9.0+ |
| Kepler | NC, NC Promo| 9.0+ |

In addition to ensuring the CUDA version and hardware are compatible, also ensure that the CUDA version is compatible with the version of the machine learning framework you're using:

- For PyTorch, you can check the compatibility by visiting [Pytorch's previous versions page](https://pytorch.org/get-started/previous-versions/).
- For Tensorflow, you can check the compatibility by visiting [Tensorflow's build from source page](https://www.tensorflow.org/install/source#gpu).

### Compute isolation

Azure Machine Learning compute offers VM sizes that are isolated to a specific hardware type and dedicated to a single customer. Isolated VM sizes are best suited for workloads that require a high degree of isolation from other customers' workloads for reasons that include meeting compliance and regulatory requirements. Utilizing an isolated size guarantees that your VM is the only one running on that specific server instance.

The current isolated VM offerings include:

* Standard_M128ms
* Standard_F72s_v2
* Standard_NC24s_v3
* Standard_NC24rs_v3 (RDMA capable)

To learn more about isolation, see [Isolation in the Azure public cloud](/azure/security/fundamentals/isolation-choices).

## Unmanaged compute

Azure Machine Learning doesn't manage an *unmanaged* compute target. You create this type of compute target outside Azure Machine Learning and then attach it to your workspace. Unmanaged compute resources can require extra steps for you to maintain or to improve performance for machine learning workloads.

Azure Machine Learning supports the following unmanaged compute types:

* Remote virtual machines
* Azure HDInsight
* Azure Databricks
* Azure Data Lake Analytics
:::moniker range="azureml-api-1"
* [Azure Kubernetes Service](./v1/how-to-create-attach-kubernetes.md)
* [Azure Synapse Spark pool](v1/how-to-link-synapse-ml-workspaces.md) (deprecated)
:::moniker-end
:::moniker range="azureml-api-2"
* [Kubernetes](how-to-attach-kubernetes-anywhere.md)
:::moniker-end

For more information, see [Manage compute resources](how-to-create-attach-compute-studio.md).

## Related content

:::moniker range="azureml-api-2"
* [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md)
:::moniker-end
:::moniker range="azureml-api-1"
* [Deploy machine learning models to Azure](./v1/how-to-deploy-and-where.md)
:::moniker-end
