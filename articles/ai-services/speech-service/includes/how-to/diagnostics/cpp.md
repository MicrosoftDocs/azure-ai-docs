---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/18/2025
ms.author: pafarley
---

[!INCLUDE [Introduction](intro.md)]

### Samples

```cpp
using namespace Microsoft::CognitiveServices::Speech;
using namespace Microsoft::CognitiveServices::Speech::Diagnostics::Logging;

void FileLoggerWithoutFilters()
{
    FileLogger::Start("LogfilePathAndName");

    // Other Speech SDK calls

    FileLogger::Stop();
}

void FileLoggerWithFilters()
{
    std::initializer_list<std::string> filters = { "YourFirstString", "YourSecondString" };
    FileLogger::SetFilters(filters);
    FileLogger::Start("LogfilePathAndName");

    // Other Speech SDK calls
    
    FileLogger::Stop();
    FileLogger::SetFilters();
}

void MemoryLoggerWithoutFilters()
{
    MemoryLogger::Start();

    // Other Speech SDK calls

    // At any time (whether logging is stopped) you can dump the traces in memory to a file
    MemoryLogger::Dump("LogfilePathAndName");

    // Or dump to any stream object that is derived from std::ostream. For example, std::cout
    MemoryLogger::Dump(std::cout);

    // Or dump to a vector of strings
    std::vector<std::string> messages = MemoryLogger::Dump();

    MemoryLogger::Stop();
}

void EventLoggerWithoutFilters()
{
    std::mutex mtx;
    std::vector<std::string> messages;

    // Register a callback that will get invoked by Speech SDK on every new log message
    EventLogger::SetCallback([&messages, &mtx](std::string message) {
        // Store the message for later processing. Better not processing it in the event thread
        std::unique_lock<std::mutex> lock(mtx);
        messages.push_back(message);
    });

    // Other Speech SDK calls

    // Stop logging by setting an empty callback
    EventLogger::SetCallback();
}
```
