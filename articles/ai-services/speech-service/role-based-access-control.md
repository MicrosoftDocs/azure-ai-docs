---
title: Role-based access control for Speech resources
titleSuffix: Foundry Tools
description: Learn how to assign access roles for an AI Speech resource.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 12/19/2025
ms.author: pafarley
# Customer intent: As a developer, I want to learn how to assign access roles for an AI Speech resource.
---

# Role-based access control for Speech resources

You can manage access and permissions to your Speech resources with Azure role-based access control (Azure RBAC). Assigned roles can vary across Speech resources. 

For example, you can assign a role to an AI Speech resource that should only be used to train a custom speech model. You can assign another role to an AI Speech resource that is used to transcribe audio files. 

Depending on who can access each Speech resource, you can effectively set a different level of access per application or user. For more information on Azure RBAC, see the [Azure RBAC documentation](/azure/role-based-access-control/overview).

> [!NOTE]
> This article describes how to assign access roles for an AI Speech resource. For information on how to assign access roles for Microsoft Foundry resources, see the [Microsoft Foundry documentation](../../ai-foundry/concepts/rbac-foundry.md).

## Roles for Speech resources

A role definition is a collection of permissions. An AI Speech resource can inherit or be assigned multiple roles. The final level of access to the resource is a combination of all role permissions. When you create an AI Speech resource, the built-in roles in the following table are available for assignment. 

| Role | Can list resource keys | Access to data, models, and endpoints in custom projects| Access to speech transcription and synthesis APIs
| ---| ---| ---| ---|
|**Owner** |Yes |None |No |
|**Contributor** |Yes |None |No |
|**Cognitive Services Contributor** |Yes |None |No |
|**Cognitive Services User** |Yes |View, create, edit, and delete |Yes |
|**Cognitive Services Speech Contributor** |No | View, create, edit, and delete |Yes |
|**Cognitive Services Speech User** |No |View only |Yes |
|**Cognitive Services Data Reader (Preview)** |No |View only |Yes |

Keep the built-in roles if your Speech resource can have full read and write access to the projects. 

For finer-grained resource access control, you can [add or remove roles](/azure/role-based-access-control/role-assignments-portal?tabs=current) using the Azure portal. For example, you could create a custom role with permission to upload custom speech datasets, but without permission to deploy a custom speech model to an endpoint. 

### Special considerations for Speech resources

> [!IMPORTANT]
> Speech service architecture differs from other Foundry Tools in the way it uses [Azure control plane and data plane](/azure/azure-resource-manager/management/control-plane-and-data-plane). 

Speech service is extensively using data plane comparing to other Foundry Tools, and this requires different setup for the roles. Because of this some general *"Cognitive Services"* roles have actual access right set that doesn't exactly match their name when used in Speech services scenario. 

For instance *Cognitive Services User* provides in effect the Contributor rights, while *Cognitive Services Contributor* provides no access at all. The same is true for generic *Owner* and *Contributor* roles, which have no data plane rights and therefore provide no access to Speech resource. 

To keep consistency, we recommend using roles containing *Speech* in their names. These roles are *Cognitive Services Speech User* and *Cognitive Services Speech Contributor*. Their access right sets were designed specifically for the Speech service. 

## Authentication with keys and tokens

The [roles](#roles-for-speech-resources) define what permissions you have. Authentication is required to use the Speech resource. 

To authenticate with Speech resource keys, all you need is the key and region. To authenticate with a Microsoft Entra token, the Speech resource must have a [custom subdomain](speech-services-private-link.md#create-a-custom-domain-name).

Here's how to create a new Speech resource with a custom subdomain. You can also use an existing resource, but it must have a custom subdomain. For more information about creating a custom subdomain, see [Create a custom domain name](speech-services-private-link.md#create-a-custom-domain-name).

```bash
resourceGroupName=my-speech-rg
location=eastus
AIServicesResourceName=my-aiservices-$location

# create an AIServices resource for Speech and other Foundry Tools
az cognitiveservices account create --name $AIServicesResourceName --resource-group $resourceGroupName --kind AIServices --sku S0 --location $location --custom-domain $AIServicesResourceName

# get the resource id
speechResourceId=$(az cognitiveservices account show --name $AIServicesResourceName --resource-group $resourceGroupName --query id -o tsv)
# assign Cognitive Services User role to the app id
appId=$(az ad signed-in-user show --query id -o tsv)
az role assignment create --role "Cognitive Services User" --assignee $appId --scope $speechResourceId
# assign Cognitive Services Speech User role to the app id
az role assignment create --role "Cognitive Services Speech User" --assignee $appId --scope $speechResourceId

# get an access token
accessToken=$(az account get-access-token --scope "https://cognitiveservices.azure.com/.default" --query accessToken -o tsv)
echo $accessToken
```

The returned `accessToken` is a Microsoft Entra token that you can use to authenticate without API keys. The token has a [limited lifetime](/entra/identity-platform/configurable-token-lifetimes#access-tokens).

Now you can use the `accessToken` to authenticate with the Foundry resource. For example, you can use the token via the [Fast transcription REST API](./fast-transcription-create.md):

```bash
uri="https://$AIServicesResourceName.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15"

curl -v "$uri" \
    --header 'Content-Type: multipart/form-data' \
    --form 'definition={"locales": ["en-US"]}' \
    --form 'audio=@Call1_separated_16k_health_insurance.wav' \
    --header "Authorization: Bearer $accessToken" 
```

### Speech SDK authentication

For the SDK, you configure whether to authenticate with an API key or Microsoft Entra token. For details, see [Microsoft Entra authentication with the Speech SDK](how-to-configure-azure-ad-auth.md).                    |

## Related content

* [Microsoft Entra authentication with the Speech SDK](how-to-configure-azure-ad-auth.md).
* [Speech service encryption of data at rest](speech-encryption-of-data-at-rest.md).
