---
title: 'How to use Agents with Morningstar licensed data'
titleSuffix: Azure AI services
description: Learn how to use your developer account with Morningstar grounding with Azure AI Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 03/04/2025
author: aahill
ms.author: aahi
recommendations: false
---

# Use Morningstar data to ground your AI agents

Azure AI Agent Service lets you integrate licensed data from specialized data providers to enhance the quality of your agent's responses with high-quality, fresh data. [Morningstar](https://developer.morningstar.com/). Morningstar is a prominent investment research company that provides comprehensive analysis, ratings, and data on mutual funds, ETFs, stocks, and bonds. The insights from this data source can empower your agents to deliver nuanced, informed solutions tailored to specific use cases.

> [!IMPORTANT]
> - Your use of connected non-Microsoft services is subject to the terms between you and the service provider. By connecting to a non-Microsoft service, you acknowledge that some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft data.
> - Grounding with licensed data incurs usage with licensed data providers, review the pricing plan with your selected licensed data providers.


## Prerequisites

Create a developer account with Morningstar: To start, access the Morningstar tool with your Morningstar credentials. If you don't have a Morningstar account, contact `iep-dev@morningstar.com`. Provide an email address for your account username during onboarding. Morningstar will email instructions for creating a password and activating your account. Store and transmit your unique username and password securely. 

To get your token for your Morningstar developer account, you can use the following script: 

```python 
import requests 
from requests.auth import HTTPBasicAuth 
url = "https://www.us-api.morningstar.com/token/oauth" 
auth = HTTPBasicAuth("YOUR_EMAIL_ADDRESS", "YOUR_PASSWORD") 
response = requests.post(url, auth=auth) 
print(response.text) 
#Note: This token expires, remember to refresh your credentials. 
``` 

[!INCLUDE [licensed-data-setup](../../includes/licensed-data-setup.md)]

## Use your tool in code

You can follow the instructions in [OpenAPI spec tool](./openapi-spec.md) to connect your tool through the OpenAPI spec.

1. Remember to store and import your [Morningstar](https://developer.morningstar.com/content/documentation/intelligence-engine/apps/morningstar-agent-api/3.1.0/morningstar-agent-api.json) OpenAPI spec. You can find it in the Azure AI Foundry portal.

1. Make sure you have updated the authentication method to be `connection` and fill in the connection ID of your custom key connection.

   ``` python
   auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id="your_connection_id"))
   ```
    
   > [!TIP]
   > Your connection ID will have the following format:`/subscriptions/{subscription ID}/resourceGroups/{resource group name}/providers/Microsoft.CognitiveService/account/{project name}/connections/{connection name}`  