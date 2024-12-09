---
title: Custom tool package creation and usage in prompt flow
titleSuffix: Azure Machine Learning
description: Learn how to develop your own tool package in prompt flow.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: keli19
ms.date: 11/26/2024
---

# Custom tool package creation and usage

When developing flows, you can not only use the built-in tools provided by prompt flow, but also develop your own custom tool. In this document, we guide you through the process of developing your own tool package, offering detailed steps and advice on how to utilize the custom tool package.

After successful installation, your custom "tool" can show up in the tool list:
:::image type="content" source="./media/how-to-custom-tool-package-creation-and-usage/test-customer-tool-on-ui.png" alt-text="Screenshot of custom tools in the UI tool list."lightbox = "./media/how-to-custom-tool-package-creation-and-usage/test-customer-tool-on-ui.png":::

## Create your own tool package

Your tool package should be a python package. To develop your custom tool, follow the steps **Create your own tool package** and **build and share the tool package** in [Create and Use Tool Package](https://microsoft.github.io/promptflow/how-to-guides/develop-a-tool/create-and-use-tool-package.html). You can find more advanced development guidance in [How to develop a tool](https://microsoft.github.io/promptflow/how-to-guides/develop-a-tool/index.html).

## Prepare compute session

In order to add the custom tool to your tool list for use, it's necessary to prepare the compute session. Here we use [my-tools-package](https://pypi.org/project/my-tools-package/) as an example.

When using compute session, you can readily install the publicly released package by adding the custom tool package name into the `requirements.txt` file in the flow folder. Then to start installation select the 'Save and install' button. After completion, you can see the custom tools displayed in the tool list. To learn more, see [How to manage compute session](./how-to-manage-compute-session.md).
:::image type="content" source="./media/how-to-custom-tool-package-creation-and-usage/install-package-on-compute-session.png" alt-text="Screenshot of how to install packages on compute session."lightbox = "./media/how-to-custom-tool-package-creation-and-usage/install-package-on-compute-session.png":::

Another method is applicable for not only publicly released packages, but also local or private feed packages. Firstly you should build an image following the two steps in [how to customize base image for compute session](./how-to-customize-session-base-image.md), and then [change the base image for compute session](./how-to-manage-compute-session.md#change-the-base-image-for-compute-session).

## Test from prompt flow UI
1. Create a standard flow.
2. Start compute session.
    :::image type="content" source="./media/how-to-custom-tool-package-creation-and-usage/start-compute-session.png" alt-text="Screenshot of flow in Azure Machine Learning studio starting compute session."lightbox ="./media/how-to-custom-tool-package-creation-and-usage/start-compute-session.png":::

3. Add your tools.
    :::image type="content" source="./media/how-to-custom-tool-package-creation-and-usage/test-customer-tool-on-ui-step-1.png" alt-text="Screenshot of flow in Azure Machine Learning studio showing more tools dropdown."lightbox ="./media/how-to-custom-tool-package-creation-and-usage/test-customer-tool-on-ui-step-1.png":::
4. Change flow based on your requirements and run flow.
    :::image type="content" source="./media/how-to-custom-tool-package-creation-and-usage/test-customer-tool-on-ui-step-2.png" alt-text="Screenshot of flow in Azure Machine Learning studio showing adding a tool."lightbox ="./media/how-to-custom-tool-package-creation-and-usage/test-customer-tool-on-ui-step-2.png":::

## FAQ
### How to install the custom tool package in the VS Code extension?
1. Install prompt flow for VS Code extension
    :::image type="content" source="./media/how-to-custom-tool-package-creation-and-usage/prompt-flow-vs-code-extension.png" alt-text="Screenshot of prompt flow VS Code extension."lightbox ="./media/how-to-custom-tool-package-creation-and-usage/prompt-flow-vs-code-extension.png":::
2. Go to terminal and install the tool package in conda environment of the extension. Assume your conda env name is `prompt-flow`.

   ```sh
   (local_test) PS D:\projects\promptflow\tool-package-quickstart> conda activate prompt-flow
   (prompt-flow) PS D:\projects\promptflow\tool-package-quickstart> pip install my-tools-package==0.0.1
   ```

3. Go to the extension and open one flow folder. Select 'flow.dag.yaml' and preview the flow. Next, select `+` button and you can see your tools. You need to **reload the windows** to clean previous cache if you don't see your tool in the list.

    :::image type="content" source="./media/how-to-custom-tool-package-creation-and-usage/auto-list-tool-in-extension.png" alt-text="Screenshot of the VS Code showing the tools." lightbox ="./media/how-to-custom-tool-package-creation-and-usage/auto-list-tool-in-extension.png":::

### Why is my custom tool not showing up in the UI?
You can test your tool package using the following script to ensure that you've packaged your tool YAML files and configured the package tool entry point correctly.

  1. Make sure to install the tool package in your conda environment before executing this script.
  2. Create a python file anywhere and copy the following content into it.

      ```python
      def test():
          # `collect_package_tools` gathers all tools info using the `package-tools` entry point. This ensures that your package is correctly packed and your tools are accurately collected. 
          from promptflow.core.tools_manager import collect_package_tools
          tools = collect_package_tools()
          print(tools)
      if __name__ == "__main__":
          test()
      ```

  3. Run this script in your conda environment. It returns the metadata of all tools installed in your local environment, and you should verify that your tools are listed.

### Why am I unable to upload package to PyPI?

- Make sure that the entered username and password of your PyPI account are accurate.
- If you encounter a `403 Forbidden Error`, it's likely due to a naming conflict with an existing package. You need to choose a different name. Package names must be unique on PyPI to avoid confusion and conflicts among users. Before creating a new package, it's recommended to search PyPI (https://pypi.org/) to verify that your chosen name isn't already taken. If the name you want is unavailable, consider selecting an alternative name or a variation that clearly differentiates your package from the existing one.

## Next steps

- Learn more about [how to manage compute session](./how-to-manage-compute-session.md)
- Learn more about [how to customize base image for compute session](./how-to-customize-session-base-image.md)
