---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/18/2025
ms.author: pafarley
ms.custom: devx-track-csharp
---

[!INCLUDE [Introduction](intro.md)]

### Samples

```csharp
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Diagnostics.Logging;

class Program 
{
    public static void FileLoggerWithoutFilters()
    {
        FileLogger.Start("LogfilePathAndName");

        // Other Speech SDK calls

        FileLogger.Stop();
    }

    public static void FileLoggerWithFilters()
    {
        string[] filters = { "YourFirstString", "YourSecondString" };
        FileLogger.SetFilters(filters);
        FileLogger.Start("LogfilePathAndName");

        // Other Speech SDK calls
        
        FileLogger.Stop();
        FileLogger.SetFilters();
    }

    public static void MemoryLoggerWithoutFilters()
    {
        MemoryLogger.Start();

        // Other Speech SDK calls

        // At any time (whether logging is stopped) you can dump the traces in memory to a file
        MemoryLogger.Dump("LogfilePathAndName");

        // Or dump to any object that is derived from System.IO.TextWriter. For example, System.Console.Out
        MemoryLogger.Dump(System.Console.Out);

        // Or dump to a vector of strings
        List<string> messages = MemoryLogger.Dump().ToList<string>();

        MemoryLogger.Stop();
    }

    // These variables and method are used by the EvenLogger sample below.
    private static readonly object lockObject = new object();
    private static List<string> eventMessages = new List<string>();
    private static void OnMessageEvent(object sender, string message)
    {
        lock (lockObject)
        {
            // Store the message for later processing. Better not processing it in the event thread
            eventMessages.Add(message);
        }
    }

    public static void EventLoggerWithoutFilters()
    {
        // Subscribe an event that will get invoked by Speech SDK on every new log message
        EventLogger.OnMessage += OnMessageEvent;

        // Other Speech SDK calls

        // Unsubscribe to stop getting events
        EventLogger.OnMessage -= OnMessageEvent;
    }
}
```
