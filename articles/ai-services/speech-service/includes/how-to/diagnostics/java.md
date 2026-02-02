---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/18/2025
ms.author: pafarley
ms.custom: devx-track-java
---

[!INCLUDE [Introduction](intro.md)]

### Samples

```java
import com.microsoft.cognitiveservices.speech.*;
import com.microsoft.cognitiveservices.speech.diagnostics.logging.EventLogger;
import com.microsoft.cognitiveservices.speech.diagnostics.logging.FileLogger;
import com.microsoft.cognitiveservices.speech.diagnostics.logging.MemoryLogger;

public class SpeechLoggingSamples {
    public static void fileLoggerWithoutFilters()
    {
        FileLogger.start("LogfilePathAndName");

        // Other Speech SDK calls

        FileLogger.stop();
    }

    public static void FileLoggerWithFilters()
    {
        String[] filters = { "YourFirstString", "YourSecondString" };
        FileLogger.setFilters(filters);
        FileLogger.start("LogfilePathAndName");

        // Other Speech SDK calls
        
        FileLogger.stop();
        FileLogger.setFilters();
    }

    public static void memoryLoggerWithoutFilters()
    {
        MemoryLogger.start();

        // Other Speech SDK calls

        // At any time (whether logging is stopped) you can dump the traces in memory to a file
        MemoryLogger.dump("LogfilePathAndName");

        // Or dump to any object that is derived from java.io.Writer. For example, System.out
        MemoryLogger.dump(System.out);

        // Or dump to a list of strings
        List<String> messages = MemoryLogger.dump();

        MemoryLogger.stop();
    }

    public static void eventLoggerWithoutFilters()
    {
        final Object lockObject = new Object();
        List<String> messages = new ArrayList<>();

        // Register a callback that will get invoked by Speech SDK on every new log message
        EventLogger.setCallback((message) -> {
            // Store the message for later processing. Better not processing it in the event thread
            synchronized (lockObject) {
                messages.add(message);
            }
        });

        // Other Speech SDK calls

        // Stop logging by setting an empty callback
        EventLogger.setCallback();
    }
}
```