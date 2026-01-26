---
title: 'Start Visual Studio Code Integrated with Azure Machine Learning'
titleSuffix: Azure Machine Learning
description: Connect to an Azure Machine Learning compute instance in Visual Studio Code to run interactive Jupyter Notebook and remote development workloads.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.custom: build-2023
ms.topic: how-to
ms.author: scottpolly
author: s-polly
ms.reviewer: lebaro
ms.date: 12/22/2025
monikerRange: 'azureml-api-1 || azureml-api-2'
#Customer intent: As a data scientist, I want to connect to an Azure Machine Learning compute instance in Visual Studio Code to access my resources and run my code.
---

# Start Visual Studio Code integrated with Azure Machine Learning

In this article, you learn how to start Visual Studio Code remotely connected to an Azure Machine Learning compute instance. Use VS Code as your integrated development environment (IDE) together with the power of Azure Machine Learning resources. Use VS Code in the browser with VS Code for the Web, or use the VS Code desktop application.

There are two ways you can connect to a compute instance from VS Code. We recommend the first approach.

- **Use VS Code as your workspace's IDE.** This option provides a full-featured development environment for building your machine learning projects.
    * You can open VS Code from your workspace either in the browser by using [VS Code for the Web](?tabs=vscode-web#use-vs-code-as-your-workspace-ide) or use [VS Code desktop](?tabs=vscode-desktop#use-vs-code-as-your-workspace-ide).
    * We recommend VS Code for the Web because you can do all your machine learning work directly from a browser, without any required installations or dependencies.

- **Use a Remote Jupyter Notebook server**. This option enables you to set a compute instance as a remote Jupyter Notebook server. This option is available only in VS Code desktop.

> [!IMPORTANT]
> For information about connecting to a compute instance behind a firewall, see [Configure inbound and outbound network traffic](how-to-access-azureml-behind-firewall.md#scenario-visual-studio-code).

## Prerequisites

- [!INCLUDE [workspace and compute instance](includes/prerequisite-workspace-compute-instance.md)]
- [!INCLUDE [sign in](includes/prereq-sign-in.md)]

## Use VS Code as your workspace IDE

Use one of these options to connect VS Code to your compute instance and workspace files.

# [Studio > VS Code for the Web](#tab/vscode-web)

VS Code for the Web provides a full-featured development environment for building your machine learning projects, all from a browser and without required installations or dependencies. When you connect your Azure Machine Learning compute instance, the rich and integrated development experience VS Code offers is enhanced by the power of Azure Machine Learning.

You can start VS Code for the Web with one click from Azure Machine Learning studio and seamlessly continue your work.

Sign in to [Azure Machine Learning studio](https://ml.azure.com) and follow the steps to start a VS Code for the Web browser tab that's connected to your Azure Machine Learning compute instance.

You can create the connection from either the **Notebooks** or the **Compute** section of Azure Machine Learning studio.

* Notebooks

    1. In the left menu, select **Notebooks**. 
    1. In the **Files** list, select the file you want to edit.
    1. If the compute instance is stopped, select **Start compute** and wait until it's running.

        :::image type="content" source="media/how-to-launch-vs-code-remote/start-compute.png" alt-text="Screenshot that shows how to start compute if it's stopped." lightbox="media/how-to-launch-vs-code-remote/start-compute.png":::

    1. In the list of code editors, select **Edit in VS Code (Web)**.

       :::image type="content" source="media/how-to-launch-vs-code-remote/edit-in-vs-code.png" alt-text="Screenshot of how to connect to Compute Instance VS Code (Web) Azure Machine Learning Notebook." lightbox="media/how-to-launch-vs-code-remote/edit-in-vs-code.png":::

    - You can also start VS Code for Web without opening a notebook by selecting the **VS Code (Web)** button above the **Files** list or by right-clicking a folder in the **Files** list. 

        :::image type="content" source="media/how-to-launch-vs-code-remote/file-explorer.png" alt-text="Screenshot that shows the VS Code (Web) button above the **Files** list.":::

* Compute

    1. In the left menu, select **Compute**.
    1. If the compute instance you want to use is stopped, select it, and then select **Start**.
    1. When the compute instance is running, in the **Applications** column, select **VS Code (Web)**.

    :::image type="content" source="media/how-to-launch-vs-code-remote/vs-code-from-compute.png" alt-text="Screenshot that shows how to connect to a VS Code for the Web compute instance." lightbox="media/how-to-launch-vs-code-remote/vs-code-from-compute.png":::

# [Studio > VS Code desktop](#tab/vscode-desktop)

This option starts the VS Code desktop application and connects it to your compute instance.

On the initial connection, you might be prompted to install the Azure Machine Learning VS Code extension if you don't already have it. For more information, see the [Azure Machine Learning VS Code extension setup guide](how-to-setup-vs-code.md).

> [!IMPORTANT]
> When you connect to your remote compute instance from VS Code, make sure that the account you're signed in to in Azure Machine Learning studio is the same one you use in VS Code.

You can create the connection from either the **Notebooks** or the **Compute** section of Azure Machine Learning studio.

* Notebooks

    1. In the left menu, select **Notebooks**. 
    1. In the **Files** list, select the file you want to edit.
    1. If the compute instance is stopped, select **Start compute** and wait until it's running.

        :::image type="content" source="media/how-to-launch-vs-code-remote/start-compute.png" alt-text="Screenshot that shows how to start compute if it's stopped." lightbox="media/how-to-launch-vs-code-remote/start-compute.png":::

    1. In the list of code editors, select **Edit in VS Code (Desktop)**.

        :::image type="content" source="media/how-to-launch-vs-code-remote/edit-in-vs-code.png" alt-text="Screenshot that shows how to connect to a compute instance from a Notebook." lightbox="media/how-to-launch-vs-code-remote/edit-in-vs-code.png":::

* Compute

    1. In the left menu, select **Compute**.
    1. If the compute instance you want to use is stopped, select it, and then select **Start**.
    1. After the compute instance is running, in the **Applications** column, select **VS Code (Desktop)**.

    :::image type="content" source="media/how-to-launch-vs-code-remote/studio-compute-instance-vs-code-launch.png" alt-text="Screenshot that shows how to connect to a VS Code desktop compute instance." lightbox="media/how-to-launch-vs-code-remote/studio-compute-instance-vs-code-launch.png":::

# [From VS Code](#tab/extension)

This option connects your current VS Code session to a remote compute instance. To connect to your compute instance from VS Code, you need to install the Azure Machine Learning Visual Studio Code extension. For more information, see the [Azure Machine Learning VS Code extension setup guide](how-to-setup-vs-code.md).

### Azure Machine Learning extension

1. In VS Code, start the Azure Machine Learning extension.
1. Expand the **Compute instances** node in your extension.
1. Right-click the compute instance you want to connect to, and then select **Connect In New Window**.

:::image type="content" source="media/how-to-launch-vs-code-remote/vs-code-connect-compute-instance.png" alt-text="Screenshot that shows how to connect to a compute instance." lightbox="media/how-to-launch-vs-code-remote/vs-code-connect-compute-instance.png":::

### Command palette

1. In VS Code, open the command palette by selecting **View > Command Palette**.
1. Filter for and select **Azure ML- Remote: Connect to compute instance in New Window**.
1. Select your subscription.
1. Select your workspace.
1. Select your compute instance or create a new one.

---

If you pick one of the click-out experiences, a new VS Code window is opened, and an attempt to connect to the remote compute instance is made. When you attempt to make this connection, the following steps take place:

1. Authorization. Some checks are performed to make sure the user attempting to make a connection is authorized to use the compute instance.
1. VS Code Remote Server is installed on the compute instance.
1. A WebSocket connection is established for real-time interaction.

After the connection is established, it's persisted. A token is issued at the start of the session, and it's refreshed automatically to maintain the connection with your compute instance.

After you connect to your remote compute instance, use the editor to:

* [Author and manage files on your remote compute instance or file share](https://code.visualstudio.com/docs/editor/codebasics).
* Use the [VS Code integrated terminal](https://code.visualstudio.com/docs/editor/integrated-terminal) to run commands and applications on your remote compute instance.
* [Debug your scripts and applications](https://code.visualstudio.com/Docs/editor/debugging).
* [Use VS Code to manage your Git repositories](concept-train-model-git-integration.md).

## Remote Jupyter Notebook server

This option allows you to use a compute instance as a remote Jupyter Notebook server from VS Code desktop. This option connects only to the compute instance, not to the rest of the workspace. You won't see your workspace files in VS Code when you use this option.

To configure a compute instance as a remote Jupyter Notebook server, first install the Azure Machine Learning VS Code extension. For more information, see the [Azure Machine Learning VS Code extension setup guide](how-to-setup-vs-code.md).

To connect to a compute instance:

1. Open a Jupyter Notebook in VS Code.
1. When the integrated notebook experience loads, click **Select Kernel**.

    :::image type="content" source="media/how-to-launch-vs-code-remote/launch-server-selection-dropdown.png" alt-text="Screenshot that shows how to select a Jupyter Server." lightbox="media/how-to-launch-vs-code-remote/launch-server-selection-dropdown.png"::: 

    Alternatively, use the command palette:

    1. Select **View > Command Palette**  to open the command palette.
    1. Filter for and select **Azure ML: Connect to compute instance Jupyter server**.

1. Select **Azure ML compute instance** from the list of Jupyter server options.
1. Select a Kernel.
1. Select your subscription in the list of subscriptions. If you have previously configured your default Azure Machine Learning workspace, this step is skipped.
1. Select your workspace.
1. Select your compute instance from the list. If you don't have one, select **Create new Azure Machine Learning Compute Instance** and follow the prompts to create one.
1. For the changes to take effect, you need to reload VS Code.
1. Open a Jupyter Notebook and run a cell.

> [!IMPORTANT]
> You must run a cell to establish the connection.

At this point, you can continue to run cells in your Jupyter Notebook.

> [!TIP]
> You can also work with Python script files (.py) containing Jupyter-like code cells. For more information, see the [Visual Studio Code Python Interactive documentation](https://code.visualstudio.com/docs/python/jupyter-support-py).

## Next steps

Now that you've started VS Code remotely connected to a compute instance, you can prepare your data, edit and debug your code, and submit training jobs with the Azure Machine Learning extension.

To learn more about how to make the most of VS Code integrated with Azure Machine Learning, see [Work in VS Code remotely connected to a compute instance](how-to-work-in-vs-code-remote.md).
