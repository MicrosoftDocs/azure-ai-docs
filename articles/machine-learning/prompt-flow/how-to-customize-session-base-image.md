---
title: Customize base image for compute session in prompt flow
titleSuffix: Azure Machine Learning
description: Learn how to create a custom base image for a compute session in prompt flow with Azure Machine Learning studio.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - build-2024
  - dev-focus
ai-usage: ai-assisted
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 03/12/2026
ms.update-cycle: 365-days
---

# Customize a  base image for compute session

Before you begin, make sure you're familiar with [Docker](https://www.docker.com/) and [Azure Machine Learning environments](../concept-environments.md).

## Step 1: Prepare the Docker context

### Create `image_build` folder

In your local environment, create a folder that contains the following files. The folder structure should look like this:

```
|--image_build
|  |--requirements.txt
|  |--Dockerfile
|  |--environment.yaml
```

### Define your required packages in `requirements.txt`

**Optional**: Add packages in private PyPI repository.

Use the following command to download your packages locally: `pip wheel <package_name> --index-url=<private pypi> --wheel-dir <local path to save packages>`

Open the `requirements.txt` file and add your extra packages and their specific versions. For example:

```
###### Requirements with Version Specifiers ######
numpy == 2.2.0              # Version Matching. Must be version 2.2.0
requests >= 2.31.0          # Minimum version 2.31.0
coverage != 3.5             # Version Exclusion. Anything except version 3.5
pydantic ~= 2.0             # Compatible release. Same as >= 2.0, == 2.*
<path_to_local_package>     # reference to local pip wheel package
```

For more information about structuring the `requirements.txt` file, see [Requirements file format](https://pip.pypa.io/en/stable/reference/requirements-file-format/) in the pip documentation.

### Define the `Dockerfile`

Create a `Dockerfile` and add the following content, then save the file:

```
FROM <Base_image>
COPY ./* ./
RUN pip install -r requirements.txt
```

> [!NOTE]
> Build this Docker image from the prompt flow base image `mcr.microsoft.com/azureml/promptflow/promptflow-runtime:<newest_version>`. If possible, use the [latest version of the base image](https://mcr.microsoft.com/v2/azureml/promptflow/promptflow-runtime/tags/list). 

## Step 2: Create custom Azure Machine Learning environment 

### Define your environment in `environment.yaml`

On your local computer, use the CLI (v2) to create a customized environment based on your Docker image.

> [!NOTE]
> - Make sure to meet the [prerequisites](../how-to-manage-environments-v2.md#prerequisites) for creating environment.
> - Ensure you have [connected to your workspace](../how-to-manage-environments-v2.md?#connect-to-the-workspace).


```shell
az login # if not already authenticated

az account set --subscription <subscription ID>
az configure --defaults workspace=<Azure Machine Learning workspace name> group=<resource group>
```

Open the `environment.yaml` file and add the following content. Replace the <environment_name> placeholder with your desired environment name.

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: <environment_name>
build:
  path: .
```

### Create an environment

```shell
cd image_build
az ml environment create -f environment.yaml --subscription <sub-id> -g <resource-group> -w <workspace>
```

> [!NOTE]
> Building the environment image might take several minutes.
> Building the environment image might take several minutes.

Go to your workspace UI page, then go to the **environment** page, and locate the custom environment you created. 

You can also find the image in the environment detail page and use it as base image for compute session of prompt flow. This image is also used to build environment for flow deployment from UI. To learn more, see [how to specify base image in compute session](how-to-manage-compute-session.md#change-the-base-image-for-compute-session).

To learn more about environment CLI, see [Manage environments](../how-to-manage-environments-v2.md#manage-environments).


## Next steps

- [Develop a prompt flow](how-to-develop-flow.md)
