---
author: s-polly
ms.service: azure-machine-learning
ms.topic: include
ms.date: 09/20/2022
ms.author: scottpolly
---

Run this code to connect to your Azure Machine Learning workspace. 

Replace your Subscription ID, Resource Group name, and Workspace name in the following code. To find these values:

1. Sign in to [Azure Machine Learning studio](https://ml.azure.com).
1. Open the workspace you wish to use.
1. Select your workspace name in the upper right Azure Machine Learning studio toolbar.
1. Copy the value for workspace, resource group, and subscription ID into the code.  

[!INCLUDE [sdk v2](./machine-learning-sdk-v2.md)]

[!notebook-python[](~/azureml-examples-main/sdk/python/resources/compute/compute.ipynb?name=subscription_id)]

[!notebook-python[](~/azureml-examples-main/sdk/python/resources/compute/compute.ipynb?name=ml_client)]

`ml_client` is a handler to the workspace that you use to manage other resources and jobs.