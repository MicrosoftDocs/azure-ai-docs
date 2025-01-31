## Getting started

# [Microsoft Entra ID](#tab/dotnet-entra-id)

```csharp

```

# [Key-based auth](#tab/dotnet-keys)

```csharp

```

---

## Function calling with structured outputs

Structured Outputs for function calling can be enabled with a single parameter, by supplying `strict: true`. 

> [!NOTE]
> Structured outputs are not supported with parallel function calls. When using structured outputs set `parallel_tool_calls` to `false`.

# [Microsoft Entra ID](#tab/dotnet-entra-id)

```csharp

```

# [Key-based auth](#tab/dotnet-keys)

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using Newtonsoft.Json.Schema;
using Newtonsoft.Json.Schema.Generation;
using OpenAI.Assistants;
using OpenAI.Chat;
using OpenAI.Files;
using System;
using System.ClientModel;
using System.Text;
using System.Text.Json;

string GetTemperature(string location, string date)
{
    // Call the weather API here.
    if(location == "Seattle" && date == "2025-06-01")
    {
        return "45";
    }

    return "50";
}

ChatTool GetTemperatureTool = ChatTool.CreateFunctionTool(
    functionName: nameof(GetTemperature),
    functionSchemaIsStrict: true,
    functionDescription: "Get the projected temperature by date and location.",
    functionParameters: BinaryData.FromBytes("""
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location of the weather."
                },
                "date": {
                    "type": "string",
                    "description": "The date of the projected weather."
                }
            },
            "required": ["location", "date"],
            "additionalProperties": false  
        }
        """u8.ToArray())
);

AzureOpenAIClient openAIClient = new(new Uri(""), new ApiKeyCredential(""));

var chat = new List<ChatMessage>()
    {
         new SystemChatMessage("Extract the event information and projected weather."),
         new UserChatMessage("Alice and Bob are going to a science fair in Seattle on June 1st, 2025.")
    };

JSchemaGenerator generator = new JSchemaGenerator();
var schema = generator.Generate(typeof(CalendarEvent));
string jsonSchema = schema.ToString();

var json = Encoding.UTF8.GetBytes(schema.ToString());

var client = openAIClient.GetChatClient("gpt-4o");

bool requiresAction;

do
{
    requiresAction = false;
    var completion = client.CompleteChat(
        chat,
        new ChatCompletionOptions()
        {
            ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
                "calenderEvent",
                BinaryData.FromString(jsonSchema)),
            Tools = { GetTemperatureTool }
        });

    switch (completion.Value.FinishReason)
    {
        case ChatFinishReason.Stop:
            {
                // Add the assistant message to the conversation history.
                chat.Add(new AssistantChatMessage(completion));
                Console.WriteLine(completion.Value.Content[0].Text);
                break;
            }

        case ChatFinishReason.ToolCalls:
            {
                // First, add the assistant message with tool calls to the conversation history.
                chat.Add(new AssistantChatMessage(completion));

                // Then, add a new tool message for each tool call that is resolved.
                foreach (ChatToolCall toolCall in completion.Value.ToolCalls)
                {
                    switch (toolCall.FunctionName)
                    {
                        case nameof(GetTemperature):
                            {
                                using JsonDocument argumentsJson = JsonDocument.Parse(toolCall.FunctionArguments);
                                bool hasLocation = argumentsJson.RootElement.TryGetProperty("location", out JsonElement location);
                                bool hasDate = argumentsJson.RootElement.TryGetProperty("date", out JsonElement date);

                                if (!hasLocation || !hasDate)
                                {
                                    throw new ArgumentNullException(nameof(location), "The location and date arguments are required.");
                                }

                                string toolResult = GetTemperature(location.GetString(), date.GetString());
                                chat.Add(new ToolChatMessage(toolCall.Id, toolResult));
                                break;
                            }

                        default:
                            {
                                // Handle other unexpected calls.
                                throw new NotImplementedException();
                            }
                    }
                }

                requiresAction = true;
                break;
            }

        case ChatFinishReason.Length:
            throw new NotImplementedException("Incomplete model output due to MaxTokens parameter or token limit exceeded.");

        case ChatFinishReason.ContentFilter:
            throw new NotImplementedException("Omitted content due to a content filter flag.");

        case ChatFinishReason.FunctionCall:
            throw new NotImplementedException("Deprecated in favor of tool calls.");

        default:
            throw new NotImplementedException(completion.Value.FinishReason.ToString());
    }

} while (requiresAction);


public class CalendarEvent()
{
    public string Name { get; set; }
    public string Date { get; set; }
    public string Temperature { get; set; }
    public List<string> Participants { get; set; }
}
```
