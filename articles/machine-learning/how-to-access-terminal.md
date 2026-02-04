---
title: How to access a compute terminal
titleSuffix: Azure Machine Learning
description: Learn how to use the terminal on an Azure Machine Learning compute instance for Git operations, to install packages, and to add kernels.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.service: azure-machine-learning
ms.subservice: compute
ms.topic: how-to
ms.date: 02/04/2026
ms.custom: FY25Q1-Linter
#Customer intent: As a data scientist, I want to use the terminal on a compute instance in Azure Machine Learning studio so I can use Git, install packages, and add kernels to the instance.
---

# Access a compute instance terminal

You can use the terminal of a compute instance in your Azure Machine Learning workspace to access Git operations, install packages, and add kernels to the instance.

## Prerequisites

* An Azure subscription. You can create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An Azure Machine Learning workspace. For more information, see [Create workspace resources](quickstart-create-resources.md).

## Access a terminal

To access the terminal from your workspace in [Azure Machine Learning studio](https://ml.azure.com):

1. Select **Notebooks** from the left menu.
1. Select the **Terminal** icon.

   :::image type="content" source="media/how-to-use-terminal/open-terminal-window.png" alt-text="Screenshot that shows how to open the terminal window.":::

1. If a compute instance is running, the terminal window for that instance opens. If no compute instance is running, select the **Start** or **Create** icons next to **Compute** to start or create a compute instance.

   :::image type="content" source="media/how-to-use-terminal/start-or-create-compute.png" alt-text="Screenshot that shows how to start or create a compute instance.":::

### Other ways to access the terminal

You can also access a compute instance terminal in the following ways:

- In Visual Studio Code, select **Terminal** > **New Terminal** from the top menu. For more information about connecting to your workspace from Visual Studio Code, see [Work in Visual Studio Code remotely connected to a compute instance](how-to-work-in-vs-code-remote.md).
- In RStudio or Posit Workbench, select the **Terminal** tab at top left. For more information, see [Add custom applications such as RStudio or Posit Workbench](how-to-create-compute-instance.md?tabs=python#add-custom-applications-such-as-rstudio-or-posit-workbench).
- In JupyterLab, select the **Terminal** tile under **Other** in the Launcher.
- In Jupyter, select **File** > **New** > **Terminal** from the top menu.
- If the compute instance has secure shell (SSH) access enabled, SSH to the machine. If the compute is in a managed virtual network and doesn't have a public IP address, use the `az ml compute connect-ssh` command to connect.

### Copy and paste in the terminal 

, You can copy and paste text between the terminal and Azure Machine Learning studio notebook cells. For Windows, use **Ctrl**+**C** to copy and **Ctrl**+**V**, **Ctrl**+**Shift**+**V**, or **Shift**+**Insert** to paste. For MacOS, use **Cmd**+**C** to copy and **Cmd**+**V** to paste.

<a name=git></a>
## Access Git operations and files

You can access all Git operations from the terminal. All Git files and folders are stored in your workspace file system so you can use them from any compute instance in your workspace.

> [!NOTE]
> Add your files and folders anywhere under `~/cloudfiles/code/Users/<your_user_name>` to ensure they're visible in all your notebook environments.

To integrate Git with your Azure Machine Learning workspace, see [Git integration for Azure Machine Learning](concept-train-model-git-integration.md).

## Install packages

You can use a terminal window.to install packages into the kernel you want to use for your notebook. The default kernel is `python310-sdkv2`.

For Python, you can add and execute package install code in a notebook cell. For package management within a Python notebook, use `%pip` or `%conda` magic functions to automatically install packages into the current running kernel. Don't use `!pip` or `!conda`, which refer to all packages including packages outside the currently running kernel.

You can also install packages directly in Jupyter Notebooks, RStudio, or Posit Workbench. Use the **Packages** tab at lower right or the **Console** tab at upper left. For more information, see [Add custom applications such as RStudio or Posit Workbench](how-to-create-compute-instance.md#add-custom-applications-such-as-rstudio-or-posit-workbench).

## Add new kernels

Run the following code examples in a terminal window to add new kernels to the compute instance.

To install a new Jupyter kernel, run the following code. You can install any of the [available Jupyter kernels](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels).

1. Run the following command to create a new environment named `newenv`.

   ```console
   conda create --name newenv
   ```

1. Activate the environment.

   ```console
   conda activate newenv
   ```

1. Install the `pip` and `ipykernel` packages and create a kernel for the new Conda environment.

   ```console
   conda install pip
   conda install ipykernel
   python -m ipykernel install --user --name newenv --display-name "Python (newenv)"
   ```

To add a new R kernel to the compute instance:

1. Use the terminal window to create a new environment. The following command creates `r_env`.

   ```console
   conda create -n r_env r-essentials r-base
   ```

1. Activate the environment.

   ```console
   conda activate r_env
   ```

1. Run R in the new environment.

   ```console
   R
   ```

1. At the R prompt, run `IRkernel` to create a new kernel named `irenv`.

   ```r
   IRkernel::installspec(name = 'irenv', displayname = 'New R Env')
   ```

1. Quit the R session.

   ```r
   q()
   ```

The new R kernel can take a few minutes to be ready to use. If you see an error saying the kernel is invalid, wait a few minutes and try again.

- For more information about Conda, see [Using R language with Anaconda](https://www.anaconda.com/docs/getting-started/working-with-conda/packages/using-r-language).
- For more information about `IRkernel`, see [Native R kernel for Jupyter](https://cran.r-project.org/web/packages/IRkernel/readme/README.html).

### Remove added kernels

To remove an added Jupyter kernel from the compute instance, you must remove the `kernelspec`, and can optionally remove the Conda environment. You can also choose to keep the Conda environment. You must remove the `kernelspec` to prevent the kernel from remaining selectable and causing unexpected behavior.

> [!IMPORTANT]
> When you customize the compute instance, make sure you don't delete Conda environments or Jupyter kernels that you didn't create, which could damage Jupyter or JupyterLab functionality.

To remove the `kernelspec`:

1. Use the terminal window to list and find the `kernelspec`:

   ```console
   jupyter kernelspec list
   ```

1. Remove the `kernelspec`, replacing `<UNWANTED_KERNEL>` with the kernel you want to remove.

   ```console
   jupyter kernelspec uninstall <UNWANTED_KERNEL>
   ```

To also remove the Conda environment:

1. Use the terminal window to list and find the Conda environment:

   ```console
   conda env list
   ```

1. Remove the Conda environment, replacing `<ENV_NAME>` with the Conda environment you want to remove.

   ```console
   conda env remove -n ENV_NAME
   ```

When you refresh, the kernel list in your **Notebooks** view should reflect your changes.

## Manage terminal sessions

Terminal sessions can stay active if you don't properly close terminal tabs. Too many active terminal sessions can affect the performance of your compute instance. Make sure to close any sessions you no longer need to preserve your compute instance resources and optimize performance.

To see a list of all active terminal sessions, select the **Manage active sessions** icon at far right in the terminal toolbar. Shut down any sessions you no longer need.

For more information about how to manage sessions running on your compute, see [Manage notebook and terminal sessions](how-to-manage-compute-sessions.md).

## Related content

* [Manage notebook and terminal sessions](how-to-manage-compute-sessions.md)
* [Git integration for Azure Machine Learning](concept-train-model-git-integration.md)
* [Work in Visual Studio Code remotely connected to a compute instance](how-to-work-in-vs-code-remote.md)