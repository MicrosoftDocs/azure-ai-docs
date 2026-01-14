---
title: Distributed GPU training guide (SDK v2)
titleSuffix: Azure Machine Learning
description: Learn best practices for distributed training with supported frameworks, such as PyTorch, DeepSpeed, TensorFlow, and InfiniBand.
#customer intent: As a machine learning engineer, I want to understand how to set up distributed GPU training in Azure Machine Learning so that I can optimize training performance for large-scale models.
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.service: azure-machine-learning
ms.subservice: training
ms.topic: concept-article
ms.date: 01/14/2026
ms.custom: sdkv2, update-code2
---

# Distributed GPU training guide (SDK v2)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

This article describes how to use distributed GPU training code in Azure Machine Learning. You see how to run existing code with tips and examples for PyTorch, DeepSpeed, and TensorFlow. You also learn about accelerating distributed GPU training with InfiniBand.

> [!TIP]
> More than 90% of the time, you should use [distributed data parallelism](concept-distributed-training.md#data-parallelism) as your distributed parallelism type.

## Prerequisite

- Understanding of the basic concepts of [distributed GPU training](concept-distributed-training.md), such as *data parallelism*, *distributed data parallelism*, and *model parallelism*.
- The [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install) with the `azure-ai-ml` version 1.5.0 or later package installed.

## PyTorch

Azure Machine Learning supports running distributed jobs by using PyTorch's native distributed training capabilities, `torch.distributed`.

For data parallelism, the [official PyTorch guidance](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html#comparison-between-dataparallel-and-distributeddataparallel) advises using DistributedDataParallel (DDP) over DataParallel for both single-node and multinode distributed training. PyTorch also recommends using [DistributedDataParallel over the multiprocessing package](https://pytorch.org/docs/stable/notes/cuda.html#use-nn-parallel-distributeddataparallel-instead-of-multiprocessing-or-nn-dataparallel). Therefore, Azure Machine Learning documentation and examples focus on DistributedDataParallel training.

### Process group initialization

The backbone of any distributed training is a group of processes that recognize and can communicate with each other by using a backend. For PyTorch, you create the process group by calling [torch.distributed.init_process_group](https://pytorch.org/docs/stable/distributed.html#torch.distributed.init_process_group) in all distributed processes to collectively form a process group.

```python
torch.distributed.init_process_group(backend='nccl', init_method='env://', ...)
```

The most common communication backends are `mpi`, `nccl`, and `gloo`. For GPU-based training, use `nccl` for the best performance.

To run distributed PyTorch on Azure Machine Learning, use the `init_method` parameter in your training code. This parameter specifies how each process discovers the other processes and how they initialize and verify the process group by using the communication backend. By default, if you don't specify `init_method`, PyTorch uses the environment variable initialization method `env://`.

PyTorch looks for the following environment variables for initialization:

- **MASTER_ADDR**: IP address of the machine that hosts the process with rank `0`.
- **MASTER_PORT**: A free port on the machine that hosts the process with rank `0`.
- **WORLD_SIZE**: The total number of processes. Should be equal to the total number of GPU devices used for distributed training.
- **RANK**: The global rank of the current process. The possible values are `0` to `(<world size> - 1)`.

For more information on process group initialization, see the [PyTorch documentation](https://pytorch.org/docs/stable/distributed.html#torch.distributed.init_process_group).

### Environment variables

Many applications also need the following environment variables:

- **LOCAL_RANK**: The local relative rank of the process within the node. The possible values are `0` to `(<# of processes on the node> - 1)`. This information is useful because many operations such as data preparation only need to be performed once per node, usually on `local_rank = 0`.
- **NODE_RANK**: The rank of the node for multinode training. The possible values are `0` to `(<total # of nodes> - 1)`.

### Run a distributed PyTorch job

You don't need to use a launcher utility like `torch.distributed.launch` to run a distributed PyTorch job. You can:

1. Specify the training script and arguments.
1. Create a `command`, and specify the `type` as `PyTorch` and the `process_count_per_instance` in the `distribution` parameter.

   The `process_count_per_instance` corresponds to the total number of processes you want to run for your job, and should typically equal the number of GPUs per node. If you don't specify `process_count_per_instance`, Azure Machine Learning launches one process per node by default.

Azure Machine Learning sets the `MASTER_ADDR`, `MASTER_PORT`, `WORLD_SIZE`, and `NODE_RANK` environment variables on each node, and sets the process-level `RANK` and `LOCAL_RANK` environment variables.

### PyTorch example

[!Notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/pytorch/distributed-training/distributed-cifar10.ipynb?name=job)]

For the full notebook to run the PyTorch example, see [azureml-examples: Distributed training with PyTorch on CIFAR-10](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/pytorch/distributed-training/distributed-cifar10.ipynb).

## DeepSpeed

Azure Machine Learning supports [DeepSpeed](https://www.deepspeed.ai/tutorials/azure/) as a top-level feature to run distributed jobs with near linear scalability for increased model size and increased GPU numbers.

You can enable DeepSpeed for running distributed training by using either PyTorch distribution or Message Passing Interface (MPI). Azure Machine Learning supports the DeepSpeed launcher to launch distributed training, and autotuning to get optimal `ds` configuration.

You can use a [curated environment](resource-curated-environments.md) with the latest state-of-the-art technologies, including DeepSpeed, ONNX (Open Neural Network Exchange) Runtime (ORT), Microsoft Collective Communication Library (MSSCCL), and PyTorch, for your DeepSpeed training jobs.

### DeepSpeed example

For DeepSpeed training and autotuning examples, see [https://github.com/Azure/azureml-examples/cli/jobs/deepspeed](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/deepspeed).

## TensorFlow

If you use [native distributed TensorFlow](https://www.tensorflow.org/guide/distributed_training) in your training code, such as the TensorFlow 2.x `tf.distribute.Strategy` API, you can launch the distributed job via Azure Machine Learning by using `distribution` parameters or the `TensorFlowDistribution` object.

[!Notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/mnist-distributed/tensorflow-mnist-distributed.ipynb?name=job)]

If your training script uses the parameter server strategy for distributed training, such as for legacy TensorFlow 1.x, you also need to specify the number of parameter servers to use in the job. In the preceding example, you specify `"parameter_server_count" : 1` and `"worker_count": 2` inside the `distribution` parameter of the `command`.

### TF_CONFIG

To train on multiple machines in TensorFlow, you use the `TF_CONFIG` environment variable. For TensorFlow jobs, Azure Machine Learning sets the `TF_CONFIG` variable correctly for each worker before running your training script.

You can access `TF_CONFIG` from your training script if you need to by using `os.environ['TF_CONFIG']`.

The following example sets `TF_CONFIG` on a chief worker node:

```json
TF_CONFIG='{
    "cluster": {
        "worker": ["host0:2222", "host1:2222"]
    },
    "task": {"type": "worker", "index": 0},
    "environment": "cloud"
}'
```

### TensorFlow example

For the full notebook to run a TensorFlow example, see [tensorflow-mnist-distributed-example](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/mnist-distributed/tensorflow-mnist-distributed.ipynb).

<a name="accelerating-distributed-gpu-training-with-infiniband"></a>
## InfiniBand

As you increase the number of virtual machines (VMs) that train a model, the time required to train that model should decrease in linear proportion to the number of training VMs. For instance, if training a model on one virtual machine (VM) takes 100 seconds, training the same model on two VMs should take 50 seconds, training the model on four VMs should take 25 seconds, and so on.

InfiniBand can help you attain this linear scaling by enabling low-latency, GPU-to-GPU communication across nodes in a cluster. InfiniBand requires specialized hardware to operate, such as the Azure VM NC-, ND-, or H-series. These VMs have Remote Direct Memory Access (RDMA)-capable VMs with Single Root I/O Virtualization (SR-IOV) and InfiniBand support.

These VMs communicate over the low-latency and high-bandwidth InfiniBand network, which performs better than Ethernet-based connectivity. SR-IOV for InfiniBand enables near bare-metal performance for any MPI library, as used by many distributed training frameworks and tools like NVIDIA Collective Communications Library (NCCL).

These Stock Keeping Units (SKUs) are intended to meet the needs of computationally intensive, GPU-accelerated machine-learning workloads. For more information, see [Accelerating Distributed Training in Azure Machine Learning with SR-IOV](https://techcommunity.microsoft.com/t5/azure-ai/accelerating-distributed-training-in-azure-machine-learning/ba-p/1059050).

Typically, only VM SKUs with *r* in their names, referring to RDMA, contain the required InfiniBand hardware. For instance, the VM SKU `Standard_NC24rs_v3` is InfiniBand-enabled, but `Standard_NC24s_v3` isn't. The specs for these two SKUs are largely the same except for the InfiniBand capabilities. Both SKUs have 24 cores, 448-GB RAM, 4 GPUs of the same SKU, and so on. For more information about RDMA- and InfiniBand-enabled machine SKUs, see [High performance compute](/azure/virtual-machines/sizes-hpc#rdma-capable-instances).

>[!NOTE]
>The older-generation machine SKU `Standard_NC24r` is RDMA-enabled, but doesn't contain the SR-IOV hardware required for InfiniBand.

If you create an `AmlCompute` cluster using one of these RDMA-capable, InfiniBand-enabled sizes, the OS image comes with the Mellanox OpenFabrics Enterprise Distribution (OFED) driver required to enable InfiniBand preinstalled and preconfigured.

## Related content

* [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md)
* [Reference architecture for distributed deep learning training in Azure](/azure/architecture/reference-architectures/ai/training-deep-learning)
* [Troubleshoot environment issues](how-to-troubleshoot-environments.md)
