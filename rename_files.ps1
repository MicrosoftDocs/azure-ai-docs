cd 'c:\git\azure-ai-docs-pr'

$renames = @(
    @{ old = 'articles\ai-foundry\what-is-azure-ai-foundry.md'; new = 'articles\ai-foundry\what-is-foundry.md' },
    @{ old = 'articles\ai-foundry\whats-new-azure-ai-foundry.md'; new = 'articles\ai-foundry\whats-new-foundry.md' },
    @{ old = 'articles\ai-foundry\concepts\rbac-azure-ai-foundry.md'; new = 'articles\ai-foundry\concepts\rbac-foundry.md' },
    @{ old = 'articles\ai-foundry\concepts\hub-rbac-azure-ai-foundry.md'; new = 'articles\ai-foundry\concepts\hub-rbac-foundry.md' },
    @{ old = 'articles\ai-services\connect-services-ai-foundry-portal.md'; new = 'articles\ai-services\connect-services-foundry-portal.md' },
    @{ old = 'articles\ai-foundry\azure-ai-foundry-status-dashboard-documentation.md'; new = 'articles\ai-foundry\foundry-status-dashboard-documentation.md' },
    @{ old = 'articles\ai-foundry\openai\includes\audio-completions-ai-foundry.md'; new = 'articles\ai-foundry\openai\includes\audio-completions-foundry.md' }
)

foreach ($item in $renames) {
    $oldPath = Join-Path $PSScriptRoot $item.old
    $newPath = Join-Path $PSScriptRoot $item.new
    
    if (Test-Path $oldPath) {
        Move-Item -Path $oldPath -Destination $newPath -Force
        Write-Host "✓ Renamed: $($item.old) -> $($item.new)"
    } else {
        Write-Host "✗ NOT FOUND: $($item.old)"
    }
}

Write-Host "`nDone!"
