---
title: What is distributed training?
titleSuffix: Azure Machine Learning
description: Learn what type of distributed training Azure Machine Learning supports and the open source framework integrations available for distributed training.
services: machine-learning
ms.service: azure-machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.subservice: training
ms.custom: build-2023
ms.topic: concept-article
ms.date: 11/24/2025
---

# Distributed training with Azure Machine Learning

In this article, you learn about distributed training and how Azure Machine Learning supports it for deep learning models. 

In distributed training, you split up the workload to train a model and share it among multiple mini processors, called worker nodes. These worker nodes work in parallel to speed up model training. You can use distributed training for traditional machine learning models, but it's better suited for compute and time intensive tasks, like [deep learning](concept-deep-learning-vs-machine-learning.md) for training deep neural networks. 

## Deep learning and distributed training

There are two main types of distributed training: [data parallelism](#data-parallelism) and [model parallelism](#model-parallelism). For distributed training on deep learning models, the [Azure Machine Learning SDK in Python](https://github.com/Azure/azure-sdk-for-python/blob/main/README.md) supports integrations with PyTorch and TensorFlow. Both are popular frameworks that employ data parallelism for distributed training, and can use [Horovod](https://horovod.readthedocs.io/en/latest/summary_include.html) to optimize compute speeds.

* [Distributed training with PyTorch](how-to-train-distributed-gpu.md#pytorch)

* [Distributed training with TensorFlow](how-to-train-distributed-gpu.md#tensorflow)

For machine learning models that don't require distributed training, see [Train models with Azure Machine Learning](concept-train-machine-learning-model.md#python-sdk) for different ways to train models using the Python SDK.

## Data parallelism

Data parallelism is the easiest to implement of the two distributed training approaches, and is sufficient for most use cases.

In this approach, you divide the data into partitions, where the number of partitions equals the total number of available nodes in the compute cluster or [serverless compute](./how-to-use-serverless-compute.md). You copy the model in each of these worker nodes, and each node operates on its own subset of the data. Keep in mind that each node must have the capacity to support the model that's being trained, that is, the entire model has to fit on each node.

The following diagram shows this approach.

:::image type="content" source="media/concept-distributed-training/distributed-training.svg" alt-text="Diagram of data parallelism showing the model copied into worker nodes.":::

Each node independently computes the errors between its predictions for its training samples and the labeled outputs. In turn, each node updates its model based on the errors and must communicate all of its changes to the other nodes to update their corresponding models. Worker nodes need to synchronize the model parameters, or gradients, at the end of the batch computation to ensure they're training a consistent model. 

## Model parallelism

In model parallelism, also known as network parallelism, you segment the model into different parts that run concurrently on different nodes. Each part runs on the same data. The scalability of this method depends on the degree of task parallelization of the algorithm. It's more complex to implement than data parallelism. 

In model parallelism, worker nodes only need to synchronize the shared parameters, usually once for each forward or backward-propagation step. Also, larger models aren't a concern since each node operates on a subsection of the model on the same training data.

## Related content

* [Artificial intelligence (AI) architecture design](/azure/architecture/reference-architectures/ai/training-deep-learning)
* [Distributed GPU training guide](how-to-train-distributed-gpu.md)
