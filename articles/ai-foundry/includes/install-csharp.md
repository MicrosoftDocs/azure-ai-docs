---
title: include file
description: include file
author: pablolopes
ms.reviewer: pablolopes
ms.author: pablolopes
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/30/2025
ms.custom: include, build-2025
---

Ensure you have the necessary tools installed for .NET development.

### Install the .NET SDK

You need the .NET SDK (Software Development Kit) to create, build, and run .NET applications. We recommend installing the latest LTS (Long Term Support) version or a later version if required by your project.

1. Download the .NET SDK from the [official .NET download page](https://dotnet.microsoft.com/download). Select the appropriate installer for your operating system (Windows, Linux, or macOS).
1. Follow the installation instructions for your operating system.
1. Verify the installation by opening a terminal or command prompt and running:

    ```bash
    dotnet --version
    ```

    The response should be the installed SDK version.

### Install the C# Dev Kit for Visual Studio Code

For the best C# development experience in VS Code, install the official C# Dev Kit extension:

1. Open Visual Studio Code.
1. Go to the Extensions view (Ctrl+Shift+X or Cmd+Shift+X).
1. Search for **C# Dev Kit**.
1. Install the extension published by Microsoft. This will also install the base C# extension if you don't already have it.

### Create a new .NET Project

You can create a new .NET project using the terminal integrated into Visual Studio Code (Terminal > New Terminal).

For example, to create a new console application:

```bash
# Navigate to the directory where you want to create your project
# cd path/to/your/projects

# Create a new console application in a subfolder named MyConsoleApp
dotnet new console -o MyConsoleApp

# Navigate into the newly created project folder
cd MyConsoleApp
```

You can now open this `MyConsoleApp` folder in VS Code (File > Open Folder...) to start working on your C# project. VS Code, with the C# Dev Kit extension, will automatically detect the project, enabling features like IntelliSense, debugging, and build tasks.