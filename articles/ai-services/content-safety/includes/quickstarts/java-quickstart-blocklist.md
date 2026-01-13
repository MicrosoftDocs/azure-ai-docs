---
title: "Quickstart: Use a blocklist with Java"
description: In this quickstart, get started using the Azure AI Content Safety Java SDK to create and use blocklists for text analysis.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 07/23/2025
ms.author: pafarley
---

[Reference documentation](/java/api/overview/azure/ai-contentsafety-readme) | [Library source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentsafety/azure-ai-contentsafety/src) | [Artifact (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-contentsafety) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/java/1.0.0)

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* The current version of the [Java Development Kit (JDK)](https://www.microsoft.com/openjdk)
* The [Gradle build tool](https://gradle.org/install/), or another dependency manager.
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.

## Set up application

Create a new Gradle project.

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. 
    
```console
mkdir myapp && cd myapp
```

Run the `gradle init` command from your working directory. This command will create essential build files for Gradle, including *build.gradle.kts*, which is used at runtime to create and configure your application.

```console
gradle init --type basic
```

When prompted to choose a **DSL**, select **Kotlin**.


### Install the client SDK 

This quickstart uses the Gradle dependency manager. You can find the client library and information for other dependency managers on the [Maven Central Repository](https://central.sonatype.com/artifact/com.azure/azure-ai-contentsafety).

Locate *build.gradle.kts* and open it with your preferred IDE or text editor. Then copy in the following build configuration. This configuration defines the project as a Java application whose entry point is the class **ContentSafetyBlocklistQuickstart**. It imports the Azure AI Content Safety library.

```kotlin
plugins {
    java
    application
}
application { 
    mainClass.set("ContentSafetyBlocklistQuickstart")
}
repositories {
    mavenCentral()
}
dependencies {
    implementation(group = "com.azure", name = "azure-ai-contentsafety", version = "1.0.0")
}
```

[!INCLUDE [Create environment variables](../env-vars.md)]

## Create and use a blocklist

From your working directory, run the following command to create a project source folder:

```console
mkdir -p src/main/java
```

Navigate to the new folder and create a file called *ContentSafetyBlocklistQuickstart.java*.

Open *ContentSafetyBlocklistQuickstart.java* in your preferred editor or IDE and paste in the following code. This code creates a new blocklist, adds items to it, and then analyzes a text string against the blocklist.

```java
import com.azure.ai.contentsafety.*;


import com.azure.ai.contentsafety.models.AddOrUpdateTextBlocklistItemsOptions;
import com.azure.ai.contentsafety.models.AddOrUpdateTextBlocklistItemsResult;
import com.azure.ai.contentsafety.models.AnalyzeTextOptions;
import com.azure.ai.contentsafety.models.AnalyzeTextResult;
import com.azure.ai.contentsafety.models.RemoveTextBlocklistItemsOptions;
import com.azure.ai.contentsafety.models.TextBlocklist;
import com.azure.ai.contentsafety.models.TextBlocklistItem;
import com.azure.ai.contentsafety.models.TextBlocklistMatch;
import com.azure.core.credential.KeyCredential;
import com.azure.core.exception.HttpResponseException;
import com.azure.core.http.rest.PagedIterable;
import com.azure.core.http.rest.RequestOptions;
import com.azure.core.http.rest.Response;
import com.azure.core.util.BinaryData;
import com.azure.core.util.Configuration;

import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;

public class ContentSafetyBlocklistQuickstart {
    public static void main(String[] args) {
        String endpoint = Configuration.getGlobalConfiguration().get("CONTENT_SAFETY_ENDPOINT");
        String key = Configuration.getGlobalConfiguration().get("CONTENT_SAFETY_KEY");

        BlocklistClient blocklistClient = new BlocklistClientBuilder()
            .credential(new KeyCredential(key))
            .endpoint(endpoint).buildClient();

        String blocklistName = "ProductSaleBlocklist";
        Map<String, String> description = new HashMap<>();
        description.put("description", "Contains terms related to the sale of a product.");
        BinaryData resource = BinaryData.fromObject(description);
        RequestOptions requestOptions = new RequestOptions();
        Response<BinaryData> response =
            blocklistClient.createOrUpdateTextBlocklistWithResponse(blocklistName, resource, requestOptions);
        if (response.getStatusCode() == 201) {
            System.out.println("\nBlocklist " + blocklistName + " created.");
        } else if (response.getStatusCode() == 200) {
            System.out.println("\nBlocklist " + blocklistName + " updated.");
        }

        String blockItemText1 = "price";
        String blockItemText2 = "offer";
        List<TextBlocklistItem> blockItems = Arrays.asList(
            new TextBlocklistItem(blockItemText1).setDescription("Price word"),
            new TextBlocklistItem(blockItemText2).setDescription("Offer word")
        );
        AddOrUpdateTextBlocklistItemsResult addedBlockItems = blocklistClient.addOrUpdateBlocklistItems(blocklistName,
            new AddOrUpdateTextBlocklistItemsOptions(blockItems));
        if (addedBlockItems != null && addedBlockItems.getBlocklistItems() != null) {
            System.out.println("\nBlockItems added:");
            for (TextBlocklistItem addedBlockItem : addedBlockItems.getBlocklistItems()) {
                System.out.println("BlockItemId: " + addedBlockItem.getBlocklistItemId() + ", Text: " + addedBlockItem.getText() + ", Description: " + addedBlockItem.getDescription());
            }
        }

        ContentSafetyClient contentSafetyClient = new ContentSafetyClientBuilder()
            .credential(new KeyCredential(key))
            .endpoint(endpoint).buildClient();
        AnalyzeTextOptions request = new AnalyzeTextOptions("You can order a copy now for the low price of $19.99.");
        request.setBlocklistNames(Arrays.asList(blocklistName));
        request.setHaltOnBlocklistHit(true);

        AnalyzeTextResult analyzeTextResult;
        try {
            analyzeTextResult = contentSafetyClient.analyzeText(request);
        } catch (HttpResponseException ex) {
            System.out.println("Analyze text failed.\nStatus code: " + ex.getResponse().getStatusCode() + ", Error message: " + ex.getMessage());
            throw ex;
        }

        if (analyzeTextResult.getBlocklistsMatch() != null) {
            System.out.println("\nBlocklist match result:");
            for (TextBlocklistMatch matchResult : analyzeTextResult.getBlocklistsMatch()) {
                System.out.println("BlocklistName: " + matchResult.getBlocklistName() + ", BlockItemId: " + matchResult.getBlocklistItemId() + ", BlockItemText: " + matchResult.getBlocklistItemText());
            }
        }
    }
}

```

Optionally replace the blocklist name and items with your own.

Navigate back to the project root folder, and build the app with:

```console
gradle build
```

Then, run it with the `gradle run` command:

```console
gradle run
```

## Output

```console
Blocklist ProductSaleBlocklist updated.

BlockItems added:
BlockItemId: 6155969c-1589-4c27-8cb0-61758985b2d9, Text: price, Description: Price word
BlockItemId: 0ca9ff49-d89b-4ecd-a451-28bd303342e1, Text: offer, Description: Offer word

Blocklist match result:
BlocklistName: ProductSaleBlocklist, BlockItemId: 6155969c-1589-4c27-8cb0-61758985b2d9, BlockItemText: price
```