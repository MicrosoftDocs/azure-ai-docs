---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
## Typical workflow

To use this feature, you submit data for analysis and handle the API output in your application. Analysis is performed as-is, with no added customization to the model used on your data.

1. Create an Azure Language in Foundry Tools resource, which grants you access to the features offered by Language. It generates a password (called a key) and an endpoint URL that you use to authenticate API requests.

2. Create a request using either the REST API or the client library for C#, Java, JavaScript, and Python. You can also send asynchronous calls with a batch request to combine API requests for multiple features into a single call.

3. Send the request containing your text data. Your key and endpoint are used for authentication.

4. Stream or store the response locally.
