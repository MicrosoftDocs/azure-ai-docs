---
title: Deploy a Flow as a Managed Online Endpoint for Real-Time Inference
titleSuffix: Microsoft Foundry
description: Learn how to deploy a flow as a managed online endpoint for real-time inference with Microsoft Foundry.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ms.topic: how-to
ms.date: 10/18/2025
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---

# Deploy a flow for real-time inference

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

After you build a prompt flow and test it, you can deploy it as an online endpoint. Deployments are hosted in an endpoint. They can receive data from clients and send responses in real time.

You can invoke the endpoint for real-time inference for chat, a copilot, or another generative AI application. Prompt flows support endpoint deployment from a flow or a bulk test run.

In this article, you learn how to deploy a flow as a managed online endpoint for real-time inference.

- Test your flow and get it ready for deployment.
- Create an online deployment.
- Grant permissions to the endpoint.
- Test the endpoint.
- Consume the endpoint.

## Prerequisites

 [!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

To deploy a prompt flow as an online endpoint, you need:

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry project.
- A `Microsoft.PolicyInsights` resource provider registered in your subscription. For more information, see [Register a resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1).

## Create an online deployment

After you build a flow and test it, create your online endpoint for real-time inference.

To deploy a prompt flow as an online endpoint in the Foundry portal:

1. Have a prompt flow ready for deployment. If you don't have one, see [Develop a prompt flow](./flow-develop.md).
1. Optional: Select **Chat** to test if the flow is working correctly. We recommend that you test your flow before deployment.

1. Select **Deploy** on the flow editor.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-from-flow.png" alt-text="Screenshot that shows the Deploy button from a prompt flow editor." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-from-flow.png":::

1. On the **Basic Settings** page, provide the necessary information.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-basic-settings.png" alt-text="Screenshot that shows the Basic settings page in the deployment wizard." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deploy-basic-settings.png":::

1. Select **Review + Create**. Or, select **Next** to proceed to the advanced settings pages not needed for this article.

1. Select **Create** to deploy the prompt flow.

1. To view the status of your deployment, select **Models + endpoints** on the left pane. After the deployment is created successfully, select the deployment to see more information.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-state-updating.png" alt-text="Screenshot that shows the deployment state in progress." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-state-updating.png":::

1. Select the **Consume** tab to see code samples that you can use to consume the deployed model in your application.

    On this page, you can also see the endpoint URL that you can use to consume the endpoint.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url.png" alt-text="Screenshot that shows the deployment detail page." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url.png":::

1. You can use the REST endpoint directly or get started with one of the samples shown here.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url-samples.png" alt-text="Screenshot that shows the deployment endpoint and code samples." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/deployments-score-url-samples.png":::

For information about how to deploy a base model, see [Deploy models with Foundry](deploy-models-managed.md).

## Settings and configurations

### Requirements text file

Optionally, you can specify extra packages that you need in `requirements.txt`. You can find `requirements.txt` in the root folder of your flow folder. When you deploy a prompt flow to a managed online endpoint in the UI, by default, the deployment uses the environment that was created based on the base image specified in `flow.dag.yaml` and the dependencies specified in `requirements.txt`.

The base image specified in `flow.dag.yaml` is created based on the prompt flow base image `mcr.microsoft.com/azureml/promptflow/promptflow-runtime-stable:<newest_version>`. To see the latest version, see [this list](https://mcr.microsoft.com/v2/azureml/promptflow/promptflow-runtime-stable/tags/list). If you don't specify the base image in `flow.dag.yaml`, the deployment uses the default base image `mcr.microsoft.com/azureml/promptflow/promptflow-runtime-stable:latest`.

:::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/flow-environment-image.png" alt-text="Screenshot that shows specifying the base image in the raw yaml file of the flow. " lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/flow-environment-image.png":::

### Basic settings

In this step, you configure the basic settings when you select **Deploy** on the flow editor.

|Property| Description |
|---|-----|
|**Endpoint**|Select whether you want to deploy a new endpoint or update an existing endpoint. <br> If you select **New**, you need to specify the endpoint name.|
|**Deployment name**| - In the same endpoint, the deployment name should be unique. <br> - If you select an existing endpoint and enter an existing deployment name, that deployment is overwritten with the new configurations. |
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

This setting identifies the authentication method for the endpoint. Key-based authentication provides a primary and secondary key that doesn't expire. Azure Machine Learning token-based authentication provides a token that periodically refreshes.

#### Identity type

The endpoint needs to access Azure resources for inferencing, such as Azure Container Registry or your Foundry hub connections. You can allow the endpoint permission to access Azure resources by giving permission to its managed identity.

System-assigned identity is created after your endpoint is created. The user creates the user-assigned identity. For more information, see [Managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview).

##### System assigned

The **Enforce access to connection secrets (preview)** option is enabled by default. If your flow uses connections, the endpoint needs to access connections to perform inference.

If you have connection secrets reader permission, the endpoint is granted access to the Azure Machine Learning Workspace Connection Secrets Reader role to access connections. If you disable this option, you need to grant this role to the system-assigned identity manually or ask your admin for help. For more information, see [Grant permission to the endpoint identity](#grant-permissions-to-the-endpoint).

##### User assigned

When you create the deployment, Azure tries to pull the user container image from the Foundry hub's container registry and mounts the user model and code artifacts into the user container from the hub's storage account.

If you create the associated endpoint with the **User Assigned Identity** option, grant the user-assigned identity the following roles before you create the deployment. Otherwise, the deployment creation fails.

|Scope|Role|Why it's needed|
|---|---|---|
|Foundry project|**Azure Machine Learning Workspace Connection Secrets Reader** role or a customized role with `Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action` | Gets project connections.|
|Foundry project container registry |**ACR Pull** |Pulls container images. |
|Foundry project default storage| **Storage Blob Data Reader**| Loads a model from storage. |
|Foundry project|**Azure Machine Learning Metrics Writer (preview)**| After you deploy the endpoint, if you want to monitor the endpoint-related metrics like CPU/GPU/Disk/Memory utilization, grant this permission to the identity.<br/><br/>Optional.|

For more information about how to grant permissions to the endpoint identity, see [Grant permissions to the endpoint](#grant-permissions-to-the-endpoint).

> [!IMPORTANT]
> If your flow uses authentication connections based on Microsoft Entra ID, you always need to grant the managed identity appropriate roles for the corresponding resources so that it can make API calls to that resource. This configuration is necessary whether you use system-assigned identity or user-assigned identity.
>
> For example, if your Azure OpenAI connection uses Microsoft Entra ID-based authentication, you need to grant your endpoint managed identity the Cognitive Services OpenAI User or Cognitive Services OpenAI Contributor role of the corresponding Azure OpenAI resources.

### Advanced settings: Outputs and connections

In this step, you can view all flow outputs and specify which outputs to include in the response of the endpoint you deploy. By default, all flow outputs are selected.

You can also specify the connections that the endpoint uses when it performs inference. By default, the endpoint inherits the connections from the flow.

After you configure and review all the preceding steps, select **Review + Create** to finish the creation.

Expect the endpoint creation to take more than 15 minutes. The stages include creating an endpoint, registering a model, and creating a deployment.

The deployment creation progress sends a notification that starts with **Prompt flow deployment**.

#### Enable tracing by turning on Application Insights diagnostics (preview)

If you enable this capability, tracing data and system metrics during inference time are collected in workspace-linked Application Insights. These metrics include token count, flow latency, and flow request. For more information, see [Enable tracing and collect feedback for a flow deployment](./develop/trace-production-sdk.md).

## Grant permissions to the endpoint

> [!IMPORTANT]
> Only the owner of the Azure resources can grant permissions by adding a role assignment. You might need to contact your Azure subscription owner. This person might be your IT admin.
>
> We recommend that you grant roles to the user-assigned identity as soon as the endpoint creation finishes. It might take more than 15 minutes for the granted permission to take effect.

To grant the required permissions in the Azure portal, follow these steps:

1. Go to the Foundry project overview page in the [Azure portal](https://ms.portal.azure.com/#home).

1. Select **Access control (IAM)**, and then select **Add role assignment**.

    :::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/access-control.png" alt-text="Screenshot that shows Access control with Add role assignment highlighted." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/access-control.png":::

1. Select **Azure Machine Learning Workspace Connection Secrets Reader**, and select **Next**.

    The **Azure Machine Learning Workspace Connection Secrets Reader** role is a built-in role that has permission to get hub connections.

    If you want to use a customized role, make sure that the customized role has the permission of `Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action`. Learn more about [how to create custom roles](/azure/role-based-access-control/custom-roles-portal#step-3-basics).

1. Select **Managed identity** and then select members:

    - **System-assigned identity**: Under **System-assigned managed identity**, select **Machine learning online endpoint** and search by endpoint name.
    - **User-assigned identity**: Select **User-assigned managed identity**, and search by identity name.

1. For user-assigned identity, grant permissions to the hub container registry and storage account. You can find the container registry and storage account on the hub overview page in the Azure portal.

    Go to the hub container registry overview page and select **Access control** > **Add role assignment**. Assign **ACR Pull** to the endpoint identity.

    Go to the hub default storage overview page and select **Access control** > **Add role assignment**. Assign **Storage Blob Data Reader** to the endpoint identity.

1. Optional: For user-assigned identity, if you want to monitor the endpoint-related metrics like CPU/GPU/Disk/Memory utilization, you need to grant the **Workspace metrics writer** role of the hub to the identity.

## Check the status of the endpoint

After the deployment finishes, you receive notifications. After the endpoint and deployment are created successfully, select **View details** in the notification to deployment detail page.

You can also go directly to the **Model + endpoints** page on the left pane and select the deployment to check the status.

## Test the endpoint

On the deployment detail page, select the **Test** tab.

For endpoints deployed from standard flow, you can enter values in the form editor or JSON editor to test the endpoint.

### Test the endpoint deployed from a chat flow

For endpoints deployed from a chat flow, you can test it in an immersive chat window.

The `chat_input` message was set during the development of the chat flow. You can put the `chat_input` message in the input box. If your flow has multiple inputs, specify the values for other inputs besides the `chat_input` message on the **Inputs** pane on the right side.

## Consume the endpoint

On the deployment detail page, select the **Consume** tab. You can find the REST endpoint and key/token to consume your endpoint. Sample code is also available for you to consume the endpoint in different languages.

:::image type="content" source="../media/prompt-flow/how-to-deploy-for-real-time-inference/consume-sample-code.png" alt-text="Screenshot that shows the sample code of consuming endpoints." lightbox = "../media/prompt-flow/how-to-deploy-for-real-time-inference/consume-sample-code.png":::

You need to input values for `RequestBody` or `data` and `api_key`. For example, if your flow has two inputs, `location` and `url`, specify data as the following example:

```json
 {
"location": "LA",
"url": "<the_url_to_be_classified>"
}
```

## Clean up resources

If you aren't going to use the endpoint after you finish this tutorial, delete the endpoint. The complete deletion might take 20 minutes.

## Related content

- Learn more about what you can do in [Foundry](../what-is-foundry.md).
- Get answers to frequently asked questions in the [Foundry FAQ](../faq.yml).
- [Enable trace and collect feedback for your deployment](./develop/trace-production-sdk.md).
