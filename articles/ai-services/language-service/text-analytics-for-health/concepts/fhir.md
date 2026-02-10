---
title: Fast Healthcare Interoperability Resources (FHIR) structuring in Text Analytics for health
titleSuffix: Foundry Tools
description: Learn about Fast Healthcare Interoperability Resources (FHIR) structuring
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 12/05/2025
ms.author: lajanuar
ms.custom: language-service-health, ignite-2024
---
# Utilizing Fast Healthcare Interoperability Resources (FHIR) structuring in Text Analytics for Health

When you process unstructured data using Text Analytics for health, you can request that the output response includes a Fast Healthcare Interoperability Resources (FHIR) resource bundle. The FHIR resource bundle output is enabled by passing the FHIR version as part of the options in each request. How you pass the FHIR version differs depending on whether you're using the SDK or the REST API.

## Use the REST API
When you use the REST API as part of building the request payload, you include a Tasks object. Each of the Tasks can have parameters. One of the options for parameters is `fhirVersion`. By including the `fhirVersion` parameter in the Task object parameters, you're requesting the output to include a FHIR resource bundle in addition to the normal Text Analytics for health output. The following example shows the inclusion of `fhirVersion` in the request parameters.

```json
{
      "analysis input": {
            "documents:"[
                {
                text:"54 year old patient had pain in the left elbow with no relief from 100 mg Ibuprofen",
                "language":"en",
                "id":"1"
                }
            ]
        },
    "tasks"[
       {
       "taskId":"analyze 1",
       "kind":"Healthcare",
       "parameters":
            {
            "fhirVersion":"4.0.1"
            }
        }
    ]
}
```

Once the request completes processing by Text Analytics for health and you pull the response from the REST API, you can find the FHIR resource bundle in the output. You can locate the FHIR resource bundle inside each document processed using the property name `fhirBundle`. The following partial sample is output highlighting the `fhirBundle`.

```json
{
  "jobID":"50d11b05-7a03-a611-6f1e95ebde07",
  "lastUpdatedDateTime":"2024-06-05T17:29:51Z",
  "createdDateTime:"2024-06-05T17:29:40Z",
  "expirationDateTime":"2024-06-05T17:29:40Z",
  "status":"succeeded",
  "errors":[],
  "tasks":{
    "completed": 1,
    "failed": 0,
    "inProgress": 0,
    "total": 1,
    "items": [
        {
          "kind":"HealthcareLROResults",
          "lastUpdatedDateTime":"2024-06-05T17:29:51.5839858Z",
          "status":"succeeded",
          "results": {
              "documents": [
                  {
                    "id": "1",
                    "entities": [...
                    ],
                    "relations": [...
                    ].
                    "warnings":[],
                    "fhirBundle": {
                        "resourceType": "Bundle",
                        "id": "b4d907ed-0334-4186-9e21-8ed4d79e709f",
                        "meta": {
                            "profile": [
                                "http://hl7.org/fhir/4.0.1/StructureDefinition/Bundle"
                                  ]
                                },  
```

## Use the REST SDK
You can also use the SDK to make the request for Text Analytics for health to include the FHIR resource bundle in the output. To accomplish this request with the SDK, you would create an instance of `AnalyzeHealthcareEntitiesOptions` and populate the `FhirVersion` property with the FHIR version. This options object is then passed to each `StartAnalyzeHealthcareEntitiesAsync` method call to configure the request to include a FHIR resource bundle in the output.

## Next steps

* [How to call the Text Analytics for health](../how-to/call-api.md)
