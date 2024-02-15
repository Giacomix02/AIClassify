# Check if 'python' is in the system path
$pythonLocation = Get-Command python -ErrorAction SilentlyContinue

$pythonLocationPath = $pythonLocation.Path

# remove from pythonLocationPath the string 'python.exe'
$pythonLocationPath1 = $pythonLocationPath.Replace("\python.exe", "")



if ($pythonLocation) {

    Write-Host "Python executable found at: $($pythonLocationPath1)"
} else {
    Write-Host "Python not found in the system path."
}


# Specify the file path
$filePath = "./ai/pyvenv.cfg"

# Specify the content
$fileContent = @"
home = $pythonLocationPath1
include-system-site-packages = false
version = 3.10.0
"@

# Write content to the file
$fileContent | Out-File -FilePath $filePath -Encoding UTF8

Write-Host "File 'pyvenv.cfg' created successfully with the specified content."




# Read-Host -Prompt "Press Enter to continue"



###################################################################




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