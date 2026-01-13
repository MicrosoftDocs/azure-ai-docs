---
title: Export/import/refresh | custom question answering projects and projects
description: Learn about backing up your custom question answering projects and projects
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
recommendations: false
ms.date: 12/15/2025
---
# Export-import-refresh in custom question answering

You might want to create a copy of your custom question answering project or related question and answer pairs for several reasons:

* To implement a backup and restore process
* To integrate with your CI/CD pipeline
* To move your data to different regions

## Prerequisites

* An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
* A [language resource](https://aka.ms/create-language-resource) with the custom question answering feature enabled. Remember your Microsoft Entra ID, Subscription, language resource name you selected when you created the resource.


### Export a project programmatically

To automate the export process, use the [export functionality of the authoring API](./authoring.md#export-project-metadata-and-assets)

### Import a project programmatically

To automate the import process, use the [import functionality of the authoring API](./authoring.md#import-project)

### Refresh a URL programmatically

To automate the URL refresh process, use the [update sources functionality of the authoring API](./authoring.md#update-sources)

The update sources example in the [Authoring API docs](./authoring.md#update-sources) shows the syntax for adding a new URL-based source. An example query for an update would be as follows:

|Variable name | Value |
|--------------------------|-------------|
| `ENDPOINT`               | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. An example endpoint is: `https://southcentralus.cognitiveservices.azure.com/` and you only need to add the region-specific portion of `southcentral`. The endpoint path is already present.|
| `API-KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either Key1 or Key2. Always having two valid keys allows for secure key rotation with zero downtime. The key value is part of the sample request.|
| `PROJECT-NAME` | The name of project where you would like to update sources.|

```bash
curl -X PATCH -H "Ocp-Apim-Subscription-Key: {API-KEY}" -H "Content-Type: application/json" -d '[
  {
    "op": "replace",
    "value": {
      "displayName": "source5",
      "sourceKind": "url",
      "sourceUri": https://download.microsoft.com/download/7/B/1/7B10C82E-F520-4080-8516-5CF0D803EEE0/surface-book-user-guide-EN.pdf,
      "refresh": "true"
    }
  }
]'  -i 'https://{ENDPOINT}.cognitiveservices.azure.com/language/query-knowledgebases/projects/{PROJECT-NAME}/sources?api-version=2021-10-01'
```


## Next steps

* [Learn how to use the Authoring API](./authoring.md)
