---
title: "How-to: Copy custom analyzers using the Content Understanding Python SDK"
author: PatrickFarley
manager: nitinme
description: Learn to copy custom analyzers with Content Understanding using the Python SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 04/14/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->


This guide shows you how to use the Content Understanding Python SDK to copy custom analyzers within a resource and across Foundry resources.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key.
* [Python 3.9 or later](https://www.python.org/).
* An existing custom analyzer in your resource. See [Create a custom analyzer](../../tutorial/create-custom-analyzer.md) if you need to create one.

## Set up

1. Install the Content Understanding client library for Python with pip:

    ```console
    pip install azure-ai-contentunderstanding
    ```

1. Optionally, install the Azure Identity library for Microsoft Entra authentication:

    ```console
    pip install azure-identity
    ```

## Set up environment variables

To authenticate with the Content Understanding service, set the environment variables with your own values before running the sample:
- `CONTENTUNDERSTANDING_ENDPOINT` - the endpoint to your Content Understanding resource.
- `CONTENTUNDERSTANDING_KEY` - your Content Understanding API key (optional if using [Microsoft Entra ID](../../concepts/secure-communications.md) DefaultAzureCredential).

### Windows

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

### Linux / macOS

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create the client

```python
import os
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential

endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
key = os.getenv("CONTENTUNDERSTANDING_KEY")
credential = AzureKeyCredential(key) if key else DefaultAzureCredential()

client = ContentUnderstandingClient(
    endpoint=endpoint, credential=credential
)
```

## Copy within a Foundry resource

To copy an analyzer within the same resource, call the `begin_copy_analyzer` method with the target and source analyzer IDs.

```python
source_analyzer_id = "my-source-analyzer"
target_analyzer_id = "my-target-analyzer"

poller = client.begin_copy_analyzer(
    analyzer_id=target_analyzer_id,
    source_analyzer_id=source_analyzer_id,
)
poller.result()

print("Analyzer copied successfully!")
```

> [!TIP]
> This code is based on the [copy analyzer sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_copy_analyzer.py) in the SDK repository.

## Copy across Foundry resources

Copying an analyzer across Foundry resources is a multi-step process:

1. Grant copy authorization on the source resource.
1. Use the authorization to call the copy API on the target resource.

> [!IMPORTANT]
> Both the source and target resources require the **Cognitive Services User** role to be granted to the credential used to run the code. This role is required for cross-resource copying operations.

For cross-resource copying, set the following additional environment variables:
- `CONTENTUNDERSTANDING_SOURCE_RESOURCE_ID` - Full Azure Resource Manager resource ID of the source resource.
- `CONTENTUNDERSTANDING_SOURCE_REGION` - Azure region of the source resource.
- `CONTENTUNDERSTANDING_TARGET_ENDPOINT` - Target resource endpoint.
- `CONTENTUNDERSTANDING_TARGET_RESOURCE_ID` - Full Azure Resource Manager resource ID of the target resource.
- `CONTENTUNDERSTANDING_TARGET_REGION` - Azure region of the target resource.
- `CONTENTUNDERSTANDING_TARGET_KEY` - Target API key (optional if using DefaultAzureCredential).

Example resource ID format:
`/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{name}`

```python
source_endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
source_key = os.getenv("CONTENTUNDERSTANDING_KEY")
source_credential = (
    AzureKeyCredential(source_key) if source_key else DefaultAzureCredential()
)

source_resource_id = os.environ["CONTENTUNDERSTANDING_SOURCE_RESOURCE_ID"]
source_region = os.environ["CONTENTUNDERSTANDING_SOURCE_REGION"]

target_endpoint = os.environ["CONTENTUNDERSTANDING_TARGET_ENDPOINT"]
target_key = os.getenv("CONTENTUNDERSTANDING_TARGET_KEY")
target_credential = (
    AzureKeyCredential(target_key) if target_key else DefaultAzureCredential()
)

target_resource_id = os.environ["CONTENTUNDERSTANDING_TARGET_RESOURCE_ID"]
target_region = os.environ["CONTENTUNDERSTANDING_TARGET_REGION"]

source_analyzer_id = "my-source-analyzer"
target_analyzer_id = "my-target-analyzer"

# Create source and target clients
source_client = ContentUnderstandingClient(
    endpoint=source_endpoint, credential=source_credential
)
target_client = ContentUnderstandingClient(
    endpoint=target_endpoint, credential=target_credential
)

# Step 1: Grant copy authorization on the source resource
copy_auth = source_client.grant_copy_authorization(
    analyzer_id=source_analyzer_id,
    target_azure_resource_id=target_resource_id,
    target_region=target_region,
)

print("Authorization granted successfully!")
print(f"  Target Azure Resource ID: {copy_auth.target_azure_resource_id}")
print(f"  Expires at: {copy_auth.expires_at}")

# Step 2: Copy analyzer to target resource
copy_poller = target_client.begin_copy_analyzer(
    analyzer_id=target_analyzer_id,
    source_analyzer_id=source_analyzer_id,
    source_azure_resource_id=source_resource_id,
    source_region=source_region,
)
copy_poller.result()

print("Analyzer copied successfully to target resource!")
```

> [!TIP]
> This code is based on the [grant copy auth sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_grant_copy_auth.py) in the SDK repository.

> [!NOTE]
>
> Analyzers now support classification/segmentation and analysis of each of the identified classes and segments in a single request. When copying an analyzer that uses this feature, you need to copy any referenced analyzers as well.

## Verify the copy

Validate that the analyzer was copied by retrieving it from the target resource.

```python
copied_analyzer = target_client.get_analyzer(
    analyzer_id=target_analyzer_id
)
print(f"  Target Analyzer ID: {copied_analyzer.analyzer_id}")
print(f"  Description: {copied_analyzer.description}")
print(f"  Status: {copied_analyzer.status}")
```
