# Check if 'python' is in the system path
$pythonLocation = Get-Command python -ErrorAction SilentlyContinue

$pythonLocationPath = $pythonLocation.Path

# remove from pythonLocationPath the string 'python.exe'
$pythonLocationPath1 = $pythonLocationPath.Replace("\python.exe", " ")



if ($pythonLocation) {

    Write-Host "Python executable found at: $($pythonLocationPath1)"
} else {
    Write-Host "Python not found in the system path."
}

Read-Host -Prompt "Press Enter to exit"


# Specify the file path
$filePath = "pyvenv.cfg"

# Specify the content
$fileContent = @"
home = $pythonLocationPath1
include-system-site-packages = false
version = 3.10.0
"@

# Write content to the file
$fileContent | Out-File -FilePath $filePath -Encoding UTF8

Write-Host "File 'pyvenv.cfg' created successfully with the specified content."