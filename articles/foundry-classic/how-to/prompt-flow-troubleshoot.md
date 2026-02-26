---
title: Troubleshoot Guidance for Prompt Flow
titleSuffix: Microsoft Foundry
description: This article addresses frequently asked questions about prompt flow usage. Learn how to deal with compute session related issues.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-prompt-flow
ms.custom:
  - ignite-2024
ms.topic: concept-article
author: lgayhardt
ms.author: lagayhar
ms.reviewer: none
ms.date: 10/16/2025
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---

# Troubleshoot guidance for prompt flow

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

This article addresses frequently asked questions about prompt flow usage.

## Compute session-related issues

### Why did the run fail with a "No module named XXX" error?

This type of error is related to a compute session that lacks required packages. If you use a default environment, make sure that the image of your compute session uses the latest version. If you use a custom base image, make sure that you installed all the required packages in your Docker context.

### How do I find the serverless instance used by a compute session?

You can view the serverless instance used by a compute session on the compute session list tab on the compute page. To learn more about how to manage serverless instance, see [Manage a compute session](./create-manage-compute-session.md#manage-a-compute-session).

## Compute session failures that use a custom base image: Flow run-related issues

### How do I find the raw inputs and outputs of the language model tool for further investigation?

In a prompt flow, on a **Flow** page with a successful run and run detail page, you can find the raw inputs and outputs of the language model tool in the output section. Select **View full output** to view the full output.

:::image type="content" source="../media/prompt-flow/view-full-output.png" alt-text="Screenshot that shows the View full output button on the language model node." lightbox = "../media/prompt-flow/view-full-output.png":::

The **Trace** section includes each request and response to the language model tool. You can check the raw message sent to the language model and the raw response from the language model.

:::image type="content" source="../media/prompt-flow/trace-large-language-model-tool.png" alt-text="Screenshot that shows a raw request send to language model and the response from the language model." lightbox = "../media/prompt-flow/trace-large-language-model-tool.png":::

### How do I fix a 429 error from Azure OpenAI?

You might encounter a 429 error from Azure OpenAI. This error means that you reached the rate limit of Azure OpenAI. You can check the error message in the output section of the language model node. To learn more about the rate limit, see [Azure OpenAI in Microsoft Foundry Models quotas and limits](../openai/quotas-limits.md).

:::image type="content" source="../media/prompt-flow/429-rate-limit.png" alt-text="Screenshot that shows a 429 rate limit error from Azure OpenAI." lightbox = "../media/prompt-flow/429-rate-limit.png":::

### How do I identify which node consumes the most time?

1. Check the compute session logs.

1. Try to find the following warning log format: `<node_name> has been running for <duration> seconds`.

    For example:

   - **Case 1:** Python script node runs for a long time.

        :::image type="content" source="../media/prompt-flow/runtime-timeout-running-for-long-time.png" alt-text="Screenshot that shows a timeout run sign." lightbox = "../media/prompt-flow/runtime-timeout-running-for-long-time.png":::

        In this case, you can see that `PythonScriptNode` was running for a long time, almost 300 seconds. Check the node details to see what's causing the problem.

   - **Case 2:** The language model node runs for a long time.

        :::image type="content" source="../media/prompt-flow/runtime-timeout-by-language-model-timeout.png" alt-text="Screenshot that shows timeout logs caused by a language model timeout." lightbox = "../media/prompt-flow/runtime-timeout-by-language-model-timeout.png":::

        If you see the message `request canceled` in the logs, it might be because the OpenAI API call is taking too long and exceeding the timeout limit.

        A network issue or a complex request that requires more processing time might cause the OpenAI time out.
     
        Wait a few seconds and retry your request. This action usually resolves any network issues.

        If retrying doesn't work, check whether you're using a long context model, such as `gpt-4-32k`, and set a large value for `max_tokens`. If so, the behavior is expected because your prompt might generate a long response that takes longer than the interactive mode's upper threshold. In this situation, we recommend that you try the `Bulk test` mode, which doesn't have a timeout setting.

## Compute session failures that use a custom base image: Flow deployment-related issues

### How do I resolve an upstream request timeout issue?

If you use the Azure CLI or SDK to deploy the flow, you might encounter a timeout error. By default, `request_timeout_ms` is `5000`. You can specify a maximum of five minutes, which is 300,000 ms. The following example shows how to specify a request timeout in the deployment .yaml file. To learn more, see [CLI managed online deployment YAML schema](/azure/machine-learning/reference-yaml-deployment-managed-online).

```yaml
request_settings:
  request_timeout_ms: 300000
```

### What do I do when OpenAI API generates an authentication error?

If you regenerate your Azure OpenAI key and manually update the connection used in a prompt flow, you might see error messages like "Unauthorized. Access token is missing, invalid, audience is incorrect or have expired." You might see these messages when you invoke an existing endpoint that was created before the key was regenerated.

This error occurs because the connections used in the endpoints/deployments aren't automatically updated. You should manually update any change for a key or secrets in deployments, which aims to avoid affecting online production deployment because of unintentional offline operation.

- If you deployed the endpoint in the Foundry portal, redeploy the flow to the existing endpoint by using the same deployment name.
- If you deployed by using the SDK or the Azure CLI, make a modification to the deployment definition, such as adding a dummy environment variable. Then use `az ml online-deployment update` to update your deployment.

### How do I resolve vulnerability issues in prompt flow deployments?

For prompt flow runtime-related vulnerabilities, try the following approaches:

- Update the dependency packages in your `requirements.txt` file in your flow folder.
- If you use a customized base image for your flow, update the prompt flow runtime to the latest version and rebuild your base image. Then redeploy the flow.

For any other vulnerabilities of managed online deployments, Azure AI fixes the issues monthly.

### What do I do if I get "MissingDriverProgram" or "Could not find driver program in the request" errors?

If you deploy your flow and encounter the following error, it might be related to the deployment environment:

```text
'error': 
{
    'code': 'BadRequest', 
    'message': 'The request is invalid.', 
    'details': 
         {'code': 'MissingDriverProgram', 
          'message': 'Could not find driver program in the request.', 
          'details': [], 
          'additionalInfo': []
         }
}
```

```text
Could not find driver program in the request
```

There are two ways to fix this error:

- Recommended: Find the container image URI on your custom environment detail page. Set it as the flow base image in the `flow.dag.yaml` file. When you deploy the flow in the UI, select **Use environment of current flow definition**. The back-end service creates the customized environment based on this base image and `requirement.txt` for your deployment. For more information, see [Requirements text file](./flow-deploy.md#requirements-text-file).
- Add `inference_config` in your custom environment definition.

The following sample is an example of a customized environment definition.

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: pf-customized-test
build:
  path: ./image_build
  dockerfile_path: Dockerfile
description: promptflow customized runtime
inference_config:
  liveness_route:
    port: 8080
    path: /health
  readiness_route:
    port: 8080
    path: /health
  scoring_route:
    port: 8080
    path: /score
```

### What do I do if my model response takes too long?

You might notice that the deployment takes a long time to respond. This delay can occur because of several factors:

- The model used in the flow isn't powerful enough. For example, use GPT 3.5 instead of `text-ada`.
- The index query isn't optimized and takes too long.
- The flow has many steps to process.

To improve the performance of the model, consider optimizing the endpoint with the preceding considerations.

### What do I do if I'm unable to fetch deployment schema?

After you deploy the endpoint, you need to test it on the **Test** tab on the deployment detail page. To get to the **Test** tab, on the left pane, under **My assets**, select **Models + endpoints**. Then select the deployment to view the details. If the **Test** tab shows **Unable to fetch deployment schema**, try the following two methods:

:::image type="content" source="../media/prompt-flow//unable-to-fetch-deployment-schema.png" alt-text="Screenshot that shows the Test tab on the deployment detail page." lightbox = "../media/prompt-flow/unable-to-fetch-deployment-schema.png":::

- Make sure that you granted the correct permission to the endpoint identity. For more information, see [Grant permissions to the endpoint](./flow-deploy.md#grant-permissions-to-the-endpoint).
- If you ran your flow in an old version runtime and then deployed the flow, maybe the deployment used the environment of the runtime that was the old version. To update the runtime, follow the steps in [Upgrade compute instance runtime](./create-manage-compute-session.md#upgrade-compute-instance-runtime). Rerun the flow in the latest runtime, and then deploy the flow again.

### What do I do if I get an "Access denied to list workspace secret" error?

If you encounter an error like "Access denied to list workspace secret," check whether you granted the correct permission to the endpoint identity. For more information, see [Grant permissions to the endpoint](./flow-deploy.md#grant-permissions-to-the-endpoint).
