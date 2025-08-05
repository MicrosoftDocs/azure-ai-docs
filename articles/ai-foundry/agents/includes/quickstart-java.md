
| [Reference documentation](/dotnet/api/overview/azure/ai.agents.persistent-readme) | [Samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/csharp/getting-started-agents) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Agents.Persistent) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.Agents.Persistent) |

## Prerequisites

[!INCLUDE [universal-prerequisites](universal-prerequisites.md)]

## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models in conjunction with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |

1. Create a New Java Console project. You will need the following dependencies to run the code:
    
    ```xml
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-ai-agents-persistent</artifactId>
            <version>1.0.0-beta.2</version>
        </dependency>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-identity</artifactId>
            <version>1.17.0-beta.1</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.32</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>1.7.32</version>
        </dependency>
    </dependencies>
    ```

Next, to authenticate your API requests and run the program, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Use the following code to create and run an agent. To run this code, you will need to get the endpoint for your project. This string is in the format:

`https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>`

[!INCLUDE [connection-string-deprecation](connection-string-deprecation.md)]

[!INCLUDE [endpoint-string-portal](endpoint-string-portal.md)]

Set this endpoint in an environment variable named `ProjectEndpoint`.

[!INCLUDE [model-name-portal](model-name-portal.md)]

Save the name of your model deployment name as an environment variable named `ModelDeploymentName`. 

## Code example

```java
package com.example.agents;

import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.ai.agents.persistent.PersistentAgentsAdministrationClient;
import com.azure.ai.agents.persistent.models.CreateAgentOptions;
import com.azure.ai.agents.persistent.models.CreateThreadAndRunOptions;
import com.azure.ai.agents.persistent.models.PersistentAgent;
import com.azure.ai.agents.persistent.models.ThreadRun;
import com.azure.core.credential.TokenCredential;
import com.azure.core.exception.HttpResponseException;
import com.azure.core.util.logging.ClientLogger;
import com.azure.identity.DefaultAzureCredentialBuilder;

public class Main {
    private static final ClientLogger logger = new ClientLogger(Main.class);

    public static void main(String[] args) {
        // Load environment variables with better error handling, supporting both .env and system environment variables
        String endpoint = System.getenv("AZURE_ENDPOINT");
        String projectEndpoint = System.getenv("PROJECT_ENDPOINT");
        String modelName = System.getenv("MODEL_DEPLOYMENT_NAME");
        String agentName = System.getenv("AGENT_NAME");
        String instructions = "You are a helpful assistant that provides clear and concise information.";     

        // Check for required endpoint configuration
        if (projectEndpoint == null && endpoint == null) {
            String errorMessage = "Environment variables not configured. Required: either PROJECT_ENDPOINT or AZURE_ENDPOINT must be set.";
            logger.error("ERROR: {}", errorMessage);
            logger.error("Please set your environment variables or create a .env file. See README.md for details.");
            return;
        }
        
        // Use AZURE_ENDPOINT as fallback if PROJECT_ENDPOINT not set
        if (projectEndpoint == null) {
            projectEndpoint = endpoint;
            logger.info("Using AZURE_ENDPOINT as PROJECT_ENDPOINT: {}", projectEndpoint);
        }

        // Set defaults for optional parameters with informative logging
        if (modelName == null) {
            modelName = "gpt-4o";
            logger.info("No MODEL_DEPLOYMENT_NAME provided, using default: {}", modelName);
        }
        if (agentName == null) {
            agentName = "java-quickstart-agent";
            logger.info("No AGENT_NAME provided, using default: {}", agentName);
        }
        if (instructions == null) {
            instructions = "You are a helpful assistant that provides clear and concise information.";
            logger.info("No AGENT_INSTRUCTIONS provided, using default instructions");
        }

        // Create Azure credential with DefaultAzureCredentialBuilder
        // This supports multiple authentication methods including environment variables,
        // managed identities, and interactive browser login
        logger.info("Building DefaultAzureCredential");
        TokenCredential credential = new DefaultAzureCredentialBuilder().build();

        try {
            // Build the general agents client
            logger.info("Creating PersistentAgentsClient with endpoint: {}", projectEndpoint);
            PersistentAgentsClient agentsClient = new PersistentAgentsClientBuilder()
                .endpoint(projectEndpoint)
                .credential(credential)
                .buildClient();

            // Derive the administration client
            logger.info("Getting PersistentAgentsAdministrationClient");
            PersistentAgentsAdministrationClient adminClient =
                agentsClient.getPersistentAgentsAdministrationClient();

            // Create an agent
            logger.info("Creating agent with name: {}, model: {}", agentName, modelName);
            PersistentAgent agent = adminClient.createAgent(
                new CreateAgentOptions(modelName)
                    .setName(agentName)
                    .setInstructions(instructions)
            );
            logger.info("Agent created: ID={}, Name={}", agent.getId(), agent.getName());
            logger.info("Agent model: {}", agent.getModel());

            // Start a thread/run on the general client
            logger.info("Creating thread and run with agent ID: {}", agent.getId());
            ThreadRun runResult = agentsClient.createThreadAndRun(
                new CreateThreadAndRunOptions(agent.getId())
            );
            logger.info("ThreadRun created: ThreadId={}", runResult.getThreadId());

            // List available getters on ThreadRun for informational purposes
            logger.info("\nAvailable getters on ThreadRun:");
            for (var method : ThreadRun.class.getMethods()) {
                if (method.getName().startsWith("get")) {
                    logger.info(" - {}", method.getName());
                }
            }

            logger.info("\nDemo completed successfully!");
            
        } catch (HttpResponseException e) {
            // Handle service-specific errors with detailed information
            int statusCode = e.getResponse().getStatusCode();
            logger.error("Service error {}: {}", statusCode, e.getMessage());
            logger.error("Refer to the Azure AI Agents documentation for troubleshooting information.");
        } catch (Exception e) {
            // Handle general exceptions
            logger.error("Error in agent sample: {}", e.getMessage(), e);
        }
    }
}
```