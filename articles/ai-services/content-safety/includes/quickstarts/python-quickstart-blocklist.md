---
title: "Quickstart: Use a blocklist with Python"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 02/22/2025
ms.author: pafarley
---

[Reference documentation](https://pypi.org/project/azure-ai-contentsafety/) | [Library source code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentsafety/azure-ai-contentsafety) | [Package (PyPI)](https://pypi.org/project/azure-ai-contentsafety/) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/python/1.0.0) |

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
* [Python 3.x](https://www.python.org/)
  * Your Python installation should include [pip](https://pip.pypa.io/en/stable/). You can check if you have pip installed by running `pip --version` on the command line. Get pip by installing the latest version of Python.

[!INCLUDE [Create environment variables](../env-vars.md)]

## Create and use a blocklist

The code in this section creates a new blocklist, adds items to it, and then analyzes a text string against the blocklist.

1. Open a command prompt, navigate to your project folder, and create a new file named *quickstart.py*.
1. Run this command to install the Azure AI Content Safety library:

    ```console
    pip install azure-ai-contentsafety
    ```

1. Copy the following code into *quickstart.py*:

    ```python
    import os
    from azure.ai.contentsafety import BlocklistClient
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import HttpResponseError
    from azure.ai.contentsafety.models import (
        TextBlocklist, AddOrUpdateTextBlocklistItemsOptions, TextBlocklistItem, AnalyzeTextOptions
    )
    from azure.core.exceptions import HttpResponseError
    
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
      
    # Create a Blocklist client
    client = BlocklistClient(endpoint, AzureKeyCredential(key))
    
    blocklist_name = "<your-blocklist-name>"
    blocklist_description = "<description>"
    
    try:
        blocklist = client.create_or_update_text_blocklist(
            blocklist_name=blocklist_name,
            options=TextBlocklist(blocklist_name=blocklist_name, description=blocklist_description),
        )
        if blocklist:
            print("\nBlocklist created or updated: ")
            print(f"Name: {blocklist.blocklist_name}, Description: {blocklist.description}")
    except HttpResponseError as e:
        print("\nCreate or update text blocklist failed: ")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    
    
    # add items
    blocklist_item_text_1 = "<block_item_text_1>"
    blocklist_item_text_2 = "<block_item_text_2>"
    
    blocklist_items = [TextBlocklistItem(text=blocklist_item_text_1), TextBlocklistItem(text=blocklist_item_text_2)]
    try:
        result = client.add_or_update_blocklist_items(
            blocklist_name=blocklist_name, options=AddOrUpdateTextBlocklistItemsOptions(blocklist_items=blocklist_items))
        for blocklist_item in result.blocklist_items:
            print(
                f"BlocklistItemId: {blocklist_item.blocklist_item_id}, Text: {blocklist_item.text}, Description: {blocklist_item.description}"
            )
    except HttpResponseError as e:
        print("\nAdd blocklistItems failed: ")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    
    # analyze
    
    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    input_text = "<sample input text>"
    
    try:
        # After you edit your blocklist, it usually takes effect in 5 minutes, please wait some time before analyzing
        # with blocklist after editing.
        analysis_result = client.analyze_text(
            AnalyzeTextOptions(text=input_text, blocklist_names=[blocklist_name], halt_on_blocklist_hit=False)
        )
        if analysis_result and analysis_result.blocklists_match:
            print("\nBlocklist match results: ")
            for match_result in analysis_result.blocklists_match:
                print(
                    f"BlocklistName: {match_result.blocklist_name}, BlocklistItemId: {match_result.blocklist_item_id}, "
                    f"BlocklistItemText: {match_result.blocklist_item_text}"
                )
    except HttpResponseError as e:
        print("\nAnalyze text failed: ")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    ```

1. Replace the following placeholders with your own values:
   * `<your-blocklist-name>`: A unique name for your blocklist.
   * `<description>`: A description of your blocklist.
   * `<block_item_text_1>`: The first item to add to your blocklist.
   * `<block_item_text_2>`: The second item to add to your blocklist.
   * `<sample input text>`: The text you want to analyze against the blocklist.
1. Then run the application with the `python` command on your quickstart file.

    ```console
    python quickstart.py
    ```