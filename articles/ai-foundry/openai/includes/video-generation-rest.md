---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 5/29/2025
---



## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](/azure/ai-foundry/openai/concepts/models#video-generation-models).
- Then, you need to deploy a `sora` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

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
    
    # [Windows](#tab/windows)
    
    ```bash
    py -3 -m venv .venv
    .venv\scripts\activate
    ```
    
    # [Linux](#tab/linux)
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
    # [macOS](#tab/macos)
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
    ---
    
    Activating the Python environment means that when you run ```python``` or ```pip``` from the command line, you then use the Python interpreter contained in the ```.venv``` folder of your application. You can use the ```deactivate``` command to exit the python virtual environment, and can later reactivate it when needed.

    > [!TIP]
    > We recommend that you create and activate a new Python environment to use to install the packages you need for this tutorial. Don't install packages into your global python installation. You should always use a virtual or conda environment when installing python packages, otherwise you can break your global installation of Python.

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `azure-identity` package with:

    ```console
    pip install azure-identity
    ```


## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Generate video with Sora

You can generate a video with the Sora model by creating a video generation job, polling for its status, and retrieving the generated video. The following code shows how to do this via the REST API using Python.

1. Create the `sora-quickstart.py` file and add the following code to authenticate your resource:

    ## [Microsoft Entra ID](#tab/keyless)

    ```python
    import requests
    import base64 
    import os
    from azure.identity import DefaultAzureCredential
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    
    # Keyless authentication
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")

    api_version = 'preview'
    headers= { "Authorization": f"Bearer {token.token}", "Content-Type": "application/json" }
    ```

    ## [API key](#tab/api-key)

    ```python
    import requests
    import base64 
    import os
    from azure.identity import DefaultAzureCredential
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']

    api_version = 'preview'
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    ```
    ---

1. Create the video generation job. You can create it from a text prompt only, or from an input image and text prompt.

    ## [Text prompt](#tab/text-prompt)

    ```python
    # 1. Create a video generation job
    create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version={api_version}"
    body = {
        "prompt": "A cat playing piano in a jazz bar.",
        "width": 480,
        "height": 480,
        "n_seconds": 5,
        "model": "sora"
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

    ## [Image prompt](#tab/image-prompt)

    Replace the `"file_name"` field in `"inpaint_items"` with the name of your input image file. Also replace the construction of the `files` array, which associates the path to the actual file with the filename that the API uses.

    Use the `"crop_bounds"` data (image crop distances, from each direction, as a fraction of the total image dimensions) to specify which part of the image should be used in video generation.

    You can optionally set the `"frame_index"` to the frame in the generated video where your image should appear (the default is 0, the start of the video).


    ```python
    # 1. Create a video generation job with image inpainting (multipart upload)
    create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version=preview"
    
    # Flatten the body for multipart/form-data
    data = {
        "prompt": "A serene forest scene transitioning into autumn",
        "height": str(1080),
        "width": str(1920),
        "n_seconds": str(10),
        "n_variants": str(1),
        "model": "sora",
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
    status_url = f"{endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version=preview"
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
            video_url = f"{endpoint}/openai/v1/video/generations/{generation_id}/content/video?api-version=preview"
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



    ## [Video prompt](#tab/video-prompt)

    Replace the `"file_name"` field in `"inpaint_items"` with the name of your input video file. Also replace the construction of the `files` array, which associates the path to the actual file with the filename that the API uses.

    Use the `"crop_bounds"` data (image crop distances, from each direction, as a fraction of the total frame dimensions) to specify which part of the video frame should be used in video generation.

    You can optionally set the `"frame_index"` to the frame in the generated video where your input video should start (the default is 0, the beginning).


    ```python
    # 1. Create a video generation job with video inpainting (multipart upload)
    create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version=preview"
    
    # Flatten the body for multipart/form-data
    data = {
        "prompt": "A serene forest scene transitioning into autumn",
        "height": str(1080),
        "width": str(1920),
        "n_seconds": str(10),
        "n_variants": str(1),
        "model": "sora",
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
    status_url = f"{endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version=preview"
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
            video_url = f"{endpoint}/openai/v1/video/generations/{generation_id}/content/video?api-version=preview"
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
    ---


1. Run the Python file.

    ```shell
    python sora-quickstart.py
    ```

    Wait a few moments to get the response.

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
    "model": "sora",
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

