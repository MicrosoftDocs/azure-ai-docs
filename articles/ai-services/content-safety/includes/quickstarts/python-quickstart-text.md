---
title: "Quickstart: Analyze text content with Python"
description: In this quickstart, get started using the Azure AI Content Safety Python SDK to analyze text content for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2023
ms.topic: include
ms.date: 05/03/2023
ms.author: pafarley
---

[Reference documentation](https://pypi.org/project/azure-ai-contentsafety/) | [Library source code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentsafety/azure-ai-contentsafety) | [Package (PyPI)](https://pypi.org/project/azure-ai-contentsafety/) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/python/1.0.0) |

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/) 
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
* [Python 3.x](https://www.python.org/)
  * Your Python installation should include [pip](https://pip.pypa.io/en/stable/). You can check if you have pip installed by running `pip --version` on the command line. Get pip by installing the latest version of Python.

[!INCLUDE [Create environment variables](../env-vars.md)]


## Analyze text content

The following section walks through a sample request with the Python SDK.

1. Open a command prompt, navigate to your project folder, and create a new file named *quickstart.py*.
1. Run this command to install the Azure AI Content Safety library:

    ```console
    pip install azure-ai-contentsafety
    ```

1. Copy the following code into *quickstart.py*:

    ```python
    import os
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import HttpResponseError
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
    
    def analyze_text():
        # analyze text
        key = os.environ["CONTENT_SAFETY_KEY"]
        endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
    
        # Create an Azure AI Content Safety client
        client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
        # Contruct request
        request = AnalyzeTextOptions(text="Your input text")
    
        # Analyze text
        try:
            response = client.analyze_text(request)
        except HttpResponseError as e:
            print("Analyze text failed.")
            if e.error:
                print(f"Error code: {e.error.code}")
                print(f"Error message: {e.error.message}")
                raise
            print(e)
            raise

        hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
        self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
        sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
        violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)
    
        if hate_result:
            print(f"Hate severity: {hate_result.severity}")
        if self_harm_result:
            print(f"SelfHarm severity: {self_harm_result.severity}")
        if sexual_result:
            print(f"Sexual severity: {sexual_result.severity}")
        if violence_result:
            print(f"Violence severity: {violence_result.severity}")
    
    if __name__ == "__main__":
        analyze_text()
    ```
1. Replace `"Your input text"` with the text content you'd like to use.
    > [!TIP]
    > Text size and granularity
    >
    > See [Input requirements](../../overview.md#input-requirements) for maximum text length limitations.
1. Then run the application with the `python` command on your quickstart file.

    ```console
    python quickstart.py
    ```
