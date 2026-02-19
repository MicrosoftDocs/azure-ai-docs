---
title: Troubleshoot SerializationError
titleSuffix: Azure Machine Learning
description: Troubleshooting steps when you get the "cannot import name 'SerializationError'" message.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
author: s-polly
ms.author: scottpolly
ms.reviewer: larryfr
ms.topic: troubleshooting 
ms.date: 03/10/2025
---


# Troubleshoot "cannot import name 'SerializationError'"

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

When using Azure Machine Learning, you might receive one of the following errors:

* `cannot import name 'SerializationError'`
* `cannot import name 'SerializationError' from 'azure.core.exceptions'`

This error might occur when using an Azure Machine Learning environment. For example, when submitting a training job or using AutoML.

## Cause

This problem is caused by a bug in the Azure Machine Learning SDK version 1.42.0.

## Resolution

Update the affected environment to use SDK version 1.42.0.post1 or greater. For a local development environment or compute instance, use the following command:

```bash
pip install azureml-sdk[automl,explain,notebooks]>=1.42.0
```

For more information on updating an Azure Machine Learning environment (for training or deployment), see the following articles:

* [Manage environments in studio](../how-to-manage-environments-in-studio.md#rebuild-an-environment)
* [Create & use software environments](how-to-use-environments.md)

To verify the version of your installed SDK, use the following command:

```bash
pip show azureml-core
```

## Next steps

For more information on updating an Azure Machine Learning environment (for training or deployment), see the following articles:

* [Manage environments in studio](../how-to-manage-environments-in-studio.md#rebuild-an-environment)
* [Create & use software environments](how-to-use-environments.md)