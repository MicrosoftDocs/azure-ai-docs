---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 01/22/2026
ms.topic: include
---

Before you troubleshoot, verify that you have the right permissions assigned:

1. Go to the [Azure portal](https://portal.azure.com) and locate the **Microsoft Foundry resource** that you're using.

1. On the left pane, select **Access control (IAM)** and then select **Check access**.

1. Type the name of the user or identity you're using to connect to the service.

1. Verify that the role **Cognitive Services User** is listed (or a role that contains the required permissions, as explained in the Prerequisites section).

    > [!IMPORTANT]
    > Roles like **Owner** or **Contributor** don't provide access via Microsoft Entra ID.

1. If the role isn't listed, follow the steps in this guide before you continue.

The following table contains multiple scenarios that can help you troubleshoot Microsoft Entra ID:

| Error / Scenario     | Root cause    | Solution |
| -------------------- | ------------- | -------- |
| You're using an SDK | Known issues | Before you troubleshoot further, install the latest version of the software you're using to connect to the service. Authentication bugs might already be fixed in a newer version of the software you're using. |
| `401 Principal does not have access to API/Operation` | The request indicates authentication in the correct way, but the user principal doesn't have the required permissions to use the inference endpoint. | Ensure you have: <br /> 1. Assigned the role **Cognitive Services User** to your principal to the Foundry resource. Notice that **Cognitive Services OpenAI User** grants only access to OpenAI models. **Owner** or **Contributor** don't provide access either.<br /> 1. Waited at least 5 minutes before making the first call. |
| `401 HTTP/1.1 401 PermissionDenied` | The request indicates authentication in the correct way, but the user principal doesn't have the required permissions to use the inference endpoint. | Assigned the role **Cognitive Services User** to your principal in the Foundry resource. Roles like **Administrator** or **Contributor** don't grant inference access. Wait at least 5 minutes before making the first call. |
| You're using REST API calls and you get `401 Unauthorized. Access token is missing, invalid, audience is incorrect, or have expired.` | The request fails to authenticate with Microsoft Entra ID. | Ensure the `Authentication` header contains a valid token with a scope `https://cognitiveservices.azure.com/.default`. |
| You're using `AzureOpenAI` class and you get `401 Unauthorized. Access token is missing, invalid, audience is incorrect, or have expired.` | The request fails to perform authentication with Microsoft Entra ID. | Ensure that you're using an **OpenAI model** connected to the endpoint `https://<resource>.openai.azure.com`. You can't use `OpenAI` class or a Models-as-a-Service model. If your model isn't from OpenAI, use the Azure AI Inference SDK. |
| You're using the Azure AI Inference SDK and you get `401 Unauthorized. Access token is missing, invalid, audience is incorrect, or have expired.` | The request fails to perform authentication with Microsoft Entra ID. | Ensure you're connected to the endpoint `https://<resource>.services.ai.azure.com/model` and that you indicated the right scope for Microsoft Entra ID (`https://cognitiveservices.azure.com/.default`). |
| `404 Not found` | The endpoint URL is incorrect based on the SDK you're using, or the model deployment doesn't exist. | Ensure you're using the right SDK connected to the right endpoint: <br /> 1. If you're using the Azure AI inference SDK, ensure the endpoint is `https://<resource>.services.ai.azure.com/model` with `model="<model-deployment-name>"` in the payloads, or endpoint is `https://<resource>.openai.azure.com/deployments/<model-deployment-name>`. <br /> 1. If you're using the `AzureOpenAI` class, ensure the endpoint is `https://<resource>.openai.azure.com`. |
