---
title: 'Quickstart: Use Azure OpenAI in Microsoft Foundry Models with the Java SDK to generate images'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first image generation call with the Java SDK. 
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
author: PatrickFarley
ms.author: pafarley
ms.date: 01/29/2026
ai-usage: ai-assisted
---

Use this guide to get started generating images with the Azure OpenAI SDK for Java.

[Library source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai) | [Artifact (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-openai/1.0.0-beta.3) | [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai/src/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- The current version of the [Java Development Kit (JDK)](https://www.microsoft.com/openjdk)
- Install [Apache Maven](https://maven.apache.org/install.html).
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `image-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir image-quickstart && cd image-quickstart
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
                <version>1.0.0-beta.3</version>
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
OpenAIAsyncClient client = new OpenAIClientBuilder()
    .endpoint(endpoint)
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

#### [API key](#tab/api-key)

```java
OpenAIAsyncClient client = new OpenAIClientBuilder()
    .endpoint(endpoint)
    .credential(new AzureKeyCredential(key))
    .buildAsyncClient();
```
---

#### [Microsoft Entra ID](#tab/keyless)

Follow these steps to create a console application for image generation.

1. Create a new file named *Quickstart.java* in the same project root directory.
1. Copy the following code into *Quickstart.java*:

    ```java
    import com.azure.ai.openai.OpenAIAsyncClient;
    import com.azure.ai.openai.OpenAIClientBuilder;
    import com.azure.ai.openai.models.ImageGenerationOptions;
    import com.azure.ai.openai.models.ImageLocation;
    import com.azure.core.credential.AzureKeyCredential;
    import com.azure.core.models.ResponseError;
    
    import java.util.concurrent.TimeUnit;
    
    public class Quickstart {

        public static void main(String[] args) throws InterruptedException {
            
            String endpoint = System.getenv("AZURE_OPENAI_ENDPOINT");
    
            // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    
            OpenAIAsyncClient client = new OpenAIClientBuilder()
                .endpoint(endpoint)
                .credential(new DefaultAzureCredentialBuilder().build())
                .buildAsyncClient();
                
            ImageGenerationOptions imageGenerationOptions = new ImageGenerationOptions(
                "A drawing of the Seattle skyline in the style of Van Gogh");
            client.getImages(imageGenerationOptions).subscribe(
                images -> {
                    for (ImageLocation imageLocation : images.getData()) {
                        ResponseError error = imageLocation.getError();
                        if (error != null) {
                            System.out.printf("Image generation operation failed. Error code: %s, error message: %s.%n",
                                error.getCode(), error.getMessage());
                        } else {
                            System.out.printf(
                                "Image location URL that provides temporary access to download the generated image is %s.%n",
                                imageLocation.getUrl());
                        }
                    }
                },
                error -> System.err.println("There was an error getting images." + error),
                () -> System.out.println("Completed getImages."));
    
            // The .subscribe() creation and assignment isn't a blocking call.
            // The thread sleeps so the program does not end before the send operation is complete. 
            // Use .block() instead of .subscribe() for a synchronous call.
            TimeUnit.SECONDS.sleep(10);
        }
    }
    ```

1. Run your new console application to generate an image:

    ```console
    javac Quickstart.java -cp ".;target\dependency\*"
    java -cp ".;target\dependency\*" Quickstart
    ```

#### [API key](#tab/api-key)

Follow these steps to create a console application for image generation.

1. Create a new file named *Quickstart.java* in the same project root directory.
1. Copy the following code into *Quickstart.java*:

    ```java
    import com.azure.ai.openai.OpenAIAsyncClient;
    import com.azure.ai.openai.OpenAIClientBuilder;
    import com.azure.ai.openai.models.ImageGenerationOptions;
    import com.azure.ai.openai.models.ImageLocation;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.azure.core.models.ResponseError;
    
    import java.util.concurrent.TimeUnit;
    
    public class Quickstart {
    
        public static void main(String[] args) throws InterruptedException {
            
            String key = System.getenv("AZURE_OPENAI_API_KEY");
            String endpoint = System.getenv("AZURE_OPENAI_ENDPOINT");
    
            OpenAIAsyncClient client = new OpenAIClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(key))
                .buildAsyncClient();
    
            ImageGenerationOptions imageGenerationOptions = new ImageGenerationOptions(
                "A drawing of the Seattle skyline in the style of Van Gogh");
            client.getImages(imageGenerationOptions).subscribe(
                images -> {
                    for (ImageLocation imageLocation : images.getData()) {
                        ResponseError error = imageLocation.getError();
                        if (error != null) {
                            System.out.printf("Image generation operation failed. Error code: %s, error message: %s.%n",
                                error.getCode(), error.getMessage());
                        } else {
                            System.out.printf(
                                "Image location URL that provides temporary access to download the generated image is %s.%n",
                                imageLocation.getUrl());
                        }
                    }
                },
                error -> System.err.println("There was an error getting images." + error),
                () -> System.out.println("Completed getImages."));
    
            // The .subscribe() creation and assignment isn't a blocking call.
            // The thread sleeps so the program does not end before the send operation is complete. 
            // Use .block() instead of .subscribe() for a synchronous call.
            TimeUnit.SECONDS.sleep(10);
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

The URL of the generated image is printed to the console.

```console
Image location URL that provides temporary access to download the generated image is <SAS URL>.
Completed getImages.
```

> [!NOTE]
> The Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it won't return a generated image. For more information, see the [content filter](../concepts/content-filter.md) article.


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
