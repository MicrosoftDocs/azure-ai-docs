---
title: Speech SDK logging - Speech service
titleSuffix: Foundry Tools
description: Learn about how to enable logging in the Speech SDK (C++, C#, Python, Objective-C, Java).
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 08/07/2025
zone_pivot_groups: programming-languages-set-two-objective-c
ms.custom: devx-track-csharp, devx-track-extended-java, devx-track-python
#Customer intent: As a developer, I want to learn how to enable logging in the Speech SDK so that I can get additional information and diagnostics from the Speech SDK's core components.
---

# Enable logging in the Speech SDK

Logging to file is an optional feature for the Speech SDK. During development, logging provides additional information and diagnostics from the Speech SDK's core components. Logging is handled by static classes in Speech SDK's native library. All instances in the same process write log entries to the same log file.

## Use the logging API

The recommended way to enable logging is to use the static logger classes available in Speech SDK version 1.43.0 and later. The logging API provides three types of loggers:

- **File logger**: Writes log messages directly to a file. This is the simplest logging solution and is suitable for diagnosing most on-device issues.
- **Memory logger**: Stores log messages in a fixed 2-MB ring buffer in memory. You can dump the buffer contents to a file or stream at any time. This is suitable for diagnosing issues that occur in a short period of time.
- **Event logger**: Sends log messages to an event handler that you provide. This is suitable when you need to integrate Speech SDK logs with your existing logging collection system.

These loggers are process-wide constructs. If you have multiple speech recognizer objects running in parallel, there's one shared log containing interleaved log lines from all recognizers. You can use the File logger, Memory logger, and Event logger simultaneously in the same process.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C# include](includes/how-to/diagnostics/csharp.md)]
::: zone-end

::: zone pivot="programming-language-cpp"
[!INCLUDE [C++ include](includes/how-to/diagnostics/cpp.md)]
::: zone-end

::: zone pivot="programming-language-java"
[!INCLUDE [Java include](includes/how-to/diagnostics/java.md)]
::: zone-end

::: zone pivot="programming-language-objectivec"
[!INCLUDE [ObjectiveC include](includes/how-to/diagnostics/objectivec.md)]
::: zone-end

::: zone pivot="programming-language-python"
[!INCLUDE [Python include](./includes/how-to/diagnostics/python.md)]
::: zone-end

### JavaScript

For JavaScript, logging is enabled via SDK diagnostics:

```javascript
sdk.Diagnostics.SetLoggingLevel(sdk.LogLevel.Debug);
sdk.Diagnostics.SetLogOutputPath("LogfilePathAndName");
```

## Log file locations by platform

When using `FileLogger.Start()` or `MemoryLogger.Dump()`, you need to provide a file path. The path requirements vary by platform.

For Windows or Linux, the log file can be in any path the user has write permission for. Write permissions to file system locations in other operating systems might be limited or restricted by default.

### Universal Windows Platform (UWP)

UWP applications need to place log files in one of the application data locations (local, roaming, or temporary). A log file can be created in the local application folder:

```csharp
StorageFolder storageFolder = ApplicationData.Current.LocalFolder;
StorageFile logFile = await storageFolder.CreateFileAsync("logfile.txt", CreationCollisionOption.ReplaceExisting);
FileLogger.Start(logFile.Path);
```

Within a Unity UWP application, a log file can be created using the application persistent data path folder as follows:

```csharp
#if ENABLE_WINMD_SUPPORT
    string logFile = Application.persistentDataPath + "/logFile.txt";
    FileLogger.Start(logFile);
#endif
```

For more about file access permissions in UWP applications, see [File access permissions](/windows/uwp/files/file-access-permissions).

### Android

You can save a log file to either internal storage, external storage, or the cache directory. Files created in the internal storage or the cache directory are private to the application. It's preferable to create a log file in external storage.

```java
File dir = context.getExternalFilesDir(null);
File logFile = new File(dir, "logfile.txt");
FileLogger.start(logFile.getAbsolutePath());
```

The code saves a log file to the external storage in the root of an application-specific directory. A user can access the file with the file manager (usually in `Android/data/ApplicationName/logfile.txt`). The file is deleted when the application is uninstalled.

You also need to request `WRITE_EXTERNAL_STORAGE` permission in the manifest file:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="...">
  ...
  <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
  ...
</manifest>
```

Within a Unity Android application, the log file can be created using the application persistent data path folder as follows:

```csharp
string logFile = Application.persistentDataPath + "/logFile.txt";
FileLogger.Start(logFile);
```

In addition, you need to set write permission in your Unity Player settings for Android to "External (SDCard)". The log is written to a directory that you can get by using a tool such as AndroidStudio Device File Explorer. The exact directory path can vary between Android devices. The location is typically the `sdcard/Android/data/your-app-packagename/files` directory.

For more information about data and file storage for Android applications, see [Data and file storage overview](https://developer.android.com/guide/topics/data/data-storage.html).

### iOS

Only directories inside the application sandbox are accessible. Files can be created in the documents, library, and temp directories. Files in the documents directory can be made available to a user.

If you're using Objective-C on iOS, use the following code snippet to create a log file in the application document directory:

```objc
NSString *filePath = [
  [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject]
    stringByAppendingPathComponent:@"logfile.txt"];
[SPXFileLogger start:filePath];
```

To access a created file, add the following properties to the `Info.plist` property list of the application:

```xml
<key>UIFileSharingEnabled</key>
<true/>
<key>LSSupportsOpeningDocumentsInPlace</key>
<true/>
```

If you're using Swift on iOS, use the following code snippet to enable logs:

```swift
let documentsDirectoryPathString = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true).first!
let documentsDirectoryPath = NSURL(string: documentsDirectoryPathString)!
let logFilePath = documentsDirectoryPath.appendingPathComponent("swift.log")
SPXFileLogger.start(logFilePath!.absoluteString)
```

For more information about iOS file systems, see [File System Programming Guide](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html).

## Legacy approach: set property on configuration object

You can also enable logging by setting the `Speech_LogFilename` property on a speech configuration object. This approach is less flexible than using the static logger classes.

Taking the `SpeechConfig` as an example and assuming that you created an instance called `speechConfig`:

```csharp
speechConfig.SetProperty(PropertyId.Speech_LogFilename, "LogfilePathAndName");
```

```java
speechConfig.setProperty(PropertyId.Speech_LogFilename, "LogfilePathAndName");
```

```C++
speechConfig->SetProperty(PropertyId::Speech_LogFilename, "LogfilePathAndName");
```

```Python
speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "LogfilePathAndName")
```

```objc
[speechConfig setPropertyTo:@"LogfilePathAndName" byId:SPXSpeechLogFilename];
```

```go
import ("github.com/Microsoft/cognitive-services-speech-sdk-go/common")

speechConfig.SetProperty(common.SpeechLogFilename, "LogfilePathAndName")
```

You can create a recognizer from the configuration object. This enables logging for all recognizers.

> [!NOTE]
> If you create a `SpeechSynthesizer` from the configuration object, it doesn't enable logging. If logging is enabled though, you also receive diagnostics from the `SpeechSynthesizer`.

For platform-specific file path guidance, see [Log file locations by platform](#log-file-locations-by-platform). The same path requirements apply when using the property approach.

### Logging with multiple recognizers

When using the legacy property approach, a log file output path is specified as a configuration property into a `SpeechRecognizer` or other SDK object. However, SDK logging is a singleton, process-wide facility with no concept of individual instances. You can think of this as the `SpeechRecognizer` constructor (or similar) implicitly calling a static and internal "Configure Global Logging" routine with the property data available in the corresponding `SpeechConfig`.

This means that you can't, as an example, configure six parallel recognizers to output simultaneously to six separate files. Instead, the latest recognizer created will configure the global logging instance to output to the file specified in its configuration properties and all SDK logging is emitted to that file.

This also means that the lifetime of the object that configured logging isn't tied to the duration of logging. Logging won't stop in response to the release of an SDK object and will continue as long as no new logging configuration is provided. Once started, process-wide logging can be stopped by setting the log file path to an empty string when creating a new object.

To reduce potential confusion when configuring logging for multiple instances, it might be useful to abstract control of logging from objects doing real work. An example pair of helper routines:

```cpp
void EnableSpeechSdkLogging(const char* relativePath)
{
	auto configForLogging = SpeechConfig::FromSubscription("unused_key", "unused_region");
	configForLogging->SetProperty(PropertyId::Speech_LogFilename, relativePath);
	auto emptyAudioConfig = AudioConfig::FromStreamInput(AudioInputStream::CreatePushStream());
	auto temporaryRecognizer = SpeechRecognizer::FromConfig(configForLogging, emptyAudioConfig);
}

void DisableSpeechSdkLogging()
{
	EnableSpeechSdkLogging("");
}
```

## Next steps

> [!div class="nextstepaction"]
> [Explore our samples on GitHub](https://aka.ms/csspeech/samples)
