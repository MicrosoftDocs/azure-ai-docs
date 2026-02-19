---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 01/29/2026
ai-usage: ai-assisted
---



## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](/azure/ai-foundry/openai/concepts/models#video-generation-models).
- Then, you need to deploy a `sora` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Limitations and quotas

Sora video generation is currently in preview. Keep the following limitations in mind:

- **Region availability**: Sora is available only in **East US 2** and **Sweden Central** (Global Standard deployments).
- **Supported resolutions**: 480×480, 720×720, 1080×1080, 1280×720, 1920×1080 (width × height).
- **Video duration**: 5 to 20 seconds (`n_seconds` parameter).
- **Variants**: Generate 1 to 4 video variants per request (`n_variants` parameter).
- **Rate limits**: Subject to your deployment's tokens-per-minute (TPM) quota. See [Quotas and limits](../quotas-limits.md) for details.
- **Content filtering**: Prompts are subject to content moderation. Requests with harmful content are rejected.

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `video-generation-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir video-generation-quickstart && cd video-generation-quickstart
    ```
    
1. Create a virtual environment. If you already have Python 3.10 or higher installed, you can create a virtual environment using the following commands:

    **Windows**

    ```bash
    py -3 -m venv .venv
    .venv\scripts\activate
    ```

    **Linux**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    **macOS**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    Activating the Python environment means that when you run ```python``` or ```pip``` from the command line, you then use the Python interpreter contained in the ```.venv``` folder of your application. You can use the ```deactivate``` command to exit the python virtual environment, and can later reactivate it when needed.

    > [!TIP]
    > We recommend that you create and activate a new Python environment to use to install the packages you need for this tutorial. Don't install packages into your global python installation. You should always use a virtual or conda environment when installing python packages, otherwise you can break your global installation of Python.

1. Install the required packages.

    **Microsoft Entra ID**

    ```console
    pip install requests azure-identity
    ```

    The [azure-identity](/python/api/overview/azure/identity-readme) package provides `DefaultAzureCredential` for secure, keyless authentication.

    **API key**

    ```console
    pip install requests
    ```

    The [requests](https://requests.readthedocs.io/) library handles HTTP calls to the REST API.

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Generate video with Sora

You can generate a video with the Sora model by creating a video generation job, polling for its status, and retrieving the generated video. The following code shows how to do this via the REST API using Python.

### Choose your input type

Sora supports three input modes:

| Input type | Best for | Example use case |
|------------|----------|------------------|
| **Text prompt only** | Creating entirely new scenes from descriptions | "A cat playing piano in a jazz bar" |
| **Image + text prompt** | Animating a still image or using it as a starting frame | Bring a product photo to life |
| **Video + text prompt** | Extending or modifying existing video footage | Add visual effects to existing clips |

### Set up authentication

1. Create the `sora-quickstart.py` file and add the following code to authenticate your resource:

    **Microsoft Entra ID**

    ```python
    import json
    import requests
    import time
    import os
    from azure.identity import DefaultAzureCredential
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    deployment_name = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    if not endpoint or not deployment_name:
        raise ValueError("Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME.")
    
    # Keyless authentication
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")

    # Video generation uses 'preview' as the API version during the preview period
    api_version = 'preview'
    headers= { "Authorization": f"Bearer {token.token}", "Content-Type": "application/json" }
    ```


    **API key**

    ```python
    import json
    import requests
    import time
    import os
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    deployment_name = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    api_key = os.environ.get('AZURE_OPENAI_API_KEY')
    if not endpoint or not deployment_name or not api_key:
        raise ValueError(
            "Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME, and AZURE_OPENAI_API_KEY."
        )

    # Video generation uses 'preview' as the API version during the preview period
    api_version = 'preview'
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    ```
### Create the video generation job

1. Add the code to create and monitor the video generation job. Choose the input type that matches your use case.

    **Text prompt**

    ```python
    # 1. Create a video generation job
    create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version={api_version}"
    body = {
        "prompt": "A cat playing piano in a jazz bar.",
        "width": 480,
        "height": 480,
        "n_seconds": 5,
        "model": deployment_name
    }
    response = requests.post(create_url, headers=headers, json=body)
    response.raise_for_status()
    print("Full response JSON:", response.json())
    job_id = response.json()["id"]
    print(f"Job created: {job_id}")
    
    # 2. Poll for job status
    status_url = f"{endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version={api_version}"
    status=None
    while status not in ("succeeded", "failed", "cancelled"):
        time.sleep(5)  # Wait before polling again
        status_response = requests.get(status_url, headers=headers).json()
        status = status_response.get("status")
        print(f"Job status: {status}")
        
    # 3. Retrieve generated video 
    if status == "succeeded":
        generations = status_response.get("generations", [])
        if generations:
            print(f"✅ Video generation succeeded.")
            generation_id = generations[0].get("id")
            video_url = f"{endpoint}/openai/v1/video/generations/{generation_id}/content/video?api-version={api_version}"
            video_response = requests.get(video_url, headers=headers)
            if video_response.ok:
                output_filename = "output.mp4"
                with open(output_filename, "wb") as file:
                    file.write(video_response.content)
                    print(f'Generated video saved as "{output_filename}"')
        else:
            raise Exception("No generations found in job result.")
    else:
        raise Exception(f"Job didn't succeed. Status: {status}")
    ```


    **Image prompt**

    Replace the `"file_name"` field in `"inpaint_items"` with the name of your input image file. Also replace the construction of the `files` array, which associates the path to the actual file with the filename that the API uses.

    Use the `"crop_bounds"` data (image crop distances, from each direction, as a fraction of the total image dimensions) to specify which part of the image should be used in video generation.

    You can optionally set the `"frame_index"` to the frame in the generated video where your image should appear (the default is 0, the start of the video).

    The `"n_variants"` parameter specifies how many different video variations to generate from the same prompt (1 to 4). Each variant provides a unique interpretation of your input.


    ```python
    # 1. Create a video generation job with image inpainting (multipart upload)
    create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version={api_version}"
    
    # Flatten the body for multipart/form-data
    data = {
        "prompt": "A serene forest scene transitioning into autumn",
        "height": str(1080),
        "width": str(1920),
        "n_seconds": str(10),
        "n_variants": str(1),
        "model": deployment_name,
        # inpaint_items must be JSON string
        "inpaint_items": json.dumps([
            {
                "frame_index": 0,
                "type": "image",
                "file_name": "dog_swimming.jpg",
                "crop_bounds": {
                    "left_fraction": 0.1,
                    "top_fraction": 0.1,
                    "right_fraction": 0.9,
                    "bottom_fraction": 0.9
                }
            }
        ])
    }
    
    # Replace with your own image file path
    with open("dog_swimming.jpg", "rb") as image_file:
        files = [
            ("files", ("dog_swimming.jpg", image_file, "image/jpeg"))
        ]
        multipart_headers = {k: v for k, v in headers.items() if k.lower() != "content-type"}
        response = requests.post(
            create_url,
            headers=multipart_headers,
            data=data,
            files=files
        )
    
    if not response.ok:
        print("Error response:", response.status_code, response.text)
        response.raise_for_status()
    print("Full response JSON:", response.json())
    job_id = response.json()["id"]
    print(f"Job created: {job_id}")
    
    # 2. Poll for job status
    status_url = f"{endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version={api_version}"
    status = None
    while status not in ("succeeded", "failed", "cancelled"):
        time.sleep(5)
        status_response = requests.get(status_url, headers=headers).json()
        status = status_response.get("status")
        print(f"Job status: {status}")
    
    # 3. Retrieve generated video
    if status == "succeeded":
        generations = status_response.get("generations", [])
        if generations:
            generation_id = generations[0].get("id")
            video_url = f"{endpoint}/openai/v1/video/generations/{generation_id}/content/video?api-version={api_version}"
            video_response = requests.get(video_url, headers=headers)
            if video_response.ok:
                output_filename = "output.mp4"
                with open(output_filename, "wb") as file:
                    file.write(video_response.content)
                    print(f'✅ Generated video saved as "{output_filename}"')
        else:
            raise Exception("No generations found in job result.")
    else:
        raise Exception(f"Job didn't succeed. Status: {status}")
    ```




    **Video prompt**

    Replace the `"file_name"` field in `"inpaint_items"` with the name of your input video file. Also replace the construction of the `files` array, which associates the path to the actual file with the filename that the API uses.

    Use the `"crop_bounds"` data (image crop distances, from each direction, as a fraction of the total frame dimensions) to specify which part of the video frame should be used in video generation.

    You can optionally set the `"frame_index"` to the frame in the generated video where your input video should start (the default is 0, the beginning).


    ```python
    # 1. Create a video generation job with video inpainting (multipart upload)
    create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version={api_version}"
    
    # Flatten the body for multipart/form-data
    data = {
        "prompt": "A serene forest scene transitioning into autumn",
        "height": str(1080),
        "width": str(1920),
        "n_seconds": str(10),
        "n_variants": str(1),
        "model": deployment_name,
        # inpaint_items must be JSON string
        "inpaint_items": json.dumps([
            {
                "frame_index": 0,
                "type": "video",
                "file_name": "dog_swimming.mp4",
                "crop_bounds": {
                    "left_fraction": 0.1,
                    "top_fraction": 0.1,
                    "right_fraction": 0.9,
                    "bottom_fraction": 0.9
                }
            }
        ])
    }
    
    # Replace with your own video file path
    with open("dog_swimming.mp4", "rb") as video_file:
        files = [
            ("files", ("dog_swimming.mp4", video_file, "video/mp4"))
        ]
        multipart_headers = {k: v for k, v in headers.items() if k.lower() != "content-type"}
        response = requests.post(
            create_url,
            headers=multipart_headers,
            data=data,
            files=files
        )
    
    if not response.ok:
        print("Error response:", response.status_code, response.text)
        response.raise_for_status()
    print("Full response JSON:", response.json())
    job_id = response.json()["id"]
    print(f"Job created: {job_id}")
    
    # 2. Poll for job status
    status_url = f"{endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version={api_version}"
    status = None
    while status not in ("succeeded", "failed", "cancelled"):
        time.sleep(5)
        status_response = requests.get(status_url, headers=headers).json()
        status = status_response.get("status")
        print(f"Job status: {status}")
    
    # 3. Retrieve generated video
    if status == "succeeded":
        generations = status_response.get("generations", [])
        if generations:
            generation_id = generations[0].get("id")
            video_url = f"{endpoint}/openai/v1/video/generations/{generation_id}/content/video?api-version={api_version}"
            video_response = requests.get(video_url, headers=headers)
            if video_response.ok:
                output_filename = "output.mp4"
                with open(output_filename, "wb") as file:
                    file.write(video_response.content)
                    print(f'✅ Generated video saved as "{output_filename}"')
        else:
            raise Exception("No generations found in job result.")
    else:
        raise Exception(f"Job didn't succeed. Status: {status}")
    ```
1. Run the Python file.

    ```shell
    python sora-quickstart.py
    ```

    Video generation typically takes **1 to 5 minutes** depending on the resolution and duration. You should see status updates in your terminal as the job progresses through `queued`, `preprocessing`, `running`, `processing`, and finally `succeeded`.

### Output

The output will show the full response JSON from the video generation job creation request, including the job ID and status. 

```json
{
    "object": "video.generation.job",
    "id": "task_01jwcet0eje35tc5jy54yjax5q",
    "status": "queued",
    "created_at": 1748469875,
    "finished_at": null,
    "expires_at": null,
    "generations": [],
    "prompt": "A cat playing piano in a jazz bar.",
    "model": "<your-deployment-name>",
    "n_variants": 1,
    "n_seconds": 5,
    "height": 480,
    "width": 480,
    "failure_reason": null
}
```

The generated video will be saved as `output.mp4` in the current directory.

```text
Job created: task_01jwcet0eje35tc5jy54yjax5q
Job status: preprocessing
Job status: running
Job status: processing
Job status: succeeded
✅ Video generation succeeded.
Generated video saved as "output.mp4"
```

## Troubleshooting

If you encounter issues, check the following common problems and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid or expired credentials | For Microsoft Entra ID, run `az login` to refresh your token. For API key, verify `AZURE_OPENAI_API_KEY` is correct. |
| `403 Forbidden` | Missing role assignment | Assign the **Cognitive Services User** role to your account in the Azure portal. |
| `404 Not Found` | Incorrect endpoint or deployment name | Verify `AZURE_OPENAI_ENDPOINT` includes your resource name and `AZURE_OPENAI_DEPLOYMENT_NAME` matches your Sora deployment. |
| `429 Too Many Requests` | Rate limit exceeded | Wait and retry, or request a quota increase in the Azure portal. |
| `400 Bad Request` with dimension error | Unsupported resolution | Use a supported resolution: 480×480, 720×720, 1080×1080, 1280×720, or 1920×1080. |
| Job status `failed` | Content policy violation or internal error | Check `failure_reason` in the response. Modify your prompt if it triggered content filtering. |
| Timeout during polling | Long generation time | Videos can take up to 5 minutes. Increase your polling timeout or check job status manually. |

> [!TIP]
> To debug authentication issues, test your credentials with a simple API call first:
> ```python
> # Test endpoint connectivity
> test_url = f"{endpoint}/openai/deployments?api-version=2024-02-01"
> response = requests.get(test_url, headers=headers)
> print(response.status_code, response.text)
> ```

