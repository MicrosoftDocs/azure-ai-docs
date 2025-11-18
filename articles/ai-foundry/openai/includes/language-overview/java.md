---
title: Azure OpenAI Java support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI Java support
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 10/02/2025
---


[Source code](https://github.com/openai/openai-java/blob/main/README.md) |[REST API reference documentation](../../latest.md) | [Package reference documentation](https://javadoc.io/doc/com.openai/openai-java/latest/index.html) | [Maven Central](https://central.sonatype.com/artifact/com.openai/openai-java/4.0.1)

## Azure OpenAI API version support

- v1 Generally Available (GA) API now allows access to both GA and Preview operations. To learn more, see the [API version lifecycle guide](../../api-version-lifecycle.md).

## Installation

### Gradle

```kotlin
implementation("com.openai:openai-java:4.0.1")
```

### Maven

```xml
<dependency>
  <groupId>com.openai</groupId>
  <artifactId>openai-java</artifactId>
  <version>4.0.1</version>
</dependency>
```

## Authentication

# [Microsoft Entra ID](#tab/secure)

Authentication with Microsoft Entra ID requires some initial setup:

Add the Azure Identity package:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.18.0</version>
</dependency>
```

After setup, you can choose which type of credential from `azure.identity` to use. As an example, `DefaultAzureCredential` can be used to authenticate the client: Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra ID application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET.

Authorization is easiest using `DefaultAzureCredential`. It finds the best credential to use in its running environment though use of `DefaultAzureCredential` is only recommended for testing, not for production.  

```java
Credential tokenCredential = BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
                new DefaultAzureCredentialBuilder().build(),
                "https://cognitiveservices.azure.com/.default"));
OpenAIClient client = OpenAIOkHttpClient.builder()
        .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
        .credential(tokenCredential)
        .build();
```

For more information about Azure OpenAI keyless authentication, see [Use Azure OpenAI without keys](/azure/developer/ai/keyless-connections?tabs=java%2Cazure-cli).

# [API Key](#tab/api-key)

```java
OpenAIClient client = OpenAIOkHttpClient.builder()
                .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
                .apiKey(apiKey)
                .build();
```

---

## Responses

```java
package com.example;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.azure.core.credential.AzureKeyCredential;

public class OpenAITest {
    public static void main(String[] args) {
        // Get API key from environment variable for security
        String apiKey = System.getenv("OPENAI_API_KEY");
        String resourceName = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";
        String modelDeploymentName = "gpt-4.1"; //replace with you model deployment name

        try {
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    .baseUrl(resourceName)
                    .apiKey(apiKey)
                    .build();

            ResponseCreateParams params = ResponseCreateParams.builder()
                    .input("Tell me about the bitter lesson?")
                    .model(modelDeploymentName)
                    .build();

            Response response = client.responses().create(params);
            
            System.out.println("Response: " + response);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```