---
title: Create an Immersive Reader resource
titleSuffix: Azure AI services
description: Learn how to create a new Immersive Reader resource with a custom subdomain and then configure Microsoft Entra ID in your Azure tenant.
author: rwallerms
manager: nitinme
ms.service: azure-ai-immersive-reader
ms.topic: how-to
ms.date: 02/12/2024
ms.author: rwaller
ms.custom:
  - devx-track-azurecli
  - sfi-image-nochange
---

# Create an Immersive Reader resource and configure Microsoft Entra authentication

This article explains how to create an Immersive Reader resource by using the provided script. This script also configures Microsoft Entra authentication. Each time an Immersive Reader resource is created, whether with this script or in the portal, it must be configured with Microsoft Entra permissions.

The script creates and configures all the necessary Immersive Reader and Microsoft Entra resources for you. However, you can also configure Microsoft Entra authentication for an existing Immersive Reader resource, if you already created one in the Azure portal. The script first looks for existing Immersive Reader and Microsoft Entra resources in your subscription, and creates them only if they don't already exist.

For some customers, it might be necessary to create multiple Immersive Reader resources, for development versus production, or perhaps for different regions where your service is deployed. For those cases, you can come back and use the script multiple times to create different Immersive Reader resources and get them configured with Microsoft Entra permissions.

## Permissions

The listed **Owner** of your Azure subscription has all the required permissions to create an Immersive Reader resource and configure Microsoft Entra authentication.

If you aren't an owner, the following scope-specific permissions are required:

* **Contributor**. You need to have at least a Contributor role associated with the Azure subscription:

    :::image type="content" source="media/contributor-role.png" alt-text="Screenshot of contributor built-in role description.":::

* **Application Developer**. You need to have at least an Application Developer role associated in Microsoft Entra ID:

    :::image type="content" source="media/application-developer-role.png" alt-text="Screenshot of the developer built-in role description.":::

For more information, see [Microsoft Entra built-in roles](/azure/active-directory/roles/permissions-reference#application-developer).

## Set up PowerShell resources

1. Start by opening the [Azure Cloud Shell](/azure/cloud-shell/overview). Ensure that Cloud Shell is set to **PowerShell** in the upper-left hand dropdown or by typing `pwsh`.

1. Copy and paste the following code snippet into the shell.

    ```azurepowershell-interactive
    function Create-ImmersiveReaderResource(
        [Parameter(Mandatory=$true, Position=0)] [String] $SubscriptionName,
        [Parameter(Mandatory=$true)] [String] $ResourceName,
        [Parameter(Mandatory=$true)] [String] $ResourceSubdomain,
        [Parameter(Mandatory=$true)] [String] $ResourceSKU,
        [Parameter(Mandatory=$true)] [String] $ResourceLocation,
        [Parameter(Mandatory=$true)] [String] $ResourceGroupName,
        [Parameter(Mandatory=$true)] [String] $ResourceGroupLocation,
        [Parameter(Mandatory=$true)] [String] $AADAppDisplayName,
        [Parameter(Mandatory=$true)] [String] $AADAppIdentifierUri,
        [Parameter(Mandatory=$true)] [String] $AADAppClientSecretExpiration
    )
    {
        $unused = ''
        if (-not [System.Uri]::TryCreate($AADAppIdentifierUri, [System.UriKind]::Absolute, [ref] $unused)) {
            throw "Error: AADAppIdentifierUri must be a valid URI"
        }

        Write-Host "Setting the active subscription to '$SubscriptionName'"
        $subscriptionExists = Get-AzSubscription -SubscriptionName $SubscriptionName
        if (-not $subscriptionExists) {
            throw "Error: Subscription does not exist"
        }
        az account set --subscription $SubscriptionName

        $resourceGroupExists = az group exists --name $ResourceGroupName
        if ($resourceGroupExists -eq "false") {
            Write-Host "Resource group does not exist. Creating resource group"
            $groupResult = az group create --name $ResourceGroupName --location $ResourceGroupLocation
            if (-not $groupResult) {
                throw "Error: Failed to create resource group"
            }
            Write-Host "Resource group created successfully"
        }

        # Create an Immersive Reader resource if it doesn't already exist
        $resourceId = az cognitiveservices account show --resource-group $ResourceGroupName --name $ResourceName --query "id" -o tsv
        if (-not $resourceId) {
            Write-Host "Creating the new Immersive Reader resource '$ResourceName' (SKU '$ResourceSKU') in '$ResourceLocation' with subdomain '$ResourceSubdomain'"
            $resourceId = az cognitiveservices account create `
                            --name $ResourceName `
                            --resource-group $ResourceGroupName `
                            --kind ImmersiveReader `
                            --sku $ResourceSKU `
                            --location $ResourceLocation `
                            --custom-domain $ResourceSubdomain `
                            --query "id" `
                            -o tsv

            if (-not $resourceId) {
                throw "Error: Failed to create Immersive Reader resource"
            }
            Write-Host "Immersive Reader resource created successfully"
        }

        # Create a Microsoft Entra app if it doesn't already exist
        $clientId = az ad app show --id $AADAppIdentifierUri --query "appId" -o tsv
        if (-not $clientId) {
            Write-Host "Creating new Microsoft Entra app"
            $clientId = az ad app create --display-name $AADAppDisplayName --identifier-uris $AADAppIdentifierUri --query "appId" -o tsv
            if (-not $clientId) {
                throw "Error: Failed to create Microsoft Entra application"
            }
            Write-Host "Microsoft Entra application created successfully."

            $clientSecret = az ad app credential reset --id $clientId --end-date "$AADAppClientSecretExpiration" --query "password" | % { $_.Trim('"') }
            if (-not $clientSecret) {
                throw "Error: Failed to create Microsoft Entra application client secret"
            }
            Write-Host "Microsoft Entra application client secret created successfully."

            Write-Host "NOTE: To manage your Microsoft Entra application client secrets after this Immersive Reader Resource has been created please visit https://portal.azure.com and go to Home -> Microsoft Entra ID -> App Registrations -> (your app) '$AADAppDisplayName' -> Certificates and Secrets blade -> Client Secrets section" -ForegroundColor Yellow
        }

        # Create a service principal if it doesn't already exist
        $principalId = az ad sp show --id $AADAppIdentifierUri --query "id" -o tsv
        if (-not $principalId) {
            Write-Host "Creating new service principal"
            az ad sp create --id $clientId | Out-Null
            $principalId = az ad sp show --id $AADAppIdentifierUri --query "id" -o tsv

            if (-not $principalId) {
                throw "Error: Failed to create new service principal"
            }
            Write-Host "New service principal created successfully"

            # Sleep for 5 seconds to allow the new service principal to propagate
            Write-Host "Sleeping for 5 seconds"
            Start-Sleep -Seconds 5
        }

        Write-Host "Granting service principal access to the newly created Immersive Reader resource"
        $accessResult = az role assignment create --assignee $principalId --scope $resourceId --role "Cognitive Services Immersive Reader User"
        if (-not $accessResult) {
            throw "Error: Failed to grant service principal access"
        }
        Write-Host "Service principal access granted successfully"

        # Grab the tenant ID, which is needed when obtaining a Microsoft Entra token
        $tenantId = az account show --query "tenantId" -o tsv

        # Collect the information needed to obtain a Microsoft Entra token into one object
        $result = @{}
        $result.TenantId = $tenantId
        $result.ClientId = $clientId
        $result.ClientSecret = $clientSecret
        $result.Subdomain = $ResourceSubdomain

        Write-Host "`nSuccess! " -ForegroundColor Green -NoNewline
        Write-Host "Save the following JSON object to a text file for future reference."
        Write-Host "*****"
        if($clientSecret -ne $null) {

            Write-Host "This function has created a client secret (password) for you. This secret is used when calling Microsoft Entra to fetch access tokens."
            Write-Host "This is the only time you will ever see the client secret for your Microsoft Entra application, so save it now." -ForegroundColor Yellow
        }
        else{
            Write-Host "You will need to retrieve the ClientSecret from your original run of this function that created it. If you don't have it, you will need to go create a new client secret for your Microsoft Entra application. Please visit https://portal.azure.com and go to Home -> Microsoft Entra ID -> App Registrations -> (your app) '$AADAppDisplayName' -> Certificates and Secrets blade -> Client Secrets section." -ForegroundColor Yellow
        }
        Write-Host "*****`n"
        Write-Output (ConvertTo-Json $result)
    }
    ```

1. Run the function `Create-ImmersiveReaderResource`, supplying the '<PARAMETER_VALUES>' placeholders with your own values as appropriate.

    ```azurepowershell-interactive
    Create-ImmersiveReaderResource -SubscriptionName '<SUBSCRIPTION_NAME>' -ResourceName '<RESOURCE_NAME>' -ResourceSubdomain '<RESOURCE_SUBDOMAIN>' -ResourceSKU '<RESOURCE_SKU>' -ResourceLocation '<RESOURCE_LOCATION>' -ResourceGroupName '<RESOURCE_GROUP_NAME>' -ResourceGroupLocation '<RESOURCE_GROUP_LOCATION>' -AADAppDisplayName '<MICROSOFT_ENTRA_DISPLAY_NAME>' -AADAppIdentifierUri '<MICROSOFT_ENTRA_IDENTIFIER_URI>' -AADAppClientSecretExpiration '<MICROSOFT_ENTRA_CLIENT_SECRET_EXPIRATION>'
    ```

    The full command looks something like the following. Here we put each parameter on its own line for clarity, so you can see the whole command. __Do not copy or use this command as-is.__ Copy and use the command with your own values. This example has dummy values for the `<PARAMETER_VALUES>`. Yours might be different, as you come up with your own names for these values.

    ```
    Create-ImmersiveReaderResource
        -SubscriptionName 'MyOrganizationSubscriptionName'
        -ResourceName 'MyOrganizationImmersiveReader'
        -ResourceSubdomain 'MyOrganizationImmersiveReader'
        -ResourceSKU 'S0'
        -ResourceLocation 'westus2'
        -ResourceGroupName 'MyResourceGroupName'
        -ResourceGroupLocation 'westus2'
        -AADAppDisplayName 'MyOrganizationImmersiveReaderAADApp'
        -AADAppIdentifierUri 'api://MyOrganizationImmersiveReaderAADApp'
        -AADAppClientSecretExpiration '2021-12-31'
    ```

    | Parameter | Comments |
    | --- | --- |
    | SubscriptionName |Name of the Azure subscription to use for your Immersive Reader resource. You must have a subscription in order to create a resource. |
    | ResourceName |  Must be alphanumeric, and can contain `-`, as long as the `-` isn't the first or last character. Length can't exceed 63 characters.|
    | ResourceSubdomain |A custom subdomain is needed for your Immersive Reader resource. The subdomain is used by the SDK when calling the Immersive Reader service to launch the Reader. The subdomain must be globally unique. The subdomain must be alphanumeric, and can contain `-`, as long as the `-` isn't the first or last character. Length can't exceed 63 characters. This parameter is optional if the resource already exists. |
    | ResourceSKU |Options: `S0` (Standard tier) or `S1` (Education/Nonprofit organizations). To learn more about each available SKU, visit our [Azure AI services pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/immersive-reader/). This parameter is optional if the resource already exists. |
    | ResourceLocation |Options: `australiaeast`, `brazilsouth`, `canadacentral`, `centralindia`, `centralus`, `eastasia`, `eastus`, `eastus2`, `francecentral`, `germanywestcentral`, `japaneast`, `japanwest`, `jioindiawest`, `koreacentral`, `northcentralus`, `northeurope`, `norwayeast`, `southafricanorth`, `southcentralus`, `southeastasia`, `swedencentral`, `switzerlandnorth`, `switzerlandwest`, `uaenorth`, `uksouth`, `westcentralus`, `westeurope`, `westus`, `westus2`, `westus3`. This parameter is optional if the resource already exists. |
    | ResourceGroupName |Resources are created in resource groups within subscriptions. Supply the name of an existing resource group. If the resource group doesn't already exist, a new one with this name is created. |
    | ResourceGroupLocation |If your resource group doesn't exist, you need to supply a location in which to create the group. To find a list of locations, run `az account list-locations`. Use the *name* property (without spaces) of the returned result. This parameter is optional if your resource group already exists. |
    | AADAppDisplayName |The Microsoft Entra application display name. If an existing Microsoft Entra application isn't found, a new one with this name is created. This parameter is optional if the Microsoft Entra application already exists. |
    | AADAppIdentifierUri |The URI for the Microsoft Entra application. If an existing Microsoft Entra application isn't found, a new one with this URI is created. For example, `api://MyOrganizationImmersiveReaderAADApp`. Here we're using the default Microsoft Entra URI scheme prefix of `api://` for compatibility with the [Microsoft Entra policy of using verified domains](/azure/active-directory/develop/reference-breaking-changes#appid-uri-in-single-tenant-applications-will-require-use-of-default-scheme-or-verified-domains). |
    | AADAppClientSecretExpiration |The date or datetime after which your Microsoft Entra Application Client Secret (password) expires (for example, '2020-12-31T11:59:59+00:00' or '2020-12-31'). This function creates a client secret for you. |

    To manage your Microsoft Entra application client secrets after you create this resource, visit the [Azure portal](https://portal.azure.com) and go to **Home** -> **Microsoft Entra ID** -> **App Registrations** -> (your app) `[AADAppDisplayName]` -> **Certificates and Secrets** section -> **Client Secrets** section.

    :::image type="content" source="media/client-secrets-blade.png" alt-text="Screenshot of the Azure portal Certificates and Secrets pane." lightbox="media/client-secrets-blade.png":::

1. Copy the JSON output into a text file for later use. The output should look like the following.

    ```json
    {
      "TenantId": "...",
      "ClientId": "...",
      "ClientSecret": "...",
      "Subdomain": "..."
    }
    ```

## Next step

> [!div class="nextstepaction"]
> [How to launch the Immersive Reader](how-to-launch-immersive-reader.md)
