---
title: Include file
description: Include file
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 03/24/2026
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include
  - classic-and-new
---

- [Set up your development environment](../how-to/develop/install-cli-sdk.md?tabs=python).
- Run `az login` or `az login --use-device-code` in your environment before running code.
- Install packages: `pip install azure-identity azure-mgmt-cognitiveservices~=13.7.0`. If you're in a notebook cell, use `%pip install` instead.
- Use `pip show azure-mgmt-cognitiveservices` to check that your version is 13.7 or greater.
- **Quick validation**: Before creating a project, verify your SDK and authentication by testing the client:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
    
    # Test authentication by instantiating the client
    credential = DefaultAzureCredential()
    subscription_id = "<your-subscription-id>"  # Replace with your subscription ID
    client = CognitiveServicesManagementClient(credential, subscription_id)
    print("✓ Authentication successful! Ready to create a project.")
    ```


- Start your script with the following code to create the `client` connection and variables used throughout this article. This example creates the project in East US:

    :::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/create_project.py" id="create_client":::

- (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID you want to use into `DefaultAzureCredential`:

    ```python
    DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
    ```
    