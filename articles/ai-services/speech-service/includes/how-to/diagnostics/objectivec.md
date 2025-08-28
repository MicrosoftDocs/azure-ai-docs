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

```Objective-C

- (void)fileLoggerWithoutFilters {
    NSString *logFileName = @"speech_sdk.log";
    NSString *logFile = [[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject]
                         stringByAppendingPathComponent:logFileName];
    [SPXFileLogger start:logFile];
    
    // Other Speech SDK calls

    [SPXFileLogger stop];
}

- (void)fileLoggerWithFilters {
    NSString *logFileName = @"speech_sdk.log";
    NSString *logFile = [[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject]
                         stringByAppendingPathComponent:logFileName];
    NSArray *filters = @[@"YourFirstString", @"YourSecondString"];
    [SPXFileLogger setFilters:filters];
    [SPXFileLogger start:logFile];
    
    // Other Speech SDK calls

    [SPXFileLogger stop];
    [SPXFileLogger setFilters:nil];
}

- (void)memoryLoggerWithoutFilters {
    NSString *logFileName = @"speech_sdk.log";
    NSString *logFile = [[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject]
                         stringByAppendingPathComponent:logFileName];

    [SPXMemoryLogger start];
    
    // Other Speech SDK calls

    // At any time (whether logging is stopped) you can dump the traces in memory to a file
    [SPXMemoryLogger dumpToFile:logFile];

    [SPXMemoryLogger stop];
}

- (void)eventLoggingWithoutFilters {
    __block NSMutableArray *eventMsgs = [NSMutableArray array];

    // Register a callback that will get invoked by Speech SDK on every new log message
    [SPXEventLogger setCallback:^(NSString *message) {
        @synchronized(self) {
            [eventMsgs addObject:message];
        }
    }];
    
    // Other Speech SDK calls

    // Stop event logging 
    [SPXEventLogger setCallback:nil];
}
```
