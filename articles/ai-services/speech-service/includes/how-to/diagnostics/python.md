---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/18/2025
ms.author: pafarley
---

[!INCLUDE [Introduction](intro.md)]

### Samples

```Python
import azure.cognitiveservices.speech as speechsdk
import azure.cognitiveservices.speech.diagnostics.logging as speechsdk_logging


def file_logger_without_filters():
    speechsdk_logging.FileLogger.start("LogfilePathAndName")
    # Other Speech SDK calls
    speechsdk_logging.FileLogger.stop()


def file_logger_with_filters():
    filters = { "YourFirstString", "YourSecondString" }
    speechsdk_logging.FileLogger.set_filters(filters)
    speechsdk_logging.FileLogger.start("LogfilePathAndName")
    # Other Speech SDK calls
    speechsdk_logging.FileLogger.stop()
    speechsdk_logging.FileLogger.set_filters()


def memory_logger_without_filter():
    speechsdk_logging.MemoryLogger.start()
    #
    # Other Speech SDK calls
    #
    # At any time (whether logging is stopped) you can dump the traces in memory to a file
    speechsdk_logging.MemoryLogger.dump("LogfilePathAndName")
    # Or dump to any object that is derived from IOBase. For example, sys.stdout
    speechsdk_logging.MemoryLogger.dump_to_stream(sys.stdout)
    # Or dump to a list of strings
    messages = speechsdk_logging.MemoryLogger.dump_to_list()
    speechsdk_logging.MemoryLogger.stop()


def event_logger_without_filter():
    messages = []
    lock = threading.Lock()
    # Register a callback that will get invoked by Speech SDK on every new log message
    def on_log(msg):
        with lock:
            # Store the message for later processing. Better not processing it in the event thread
            messages.append(msg)
    speechsdk_logging.EventLogger.set_callback(on_log)
    #
    # Other Speech SDK calls
    #
    # Stop logging by setting an empty callback
    speechsdk_logging.EventLogger.set_callback()
```
