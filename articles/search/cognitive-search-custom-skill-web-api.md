---
title: Custom Web API Skill in Skillsets
description: Extend capabilities of Azure AI Search skillsets by calling out to Web APIs. Use the Custom Web API skill to integrate your custom code.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ai-usage: ai-assisted
ms.topic: reference
ms.date: 07/30/2026
ms.update-cycle: 365-days
---

# Custom Web API skill in an Azure AI Search enrichment pipeline

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Use the **Custom Web API** skill to extend AI enrichment by calling a Web API endpoint that provides custom operations. Like built-in skills, a **Custom Web API** skill has inputs and outputs. Depending on the inputs, your Web API receives a JSON payload when the indexer runs, and returns a JSON payload as a response, along with a success status code. The response must include the outputs specified by your custom skill. Any other response is considered an error and no enrichments are performed. The structure of the JSON payload is described later in this document.

The **Custom Web API** skill is also used in the implementation of the [Azure OpenAI On Your Data](/azure/ai-services/openai/concepts/use-your-data) feature. If Azure OpenAI is [configured for role-based access](/azure/ai-services/openai/how-to/use-your-data-securely#configure-azure-openai) and you get `403 Forbidden` errors when creating the vector index, verify that Azure AI Search has a [system assigned identity](search-how-to-managed-identities.md#create-a-system-managed-identity) and runs as a [trusted service](/azure/ai-services/openai/how-to/use-your-data-securely#enable-trusted-service) on Azure OpenAI. 

> [!NOTE]
> The indexer retries twice for certain standard HTTP status codes returned from the Web API. These HTTP status codes are: 
> * `502 Bad Gateway`
> * `503 Service Unavailable`
> * `429 Too Many Requests`

## @odata.type

Microsoft.Skills.Custom.WebApiSkill

## Skill parameters

Parameters are case sensitive.

| Parameter name	 | Description |
|--------------------|-------------|
| `uri` | The URI of the Web API to which the JSON payload is sent. Only the **https** URI scheme is allowed. When you retrieve the skillset with GET, the service returns the `?code=` query parameter value as `?code=<redacted>` to prevent exposure of function keys. To update the skill without changing the stored URI, set `uri` to `<unchanged>`. |
| `authResourceId` | (Optional) A string that, when set, indicates that this skill should use a system managed identity on the connection to the function or app hosting the code. This property takes an application (client) ID or an app's registration in Microsoft Entra ID in any of these formats: `api://<appId>`, `<appId>/.default`, or `api://<appId>/.default`. This value is used to scope the authentication token retrieved by the indexer and is sent along with the Custom Web API skill request to the function or app. Setting this property requires that your search service is [configured for managed identity](search-how-to-managed-identities.md) and your Azure function app is [configured for a Microsoft Entra sign in](/azure/app-service/configure-authentication-provider-aad). To use this parameter, call the API with `api-version=2023-10-01-preview` or later. For guidance on choosing the correct value, see [Understand the `authResourceId` value](#understand-the-authresourceid-value). |
| `authIdentity`   | (Optional) A user-managed identity used by the search service for connecting to the function or app hosting the code. You can use either a [system or user managed identity](search-how-to-managed-identities.md). To use a system managed identity, leave `authIdentity` blank. |
| `httpMethod` | The method to use while sending the payload. Allowed methods are `PUT` or `POST` |
| `httpHeaders` | A collection of key-value pairs where the keys represent header names and values represent header values that are sent to your Web API along with the payload. The following headers are prohibited from being in this collection: `Accept`, `Accept-Charset`, `Accept-Encoding`, `Content-Length`, `Content-Type`, `Cookie`, `Host`, `TE`, `Upgrade`, `Via`. When you retrieve the skillset with GET, the service returns `<redacted>` for all header values to prevent exposure of credentials such as bearer tokens and API keys. To update the skill without changing stored header values, set each value to `<unchanged>`. The service restores the original stored value. |
| `timeout` | (Optional) When specified, indicates the timeout for the http client making the API call. It must be formatted as an XSD "dayTimeDuration" value (a restricted subset of an [ISO 8601 duration](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration) value). For example, `PT60S` for 60 seconds. If not set, a default value of 30 seconds is chosen. The timeout can be set to a maximum of 230 seconds and a minimum of 1 second. |
| `batchSize` | (Optional) Indicates how many "data records" (see JSON payload structure below) is sent per API call. If not set, a default of 1000 is chosen. Use this parameter to achieve a suitable tradeoff between indexing throughput and load on your API. |
| `degreeOfParallelism` | (Optional) When specified, indicates the number of calls the indexer makes in parallel to the endpoint you provide. You can decrease this value if your endpoint is failing under pressure, or raise it if your endpoint can handle the load. If not set, a default value of 5 is used. The `degreeOfParallelism` can be set to a maximum of 10 and a minimum of 1. |

### Understand the `authResourceId` value

When a Custom Web API skill uses managed identity authentication, Azure AI Search obtains a Microsoft Entra access token and sends it to the custom skill endpoint. The `authResourceId` property specifies the resource identifier, also known as the audience or Application ID URI, for which the token is requested. The value must match what the target application expects during token validation. Otherwise, authentication fails with a `401 Unauthorized` response.

The `authResourceId` value identifies the application hosting your custom skill. It isn't the URL of your search service or indexer.

The following table shows common formats:

| Target application | `authResourceId` value |
|---|---|
| Microsoft Entra protected web application | `api://<application-client-id>` |
| Application configured with a custom Application ID URI | Custom Application ID URI, such as `api://contoso-customskill` |
| Azure Function protected by Microsoft Entra ID | Application ID URI configured for the function app's app registration, such as `api://contoso-funcapp` |

The property accepts formats with and without the `.default` scope suffix. Use `api://<appId>` to match the Application ID URI directly. If you include a `.default` suffix, such as `api://<appId>/.default`, the access token's `aud` claim contains the base Application ID URI without the suffix.

For steps to configure Microsoft Entra authentication for an Azure Function and set `authResourceId`, see [Use a search service managed identity to connect to an Azure Function app](search-howto-managed-identities-azure-functions.md).

**Example: Azure Function protected by Microsoft Entra ID**

In this example, Azure AI Search acquires an access token for the audience specified by `authResourceId` and includes the token when invoking the custom skill endpoint.

```json
{
  "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
  "uri": "https://contoso-function.azurewebsites.net/api/enrich",
  "authResourceId": "api://contoso-customskill"
}
```

## Skill inputs

This skill has no predefined inputs. The inputs are any existing field, or any [node in the enrichment tree](cognitive-search-working-with-skillsets.md#enrichment-tree) that you want to pass to your custom skill.

## Skill outputs

This skill has no predefined outputs. Be sure to [define an output field mapping](cognitive-search-output-field-mapping.md) in the indexer if the skill's output should be sent to a field in the search index.

## Sample definition

```json
{
  "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
  "description": "A custom skill that can identify positions of different phrases in the source text",
  "uri": "https://contoso.count-things.com",
  "batchSize": 4,
  "context": "/document",
  "inputs": [
    {
      "name": "text",
      "source": "/document/content"
    },
    {
      "name": "language",
      "source": "/document/languageCode"
    },
    {
      "name": "phraseList",
      "source": "/document/keyphrases"
    }
  ],
  "outputs": [
    {
      "name": "hitPositions"
    }
  ]
}
```

> [!NOTE]
> When you retrieve a skillset by using GET, the service returns `<redacted>` for all `httpHeaders` values and `?code=<redacted>` for any `?code=` query parameter in the `uri`. Both values prevent exposure of credentials to callers who hold the Search Service Contributor role but no role on the external service. To update the skill without changing those stored values, pass `<unchanged>` for each affected field.
>
> The following example shows a GET response for a skill that uses header-based authentication and an Azure Function URI:
>
> ```json
> {
>   "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
>   "uri": "https://contoso.example.org/api?code=<redacted>",
>   "httpMethod": "POST",
>   "name": "myCustomSkill",
>   "httpHeaders": {
>     "Authorization": "<redacted>",
>     "Ocp-Apim-Subscription-Key": "<redacted>"
>   }
> }
> ```
>
> To update this skill without changing the existing values, use `<unchanged>`:
>
> ```json
> {
>   "uri": "<unchanged>",
>   "httpHeaders": {
>     "Authorization": "<unchanged>",
>     "Ocp-Apim-Subscription-Key": "<unchanged>"
>   }
> }
> ```

## Sample input JSON structure

This JSON structure represents the payload that you send to your Web API.
It always follows these constraints:

* The top-level entity is called `values` and is an array of objects. The number of these objects is at most the `batchSize`.

* Each object in the `values` array has:

  * A `recordId` property that's a **unique** string, used to identify that record.

  * A `data` property that's a JSON object. The fields of the `data` property correspond to the "names" specified in the `inputs` section of the skill definition. The values of those fields come from the `source` of those fields (which could be from a field in the document, or potentially from another skill).

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
             "text": "Este es un contrato en Inglés",
             "language": "es",
             "phraseList": ["Este", "Inglés"]
           }
      },
      {
        "recordId": "1",
        "data":
           {
             "text": "Hello world",
             "language": "en",
             "phraseList": ["Hi"]
           }
      },
      {
        "recordId": "2",
        "data":
           {
             "text": "Hello world, Hi world",
             "language": "en",
             "phraseList": ["world"]
           }
      },
      {
        "recordId": "3",
        "data":
           {
             "text": "Test",
             "language": "es",
             "phraseList": []
           }
      }
    ]
}
```

## Sample output JSON structure

The "output" corresponds to the response returned from your Web API. The Web API should only return a JSON payload (verified by looking at the `Content-Type` response header) and should satisfy the following constraints:

* There should be a top-level entity called `values`, which should be an array of objects.

* The number of objects in the array should be the same as the number of objects sent to the Web API.

* Each object should have:

  * A `recordId` property.

  * A `data` property, which is an object where the fields are enrichments matching the "names" in the `output` and whose value is considered the enrichment.

  * An `errors` property, an array listing any errors encountered that is added to the indexer execution history. This property is required, but can have a `null` value.

  * A `warnings` property, an array listing any warnings encountered that is added to the indexer execution history. This property is required, but can have a `null` value.

* The ordering of objects in the `values` in either the request or response isn't important. However, the `recordId` is used for correlation so any record in the response containing a `recordId`, which wasn't part of the original request to the Web API is discarded.

```json
{
    "values": [
        {
            "recordId": "3",
            "data": {
            },
            "errors": [
              {
                "message" : "'phraseList' should not be null or empty"
              }
            ],
            "warnings": null
        },
        {
            "recordId": "2",
            "data": {
                "hitPositions": [6, 16]
            },
            "errors": null,
            "warnings": null
        },
        {
            "recordId": "0",
            "data": {
                "hitPositions": [0, 23]
            },
            "errors": null,
            "warnings": null
        },
        {
            "recordId": "1",
            "data": {
                "hitPositions": []
            },
            "errors": null,
            "warnings": [
              {
                "message": "No occurrences of 'Hi' were found in the input text"
              }
            ]
        },
    ]
}

```

## Error cases

In addition to your Web API being unavailable or sending non-successful status codes, consider the following cases as errors:

* If the Web API returns a success status code but the response indicates that it isn't `application/json`, the response is invalid and no enrichments are performed.

* If the response `values` array contains invalid records (for example, missing or duplicated `recordId`), the invalid records aren't enriched. When developing custom skills, adhere to the Web API skill contract. You can refer to [this example](https://github.com/Azure-Samples/azure-search-power-skills/blob/main/Common/WebAPISkillContract.cs) provided in the [Power Skill repository](https://github.com/Azure-Samples/azure-search-power-skills/tree/main) that follows the expected contract. 

For cases when the Web API is unavailable or returns an HTTP error, the indexer execution history includes a friendly error with any available details about the HTTP error.

## Security considerations for managed identity authentication

When using managed identity authentication with a Custom Web API skill, Azure AI Search obtains a Microsoft Entra access token for the application identified by `authResourceId` and includes that token in requests sent to the endpoint specified by `uri`. The endpoint referenced by `uri` is typically your Azure Function, Azure App Service, Azure API Management endpoint, or another Microsoft Entra-protected application. You're responsible for configuring and maintaining the relationship between the endpoint and the application identified by `authResourceId`.

Regardless of the authentication method, custom skill inputs can contain values from customer-provided documents or values derived from those documents. Treat all custom skill inputs as untrusted input. Azure AI Search forwards the inputs configured in the skillset to your endpoint without interpreting, validating, or constraining their content for your custom implementation.

Validate and constrain document-derived values in your custom skill before using them in outbound requests or other security-sensitive operations. Use input validation, destination allowlists, URL and hostname validation, protocol restrictions, and least-privilege network access that permits only the destinations and ports the skill requires. For more information, see [Architecture strategies for networking and connectivity](/azure/well-architected/security/networking#classify-the-traffic-flows).

### Recommended security practices

To help maintain a secure deployment, follow these practices:

- Configure the `uri` property to point only to trusted endpoints that are intended to receive requests from Azure AI Search.
- Configure `authResourceId` to identify the Microsoft Entra application that is expected to receive and validate the access token.
- Ensure that the application receiving requests validates standard token claims, including audience (`aud`), issuer (`iss`), tenant (`tid`), and any required application roles or permissions, before processing requests.
- Apply the principle of least privilege when granting permissions to the Azure AI Search managed identity.
- Periodically review Custom Web API skill definitions, Microsoft Entra application registrations, and app role assignments and permissions granted to Azure AI Search managed identities. Review configuration changes through your established change-management and security-review processes.
- Periodically review endpoint configurations for Azure Functions, App Services, APIs, and API gateways.
- Monitor application sign-in logs, authentication events, and API access logs for unexpected or unauthorized activity.
- Remove unused endpoints, permissions, application registrations, and role assignments that are no longer required.

### Restrict access to skillset configuration

Users who can create, modify, or run skillsets can control both the destination endpoint and the authentication configuration used by a Custom Web API skill. Restrict these permissions to trusted administrators and follow your standard change-management and security review processes when configuring managed identity-enabled custom skills.

> [!IMPORTANT]
> The `authResourceId` value identifies the intended recipient application for the access token. Ensure that the endpoint specified in `uri` is the endpoint that is expected to receive and validate tokens for that application. Incorrect configuration can result in authentication failures or requests being sent to an unintended endpoint.

## See also

+ [Define a skillset](cognitive-search-defining-skillset.md)
+ [Add custom skill to an AI enrichment pipeline](cognitive-search-custom-skill-interface.md)
+ [Example: Creating a custom skill for AI enrichment](cognitive-search-create-custom-skill-example.md)
+ [Power Skill repository](https://github.com/Azure-Samples/azure-search-power-skills/tree/main)
