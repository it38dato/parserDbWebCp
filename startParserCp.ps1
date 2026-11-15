if ($Host.UI.RawUI.BufferSize) {
    $Host.UI.RawUI.BufferSize = New-Object System.Management.Automation.Host.Size(3000, $Host.UI.RawUI.BufferSize.Height)
}

#$project = "parserCp"
$project = Split-Path -Path $PSScriptRoot -Leaf
#$envProject = "envParserWeb"
$userProfile = $env:USERPROFILE

$configPath = Join-Path -Path $PSScriptRoot -ChildPath "config.json"
$envProject = $null
if (Test-Path $configPath) {
    # Читаем json и превращаем в объект, затем берем свойство VENVPATH1
    $config = Get-Content -Raw -Path $configPath | ConvertFrom-Json
    $envProject = $config.VENVPATH1
}
# Проверяем, что значение успешно загрузилось
if ([string]::IsNullOrWhiteSpace($envProject)) {
    Write-Error "- Critical error: Variable VENVPATH1 not found in the config.json file or the file is missing!"
    exit 1
}
#Write "Venv Folder $envProject"
$dirNetPath = $null
if (Test-Path $configPath) {
    # Читаем json и превращаем в объект, затем берем свойство LINKNETPATH1
    $config = Get-Content -Raw -Path $configPath | ConvertFrom-Json
    $dirNetPath = $config.LINKNETPATH1
}
# Проверяем, что значение успешно загрузилось
if ([string]::IsNullOrWhiteSpace($dirNetPath)) {
    Write-Error "- Critical error: Variable LINKNETPATH1 not found in the config.json file or the file is missing!"
    exit 1
}
#Write "Venv Folder $dirNetPath"

$envPath = Join-Path -Path $PSScriptRoot -ChildPath ".env"
$D1 = $null
if (Test-Path $envPath) {
    # Находим строку, начинающуюся строго с D1= (игнорируя пробелы)
    $envMatch = Get-Content $envPath | Where-Object { $_ -match '^D1\s*=' }
    if ($envMatch) {
        # Извлекаем значение после знака "=" и очищаем от возможных кавычек и пробелов
        $D1 = $envMatch.Split('=', 2)[1].Trim() -replace "['`"]", ""
    }
}
# Если переменная D1 не найдена или пустая — останавливаем скрипт
if ([string]::IsNullOrWhiteSpace($D1)) {
    Write-Error "- Critical error: Variable D1 not found in the .env file or the file is missing! The script has stopped working."
    exit 1
}
$networkPath = "\\$D1\$dirNetPath"
#Write "Network Folder $networkPath"

# 1. Используем интерполяцию строк (переменные внутри двойных кавычек) для задания пути транскрипта
$logName = "outShellScript_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
$logFullPath = "$userProfile\$project\$logName"
Start-Transcript -Path $logFullPath

# 2. Активация виртуального окружения с использованием оператора dot sourcing (точки и пробела)
# Это гарантирует, что окружение активируется в текущей сессии PowerShell
cd "$userProfile\$envProject\Scripts\"
. .\Activate.ps1
cd "$userProfile\$project"
python parserCes.py
deactivate

# 6. Остановка транскрипта
Stop-Transcript

# 7. Перемещение файлов в сетевую папку
#if (Test-Path $networkPath) {
    # Перемещаем .csv, .png и сторонние логи outShellScript_*.txt / *.log
#    Get-ChildItem -Path ".\*" -Include "*.png", "*.jpeg" |
#        Where-Object { $_.FullName -ne $logFullPath } |
#        Move-Item -Destination $networkPath -Force
    # Перемещаем сам файл текущего лога, который только что закрылся
#    if (Test-Path $logFullPath) {
#        Move-Item -Path $logFullPath -Destination $networkPath -Force
#    }
#} else {
#    Write-Warning "Network folder $networkPath unavailable. The files were not moved."
#}