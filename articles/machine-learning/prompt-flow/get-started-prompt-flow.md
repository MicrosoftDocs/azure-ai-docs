---
title: Get started with prompt flow
titleSuffix: Azure Machine Learning
description: Learn how to set up, create, evaluate, and deploy a prompt flow in Azure Machine Learning studio.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar 
ms.date: 07/17/2025
ms.custom:
  - ignite-2023
  - build-2024
  - sfi-image-nochange
ms.update-cycle: 365-days
---

# Get started with prompt flow

This article walks you through the main user journey of using prompt flow in Azure Machine Learning studio. You learn how to enable prompt flow in your Azure Machine Learning workspace, create and develop a prompt flow, test and evaluate the flow, and then deploy it to production.

## Prerequisites 

- An Azure Machine Learning workspace. The default storage for the workspace must be blob type.
- An Azure OpenAI account, or an existing Azure OpenAI connection with a deployment. For more information, see [Create a resource and deploy a model using Azure OpenAI](/azure/cognitive-services/openai/how-to/create-resource).
  >[!NOTE]
  >If you want to secure your prompt flow with a virtual network, also follow the instructions at [Secure prompt flow with workspace managed virtual network](how-to-secure-prompt-flow.md#secure-prompt-flow-with-workspace-managed-virtual-network).

<a name="set-up-connection"></a>
## Set up a connection

A connection helps securely store and manage secret keys or other sensitive credentials required for interacting with Large Language Models (LLM) and other external tools such as Azure Content Safety. Connection resources are shared with all members in the workspace.

> [!NOTE]
> The LLM tool in prompt flow does not support reasoning models (such as OpenAI o1 or o3). For reasoning model integration, use the Python tool to call the model APIs directly. For more information, see [Call a reasoning model from the Python tool](tools-reference/python-tool.md#call-a-reasoning-model-from-the-python-tool).. 

1. To check if you already have an Azure OpenAI connection, select **Prompt flow** from the Azure Machine Learning studio left menu and then select the **Connections** tab on the **Prompt flow** screen.

   :::image type="content" source="./media/get-started-prompt-flow/connection-creation-entry-point.png" alt-text="Screenshot of the connections tab with create highlighted." lightbox = "./media/get-started-prompt-flow/connection-creation-entry-point.png":::

   If you already see a connection whose provider is **AzureOpenAI**, you can skip the rest of this setup process. Note that this connection must have a deployment to be able to run the LLM nodes in the example flow. For more information, see [Deploy a model](/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model).

1. If you don't have an Azure OpenAI connection, select **Create** and then select **AzureOpenAI** from the dropdown menu.

1. In the **Add Azure OpenAI connection** pane, provide a name for the connection, select your **Subscription ID** and **Azure OpenAI Account Name**, and provide an **Auth Mode** and API information.

   Prompt flow supports either **API Key** or **Microsoft Entra ID** authentication for Azure OpenAI resources. For this tutorial, select **API key** under **Auth Mode**.

   :::image type="content" source="./media/get-started-prompt-flow/azure-openai-connection.png" alt-text="Screenshot of the Azure OpenAI connection screen." lightbox = "./media/get-started-prompt-flow/azure-openai-connection.png":::

   To get the API information, go to the [Chat playground](https://oai.azure.com/portal/chat) in the Azure OpenAI portal and select your Azure OpenAI resource name. Copy the **Key** and paste it into the **API key** field in the **Add Azure OpenAI connection** form, and copy the **Endpoint** and paste it into the **API base** field in the form.

   :::image type="content" source="./media/get-started-prompt-flow/create-aoai-connection.png" alt-text="Screenshot of the chat playground showing the Key and Endpoint for an Azure OpenAI resource." lightbox = "./media/get-started-prompt-flow/create-aoai-connection.png":::

   For information about Microsoft Entra ID authentication, see [How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication](/azure/ai-services/openai/how-to/managed-identity).

1. After you fill out all fields, select **Save** to create the connection.

1. The connection must be associated with a deployment before you can run the LLM nodes in the example flow. To create the deployment, see [Deploy a model](/azure/ai-services/openai/how-to/create-resource#deploy-a-model).

## Create and develop your prompt flow

In the **Flows** tab of the **Prompt flow** home page, select **Create** to create the prompt flow. The **Create a new flow** page shows flow types you can create, built-in samples you can clone to create a flow, and ways to import a flow.

### Clone from a sample

In the **Explore gallery**, you can browse the built-in samples and select **View detail** on any tile to preview whether it's suitable for your scenario.

This tutorial uses the **Web Classification** sample to walk through the main user journey. Web Classification is a flow demonstrating multiclass classification with an LLM. Given a URL, the flow classifies the URL into a web category with just a few shots, simple summarization, and classification prompts. For example, given a URL `https://www.imdb.com`, it classifies the URL into `Movie`.

To clone the sample, select **Clone** on the **Web Classification** tile.

:::image type="content" source="./media/get-started-prompt-flow/sample-in-gallery.png" alt-text="Screenshot of create from galley highlighting web classification." lightbox = "./media/get-started-prompt-flow/sample-in-gallery.png":::

The **Clone flow** pane shows the location to store your flow within your workspace fileshare storage. You can customize the folder if you want. Then select **Clone**.

The cloned flow opens in the authoring UI. You can select the **Edit** pencil icon to edit flow details like name, description, and tags.

### Start the compute session

A compute session is necessary for flow execution. The compute session manages the computing resources required for the application to run, including a Docker image that contains all necessary dependency packages.

On the flow authoring page, start a compute session by selecting **Start compute session**.

:::image type="content" source="./media/get-started-prompt-flow/start-compute-session.png" alt-text="Screenshot of starting a start-compute-session." lightbox = "./media/get-started-prompt-flow/start-compute-session.png":::

### Inspect the flow authoring page

The compute session can take a few minutes to start. While the compute session is starting, view the parts of the flow authoring page.

- The **Flow** or *flatten* view on the left side of the page is the main working area, where you can author the flow by adding or removing nodes, editing and running nodes inline, or editing prompts. In the **Inputs** and **Outputs** sections, you can view, add or remove, and edit inputs and outputs.

  When you cloned the current Web Classification sample, the inputs and outputs were already set. The input schema for the flow is `name: url; type: string`, a URL of string type. You can change the preset input value to another value like `https://www.imdb.com` manually.

- **Files** at top right shows the folder and file structure of the flow. Each flow folder contains a *flow.dag.yaml* file, source code files, and system folders. You can create, upload, or download files for testing, deployment, or collaboration.

- The **Graph** view at lower right is for visualizing what the flow looks like. You can zoom in or out, or use auto layout.

You can edit files inline in the **Flow** or flatten view, or you can turn on the **Raw file mode** toggle and select a file from **Files** to open the file in a tab for editing.

:::image type="content" source="./media/get-started-prompt-flow/file-edit-tab.png" alt-text="Screenshot of the file edit tab under raw file mode." lightbox = "./media/get-started-prompt-flow/file-edit-tab.png":::

For this sample, the input is a URL to classify. The flow uses a Python script to fetch text content from the URL, uses LLM to summarize the text content in 100 words, and classifies based on the URL and summarized text content. A Python script then converts LLM output into a dictionary. The **prepare_examples** node feeds a few example shots to the classification node's prompt.

### Set up LLM nodes

For each LLM node, you need to select a **Connection** to set the LLM API keys. Select your Azure OpenAI connection.

Depending on the connection type, you must select a **deployment_name** or a model from the dropdown list. For an Azure OpenAI connection, select a deployment. If you don't have a deployment, create one in the Azure OpenAI portal by following instructions at [Deploy a model](/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model).

>[!NOTE]
>If you use an OpenAI connection rather than an Azure OpenAI connection, you need to select a model rather than a deployment in the **Connection** field.

For this example, make sure the API type is **chat**, because the provided prompt example is for the chat API. For more information about the difference between the chat and completion APIs, see [Develop a flow](how-to-develop-flow.md).

:::image type="content" source="./media/get-started-prompt-flow/select-a-connection.png" alt-text="Screenshot of Web classification showing the connection dropdown." lightbox = "./media/get-started-prompt-flow/select-a-connection.png":::

Set up connections for both of the LLM nodes in the flow, **summarize_text_content** and **classify_with_llm**.

### Run a single node

To test and debug a single node, select the **Run** icon at the top of a node in the **Flow** view. You can expand **Inputs** and change the flow input URL to test the node behavior for different URLs.

The run status appears at the top of the node. After the run completes, run output appears in the node **Output** section.

:::image type="content" source="./media/get-started-prompt-flow/run-single-node.png" alt-text="Screenshot of Web classification showing first you run the python node then check the output, next you run the LLM node then check its output." lightbox = "./media/get-started-prompt-flow/run-single-node.png":::

The **Graph** view also shows the single run node status.

Run **fetch_text_content_from_url** and then run **summarize_text_content** to check if the flow can successfully fetch content from the web and summarize the web content.

### Run the whole flow

To test and debug the whole flow, select **Run** at the top of the screen. You can change the flow input URL to test how the flow behaves for different URLs.

:::image type="content" source="./media/get-started-prompt-flow/run-flow.png" alt-text="Screenshot of Web classification showing a whole run and highlighting the run button." lightbox = "./media/get-started-prompt-flow/run-flow.png":::

Check the run status and output of each node.

### View flow outputs

You can also set flow outputs to check outputs of multiple nodes in one place. Flow outputs help you:

- Check bulk test results in a single table.
- Define evaluation interface mapping.
- Set deployment response schema.

In the cloned sample, the **category** and **evidence** flow outputs are already set.

1. Select **View outputs** in the top banner or the top menu bar to view detailed input, output, flow execution, and orchestration information.

   :::image type="content" source="./media/get-started-prompt-flow/authoring-view-trace.png" alt-text="Screenshot of view output button in two locations." lightbox = "./media/get-started-prompt-flow/authoring-view-trace.png":::

1. On the **Outputs** tab of the **Outputs** screen, note that the flow predicts the input URL with a **category** and **evidence**.

   :::image type="content" source="./media/get-started-prompt-flow/outputs-overview.png" alt-text="Screenshot of viewing outputs in Outputs page." lightbox ="./media/get-started-prompt-flow/outputs-overview.png":::

1. Select the **Trace** tab on the **Outputs** screen and then select **flow** under **node name** to see detailed flow overview information in the right pane. Expand **flow** and select any step to see detailed information for that step.

   :::image type="content" source="./media/get-started-prompt-flow/view-outputs-entry-point.png" alt-text="Screenshot of the flow Trace screen." lightbox = "./media/get-started-prompt-flow/view-outputs-entry-point.png":::

## Test and evaluate

After the flow runs successfully with a single row of data, test whether it performs well with a large set of data. You can run a bulk test and optionally add an evaluation flow, and then check the results.

You need to prepare test data first. Azure Machine Learning supports CSV, TSV, and JSONL file formats for data.

- Go to GitHub and download [data.csv](https://github.com/Azure/azureml-assets/blob/main/assets/promptflow/data/web-classification/data.csv), the golden dataset for the Web Classification sample.

Use the **Batch run & Evaluate** wizard to configure and submit a batch run and optionally an evaluation method. Evaluation methods are also flows, which use Python or LLM to calculate metrics like accuracy and relevance score.

1. Select **Evaluate** from the top menu of your flow authoring page.

1. On the **Basic settings** screen, change the **Run display name** if desired, add an optional **Run description** and **Tags**, and then select **Next**.

1. On the **Batch run settings** screen, select **Add new data**. On the **Add data** screen, provide a **Name** for the dataset, select **Browse** to upload the *data.csv* file you downloaded, and then select **Add**.

   After you upload the data, or if your workspace has another dataset you want to use, search for and choose the dataset from the dropdown list to preview the first five rows.

   The **Input mapping** feature supports mapping your flow input to any data column in your dataset, even if the column names don't match.

   :::image type="content" source="./media/get-started-prompt-flow/upload-new-data-batch-run.png" alt-text="Screenshot of Batch run and evaluate, highlighting upload new data." lightbox = "./media/get-started-prompt-flow/upload-new-data-batch-run.png":::

1. Select **Next** to optionally select one or multiple evaluation methods. The **Select evaluation** page shows built-in and customized evaluation flows. To see how the metrics are defined for built-in evaluation methods, you can select **More details** on the method's tile.

   Web Classification is a classification scenario, so select **Classification Accuracy Evaluation** to use for evaluation, and then select **Next**.

   :::image type="content" source="./media/get-started-prompt-flow/accuracy.png" alt-text="Screenshot of Web classification showing the batch run and evaluate on evaluation methods." lightbox = "./media/get-started-prompt-flow/accuracy.png":::

1. On the **Configure evaluation** screen, set **Evaluation input mapping** to map **groundtruth** to flow input **${data.category}** and map **prediction** to flow output **${run.outputs.category}**.

   :::image type="content" source="./media/get-started-prompt-flow/accuracy-configure.png" alt-text="Screenshot of Web classification showing the batch run and evaluate on the evaluation settings." lightbox = "./media/get-started-prompt-flow/accuracy-configure.png":::

1. Select **Review + submit** and then select **Submit** to submit a batch run and the selected evaluation method.

### Check results

When your run submits successfully, select **View run list** to view run status on the prompt flow **Runs** page. The batch run might take a while to finish. You can select **Refresh** to load the latest status. 

After the batch run completes, select the check next to the run and then select **Visualize outputs** to view the result of your batch run. 

:::image type="content" source="./media/get-started-prompt-flow/views.png" alt-text="Screenshot of selecting Visualize outputs on the Runs page." lightbox = "./media/get-started-prompt-flow/views.png":::

On the **Visualize outputs** screen, enable the eye icon next to the child run to append evaluation results to the table of batch run results. You can see the total token count and overall accuracy. The **Output** table shows the results for each row of data: input, flow output, system metrics, and evaluation result of **Correct** or **Incorrect**.

:::image type="content" source="./media/get-started-prompt-flow/check-outputs.png" alt-text="Screenshot of Web classification batch run details page to view outputs." lightbox = "./media/get-started-prompt-flow/check-outputs.png":::

In the **Output** table, you can:

- Adjust column width, hide or unhide columns, or change column order.
- Select **Export** to **Download current page** as a CSV file or **Download data export script** as a Jupyter notebook file you can run to download outputs locally.
- Select the **View details** icon next to any row to open the **Trace view** showing the complete details for that row.

Accuracy isn't the only metric that can evaluate a classification task. For example, you can also use recall to evaluate. To run other evaluations, select **Evaluate** next to **Visualize outputs** on the **Runs** page, and select other evaluation methods.

## Deploy as an endpoint

After you build and test a flow, you can deploy it as an endpoint so that you can invoke the endpoint for real-time inference.

### Configure the endpoint

1. On the batch **Runs** page, select the run name link, and on the run detail page, select **Deploy** on the top menu bar to open the deployment wizard.

1. On the **Basic settings** page, specify an **Endpoint name** and **Deployment name** and select a **Virtual machine** type and **Instance count**.

1. You can select **Next** to configure advanced **Endpoint**, **Deployment**, and **Outputs & connections** settings. For this example, use the default settings.

1. Select **Review + Create** and then select **Create** to start the deployment.

### Test the endpoint

You can go to your endpoint detail page from the notification, or by selecting **Endpoints** in the studio left navigation and selecting your endpoint from the **Real-time endpoints** tab. It takes several minutes to deploy the endpoint. After the endpoint is deployed successfully, you can test it in the **Test** tab. 

Put the URL you want to test in the input box, and select **Test**. You see the result predicted by your endpoint.

## Clean up resources

To conserve compute resources and costs, you can stop your compute session if you're done using it for now. Select the running session and then select **Stop compute session**.

You can also stop a compute instance by selecting **Compute** from the studio left navigation, selecting your compute instance in the **Compute instances** list, and selecting **Stop**.

If you don't plan to use any of the resources that you created in this tutorial, you can delete them so they don't incur charges. In the Azure portal, search for and select **Resource groups**. From the list, select the resource group that contains the resources you created, and then select **Delete resource group** from the top menu on the resource group page.

## Related content

- [Manage compute session](how-to-manage-compute-session.md)
- [Develop a standard flow](how-to-develop-a-standard-flow.md)
- [Submit bulk test and evaluate a flow](how-to-develop-a-standard-flow.md)
- [Tune prompts using variants](how-to-tune-prompts-using-variants.md)
- [Deploy a flow](how-to-deploy-for-real-time-inference.md)
