# Define the Activate-VirtualEnvironment function
function Activate-VirtualEnvironment {
    param (
        [string]$Path
    )

    # Construct the path to the activate script based on the operating system
    $activateScript = if ($env:OS -eq "Windows_NT") {
        Join-Path $Path "Scripts\Activate"
    } else {
        Join-Path $Path "bin\activate"
    }

    # Activate the virtual environment
    if (Test-Path $activateScript) {
        & $activateScript
    } else {
        Write-Host "Virtual environment activation script not found."
    }
}

# Specify the path to your Python virtual environment
$venvPath = "./ai/"

# Specify the path to your Python script
$pythonScriptPath = "./ai/src/bottle_server.py"

# Activate the Python virtual environment
Activate-VirtualEnvironment -Path $venvPath

# Run the Python script
python $pythonScriptPath

# Pause to keep the console window open
Read-Host -Prompt "Press Enter to exit"