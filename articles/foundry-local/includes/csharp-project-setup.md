---
title: Include file
description: Include file
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 05/19/2025
ms.custom: include file
---

Use Foundry Local in your C# project by following these Windows-specific or Cross-Platform (macOS/Linux/Windows) instructions:

### [Windows](#tab/windows)

1. Create a new C# project and navigate into it:
    ```bash
    dotnet new console -n app-name
    cd app-name
    ```
1. Open and edit the `app-name.csproj` file to:
    ```xml
    <Project Sdk="Microsoft.NET.Sdk">
    
      <PropertyGroup>
        <OutputType>Exe</OutputType>
        <TargetFramework>net9.0-windows10.0.26100</TargetFramework>
        <RootNamespace>app-name</RootNamespace>
        <ImplicitUsings>enable</ImplicitUsings>
        <Nullable>enable</Nullable>
        <WindowsAppSDKSelfContained>false</WindowsAppSDKSelfContained>
        <WindowsPackageType>None</WindowsPackageType>
        <EnableCoreMrtTooling>false</EnableCoreMrtTooling>
      </PropertyGroup>

      <PropertyGroup Condition="'$(RuntimeIdentifier)'==''">
        <RuntimeIdentifier>$(NETCoreSdkRuntimeIdentifier)</RuntimeIdentifier>
      </PropertyGroup>
    
      <ItemGroup>
        <PackageReference Include="Microsoft.AI.Foundry.Local.WinML" Version="1.0.0" />
        <PackageReference Include="Microsoft.Extensions.Logging" Version="9.0.10" />
        <PackageReference Include="OpenAI" Version="2.5.0" />
      </ItemGroup>
    
    </Project>
    ```

### [Cross-Platform](#tab/xplatform)

1. Create a new C# project and navigate into it:
    ```bash
    dotnet new console -n app-name
    cd app-name
    ```
1. Open and edit the `app-name.csproj` file to:
    ```xml
    <Project Sdk="Microsoft.NET.Sdk">
    
        <PropertyGroup>
          <OutputType>Exe</OutputType>
          <TargetFramework>net9.0</TargetFramework>
          <ImplicitUsings>enable</ImplicitUsings>
          <Nullable>enable</Nullable>
        </PropertyGroup>

        <PropertyGroup Condition="'$(RuntimeIdentifier)'==''">
            <RuntimeIdentifier>$(NETCoreSdkRuntimeIdentifier)</RuntimeIdentifier>
        </PropertyGroup>
    
        <ItemGroup>
          <PackageReference Include="Microsoft.AI.Foundry.Local" Version="1.0.0" />
          <PackageReference Include="Microsoft.Extensions.Logging" Version="9.0.10" />
          <PackageReference Include="OpenAI" Version="2.5.0" />
        </ItemGroup>
    
    </Project>
    ```

---

> [!NOTE]
> The Microsoft.AI.Foundry.Local NuGet package targets net8.0. With .NET's forward compatibility, it works seamlessly in projects targeting .NET 9, .NET 10, and later—no other configuration needed. The SDK uses only .NET 8 APIs and contains no framework-specific code paths, so behavior is identical regardless of which runtime your app targets. We target .NET 8 as it's the current Long Term Support (LTS) release with the broadest install base.
