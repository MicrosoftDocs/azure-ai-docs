---
title: "Quickstart: Generate images with Azure OpenAI in Microsoft Foundry Models using PowerShell"
titleSuffix: Azure OpenAI
description: Learn how to generate images with Azure OpenAI by using PowerShell and the endpoint and access keys for your Azure OpenAI resource.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 01/29/2026
ai-usage: ai-assisted
---

Use this guide to get started calling the Azure OpenAI in Microsoft Foundry Models image generation APIs with PowerShell.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- For this task, <a href="https://aka.ms/installpowershell" target="_blank">the latest version of PowerShell 7</a> is recommended because the examples use new features not available in Windows PowerShell 5.1.
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.



## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Generate images

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```powershell
    az login
    ```

1. Get an Azure OpenAI auth token and set it as an environment variable for the current PowerShell session:

    ```powershell
    $Env:DEFAULT_AZURE_CREDENTIAL_TOKEN = az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv
    ```

1. Create a new PowerShell file called *quickstart.ps1*. Then open it up in your preferred editor or IDE.

1. Replace the contents of _quickstart.ps1_ with the following code. Make sure `AZURE_OPENAI_ENDPOINT` is set, and change the value of `prompt` to your preferred text.

    To use API key authentication instead of keyless authentication, set `AZURE_OPENAI_API_KEY` and uncomment the `'api-key'` line.

   ```powershell
    # Azure OpenAI metadata variables
    $openai = @{
        api_base    = $Env:AZURE_OPENAI_ENDPOINT 
        api_version = '2023-06-01-preview' # This can change in the future.
    }
    
    # Use the recommended keyless authentication via bearer token.
    $headers = [ordered]@{
        #'api-key' = $Env:AZURE_OPENAI_API_KEY
        'Authorization' = "Bearer $($Env:DEFAULT_AZURE_CREDENTIAL_TOKEN)"
    }
    
    # Text to describe image
    $prompt = 'A painting of a dog'
    
    # Adjust these values to fine-tune completions
    $body = [ordered]@{
        prompt = $prompt
        size   = '1024x1024'
        n      = 1
    } | ConvertTo-Json
    
    # Call the API to generate the image and retrieve the response
    $url = "$($openai.api_base)/openai/images/generations:submit?api-version=$($openai.api_version)"
    
    $submission = Invoke-RestMethod -Uri $url -Headers $headers -Body $body -Method Post -ContentType 'application/json' -ResponseHeadersVariable submissionHeaders
    
    $operation_location = $submissionHeaders['operation-location'][0]
    $status = ''
    while ($status -ne 'succeeded') {
        Start-Sleep -Seconds 1
        $response = Invoke-RestMethod -Uri $operation_location -Headers $headers
        $status   = $response.status
    }
    
    # Set the directory for the stored image
    $image_dir = Join-Path -Path $pwd -ChildPath 'images'
    
    # If the directory doesn't exist, create it
    if (-not(Resolve-Path $image_dir -ErrorAction Ignore)) {
        New-Item -Path $image_dir -ItemType Directory
    }
    
    # Initialize the image path (note the filetype should be png)
    $image_path = Join-Path -Path $image_dir -ChildPath 'generated_image.png'
    
    # Retrieve the generated image
    $image_url = $response.result.data[0].url  # extract image URL from response
    $generated_image = Invoke-WebRequest -Uri $image_url -OutFile $image_path  # download the image
    return $image_path
   ```

   > [!IMPORTANT]
   > For production, use a secure way of storing and accessing your credentials like [The PowerShell Secret Management with Azure Key Vault](/powershell/utility-modules/secretmanagement/how-to/using-azure-keyvault). For more information about credential security, see this [security](../../../ai-services/security-features.md) article.

1. Run the script using PowerShell:

   ```powershell
   ./quickstart.ps1
   ```

   The script loops until the generated image is ready.

## Output

PowerShell requests the image from Azure OpenAI and stores the output image in the _generated_image.png_ file in your specified directory. For convenience, the full path for the file is returned at the end of the script.

The Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filtering](../concepts/content-filter.md).

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure PowerShell](../../../ai-services/multi-service-resource.md?pivots=azpowershell#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
- Try examples in the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
