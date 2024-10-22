---
title: Integrate LangChain in prompt flows
titleSuffix: Azure Machine Learning
description: Learn how to integrate LangChain into prompt flows in Azure Machine Learning studio.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: chenlujiao
ms.date: 10/22/2024
---

# Integrate LangChain in prompt flows

The [LangChain](https://python.langchain.com) Python library is a framework for developing applications powered by large language models (LLMs), agents, and dependency tools. You can use LangChain in Azure Machine Learning prompt flows. This article shows you how to supercharge your LangChain development with prompt flow.

The integration of LangChain with prompt flow is a powerful combination that can help you build and test your custom language models with ease. You can use LangChain modules to initially build the flow, and then use the prompt flow process to scale experiments for bulk testing, evaluation, and eventual deployment. For example, you can conduct large scale experiments based on larger datasets.

If you already have a local prompt flow based on LangChain code, you can use streamlined prompt flow integration to easily convert it into an Azure Machine Learning prompt flow for further experimentation. Or, if you prefer to use LangChain SDK classes and functions directly, you can easily build flows that use Python nodes containing your custom LangChain code.

## Prerequisites

- A local LangChain flow that's properly tested and ready for deployment.
- A compute session that can run the Machine Learning prompt flow by adding packages listed in the *requirements.txt* file, including `langchain`. For more information, see [Manage prompt flow compute session](how-to-manage-compute-session.md).

## Convert LangChain code into prompt flows

The rest of the article describes how to convert your local LangChain code to a runnable Azure Machine Learning prompt flow.

### Convert credentials to a prompt flow connection

Your LangChain code might [define environment variables](https://python.langchain.com/docs/integrations/platforms/microsoft) to store credentials, such as the AzureOpenAI API key necessary for invoking AzureOpenAI models. For example, the following image shows environmental variables being set for OpenAI API type, key, base, and version.

:::image type="content" source="./media/how-to-integrate-with-langchain/langchain-env-variables.png" alt-text="Screenshot of Azure OpenAI example in LangChain.":::

When you run an Azure Machine Learning prompt flow in the cloud, it's better not to expose credentials as environment variables. To securely store and manage credentials separately from your code, you should convert the environmental variables into a prompt flow connection.

To create a connection that securely stores credentials such as your LLM API key or other required keys, follow these instructions:

1. On the **Prompt flow** page in your Azure Machine Learning workspace, select the **Connections** tab, and then select **Create**.
1. Select a connection type from the dropdown list. For this example, select **Custom**.

   :::image type="content" source="./media/how-to-integrate-with-langchain/custom-connection-1.png" alt-text="Screenshot of selecting Create and then Custom on the Connections tab of the Prompt flow page.":::

1. In the right pane, define your connection **Name**, and then add **Key-value pairs** to store your credentials and keys by selecting **Add key-value pairs**.

   :::image type="content" source="./media/how-to-integrate-with-langchain/custom-connection-2.png" alt-text="Screenshot of adding custom connection key-value pairs.":::

1. To store an encrypted value for a key, select the **is secret** checkbox next to one or more key-value pairs. At least one value must be set as secret for the connection creation to succeed.

1. Select **Save**.

The custom connection can replace the keys and credentials or corresponding environmental variables explicitly defined in your LangChain code. To use the custom connection in the flow, see [Configure connection](#configure-connection).

### Convert LangChain code to a runnable flow

To create a flow, select **Create** on the **Prompt flow** page in Azure Machine Learning studio, and choose a flow type. On the flow authoring page, start your compute session before you author the flow. Select tool types at the top of the pane to insert corresponding nodes into the flow. For detailed flow authoring instructions, see [Develop prompt flow](how-to-develop-a-standard-flow.md).

All your LangChain code can directly run in Python nodes in your flow, as long as your compute session contains the `langchain` package dependency.

There are two ways to convert your LangChain code into a flow:

- For a simple conversion process, you can initialize and invoke the LLM model within a Python node by using the integrated LangChain LLM library.
- For better experiment management, you can convert the LLM model to use Azure Machine Learning Python LLM tools in the flow.

The type of flow to implement depends on your use case.

| Flow type | Implementation | Use case |
|-------| -------- | -------- | -------- |
| A flow that includes both prompt nodes and Python nodes | Extract your prompt template into a prompt node, and combine the remaining code in single or multiple Python nodes or tools. | Easy prompt tuning by running flow variants, to choose the optimal prompt based on evaluation results.|
| A flow that includes Python nodes only| Create a new flow with Python nodes only. All code runs in Python nodes, including prompt definitions. | Faster batch testing based on larger scale datasets. |

The following example shows a flow that uses both prompt nodes and Python nodes:

:::image type="content" source="./media/how-to-integrate-with-langchain/flow-node-a-1.png" alt-text="Screenshot of flows highlighting the prompt button and system template. " lightbox = "./media/how-to-integrate-with-langchain/flow-node-a-1.png":::

The following example shows a flow that uses Python nodes only:

:::image type="content" source="./media/how-to-integrate-with-langchain/flow-node-b.png" alt-text="Screenshot of flows showing the LangChain code node and graph. " lightbox = "./media/how-to-integrate-with-langchain/flow-node-b.png":::

### Configure connection

After you structure your flow and move your code to specific tool nodes, you need to replace your original environment variables with the corresponding keys from your connection. To use the custom connection you created, follow these steps:

1. In your Python code, import the custom connection library by entering `from promptflow.connections import CustomConnection`.

   >[!NOTE]
   >For an Azure OpenAI connection, use `from promptflow.connections import AzureOpenAIConnection`.

1. In your tool function, define an input parameter of the type `CustomConnection`.

   :::image type="content" source="./media/how-to-integrate-with-langchain/custom-connection-python-node-1.png" alt-text="Screenshot of doc search chain node highlighting the custom connection. " lightbox = "./media/how-to-integrate-with-langchain/custom-connection-python-node-1.png":::
   
1. Parse the input to the input section, and then select your custom connection in the value dropdown.

   :::image type="content" source="./media/how-to-integrate-with-langchain/custom-connection-python-node-2.png" alt-text="Screenshot of the chain node highlighting the connection. " lightbox = "./media/how-to-integrate-with-langchain/custom-connection-python-node-2.png":::
   
1. In your code, replace the environment variables that originally defined the key and credential with the corresponding key added in the connection.
1. Save, return to the authoring page, and also configure the connection parameter in the node input.

If you have a LangChain code that consumes an AzureOpenAI model, import the library by entering `from promptflow.connections import AzureOpenAIConnection`. Replace the environment variables with the corresponding keys from the Azure OpenAI connection. 

:::image type="content" source="./media/how-to-integrate-with-langchain/code-consume-aoai.png" alt-text="Screenshot of LangChain code in prompt flow. " lightbox = "./media/how-to-integrate-with-langchain/code-consume-aoai.png":::

### Configure input and output

Before you run the flow, configure the node inputs and outputs and the overall flow inputs and outputs. This step is crucial to ensure that all the required data passes properly through the flow and produces desired results. For more information, see [Flow inputs and outputs](how-to-develop-flow.md#flow-input-and-output).

## Related content

- [Langchain](https://langchain.com)
- [Manage compute session](how-to-manage-compute-session.md)
- [Customize base image of compute session](how-to-customize-session-base-image.md)
