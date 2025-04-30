---
title: Deploy a Flow as a Managed Online Endpoint for Real-Time Inference
titleSuffix: Azure AI Foundry
description: Learn how to deploy a flow as a managed online endpoint for real-time inference with Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 01/27/2025
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
---

# Deploy a flow for real-time inference

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

After you build a prompt flow and test it properly, you might want to deploy it as an online endpoint. Deployments are hosted within an endpoint, and they can receive data from clients and send responses back in real time.

You can invoke the endpoint for real-time inference for chat, a copilot, or another generative AI application. Prompt flow supports endpoint deployment from a flow or a bulk test run.

In this article, you learn how to deploy a flow as a managed online endpoint for real-time inference. The steps you take are:

- Test your flow and get it ready for deployment.
- Create an online deployment.
- Grant permissions to the endpoint.
- Test the endpoint.
- Consume the endpoint.

## Prerequisites

 [!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

To deploy a prompt flow as an online endpoint, you need:

* An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.
* An Azure AI Foundry project.
* A `Microsoft.PolicyInsights` resource provider registered in the selected subscription. For more information on how to register a resource provider, see [Register a resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1).

## Create an online deployment

After you build a flow and test it properly, it's time to create your online endpoint for real-time inference.

To deploy a prompt flow as an online endpoint in the Azure AI Foundry portal:

1. Have a prompt flow ready for deployment. If you don't have one, see [Develop a prompt flow](./flow-develop.md).
1. Optional: Select **Chat** to test if the flow is working correctly. We recommend that you test your flow before deployment.

1. Select **Deploy** on the flow editor.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-from-flow.png" alt-text="Screenshot that shows the Deploy button from a prompt flow editor." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-from-flow.png":::

1. Provide the requested information on the **Basic Settings** page in the deployment wizard.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-basic-settings.png" alt-text="Screenshot that shows the Basic settings page in the deployment wizard." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-basic-settings.png":::

1. Select **Review + Create** to review the settings and create the deployment. Otherwise, select **Next** to proceed to the advanced settings pages.

1. Select **Create** to deploy the prompt flow.

1. To view the status of your deployment, select **Models + endpoints** on the left pane. After the deployment is created successfully, select the deployment to see more information.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-state-updating.png" alt-text="Screenshot that shows the deployment state in progress." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-state-updating.png":::

1. Select the **Consume** tab to see code samples that you can use to consume the deployed model in your application.

    On this page, you can also see the endpoint URL that you can use to consume the endpoint.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url.png" alt-text="Screenshot that shows the deployment detail page." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url.png":::

1. You can use the REST endpoint directly or get started with one of the samples shown here.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url-samples.png" alt-text="Screenshot that shows the deployment endpoint and code samples." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url-samples.png":::

For information about how to deploy a base model, see [Deploy models with Azure AI Foundry](deploy-models-managed.md).

## Settings and configurations

### Requirements text file

Optionally, you can specify extra packages that you need in `requirements.txt`. You can find `requirements.txt` in the root folder of your flow folder. When you deploy a prompt flow to a managed online endpoint in the UI, by default, the deployment uses the environment that was created based on the base image specified in `flow.dag.yaml` and the dependencies specified in `requirements.txt` of the flow.

The base image specified in `flow.dag.yaml` must be created based on the prompt flow base image `mcr.microsoft.com/azureml/promptflow/promptflow-runtime-stable:<newest_version>`. You can find the latest version on [this website](https://mcr.microsoft.com/v2/azureml/promptflow/promptflow-runtime-stable/tags/list). If you don't specify the base image in `flow.dag.yaml`, the deployment uses the default base image `mcr.microsoft.com/azureml/promptflow/promptflow-runtime-stable:latest`.

:::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/flow-environment-image.png" alt-text="Screenshot that shows specifying the base image in the raw yaml file of the flow. " lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/flow-environment-image.png":::

### Basic settings

In this step, you configure the basic settings when you select **Deploy** on the flow editor.

|Property| Description |
|---|-----|
|**Endpoint**|Select whether you want to deploy a new endpoint or update an existing endpoint. <br> If you select **New**, you need to specify the endpoint name.|
|**Deployment name**| - Within the same endpoint, the deployment name should be unique. <br> - If you select an existing endpoint and input an existing deployment name, that deployment is overwritten with the new configurations. |
|**Virtual machine**| The virtual machine size to use for the deployment.|
|**Instance count**| The number of instances to use for the deployment. Specify the value on the workload you expect. For high availability, we recommend that you set the value to at least `3`. We reserve an extra 20% for performing upgrades.|
|**Inference data collection**| If you enable this setting, the flow inputs and outputs are autocollected in an Azure Machine Learning data asset. You can use them for later monitoring.|

After you finish the basic settings, select **Review + Create** to finish the creation. You can also select **Next** to configure advanced settings.

### Advanced settings: Endpoint

You can specify the following settings for the endpoint.

:::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-advanced-endpoint.png" alt-text="Screenshot that shows the advanced endpoint settings." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-advanced-endpoint.png":::

In the **Advanced settings** workflow, you can also specify deployment tags and select a custom environment.

:::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-advanced-deployment.png" alt-text="Screenshot that shows the advanced deployment settings." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-advanced-deployment.png":::

#### Authentication type

This setting identifies the authentication method for the endpoint. Key-based authentication provides a primary and secondary key that doesn't expire. Azure Machine Learning token-based authentication provides a token that periodically refreshes automatically.

#### Identity type

The endpoint needs to access Azure resources, such as Azure Container Registry or your Azure AI Foundry hub connections, for inferencing. You can allow the endpoint permission to access Azure resources by giving permission to its managed identity.

System-assigned identity is autocreated after your endpoint is created. The user creates the user-assigned identity. For more information, see the [managed identities overview](/azure/active-directory/managed-identities-azure-resources/overview).

##### System assigned

Notice the option **Enforce access to connection secrets (preview)**. If your flow uses connections, the endpoint needs to access connections to perform inference. The option is enabled by default. 

The endpoint is granted the Azure Machine Learning Workspace Connection Secrets Reader role to access connections automatically if you have connection secrets reader permission. If you disable this option, you need to grant this role to the system-assigned identity manually or ask your admin for help. For more information, see [Grant permission to the endpoint identity](#grant-permissions-to-the-endpoint).

##### User assigned

When you create the deployment, Azure tries to pull the user container image from the Azure AI Foundry hub's container registry and mounts the user model and code artifacts into the user container from the hub's storage account.

If you created the associated endpoint with the **User Assigned Identity** option, the user-assigned identity must be granted the following roles before the deployment creation. Otherwise, the deployment creation fails.

|Scope|Role|Why it's needed|
|---|---|---|
|Azure AI Foundry project|**Azure Machine Learning Workspace Connection Secrets Reader** role or a customized role with `Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action` | Gets project connections.|
|Azure AI Foundry project container registry |**ACR Pull** |Pulls container images. |
|Azure AI Foundry project default storage| **Storage Blob Data Reader**| Loads a model from storage. |
|Azure AI Foundry project|**Azure Machine Learning Metrics Writer (preview)**| After you deploy the endpoint, if you want to monitor the endpoint-related metrics like CPU/GPU/Disk/Memory utilization, give this permission to the identity.<br/><br/>Optional.|

For more information about how to grant permissions to the endpoint identity, see [Grant permissions to the endpoint](#grant-permissions-to-the-endpoint).

> [!IMPORTANT]
> If your flow uses authentication connections based on Microsoft Entra ID, whether you use system-assigned identity or user-assigned identity, you always need to grant the managed identity appropriate roles of the corresponding resources so that it can make API calls to that resource. For example, if your Azure OpenAI connection uses Microsoft Entra ID-based authentication, you need to grant your endpoint managed identity the Cognitive Services OpenAI User or Cognitive Services OpenAI Contributor role of the corresponding Azure OpenAI resources.

### Advanced settings: Outputs and connections

In this step, you can view all flow outputs and specify which outputs to include in the response of the endpoint you deploy. By default, all flow outputs are selected.

You can also specify the connections that are used by the endpoint when it performs inference. By default, they're inherited from the flow.

After you configure and review all the preceding steps, select **Review + Create** to finish the creation.

Expect the endpoint creation to take more than 15 minutes. The stages include creating an endpoint, registering a model, and creating a deployment.

The deployment creation progress sends a notification that starts with **Prompt flow deployment**.

#### Enable tracing by turning on Application Insights diagnostics (preview)

If you enable this capability, tracing data and system metrics during inference time (such as token count, flow latency, and flow request) are collected into workspace-linked Application Insights. To learn more, see [Prompt flow serving tracing data and metrics](./develop/trace-production-sdk.md).

## Grant permissions to the endpoint

> [!IMPORTANT]
> Granting permissions (adding a role assignment) is enabled only to the owner of the specific Azure resources. You might need to ask your Azure subscription owner for help. This person might be your IT admin.
>
> We recommend that you grant roles to the user-assigned identity as soon as the endpoint creation finishes. It might take more than 15 minutes for the granted permission to take effect.

To grant the required permissions in the Azure portal UI, follow these steps:

1. Go to the Azure AI Foundry project overview page in the [Azure portal](https://ms.portal.azure.com/#home).

1. Select **Access control (IAM)**, and then select **Add role assignment**.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/access-control.png" alt-text="Screenshot that shows Access control with Add role assignment highlighted." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/access-control.png":::

1. Select **Azure Machine Learning Workspace Connection Secrets Reader**, and select **Next**.

    The **Azure Machine Learning Workspace Connection Secrets Reader** role is a built-in role that has permission to get hub connections.

    If you want to use a customized role, make sure that the customized role has the permission of `Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action`. Learn more about [how to create custom roles](/azure/role-based-access-control/custom-roles-portal#step-3-basics).

1. Select **Managed identity** and then select members:

    - **System-assigned identity**: Under **System-assigned managed identity**, select **Machine learning online endpoint** and search by endpoint name.
    - **User-assigned identity**: Select **User-assigned managed identity**, and search by identity name.

1. For user-assigned identity, you need to grant permissions to the hub container registry and storage account. You can find the container registry and storage account on the hub overview page in the Azure portal.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/storage-container-registry.png" alt-text="Screenshot that shows the overview page with the storage and container registry." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/storage-container-registry.png":::

    Go to the hub container registry overview page and select **Access control** > **Add role assignment**. Assign **ACR Pull** to the endpoint identity.

    Go to the hub default storage overview page and select **Access control** > **Add role assignment**. Assign **Storage Blob Data Reader** to the endpoint identity.

1. Optional: For user-assigned identity, if you want to monitor the endpoint-related metrics like CPU/GPU/Disk/Memory utilization, you need to grant the **Workspace metrics writer** role of the hub to the identity.

## Check the status of the endpoint

You receive notifications after you finish the deployment wizard. After the endpoint and deployment are created successfully, select **View details** in the notification to deployment detail page.

You can also go directly to the **Model + endpoints** page on the left pane, select the deployment, and check the status.

## Test the endpoint

On the deployment detail page, select the **Test** tab.

For endpoints deployed from standard flow, you can input values in the form editor or JSON editor to test the endpoint.

### Test the endpoint deployed from a chat flow

For endpoints deployed from a chat flow, you can test it in an immersive chat window.

The `chat_input` message was set during the development of the chat flow. You can put the `chat_input` message in the input box. If your flow has multiple inputs, you can specify the values for other inputs besides the `chat_input` message on the **Inputs** pane on the right side.

## Consume the endpoint

On the deployment detail page, select the **Consume** tab. You can find the REST endpoint and key/token to consume your endpoint. Sample code is also available for you to consume the endpoint in different languages.

:::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/consume-sample-code.png" alt-text="Screenshot that shows the sample code of consuming endpoints." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/consume-sample-code.png":::

You need to input values for `RequestBody` or `data` and `api_key`. For example, if your flow has two inputs, `location` and `url`, you need to specify data as the following example:

```json
 {
"location": "LA",
"url": "<the_url_to_be_classified>"
}
```

## Clean up resources

If you aren't going to use the endpoint after you finish this tutorial, delete the endpoint. The complete deletion might take approximately 20 minutes.

## Related content

- Learn more about what you can do in [Azure AI Foundry](../what-is-azure-ai-foundry.md).
- Get answers to frequently asked questions in the [Azure AI Foundry FAQ](../faq.yml).
- [Enable trace and collect feedback for your deployment](./develop/trace-production-sdk.md).
