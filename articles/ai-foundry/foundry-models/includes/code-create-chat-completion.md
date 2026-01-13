---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
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
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Explain Riemann's conjecture in 1 paragraph"),
    ],
    model="mistral-large"
)

print(response.choices[0].message.content)
```

# [JavaScript](#tab/javascript)

```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: "Explain Riemann's conjecture in 1 paragraph" },
];

var response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        model: "mistral-large"
    }
});

console.log(response.body.choices[0].message.content)
```

# [C#](#tab/csharp)

```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("Explain Riemann's conjecture in 1 paragraph")
    },
    Model = "mistral-large"
};

response = client.Complete(requestOptions);
Console.WriteLine($"Response: {response.Value.Content}");
```

# [Java](#tab/java)

```java
List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant"));
chatMessages.add(new ChatRequestUserMessage("Explain Riemann's conjecture in 1 paragraph"));

ChatCompletions chatCompletions = client.complete(new ChatCompletionsOptions(chatMessages));

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
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": "Explain Riemann's conjecture in 1 paragraph"
        }
    ],
    "model": "mistral-large"
}
```

---
