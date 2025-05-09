---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 01/23/2025
ms.topic: include
---

Before troubleshooting, verify that you have the right permissions assigned:

1. Go to the [Azure portal](https://portal.azure.com) and locate the **Azure AI Services** resource you're using.

2. On the left pane, select **Access control (IAM)** and then select **Check access**.

3. Type the name of the user or identity you are using to connect to the service.

4. Verify that the role **Cognitive Services User** is listed (or a role that contains the required permissions as explained in [Prerequisites](#prerequisites)).

    > [!IMPORTANT]
    > Roles like **Owner** or **Contributor** don't provide access via Microsoft Entra ID.

5. If not listed, follow the steps in this guide before continuing.

The following table contains multiple scenarios that can help troubleshooting Microsoft Entra ID:

| Error / Scenario     | Root cause    | Solution |
| -------------------- | ------------- | -------- |
| You're using an SDK. | Known issues. | Before making further troubleshooting, it's advisable to install the latest version of the software you are using to connect to the service. Authentication bugs may have been fixed in a newer version of the software you're using. |
| `401 Principal does not have access to API/Operation` | The request indicates authentication in the correct way, however, the user principal doesn't have the required permissions to use the inference endpoint. | Ensure you have: <br /> 1. Assigned the role **Cognitive Services User** to your principal to the Azure AI Services resource. Notice that **Cognitive Services OpenAI User** grants only access to OpenAI models. **Owner** or **Contributor** don't provide access either.<br /> 2. Wait at least 5 minutes before making the first call. |
| `401 HTTP/1.1 401 PermissionDenied` | The request indicates authentication in the correct way, however, the user principal doesn't have the required permissions to use the inference endpoint. | Assigned the role **Cognitive Services User** to your principal in the Azure AI Services resource. Roles like **Administrator** or **Contributor** don't grand inference access. Wait at least 5 minutes before making the first call. |
| You're using REST API calls and you get `401 Unauthorized. Access token is missing, invalid, audience is incorrect, or have expired.` | The request is failing to perform authentication with Entra ID. | Ensure the `Authentication` header contains a valid token with a scope `https://cognitiveservices.azure.com/.default`. |
| You're using `AzureOpenAI` class and you get `401 Unauthorized. Access token is missing, invalid, audience is incorrect, or have expired.` | The request is failing to perform authentication with Entra ID. | Ensure that you are using an **OpenAI model** connected to the endpoint `https://<resource>.openai.azure.com`. You can't use `OpenAI` class or a Models-as-a-Service model. If your model is not from OpenAI, use the Azure AI Inference SDK. |
| You're using the Azure AI Inference SDK and you get `401 Unauthorized. Access token is missing, invalid, audience is incorrect, or have expired.` | The request is failing to perform authentication with Entra ID. | Ensure you're connected to the endpoint `https://<resource>.services.ai.azure.com/model` and that you indicated the right scope for Entra ID (`https://cognitiveservices.azure.com/.default`). |
| `404 Not found` | The endpoint URL is incorrect based on the SDK you are using, or the model deployment doesn't exist. | Ensure you are using the right SDK connected to the right endpoint: <br /> 1. If you are using the Azure AI inference SDK, ensure the endpoint is `https://<resource>.services.ai.azure.com/model` with `model="<model-deployment-name>"` in the payloads, or endpoint is `https://<resource>.openai.azure.com/deployments/<model-deployment-name>`. <br /> If you are using the `AzureOpenAI` class, ensure the endpoint is `https://<resource>.openai.azure.com`. |
