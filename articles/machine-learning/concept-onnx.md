---
title: ONNX Runtime and Models
titleSuffix: Azure Machine Learning
description: Learn how using the Open Neural Network Exchange (ONNX) can help optimize inference of your machine learning models.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: concept-article
ms.author: scottpolly
author: s-polly
ms.reviewer: kritifaujdar
ms.date: 10/13/2025
#customer intent: As a data scientist, I want to learn about ONNX so I can use it to optimize the inference of my machine learning models.
---

# ONNX and Azure Machine Learning

This article describes how the [Open Neural Network Exchange (ONNX)](https://onnx.ai) can help optimize the inference of your machine learning models. *Inference*, or model scoring, is the process of using a deployed model to generate predictions on production data.

Optimizing machine learning models for inference requires you to tune the model and the inference library to make the most of hardware capabilities. This task becomes complex if you want to get optimal performance on different platforms, such as cloud, edge, CPU, or GPU, because each platform has different capabilities and characteristics. The complexity increases if you need to run models from various frameworks on different platforms. It can be time-consuming to optimize all the different combinations of frameworks and hardware.

A useful solution is to train your model one time in your preferred framework, and then export or convert it to ONNX so it can run anywhere on the cloud or edge. Microsoft and a community of partners created ONNX as an open standard for representing machine learning models. You can export or convert models from [many frameworks](https://onnx.ai/supported-tools) to the standard ONNX format. Supported frameworks include TensorFlow, PyTorch, scikit-learn, Keras, Chainer, MXNet, and MATLAB. You can run models in the ONNX format on various platforms and devices.

This ONNX flow diagram shows available frameworks and deployment options.

:::image type="content" source="media/concept-onnx/onnx.png" alt-text="ONNX flow diagram showing training, converters, and deployment." border="false" lightbox="media/concept-onnx/onnx.png":::

## ONNX Runtime

[ONNX Runtime](https://onnxruntime.ai) is a high-performance inference engine for deploying ONNX models to production. ONNX Runtime is optimized for both cloud and edge, and works on Linux, Windows, and macOS. ONNX is written in C++, but also has C, Python, C#, Java, and JavaScript (Node.js) APIs that you can use in those environments.

ONNX Runtime supports both deep neural networks (DNN) and traditional machine learning models. It integrates with accelerators on different hardware, such as TensorRT on NVIDIA GPUs, OpenVINO on Intel processors, and DirectML on Windows. By using ONNX Runtime, you can benefit from extensive production-grade optimizations, testing, and ongoing improvements.

High-scale Microsoft services such as Bing, Office, and Azure AI use ONNX Runtime. Although performance gains depend on many factors, these Microsoft services average a 2x performance gain on CPU because they use ONNX. ONNX Runtime runs in Azure Machine Learning and other Microsoft products that support machine learning workloads, including:

- **Windows**. ONNX Runtime is built into Windows as part of [Windows Machine Learning](/windows/ai/windows-ml/) and runs on hundreds of millions of devices.
- **Azure SQL**. [Azure SQL Edge](/azure/azure-sql-edge/onnx-overview) and [Azure SQL Managed Instance](/azure/azure-sql/managed-instance/machine-learning-services-overview) use ONNX to run native scoring on data.
- **ML.NET**. For an example, see [Tutorial: Detect objects by using ONNX in ML.NET](/dotnet/machine-learning/tutorials/object-detection-onnx).

## Ways to get ONNX models

You can get ONNX models in several ways:

- [Train a new ONNX model in Azure Machine Learning](https://github.com/onnx/onnx/tree/main/examples) or use [automated machine learning capabilities](concept-automated-ml.md#automl--onnx).
- Convert an existing model from another format to ONNX. For more information, see [ONNX Tutorials](https://github.com/onnx/tutorials).
- Get a pretrained ONNX model from the [ONNX Model Zoo](https://github.com/onnx/models).
- Generate a customized ONNX model from the [Azure AI Custom Vision service](/azure/ai-services/custom-vision-service/).

You can represent many models as ONNX, including image classification, object detection, and text processing models. If you can't convert your model successfully, file a GitHub issue in the repository of the converter you used.

## ONNX model deployment in Azure

You can deploy, manage, and monitor your ONNX models in Azure Machine Learning. By using a standard [MLOps deployment workflow](concept-model-management-and-deployment.md#deploy-models-as-endpoints) with ONNX Runtime, you can create a REST endpoint hosted in the cloud.

## Python packages for ONNX Runtime

Python packages for the [CPU](https://pypi.org/project/onnxruntime) and [GPU](https://pypi.org/project/onnxruntime-gpu) ONNX Runtime are available on [PyPi.org](https://pypi.org). Be sure to review system requirements before installation.

To install ONNX Runtime for Python, use one of the following commands:

```python    
pip install onnxruntime       # CPU build
pip install onnxruntime-gpu   # GPU build
```

To call ONNX Runtime in your Python script, use the following code:

```python
import onnxruntime
session = onnxruntime.InferenceSession("path to model")
```

The documentation accompanying the model usually tells you the inputs and outputs for using the model. You can also use a visualization tool such as [Netron](https://github.com/lutzroeder/Netron) to view the model.

ONNX Runtime lets you query the model metadata, inputs, and outputs, as follows:

```python
session.get_modelmeta()
first_input_name = session.get_inputs()[0].name
first_output_name = session.get_outputs()[0].name
```

To perform inferencing on your model, use `run` and pass in the list of outputs you want returned and a map of the input values. Leave the output list empty if you want all of the outputs. The result is a list of the outputs.

```python
results = session.run(["output1", "output2"], {
                      "input1": indata1, "input2": indata2})
results = session.run([], {"input1": indata1, "input2": indata2})
```

For the complete ONNX Runtime API reference, see the [Python API documentation](https://onnxruntime.ai/docs/api/python/api_summary.html).

## Related content

- [ONNX project website](https://onnx.ai)
- [ONNX GitHub repository](https://github.com/onnx/onnx)
- [ONNX Runtime project website](https://onnxruntime.ai)
- [ONNX Runtime GitHub repository](https://github.com/Microsoft/onnxruntime)
