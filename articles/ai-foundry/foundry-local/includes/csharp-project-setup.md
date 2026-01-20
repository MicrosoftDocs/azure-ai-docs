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
    
      <ItemGroup>
        <PackageReference Include="Microsoft.AI.Foundry.Local.WinML" Version="0.8.2.1" />
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
          <package pattern="*Foundry*" />
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
1. Open and edit the `app-name.csproj` file to:
    ```xml
    <Project Sdk="Microsoft.NET.Sdk">
    
        <PropertyGroup>
          <OutputType>Exe</OutputType>
          <TargetFramework>net9.0</TargetFramework>
          <ImplicitUsings>enable</ImplicitUsings>
          <Nullable>enable</Nullable>
        </PropertyGroup>
    
        <ItemGroup>
          <PackageReference Include="Microsoft.AI.Foundry.Local" Version="0.8.2.1" />
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
          <package pattern="*Foundry*" />
        </packageSource>
      </packageSourceMapping>
    </configuration>
    ```

---
