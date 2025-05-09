---
title: 'Quickstart: Use Azure OpenAI Service with the Java SDK'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first chat completions call with the Java SDK. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 3/21/2025
---

[Source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai) | [Artifact (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-openai/1.0.0-beta.10) | [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai/src/samples) | [Retrieval Augmented Generation (RAG) enterprise chat template](/azure/developer/java/quickstarts/get-started-app-chat-template) | [IntelliJ IDEA](/azure/developer/java/toolkit-for-intellij/chatgpt-intellij) 

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
* The current version of the [Java Development Kit (JDK)](https://www.microsoft.com/openjdk)
- The [Gradle build tool](https://gradle.org/install/), or another dependency manager.
- An Azure OpenAI Service resource with the `gpt-4` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `chat-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir chat-quickstart && cd chat-quickstart
    ```

1. Install [Apache Maven](https://maven.apache.org/install.html). Then run `mvn -v` to confirm successful installation.
1. Create a new `pom.xml` file in the root of your project, and copy the following code into it:

   ```xml
   <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.azure.samples</groupId>
        <artifactId>quickstart-dall-e</artifactId>
        <version>1.0.0-SNAPSHOT</version>
        <build>
            <sourceDirectory>src</sourceDirectory>
            <plugins>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.7.0</version>
                <configuration>
                <source>1.8</source>
                <target>1.8</target>
                </configuration>
            </plugin>
            </plugins>
        </build>
        <dependencies>    
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-ai-openai</artifactId>
                <version>1.0.0-beta.10</version>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-core</artifactId>
                <version>1.53.0</version>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-identity</artifactId>
                <version>1.15.1</version>
            </dependency>
            <dependency>
                <groupId>org.slf4j</groupId>
                <artifactId>slf4j-simple</artifactId>
                <version>1.7.9</version>
            </dependency>
        </dependencies>
    </project>
   ```

1. Install the Azure OpenAI SDK and dependencies.

   ```console
   mvn clean dependency:copy-dependencies
   ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```console
    az login
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Run the app

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with an `AzureKeyCredential` object. 

#### [Microsoft Entra ID](#tab/keyless)

```java
OpenAIClient client = new OpenAIClientBuilder()
    .endpoint(endpoint)
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

#### [API key](#tab/api-key)

```java
OpenAIClient client = new OpenAIClientBuilder()
    .endpoint(endpoint)
    .credential(new AzureKeyCredential(key))
    .buildAsyncClient();
```
---

#### [Microsoft Entra ID](#tab/keyless)

Follow these steps to create a console application for speech recognition.

1. Create a new file named *Quickstart.java* in the same project root directory.
1. Copy the following code into *Quickstart.java*:

    ```java
    import com.azure.ai.openai.OpenAIClient;
    import com.azure.ai.openai.OpenAIClientBuilder;
    import com.azure.ai.openai.models.ChatChoice;
    import com.azure.ai.openai.models.ChatCompletions;
    import com.azure.ai.openai.models.ChatCompletionsOptions;
    import com.azure.ai.openai.models.ChatRequestAssistantMessage;
    import com.azure.ai.openai.models.ChatRequestMessage;
    import com.azure.ai.openai.models.ChatRequestSystemMessage;
    import com.azure.ai.openai.models.ChatRequestUserMessage;
    import com.azure.ai.openai.models.ChatResponseMessage;
    import com.azure.ai.openai.models.CompletionsUsage;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.azure.core.util.Configuration;
    
    import java.util.ArrayList;
    import java.util.List;
    
    public class QuickstartEntra {
    
        public static void main(String[] args) {
    
            String endpoint = Configuration.getGlobalConfiguration().get("AZURE_OPENAI_ENDPOINT");
            String deploymentOrModelId = "gpt-4o";
    
            // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    
            OpenAIClient client = new OpenAIClientBuilder()
                .endpoint(endpoint)
                .credential(new DefaultAzureCredentialBuilder().build())
                .buildClient();
    
            List<ChatRequestMessage> chatMessages = new ArrayList<>();
            chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant."));
            chatMessages.add(new ChatRequestUserMessage("Can I use honey as a substitute for sugar?"));
            chatMessages.add(new ChatRequestAssistantMessage("Yes, you can use use honey as a substitute for sugar."));
            chatMessages.add(new ChatRequestUserMessage("What other ingredients can I use as a substitute for sugar?"));    
    
            ChatCompletions chatCompletions = client.getChatCompletions(deploymentOrModelId, new ChatCompletionsOptions(chatMessages));
    
            System.out.printf("Model ID=%s is created at %s.%n", chatCompletions.getId(), chatCompletions.getCreatedAt());
            for (ChatChoice choice : chatCompletions.getChoices()) {
                ChatResponseMessage message = choice.getMessage();
                System.out.printf("Index: %d, Chat Role: %s.%n", choice.getIndex(), message.getRole());
                System.out.println("Message:");
                System.out.println(message.getContent());
            }
    
            System.out.println();
            CompletionsUsage usage = chatCompletions.getUsage();
            System.out.printf("Usage: number of prompt token is %d, "
                    + "number of completion token is %d, and number of total tokens in request and response is %d.%n",
                usage.getPromptTokens(), usage.getCompletionTokens(), usage.getTotalTokens());
        }
    }
    ```

1. Run your new console application to generate an image:

    ```console
    javac Quickstart.java -cp ".;target\dependency\*"
    java -cp ".;target\dependency\*" Quickstart
    ```

#### [API key](#tab/api-key)

Follow these steps to create a console application for speech recognition.

1. Create a new file named *Quickstart.java* in the same project root directory.
1. Copy the following code into *Quickstart.java*:

    ```java
    import com.azure.ai.openai.OpenAIClient;
    import com.azure.ai.openai.OpenAIClientBuilder;
    import com.azure.ai.openai.models.ChatChoice;
    import com.azure.ai.openai.models.ChatCompletions;
    import com.azure.ai.openai.models.ChatCompletionsOptions;
    import com.azure.ai.openai.models.ChatRequestAssistantMessage;
    import com.azure.ai.openai.models.ChatRequestMessage;
    import com.azure.ai.openai.models.ChatRequestSystemMessage;
    import com.azure.ai.openai.models.ChatRequestUserMessage;
    import com.azure.ai.openai.models.ChatResponseMessage;
    import com.azure.ai.openai.models.CompletionsUsage;
    import com.azure.core.credential.AzureKeyCredential;
    import com.azure.core.util.Configuration;
    
    import java.util.ArrayList;
    import java.util.List;
    
    public class Quickstart {
    
        public static void main(String[] args) {
            String key = Configuration.getGlobalConfiguration().get("AZURE_OPENAI_API_KEY");
            String endpoint = Configuration.getGlobalConfiguration().get("AZURE_OPENAI_ENDPOINT");
            String deploymentOrModelId = "gpt-4o";
    
            OpenAIClient client = new OpenAIClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(key))
                .buildClient();
    
            List<ChatRequestMessage> chatMessages = new ArrayList<>();
            chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant."));
            chatMessages.add(new ChatRequestUserMessage("Can I use honey as a substitute for sugar?"));
            chatMessages.add(new ChatRequestAssistantMessage("Yes, you can use use honey as a substitute for sugar."));
            chatMessages.add(new ChatRequestUserMessage("What other ingredients can I use as a substitute for sugar?"));    
    
            ChatCompletions chatCompletions = client.getChatCompletions(deploymentOrModelId, new ChatCompletionsOptions(chatMessages));
    
            System.out.printf("Model ID=%s is created at %s.%n", chatCompletions.getId(), chatCompletions.getCreatedAt());
            for (ChatChoice choice : chatCompletions.getChoices()) {
                ChatResponseMessage message = choice.getMessage();
                System.out.printf("Index: %d, Chat Role: %s.%n", choice.getIndex(), message.getRole());
                System.out.println("Message:");
                System.out.println(message.getContent());
            }
    
            System.out.println();
            CompletionsUsage usage = chatCompletions.getUsage();
            System.out.printf("Usage: number of prompt token is %d, "
                    + "number of completion token is %d, and number of total tokens in request and response is %d.%n",
                usage.getPromptTokens(), usage.getCompletionTokens(), usage.getTotalTokens());
        }
    }
    ```

1. Run your new console application to generate an image:

    ```console
    javac Quickstart.java -cp ".;target\dependency\*"
    java -cp ".;target\dependency\*" Quickstart
    ```

---


## Output

```output
Model ID=chatcmpl-BDgC0Yr8YNhZFhLABQYfx6QfERsVO is created at 2025-03-21T23:35:52Z.
Index: 0, Chat Role: assistant.
Message:
If you're looking to replace sugar in cooking, baking, or beverages, there are several alternatives you can use depending on your tastes, dietary needs, and the recipe. Here's a list of common sugar substitutes:

### **Natural Sweeteners**
1. **Honey**
   - Sweeter than sugar, so you may need less.
   - Adds moisture to recipes.
   - Adjust liquids and cooking temperature when baking to avoid over-browning.

2. **Maple Syrup**
   - Provides a rich, complex flavor.
   - Can be used in baking, beverages, and sauces.
   - Reduce the liquid content slightly in recipes.

3. **Agave Syrup**
   - Sweeter than sugar and has a mild flavor.
   - Works well in drinks, smoothies, and desserts.
   - Contains fructose, so use sparingly.

4. **Date Sugar or Date Paste**
   - Made from dates, it's a whole-food sweetener with fiber and nutrients.
   - Great for baked goods and smoothies.
   - May darken recipes due to its color.

5. **Coconut Sugar**
   - Similar in taste and texture to brown sugar.
   - Less refined than white sugar.
   - Slightly lower glycemic index, but still contains calories.

6. **Molasses**
   - Dark, syrupy byproduct of sugar refining.
   - Strong flavor; best for specific recipes like gingerbread or BBQ sauce.

### **Artificial Sweeteners**
1. **Stevia**
   - Extracted from the leaves of the stevia plant.
   - Virtually calorie-free and much sweeter than sugar.
   - Available as liquid, powder, or granulated.

2. **Erythritol**
   - A sugar alcohol with few calories and a clean, sweet taste.
   - Doesn?t caramelize like sugar.
   - Often blended with other sweeteners.

3. **Xylitol**
   - A sugar alcohol similar to erythritol.
   - Commonly used in baking and beverages.
   - Toxic to pets (especially dogs), so handle carefully.

### **Whole Fruits**
1. **Mashed Bananas**
   - Natural sweetness works well in baking.
   - Adds moisture to recipes.
   - Can replace sugar partially or fully depending on the dish.

2. **Applesauce (Unsweetened)**
   - Adds sweetness and moisture to baked goods.
   - Reduce other liquids in the recipe accordingly.

3. **Pureed Dates, Figs, or Prunes**
   - Dense sweetness with added fiber and nutrients.
   - Ideal for energy bars, smoothies, and baking.

### **Other Options**
1. **Brown Rice Syrup**
   - Less sweet than sugar, with a mild flavor.
   - Good for granola bars and baked goods.

2. **Yacon Syrup**
   - Extracted from the root of the yacon plant.
   - Sweet and rich in prebiotics.
   - Best for raw recipes.

3. **Monk Fruit Sweetener**
   - Natural sweetener derived from monk fruit.
   - Often mixed with erythritol for easier use.
   - Provides sweetness without calories.

### **Tips for Substitution**
- Sweeteners vary in sweetness, texture, and liquid content, so adjust recipes accordingly.
- When baking, reducing liquids or fats slightly may be necessary.
- Taste test when possible to ensure the sweetness level matches your preference.

Whether you're seeking healthier options, low-calorie substitutes, or simply alternatives for flavor, these sugar substitutes can work for a wide range of recipes!

Usage: number of prompt token is 60, number of completion token is 740, and number of total tokens in request and response is 800.
```


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* [Get started with the chat using your own data sample for Java](/azure/developer/java/ai/get-started-app-chat-template?toc=/azure/ai-services/openai/toc.json&bc=/azure/ai-services/openai/breadcrumb/toc.json&tabs=github-codespaces)
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
