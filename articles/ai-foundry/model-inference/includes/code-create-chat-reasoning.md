---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

# [Python](#tab/python)

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        UserMessage(content="How many languages are in the world?"),
    ],
    model="DeepSeek-R1"
)

print(response.choices[0].message.content)
```

# [JavaScript](#tab/javascript)

```javascript
var messages = [
    { role: "user", content: "How many languages are in the world?" },
];

var response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        model: "DeepSeek-R1"
    }
});

console.log(response.choices[0].message.content)
```

# [C#](#tab/csharp)

```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestUserMessage("How many languages are in the world?")
    },
    Model = "DeepSeek-R1"
};

response = client.Complete(requestOptions);
Console.WriteLine($"Response: {response.Value.Content}");
```

# [Java](#tab/java)

```java
List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestUserMessage("How many languages are in the world?"));

ChatCompletions chatCompletions = client.complete(new ChatCompletionsOptions(chatMessages, "DeepSeek-R1"));

for (ChatChoice choice : chatCompletions.getChoices()) {
    ChatResponseMessage message = choice.getMessage();
    System.out.println("Response:" + message.getContent());
}
```

# [REST](#tab/rest)

__Request__

```HTTP/1.1
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
api-key: <api-key>
Content-Type: application/json
```

```JSON
{
    "messages": [
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ],
    "model": "DeepSeek-R1"
}
```

---
