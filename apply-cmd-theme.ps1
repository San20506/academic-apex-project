# Academic Apex CMD Theme Application Script
# Run this script as Administrator to apply the theme to Windows Command Prompt
# Author: Academic Apex Project
# Version: 1.0.0

param(
    [switch]$Force,
    [switch]$Backup
)

# Color scheme based on Academic Apex Slider Theme
$ThemeColors = @{
    'ColorTable00' = 0x1a1a1a  # Black (Background) - Dark theme base
    'ColorTable01' = 0x4a9eff  # Blue (Accent) - Primary accent color
    'ColorTable02' = 0x4caf50  # Green (Success) - Success messages
    'ColorTable03' = 0x00d4aa  # Cyan (Info) - Information highlights
    'ColorTable04' = 0xf44336  # Red (Error) - Error messages
    'ColorTable05' = 0x9c27b0  # Magenta - Special highlights
    'ColorTable06' = 0xff9800  # Yellow (Warning) - Warning messages
    'ColorTable07' = 0xffffff  # White (Text) - Primary text color
    'ColorTable08' = 0x555555  # Bright Black - Muted text
    'ColorTable09' = 0x6ec6ff  # Bright Blue - Bright accent
    'ColorTable10' = 0x81c784  # Bright Green - Bright success
    'ColorTable11' = 0x4dd0e1  # Bright Cyan - Bright info
    'ColorTable12' = 0xe57373  # Bright Red - Bright error
    'ColorTable13' = 0xba68c8  # Bright Magenta - Bright special
    'ColorTable14' = 0xffb74d  # Bright Yellow - Bright warning
    'ColorTable15' = 0xffffff  # Bright White - Brightest text
}

$ThemeSettings = @{
    'ScreenColors' = 0x07       # White text on black background
    'PopupColors' = 0x17        # White text on blue background
    'FontFamily' = 0x36         # TrueType font family (Consolas)
    'FontSize' = 0x000c0000     # Font size (12pt)
    'FontWeight' = 0x190        # Normal weight (400)
    'CursorSize' = 0x19         # Cursor size (25%)
    'HistoryBufferSize' = 0x32  # Command history size (50 commands)
    'NumberOfHistoryBuffers' = 0x4  # Number of history buffers (4)
    'QuickEdit' = 0x1           # Enable QuickEdit mode
    'InsertMode' = 0x1          # Enable insert mode
    'WindowSize' = 0x00190050   # Window size (80x25)
    'ScreenBufferSize' = 0x012c0050  # Screen buffer size (80x300)
    'FaceName' = 'Consolas'     # Font name (must be string type)
}

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    $colors = @{
        "Red" = "DarkRed"
        "Green" = "DarkGreen" 
        "Yellow" = "DarkYellow"
        "Blue" = "DarkBlue"
        "Cyan" = "DarkCyan"
        "White" = "White"
    }
    
    Write-Host $Message -ForegroundColor $colors[$Color]
}

function Test-AdminRights {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Backup-CurrentSettings {
    param([string]$BackupPath)
    
    try {
        $regPath = "HKCU:\Console"
        if (Test-Path $regPath) {
            Write-ColoredOutput "Creating backup of current CMD settings..." "Yellow"
            
            $currentSettings = @{}
            $allKeys = ($ThemeColors.Keys + $ThemeSettings.Keys) | Sort-Object | Get-Unique
            
            foreach ($key in $allKeys) {
                try {
                    $value = Get-ItemProperty -Path $regPath -Name $key -ErrorAction SilentlyContinue
                    if ($value) {
                        $currentSettings[$key] = $value.$key
                    }
                } catch {
                    # Key doesn't exist, skip it
                }
            }
            
            $backup = @{
                'timestamp' = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                'settings' = $currentSettings
            }
            
            $backup | ConvertTo-Json -Depth 3 | Out-File -FilePath $BackupPath -Encoding UTF8
            Write-ColoredOutput "✓ Backup saved to: $BackupPath" "Green"
            return $true
        }
    } catch {
        Write-ColoredOutput "✗ Failed to create backup: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Apply-ThemeSettings {
    try {
        $regPath = "HKCU:\Console"
        
        # Ensure the registry path exists
        if (-not (Test-Path $regPath)) {
            Write-ColoredOutput "Creating Console registry path..." "Yellow"
            New-Item -Path $regPath -Force | Out-Null
        }

        Write-ColoredOutput "Applying Academic Apex theme colors..." "Cyan"
        
        # Apply color table
        foreach ($colorKey in $ThemeColors.Keys) {
            try {
                Set-ItemProperty -Path $regPath -Name $colorKey -Value $ThemeColors[$colorKey] -Type DWord -Force
                Write-ColoredOutput "  ✓ Applied $colorKey" "Green"
            } catch {
                Write-ColoredOutput "  ✗ Failed to apply $colorKey : $($_.Exception.Message)" "Red"
            }
        }

        Write-ColoredOutput "Applying theme settings..." "Cyan"
        
        # Apply other settings
        foreach ($settingKey in $ThemeSettings.Keys) {
            try {
                if ($settingKey -eq 'FaceName') {
                    Set-ItemProperty -Path $regPath -Name $settingKey -Value $ThemeSettings[$settingKey] -Type String -Force
                } else {
                    Set-ItemProperty -Path $regPath -Name $settingKey -Value $ThemeSettings[$settingKey] -Type DWord -Force
                }
                Write-ColoredOutput "  ✓ Applied $settingKey" "Green"
            } catch {
                Write-ColoredOutput "  ✗ Failed to apply $settingKey : $($_.Exception.Message)" "Red"
            }
        }

        return $true
    } catch {
        Write-ColoredOutput "✗ Critical error applying theme: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Show-ThemeInfo {
    Write-ColoredOutput @"

╔══════════════════════════════════════════════════════════════╗
║                    Academic Apex CMD Theme                   ║
║                      Application Script                      ║
╚══════════════════════════════════════════════════════════════╝

This script will apply the Academic Apex color scheme and 
settings to your Windows Command Prompt.

Theme Features:
• Dark background with professional color scheme
• Syntax highlighting colors for better readability  
• Optimized font settings (Consolas 12pt)
• Enhanced cursor and window configuration
• QuickEdit mode enabled for better usability

"@ "White"
}

# Main execution
try {
    Show-ThemeInfo
    
    # Check if running as administrator (recommended but not required for user settings)
    if (-not (Test-AdminRights)) {
        Write-ColoredOutput "⚠ Warning: Not running as administrator" "Yellow"
        Write-ColoredOutput "  The script can still modify user-specific CMD settings." "Yellow"
        Write-ColoredOutput "  For system-wide changes, run as administrator." "Yellow"
        Write-ColoredOutput ""
    }

    # Create backup if requested
    if ($Backup) {
        $backupFile = Join-Path $PWD "cmd-theme-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
        if (-not (Backup-CurrentSettings -BackupPath $backupFile)) {
            if (-not $Force) {
                Write-ColoredOutput "Backup failed. Use -Force to continue anyway." "Red"
                exit 1
            }
        }
    }

    # Apply the theme
    Write-ColoredOutput "Starting theme application..." "Cyan"
    
    if (Apply-ThemeSettings) {
        Write-ColoredOutput @"

✅ Academic Apex theme applied successfully!

Next Steps:
1. Close any open Command Prompt windows
2. Open a new Command Prompt to see the changes
3. The theme will now be applied to all new CMD windows

Theme Colors Applied:
• Background: Dark (#1a1a1a)
• Primary Text: White (#ffffff) 
• Accent: Blue (#4a9eff)
• Success: Green (#4caf50)
• Warning: Orange (#ff9800)
• Error: Red (#f44336)

Additional Features:
• Font: Consolas 12pt
• QuickEdit enabled
• Enhanced history buffer
• Optimized window size

"@ "Green"

        # Test the configuration
        Write-ColoredOutput "Testing configuration..." "Cyan"
        $regPath = "HKCU:\Console"
        $testKey = 'ColorTable00'
        $testValue = Get-ItemProperty -Path $regPath -Name $testKey -ErrorAction SilentlyContinue
        
        if ($testValue -and $testValue.$testKey -eq $ThemeColors[$testKey]) {
            Write-ColoredOutput "✓ Configuration test passed" "Green"
        } else {
            Write-ColoredOutput "⚠ Configuration test failed - theme may not be fully applied" "Yellow"
        }

    } else {
        Write-ColoredOutput @"

❌ Theme application failed!

Possible solutions:
• Run the script as Administrator
• Check if Console registry key is accessible
• Use -Force parameter to ignore non-critical errors
• Try running: Get-Help .\apply-cmd-theme.ps1 -Full

"@ "Red"
        exit 1
    }

} catch {
    Write-ColoredOutput "💥 Unexpected error occurred:" "Red"
    Write-ColoredOutput $_.Exception.Message "Red"
    Write-ColoredOutput $_.ScriptStackTrace "Red"
    exit 1
}

# Success exit
Write-ColoredOutput "🎉 Academic Apex CMD theme setup complete!" "Green"
exit 0
