---
title: How to configure Microsoft Entra authentication
titleSuffix: Foundry Tools
description: Learn how to authenticate using Microsoft Entra authentication
author: goergenj
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 11/13/2025
ms.author: jagoerge
zone_pivot_groups: programming-languages-set-two
ms.custom: devx-track-azurepowershell, devx-track-extended-java, devx-track-python, devx-track-azurecli
---

# Microsoft Entra authentication with the Speech SDK

When using the Speech SDK to access the Speech service, there are three authentication methods available: service keys, a key-based token, and Microsoft Entra ID. This article describes how to configure a Foundry resource and create a Speech SDK configuration object to use Microsoft Entra ID for authentication.

This article shows how to use Microsoft Entra authentication with the Speech SDK. You learn how to:

> [!div class="checklist"]
>
> - Create a Foundry resource
> - Configure the Speech resource for Microsoft Entra authentication
> - Get a Microsoft Entra access token
> - Create the appropriate SDK configuration object.

To learn more about Microsoft Entra access tokens, including token lifetime, visit [Access tokens in the Microsoft identity platform](/azure/active-directory/develop/access-tokens).

## Create a Foundry resource
To create a Foundry resource in the [Azure portal](https://portal.azure.com), see [this quickstart](~/articles/ai-services/multi-service-resource.md?pivots=azportal).

<a name='configure-the-speech-resource-for-azure-ad-authentication'></a>

## Configure the Speech resource for Microsoft Entra authentication

To configure your Speech resource for Microsoft Entra authentication, create a custom domain name and assign roles.

### Create a custom domain name
[!INCLUDE [Custom Domain include](includes/how-to/custom-domain.md)]

### Assign roles
For Microsoft Entra authentication with Speech resources, you need to assign either the *Cognitive Services Speech Contributor* or *Cognitive Services Speech User* role.

You can assign roles to the user or application using the [Azure portal](/azure/role-based-access-control/role-assignments-portal) or [PowerShell](/azure/role-based-access-control/role-assignments-powershell).

<a name='get-an-azure-ad-access-token'></a>

## Get a Microsoft Entra access token
::: zone pivot="programming-language-csharp"
To get a Microsoft Entra access token in C#, use the [Azure Identity Client Library](/dotnet/api/overview/azure/identity-readme).

Here's an example of using Azure Identity to get a Microsoft Entra access token from an interactive browser:
```c#
TokenRequestContext context = new Azure.Core.TokenRequestContext(new string[] { "https://cognitiveservices.azure.com/.default" });
InteractiveBrowserCredential browserCredential = new InteractiveBrowserCredential();
var browserToken = browserCredential.GetToken(context);
string aadToken = browserToken.Token;
```
> [!NOTE]
> The token context must be set to "https://cognitiveservices.azure.com/.default".

::: zone-end

::: zone pivot="programming-language-cpp"
To get a Microsoft Entra access token in C++, use the [Azure Identity Client Library](https://github.com/Azure/azure-sdk-for-cpp/tree/main/sdk/identity/azure-identity).

Here's an example of using Azure Identity to get a Microsoft Entra access token with your tenant ID, client ID, and client secret credentials:
```cpp
const std::string tokenContext = "https://cognitiveservices.azure.com/.default";

Azure::Identity::DefaultAzureCredential();

Azure::Core::Credentials::TokenRequestContext context;
context.Scopes.push_back(tokenContext);

auto token = cred.GetToken(context, Azure::Core::Context());
```

> [!NOTE]
> The token context must be set to "https://cognitiveservices.azure.com/.default".

::: zone-end

::: zone pivot="programming-language-java"
To get a Microsoft Entra access token in Java, use the [Azure Identity Client Library](/java/api/overview/azure/identity-readme).

Here's an example of using Azure Identity to get a Microsoft Entra access token from a browser:
```java
TokenRequestContext context = new TokenRequestContext();
context.addScopes("https://cognitiveservices.azure.com/.default");

InteractiveBrowserCredentialBuilder builder = new InteractiveBrowserCredentialBuilder();
InteractiveBrowserCredential browserCredential = builder.build();

AccessToken browserToken = browserCredential.getToken(context).block();
String token = browserToken.getToken();
```

> [!NOTE]
> The token context must be set to "https://cognitiveservices.azure.com/.default".

::: zone-end

::: zone pivot="programming-language-python"
To get a Microsoft Entra access token in Python, use the [Azure Identity Client Library](/python/api/overview/azure/identity-readme).

Here's an example of using Azure Identity to get a Microsoft Entra access token from an interactive browser:
```Python
from azure.identity import  InteractiveBrowserCredential
ibc = InteractiveBrowserCredential()
aadToken = ibc.get_token("https://cognitiveservices.azure.com/.default")
```
::: zone-end

### More samples

Find samples that get a Microsoft Entra access token in [Microsoft identity platform code samples](/azure/active-directory/develop/sample-v2-code).

For programming languages where a Microsoft identity platform client library isn't available, you can directly [request an access token](/azure/active-directory/develop/v2-oauth-ropc).

## Get the Speech resource ID

You need your Speech resource ID to make SDK calls using Microsoft Entra authentication in scenarios that don't yet support Entra ID directly.

# [Azure portal](#tab/portal)

To get the resource ID in the Azure portal:

1. Go to the [Azure portal](https://portal.azure.com/) and sign in to your Azure account.
1. Select a Foundry resource.
1. In the **Resource Management** group on the left pane, select **Properties**.
1. Copy the **Resource ID**

# [PowerShell](#tab/powershell)

To get the resource ID using PowerShell, confirm that you have PowerShell version 7.x or later with the Azure PowerShell module version 5.1.0 or later. To see the versions of these tools, follow these steps:

1. In a PowerShell window, enter:

    `$PSVersionTable`

    Confirm that the `PSVersion` value is 7.x or later. To upgrade PowerShell, follow the instructions at [Installing various versions of PowerShell](/powershell/scripting/install/installing-powershell).

1. In a PowerShell window, enter:

    `Get-Module -ListAvailable Az`

    If nothing appears, or if that version of the Azure PowerShell module is earlier than 5.1.0, follow the instructions at [Install the Azure PowerShell module](/powershell/azure/install-azure-powershell) to upgrade.

Now run `Connect-AzAccount` to create a connection with Azure.

```azurepowershell
Connect-AzAccount
$subscriptionId = "Your Azure subscription Id"
$resourceGroup = "Resource group name where Speech resource is located"
$speechResourceName = "Your Speech resource name"

# Select the Azure subscription that contains the Speech resource.
# You can skip this step if your Azure account has only one active subscription.
Set-AzContext -SubscriptionId $subscriptionId

# Get the Speech resource 
$resource = Get-AzCognitiveServicesAccount -Name $speechResourceName -ResourceGroupName $resourceGroup

# Get the resource ID:
$resourceId = resource.Id
```

---

## Create the Speech SDK configuration object

With a Microsoft Entra access token, you can now create a Speech SDK configuration object.

The method of providing the token, and the method to construct the corresponding Speech SDK ```Config``` object varies by the object you're using.

::: zone pivot="programming-language-csharp"
### SpeechRecognizer, SourceLanguageRecognizer, ConversationTranscriber

For ```SpeechRecognizer```, ```SourceLanguageRecognizer```, ```ConversationTranscriber``` objects, use an appropriate instance of [TokenCredential](/dotnet/api/azure.core.tokencredential) for authentication, along with the endpoint that includes your [custom domain](/azure/ai-services/speech-service/speech-services-private-link?tabs=portal#create-a-custom-domain-name), to create a ```SpeechConfig``` object.

```C#
TokenCredential browserCredential = new InteractiveBrowserCredential();

// Define the custom domain endpoint for your Speech resource.
var endpoint = "https://{your custom name}.cognitiveservices.azure.com/";

// Create the SpeechConfig object using the custom domain endpoint and TokenCredential.
var speechConfig = SpeechConfig.FromEndpoint(new Uri(endpoint), browserCredential);
```

### TranslationRecognizer

For ```TranslationRecognizer``` object, use an appropriate instance of [TokenCredential](/dotnet/api/azure.core.tokencredential) for authentication, along with the endpoint that includes your [custom domain](/azure/ai-services/speech-service/speech-services-private-link?tabs=portal#create-a-custom-domain-name), to create a ```SpeechTranslationConfig``` object.

```C#
TokenCredential browserCredential = new InteractiveBrowserCredential();

// Define the custom domain endpoint for your Speech resource
var endpoint = "https://{your custom name}.cognitiveservices.azure.com/";

// Create the SpeechTranslationConfig object using the custom domain endpoint and TokenCredential.
var speechConfig = SpeechTranslationConfig.FromEndpoint(new Uri(endpoint), browserCredential);
```

### SpeechSynthesizer

For ```SpeechSynthesizer``` objects, build the authorization token from the resource ID and the Microsoft Entra access token and then use it to create a ```SpeechConfig``` object.

```C#
string resourceId = "Your Resource ID";
string aadToken = "Your Microsoft Entra access token";
string region =  "Your Speech Region";

// You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
var authorizationToken = $"aad#{resourceId}#{aadToken}";
var speechConfig = SpeechConfig.FromAuthorizationToken(authorizationToken, region);
```
::: zone-end

::: zone pivot="programming-language-cpp"
### SpeechRecognizer, SpeechSynthesizer, ConversationTranscriber

For ```SpeechRecognizer```, ```SpeechSynthesizer```, ```ConversationTranscriber``` objects, build the authorization token from the resource ID and the Microsoft Entra access token and then use it to create a ```SpeechConfig``` object.

```C++
std::string resourceId = "Your Resource ID";
std::string aadToken = "Your Microsoft Entra access token";
std::string region = "Your Speech Region";

// You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
auto authorizationToken = "aad#" + resourceId + "#" + aadToken;
auto speechConfig = SpeechConfig::FromAuthorizationToken(authorizationToken, region);
```

### TranslationRecognizer

For the ```TranslationRecognizer```, build the authorization token from the resource ID and the Microsoft Entra access token and then use it to create a ```SpeechTranslationConfig``` object.

```cpp
std::string resourceId = "Your Resource ID";
std::string aadToken = "Your Microsoft Entra access token";
std::string region = "Your Speech Region";

// You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
auto authorizationToken = "aad#" + resourceId + "#" + aadToken;
auto speechConfig = SpeechTranslationConfig::FromAuthorizationToken(authorizationToken, region);
```

::: zone-end

::: zone pivot="programming-language-java"
### SpeechRecognizer, ConversationTranscriber

For ```SpeechRecognizer```, ```ConversationTranscriber``` objects, use an appropriate instance of [TokenCredential](/dotnet/api/azure.core.tokencredential) for authentication, along with the endpoint that includes your [custom domain](/azure/ai-services/speech-service/speech-services-private-link?tabs=portal#create-a-custom-domain-name), to create a ```SpeechConfig``` object.

```Java
TokenCredential browserCredential = new InteractiveBrowserCredentialBuilder().build();

// Define the custom domain endpoint for your Speech resource.
String endpoint = "https://{your custom name}.cognitiveservices.azure.com/";

// Create the SpeechConfig object using the custom domain endpoint and TokenCredential.
SpeechConfig speechConfig = SpeechConfig.fromEndpoint(new java.net.URI(endpoint), browserCredential);
```

### TranslationRecognizer

For ```TranslationRecognizer``` object, use an appropriate instance of [TokenCredential](/dotnet/api/azure.core.tokencredential) for authentication, along with the endpoint that includes your [custom domain](/azure/ai-services/speech-service/speech-services-private-link?tabs=portal#create-a-custom-domain-name), to create a ```SpeechTranslationConfig``` object.

```Java
TokenCredential browserCredential = new InteractiveBrowserCredentialBuilder().build();

// Define the custom domain endpoint for your Speech resource
String endpoint = "https://{your custom name}.cognitiveservices.azure.com/";

// Create the SpeechTranslationConfig object using the custom domain endpoint and TokenCredential.
SpeechConfig speechConfig = SpeechTranslationConfig.fromEndpoint(new java.net.URI(endpoint), browserCredential);
```

### SpeechSynthesizer

For ```SpeechSynthesizer```, objects, build the authorization token from the resource ID and the Microsoft Entra access token and then use it to create a ```SpeechConfig``` object.

```Java
String resourceId = "Your Resource ID";
String region = "Your Region";

// You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
String authorizationToken = "aad#" + resourceId + "#" + token;
SpeechConfig speechConfig = SpeechConfig.fromAuthorizationToken(authorizationToken, region);
```
::: zone-end

::: zone pivot="programming-language-python"
### SpeechRecognizer, ConversationTranscriber

For ```SpeechRecognizer```, ```ConversationTranscriber``` objects, use an appropriate instance of [TokenCredential](/dotnet/api/azure.core.tokencredential) for authentication, along with the endpoint that includes your [custom domain](/azure/ai-services/speech-service/speech-services-private-link?tabs=portal#create-a-custom-domain-name), to create a ```SpeechConfig``` object.

```Python
browserCredential = InteractiveBrowserCredential()

// Define the custom domain endpoint for your Speech resource.
custom_endpoint = "https://{your custom name}.cognitiveservices.azure.com/"

// Create the SpeechConfig object using the custom domain endpoint and TokenCredential.
speechConfig = SpeechConfig(token_credential=credential, endpoint=custom_endpoint)
```

### TranslationRecognizer

For ```TranslationRecognizer``` object, use an appropriate instance of [TokenCredential](/dotnet/api/azure.core.tokencredential) for authentication, along with the endpoint that includes your [custom domain](/azure/ai-services/speech-service/speech-services-private-link?tabs=portal#create-a-custom-domain-name), to create a ```SpeechTranslationConfig``` object.

```Python
browserCredential = InteractiveBrowserCredential()

// Define the custom domain endpoint for your Speech resource
custom_endpoint = "https://{your custom name}.cognitiveservices.azure.com/"

// Create the SpeechTranslationConfig object using the custom domain endpoint and TokenCredential.
speechTranslationConfig = SpeechTranslationConfig(token_credential=credential, endpoint=custom_endpoint)
```

### SpeechSynthesizer

For ```SpeechSynthesizer``` object, build the authorization token from the resource ID and the Microsoft Entra access token and then use it to create a ```SpeechConfig``` object.

```Python
resourceId = "Your Resource ID"
region = "Your Region"
# You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
authorizationToken = "aad#" + resourceId + "#" + aadToken.token
speechConfig = SpeechConfig(auth_token=authorizationToken, region=region)
```
::: zone-end

### VoiceProfileClient
To use the ```VoiceProfileClient``` with Microsoft Entra authentication, use the custom domain name created above.

::: zone pivot="programming-language-csharp"
```C#
string customDomainName = "Your Custom Name";
string hostName = $"https://{customDomainName}.cognitiveservices.azure.com/";
string token = "Your Microsoft Entra access token";

var config =  SpeechConfig.FromHost(new Uri(hostName));

// You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
var authorizationToken = $"aad#{resourceId}#{aadToken}";
config.AuthorizationToken = authorizationToken;
```
::: zone-end

::: zone pivot="programming-language-cpp"
```cpp
std::string customDomainName = "Your Custom Name";
std::string aadToken = "Your Microsoft Entra access token";

auto speechConfig = SpeechConfig::FromHost("https://" + customDomainName + ".cognitiveservices.azure.com/");

// You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
auto authorizationToken = "aad#" + resourceId + "#" + aadToken;
speechConfig->SetAuthorizationToken(authorizationToken);
```
::: zone-end

::: zone pivot="programming-language-java"
```Java
String aadToken = "Your Microsoft Entra access token";
String customDomainName = "Your Custom Name";
String hostName = "https://" + customDomainName + ".cognitiveservices.azure.com/";
SpeechConfig speechConfig = SpeechConfig.fromHost(new URI(hostName));

// You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
String authorizationToken = "aad#" + resourceId + "#" + token;

speechConfig.setAuthorizationToken(authorizationToken);
```
::: zone-end

::: zone pivot="programming-language-python"
The ```VoiceProfileClient``` isn't available with the Speech SDK for Python.
::: zone-end

> [!NOTE]
> The ```ConversationTranslator``` doesn't support Microsoft Entra authentication.
