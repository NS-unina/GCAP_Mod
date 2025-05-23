# Initialize variables
$architecture = ""
$rules = ""
$output = ""
$showHelp = $false

# Parse command-line arguments manually
for ($i = 0; $i -lt $args.Length; $i++) {
    switch ($args[$i]) {
        "-a" { $architecture = $args[$i + 1]; $i++ }
        "--architecture" { $architecture = $args[$i + 1]; $i++ }
        "-r" { $rules = $args[$i + 1]; $i++ }
        "--rules" { $rules = $args[$i + 1]; $i++ }
        "-o" { $output = $args[$i + 1]; $i++ }
        "--output" { $output = $args[$i + 1]; $i++ }
        "-h" { $showHelp = $true }
        "--help" { $showHelp = $true }
        default {
            Write-Host "Unknown argument: $($args[$i])"
            $showHelp = $true
        }
    }
}

if ($showHelp -or !$architecture -or !$rules -or !$output) {
    Write-Host "Usage: .\genScript.ps1 -a <architecture> -r <rules> -o <output>"
    exit 1
}

Write-Host "Architecture file: $architecture"
Write-Host "Rules file: $rules"
Write-Host "Output directory: $output"

# Check if output directory exists
if (Test-Path $output) {
    $response = Read-Host "The directory '$output' already exists. Do you want to delete it? (y/n)"
    if ($response -eq 'y') {
        Remove-Item -Recurse -Force $output
        Write-Host "Directory '$output' deleted."
    } else {
        Write-Host "Exiting script without creating or deleting the directory."
        exit 0
    }
}

# Create output directory
New-Item -ItemType Directory -Path $output | Out-Null

# Build full absolute path for volume mapping
$fullOutputPath = (Resolve-Path $output).Path

# Run Docker commands
docker run -ti --name mulval -v "${fullOutputPath}:/input" -d --rm wilbercui/mulval bash -c "tail -f /dev/null"
docker cp $architecture mulval:/input
docker cp $rules mulval:/input
docker exec mulval bash -c "graph_gen.sh $architecture -v -p -r $rules --nometric"
docker stop mulval