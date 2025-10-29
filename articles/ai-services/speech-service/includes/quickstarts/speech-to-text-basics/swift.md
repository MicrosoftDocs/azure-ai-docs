---
author: PatrickFarley
ms.service: azure-ai-speech
ms.custom:
  - build-2024
ms.topic: include
ms.date: 7/16/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/swift.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Set up the environment

The Speech SDK for Swift is distributed as a framework bundle. The framework supports both Objective-C and Swift on both iOS and macOS.

The Speech SDK can be used in Xcode projects as a [CocoaPod](https://cocoapods.org/), or [downloaded directly](https://aka.ms/csspeech/macosbinary) and linked manually. This guide uses a CocoaPod. Install the CocoaPod dependency manager as described in its [installation instructions](https://guides.cocoapods.org/using/getting-started.html).

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables.md)]

## Recognize speech from a microphone

Follow these steps to recognize speech in a macOS application.

1. Clone the [Azure-Samples/cognitive-services-speech-sdk](https://github.com/Azure-Samples/cognitive-services-speech-sdk) repository to get the [Recognize speech from a microphone in Swift on macOS](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/quickstart/swift/macos/from-microphone) sample project. The repository also has iOS samples.
1. Navigate to the directory of the downloaded sample app (`helloworld`) in a terminal.
1. Run the command `pod install`. This command generates a `helloworld.xcworkspace` Xcode workspace containing both the sample app and the Speech SDK as a dependency.
1. Open the `helloworld.xcworkspace` workspace in Xcode.
1. Open the file named *AppDelegate.swift* and locate the `applicationDidFinishLaunching` and `recognizeFromMic` methods as shown here.

   ```swift
   import Cocoa

   @NSApplicationMain
   class AppDelegate: NSObject, NSApplicationDelegate {
       var label: NSTextField!
       var fromMicButton: NSButton!

       var sub: String!
       var region: String!

       @IBOutlet weak var window: NSWindow!

       func applicationDidFinishLaunching(_ aNotification: Notification) {
           print("loading")
           // load subscription information
           sub = ProcessInfo.processInfo.environment["SPEECH_KEY"]
           region = ProcessInfo.processInfo.environment["SPEECH_REGION"]

           label = NSTextField(frame: NSRect(x: 100, y: 50, width: 200, height: 200))
           label.textColor = NSColor.black
           label.lineBreakMode = .byWordWrapping

           label.stringValue = "Recognition Result"
           label.isEditable = false

           self.window.contentView?.addSubview(label)

           fromMicButton = NSButton(frame: NSRect(x: 100, y: 300, width: 200, height: 30))
           fromMicButton.title = "Recognize"
           fromMicButton.target = self
           fromMicButton.action = #selector(fromMicButtonClicked)
           self.window.contentView?.addSubview(fromMicButton)
       }

       @objc func fromMicButtonClicked() {
           DispatchQueue.global(qos: .userInitiated).async {
               self.recognizeFromMic()
           }
       }

       func recognizeFromMic() {
           var speechConfig: SPXSpeechConfiguration?
           do {
               try speechConfig = SPXSpeechConfiguration(subscription: sub, region: region)
           } catch {
               print("error \(error) happened")
               speechConfig = nil
           }
           speechConfig?.speechRecognitionLanguage = "en-US"

           let audioConfig = SPXAudioConfiguration()

           let reco = try! SPXSpeechRecognizer(speechConfiguration: speechConfig!, audioConfiguration: audioConfig)

           reco.addRecognizingEventHandler() {reco, evt in
               print("intermediate recognition result: \(evt.result.text ?? "(no result)")")
               self.updateLabel(text: evt.result.text, color: .gray)
           }

           updateLabel(text: "Listening ...", color: .gray)
           print("Listening...")

           let result = try! reco.recognizeOnce()
           print("recognition result: \(result.text ?? "(no result)"), reason: \(result.reason.rawValue)")
           updateLabel(text: result.text, color: .black)

           if result.reason != SPXResultReason.recognizedSpeech {
               let cancellationDetails = try! SPXCancellationDetails(fromCanceledRecognitionResult: result)
               print("cancelled: \(result.reason), \(cancellationDetails.errorDetails)")
               print("Did you set the speech resource key and region values?")
               updateLabel(text: "Error: \(cancellationDetails.errorDetails)", color: .red)
           }
       }

       func updateLabel(text: String?, color: NSColor) {
           DispatchQueue.main.async {
               self.label.stringValue = text!
               self.label.textColor = color
           }
       }
   }
   ```

1. In *AppDelegate.m*, use the [environment variables that you previously set](#set-environment-variables) for your Speech resource key and region.

   ```swift
   sub = ProcessInfo.processInfo.environment["SPEECH_KEY"]
   region = ProcessInfo.processInfo.environment["SPEECH_REGION"]
   ```

1. To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md). For example, use `es-ES` for Spanish (Spain). If you don't specify a language, the default is `en-US`. For details about how to identify one of multiple languages that might be spoken, see [Language identification](~/articles/ai-services/speech-service/language-identification.md).
1. To make the debug output visible, select **View** > **Debug Area** > **Activate Console**.
1. Build and run the example code by selecting **Product** > **Run** from the menu or selecting the **Play** button.

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `SPEECH_REGION` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

After you select the button in the app and say a few words, you should see the text that you spoke on the lower part of the screen. When you run the app for the first time, it prompts you to give the app access to your computer's microphone.

## Remarks

This example uses the `recognizeOnce` operation to transcribe utterances of up to 30 seconds, or until silence is detected. For information about continuous recognition for longer audio, including multi-lingual conversations, see [How to recognize speech](~/articles/ai-services/speech-service/how-to-recognize-speech.md).

## Objective-C

The Speech SDK for Objective-C shares client libraries and reference documentation with the Speech SDK for Swift. For Objective-C code examples, see the [recognize speech from a microphone in Objective-C on macOS](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/quickstart/objectivec/macos/from-microphone) sample project in GitHub.

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
