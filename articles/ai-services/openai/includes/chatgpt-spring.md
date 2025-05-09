---
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle # external contributor: gm2552
ms.author: mbullwin
ms.date: 11/27/2023
---

[Source code](https://github.com/spring-projects/spring-ai) | [Artifacts (Maven)](https://repo.spring.io/ui/native/snapshot/org/springframework/experimental/ai/spring-ai-openai-spring-boot-starter/0.7.0-SNAPSHOT) | [Sample](https://github.com/Azure-Samples/spring-ai-samples/tree/main/ai-chat-demo)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- The current version of the [Java Development Kit (JDK)](https://www.microsoft.com/openjdk)
- The [Spring Boot CLI tool](https://docs.spring.io/spring-boot/docs/current/reference/html/getting-started.html#getting-started.installing.cli)
- An Azure OpenAI Service resource with the `gpt-4` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md). This example assumes that your deployment name matches the model name `gpt-4`

## Set up

[!INCLUDE [get-key-endpoint](get-key-endpoint.md)]

[!INCLUDE [environment-variables](spring-environment-variables.md)]



## Create a new Spring application

Create a new Spring project.

In a Bash window, create a new directory for your app, and navigate to it.

```bash
mkdir ai-chat-demo && cd ai-chat-demo
```

Run the `spring init` command from your working directory. This command creates a standard directory structure for your Spring project including the main Java class source file and the *pom.xml* file used for managing Maven based projects.

```bash
spring init -a ai-chat-demo -n AIChat --force --build maven -x
```

The generated files and folders resemble the following structure:

```
ai-chat-demo/
|-- pom.xml
|-- mvn
|-- mvn.cmd
|-- HELP.md
|-- src/
    |-- main/
    |   |-- resources/
    |   |   |-- application.properties
    |   |-- java/
    |       |-- com/
    |           |-- example/
    |               |-- aichatdemo/
    |                   |-- AiChatApplication.java
    |-- test/
        |-- java/
            |-- com/
                |-- example/
                    |-- aichatdemo/
                        |-- AiChatApplicationTests.java
```

## Edit Spring application

1. Edit the *pom.xml* file.

   From the root of the project directory, open the *pom.xml* file in your preferred editor or IDE and overwrite the file with the following content:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
      <modelVersion>4.0.0</modelVersion>
      <parent>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-parent</artifactId>
         <version>3.3.4</version>
         <relativePath/> <!-- lookup parent from repository -->
      </parent>
      <groupId>com.example</groupId>
      <artifactId>ai-chat-demo</artifactId>
      <version>0.0.1-SNAPSHOT</version>
      <name>AIChat</name>
      <description>Demo project for Spring Boot</description>
      <properties>
         <java.version>17</java.version>
         <spring-ai.version>1.0.0-M5</spring-ai.version>
      </properties>
      <dependencies>
         <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
         </dependency>
         <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-azure-openai-spring-boot-starter</artifactId>
         </dependency>
         <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
         </dependency>
      </dependencies>
      <dependencyManagement>
         <dependencies>
            <dependency>
               <groupId>org.springframework.ai</groupId>
               <artifactId>spring-ai-bom</artifactId>
               <version>${spring-ai.version}</version>
               <type>pom</type>
               <scope>import</scope>
            </dependency>
         </dependencies>
      </dependencyManagement>
      <build>
         <plugins>
            <plugin>
               <groupId>org.springframework.boot</groupId>
               <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
         </plugins>
      </build>
      <repositories>
         <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots>
               <enabled>false</enabled>
            </snapshots>
         </repository>
      </repositories>

   </project>
   ```

1. From the *src/main/java/com/example/aichatdemo* folder, open *AiChatApplication.java* in your preferred editor or IDE and paste in the following code:

   ```java
   package com.example.aichatdemo;

   import org.slf4j.Logger;
   import org.slf4j.LoggerFactory;
   import org.springframework.ai.chat.client.ChatClient;
   import org.springframework.boot.CommandLineRunner;
   import org.springframework.boot.SpringApplication;
   import org.springframework.boot.autoconfigure.SpringBootApplication;
   import org.springframework.context.annotation.Bean;

   @SpringBootApplication
   public class AiChatApplication {

      private static final Logger log = LoggerFactory.getLogger(AiChatApplication.class);

      public static void main(String[] args) {
         SpringApplication.run(AiChatApplication.class, args);
      }

      @Bean
      CommandLineRunner commandLineRunner(ChatClient.Builder builder) {
         return args -> {
            var chatClient = builder.build();
            log.info("Sending chat prompts to AI service. One moment please...");
            String response = chatClient.prompt()
                  .user("What was Microsoft's original internal codename for the project that eventually became Azure?")
                  .call()
                  .content();

            log.info("Response: {}", response);
         };
      }
   }
   ```

   > [!IMPORTANT]
   > For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see the Azure AI services [security](../../security-features.md) article.

1. Navigate back to the project root folder, and run the app by using the following command:

   ```bash
   ./mvnw spring-boot:run
   ```

## Output

```output
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v3.3.4)

2025-03-14T13:35:30.145-04:00  INFO 93252 --- [AIChat] [           main] c.example.aichatdemo.AiChatApplication   : Starting AiChatApplication using Java 23.0.2 with PID 93252 (/Users/vega/dev/msft/spring-ai-samples/ai-chat-demo/target/classes started by vega in /Users/vega/dev/msft/spring-ai-samples/ai-chat-demo)
2025-03-14T13:35:30.146-04:00  INFO 93252 --- [AIChat] [           main] c.example.aichatdemo.AiChatApplication   : No active profile set, falling back to 1 default profile: "default"
2025-03-14T13:35:30.500-04:00  INFO 93252 --- [AIChat] [           main] c.example.aichatdemo.AiChatApplication   : Started AiChatApplication in 0.445 seconds (process running for 0.633)
2025-03-14T13:35:30.501-04:00  INFO 93252 --- [AIChat] [           main] c.example.aichatdemo.AiChatApplication   : Sending chat prompts to AI service. One moment please...
2025-03-14T13:35:31.950-04:00  INFO 93252 --- [AIChat] [           main] c.example.aichatdemo.AiChatApplication   : Response: Microsoft's original internal codename for the project that eventually became Azure was "Project Red Dog." This initiative ultimately led to the development and launch of the Microsoft Azure cloud computing platform.
```


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
