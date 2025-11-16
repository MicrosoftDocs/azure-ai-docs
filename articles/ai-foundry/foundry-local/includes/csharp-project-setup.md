---
title: include file
description: include file
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: include
ms.date: 05/19/2025
ms.custom: include file
---

To use Foundry Local in your C# project, you need to set up your project with the appropriate NuGet packages. Depending on your target platform, follow the instructions below to create a new C# console application and add the necessary dependencies.

### [Windows](#tab/windows)

1. Create a new C# project and navigate into it:
    ```bash
    dotnet new console -n app-name
    cd app-name
    ```
1. Open the `app-name.csproj` file and modify to the following:
    ```xml
    <Project Sdk="Microsoft.NET.Sdk">
    
      <PropertyGroup>
        <OutputType>Exe</OutputType>
        <TargetFramework>net8.0-windows10.0.26100</TargetFramework>
        <RootNamespace>app-name</RootNamespace>
        <ImplicitUsings>enable</ImplicitUsings>
        <Nullable>enable</Nullable>
        <WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>
      </PropertyGroup>
    
      <ItemGroup>
        <PackageReference Include="Microsoft.AI.Foundry.Local.WinML" Version="0.8.0" />
        <PackageReference Include="Microsoft.Extensions.Logging" Version="9.0.10" />
        <PackageReference Include="OpenAI" Version="2.5.0" />
      </ItemGroup>
    
    </Project>
    ```
1. Create a `nuget.config` file in the project root with the following content so that the packages restore correctly:
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <configuration>
      <packageSources>
        <clear />
        <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
        <add key="ORT" value="https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/ORT/nuget/v3/index.json" />
      </packageSources>
      <packageSourceMapping>
        <packageSource key="nuget.org">
          <package pattern="*" />
        </packageSource>
        <packageSource key="ORT">
          <package pattern="Microsoft.ML.OnnxRuntime.Foundry" />
        </packageSource>
      </packageSourceMapping>
    </configuration>
    ```

### [Cross-Platform](#tab/xplatform)

1. Create a new C# project and navigate into it:
    ```bash
    dotnet new console -n app-name
    cd app-name
    ```
1. Open the `app-name.csproj` file and modify to the following:
    ```xml
    <Project Sdk="Microsoft.NET.Sdk">
    
        <PropertyGroup>
          <OutputType>Exe</OutputType>
          <TargetFramework>net9.0</TargetFramework>
          <ImplicitUsings>enable</ImplicitUsings>
          <Nullable>enable</Nullable>
        </PropertyGroup>
    
        <ItemGroup>
          <PackageReference Include="Microsoft.AI.Foundry.Local" Version="0.8.0" />
          <PackageReference Include="Microsoft.Extensions.Logging" Version="9.0.10" />
          <PackageReference Include="OpenAI" Version="2.5.0" />
        </ItemGroup>
    
    </Project>
    ```
1. Create a `nuget.config` file in the project root with the following content so that the packages restore correctly:
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <configuration>
      <packageSources>
        <clear />
        <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
        <add key="ORT" value="https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/ORT/nuget/v3/index.json" />
      </packageSources>
      <packageSourceMapping>
        <packageSource key="nuget.org">
          <package pattern="*" />
        </packageSource>
        <packageSource key="ORT">
          <package pattern="Microsoft.ML.OnnxRuntime.Foundry" />
        </packageSource>
      </packageSourceMapping>
    </configuration>
    ```

---
