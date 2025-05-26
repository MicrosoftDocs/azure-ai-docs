---
title: 'Quickstart: Generate video with Sora'
titleSuffix: Azure OpenAI
description: Learn how to get started generating video clips with Azure OpenAI.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: quickstart
author: PatrickFarley
ms.author: pafarley
ms.date: 05/22/2025
---

# Quickstart: Generate a video with Sora (preview)

In this quickstart, you generate video clips using the Azure OpenAI service. The example uses the Sora model, which is a video generation model that creates realistic and imaginative video scenes from text instructions. This guide shows you how to create a video generation job, poll for its status, and retrieve the generated video.

For more information on video generation, see [Video generation concepts](./concepts/video-generation.md).


## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>.
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).
- Then, you need to deploy a `sora` model with your Azure resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](./how-to/create-resource.md).
- [Python 3.8 or later version](https://www.python.org/).


## Setup

### Retrieve key and endpoint

To successfully call the Azure OpenAI APIs, you need the following information about your Azure OpenAI resource:

| Variable | Name | Value |
|---|---|---|
| **Endpoint** | `api_base` | The endpoint value is located under **Keys and Endpoint** for your resource in the Azure portal. You can also find the endpoint via the **Deployments** page in Azure AI Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| **Key** | `api_key` | The key value is also located under **Keys and Endpoint** for your resource in the Azure portal. Azure generates two keys for your resource. You can use either value. |

Go to your resource in the Azure portal. On the navigation pane, select **Keys and Endpoint** under **Resource Management**. Copy the **Endpoint** value and an access key value. You can use either the **KEY 1** or **KEY 2** value. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="./media/quickstarts/endpoint.png" alt-text="Screenshot that shows the Keys and Endpoint page for an Azure OpenAI resource in the Azure portal." lightbox="./media/quickstarts/endpoint.png":::



[!INCLUDE [environment-variables](./includes/environment-variables.md)]



## Create a new Python application

Create a new Python file named `quickstart.py`. Open the new file in your preferred editor or IDE.
1. Replace the contents of `quickstart.py` with the following code. Change the value of `prompt` to your preferred text.
    
    ```python
    import os
    import time
    import requests
    
    # Set these variables with your values
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]  # e.g., "https://docs-test-001.openai.azure.com"
    api_key = os.environ["AZURE_OPENAI_KEY"]
    access_token = os.environ.get("AZURE_OPENAI_TOKEN")  # Optional: if using Azure AD auth
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    # 1. Create a video generation job
    create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version=preview"
    payload = {
        "prompt": "A cat playing piano in a jazz bar.",
        "model": "sora",
        "width": 1080,
        "height": 1080,
        "n_seconds": 10
    }
    response = requests.post(create_url, headers=headers, json=payload)
    response.raise_for_status()
    job_id = response.json()["body"]["id"]
    print(f"Job created: {job_id}")
    
    # 2. Poll for job status
    status_url = f"{endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version=preview"
    while True:
        status_response = requests.get(status_url, headers=headers)
        status_response.raise_for_status()
        status = status_response.json()["body"]["status"]
        print(f"Job status: {status}")
        if status == "succeeded":
            generations = status_response.json()["body"].get("generations", [])
            if not generations:
                raise Exception("No generations found in job result.")
            generation_id = generations[0]["id"]
            break
        elif status in ("failed", "cancelled"):
            raise Exception(f"Job did not succeed. Status: {status}")
        time.sleep(5)  # Wait before polling again
    
    # 3. Retrieve the generated video
    get_video_url = f"{endpoint}/openai/v1/video/generations/{generation_id}?api-version=preview"
    video_response = requests.get(get_video_url, headers=headers)
    video_response.raise_for_status()
    download_url = video_response.json()["body"]["generations"]
    print(f"Download your video at: {download_url}")
    ```
1. Run the application with the `python` command:

    ```console
    python quickstart.py
    ```

    Wait a few moments to get the response.

---